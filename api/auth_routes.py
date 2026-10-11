"""Registration, login and protected dashboard endpoints."""
import hashlib
import os
from datetime import datetime, timezone
from datetime import date
from age_policy import registration_policy
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from auth import bearer, current_user, hash_password, issue_session, require_teacher, verify_password
from db_dependencies import get_db
from models import AuthSession, User, BetaInvite
from login_limiter import record_attempt, clear_attempts
from security_events import emit_security_event

router = APIRouter(prefix="/api/v1", tags=["authentication"])

class RegisterRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)
    date_of_birth: date
    role: str = "student"
    beta_invite: str | None = Field(default=None, min_length=16, max_length=160)

class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr
    # Align API input validation with the password hashing module's 1024-byte limit.
    password: str = Field(max_length=1024)

def public_user(user: User):
    return {"id": user.id, "full_name": user.full_name, "email": user.email,
            "role": user.role, "is_approved": user.is_approved}

@router.post("/auth/register", status_code=201)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    if body.role not in ("student", "teacher"):
        raise HTTPException(status_code=422, detail="Choose student or teacher")
    band, active = registration_policy(body.date_of_birth, body.role)
    beta_mode = os.getenv("EDUCYBER_PRIVATE_BETA") == "enabled"
    if beta_mode and (band != "adult" or body.role != "student"):
        raise HTTPException(status_code=403, detail="Private beta is for invited adults only")
    if beta_mode and not body.beta_invite:
        raise HTTPException(status_code=403, detail="A beta invitation is required")
    email = str(body.email).strip().lower()
    # Shared registration bucket is a defense-in-depth control; edge IP quotas
    # are still required to prevent bulk signups using different addresses.
    record_attempt(db, email, purpose="registration")
    if db.scalar(select(User.id).where(User.email == email)) is not None:
        raise HTTPException(status_code=409, detail="Email already registered")
    invite = None
    if beta_mode:
        digest = hashlib.sha256(body.beta_invite.encode("utf-8")).hexdigest()
        invite = db.scalar(select(BetaInvite).where(BetaInvite.code_hash == digest).with_for_update())
        if (invite is None or invite.redeemed_by is not None or
                invite.expires_at.replace(tzinfo=timezone.utc) <= datetime.now(timezone.utc)):
            raise HTTPException(status_code=403, detail="Invalid or used beta invitation")
    user = User(full_name=body.full_name.strip(), email=email,
                password_hash=hash_password(body.password), role=body.role,
                date_of_birth=body.date_of_birth, age_band=band,
                guardian_consent_verified=False, is_active=active,
                is_approved=(body.role == "student" and active))
    db.add(user)
    try:
        db.flush()
        if invite is not None:
            invite.redeemed_by = user.id
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already registered")
    db.refresh(user)
    emit_security_event("registration_succeeded")
    message = ("Guardian consent verification required before account activation" if band == "minor"
               else "Teacher approval pending" if body.role == "teacher" else "Account created")
    return {"user": public_user(user), "message": message}

@router.post("/auth/login")
def login(body: LoginRequest, db: Session = Depends(get_db)):
    email = str(body.email).strip().lower()
    record_attempt(db, email)
    user = db.scalar(select(User).where(User.email == email))
    if user is None or not verify_password(body.password, user.password_hash) or not user.is_active:
        emit_security_event("login_failed")
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if os.getenv("EDUCYBER_PRIVATE_BETA") == "enabled" and (user.age_band != "adult" or user.role != "student"):
        raise HTTPException(status_code=403, detail="Private beta is for invited adult learners only")
    token = issue_session(db, user)
    clear_attempts(db, email)
    emit_security_event("login_succeeded")
    return {"access_token": token, "token_type": "bearer", "expires_in": 43200, "user": public_user(user)}

@router.get("/auth/me")
def me(user: User = Depends(current_user)):
    return {"user": public_user(user)}

@router.post("/auth/logout")
def logout(credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
           user: User = Depends(current_user), db: Session = Depends(get_db)):
    digest = hashlib.sha256(credentials.credentials.encode()).hexdigest()
    session = db.scalar(select(AuthSession).where(AuthSession.token_hash == digest, AuthSession.user_id == user.id))
    if session is not None:
        db.delete(session)
        db.commit()
    emit_security_event("logout_succeeded")
    return {"message": "Signed out"}

@router.get("/dashboard")
def dashboard(user: User = Depends(current_user)):
    return {"user": public_user(user), "dashboard": "teacher" if user.role == "teacher" and user.is_approved else "student" if user.role == "student" else "pending"}

@router.get("/teacher/dashboard")
def teacher_dashboard(user: User = Depends(require_teacher)):
    return {"message": "Teacher workspace", "user": public_user(user)}
