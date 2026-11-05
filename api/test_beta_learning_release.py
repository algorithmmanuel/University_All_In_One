"""Exact beta-preview authority, atomic publication, preservation and reader checks."""
from copy import deepcopy
import json
import os
from unittest.mock import patch
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, func, select, text
from sqlalchemy.orm import Session

import beta_learning_release as release
from test_foundations_courses import content_state


def test_checked_in_manifest_matches_exact_current_snapshot():
    assert release.validate_snapshot()['editorial_acceptance_deferred'] is True


@pytest.mark.parametrize('change', ['missing', 'stale', 'scope'])
def test_changed_or_incomplete_snapshot_refuses_beta_exception(change):
    data = json.loads(release.MANIFEST.read_text())
    if change == 'missing': data['course_sha256'].pop(next(iter(data['course_sha256'])))
    if change == 'stale': data['course_sha256'][next(iter(data['course_sha256']))] = '0' * 64
    if change == 'scope': data['scope'] = 'production-approved'
    with patch('pathlib.Path.read_text', return_value=json.dumps(data)):
        with pytest.raises(ValueError): release.validate_snapshot()


def test_beta_exception_does_not_satisfy_production_editorial_gate():
    release.validate_snapshot()
    with patch('pathlib.Path.is_file', return_value=False):
        with pytest.raises(RuntimeError, match='Editorial approvals file missing'):
            release.publisher.require_editorial_approvals()


def test_additive_publication_is_idempotent_and_all_192_lessons_are_readable(content_state):
    from models import Course, Lesson
    client, Factory, _ = content_state
    with Factory.begin() as db:
        baseline = release.capture_existing(db.connection())
        before = db.scalar(select(func.count()).select_from(Lesson))
        assert release.publish_snapshot(db)['inserted_courses'] == 24
        release.assert_existing(db.connection(), baseline)
        assert db.scalar(select(func.count()).select_from(Lesson)) == before + 192
    with Factory.begin() as db:
        assert release.publish_snapshot(db)['inserted_courses'] == 0
        release.assert_existing(db.connection(), baseline)
    entries = client.get('/api/v1/learning/catalog').json()['courses']
    for manuscript in release.publisher.COURSES:
        item = next(row for row in entries if row['title'] == manuscript['title']
                    and row['academy_id'] == manuscript['academy_id'])
        assert item['lesson_count'] == 8
        endpoint = f"/api/v1/learning/courses/{item['id']}/lessons"
        assert client.get(endpoint).status_code == 403
        assert client.post(f"/api/v1/learning/enrollments/{item['id']}").status_code == 201
        response = client.get(endpoint)
        assert response.status_code == 200
        assert [(row['title'], row['content']) for row in response.json()['lessons']] == [
            (row['title'], row['content']) for row in manuscript['lessons']]


def test_late_course_collision_rolls_back_earlier_inserts(content_state):
    from models import Course
    _, Factory, _ = content_state
    last = release.publisher.COURSES[-1]
    with Factory.begin() as db:
        db.add(Course(academy_id=last['academy_id'], title=last['title'],
                      description='Pre-existing custom course must be retained', status='published'))
    with Factory() as db:
        baseline = release.capture_existing(db.connection())
    with pytest.raises(RuntimeError, match='different content'):
        with Factory.begin() as db: release.publish_snapshot(db)
    with Factory() as db: release.assert_existing(db.connection(), baseline)


def test_existing_lesson_content_mutation_is_detected_and_rolled_back(content_state, monkeypatch):
    from models import Lesson
    _, Factory, _ = content_state
    with Factory() as db:
        original = db.get(Lesson, 1).content
        baseline = release.capture_existing(db.connection())
    normal = release.publisher.publish
    def changed(db, course):
        result = normal(db, course)
        db.get(Lesson, 1).content = 'Unapproved old-text replacement'
        return result
    monkeypatch.setattr(release.publisher, 'publish', changed)
    with pytest.raises(ValueError, match='changed existing records'):
        with Factory.begin() as db: release.publish_snapshot(db)
    with Factory() as db:
        assert db.get(Lesson, 1).content == original
        release.assert_existing(db.connection(), baseline)


def test_launcher_routes_explicit_courses_action_to_beta_snapshot(monkeypatch):
    from test_beta_promotion import beta_script
    module = beta_script()
    monkeypatch.setattr(module, 'require_context', lambda: None)
    monkeypatch.setattr(module, 'configuration', lambda: {'EDUCYBER_ENV': 'beta'})
    ports = []
    monkeypatch.setattr(module, 'require_free_port', ports.append)
    monkeypatch.setattr(module.sys, 'argv', ['beta.py', 'courses'])
    calls = []
    monkeypatch.setattr(module.subprocess, 'call', lambda args, **kwargs: calls.append(args) or 0)
    assert module.main() == 0
    assert ports == [8000, 3000]
    assert calls == [[module.sys.executable, '-m', 'beta_learning_release']]


@pytest.mark.integration
def test_postgres_beta_snapshot_preserves_history_and_republishes_idempotently():
    from sqlalchemy.engine import make_url
    url = os.getenv('TEST_DATABASE_URL')
    if not url: pytest.skip('Isolated PostgreSQL required')
    target = make_url(url)
    if (not target.drivername.startswith('postgresql') or target.database != 'educyber_test'
            or target.host not in ('127.0.0.1', 'localhost') or os.getenv('DATABASE_URL') != url):
        pytest.fail('Refusing non-local or non-test database')
    from database import Base
    from models import Academy, Course, Lesson, User, Enrollment, LearnerProgress, BetaFeedback
    schema = 'course_preview_' + uuid4().hex
    admin = create_engine(url)
    with admin.begin() as conn: conn.execute(text('CREATE SCHEMA ' + schema))
    engine = create_engine(url, connect_args={'options': '-csearch_path=' + schema})
    try:
        Base.metadata.create_all(engine)
        with Session(engine) as db, db.begin():
            for key in ('cyber', 'secondary', 'university'):
                db.add(Academy(id=key, name='Synthetic'))
            user = User(full_name='Synthetic', email='preview@example.invalid',
                        password_hash='disabled', role='student', age_band='adult')
            old = Course(academy_id='secondary', title='Retained beta course', status='published')
            db.add_all([user, old]); db.flush()
            lesson = Lesson(course_id=old.id, position=1, title='Retained lesson', content='Original text')
            db.add(lesson); db.flush()
            db.add(Enrollment(user_id=user.id, course_id=old.id))
            db.add(LearnerProgress(learner_id=str(user.id), lesson_id=lesson.id))
            db.add(BetaFeedback(user_id=user.id, category='content', message='Retained feedback'))
        with Session(engine) as db, db.begin():
            baseline = release.capture_existing(db.connection())
            assert release.publish_snapshot(db)['inserted_courses'] == 24
            release.assert_existing(db.connection(), baseline)
        with Session(engine) as db, db.begin():
            assert release.publish_snapshot(db)['inserted_courses'] == 0
            release.assert_existing(db.connection(), baseline)
    finally:
        engine.dispose()
        with admin.begin() as conn: conn.execute(text('DROP SCHEMA ' + schema + ' CASCADE'))
        admin.dispose()
