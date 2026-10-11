"""Authentication lifecycle and authorization regression tests.

These tests use fake database sessions: no user records are created or modified.
The auth module requires DATABASE_URL during import, so integration tests are
skipped unless the isolated local PostgreSQL test URL is configured.
"""
import os
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest


@pytest.fixture
def auth_module(monkeypatch):
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.skip("Set TEST_DATABASE_URL for authentication integration tests")
    from sqlalchemy.engine import make_url
    parsed = make_url(url)
    if (not parsed.drivername.startswith("postgresql")
            or parsed.database != "educyber_test"
            or parsed.host not in ("127.0.0.1", "localhost")):
        pytest.fail("Authentication tests require local PostgreSQL educyber_test")
    existing = os.getenv("DATABASE_URL")
    if existing and existing != url:
        pytest.fail("DATABASE_URL must match TEST_DATABASE_URL")
    monkeypatch.setenv("DATABASE_URL", url)
    import auth
    return auth


class FakeSession:
    def __init__(self, session_record, user):
        self.session_record = session_record
        self.user = user

    def scalar(self, statement):
        return self.session_record

    def get(self, model, identifier):
        return self.user


def credentials(token="test-token"):
    from fastapi.security import HTTPAuthorizationCredentials
    return HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)


def expect_http_status(code, callback):
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as error:
        callback()
    assert error.value.status_code == code


def test_missing_bearer_is_rejected(auth_module):
    expect_http_status(401, lambda: auth_module.current_user(None))


@pytest.mark.parametrize("expiry,active,expected", [
    (-1, True, 401),
    (1, False, 401),
    (1, True, 200),
])
def test_session_expiry_and_inactive_account(auth_module, expiry, active, expected):
    record = SimpleNamespace(
        user_id=42,
        expires_at=datetime.now(timezone.utc) + timedelta(hours=expiry),
    )
    user = SimpleNamespace(id=42, is_active=active, role="student", is_approved=True)
    db = FakeSession(record, user)
    if expected == 200:
        assert auth_module.current_user(credentials(), db=db) is user
    else:
        expect_http_status(expected, lambda: auth_module.current_user(credentials(), db=db))


def test_revoked_session_is_rejected(auth_module):
    db = FakeSession(None, None)
    expect_http_status(401, lambda: auth_module.current_user(credentials(), db=db))


@pytest.mark.parametrize("role,approved,expected", [
    ("student", True, 403),
    ("teacher", False, 403),
    ("teacher", True, 200),
    ("admin", False, 200),
])
def test_teacher_authorization(auth_module, role, approved, expected):
    user = SimpleNamespace(role=role, is_approved=approved)
    if expected == 200:
        assert auth_module.require_teacher(user) is user
    else:
        expect_http_status(expected, lambda: auth_module.require_teacher(user))
