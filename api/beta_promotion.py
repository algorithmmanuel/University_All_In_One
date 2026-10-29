"""Explicit maintenance promotion: fresh backup, additive migrations, atomic content.

Never invoked on application startup. Only the local beta database and checkout
are allowed by the wrapper and repeated database guards. No seeds or data deletion.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone
from sqlalchemy import MetaData, Table, inspect, select, func, text
from sqlalchemy.orm import Session
from beta_runtime import validate_beta_database
from publish_foundations import publish_releases, PublicationError

TABLES = ('users', 'auth_sessions', 'beta_invites', 'beta_feedback', 'password_reset_tokens',
          'enrollments', 'learner_progress', 'quiz_attempts', 'mission_runs', 'login_attempt_buckets',
          'courses', 'lessons', 'quiz_questions', 'strategy_runs', 'strategy_commands',
          'cyber_practice_sessions', 'cyber_study_progress')
ROOT = Path(__file__).resolve().parents[1]


def fingerprint(conn, name, columns, boundary=None):
    """Hash existing rows without writing personal data into the manifest or logs."""
    table = Table(name, MetaData(), autoload_with=conn)
    statement = select(*(table.c[key] for key in columns)).order_by(*table.primary_key.columns)
    if boundary is not None: statement = statement.where(table.c.id <= boundary)
    digest = hashlib.sha256(); count = 0
    for row in conn.execute(statement):
        digest.update(json.dumps(tuple(row), sort_keys=True, default=str, ensure_ascii=True).encode() + b'\n')
        count += 1
    return {'count': count, 'sha256': digest.hexdigest()}


def capture(conn):
    existing = set(inspect(conn).get_table_names()); result = {}
    for name in TABLES:
        if name not in existing: continue
        columns = sorted(item['name'] for item in inspect(conn).get_columns(name))
        # These are the only existing field mutations deliberately allowed.
        if name == 'lessons': columns.remove('content')
        boundary = None
        if name == 'quiz_questions':
            table = Table(name, MetaData(), autoload_with=conn)
            boundary = conn.scalar(select(func.max(table.c.id))) or 0
        result[name] = {'columns': columns, 'boundary': boundary,
                        **fingerprint(conn, name, columns, boundary)}
    return result


def assert_preserved(conn, baseline):
    for name, item in baseline.items():
        current = fingerprint(conn, name, item['columns'], item['boundary'])
        if current != {k: item[k] for k in ('count', 'sha256')}:
            raise ValueError('Existing-record preservation check failed')


def publish_verified(db, baseline):
    """All three maintained courses preflight and publish in one caller transaction."""
    result = publish_releases(db, ('python', 'cyber', 'citizenship'), apply=True)
    db.flush()
    assert_preserved(db.connection(), baseline)
    return result


def run(args, *, cwd=ROOT, env=None):
    # Never echo subprocess diagnostics: database/provider settings may be present.
    return subprocess.run(args, cwd=cwd, env=env, check=True, capture_output=True, text=True).stdout.strip()


def checked_container():
    context = json.loads(run(['docker', 'context', 'inspect']))
    host = context[0]['Endpoints']['docker']['Host']
    if not host.startswith(('unix://', 'npipe://')): raise ValueError('Local Docker context required')
    container = run(['docker', 'compose', 'ps', '-q', 'postgres'])
    if not container or '\n' in container: raise ValueError('Expected one beta database container')
    details = json.loads(run(['docker', 'inspect', container]))[0]
    settings = dict(item.split('=', 1) for item in details['Config']['Env'] if '=' in item)
    ports = details['NetworkSettings']['Ports'].get('5432/tcp')
    if (details['Config']['Labels'].get('com.docker.compose.service') != 'postgres'
        or settings.get('POSTGRES_DB') != 'educyber' or settings.get('POSTGRES_USER') != 'educyber'
        or ports != [{'HostIp': '127.0.0.1', 'HostPort': '5433'}]):
        raise ValueError('Unexpected beta container or published port')
    return container


def backup(container):
    folder = ROOT / 'local-backups'; folder.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    target = folder / ('beta-promotion-' + stamp + '.dump')
    remote = '/tmp/' + target.name
    run(['docker', 'exec', container, 'pg_dump', '-U', 'educyber', '-d', 'educyber', '-Fc', '-f', remote])
    run(['docker', 'exec', container, 'pg_restore', '--list', remote])
    expected = run(['docker', 'exec', container, 'sha256sum', remote]).split()[0]
    # Docker copies binary archives directly; PowerShell text redirection is not used.
    run(['docker', 'cp', container + ':' + remote, str(target)])
    with target.open('rb') as archive:
        digest = hashlib.file_digest(archive, 'sha256').hexdigest()
    if target.stat().st_size < 1024 or digest != expected: raise ValueError('Backup copy verification failed')
    target.with_suffix('.dump.sha256').write_text(digest + '\n')
    run(['docker', 'exec', container, 'rm', '-f', remote])
    print('BACKUP VERIFIED: ' + str(target))
    return target


def prepare(environment):
    from database import engine
    validate_beta_database(environment.get('DATABASE_URL', ''))
    if environment.get('EDUCYBER_PRIVATE_BETA') != 'enabled': raise ValueError('Private beta mode required')
    with engine.connect() as conn:
        identity = conn.execute(text('SELECT current_database(), current_user')).one()
        revision = conn.scalar(text('SELECT version_num FROM alembic_version'))
        if tuple(identity) != ('educyber', 'educyber') or revision not in (
            '0009_password_reset', '0010_attempt_results', '0011_strategy_learning'):
            raise ValueError('Unexpected beta database identity or schema')
    target = backup(checked_container())
    with engine.connect() as conn: baseline = capture(conn)
    target.with_suffix('.preservation.json').write_text(json.dumps(baseline, indent=2))
    run([sys.executable, '-m', 'alembic', 'upgrade', 'head'], cwd=ROOT / 'api', env=environment)
    with Session(engine) as db:
        try:
            assert_preserved(db.connection(), baseline)
            result = publish_verified(db, baseline)
            db.commit()
        except Exception:
            db.rollback()
            raise
    print('PROMOTION PREPARED: schema 0011_strategy_learning; all three course releases published; existing records preserved.')
    print('New aligned question rows: ' + str(result['new_questions']))


if __name__ == '__main__':
    # Direct CLI use repeats the checkout/interpreter/port checks from the launcher.
    sys.path.insert(0, str(ROOT / 'scripts'))
    from beta import require_context, require_free_port
    try:
        require_context()
        for port in (8000, 3000): require_free_port(port)
        prepare(dict(os.environ))
    except PublicationError as error:
        print('Content publication refused: ' + str(error) + ' Keep beta offline; no course changes were committed.', file=sys.stderr)
        raise SystemExit(1)
    except Exception as error:
        print('Beta preparation stopped (' + type(error).__name__ + '). Keep beta offline; inspect the verified backup and configuration. No automatic restore is performed.', file=sys.stderr)
        raise SystemExit(1)
