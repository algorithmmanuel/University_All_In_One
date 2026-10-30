"""Strategy rules, saved HTTP boundaries and immutable practice snapshots.

SQLite fixtures override identity; PostgreSQL/concurrency has separate CI coverage.
"""
from copy import deepcopy
from types import SimpleNamespace
from uuid import uuid4
from collections import Counter
import pytest
import strategy_engine as engine
from cyber_content import BANK, TOPICS, lessons


def test_distinct_teaching_and_practice_content():
    assert len(BANK) == len({q['id'] for q in BANK}) == len({q['prompt'].casefold() for q in BANK}) == 500
    assert Counter(q['topic'] for q in BANK) == {key: 50 for key in TOPICS}
    modules = lessons()
    assert len(modules) == 3
    assert {s['id'] for m in modules for s in m['sections']} == set(TOPICS)
    for q in BANK:
        assert len(set(q['options'])) == 3 and 0 <= q['answer'] < 3
        assert q['explanation'] and q['module'] in {m['id'] for m in modules}
        section = next(s for m in modules for s in m['sections'] if s['id'] == q['topic'])
        assert any(c['reasoning'] == q['explanation'] for c in section['worked_cases'])
        assert q['source']['url'].startswith('https://')


def winning(seed='test'):
    state = engine.new_state(seed)
    for action, target in [('mfa', 'identity'), ('patch', 'app'), ('backup', 'backup')]:
        state = engine.advance(state, action, target)
    while state['status'] == 'active': state = engine.advance(state, 'end_turn')
    return state


def test_different_strategies_have_reproducible_consequences():
    assert winning()['status'] == 'won'
    ignored = engine.new_state('test')
    while ignored['status'] == 'active': ignored = engine.advance(ignored, 'end_turn')
    assert ignored['status'] == 'lost'
    assert winning() == winning()
    assert ignored['exposure'] >= 0


def test_staff_budget_delays_and_input_immutability():
    state = engine.new_state('test'); before = deepcopy(state)
    next_state = engine.advance(state, 'patch', 'app')
    assert state == before
    assert engine.availability(next_state) == 75 and not next_state['assets']['app']['patched']
    next_state = engine.advance(next_state, 'end_turn')
    assert next_state['assets']['app']['patched'] and engine.availability(next_state) == 100
    for target in ('gateway', 'staff', 'identity'): next_state = engine.advance(next_state, 'inspect', target)
    with pytest.raises(ValueError): engine.advance(next_state, 'inspect', 'app')
    next_state['budget'] = 0; next_state['staff'] = 3
    with pytest.raises(ValueError): engine.advance(next_state, 'monitor', 'app')


def test_hidden_state_and_observation_freshness():
    state = engine.new_state('test')
    state = engine.advance(state, 'inspect', 'staff')
    assert engine.public(state)['assets'][1]['condition'] == 'No compromise observed'
    state = engine.advance(state, 'end_turn')
    assert state['assets']['staff']['compromised']
    payload = engine.public(state)
    assert payload['assets'][1]['condition'] == 'Not investigated'
    assert 'seed' not in payload and 'compromised' not in repr(payload)
    state = engine.advance(state, 'monitor', 'staff')
    assert engine.public(state)['assets'][1]['condition'] == 'Compromise detected'


def test_containment_recovery_and_existing_compromise():
    state = engine.advance(engine.new_state('test'), 'end_turn')
    state = engine.advance(state, 'patch', 'staff')
    state = engine.advance(state, 'backup', 'backup')
    state = engine.advance(state, 'isolate', 'staff')
    state = engine.advance(state, 'end_turn')
    assert state['copy_ready'] and state['assets']['staff']['compromised']
    state = engine.advance(state, 'restore', 'staff')
    assert state['assets']['staff']['compromised']
    state = engine.advance(state, 'end_turn')
    assert not state['assets']['staff']['compromised'] and state['assets']['staff']['isolated']
    with pytest.raises(ValueError): engine.advance(state, 'mfa', 'staff')
    with pytest.raises(ValueError): engine.advance(winning(), 'end_turn')


