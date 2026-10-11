"""Database-independent API input and deployment configuration regressions."""
import os
import pytest

# Import schemas without opening a connection. CI has no PostgreSQL service.
os.environ.setdefault("DATABASE_URL", "postgresql+psycopg://test:test@127.0.0.1:5433/educyber_test")
from pydantic import ValidationError

from auth_routes import LoginRequest, RegisterRequest
from mission_routes import Decision
from quiz_routes import Submission
from main import configured_origins


@pytest.mark.parametrize("schema,payload", [
    (LoginRequest, {"email": "a@example.com", "password": "x", "is_admin": True}),
    (RegisterRequest, {"full_name": "Valid Name", "email": "a@example.com",
                       "password": "correct-password", "role": "student", "is_approved": True}),
    (Decision, {"option_index": 0, "expected_step": 0, "score": 9999}),
    (Submission, {"answers": {1: 0}, "score": 100}),
])
def test_unexpected_client_fields_are_rejected(schema, payload):
    with pytest.raises(ValidationError):
        schema.model_validate(payload)


@pytest.mark.parametrize("payload", [
    {"option_index": -1, "expected_step": 0},
    {"option_index": 0, "expected_step": -1},
    {"option_index": 0, "expected_step": 0, "finding_index": -1},
])
def test_negative_mission_indices_are_rejected(payload):
    with pytest.raises(ValidationError):
        Decision.model_validate(payload)


def test_cors_defaults_are_explicit(monkeypatch):
    monkeypatch.delenv("EDUCYBER_CORS_ORIGINS", raising=False)
    assert configured_origins() == [
        "http://localhost:3000", "http://127.0.0.1:3000"
    ]


@pytest.mark.parametrize("value", [
    "*", "https://*.example.com", "https://example.com/path",
    "file:///tmp", "https://example.com/*",
])
def test_cors_rejects_wildcard_and_non_origin_values(monkeypatch, value):
    monkeypatch.setenv("EDUCYBER_CORS_ORIGINS", value)
    with pytest.raises(ValueError):
        configured_origins()


def test_cors_accepts_explicit_production_origin(monkeypatch):
    monkeypatch.setenv("EDUCYBER_CORS_ORIGINS", "https://app.example.com")
    assert configured_origins() == ["https://app.example.com"]
