"""HTTP authentication lifecycle test against isolated local PostgreSQL.

This exercises the real login, authenticated profile and logout routes.
No production/development database may be used.
"""
import os
import uuid

import pytest


@pytest.mark.integration
def test_login_profile_logout_revokes_bearer_token():
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.skip("TEST_DATABASE_URL is required")
    from sqlalchemy.engine import make_url
    parsed = make_url(url)
    if (not parsed.drivername.startswith("postgresql")
            or parsed.database != "educyber_test"
            or parsed.host not in ("127.0.0.1", "localhost")):
        pytest.fail("Refusing to run outside local PostgreSQL educyber_test")
    existing = os.getenv("DATABASE_URL")
    if existing and existing != url:
        pytest.fail("DATABASE_URL must match TEST_DATABASE_URL")
    os.environ["DATABASE_URL"] = url

    pytest.importorskip("httpx")
    from fastapi.testclient import TestClient
    from sqlalchemy import create_engine, delete
    from sqlalchemy.orm import sessionmaker
    from database import Base
    from main import app
    from models import AuthSession, User
    from password_security import hash_password

    engine = create_engine(url, pool_pre_ping=True)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    email = f"phase8-auth-{uuid.uuid4().hex}@example.invalid"
    password = "A long test-only password 2026!"
    user_id = None
    try:
        with Session.begin() as db:
            user = User(full_name="Phase 8 Auth Test", email=email,
                        password_hash=hash_password(password), role="student",
                        is_active=True, is_approved=True)
            db.add(user)
            db.flush()
            user_id = user.id

        with TestClient(app) as client:
            wrong = client.post("/api/v1/auth/login", json={
                "email": email, "password": "incorrect-password"
            })
            assert wrong.status_code == 401
            login = client.post("/api/v1/auth/login", json={
                "email": email, "password": password
            })
            assert login.status_code == 200
            token = login.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            assert client.get("/api/v1/auth/me").status_code == 401
            profile = client.get("/api/v1/auth/me", headers=headers)
            assert profile.status_code == 200
            assert profile.json()["user"]["email"] == email
            logout = client.post("/api/v1/auth/logout", headers=headers)
            assert logout.status_code == 200
            assert client.get("/api/v1/auth/me", headers=headers).status_code == 401
    finally:
        if user_id is not None:
            with Session.begin() as db:
                db.execute(delete(AuthSession).where(AuthSession.user_id == user_id))
                db.execute(delete(User).where(User.id == user_id))
        engine.dispose()