@pytest.fixture
def lab_client():
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import StaticPool
    from database import Base
    from models import User
    import cyber_lab_routes as routes
    db_engine = create_engine('sqlite+pysqlite:///:memory:', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    Base.metadata.create_all(db_engine)
    Session = sessionmaker(bind=db_engine, expire_on_commit=False)
    with Session.begin() as db:
        for uid in (1, 2): db.add(User(id=uid, full_name='Synthetic', email=f'lab{uid}@example.invalid', password_hash='disabled', role='student'))
    user = SimpleNamespace(id=1, role='student')
    def get_db():
        with Session() as db: yield db
    app = FastAPI(); app.include_router(routes.router)
    app.dependency_overrides[routes.current_user] = lambda: user
    app.dependency_overrides[routes.get_db] = get_db
    with TestClient(app) as client: yield client, Session, user
    db_engine.dispose()


def post_command(client, run, action, target=None, **extra):
    return client.post(f"/api/v1/cyber-lab/runs/{run['id']}/commands", json={
        'command_id': str(uuid4()), 'expected_version': run['version'], 'action': action, 'target': target, **extra})


def test_http_command_deduplication_stale_state_and_reopening(lab_client):
    client, _, user = lab_client
    run = client.post('/api/v1/cyber-lab/runs').json()
    body = {'command_id': str(uuid4()), 'expected_version': 0, 'action': 'mfa', 'target': 'identity'}
    url = f"/api/v1/cyber-lab/runs/{run['id']}/commands"
    first = client.post(url, json=body)
    assert first.status_code == 200 and first.json()['budget'] == 26
    assert client.post(url, json=body).json() == first.json()
    assert client.post(url, json={**body, 'action': 'inspect'}).status_code == 409
    assert post_command(client, run, 'inspect', 'app').status_code == 409
    assert client.get(f"/api/v1/cyber-lab/runs/{run['id']}").json() == first.json()
    user.id = 2
    assert client.get(f"/api/v1/cyber-lab/runs/{run['id']}").status_code == 404
    assert client.post(url, json=body).status_code == 404
    assert client.get('/api/v1/cyber-lab/runs').json()['runs'] == []


@pytest.mark.parametrize('change', [{'expected_version': True}, {'score': 99}, {'command_id': 'bad'}, {'action': 'attack'}, {'target': 'missing'}])
def test_bad_commands_do_not_change_state(lab_client, change):
    client, _, _ = lab_client
    run = client.post('/api/v1/cyber-lab/runs').json()
    response = client.post(f"/api/v1/cyber-lab/runs/{run['id']}/commands", json={'command_id': str(uuid4()), 'expected_version': 0, 'action': 'inspect', 'target': 'app', **change})
    assert response.status_code == 422
    assert client.get(f"/api/v1/cyber-lab/runs/{run['id']}").json() == run


def test_practice_freshness_balance_pinned_grading_and_idempotency(lab_client, monkeypatch):
    from models import CyberPracticeSession
    import cyber_lab_routes as routes
    client, Session, user = lab_client
    first = client.post('/api/v1/cyber-lab/practice', json={'count': 10}).json()
    second = client.post('/api/v1/cyber-lab/practice', json={'count': 10}).json()
    assert len({q['topic'] for q in first['questions']}) == 10
    assert not {q['id'] for q in first['questions']}.intersection(q['id'] for q in second['questions'])
    assert all('answer' not in q and 'explanation' not in q for q in first['questions'])
    with Session() as db: pinned = deepcopy(db.get(CyberPracticeSession, first['id']).snapshot)
    monkeypatch.setattr(routes, 'BANK', [])
    answers = {q['id']: q['answer'] for q in pinned}
    url = f"/api/v1/cyber-lab/practice/{first['id']}/submit"
    result = client.post(url, json={'answers': answers})
    assert result.status_code == 200 and result.json()['result']['score'] == 10
    assert client.post(url, json={'answers': answers}).json() == result.json()
    changed = {**answers, pinned[0]['id']: (pinned[0]['answer'] + 1) % 3}
    assert client.post(url, json={'answers': changed}).status_code == 409
    assert client.get(f"/api/v1/cyber-lab/practice/{first['id']}").json() == result.json()
    user.id = 2
    assert client.post(url, json={'answers': answers}).status_code == 404
    assert client.get(f"/api/v1/cyber-lab/practice/{first['id']}").status_code == 404


@pytest.mark.parametrize('body', [{'count': True}, {'count': 21}, {'topic': 'unknown'}, {'difficulty': 'expert'}, {'topic': 'identity', 'difficulty': 'challenging', 'count': 11}, {'user_id': 2}])
def test_practice_rejects_unknown_and_out_of_bounds(lab_client, body):
    assert lab_client[0].post('/api/v1/cyber-lab/practice', json=body).status_code == 422


def test_practice_incomplete_forged_boolean_answers_and_study_scope(lab_client):
    client, _, user = lab_client
    practice = client.post('/api/v1/cyber-lab/practice', json={'count': 1}).json()
    url = f"/api/v1/cyber-lab/practice/{practice['id']}/submit"
    for answers in ({}, {'forged': 0}, {practice['questions'][0]['id']: True}, {practice['questions'][0]['id']: 5}):
        assert client.post(url, json={'answers': answers}).status_code == 422
    assert client.post('/api/v1/cyber-lab/study/unknown/complete').status_code == 404
    assert client.post('/api/v1/cyber-lab/study/protect/complete').status_code == 200
    assert client.post('/api/v1/cyber-lab/study/protect/complete').status_code == 200
    assert client.get('/api/v1/cyber-lab/catalog').json()['modules'][0]['completed']
    user.id = 2
    assert not client.get('/api/v1/cyber-lab/catalog').json()['modules'][0]['completed']


def test_role_and_unauthenticated_boundaries(lab_client):
    client, _, user = lab_client
    user.role = 'teacher'
    for method, path in [('GET', '/catalog'), ('POST', '/runs'), ('GET', '/practice')]:
        assert client.request(method, '/api/v1/cyber-lab'+path).status_code == 403
    client.app.dependency_overrides.clear()
    assert client.get('/api/v1/cyber-lab/catalog').status_code == 401
