"""Password recovery with Brevo delivery and single-use stored SHA-256 tokens.

Secrets, emails and reset links must never be logged. This module intentionally
keeps email-provider integration separate from the authentication routes.
"""
import hashlib
import json
import logging
import os
import secrets
from datetime import datetime, timedelta, timezone
from urllib.error import URLError
from urllib.parse import quote, urlsplit, urlunsplit
from urllib.request import Request, urlopen

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from auth import hash_password
from db_dependencies import get_db
from login_limiter import record_attempt
from models import AuthSession, PasswordResetToken, User

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])
logger = logging.getLogger("educyber.password_recovery")
TTL = timedelta(minutes=20)
GENERIC_MESSAGE = "If the account exists, a password reset email will be sent."
MAX_PENDING = 3


class ForgotPasswordRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(min_length=32, max_length=200)
    password: str = Field(min_length=12, max_length=128)


def _configuration():
    """Validate delivery settings without revealing secrets in errors."""
    api_key = os.getenv("BREVO_API_KEY")
    sender = os.getenv("EDUCYBER_EMAIL_SENDER")
    base = os.getenv("EDUCYBER_PUBLIC_WEB_URL", "").rstrip("/")
    parts = urlsplit(base)
    is_local = parts.hostname in ("localhost", "127.0.0.1")
    if (not api_key or not sender or not base or parts.username or parts.password
            or parts.query or parts.fragment or parts.path not in ("", "/")
            or (parts.scheme != "https" and not (is_local and parts.scheme == "http"))):
        raise RuntimeError("Password recovery email configuration is unavailable")
    return api_key, sender, base


def _send_reset_email(email: str, reset_url: str, api_key: str, sender: str):
    """Brevo HTTPS transactional email API; no credential values in logs."""
    payload = {
        "sender": {"email": sender},
        "to": [{"email": email}],
        "subject": "Reset your EduCyber Nigeria password",
        "textContent": (
            "A password reset was requested for your EduCyber Nigeria account.\n\n"
            f"Use this link within 20 minutes: {reset_url}\n\n"
            "If you did not request this, ignore this email."
        ),
    }
    request = Request(
        "https://api.brevo.com/v3/smtp/email",
        data=json.dumps(payload).encode("utf-8"),
        headers={"api-key": api_key, "Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=10) as response:
        if response.status not in (200, 201, 202):
            raise URLError("Mail provider rejected request")


@router.post("/forgot-password", status_code=202)
def forgot_password(body: ForgotPasswordRequest, db: Session = Depends(get_db)):
    # Fail closed before creating tokens if email delivery is not configured.
    try:
        api_key, sender, base = _configuration()
    except RuntimeError:
        raise HTTPException(status_code=503, detail="Password recovery is temporarily unavailable") from None

    email = str(body.email).strip().lower()
    # Shared PostgreSQL throttle across workers; also add edge IP quotas.
    record_attempt(db, email, purpose="password_reset")
    user = db.scalar(select(User).where(User.email == email))
    if user is None or not user.is_active:
        return {"message": GENERIC_MESSAGE}

    now = datetime.now(timezone.utc)
    db.execute(delete(PasswordResetToken).where(
        PasswordResetToken.user_id == user.id,
        PasswordResetToken.expires_at <= now,
    ))
    pending = db.scalars(
        select(PasswordResetToken).where(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.used_at.is_(None),
            PasswordResetToken.expires_at > now,
        ).with_for_update()
    ).all()
    if len(pending) >= MAX_PENDING:
        db.commit()
        return {"message": GENERIC_MESSAGE}

    token = secrets.token_urlsafe(48)
    record = PasswordResetToken(
        user_id=user.id,
        token_hash=hashlib.sha256(token.encode()).hexdigest(),
        expires_at=now + TTL,
    )
    db.add(record)
    db.commit()
    reset_url = base + "/reset-password?token=" + quote(token, safe="")
    try:
        _send_reset_email(email, reset_url, api_key, sender)
    except (URLError, OSError, ValueError, TimeoutError):
        db.delete(record)
        db.commit()
        logger.warning("password_reset_delivery_failed")
    return {"message": GENERIC_MESSAGE}


@router.post("/reset-password")
def reset_password(body: ResetPasswordRequest, db: Session = Depends(get_db)):
    digest = hashlib.sha256(body.token.encode("utf-8")).hexdigest()
    record = db.scalar(
        select(PasswordResetToken).where(PasswordResetToken.token_hash == digest).with_for_update()
    )
    now = datetime.now(timezone.utc)
    if record is None or record.used_at is not None or record.expires_at <= now:
        raise HTTPException(status_code=400, detail="Reset link is invalid or expired")

    user = db.get(User, record.user_id, with_for_update=True)
    if user is None or not user.is_active:
        raise HTTPException(status_code=400, detail="Reset link is invalid or expired")

    user.password_hash = hash_password(body.password)
    record.used_at = now
    # End all existing sessions so an attacker with a stolen session loses access.
    db.execute(delete(AuthSession).where(AuthSession.user_id == user.id))
    db.commit()
    logger.info("password_reset_completed")
    return {"message": "Password updated. Please sign in with your new password."}
