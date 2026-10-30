"""Isolated password recovery integration tests; never call the real email provider."""
import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone

import pytest


@pytest.mark.integration
def test_password_reset_lifecycle(monkeypatch):
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.skip("Set TEST_DATABASE_URL")
    from sqlalchemy.engine import make_url
    target = make_url(url)
    if (target.database != "educyber_test" or target.host not in ("localhost", "127.0.0.1")
            or target.port != 5434 or os.environ.get("DATABASE_URL") != url):
        pytest.fail("Refusing to run against any non-isolated database")

    from fastapi.testclient import TestClient
    from sqlalchemy import delete, select
    from database import SessionLocal
    from main import app
    from models import AuthSession, LoginAttemptBucket, PasswordResetToken, User
    from auth import hash_password

    monkeypatch.setenv("BREVO_API_KEY", "test-only")
    monkeypatch.setenv("EDUCYBER_EMAIL_SENDER", "noreply@example.com")
    monkeypatch.setenv("EDUCYBER_PUBLIC_WEB_URL", "http://localhost:3000")
    sent_links = []
    monkeypatch.setattr("password_recovery._send_reset_email",
                        lambda email, link, key, sender: sent_links.append(link))
    email = f"recovery-{secrets.token_hex(12)}@example.com"
    old_password = "Initial-Password-" + secrets.token_urlsafe(18)
    new_password = "Replacement-Password-" + secrets.token_urlsafe(18)
    user_id = None
    try:
        with SessionLocal.begin() as db:
            user = User(full_name="Password Recovery Test", email=email,
                        password_hash=hash_password(old_password),
                        date_of_birth=datetime(1995, 1, 1).date(),
                        age_band="adult", guardian_consent_verified=False,
                        role="student", is_active=True, is_approved=True)
            db.add(user)
            db.flush()
            user_id = user.id
            db.add(AuthSession(user_id=user_id, token_hash=hashlib.sha256(secrets.token_bytes(32)).hexdigest(),
                               expires_at=datetime.now(timezone.utc) + timedelta(hours=1)))

        with TestClient(app) as client:
            # Nonexistent users get the exact same response and no message.
            missing = client.post("/api/v1/auth/forgot-password",
                                  json={"email": "missing-" + email})
            known = client.post("/api/v1/auth/forgot-password", json={"email": email})
            assert missing.status_code == known.status_code == 202
            assert missing.json() == known.json()
            assert len(sent_links) == 1
            from urllib.parse import urlsplit, parse_qs
            token = parse_qs(urlsplit(sent_links[0]).query)["token"][0]

            # Wrong token, then correct token, then replay.
            wrong = client.post("/api/v1/auth/reset-password",
                                json={"token": secrets.token_urlsafe(48), "password": new_password})
            assert wrong.status_code == 400
            changed = client.post("/api/v1/auth/reset-password",
                                  json={"token": token, "password": new_password})
            assert changed.status_code == 200
            with SessionLocal() as db:
                assert db.scalar(select(AuthSession).where(AuthSession.user_id == user_id)) is None
            reused = client.post("/api/v1/auth/reset-password",
                                 json={"token": token, "password": new_password})
            assert reused.status_code == 400

            old_login = client.post("/api/v1/auth/login",
                                    json={"email": email, "password": old_password})
            assert old_login.status_code == 401
            # Private beta requires an invitation for login. The password
            # itself must verify after reset; check using the same hash verifier.
            from auth import verify_password
            with SessionLocal() as db:
                current = db.get(User, user_id)
                assert verify_password(new_password, current.password_hash)
                assert not verify_password(old_password, current.password_hash)

            # Explicitly expire a fresh token and verify expiry enforcement.
            expired = secrets.token_urlsafe(48)
            with SessionLocal.begin() as db:
                db.add(PasswordResetToken(
                    user_id=user_id, token_hash=hashlib.sha256(expired.encode()).hexdigest(),
                    expires_at=datetime.now(timezone.utc) - timedelta(seconds=1)))
            response = client.post("/api/v1/auth/reset-password",
                                   json={"token": expired, "password": new_password})
            assert response.status_code == 400
    finally:
        with SessionLocal.begin() as db:
            if user_id is not None:
                db.execute(delete(AuthSession).where(AuthSession.user_id == user_id))
                db.execute(delete(PasswordResetToken).where(PasswordResetToken.user_id == user_id))
                db.execute(delete(User).where(User.id == user_id))
            for identifier in (email, "missing-" + email):
                for purpose in ("password_reset:", ""):
                    key = hashlib.sha256((purpose + identifier).encode()).hexdigest()
                    db.execute(delete(LoginAttemptBucket).where(LoginAttemptBucket.key_hash == key))
