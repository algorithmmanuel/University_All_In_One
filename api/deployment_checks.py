"""Fail-closed checks for production deployment settings.

Run before starting a publicly exposed API. No network or DB access required.
"""
import os
from urllib.parse import urlsplit

from sqlalchemy.engine import make_url


def validate_production_settings(environ=None) -> None:
    """Reject unsafe production settings without printing credential values."""
    env = os.environ if environ is None else environ
    if env.get("EDUCYBER_ENV", "").lower() != "production":
        raise ValueError("EDUCYBER_ENV must be production")
    database_url = env.get("DATABASE_URL", "")
    if not database_url:
        raise ValueError("DATABASE_URL is required")
    try:
        database = make_url(database_url)
    except Exception as exc:
        raise ValueError("DATABASE_URL is invalid") from exc
    if not database.drivername.startswith("postgresql"):
        raise ValueError("Production requires PostgreSQL")
    if not database.username or not database.password or not database.host or not database.database:
        raise ValueError("Production database connection must specify credentials and host")
    if database.database == "educyber_test":
        raise ValueError("Test database cannot be used in production")
    if database.host in {"localhost", "127.0.0.1", "::1"}:
        raise ValueError("Production database host must not be loopback")
    origins = env.get("EDUCYBER_CORS_ORIGINS", "")
    if not origins.strip():
        raise ValueError("Explicit production CORS origins required")
    for origin in origins.split(","):
        origin = origin.strip()
        try:
            parts = urlsplit(origin)
            if (parts.scheme != "https" or not parts.hostname or parts.username
                    or parts.password or parts.path or parts.query or parts.fragment
                    or "*" in origin or not parts.netloc):
                raise ValueError("Production CORS origins must be exact HTTPS origins")
            if parts.hostname in {"localhost", "127.0.0.1", "::1"}:
                raise ValueError("Localhost is not a production origin")
        except ValueError as exc:
            raise ValueError("Production CORS origins must be exact HTTPS origins") from exc
    if env.get("EDUCYBER_PUBLIC_HOST", "").strip() == "":
        raise ValueError("EDUCYBER_PUBLIC_HOST is required for deployment inventory")


if __name__ == "__main__":
    validate_production_settings()
    print("Production configuration checks passed (no credentials displayed).")
