"""Distinct scenario rules, immutable v1 compatibility and saved-mistake evidence."""
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
import pytest
import strategy_engine as engine
import strategy_v1 as v1
from cyber_content import BANK, LEGACY_REVISION, BUILD_B_REVISION, REVISION, _load_file
from test_cyber_lab import lab_client


def test_original_question_bank_and_v1_rules_remain_unchanged():
    old = _load_file('cyber_practice_v1.txt', LEGACY_REVISION)
    assert len(old) == 100
    assert BANK[:100] == old
    state = v1.new_state('legacy')
    for action, target in [('mfa', 'identity'), ('backup', 'backup'), ('patch', 'app'), ('end_turn', None)]:
        expected = v1.advance(state, action, target)
        assert engine.advance(state, action, target) == expected
        state = expected
    public = engine.public(state)
    for key, value in v1.public(state).items(): assert public[key] == value
    assert len(BANK) == 500 and len({q['id'] for q in BANK}) == 500
    assert len([q for q in BANK if q['revision'] == BUILD_B_REVISION]) == 150


def step(state, action, target=None):
    return engine.advance(state, action, target)


def supplier_win(seed):
    s = engine.new_state(seed, 'supplier')
    s = step(s, 'revoke_vendor', 'gateway'); s = step(s, 'backup', 'backup')
    while s['status'] == 'active': s = step(s, 'end_turn')
    return s


def recovery_win(seed):
    s = engine.new_state(seed, 'ransomware')
    for target in ('staff', 'app', 'database'): s = step(s, 'isolate', target)
    s = step(s, 'end_turn')
    for action, target in [('backup', 'backup'), ('patch', 'staff'), ('patch', 'app')]: s = step(s, action, target)
    s = step(s, 'end_turn')
    for target in ('staff', 'app', 'database'): s = step(s, 'restore', target)
    s = step(s, 'end_turn')
    for target in ('staff', 'app', 'database'): s = step(s, 'reconnect', target)
    while s['status'] == 'active': s = step(s, 'end_turn')
    return s


@pytest.mark.parametrize('seed', ['a', 'b', 'c', 'replay'])
def test_scenarios_support_reproducible_wins_and_different_failure_paths(seed):
    assert supplier_win(seed)['status'] == 'won'
    assert recovery_win(seed)['status'] == 'won'
    assert recovery_win(seed) == recovery_win(seed)
    for scenario in ('supplier', 'ransomware'):
        s = engine.new_state(seed, scenario)
        while s['status'] == 'active': s = step(s, 'end_turn')
        assert s['status'] == 'lost'
        assert 'debrief' in engine.public(s)


def test_supplier_entry_is_independent_of_human_mfa_and_existing_compromise():
    s = engine.new_state('supplier-test', 'supplier')
    s = step(s, 'mfa', 'identity'); s = step(s, 'patch', 'gateway')
    s = step(step(s, 'end_turn'), 'end_turn')
    assert s['assets']['gateway']['compromised']
    s = step(s, 'revoke_vendor', 'gateway')
    assert s['vendor_revoked'] and s['assets']['gateway']['compromised']
    with pytest.raises(ValueError): step(s, 'revoke_vendor', 'gateway')
    with pytest.raises(ValueError): step(engine.new_state('a'), 'revoke_vendor', 'gateway')


def test_ransomware_state_visibility_and_delayed_restore():
    s = engine.new_state('r', 'ransomware'); original = deepcopy(s)
    public = engine.public(s)
    assert public['availability'] == 50
    assert public['assets'][3]['condition'] == 'Service encrypted'
    assert 'seed' not in public and 'compromised' not in public['assets'][3]
    for target in ('app', 'database', 'staff'): s = step(s, 'isolate', target)
    assert original['assets']['app']['isolated'] is False
    assert engine.availability(s) == 30
    with pytest.raises(ValueError): step(s, 'restore', 'app')


@pytest.mark.parametrize('scenario', ['branch', 'supplier', 'ransomware'])
def test_http_scenario_selection_reopening_and_authority(lab_client, scenario):
    client, _, user = lab_client
    r = client.post('/api/v1/cyber-lab/runs', json={'scenario': scenario})
    assert r.status_code == 201 and r.json()['scenario'] == scenario
    saved = client.get('/api/v1/cyber-lab/runs/'+str(r.json()['id']))
    assert saved.json() == r.json()
    user.id = 2
    assert client.get('/api/v1/cyber-lab/runs/'+str(r.json()['id'])).status_code == 404
    assert client.post('/api/v1/cyber-lab/runs', json={'scenario': '../module'}).status_code == 422
    assert client.post('/api/v1/cyber-lab/runs', json={'scenario': scenario, 'seed': 'chosen'}).status_code == 422


