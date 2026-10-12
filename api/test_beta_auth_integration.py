"""Private-beta authentication integration regressions.

Run only against the isolated local PostgreSQL test database:
    TEST_DATABASE_URL=postgresql+psycopg://...@127.0.0.1:5434/educyber_test
    DATABASE_URL=$TEST_DATABASE_URL
    pytest -q test_beta_auth_integration.py

Tests create their own invitations and users and remove them afterward. They
never use the main beta database, real invitations or real passwords.
"""
import hashlib
import os
import secrets
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

import pytest


@pytest.fixture(scope="module")
def isolated_app():
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.skip("Set TEST_DATABASE_URL to the isolated PostgreSQL test database")
    from sqlalchemy.engine import make_url
    parsed = make_url(url)
    if (not parsed.drivername.startswith("postgresql")
            or parsed.database != "educyber_test"
            or parsed.host not in ("127.0.0.1", "localhost")
            or os.getenv("DATABASE_URL") != url):
        pytest.fail("Refusing authentication integration tests outside the isolated test database")
    # Import the application only after confirming the database isolation.
    from fastapi.testclient import TestClient
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from database import Base
    from main import app
    from models import AuthSession, BetaInvite, LoginAttemptBucket, User
    engine = create_engine(url, pool_pre_ping=True)
    Base.metadata.create_all(engine)
    yield app, TestClient, sessionmaker(bind=engine), (AuthSession, BetaInvite, LoginAttemptBucket, User)
    engine.dispose()


@pytest.mark.integration
def test_private_beta_registration_login_and_independent_sessions(isolated_app, monkeypatch):
    app, TestClient, Session, models = isolated_app
    AuthSession, BetaInvite, LoginAttemptBucket, User = models
    monkeypatch.setenv("EDUCYBER_PRIVATE_BETA", "enabled")
    # Randomized credentials avoid collisions with other test runs.
    accounts = []
    invites = []
    tokens = []
    try:
        with Session.begin() as db:
            for _ in range(2):
                code = secrets.token_urlsafe(32)
                invite = BetaInvite(
                    code_hash=hashlib.sha256(code.encode()).hexdigest(),
                    expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
                )
                db.add(invite)
                invites.append((invite, code))

        def register_and_login(index):
            invite, code = invites[index]
            email = f"beta-auth-{secrets.token_hex(12)}@example.com"
            password = "StrongTest-" + secrets.token_urlsafe(24)
            with TestClient(app) as client:
                registration = client.post("/api/v1/auth/register", json={
                    "full_name": "Isolated Beta Test",
                    "email": email.upper(),
                    "password": password,
                    "date_of_birth": "1995-01-01",
                    "role": "student",
                    "beta_invite": code,
                })
                assert registration.status_code == 201, registration.status_code
                user_id = registration.json()["user"]["id"]
                login = client.post("/api/v1/auth/login", json={
                    "email": email,
                    "password": password,
                })
                assert login.status_code == 200, login.status_code
                token = login.json()["access_token"]
                dashboard = client.get("/api/v1/dashboard", headers={"Authorization": f"Bearer {token}"})
                assert dashboard.status_code == 200
                assert dashboard.json()["user"]["id"] == user_id
                wrong = client.post("/api/v1/auth/login", json={
                    "email": email, "password": password + "-wrong",
                })
                assert wrong.status_code == 401
                return user_id, token

        # Simultaneous registrations and logins must not interfere.
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(register_and_login, range(2)))
        accounts.extend(user_id for user_id, _ in results)
        tokens.extend(token for _, token in results)
        assert accounts[0] != accounts[1]
        with TestClient(app) as client:
            for user_id, token in results:
                response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
                assert response.status_code == 200
                assert response.json()["user"]["id"] == user_id
    finally:
        # Cleanup even when an assertion fails; invitations are detached first.
        from sqlalchemy import delete, update
        with Session.begin() as db:
            ids = [invite.id for invite, _ in invites]
            if ids:
                db.execute(update(BetaInvite).where(BetaInvite.id.in_(ids)).values(redeemed_by=None))
            if accounts:
                db.execute(delete(AuthSession).where(AuthSession.user_id.in_(accounts)))
                db.execute(delete(User).where(User.id.in_(accounts)))
            if ids:
                db.execute(delete(BetaInvite).where(BetaInvite.id.in_(ids)))
            # Login limiter buckets are keyed by normalized email; clean only
            # identifiers created by this test when those are available.
