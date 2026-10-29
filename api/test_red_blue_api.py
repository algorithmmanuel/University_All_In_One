"""Real bearer HTTP boundaries; SQLite for sequential tests, isolated PG for races.

No authentication overrides: each request resolves a distinct hashed session.
"""
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, delete, select, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database import Base
from models import User, AuthSession, BetaInvite, RedBlueMatch, RedBlueSeat, RedBlueReceipt
from auth import issue_session
import red_blue_routes as routes


@pytest.fixture(params=['sqlite', 'postgres'])
def arena(request, monkeypatch):
    monkeypatch.delenv('EDUCYBER_PRIVATE_BETA', raising=False)
    if request.param == 'postgres':
        url = os.getenv('TEST_DATABASE_URL')
        if not url:
            pytest.skip('Isolated PostgreSQL required')
        from sqlalchemy.engine import make_url
        p = make_url(url)
        if not (p.drivername.startswith('postgresql') and p.database == 'educyber_test'
                and p.host in ('localhost', '127.0.0.1') and os.getenv('DATABASE_URL') == url):
            pytest.fail('Refusing non-isolated PostgreSQL')
        e = create_engine(url)
    else:
        e = create_engine('sqlite://', poolclass=StaticPool, connect_args={'check_same_thread': False})
        @event.listens_for(e, 'connect')
        def foreign_keys(connection, _):
            connection.execute('PRAGMA foreign_keys=ON')
    Base.metadata.create_all(e)
    Session = sessionmaker(bind=e, expire_on_commit=False)
    ids, headers = [], []
    for role in ('student', 'student', 'student', 'teacher', 'admin'):
        with Session() as db:
            user = User(full_name='Synthetic simulator learner', email=f'{uuid4().hex}@example.invalid',
                        password_hash='disabled', role=role, age_band='adult', is_active=True, is_approved=True)
            db.add(user); db.flush(); ids.append(user.id)
            headers.append({'Authorization': 'Bearer ' + issue_session(db, user)})
    app = FastAPI(); app.include_router(routes.router)
    def get_db():
        with Session() as db:
            yield db
    app.dependency_overrides[routes.get_db] = get_db
    with TestClient(app) as client:
        yield client, headers, ids, Session, app, request.param
    with Session.begin() as db:
        db.execute(delete(RedBlueMatch).where(RedBlueMatch.creator_id.in_(ids)))
        db.execute(delete(AuthSession).where(AuthSession.user_id.in_(ids)))
        db.execute(delete(BetaInvite).where(BetaInvite.redeemed_by.in_(ids)))
        db.execute(delete(User).where(User.id.in_(ids)))
    e.dispose()


def create(arena, mode='human', side='red', scenario='microfinance'):
    c, h, *_ = arena
    response = c.post('/api/v1/red-blue/matches', headers=h[0], json={
        'scenario': scenario, 'side': side, 'mode': mode})
    assert response.status_code == 201, response.text
    return response.json()


def paired(arena):
    c, h, *_ = arena
    match = create(arena)
    path = f"/api/v1/red-blue/matches/{match['id']}"
    token = c.post(path+'/invite', headers=h[0]).json()['token']
    assert c.post('/api/v1/red-blue/join', json={'token': token}, headers=h[1]).status_code == 200
    return path


def order(side='red', turn=1, **kw):
    return {'command_id': str(uuid4()), 'expected_turn': turn, 'action': f'wait_{side}', **kw}


