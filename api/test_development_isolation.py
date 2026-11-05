"""Pure guard tests: no application imports, network calls or database access."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

from development_runtime import add_development_health, validate_development_database

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'development.py'
SPEC = importlib.util.spec_from_file_location('development_launcher', SCRIPT)
launcher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(launcher)
DATABASE = 'postgresql+psycopg://educyber_dev:test-only@127.0.0.1:5435/educyber_dev?connect_timeout=5'


class FakeApp:
    def __init__(self):
        self.routes = {}

    def get(self, path, **options):
        def register(handler):
            self.routes[path] = handler
            return handler
        return register


class DevelopmentIsolationTests(unittest.TestCase):
    def test_accepts_only_dedicated_database_target(self):
        validate_development_database(DATABASE)
        for value in (
            '', DATABASE.replace(':5435', ':5433'),
            DATABASE.replace('/educyber_dev?', '/educyber?'),
            DATABASE.replace('127.0.0.1', 'remote.example'),
            DATABASE.replace('postgresql+psycopg', 'sqlite'),
            DATABASE.replace('test-only@', '@'),
            DATABASE + '&host=remote.example',
            DATABASE + '&options=-csearch_path=other',
            DATABASE + '#fragment',
        ):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_development_database(value)

    def test_environment_removes_beta_settings_and_ignores_file_mail_settings(self):
        inherited = {
            'PATH': 'system-path', 'DATABASE_URL': 'beta-target',
            'BREVO_API_KEY': 'private', 'EDUCYBER_EMAIL_SENDER': 'private',
            'EDUCYBER_ENV': 'production', 'TEST_DATABASE_URL': 'test-target',
            'NEXT_PUBLIC_API_BASE_URL': 'https://beta.example',
            'PGHOST': 'beta-host', 'NODE_OPTIONS': '--require=unexpected',
            'PYTHONPATH': 'beta-imports',
        }
        env = launcher.application_environment(inherited, {
            'DATABASE_URL': DATABASE, 'BREVO_API_KEY': 'also-private',
        })
        self.assertEqual(env['PATH'], 'system-path')
        self.assertEqual(env['DATABASE_URL'], DATABASE)
        self.assertEqual(env['NEXT_PUBLIC_API_BASE_URL'], '')
        self.assertEqual(env['EDUCYBER_ENV'], 'development')
        for key in ('BREVO_API_KEY', 'EDUCYBER_EMAIL_SENDER', 'TEST_DATABASE_URL',
                    'PGHOST', 'NODE_OPTIONS', 'PYTHONPATH'):
            self.assertNotIn(key, env)

    def test_runtime_identity_is_absent_in_ordinary_beta_mode(self):
        app = FakeApp()
        add_development_health(app, {})
        self.assertEqual(app.routes, {})

    def test_runtime_identity_is_stable_per_app_and_different_per_instance(self):
        env = launcher.application_environment({}, {'DATABASE_URL': DATABASE})
        first, second = FakeApp(), FakeApp()
        add_development_health(first, env)
        add_development_health(second, env)
        handler = first.routes['/health/development']
        self.assertEqual(handler(), handler())
        self.assertNotEqual(handler(), second.routes['/health/development']())
        self.assertNotIn('DATABASE_URL', str(handler()))

    def test_runtime_identity_refuses_beta_database_or_production(self):
        env = launcher.application_environment({}, {'DATABASE_URL': DATABASE})
        for key, value in (('DATABASE_URL', DATABASE.replace(':5435', ':5433')),
                           ('EDUCYBER_ENV', 'production')):
            with self.subTest(key=key), self.assertRaises(ValueError):
                add_development_health(FakeApp(), {**env, key: value})

    def test_check_rejects_mismatched_frontend_before_database_access(self):
        values = [
            {'environment': 'isolated-development', 'instance_id': 'one'},
            {'environment': 'isolated-development', 'instance_id': 'two'},
        ]
        with patch.object(launcher, 'fetch_json', side_effect=values):
            with self.assertRaisesRegex(ValueError, 'identities'):
                launcher.verify({})


if __name__ == '__main__':
    unittest.main()
