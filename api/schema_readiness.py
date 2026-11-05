"""Read-only Alembic and SQLAlchemy schema readiness checks.

Never create tables or stamp a database in a health endpoint. A database can
have every table but still be missing columns or migrations.
"""
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine

from database import Base


def expected_revision() -> str:
    from pathlib import Path
    config = Config(str(Path(__file__).resolve().parent / "alembic.ini"))
    config.set_main_option('script_location', str(Path(__file__).resolve().parent / 'migrations'))
    return ScriptDirectory.from_config(config).get_current_head()


def schema_status(engine: Engine) -> dict:
    # Import all mapped tables before checking the SQLAlchemy metadata.
    import models  # noqa: F401

    expected = expected_revision()
    with engine.connect() as connection:
        inspector = inspect(connection)
        existing = set(inspector.get_table_names())
        missing_tables = sorted(set(Base.metadata.tables) - existing)
        missing_columns = sorted(
            f"{table.name}.{column.name}"
            for table in Base.metadata.sorted_tables if table.name in existing
            for column in table.columns
            if column.name not in {c["name"] for c in inspector.get_columns(table.name)}
        )
        versions = (
            [row[0] for row in connection.execute(text("SELECT version_num FROM alembic_version"))]
            if "alembic_version" in existing else []
        )
    ready = not missing_tables and not missing_columns and versions == [expected]
    return {
        "schema": "ready" if ready else "migration_required",
        "expected_revision": expected,
        "applied_revisions": versions,
        "missing_tables": missing_tables,
        "missing_columns": missing_columns,
    }
