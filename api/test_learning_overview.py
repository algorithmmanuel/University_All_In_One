"""Dashboard HTTP projection tests; synthetic SQLite and overridden identity."""
from datetime import datetime, timedelta, timezone
import pytest
from test_foundations_courses import content_state


def test_progress_and_first_incomplete_lesson_are_owned_and_read_only(content_state):
    from models import QuizAttempt, LearnerProgress
    from sqlalchemy import select
    client, Session, _ = content_state
    with Session() as db:
        before = [(a.id, a.answers, a.score, a.total) for a in db.scalars(select(QuizAttempt)).all()]
        progress_before = db.scalars(select(LearnerProgress.id)).all()
    response = client.get('/api/v1/learning/overview')
    assert response.status_code == 200
    body = response.json()
    assert body['enrolled_count'] == 4 and body['completed_courses'] == 0
    assert len(body['courses']) == len(body['recent_attempts']) == 3
    first = body['courses'][0]
    assert (first['id'], first['completed_lessons'], first['total_lessons'], first['progress_percent']) == (1, 1, 3, 33)
    assert first['next_lesson']['id'] == 2
    assert {a['id'] for a in body['recent_attempts']} == {1, 2, 3}
    assert all('answers' not in a and 'analysis' not in a for a in body['recent_attempts'])
    with Session() as db:
        assert [(a.id, a.answers, a.score, a.total) for a in db.scalars(select(QuizAttempt)).all()] == before
        assert db.scalars(select(LearnerProgress.id)).all() == progress_before


def test_completed_course_and_zero_lesson_course_are_distinguished(content_state):
    from models import Course, Enrollment
    client, Session, _ = content_state
    for lesson in (2, 3):
        assert client.post(f'/api/v1/learning/lessons/{lesson}/complete').status_code == 200
    with Session.begin() as db:
        db.get(Course, 4).status = 'draft'
    body = client.get('/api/v1/learning/overview').json()
    assert body['completed_courses'] == 1
    complete = next(c for c in body['courses'] if c['id'] == 1)
    assert complete['completed'] and complete['progress_percent'] == 100 and complete['next_lesson'] is None
    with Session.begin() as db:
        db.add(Course(id=5, academy_id='cyber', title='No lessons', status='published'))
        db.flush()
        db.add(Enrollment(user_id=1, course_id=5, enrolled_at=datetime.now(timezone.utc)+timedelta(days=1)))
    empty = next(c for c in client.get('/api/v1/learning/overview').json()['courses'] if c['id'] == 5)
    assert (empty['total_lessons'], empty['completed_lessons'], empty['progress_percent'], empty['completed']) == (0, 0, 0, False)
    assert empty['next_lesson'] is None


def test_recent_attempt_uses_chronology_not_best_score_and_has_a_bound(content_state):
    from models import QuizAttempt
    client, Session, _ = content_state
    with Session.begin() as db:
        db.add(QuizAttempt(id=100, user_id=1, course_id=1, score=0, total=5, answers={},
                           submitted_at=datetime.now(timezone.utc)+timedelta(days=1)))
        db.add(QuizAttempt(id=101, user_id=2, course_id=1, score=999, total=999, answers={},
                           submitted_at=datetime.now(timezone.utc)+timedelta(days=2)))
    attempts = client.get('/api/v1/learning/overview').json()['recent_attempts']
    assert len(attempts) == 3
    assert (attempts[0]['id'], attempts[0]['score'], attempts[0]['total'], attempts[0]['percentage']) == (100, 0, 5, 0)
    assert all(a['id'] != 101 for a in attempts)


def test_draft_and_unenrolled_courses_do_not_appear(content_state):
    from models import Course, Enrollment
    from sqlalchemy import select
    client, Session, _ = content_state
    with Session.begin() as db:
        db.get(Course, 1).status = 'draft'
        db.delete(db.scalar(select(Enrollment).where(Enrollment.user_id == 1, Enrollment.course_id == 2)))
    body = client.get('/api/v1/learning/overview').json()
    assert body['enrolled_count'] == 2
    assert {c['id'] for c in body['courses']} == {3, 4}
    assert {a['course_id'] for a in body['recent_attempts']} == {3}


def test_other_learner_receives_only_their_own_progress(content_state):
    from models import Enrollment
    client, Session, learner = content_state
    learner.id = 2
    assert client.get('/api/v1/learning/overview').json() == {
        'enrolled_count': 0, 'completed_courses': 0, 'courses': [], 'recent_attempts': []}
    with Session.begin() as db:
        db.add(Enrollment(user_id=2, course_id=1))
    course = client.get('/api/v1/learning/overview').json()['courses'][0]
    assert course['completed_lessons'] == 0 and course['next_lesson']['id'] == 1


@pytest.mark.parametrize('role', ['teacher', 'admin'])
def test_nonstudent_rejected(content_state, role):
    client, _, learner = content_state
    learner.role = role
    assert client.get('/api/v1/learning/overview').status_code == 403
