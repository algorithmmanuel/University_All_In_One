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


# Versioned V2 route-preview gates: inherited bearer auth and original PG locking.
def test_alternating_preview_is_denied_outside_isolated_development(arena, monkeypatch):
    c, h, *_ = arena
    monkeypatch.setenv('EDUCYBER_ENV', 'beta')
    assert c.get('/api/v1/red-blue/catalog', headers=h[0]).json()['alternating_preview_available'] is False
    response = c.post('/api/v1/red-blue/matches', headers=h[0], json={
        'scenario': 'microfinance', 'side': 'blue', 'mode': 'human',
        'ruleset': 'alternating_preview'})
    assert response.status_code == 403
    assert c.post('/api/v1/red-blue/matches', headers=h[0], json={
        'scenario': 'microfinance', 'side': 'blue', 'mode': 'computer'}).status_code == 201


def test_v2_two_authenticated_seats_blue_first_immediate_effect_and_secrecy(arena, monkeypatch):
    monkeypatch.setenv('EDUCYBER_ENV', 'development')
    c, h, _, Session, *_ = arena
    assert c.get('/api/v1/red-blue/catalog', headers=h[0]).json()['alternating_preview_available'] is True
    created = c.post('/api/v1/red-blue/matches', headers=h[0], json={
        'scenario': 'microfinance', 'side': 'red', 'mode': 'human',
        'ruleset': 'alternating_preview'})
    assert created.status_code == 201, created.text
    row = created.json()
    assert row['status'] == 'waiting'
    path = f"/api/v1/red-blue/matches/{row['id']}"
    token = c.post(path + '/invite', headers=h[0]).json()['token']
    joined = c.post('/api/v1/red-blue/join', headers=h[1], json={'token': token})
    assert joined.status_code == 200, joined.text
    blue = joined.json()
    assert blue['active_side'] == 'blue'
    assert blue['orders'] and blue['version'] == 0
    assert c.post(path + '/commands', headers=h[0], json=order('red')).status_code == 409
    monitor = next(x for x in blue['orders'] if x['action'] == 'monitor')
    action = {**order('blue'), **monitor}
    resolved = c.post(path + '/commands', headers=h[1], json=action)
    assert resolved.status_code == 200, resolved.text
    after_blue = resolved.json()
    assert (after_blue['turn'], after_blue['version']) == (1, 1)
    assert after_blue['active_side'] == 'red'
    assert after_blue['orders'] == [] and after_blue['committed_order'] is None
    red = c.get(path, headers=h[0]).json()
    assert red['active_side'] == 'red' and red['orders']
    assert red['committed_order'] is None
    assert not {'seed', 'transcript', 'timeline', 'plans', 'receipts', 'moves'} & red.keys()
    assert all('controls' not in a for a in red['assets'])
    same = c.post(path + '/commands', headers=h[1], json=action)
    assert same.status_code == 200 and same.json()['version'] == 1
    assert c.post(path + '/commands', headers=h[1], json={
        **action, 'action': 'wait_blue'}).status_code == 409
    red_reply = c.post(path + '/commands', headers=h[0], json=order('red'))
    assert red_reply.status_code == 200, red_reply.text
    assert red_reply.json()['turn'] == 2 and red_reply.json()['version'] == 2
    with Session() as db:
        saved = db.get(RedBlueMatch, row['id'])
        assert saved.transcript['edition'] == routes.v2_alternating.EDITION
        assert len(saved.transcript['moves']) == 2
        assert len(db.scalars(select(RedBlueReceipt).where(
            RedBlueReceipt.match_id == row['id'])).all()) == 2
    assert c.get(path, headers=h[2]).status_code == 404


@pytest.mark.parametrize('side', ['blue', 'red'])
def test_v2_development_preview_computer_acts_immediately(arena, monkeypatch, side):
    monkeypatch.setenv('EDUCYBER_ENV', 'development')
    c, h, *_ = arena
    response = c.post('/api/v1/red-blue/matches', headers=h[0], json={
        'scenario': 'microfinance', 'side': side, 'mode': 'computer',
        'ruleset': 'alternating_preview'})
    assert response.status_code == 201, response.text
    view = response.json()
    assert view['active_side'] == side
    assert view['status'] == 'active'
    assert view['version'] == (1 if side == 'red' else 0)
    cmd = order(side, view['turn'])
    result = c.post(f"/api/v1/red-blue/matches/{view['id']}/commands",
                    headers=h[0], json=cmd)
    assert result.status_code == 200, result.text
    after = result.json()
    assert after['active_side'] == side and after['turn'] >= 2
    assert after['version'] == view['version'] + 2
    assert c.post(f"/api/v1/red-blue/matches/{view['id']}/commands",
                  headers=h[0], json=cmd).json()['version'] == after['version']


