"""Explicit local startup and read-only isolation checks. Never runs migrations.

Run using api/.venv Python. Configuration is read from api/.env.development;
application settings inherited from another checkout are discarded.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
from urllib.request import HTTPRedirectHandler, ProxyHandler, build_opener

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'api'))
from development_runtime import validate_development_database

WEB = 'http://127.0.0.1:3010'
API = 'http://127.0.0.1:8010'


def application_environment(inherited, settings):
    """Copy system settings but never beta application or mail configuration."""
    database = settings.get('DATABASE_URL', '')
    validate_development_database(database)
    prefixes = ('EDUCYBER_', 'NEXT_PUBLIC_', 'BREVO', 'SMTP', 'POSTGRES_', 'PG')
    excluded = {'DATABASE_URL', 'TEST_DATABASE_URL', 'PYTHONPATH', 'PYTHONHOME',
                'VIRTUAL_ENV', 'NODE_OPTIONS', 'NODE_PATH'}
    environment = {key: value for key, value in inherited.items()
                   if key.upper() not in excluded
                   and not key.upper().startswith(prefixes)}
    environment.update({
        'DATABASE_URL': database, 'EDUCYBER_ENV': 'development',
        'EDUCYBER_PRIVATE_BETA': 'disabled',
        'EDUCYBER_LOCAL_DEVELOPMENT': 'enabled',
        'EDUCYBER_CORS_ORIGINS': WEB + ',http://localhost:3010',
        'EDUCYBER_API_ORIGIN': API, 'EDUCYBER_WEB_ORIGIN': WEB,
        'NEXT_PUBLIC_API_BASE_URL': '',
    })
    return environment


def configuration():
    branch = subprocess.check_output(
        ['git', '-C', str(ROOT), 'branch', '--show-current'], text=True
    ).strip()
    if branch != 'feature/beta-continuous-improvement':
        raise ValueError('Run this launcher only from the development branch')
    expected_python = ROOT / 'api' / '.venv'
    if Path(sys.prefix).resolve() != expected_python.resolve():
        raise ValueError('Use this checkout\'s api/.venv Python')
    env_file = ROOT / 'api' / '.env.development'
    if not env_file.is_file():
        raise ValueError('Missing api/.env.development; do not copy beta credentials')
    from dotenv import dotenv_values
    # Disable interpolation so inherited variables cannot influence the target.
    settings = dotenv_values(env_file, interpolate=False)
    return application_environment(os.environ, settings)


def require_free_port(port):
    with socket.socket() as listener:
        if os.name == 'nt':
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        listener.bind(('127.0.0.1', port))


def fetch_json(url):
    # Local readiness checks must not use an inherited HTTP proxy or redirect.
    class NoRedirect(HTTPRedirectHandler):
        def redirect_request(self, request, response, code, message, headers, new_url):
            return None

    opener = build_opener(ProxyHandler({}), NoRedirect())
    with opener.open(url, timeout=15) as response:
        if response.geturl() != url:
            raise ValueError('Unexpected redirect during isolation verification')
        return json.load(response)


def verify(environment):
    direct = fetch_json(API + '/health/development')
    proxied = fetch_json(WEB + '/health/development')
    if (direct.get('environment') != 'isolated-development'
            or not direct.get('instance_id') or direct != proxied):
        raise ValueError('Frontend and development API identities do not match')
    for origin in (API, WEB):
        if fetch_json(origin + '/health/db') != {'database': 'connected'}:
            raise ValueError('Database readiness check failed')
        if fetch_json(origin + '/health/schema').get('schema') != 'ready':
            raise ValueError('Schema readiness check failed')
    from sqlalchemy import create_engine, text
    engine = create_engine(environment['DATABASE_URL'])
    try:
        with engine.connect() as connection:
            connection.execute(text('SET TRANSACTION READ ONLY'))
            if connection.scalar(text('SELECT current_database()')) != 'educyber_dev':
                raise ValueError('Unexpected database identity')
    finally:
        engine.dispose()
    print('ISOLATION VERIFIED: frontend and API identities match; development database and schema are ready.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('api', 'web', 'check'))
    action = parser.parse_args().action
    try:
        environment = configuration()
        if action == 'check':
            verify(environment)
            return 0
        port = 8010 if action == 'api' else 3010
        require_free_port(port)
        if action == 'api':
            command = [sys.executable, '-m', 'uvicorn', 'main:app',
                       '--host', '127.0.0.1', '--port', str(port), '--no-access-log']
            directory = ROOT / 'api'
        else:
            npm = shutil.which('npm.cmd' if os.name == 'nt' else 'npm')
            if not npm:
                raise ValueError('npm was not found')
            command = [npm, 'run', 'dev', '--', '--hostname', '127.0.0.1', '--port', str(port)]
            directory = ROOT / 'web'
        print('Starting isolated development ' + action + ' on loopback.', flush=True)
        return subprocess.call(command, cwd=directory, env=environment)
    except KeyboardInterrupt:
        return 130
    except Exception as error:
        # Driver/process errors may contain credentials: report only safe context.
        print('Development action stopped (' + type(error).__name__ +
              '). Verify the branch, local environment, free ports and service readiness.',
              file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
