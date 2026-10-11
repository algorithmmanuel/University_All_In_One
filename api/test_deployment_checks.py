"""Pure configuration tests; never connect to the configured database."""
import pytest
from deployment_checks import validate_production_settings


def production():
    return {
        "EDUCYBER_ENV": "production",
        "DATABASE_URL": "postgresql+psycopg://educyber:strong-pass@db.example.com:5432/educyber",
        "EDUCYBER_CORS_ORIGINS": "https://app.example.com",
        "EDUCYBER_PUBLIC_HOST": "api.example.com",
    }


def test_valid_production_configuration():
    validate_production_settings(production())


@pytest.mark.parametrize("key,value", [
    ("EDUCYBER_ENV", "development"),
    ("DATABASE_URL", ""),
    ("DATABASE_URL", "sqlite:///dev.db"),
    ("DATABASE_URL", "postgresql+psycopg://educyber:pass@127.0.0.1/educyber"),
    ("DATABASE_URL", "postgresql+psycopg://educyber:pass@db.example.com/educyber_test"),
    ("DATABASE_URL", "postgresql+psycopg://educyber@db.example.com/educyber"),
    ("EDUCYBER_CORS_ORIGINS", ""),
    ("EDUCYBER_CORS_ORIGINS", "*"),
    ("EDUCYBER_CORS_ORIGINS", "http://app.example.com"),
    ("EDUCYBER_CORS_ORIGINS", "https://app.example.com/path"),
    ("EDUCYBER_CORS_ORIGINS", "https://localhost:3000"),
    ("EDUCYBER_CORS_ORIGINS", "https://app.example.com, http://insecure.example.com"),
    ("EDUCYBER_PUBLIC_HOST", ""),
])
def test_rejects_unsafe_settings(key, value):
    env = production()
    env[key] = value
    with pytest.raises(ValueError):
        validate_production_settings(env)


def test_missing_values_fail_closed():
    with pytest.raises(ValueError):
        validate_production_settings({})
