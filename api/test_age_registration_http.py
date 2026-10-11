"""Registration safeguarding using isolated PostgreSQL and real HTTP routes."""
import os
import uuid
import pytest


@pytest.mark.integration
def test_age_gated_registration_and_login():
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.skip("TEST_DATABASE_URL required")
    from sqlalchemy.engine import make_url
    parsed = make_url(url)
    if (parsed.database != "educyber_test" or parsed.host not in ("localhost", "127.0.0.1")
            or not parsed.drivername.startswith("postgresql")
            or os.getenv("DATABASE_URL") != url):
        pytest.fail("Refusing to run outside isolated PostgreSQL test database")
    from fastapi.testclient import TestClient
    from sqlalchemy import create_engine, delete, select
    from sqlalchemy.orm import Session
    from main import app
    from models import AuthSession, User

    engine = create_engine(url)
    ids = []
    with TestClient(app) as client:
        try:
            for dob, expected in (("2018-01-01", 403), ("2010-01-01", 201),
                                  ("1995-01-01", 201)):
                email = f"age-test-{uuid.uuid4().hex}@example.com"
                payload = {"full_name": "Age Test", "email": email,
                           "password": "long-test-only-password", "date_of_birth": dob,
                           "role": "student"}
                response = client.post("/api/v1/auth/register", json=payload)
                assert response.status_code == expected, response.text
                with Session(engine) as db:
                    user = db.scalar(select(User).where(User.email == email))
                    if expected == 403:
                        assert user is None
                        continue
                    assert user is not None
                    ids.append(user.id)
                    assert user.date_of_birth.isoformat() == dob
                    assert user.guardian_consent_verified is False
                    assert "date_of_birth" not in response.json()["user"]
                    assert "guardian_consent_verified" not in response.json()["user"]
                    assert user.is_active == (dob == "1995-01-01")
                    assert user.age_band == ("adult" if user.is_active else "minor")
                login = client.post("/api/v1/auth/login", json={
                    "email": email, "password": payload["password"]})
                assert login.status_code == (200 if dob == "1995-01-01" else 401)
        finally:
            with Session(engine) as db:
                for user_id in ids:
                    db.execute(delete(AuthSession).where(AuthSession.user_id == user_id))
                    db.execute(delete(User).where(User.id == user_id))
                db.commit()
            engine.dispose()
