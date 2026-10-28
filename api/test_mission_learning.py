"""Actual mission/review HTTP handlers with synthetic SQLite and overridden identity.

These cases do not establish full authentication or PostgreSQL lock behaviour.
"""
from datetime import datetime, timezone
from types import SimpleNamespace
import pytest
from mission_learning import GUIDES


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


@pytest.fixture(params=list(GUIDES))
def guided_client(mission_client, request):
    from mission_learning import GUIDES
    from models import MissionRun
    client, Session, learner = mission_client
    guide = GUIDES[request.param]
    with Session.begin() as db:
        for run_id in (1, 2):
            db.get(MissionRun, run_id).mission_id = guide.MISSION_ID
    return client, Session, learner, guide


def test_guided_three_stage_journey_retains_server_scoring_and_withholds_review(guided_client):
    client, _, _, guide = guided_client
    decisions = {
        'phishing-investigation': [(0, 2), (1, 1), (2, 0)],
        'password-fortress': [(0, 0), (1, 1), (2, 0)],
        'soc-alert-triage': [(1, 1), (0, 0), (2, 0)],
        'privacy-patrol': [(0, 1), (1, 2), (2, 1)],
        'scam-spotter': [(0, 1), (1, 1), (2, 0)],
        'safe-social': [(0, 1), (1, 2), (2, 1)],
        'device-defender': [(0, 1), (1, 0), (2, 1)],
        'wifi-wise': [(0, 0), (1, 0), (2, 1)],
        'digital-footprints': [(0, 1), (1, 1), (2, 0)],
        'mfa-guardian': [(0, 1), (1, 0), (2, 1)],
        'backup-buddy': [(0, 0), (1, 0), (2, 1)],
        'operation-firewall': [(0, 1), (1, 0), (2, 2)],
        'network-watch': [(1, 1), (0, 2), (2, 0)],
        'web-defense': [(0, 1), (1, 0), (2, 1)],
        'cloud-perimeter': [(0, 1), (1, 0), (2, 2)],
        'forensics-desk': [(0, 1), (1, 0), (2, 2)],
        'malware-clues': [(0, 0), (1, 0), (2, 1)],
        'identity-lab': [(0, 1), (1, 0), (2, 1)],
        'secure-code-review': [(0, 0), (1, 0), (2, 1)],
        'threat-hunter': [(0, 0), (1, 0), (2, 0)],
        'incident-response': [(0, 0), (1, 0), (2, 1)],
        'risk-command': [(1, 1), (0, 0), (2, 2)],
        'zero-trust-briefing': [(0, 1), (1, 2), (2, 1)],
        'cloud-incident': [(0, 1), (1, 0), (2, 2)],
        'supply-chain-watch': [(0, 1), (1, 0), (2, 2)],
        'ransomware-recovery': [(0, 1), (1, 2), (2, 0)],
        'identity-crisis': [(0, 1), (1, 0), (2, 1)],
    }
    response = client.post(f'/api/v1/missions/{guide.MISSION_ID}/start')
    assert response.status_code == 201
    run = response.json()
    for stage, (option, finding) in enumerate(decisions[guide.MISSION_ID]):
        assert run['step_index'] == stage and run['max_score'] == 45
        learning = run['learning']
        assert len(learning['objectives']) == 3 and len(learning['workflow']) == 4
        assert learning['revision'] == guide.REVISION
        assert learning['review'] == [] and learning['stage'] == guide.STAGES[stage]
        assert len(learning['stage']['artifacts']) == len(run['step']['evidence'])
        assert len(learning['stage']['hints']) == 2
        for item in learning['stage']['artifacts']:
            assert item['title'] and item['body']
        assert 'points' not in run['step'] and 'feedback' not in run['step']
        assert all(isinstance(option, str) for option in run['step']['options'])
        run = client.post(f"/api/v1/missions/runs/{run['run_id']}/decide", json={
            'option_index': option, 'finding_index': finding, 'expected_step': stage}).json()
        assert guide.FINDING_EXPLANATIONS[stage] in run['last_feedback']
    assert run['completed'] and run['score'] == run['max_score'] == 45
    assert run['learning']['stage'] is None and len(run['learning']['review']) == 5
    assert all(set(question) == {'id', 'prompt', 'options'} for question in run['learning']['review'])
    assert client.post(f"/api/v1/missions/runs/{run['run_id']}/decide", json={'option_index': 0, 'expected_step': 3}).status_code == 409