def answer(client, Session, session, correct):
    from models import CyberPracticeSession
    with Session() as db: snapshot = db.get(CyberPracticeSession, session['id']).snapshot
    return client.post(f"/api/v1/cyber-lab/practice/{session['id']}/submit", json={'answers': {
        q['id']: q['answer'] if correct else (q['answer']+1)%len(q['options']) for q in snapshot}})


def test_mistake_review_tracks_actual_latest_grading_and_is_user_scoped(lab_client):
    client, Session, user = lab_client
    assert client.post('/api/v1/cyber-lab/practice', json={'mode': 'mistakes', 'count': 1}).status_code == 422
    first = client.post('/api/v1/cyber-lab/practice', json={'topic': 'identity', 'count': 3}).json()
    assert answer(client, Session, first, False).status_code == 200
    review = client.post('/api/v1/cyber-lab/practice', json={'mode': 'mistakes', 'count': 3}).json()
    assert {q['id'] for q in review['questions']} == {q['id'] for q in first['questions']}
    assert answer(client, Session, review, True).status_code == 200
    assert client.post('/api/v1/cyber-lab/practice', json={'mode': 'mistakes', 'count': 1}).status_code == 422
    user.id = 2
    assert client.post('/api/v1/cyber-lab/practice', json={'mode': 'mistakes', 'count': 1}).status_code == 422


def test_old_study_completion_is_preserved_as_earlier_edition(lab_client):
    from models import CyberStudyProgress
    client, Session, _ = lab_client
    with Session.begin() as db: db.add(CyberStudyProgress(user_id=1, module_id='protect', revision=LEGACY_REVISION))
    module = client.get('/api/v1/cyber-lab/catalog').json()['modules'][0]
    assert module['previously_completed'] and not module['completed']
    assert client.post('/api/v1/cyber-lab/study/protect/complete').status_code == 200
    with Session() as db:
        assert {r.revision for r in db.query(CyberStudyProgress).filter_by(user_id=1,module_id='protect')} == {LEGACY_REVISION, REVISION}


def test_older_session_submitted_later_controls_mistake_verdict(lab_client):
    from models import CyberPracticeSession
    client, Session, _ = lab_client
    snapshot = deepcopy(BANK[:1])
    with Session.begin() as db:
        old = CyberPracticeSession(user_id=1, snapshot=snapshot)
        newer = CyberPracticeSession(user_id=1, snapshot=snapshot)
        db.add_all([old, newer]); db.flush(); older_id, newer_id = old.id, newer.id
    assert answer(client, Session, {'id': newer_id}, True).status_code == 200
    assert answer(client, Session, {'id': older_id}, False).status_code == 200
    response = client.post('/api/v1/cyber-lab/practice', json={'mode': 'mistakes', 'count': 1})
    assert response.status_code == 201 and response.json()['questions'][0]['id'] == snapshot[0]['id']


def test_challenging_counts_and_unknown_modes_are_checked(lab_client):
    client, _, _ = lab_client
    catalog = client.get('/api/v1/cyber-lab/catalog').json()
    assert catalog['question_count'] == 500 and len(catalog['scenarios']) == 4
    assert all(item['counts'] == {'foundational': 20, 'applied': 20, 'challenging': 10} for item in catalog['topics'])
    assert client.post('/api/v1/cyber-lab/practice', json={'mode': 'invented'}).status_code == 422
    assert client.post('/api/v1/cyber-lab/practice', json={'topic': 'cloud', 'difficulty': 'challenging', 'count': 5}).status_code == 201
    assert client.post('/api/v1/cyber-lab/practice', json={'topic': 'cloud', 'difficulty': 'challenging', 'count': 11}).status_code == 422


def test_unsubmitted_sessions_do_not_displace_graded_review_window(lab_client):
    from models import CyberPracticeSession
    client, Session, _ = lab_client
    first = client.post('/api/v1/cyber-lab/practice', json={'count': 1}).json()
    answer(client, Session, first, False)
    with Session.begin() as db:
        for _ in range(51): db.add(CyberPracticeSession(user_id=1, snapshot=deepcopy(BANK[:1]), result=None))
    response = client.post('/api/v1/cyber-lab/practice', json={'mode': 'mistakes', 'count': 1})
    assert response.status_code == 201


def test_new_scenarios_cannot_reconnect_during_pending_restore():
    s = engine.new_state('pending', 'ransomware')
    for target in ('app', 'database', 'staff'): s = step(s, 'isolate', target)
    s = step(s, 'end_turn'); s = step(s, 'backup', 'backup'); s = step(s, 'end_turn')
    s = step(s, 'restore', 'app')
    with pytest.raises(ValueError): step(s, 'reconnect', 'app')
    asset = next(a for a in engine.public(s)['assets'] if a['id'] == 'app')
    assert 'reconnect' not in {a['id'] for a in asset['actions']}
