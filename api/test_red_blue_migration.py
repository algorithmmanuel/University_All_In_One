"""Migration adds independent tables without rewriting existing saved learning."""
import importlib.util
from pathlib import Path
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import create_engine, inspect, text


def test_additive_red_blue_migration_round_trip():
    spec = importlib.util.spec_from_file_location('rb_migration', Path(__file__).parent / 'migrations/versions/0012_red_blue_matches.py')
    migration = importlib.util.module_from_spec(spec); spec.loader.exec_module(migration)
    e = create_engine('sqlite://')
    with e.begin() as c:
        c.execute(text('CREATE TABLE users (id INTEGER PRIMARY KEY)'))
        for table in ('learner_progress', 'quiz_attempts', 'mission_runs', 'strategy_runs', 'cyber_practice_sessions'):
            c.execute(text(f'CREATE TABLE {table} (id INTEGER PRIMARY KEY, saved TEXT)'))
            c.execute(text(f"INSERT INTO {table} VALUES (1, 'preserved')"))
        original = set(inspect(c).get_table_names())
        with Operations.context(MigrationContext.configure(c)):
            migration.upgrade()
        assert set(inspect(c).get_table_names()) - original == {'red_blue_matches', 'red_blue_seats', 'red_blue_receipts'}
        for table in original - {'users'}:
            assert c.execute(text(f'SELECT * FROM {table}')).all() == [(1, 'preserved')]
        with Operations.context(MigrationContext.configure(c)):
            migration.downgrade()
        assert set(inspect(c).get_table_names()) == original
    e.dispose()
