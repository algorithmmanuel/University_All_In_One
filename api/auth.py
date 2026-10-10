"""Database-backed bearer sessions and scrypt password hashing."""
import hashlib
import hmac
import os
import secrets
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from database import SessionLocal
from models import AuthSession, User

bearer = HTTPBearer(auto_error=False)

def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=16384, r=8, p=1)
    return "scrypt$16384$8$1$" + salt.hex() + "$" + digest.hex()

def verify_password(password: str, stored: str) -> bool:
    try:
        algorithm, n, r, p, salt_hex, digest_hex = stored.split("$")
        if algorithm != "scrypt":
            return False
        digest = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt_hex), n=int(n), r=int(r), p=int(p))
        return hmac.compare_digest(digest, bytes.fromhex(digest_hex))
    except (ValueError, TypeError):
        return False

def issue_session(db, user: User) -> str:
    token = secrets.token_urlsafe(48)
    db.add(AuthSession(user_id=user.id, token_hash=hashlib.sha256(token.encode()).hexdigest(),
                       expires_at=datetime.now(timezone.utc) + timedelta(hours=12)))
    db.commit()
    return token

def current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)) -> User:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    digest = hashlib.sha256(credentials.credentials.encode()).hexdigest()
    with SessionLocal() as db:
        session = db.scalar(select(AuthSession).where(AuthSession.token_hash == digest))
        if session is None or session.expires_at.replace(tzinfo=timezone.utc) <= datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Session expired or invalid")
        user = db.get(User, session.user_id)
        if user is None or not user.is_active:
            raise HTTPException(status_code=401, detail="Account unavailable")
        db.expunge(user)
        return user

def require_teacher(user: User = Depends(current_user)) -> User:
    if user.role not in ("teacher", "admin") or (user.role == "teacher" and not user.is_approved):
        raise HTTPException(status_code=403, detail="Approved teacher access required")
    return user