def test_timed_preview_is_forbidden_in_beta_and_visible_only_in_dev(arena, monkeypatch):
    c, h, *_ = arena
    monkeypatch.setenv('EDUCYBER_ENV', 'beta')
    assert c.get('/api/v1/red-blue/catalog', headers=h[0]).json()['timed_preview_available'] is False
    refused = c.post('/api/v1/red-blue/matches', headers=h[0], json={
        'scenario': 'microfinance', 'side': 'blue', 'mode': 'computer',
        'ruleset': 'timed_preview'})
    assert refused.status_code == 403
    monkeypatch.setenv('EDUCYBER_ENV', 'development')
    assert c.get('/api/v1/red-blue/catalog', headers=h[0]).json()['timed_preview_available'] is True


def test_timed_two_user_join_heartbeat_immediate_turn_and_private_replay(arena, monkeypatch):
    monkeypatch.setenv('EDUCYBER_ENV', 'development')
    c, h, _, Session, *_ = arena
    response = c.post('/api/v1/red-blue/matches', headers=h[0], json={
        'scenario': 'microfinance', 'side': 'red', 'mode': 'human',
        'ruleset': 'timed_preview'})
    assert response.status_code == 201, response.text
    waiting = response.json()
    assert waiting['status'] == 'waiting' and waiting['orders'] == []
    path = f"/api/v1/red-blue/matches/{waiting['id']}"
    token = c.post(path + '/invite', headers=h[0]).json()['token']
    joined = c.post('/api/v1/red-blue/join', headers=h[1], json={'token': token})
    assert joined.status_code == 200, joined.text
    blue = joined.json()
    assert blue['active_side'] == 'blue'
    assert blue['clock']['seconds_remaining'] <= 90
    assert blue['clock']['seconds_remaining'] > 0
    assert blue['clock']['deadline_at'] > 0
    assert 'last_seen_blue' not in blue['clock']
    heartbeat = c.post(path + '/heartbeat', headers=h[1], json={'expected_round': 1})
    assert heartbeat.status_code == 200, heartbeat.text
    assert heartbeat.json()['clock']['deadline_at'] == blue['clock']['deadline_at']
    assert c.post(path + '/heartbeat', headers=h[0],
                  json={'expected_round': 1}).status_code == 409
    action = order('blue')
    first = c.post(path + '/commands', headers=h[1], json=action)
    assert first.status_code == 200, first.text
    assert first.json()['active_side'] == 'red'
    assert first.json()['turn'] == 1
    assert first.json()['clock']['seconds_remaining'] > 0
    assert first.json()['clock']['deadline_at'] >= blue['clock']['deadline_at']
    red = c.get(path, headers=h[0]).json()
    assert red['active_side'] == 'red'
    assert red['committed_order'] is None
    assert not {'transcript', 'seed', 'last_seen_red', 'last_seen_blue'} & red.keys()
    repeat = c.post(path + '/commands', headers=h[1], json=action)
    assert repeat.status_code == 200 and repeat.json()['version'] == 1
    second = c.post(path + '/commands', headers=h[0], json=order('red'))
    assert second.status_code == 200, second.text
    assert second.json()['turn'] == 2
    with Session() as db:
        row = db.get(RedBlueMatch, waiting['id'])
        assert row.transcript['edition'] == routes.v2_timed.TIMED_EDITION
        assert len(row.transcript['game']['moves']) == 2
        assert len(db.scalars(select(RedBlueReceipt).where(
            RedBlueReceipt.match_id == row.id)).all()) == 2
    assert c.get(path, headers=h[2]).status_code == 404