def test_auth_eligibility_and_participant_policy(arena, monkeypatch):
    c, h, ids, Session, *_ = arena
    assert c.get('/api/v1/red-blue/catalog').status_code == 401
    for header in h[3:]:
        assert c.get('/api/v1/red-blue/catalog', headers=header).status_code == 403
    path = paired(arena)
    for suffix in ('', '/debrief'):
        assert c.get(path+suffix, headers=h[2]).status_code == 404
    assert c.post(path+'/commands', headers=h[2], json=order()).status_code == 404
    assert c.post(path+'/invite', headers=h[2]).status_code == 404
    assert c.get('/api/v1/red-blue/matches', headers=h[2]).json()['matches'] == []
    monkeypatch.setenv('EDUCYBER_PRIVATE_BETA', 'enabled')
    assert c.get(path, headers=h[0]).status_code == 403
    with Session.begin() as db:
        db.add(BetaInvite(code_hash=uuid4().hex, expires_at=datetime.now(timezone.utc)+timedelta(days=1), redeemed_by=ids[0]))
    assert c.get(path, headers=h[0]).status_code == 200
    with Session.begin() as db:
        db.execute(delete(AuthSession).where(AuthSession.user_id == ids[0]))
    assert c.get(path, headers=h[0]).status_code == 401


def test_invitations_rotate_expire_bind_once_and_wait(arena):
    c, h, _, Session, *_ = arena
    m = create(arena); path = f"/api/v1/red-blue/matches/{m['id']}"
    assert m['status'] == 'waiting' and m['orders'] == []
    assert c.post(path+'/commands', headers=h[0], json=order()).status_code == 409
    old = c.post(path+'/invite', headers=h[0]).json()['token']
    new = c.post(path+'/invite', headers=h[0]).json()['token']
    assert old != new
    assert c.post('/api/v1/red-blue/join', headers=h[1], json={'token': old}).status_code == 404
    assert c.post('/api/v1/red-blue/join', headers=h[0], json={'token': new}).status_code == 409
    with Session.begin() as db:
        db.get(RedBlueMatch, m['id']).invite_expires_at = datetime.now(timezone.utc)-timedelta(seconds=1)
    assert c.post('/api/v1/red-blue/join', headers=h[1], json={'token': new}).status_code == 404
    token = c.post(path+'/invite', headers=h[0]).json()['token']
    joined = c.post('/api/v1/red-blue/join', headers=h[1], json={'token': token})
    assert joined.json()['side'] == 'blue'
    assert c.post('/api/v1/red-blue/join', headers=h[2], json={'token': token}).status_code == 404
    assert c.post(path+'/invite', headers=h[0]).status_code == 409
    with Session() as db:
        row = db.get(RedBlueMatch, m['id'])
        assert row.invite_hash is None and row.invite_expires_at is None
        assert len(db.scalars(select(RedBlueSeat).where(RedBlueSeat.match_id == m['id'])).all()) == 2


def test_hidden_choice_idempotency_stale_and_atomic_resolution(arena):
    c, h, _, Session, *_ = arena
    path = paired(arena)
    before = c.get(path, headers=h[1]).json()
    red = order(action='phish', target='staff')
    # Use an offered attack instead of assuming the scenario's asset naming.
    offered = c.get(path, headers=h[0]).json()['orders']
    red.update(next(o for o in offered if o['action'] == 'phish'))
    sealed = c.post(path+'/commands', headers=h[0], json=red)
    assert sealed.status_code == 200, sealed.text
    assert sealed.json()['committed'] and sealed.json()['turn'] == 1
    blue = c.get(path, headers=h[1]).json()
    for key in ('assets', 'observations', 'committed_order', 'orders', 'budget'):
        assert blue[key] == before[key]
    for response in (sealed, c.get(path, headers=h[1])):
        assert response.headers['cache-control'] == 'no-store'
        assert not {'seed', 'transcript', 'seats', 'timeline', 'receipts', 'plans', 'rules_digest'} & response.json().keys()
    assert c.get(path+'/debrief', headers=h[1]).status_code == 409
    assert c.post(path+'/commands', headers=h[0], json=red).json() == sealed.json()
    assert c.post(path+'/commands', headers=h[0], json={**red, 'action': 'wait_red'}).status_code == 409
    assert c.post(path+'/commands', headers=h[0], json=order()).status_code == 409
    resolved = c.post(path+'/commands', headers=h[1], json=order('blue')).json()
    assert resolved['turn'] == 2 and resolved['version'] == 2
    assert c.post(path+'/commands', headers=h[0], json=order()).status_code == 409
    # Retrying an acknowledged old command returns current projection, no new effect.
    assert c.post(path+'/commands', headers=h[0], json=red).json()['turn'] == 2
    with Session() as db:
        row = db.get(RedBlueMatch, resolved['id'])
        match = routes.restore(row)
        assert [e['side'] for e in match.timeline] == ['blue', 'red']
        assert len(match.history) == 1 and len(match.receipts) == 2
        assert len(db.scalars(select(RedBlueReceipt).where(RedBlueReceipt.match_id == row.id)).all()) == 2


