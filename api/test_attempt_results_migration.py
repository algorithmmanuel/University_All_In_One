"""Exercise the additive migration against populated, isolated old-schema SQLite."""
import importlib.util
from pathlib import Path
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import create_engine, text


def test_additive_snapshot_migration_preserves_existing_rows():
    path = Path(__file__).parent / 'migrations/versions/0010_attempt_results.py'
    spec = importlib.util.spec_from_file_location('snapshot_migration', path)
    migration = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migration)
    engine = create_engine('sqlite+pysqlite:///:memory:')
    try:
        with engine.begin() as connection:
            connection.execute(text('CREATE TABLE quiz_attempts (id INTEGER PRIMARY KEY, answers JSON NOT NULL, score INTEGER NOT NULL, total INTEGER NOT NULL)'))
            connection.execute(text('INSERT INTO quiz_attempts VALUES (1, :answers, 1, 2)'), {'answers': '{"7":1,"8":0}'})
            before = connection.execute(text('SELECT * FROM quiz_attempts')).one()
            with Operations.context(MigrationContext.configure(connection)):
                migration.upgrade()
            after = connection.execute(text('SELECT id, answers, score, total, result_snapshot FROM quiz_attempts')).one()
            assert tuple(after[:4]) == tuple(before) and after[4] is None
            # Downgrade removes topic snapshots only; score/answer history survives.
            with Operations.context(MigrationContext.configure(connection)):
                migration.downgrade()
            assert connection.execute(text('SELECT * FROM quiz_attempts')).one() == before
    finally:
        engine.dispose()