def test_timed_expired_action_cannot_beat_worker_even_if_unprocessed(arena, monkeypatch):
    monkeypatch.setenv('EDUCYBER_ENV', 'development')
    c, h, _, Session, *_ = arena
    response = c.post('/api/v1/red-blue/matches', headers=h[0], json={
        'scenario': 'microfinance', 'side': 'blue', 'mode': 'computer',
        'ruleset': 'timed_preview'})
    assert response.status_code == 201, response.text
    path = f"/api/v1/red-blue/matches/{response.json()['id']}"
    with Session.begin() as db:
        row = db.get(RedBlueMatch, response.json()['id'])
        row.transcript = {**row.transcript,
            'clock': {**row.transcript['clock'], 'deadline_at': 1}}
    # Clock is canonical in the future test snapshot but expired; restore itself
    # still verifies underlying replay and seat alignment.
    result = c.post(path + '/commands', headers=h[0], json=order('blue'))
    assert result.status_code == 409
    assert 'deadline' in result.json()['detail'].lower()
    with Session() as db:
        row = db.get(RedBlueMatch, response.json()['id'])
        assert row.transcript['game']['moves'] == []
        assert db.scalars(select(RedBlueReceipt).where(
            RedBlueReceipt.match_id == row.id)).all() == []


def test_timed_worker_advances_late_blue_without_browser_poll(arena, monkeypatch):
    from cyber_warfare import v2_timeout_worker
    monkeypatch.setenv('EDUCYBER_ENV', 'development')
    c, h, _, Session, *_ = arena
    created = c.post('/api/v1/red-blue/matches', headers=h[0], json={
        'scenario': 'microfinance', 'side': 'blue', 'mode': 'human',
        'ruleset': 'timed_preview'})
    assert created.status_code == 201, created.text
    match_id = created.json()['id']
    path = f"/api/v1/red-blue/matches/{match_id}"
    token = c.post(path + '/invite', headers=h[0]).json()['token']
    assert c.post('/api/v1/red-blue/join', headers=h[1],
                  json={'token': token}).status_code == 200
    with Session.begin() as db:
        row = db.get(RedBlueMatch, match_id)
        row.transcript = {**row.transcript,
            'clock': {**row.transcript['clock'], 'deadline_at': 1}}
    with Session() as db:
        settled = v2_timeout_worker.process_due_once(db)
        assert settled['passes'] == 1
    old = c.post(path + '/commands', headers=h[0], json=order('blue'))
    assert old.status_code == 409
    red_view = c.get(path, headers=h[1]).json()
    assert red_view['active_side'] == 'red'
    assert red_view['version'] == 1
    assert red_view['orders']
    with Session() as db:
        row = db.get(RedBlueMatch, match_id)
        assert len(row.transcript['game']['moves']) == 1
        assert row.transcript['game']['moves'][0]['command_id'] == 'server-timeout-1-blue'


def test_saved_history_supports_mixed_sealed_alternating_and_timed_matches(arena, monkeypatch):
    """A timed record must never make existing learners' history unrenderable."""
    c, h, *_ = arena
    monkeypatch.setenv('EDUCYBER_ENV', 'development')
    items = []
    for ruleset in ('sealed', 'alternating_preview', 'timed_preview'):
        response = c.post('/api/v1/red-blue/matches', headers=h[0], json={
            'scenario': 'microfinance', 'side': 'blue', 'mode': 'computer',
            'ruleset': ruleset,
        })
        assert response.status_code == 201, response.text
        items.append(response.json()['id'])
    response = c.get('/api/v1/red-blue/matches', headers=h[0])
    assert response.status_code == 200, response.text
    history = response.json()['matches']
    selected = [row for row in history if row['id'] in items]
    assert {row['id'] for row in selected} == set(items)
    assert all(isinstance(row['title'], str) and row['title'] for row in selected)
    assert all('transcript' not in row and 'clock' not in row for row in selected)
    for identifier in items:
        resumed = c.get(f'/api/v1/red-blue/matches/{identifier}', headers=h[0])
        assert resumed.status_code == 200, resumed.text


