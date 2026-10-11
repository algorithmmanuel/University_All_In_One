"""Schema readiness tests using a disposable SQLite database."""
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
