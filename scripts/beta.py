"""Guarded laptop-beta startup and explicit preparation; never migrates on startup."""
import argparse
import getpass
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
from urllib.request import build_opener, ProxyHandler, HTTPRedirectHandler
from urllib.error import HTTPError
import json

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'api'))
from beta_runtime import BETA_BRANCH, DEV_BRANCH, MAIL_KEYS, application_environment, validate_mail


def require_context():
    branch = subprocess.check_output(['git', '-C', str(ROOT), 'branch', '--show-current'], text=True).strip()
    if branch != BETA_BRANCH: raise ValueError('Use the beta worktree')
    if Path(sys.prefix).resolve() != (ROOT / 'api' / '.venv').resolve():
        raise ValueError('Use the beta checkout api/.venv Python')


def configuration():
    from dotenv import dotenv_values
    settings = dotenv_values(ROOT / '.env', interpolate=False)
    mail = dotenv_values(ROOT / 'api' / '.env.beta', interpolate=False)
    return application_environment(os.environ, settings.get('POSTGRES_PASSWORD'), mail)


def require_free_port(port):
    with socket.socket() as sock:
        if os.name == 'nt': sock.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        sock.bind(('127.0.0.1', port))


def development_path():
    output = subprocess.check_output(['git', '-C', str(ROOT), 'worktree', 'list', '--porcelain'], text=True)
    paths = []
    for block in output.strip().split('\n\n'):
        fields = dict(line.split(' ', 1) for line in block.splitlines() if ' ' in line)
        if fields.get('branch') == 'refs/heads/' + DEV_BRANCH: paths.append(fields['worktree'])
    if len(paths) != 1 or not Path(paths[0]).is_dir(): raise ValueError('Expected one existing development worktree')
    print(paths[0])


def configure_mail(environment, public_url=None):
    from dotenv import set_key
    values = {key: environment.get(key, '') for key in MAIL_KEYS}
    if not values['BREVO_API_KEY']: values['BREVO_API_KEY'] = getpass.getpass('Existing Brevo API key (hidden): ')
    if not values['EDUCYBER_EMAIL_SENDER']: values['EDUCYBER_EMAIL_SENDER'] = input('Existing verified sender email: ').strip()
    if public_url: values['EDUCYBER_PUBLIC_WEB_URL'] = public_url.rstrip('/')
    if not values['EDUCYBER_PUBLIC_WEB_URL']: values['EDUCYBER_PUBLIC_WEB_URL'] = input('Current beta HTTPS ngrok origin: ').strip().rstrip('/')
    validate_mail(values)
    target = ROOT / 'api' / '.env.beta'
    # Refuse to save credentials unless Git confirms this path is ignored.
    if subprocess.run(['git', '-C', str(ROOT), 'check-ignore', '-q', str(target)]).returncode != 0:
        raise ValueError('Private mail file must be ignored by Git')
    if not target.exists(): target.touch(mode=0o600)
    for key, value in values.items(): set_key(str(target), key, value, quote_mode='always')
    print('Beta recovery mail settings saved privately; no values displayed.')


def check():
    from alembic.config import Config
    from alembic.script import ScriptDirectory
    config = Config(str(ROOT / 'api' / 'alembic.ini'))
    config.set_main_option('script_location', str(ROOT / 'api' / 'migrations'))
    revision = ScriptDirectory.from_config(config).get_current_head()
    class NoRedirect(HTTPRedirectHandler):
        def redirect_request(self, *args, **kwargs): return None
    opener = build_opener(ProxyHandler({}), NoRedirect())
    for origin in ('http://127.0.0.1:8000', 'http://127.0.0.1:3000'):
        checks = [('/health/db', 'database', 'connected'), ('/health/schema', 'schema', 'ready')]
        if origin.endswith(':8000'): checks.insert(0, ('/health', 'status', 'ok'))
        for path, field, expected in checks:
            with opener.open(origin + path, timeout=15) as response: data = json.load(response)
            if data.get(field) != expected: raise ValueError('Beta readiness failed')
            if path == '/health/schema' and data.get('revision') != revision: raise ValueError('Beta schema is not current')
        try: opener.open(origin + '/health/development', timeout=15)
        except HTTPError as error:
            if error.code != 404: raise
        else: raise ValueError('Beta must not expose development identity')
    print('BETA READY: direct/proxied API and schema checks passed; development identity is absent.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('api', 'web', 'build', 'check', 'prepare', 'configure-mail', 'development-path'))
    parser.add_argument('--public-url')
    args = parser.parse_args()
    try:
        require_context()
        if args.action == 'development-path': development_path(); return 0
        environment = configuration()
        if args.action == 'configure-mail': configure_mail(environment, args.public_url); return 0
        if args.action == 'check': check(); return 0
        if args.action == 'prepare':
            for port in (8000, 3000): require_free_port(port)
            return subprocess.call([sys.executable, '-m', 'beta_promotion'], cwd=ROOT / 'api', env=environment)
        port = 8000 if args.action == 'api' else 3000
        require_free_port(port)
        if args.action == 'api':
            validate_mail(environment)
            command = [sys.executable, '-m', 'uvicorn', 'main:app', '--host', '127.0.0.1', '--port', '8000', '--no-access-log']
            directory = ROOT / 'api'
        else:
            # The frontend has no need for database/provider secrets.
            for key in ('DATABASE_URL', *MAIL_KEYS): environment.pop(key, None)
            npm = shutil.which('npm.cmd' if os.name == 'nt' else 'npm')
            if not npm: raise ValueError('npm not found')
            command = [npm, 'run', 'build'] if args.action == 'build' else [npm, 'run', 'start', '--', '--hostname', '127.0.0.1', '--port', '3000']
            directory = ROOT / 'web'
        print('Starting private beta ' + args.action + ' on loopback.', flush=True)
        return subprocess.call(command, cwd=directory, env=environment)
    except KeyboardInterrupt: return 130
    except Exception as error:
        print('Beta action stopped (' + type(error).__name__ + '). Check beta branch, checkout Python, private settings and free ports; secrets are not displayed.', file=sys.stderr)
        return 1


if __name__ == '__main__': raise SystemExit(main())
