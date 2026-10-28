"""Additive migration with populated legacy rows and new-state round trip."""
import importlib.util
from pathlib import Path
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import create_engine, text, inspect


def test_strategy_migration_preserves_legacy_rows_and_reverses_only_new_tables():
    path = Path(__file__).parent / 'migrations/versions/0011_strategy_learning.py'
    spec = importlib.util.spec_from_file_location('strategy_migration', path)
    migration = importlib.util.module_from_spec(spec); spec.loader.exec_module(migration)
    e = create_engine('sqlite+pysqlite:///:memory:')
    try:
        with e.begin() as c:
            c.execute(text('CREATE TABLE users (id INTEGER PRIMARY KEY)'))
            c.execute(text('INSERT INTO users VALUES (1)'))
            c.execute(text('CREATE TABLE mission_runs (id INTEGER PRIMARY KEY, score INTEGER, choices JSON)'))
            c.execute(text("INSERT INTO mission_runs VALUES (7, 35, '[]')"))
            before = c.execute(text('SELECT * FROM mission_runs')).all()
            with Operations.context(MigrationContext.configure(c)): migration.upgrade()
            c.execute(text("INSERT INTO strategy_runs (id,user_id,state) VALUES (1,1,'{}')"))
            assert c.execute(text('SELECT * FROM mission_runs')).all() == before
            assert c.scalar(text('SELECT count(*) FROM strategy_runs')) == 1
            with Operations.context(MigrationContext.configure(c)): migration.downgrade()
            assert c.execute(text('SELECT * FROM mission_runs')).all() == before
            assert set(inspect(c).get_table_names()) == {'users', 'mission_runs'}
    finally: e.dispose()