def test_historic_runs_review_all_choices_without_mutation(guided_client):
    from models import MissionRun
    client, Session, _, guide = guided_client
    historic = client.get('/api/v1/missions/runs/1').json()
    assert historic['completed'] and historic['score'] == 20 and historic['last_feedback'] == 'Historic feedback'
    for question in guide.REVIEW:
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


@pytest.mark.parametrize('change', [
    {'question_id': 'unknown'}, {'option_index': 3}, {'option_index': -1},
    {'option_index': True}, {'option_index': '1'}, {'option_index': 1.5},
    {'score': 100}, {'question_id': ''},
])
def test_invalid_review_rejected(guided_client, change):
    client, _, _, guide = guided_client
    body = {'question_id': guide.REVIEW[0]['id'], 'option_index': 0, **change}
    assert client.post('/api/v1/missions/runs/1/review', json=body).status_code == 422


def test_review_completion_ownership_role_and_legacy_boundaries(guided_client):
    client, _, learner, guide = guided_client
    body = {'question_id': guide.REVIEW[0]['id'], 'option_index': 1}
    assert client.post('/api/v1/missions/runs/2/review', json=body).status_code == 409
    assert client.post('/api/v1/missions/runs/999/review', json=body).status_code == 404
    learner.id = 2
    assert client.post('/api/v1/missions/runs/1/review', json=body).status_code == 404
    learner.id = 1
    learner.role = 'teacher'
    assert client.post('/api/v1/missions/runs/1/review', json=body).status_code == 403
    learner.role = 'student'
    # Unsupported review applies only while unregistered guides remain. Choose
    # from source so adding a guide cannot silently invalidate this boundary case.
    from mission_data import MISSIONS
    legacy_id = next((key for key in MISSIONS if key not in GUIDES), None)
    if legacy_id is not None:
        legacy = client.post(f'/api/v1/missions/{legacy_id}/start').json()
        assert legacy['learning'] is None
        assert client.post(f"/api/v1/missions/runs/{legacy['run_id']}/review", json=body).status_code == 404


def test_review_questions_cannot_cross_mission_boundaries(guided_client):
    from mission_learning import GUIDES
    client, _, _, guide = guided_client
    for other in GUIDES.values():
        if other.MISSION_ID != guide.MISSION_ID:
            response = client.post('/api/v1/missions/runs/1/review', json={
                'question_id': other.REVIEW[0]['id'], 'option_index': 0})
            assert response.status_code == 422


def test_guides_match_engine_and_public_data_never_contains_keys():
    from mission_data import MISSIONS
    from mission_learning import GUIDES, public_learning
    prompts = []
    forbidden = {'answer', 'correct_index', 'feedback', 'points', 'finding_key', 'FINDING_EXPLANATIONS'}
    def check_keys(value):
        if isinstance(value, dict):
            assert not forbidden.intersection(value)
            for item in value.values(): check_keys(item)
        elif isinstance(value, list):
            for item in value: check_keys(item)
    for mission_id, guide in GUIDES.items():
        mission = MISSIONS[mission_id]
        assert len(guide.STAGES) == len(guide.FINDING_EXPLANATIONS) == len(mission['steps']) == 3
        assert guide.BRIEFING['revision'] == guide.REVISION
        assert len(guide.REVIEW) == 5 and len({q['id'] for q in guide.REVIEW}) == 5
        for i, stage in enumerate(guide.STAGES):
            assert len(stage['artifacts']) == len(mission['steps'][i]['evidence'])
            assert stage['task'] and len(stage['hints']) == 2 and all(stage['hints'])
            check_keys(public_learning(mission_id, i, False))
        check_keys(public_learning(mission_id, 3, True))
        for question in guide.REVIEW:
            assert 0 <= question['answer'] < len(question['options'])
            assert len(question['feedback']) == len(question['options']) and all(question['feedback'])
            assert len(set(question['options'])) == len(question['options'])
            prompts.append(question['prompt'].strip().casefold())
    assert len(prompts) == len(set(prompts)), 'Accidental repeated review prompts'


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
