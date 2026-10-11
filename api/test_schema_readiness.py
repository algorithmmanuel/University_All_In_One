"""Schema readiness tests using a disposable SQLite database."""
import os
from sqlalchemy.engine import make_url

# Configure the database module before importing it. Never inherit a development
# DATABASE_URL into test collection. PostgreSQL tests require explicit isolation.
test_url = os.getenv("TEST_DATABASE_URL")
if test_url:
    parsed = make_url(test_url)
    if (not parsed.drivername.startswith("postgresql")
            or parsed.database != "educyber_test"
            or parsed.host not in ("localhost", "127.0.0.1")):
        raise RuntimeError("TEST_DATABASE_URL must target local educyber_test")
    configured = os.getenv("DATABASE_URL")
    if configured and configured != test_url:
        raise RuntimeError("DATABASE_URL and TEST_DATABASE_URL must match for tests")
    os.environ["DATABASE_URL"] = test_url
else:
    # Unit tests use an in-memory database and never connect to the app DB.
    os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"

from sqlalchemy import create_engine
from database import Base
import models
from schema_readiness import schema_status


def test_empty_schema_is_not_ready():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    try:
        result = schema_status(engine)
        assert result["schema"] == "migration_required"
        assert "login_attempt_buckets" in result["missing_tables"]
    finally:
        engine.dispose()


def test_existing_unversioned_schema_is_not_ready():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    try:
        Base.metadata.create_all(engine)
        result = schema_status(engine)
        assert result["schema"] == "migration_required"
        assert result["missing_tables"] == []
        assert result["applied_revisions"] == []
    finally:
        engine.dispose()
