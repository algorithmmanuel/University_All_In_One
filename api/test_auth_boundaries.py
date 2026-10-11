"""Authentication request validation and access-control HTTP regressions.

Requires isolated TEST_DATABASE_URL for importing the application. No rows are
created by these validation and unauthenticated authorization checks.
"""
import os

import pytest


@pytest.mark.integration
def test_authentication_validation_and_access_boundaries():
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.skip("TEST_DATABASE_URL is required")
    from sqlalchemy.engine import make_url
    parsed = make_url(url)
    if (not parsed.drivername.startswith("postgresql")
            or parsed.database != "educyber_test"
            or parsed.host not in ("localhost", "127.0.0.1")):
        pytest.fail("Refusing to use a non-isolated database")
    if os.getenv("DATABASE_URL") not in (None, url):
        pytest.fail("DATABASE_URL differs from TEST_DATABASE_URL")
    os.environ["DATABASE_URL"] = url
    pytest.importorskip("httpx")
    from fastapi.testclient import TestClient
    from main import app

    with TestClient(app) as client:
        # Request validation must reject oversized login passwords before KDF.
        response = client.post("/api/v1/auth/login", json={
            "email": "test@example.com", "password": "x" * 1025
        })
        assert response.status_code == 422
        # Invalid email and missing fields must be rejected consistently.
        assert client.post("/api/v1/auth/login", json={
            "email": "not-an-email", "password": "valid-password"
        }).status_code == 422
        assert client.post("/api/v1/auth/login", json={
            "email": "test@example.com"
        }).status_code == 422
        # A caller without credentials cannot reach protected user resources.
        for path in ("/api/v1/auth/me", "/api/v1/teacher/dashboard",
                     "/api/v1/dashboard"):
            assert client.get(path).status_code == 401
        assert client.post("/api/v1/auth/logout").status_code == 401
        # Registration cannot choose privileged account roles.
        assert client.post("/api/v1/auth/register", json={
            "full_name": "Test Person", "email": "test@example.com",
            "password": "valid-password-123", "role": "admin"
        }).status_code == 422
