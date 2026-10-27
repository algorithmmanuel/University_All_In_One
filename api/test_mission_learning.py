"""Actual mission/review HTTP handlers with synthetic SQLite and overridden identity.

These cases do not establish full authentication or PostgreSQL lock behaviour.
"""
from datetime import datetime, timezone
from types import SimpleNamespace
import pytest


@pytest.fixture
def mission_client():
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import StaticPool
    from database import Base
    from models import MissionRun, User
    import mission_routes
    engine = create_engine('sqlite+pysqlite:///:memory:', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    Base.metadata.create_all(engine)
    with Session.begin() as db:
        for user_id in (1, 2):
            db.add(User(id=user_id, full_name='Synthetic learner', email=f'mission{user_id}@example.invalid', password_hash='disabled', role='student'))
        db.flush()
        # Historic completed and partially completed runs, with existing scores.
        db.add(MissionRun(id=1, user_id=1, mission_id='phishing-investigation', step_index=3, score=20,
                          choices=[{'feedback': 'Historic feedback', 'points': 20}], completed_at=datetime.now(timezone.utc)))
        db.add(MissionRun(id=2, user_id=1, mission_id='phishing-investigation', step_index=1, score=10,
                          choices=[{'feedback': 'Historic stage', 'points': 10}]))
    learner = SimpleNamespace(id=1, role='student')
    def get_db():
        with Session() as db:
            yield db
    app = FastAPI()
    app.include_router(mission_routes.router)
    app.dependency_overrides[mission_routes.current_user] = lambda: learner
    app.dependency_overrides[mission_routes.get_db] = get_db
    with TestClient(app) as client:
        yield client, Session, learner
    engine.dispose()


def test_pilot_three_stage_journey_retains_server_scoring_and_withholds_review(mission_client):
    from mission_learning import FINDING_EXPLANATIONS, STAGES
    client, _, _ = mission_client
    response = client.post('/api/v1/missions/phishing-investigation/start')
    assert response.status_code == 201
    run = response.json()
    for stage, (option, finding) in enumerate([(0, 2), (1, 1), (2, 0)]):
        assert run['step_index'] == stage and run['max_score'] == 45
        learning = run['learning']
        assert len(learning['objectives']) == 3 and len(learning['workflow']) == 4
        assert learning['review'] == [] and learning['stage'] == STAGES[stage]
        assert len(learning['stage']['artifacts']) == len(run['step']['evidence'])
        assert len(learning['stage']['hints']) == 2
        for item in learning['stage']['artifacts']:
            assert item['title'] and item['body']
        assert 'points' not in run['step'] and 'feedback' not in run['step']
        assert all(isinstance(option, str) for option in run['step']['options'])
        run = client.post(f"/api/v1/missions/runs/{run['run_id']}/decide", json={
            'option_index': option, 'finding_index': finding, 'expected_step': stage}).json()
        assert FINDING_EXPLANATIONS[stage] in run['last_feedback']
    assert run['completed'] and run['score'] == run['max_score'] == 45
    assert run['learning']['stage'] is None and len(run['learning']['review']) == 5
    assert all(set(question) == {'id', 'prompt', 'options'} for question in run['learning']['review'])
    assert client.post(f"/api/v1/missions/runs/{run['run_id']}/decide", json={'option_index': 0, 'expected_step': 3}).status_code == 409


def test_historic_runs_review_all_choices_without_mutation(mission_client):
    from models import MissionRun
    from mission_learning import REVIEW
    client, Session, _ = mission_client
    historic = client.get('/api/v1/missions/runs/1').json()
    assert historic['completed'] and historic['score'] == 20 and historic['last_feedback'] == 'Historic feedback'
    for question in REVIEW:
        for index, explanation in enumerate(question['feedback']):
            response = client.post('/api/v1/missions/runs/1/review', json={'question_id': question['id'], 'option_index': index})
            assert response.status_code == 200
            assert response.json() == {'question_id': question['id'], 'correct': index == question['answer'], 'explanation': explanation}
    assert client.get('/api/v1/missions/runs/1').json() == historic
    partial = client.get('/api/v1/missions/runs/2').json()
    assert (partial['step_index'], partial['score'], partial['last_feedback']) == (1, 10, 'Historic stage')
    assert partial['learning']['stage']['task']
    with Session() as db:
        assert len(db.get(MissionRun, 1).choices) == 1 and len(db.get(MissionRun, 2).choices) == 1


@pytest.mark.parametrize('body', [
    {'question_id': 'unknown', 'option_index': 0},
    {'question_id': 'pressure', 'option_index': 3},
    {'question_id': 'pressure', 'option_index': -1},
    {'question_id': 'pressure', 'option_index': True},
    {'question_id': 'pressure', 'option_index': '1'},
    {'question_id': 'pressure', 'option_index': 1.5},
    {'question_id': 'pressure', 'option_index': 1, 'score': 100},
    {'question_id': '', 'option_index': 0},
])
def test_invalid_review_rejected(mission_client, body):
    client, _, _ = mission_client
    assert client.post('/api/v1/missions/runs/1/review', json=body).status_code == 422


def test_review_completion_ownership_role_and_legacy_boundaries(mission_client):
    client, _, learner = mission_client
    body = {'question_id': 'pressure', 'option_index': 1}
    assert client.post('/api/v1/missions/runs/2/review', json=body).status_code == 409
    assert client.post('/api/v1/missions/runs/999/review', json=body).status_code == 404
    learner.id = 2
    assert client.post('/api/v1/missions/runs/1/review', json=body).status_code == 404
    learner.id = 1
    learner.role = 'teacher'
    assert client.post('/api/v1/missions/runs/1/review', json=body).status_code == 403
    learner.role = 'student'
    legacy = client.post('/api/v1/missions/password-fortress/start').json()
    assert legacy['learning'] is None
    assert client.post(f"/api/v1/missions/runs/{legacy['run_id']}/review", json=body).status_code == 404


def test_all_existing_missions_still_finish(mission_client):
    from mission_data import MISSIONS
    client, _, _ = mission_client
    for mission_id, mission in MISSIONS.items():
        run = client.post(f'/api/v1/missions/{mission_id}/start').json()
        for stage, step in enumerate(mission['steps']):
            response = client.post(f"/api/v1/missions/runs/{run['run_id']}/decide", json={'option_index': 0, 'expected_step': stage})
            assert response.status_code == 200, mission_id
            run = response.json()
        assert run['completed'] and run['step_index'] == len(mission['steps'])
