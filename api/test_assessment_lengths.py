"""Real quiz HTTP handlers against disposable in-memory SQLite, never beta data.

Authentication is overridden to isolate quiz authorisation/selection/grading;
these tests do not establish PostgreSQL concurrency or full login behaviour.
"""
import os
from types import SimpleNamespace
from unittest.mock import patch

import pytest


@pytest.fixture
def quiz_client():
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import StaticPool
    # Importing configured database modules never uses their engine here.
    # All test reads/writes use the separate in-memory engine below.
    with patch.dict(os.environ, {'DATABASE_URL': 'sqlite+pysqlite:///:memory:'}):
        import quiz_routes
        from database import Base
        from models import Academy, Course, Enrollment, QuizQuestion, User

    engine = create_engine('sqlite+pysqlite:///:memory:',
                           connect_args={'check_same_thread': False}, poolclass=StaticPool)
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    Base.metadata.create_all(engine)
    with Session.begin() as db:
        db.add(Academy(id='cyber', name='Synthetic Academy', status='published'))
        db.flush()
        db.add(User(id=1, full_name='Synthetic Learner', email='learner@example.com',
                    password_hash='disabled', role='student', age_band='adult'))
        db.add(Course(id=1, academy_id='cyber', title='Practice', status='published'))
        db.add(Course(id=2, academy_id='cyber', title='Not enrolled', status='published'))
        db.flush()
        db.add(Enrollment(user_id=1, course_id=1))
        for index in range(1, 51):
            db.add(QuizQuestion(id=index, course_id=1, position=index,
                prompt=f'Scenario {index}', options=['Safe', 'Unsafe'],
                correct_index=0, explanation='Verify before acting.'))
        db.add(QuizQuestion(id=51, course_id=1, position=51,
            prompt='  SCENARIO   1 ', options=['Safe', 'Unsafe'],
            correct_index=0, explanation='Duplicate prompt.'))

    def database_session():
        with Session() as db:
            yield db

    learner = SimpleNamespace(id=1, role='student')
    app = FastAPI()
    app.include_router(quiz_routes.router)
    app.dependency_overrides[quiz_routes.get_db] = database_session
    app.dependency_overrides[quiz_routes.current_user] = lambda: learner
    try:
        with TestClient(app) as client:
            yield client, learner
    finally:
        engine.dispose()


@pytest.mark.parametrize('count', [1, 5, 10, 20, 37, 50])
def test_chosen_length_is_selected_graded_and_persisted(quiz_client, count):
    client, _ = quiz_client
    response = client.get(f'/api/v1/quizzes/courses/1?question_count={count}')
    assert response.status_code == 200
    questions = response.json()['questions']
    assert len(questions) == count
    assert len({q['prompt'].strip().casefold() for q in questions}) == count
    assert all('correct_index' not in q and 'explanation' not in q for q in questions)
    answers = {str(q['id']): 0 for q in questions}
    result = client.post('/api/v1/quizzes/courses/1/submit',
                         json={'question_count': count, 'answers': answers})
    assert result.status_code == 201
    assert result.json()['score'] == count and result.json()['total'] == count
    history = client.get('/api/v1/quizzes/courses/1/attempts').json()['attempts']
    assert history[0]['total'] == count and history[0]['score'] == count


def test_options_count_unique_prompts_and_keep_legacy_full_bank(quiz_client):
    client, _ = quiz_client
    options = client.get('/api/v1/quizzes/courses/1/options').json()
    assert options['available_count'] == 50 and options['presets'] == [5, 10, 20]
    questions = client.get('/api/v1/quizzes/courses/1').json()['questions']
    assert len(questions) == 51
    result = client.post('/api/v1/quizzes/courses/1/submit',
        json={'answers': {str(q['id']): 0 for q in questions}})
    assert result.status_code == 201 and result.json()['total'] == 51


def test_selected_questions_are_graded_with_their_real_answer_keys(quiz_client):
    client, _ = quiz_client
    questions = client.get('/api/v1/quizzes/courses/1?question_count=5').json()['questions']
    answers = {str(q['id']): (0 if index < 3 else 1) for index, q in enumerate(questions)}
    result = client.post('/api/v1/quizzes/courses/1/submit',
        json={'question_count': 5, 'answers': answers})
    assert result.status_code == 201
    body = result.json()
    assert (body['score'], body['total'], body['percentage']) == (3, 5, 60)
    assert [item['correct'] for item in body['feedback']] == [True, True, True, False, False]
    history = client.get('/api/v1/quizzes/courses/1/attempts').json()['attempts']
    assert (history[0]['score'], history[0]['total']) == (3, 5)


@pytest.mark.parametrize('count', [0, -1, 51, 101, 'five', '2.5'])
def test_invalid_or_unavailable_lengths_are_rejected(quiz_client, count):
    client, _ = quiz_client
    assert client.get(f'/api/v1/quizzes/courses/1?question_count={count}').status_code == 422


def test_cannot_submit_an_arbitrary_subset_or_change_denominator(quiz_client):
    client, _ = quiz_client
    questions = client.get('/api/v1/quizzes/courses/1?question_count=5').json()['questions']
    answers = {str(q['id']): 0 for q in questions}
    for body in (
        {'answers': answers},
        {'question_count': 10, 'answers': answers},
        {'question_count': 5, 'answers': dict(list(answers.items())[:-1])},
        {'question_count': 5, 'answers': {**answers, '999': 0}},
        {'question_count': 5, 'answers': {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}},
    ):
        assert client.post('/api/v1/quizzes/courses/1/submit', json=body).status_code == 422
    assert client.get('/api/v1/quizzes/courses/1/attempts').json()['attempts'] == []


@pytest.mark.parametrize('value', [True, '0', 0.5, -1, 2])
def test_invalid_answer_options_do_not_create_attempts(quiz_client, value):
    client, _ = quiz_client
    assert client.post('/api/v1/quizzes/courses/1/submit',
        json={'question_count': 1, 'answers': {'1': value}}).status_code == 422
    assert client.get('/api/v1/quizzes/courses/1/attempts').json()['attempts'] == []


def test_enrolment_and_role_required_for_all_quiz_operations(quiz_client):
    client, learner = quiz_client
    for path in ('options', 'attempts', ''):
        suffix = '/' + path if path else ''
        assert client.get('/api/v1/quizzes/courses/2' + suffix).status_code == 403
    learner.role = 'teacher'
    assert client.get('/api/v1/quizzes/courses/1/options').status_code == 403
    assert client.post('/api/v1/quizzes/courses/1/submit',
        json={'question_count': 1, 'answers': {'1': 0}}).status_code == 403
