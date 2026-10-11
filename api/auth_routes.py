"""Registration, login and protected dashboard endpoints."""
import hashlib
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from auth import bearer, current_user, hash_password, issue_session, require_teacher, verify_password
from database import SessionLocal
from models import AuthSession, User
from login_limiter import record_attempt, clear_attempts

router = APIRouter(prefix="/api/v1", tags=["authentication"])

def get_db():
    with SessionLocal() as db:
        yield db

class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)
    role: str = "student"

class LoginRequest(BaseModel):
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
    email = str(body.email).strip().lower()
    if db.scalar(select(User.id).where(User.email == email)) is not None:
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(full_name=body.full_name.strip(), email=email,
                password_hash=hash_password(body.password), role=body.role,
                is_approved=(body.role == "student"))
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already registered")
    db.refresh(user)
    return {"user": public_user(user), "message": "Teacher approval pending" if body.role == "teacher" else "Account created"}

@router.post("/auth/login")
def login(body: LoginRequest, db: Session = Depends(get_db)):
    email = str(body.email).strip().lower()
    record_attempt(db, email)
    user = db.scalar(select(User).where(User.email == email))
    if user is None or not verify_password(body.password, user.password_hash) or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = issue_session(db, user)
    clear_attempts(db, email)
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
    return {"message": "Signed out"}

@router.get("/dashboard")
def dashboard(user: User = Depends(current_user)):
    return {"user": public_user(user), "dashboard": "teacher" if user.role == "teacher" and user.is_approved else "student" if user.role == "student" else "pending"}

@router.get("/teacher/dashboard")
def teacher_dashboard(user: User = Depends(require_teacher)):
    return {"message": "Teacher workspace", "user": public_user(user)}