@pytest.mark.parametrize('side', ['red', 'blue'])
def test_computer_resume_complete_and_debrief_without_private_seed(arena, side):
    c, h, *_ = arena
    m = create(arena, 'computer', side)
    path = f"/api/v1/red-blue/matches/{m['id']}"
    while not m['winner']:
        m = c.post(path+'/commands', headers=h[0], json=order(side, m['turn'])).json()
    assert m['winner'] in ('red', 'blue') and m['status'] == 'finished'
    result = c.get(path+'/debrief', headers=h[0])
    assert result.status_code == 200 and result.json()['timeline']
    assert 'seed' not in result.json() and 'roll' not in repr(result.json())
    assert c.post(path+'/commands', headers=h[0], json=order(side, m['turn'])).status_code == 409
    assert c.get(path, headers=h[0]).json() == m


@pytest.mark.parametrize('change', [{'expected_turn': True}, {'expected_turn': 31}, {'command_id': 'bad'},
    {'action': 'x'*31}, {'target': '../private'}, {'seed': 'forged'}, {'user_id': 2}, {'side': 'blue'}])
def test_bounded_commands_reject_forgery(arena, change):
    c, h, *_ = arena
    m = create(arena, 'computer')
    assert c.post(f"/api/v1/red-blue/matches/{m['id']}/commands", headers=h[0], json={**order(), **change}).status_code == 422


def test_resolution_failure_rolls_back_both_commit_and_receipt(arena, monkeypatch):
    c, h, _, Session, *_ = arena
    path = paired(arena)
    assert c.post(path+'/commands', headers=h[0], json=order()).status_code == 200
    original = routes.engine._finish_round
    def fail(match):
        original(match)
        raise RuntimeError('synthetic storage failure')
    with monkeypatch.context() as patch:
        patch.setattr(routes.engine, '_finish_round', fail)
        with pytest.raises(RuntimeError):
            c.post(path+'/commands', headers=h[1], json=order('blue'))
    m = c.get(path, headers=h[1]).json()
    assert m['turn'] == 1 and not m['committed']
    with Session() as db:
        row = db.get(RedBlueMatch, m['id'])
        assert len(row.transcript['commands']) == 1 and row.transcript['rounds'] == []
        assert len(db.scalars(select(RedBlueReceipt).where(RedBlueReceipt.match_id == m['id'])).all()) == 1
    assert c.post(path+'/commands', headers=h[1], json=order('blue')).json()['turn'] == 2


def test_postgres_two_actual_sessions_concurrent_submissions(arena):
    c, h, _, Session, app, dialect = arena
    if dialect != 'postgres':
        pytest.skip('SQLite does not prove row locking')
    path = paired(arena)
    from threading import Barrier
    def race(commands):
        barrier = Barrier(len(commands))
        def submit(item):
            header, body = item
            with TestClient(app) as client:
                barrier.wait(timeout=10)
                return client.post(path+'/commands', headers=header, json=body)
        with ThreadPoolExecutor(max_workers=len(commands)) as pool:
            return list(pool.map(submit, commands))
    red, blue = order(), order('blue')
    red.update(next(o for o in c.get(path, headers=h[0]).json()['orders'] if o['action'] == 'recon'))
    blue.update(next(o for o in c.get(path, headers=h[1]).json()['orders'] if o['action'] == 'monitor'))
    responses = race([(h[0], red), (h[1], blue), (h[0], red), (h[1], blue)])
    assert [r.status_code for r in responses] == [200]*4
    m = c.get(path, headers=h[0]).json()
    assert (m['turn'], m['version']) == (2, 2)
    responses = race([(h[0], order(turn=2)), (h[0], order(turn=2))])
    assert sorted(r.status_code for r in responses) == [200, 409]
    assert c.post(path+'/commands', headers=h[1], json=order('blue', 2)).json()['turn'] == 3
    with Session() as db:
        row = db.get(RedBlueMatch, m['id'])
        saved = routes.restore(row)
        assert len(saved.history) == 2 and len(saved.receipts) == 4
        assert [e['side'] for e in saved.timeline] == ['blue', 'red']*2
        assert saved.budgets == {'red': 23, 'blue': 23}