def test_timed_reconnect_and_two_devices_share_one_server_clock(arena, monkeypatch):
    """A second session must not reset the deadline or create another grace."""
    from cyber_warfare import v2_timeout_worker
    monkeypatch.setenv('EDUCYBER_ENV', 'development')
    c, h, ids, Session, app, _ = arena
    created = c.post('/api/v1/red-blue/matches', headers=h[0], json={
        'scenario': 'microfinance', 'side': 'blue', 'mode': 'human',
        'ruleset': 'timed_preview'})
    assert created.status_code == 201
    match_id = created.json()['id']
    path = f'/api/v1/red-blue/matches/{match_id}'
    token = c.post(path + '/invite', headers=h[0]).json()['token']
    assert c.post('/api/v1/red-blue/join', headers=h[1],
                  json={'token': token}).status_code == 200
    first = c.get(path, headers=h[0]).json()
    original_deadline = first['clock']['deadline_at']
    with Session() as db:
        blue = db.get(User, ids[0])
        second_session = {'Authorization': 'Bearer ' + issue_session(db, blue)}
        db.commit()
    with TestClient(app) as other_device:
        viewed = other_device.get(path, headers=second_session)
        assert viewed.status_code == 200
        assert viewed.json()['clock']['deadline_at'] == original_deadline
        heartbeat = other_device.post(path + '/heartbeat', headers=second_session,
                                      json={'expected_round': 1})
        assert heartbeat.status_code == 200
        assert heartbeat.json()['clock']['deadline_at'] == original_deadline
        assert c.post(path + '/heartbeat', headers=h[1],
                      json={'expected_round': 1}).status_code == 409
    with Session() as db:
        stored = db.get(RedBlueMatch, match_id)
        assert stored.transcript['clock']['last_seen_blue'] is not None
        assert stored.transcript['clock']['grace_used'] == []
    # Once the active seat stops checking in, an isolated worker may grant
    # its single 30-second extension; a later resume cannot grant another.
    with Session.begin() as db:
        row = db.get(RedBlueMatch, match_id)
        snapshot = row.transcript
        row.transcript = {**snapshot, 'clock': {**snapshot['clock'],
            'last_seen_blue': 1010, 'deadline_at': 1090}}
    with Session() as db:
        result = v2_timeout_worker.process_due_once(db, 1090)
        assert result['graces'] == 1 and result['passes'] == 0
    with Session() as db:
        saved = db.get(RedBlueMatch, match_id)
        assert saved.transcript['clock']['grace_used'] == ['blue']
        assert saved.transcript['clock']['deadline_at'] == 1120
        again = v2_timeout_worker.process_due_once(db, 1090)
        assert again['graces'] == 0
        result = v2_timeout_worker.process_due_once(db, 1120)
        assert result['passes'] == 1
        assert db.get(RedBlueMatch, match_id).transcript['clock']['grace_used'] == ['blue']


def test_postgres_timed_expired_action_races_worker_with_one_authoritative_pass(arena, monkeypatch):
    """At/after a deadline, a late HTTP command cannot win against row-lock expiry."""
    from threading import Barrier
    from cyber_warfare import v2_timeout_worker
    monkeypatch.setenv('EDUCYBER_ENV', 'development')
    c, h, _, Session, app, dialect = arena
    if dialect != 'postgres':
        pytest.skip('Requires PostgreSQL row-locking and real independent sessions')
    created = c.post('/api/v1/red-blue/matches', headers=h[0], json={
        'scenario': 'microfinance', 'side': 'blue', 'mode': 'human',
        'ruleset': 'timed_preview'})
    assert created.status_code == 201
    match_id = created.json()['id']
    path = f'/api/v1/red-blue/matches/{match_id}'
    token = c.post(path + '/invite', headers=h[0]).json()['token']
    assert c.post('/api/v1/red-blue/join', headers=h[1],
                  json={'token': token}).status_code == 200
    with Session.begin() as db:
        row = db.get(RedBlueMatch, match_id)
        row.transcript = {**row.transcript, 'clock': {
            **row.transcript['clock'], 'deadline_at': 1}}
    body = order('blue')
    barrier = Barrier(2)

    def human():
        with TestClient(app) as client:
            barrier.wait(timeout=10)
            return client.post(path + '/commands', headers=h[0], json=body)

    def timeout():
        with Session() as db:
            barrier.wait(timeout=10)
            return v2_timeout_worker.process_due_once(db)

    with ThreadPoolExecutor(max_workers=2) as pool:
        command_future = pool.submit(human)
        worker_future = pool.submit(timeout)
        response, result = command_future.result(), worker_future.result()
    assert response.status_code == 409
    assert result['passes'] == 1
    with Session() as db:
        saved = db.get(RedBlueMatch, match_id)
        assert saved.transcript['game']['moves'] == [{
            'side': 'blue', 'round': 1,
            'command_id': 'server-timeout-1-blue',
            'action': 'wait_blue', 'target': None, 'source': None}]
        assert saved.transcript['clock']['active_side'] == 'red'
        assert db.scalars(select(RedBlueReceipt).where(
            RedBlueReceipt.match_id == match_id)).all() == []
    assert c.post(path + '/commands', headers=h[0], json=body).status_code == 409
