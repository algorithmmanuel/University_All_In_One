"""Owner-authorised beta snapshot; preserves the production editorial gate.

Run through scripts/beta.py courses in the existing laptop beta checkout.
The fixed manifest binds the 4 November beta exception to exact course hashes.
No migrations, reseeding, existing lesson rewrites or approval signatures occur.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys

from sqlalchemy import MetaData, Table, func, inspect, select, text
from sqlalchemy.orm import Session

from beta_promotion import backup, checked_container, fingerprint
from beta_runtime import validate_beta_database
import publish_production_learning as publisher

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'api' / 'production_learning' / 'beta_preview_2026_11_04.json'
RELEASE_ID = 'educyber-course-beta-2026-11-04'


def course_hash(course):
    payload = json.dumps(course, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()


def validate_snapshot():
    """Require the exact owner-authorised snapshot; never manufacture review approval."""
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    if (manifest.get('release_id') != RELEASE_ID
            or manifest.get('scope') != 'owner-authorised-beta-preview'
            or manifest.get('editorial_acceptance_deferred') is not True):
        raise ValueError('Wrong beta snapshot authority or scope')
    courses = publisher.COURSES
    expected = {(path, stage) for path in publisher.PATHWAYS for stage in publisher.STAGES}
    if (len(courses) != 24 or {(c['pathway'], c['stage']) for c in courses} != expected
            or len({c['key'] for c in courses}) != 24
            or sum(len(c['lessons']) for c in courses) != 192):
        raise ValueError('Expected complete 24-course, 192-lesson beta snapshot')
    hashes = {course['key']: course_hash(course) for course in courses}
    if manifest.get('course_sha256') != hashes:
        raise ValueError('Beta snapshot changed; renewed owner-authorised manifest required')
    for course in courses:
        publisher.validate(course)
    publisher.validate_editorial_uniqueness()
    return manifest


def capture_existing(conn):
    """Fingerprint all existing table fields, including old lesson text.

    Only courses and lessons may grow. Their existing integer IDs bound the
    fingerprint so every old row remains byte-equivalent after insertion.
    All other tables must retain their complete count and fingerprint.
    """
    result = {}
    for name in sorted(inspect(conn).get_table_names()):
        table = Table(name, MetaData(), autoload_with=conn)
        if not tuple(table.primary_key.columns):
            raise ValueError('Cannot establish deterministic preservation without a primary key')
        columns = sorted(column.name for column in table.columns)
        boundary = None
        if name in ('courses', 'lessons'):
            boundary = conn.scalar(select(func.max(table.c.id))) or 0
        result[name] = {'columns': columns, 'boundary': boundary,
                        **fingerprint(conn, name, columns, boundary)}
    return result


def assert_existing(conn, baseline):
    for name, item in baseline.items():
        current = fingerprint(conn, name, item['columns'], item['boundary'])
        if current != {key: item[key] for key in ('count', 'sha256')}:
            raise ValueError('Beta publication changed existing records; transaction refused')


def publish_snapshot(db):
    """Insert all courses or fail in the caller's transaction; no existing updates."""
    validate_snapshot()
    baseline = capture_existing(db.connection())
    outcomes = [publisher.publish(db, course) for course in publisher.COURSES]
    db.flush()
    assert_existing(db.connection(), baseline)
    return {'courses': len(outcomes), 'lessons': 192,
            'inserted_courses': outcomes.count('staged')}


def prepare(environment):
    """Back up the guarded local beta database, then publish without migrations."""
    validate_snapshot()
    validate_beta_database(environment.get('DATABASE_URL', ''))
    if (environment.get('EDUCYBER_ENV') != 'beta'
            or environment.get('EDUCYBER_PRIVATE_BETA') != 'enabled'
            or environment.get('EDUCYBER_LOCAL_DEVELOPMENT') != 'disabled'):
        raise ValueError('Expected isolated private beta mode')
    from database import engine
    from schema_readiness import expected_revision
    with engine.connect() as conn:
        identity = conn.execute(text('SELECT current_database(), current_user')).one()
        revision = conn.scalar(text('SELECT version_num FROM alembic_version'))
        if tuple(identity) != ('educyber', 'educyber') or revision != expected_revision():
            raise ValueError('Unexpected beta database identity or schema; no migration attempted')
    target = backup(checked_container())
    with Session(engine) as db:
        with db.begin():
            # Serialise this explicit publication without weakening application access.
            db.execute(text('SELECT pg_advisory_xact_lock(20261104, 24)'))
            baseline = capture_existing(db.connection())
            target.with_suffix('.courses-preservation.json').write_text(
                json.dumps(baseline, indent=2), encoding='utf-8')
            result = publish_snapshot(db)
    print('BETA COURSES READY: 24 courses / 192 lessons; '
          + str(result['inserted_courses']) + ' courses inserted; existing records preserved.')
    print('Editorial review remains deferred. This is the owner-authorised beta snapshot.')


if __name__ == '__main__':
    sys.path.insert(0, str(ROOT / 'scripts'))
    from beta import require_context, require_free_port
    try:
        require_context()
        for port in (8000, 3000):
            require_free_port(port)
        prepare(dict(os.environ))
    except Exception as error:
        print('Beta course publication stopped (' + type(error).__name__
              + '). No partial course publication; inspect the backup, snapshot and beta configuration.',
              file=sys.stderr)
        raise SystemExit(1)