def test_postgres_concurrent_join_claims_one_seat(arena):
    c, h, _, Session, app, dialect = arena
    if dialect != 'postgres':
        pytest.skip('SQLite does not prove row locking')
    m = create(arena); path = f"/api/v1/red-blue/matches/{m['id']}"
    token = c.post(path+'/invite', headers=h[0]).json()['token']
    from threading import Barrier
    barrier = Barrier(2)
    def join(header):
        with TestClient(app) as client:
            barrier.wait(timeout=10)
            return client.post('/api/v1/red-blue/join', headers=header, json={'token': token})
    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(pool.map(join, h[1:3]))
    assert sorted(r.status_code for r in responses) == [200, 404]
    with Session() as db:
        seats = db.scalars(select(RedBlueSeat).where(RedBlueSeat.match_id == m['id'])).all()
        assert len(seats) == 2 and len({s.user_id for s in seats}) == 2


def test_catalog_contains_summaries_and_all_scenarios_start(arena):
    c, h, *_ = arena
    catalog = c.get('/api/v1/red-blue/catalog', headers=h[0])
    assert catalog.status_code == 200
    assert len(catalog.json()['scenarios']) == 6 and len(catalog.json()['actions']) == 20
    for scenario in catalog.json()['scenarios']:
        assert set(scenario) == {'id', 'title', 'industry', 'difficulty', 'turn_limit'}
        create(arena, 'computer', scenario=scenario['id'])
    assert c.post('/api/v1/red-blue/matches', headers=h[0], json={'scenario': 'unknown', 'side': 'red'}).status_code == 422


def test_database_failure_rolls_back_resolved_state_and_receipt(arena):
    c, h, _, Session, *_ = arena
    path = paired(arena)
    c.post(path+'/commands', headers=h[0], json=order())
    def fail(*_):
        from sqlalchemy.exc import OperationalError
        raise OperationalError('synthetic insert', {'seed': 'private-sentinel'}, Exception('synthetic database failure'))
    event.listen(RedBlueReceipt, 'after_insert', fail)
    body = order('blue')
    try:
        response = c.post(path+'/commands', headers=h[1], json=body)
        assert response.status_code == 503
        assert 'private-sentinel' not in response.text and 'synthetic insert' not in response.text
    finally:
        event.remove(RedBlueReceipt, 'after_insert', fail)
    m = c.get(path, headers=h[1]).json()
    assert m['turn'] == 1 and m['version'] == 1 and not m['committed']
    with Session() as db:
        assert len(db.scalars(select(RedBlueReceipt).where(RedBlueReceipt.match_id == m['id'])).all()) == 1
    assert c.post(path+'/commands', headers=h[1], json=body).json()['turn'] == 2


def test_raw_body_limit_applies_before_json_parsing(arena):
    c, h, *_ = arena
    # A streamed body need not provide a trustworthy Content-Length.
    response = c.post('/api/v1/red-blue/join', headers={**h[0], 'Content-Type': 'application/json'},
                      content=iter([b'{"token":"', b'x' * 4096, b'"}']))
    assert response.status_code == 413
    assert response.json()['detail'] == 'Simulator request is too large'
    assert c.get('/api/v1/red-blue/catalog', headers=h[0]).status_code == 200
