"""Consequential capstone rules, observation privacy, replay and authority."""
from copy import deepcopy
from uuid import uuid4
import pytest
import strategy_siege as siege
import strategy_engine as engine
from test_cyber_lab import lab_client, post_command


def step(s, action, target=None):
    return engine.advance(s, action, target)


def win(seed='siege-test', narrow=False):
    s = step(engine.new_state(seed, 'siege'), 'call_support', 'support')
    if narrow:
        for signal in list(s['signals']): s = step(s, 'investigate_signal', signal['id'])
        affected = next(key for key, a in s['assets'].items() if a['known'] and a['observed'])
        s = step(s, 'isolate', affected); s = step(s, 'patch', 'app')
        s = step(s, 'revoke_vendor', 'remote') if affected == 'staff' else step(s, 'mfa', 'identity')
        contained = [affected]
    else:
        contained = ['staff', 'remote']
        for key in contained: s = step(s, 'isolate', key)
        for action, key in [('mfa', 'identity'), ('patch', 'app'), ('revoke_vendor', 'remote')]: s = step(s, action, key)
    s = step(s, 'end_turn')
    if not s['mfa']: s = step(s, 'mfa', 'identity')
    if not s['vendor_revoked']: s = step(s, 'revoke_vendor', 'remote')
    s = step(s, 'backup', 'backup')
    while s['turn'] < 4: s = step(s, 'end_turn')
    for key in contained: s = step(s, 'restore', key)
    if s['staff']: s = step(s, 'validate', 'app')
    while s['turn'] < 6: s = step(s, 'end_turn')
    for key in contained: s = step(s, 'validate', key)
    if s['staff']: s = step(s, 'validate', 'database')
    s = step(s, 'end_turn')
    for key in contained: s = step(s, 'reconnect', key)
    for key in ('app', 'database'):
        if not s['assets'][key]['validated_clean']:
            if not s['staff']: s = step(s, 'end_turn')
            s = step(s, 'validate', key)
    while s['status'] == 'active': s = step(s, 'end_turn')
    return s


@pytest.mark.parametrize('seed', ['one', 'two', 'three', 'four', 'five', 'six'])
def test_different_strategies_win_with_explained_tradeoffs(seed):
    broad, narrow = win(seed), win(seed, narrow=True)
    assert broad['status'] == narrow['status'] == 'won'
    assert broad == win(seed)
    assert narrow['budget'] == broad['budget'] + 4
    assert siege.summary(narrow)['signals_reviewed'] == 2
    assert siege.summary(broad)['signals_reviewed'] == 0
    ignored = engine.new_state(seed, 'siege')
    while ignored['status'] == 'active': ignored = step(ignored, 'end_turn')
    assert ignored['status'] == 'lost'


def test_dependencies_and_two_turn_work_have_service_costs():
    s = engine.new_state('jobs', 'siege'); before = deepcopy(s)
    s = step(s, 'patch', 'app')
    assert before['assets']['app']['pending'] is None
    assert siege.availability(s) == 50 and s['assets']['app']['due_turn'] == 3
    s = step(s, 'end_turn')
    assert s['assets']['app']['pending'] == 'patch' and not s['assets']['app']['patched']
    s = step(s, 'end_turn'); assert s['assets']['app']['patched']
    s = step(s, 'isolate', 'identity'); assert siege.availability(s) == 35


def test_support_is_once_only_and_extra_staff_expires():
    s = step(engine.new_state('staff', 'siege'), 'call_support', 'support')
    assert s['budget'] == 32 and s['staff'] == 5
    with pytest.raises(ValueError): step(s, 'call_support', 'support')
    s = step(s, 'end_turn'); assert s['staff'] == 3
    s['budget'] = 0; s['support_used'] = False
    with pytest.raises(ValueError): step(s, 'call_support', 'support')


def test_restore_requires_isolation_copy_completion_and_validation():
    s = engine.new_state('restore', 'siege')
    affected = next(key for key, a in s['assets'].items() if a['compromised'])
    with pytest.raises(ValueError): step(s, 'restore', affected)
    s = step(s, 'isolate', affected)
    with pytest.raises(ValueError): step(s, 'reconnect', affected)
    s = step(s, 'validate', affected); assert not s['assets'][affected]['validated_clean']
    with pytest.raises(ValueError): step(s, 'reconnect', affected)
    s['copy_ready'] = True; s['staff'] = 3
    s = step(s, 'restore', affected)
    with pytest.raises(ValueError): step(s, 'reconnect', affected)
    s = step(s, 'end_turn'); assert s['assets'][affected]['compromised']
    s = step(s, 'end_turn'); assert not s['assets'][affected]['compromised']
    with pytest.raises(ValueError): step(s, 'reconnect', affected)
    s = step(s, 'validate', affected); s = step(s, 'reconnect', affected)
    assert not s['assets'][affected]['isolated']


def test_observation_history_does_not_leak_hidden_changes():
    s = engine.new_state('private', 'siege'); public = engine.public(s)
    assert 'seed' not in public and 'decisions' not in public
    assert all('compromised' not in a and 'observed' not in a for a in public['assets'])
    assert all(a['condition'] == 'Not investigated' for a in public['assets'])
    s = step(s, 'inspect', 'database'); s['assets']['database']['compromised'] = True
    assert next(a for a in engine.public(s)['assets'] if a['id'] == 'database')['condition'] == 'No compromise observed'
    s['assets']['database']['monitored'] = True; s['assets']['collector']['isolated'] = True
    s = step(s, 'end_turn')
    assert next(a for a in engine.public(s)['assets'] if a['id'] == 'database')['condition'] == 'Not investigated'
    s = step(s, 'inspect', 'database')
    assert next(a for a in engine.public(s)['assets'] if a['id'] == 'database')['condition'] == 'Compromise detected'


def test_signal_findings_are_saved_and_investigations_cannot_be_repeated():
    s = engine.new_state('signals', 'siege'); findings = []
    for signal in list(s['signals']):
        s = step(s, 'investigate_signal', signal['id'])
        findings.append(s['signals'][int(signal['id'].split('-')[1])-1]['finding'])
    assert set(findings) == {'No compromise observed', 'Compromise detected'}
    for target in ('signal-999', 'signal-1'):
        with pytest.raises(ValueError): step(s, 'investigate_signal', target)


def test_illegal_actions_and_terminal_mutation_are_rejected():
    s = engine.new_state('invalid', 'siege')
    for action, target in [('restore', 'missing'), ('revoke_vendor', 'gateway'), ('patch', 'signal-1'), ('end_turn', 'staff')]:
        with pytest.raises(ValueError): step(s, action, target)
    s['budget'] = 0
    with pytest.raises(ValueError): step(s, 'monitor', 'staff')
    with pytest.raises(ValueError): step(win(), 'inspect', 'staff')


def test_http_ownership_deduplication_and_stale_versions(lab_client):
    client, _, user = lab_client
    response = client.post('/api/v1/cyber-lab/runs', json={'scenario': 'siege'})
    assert response.status_code == 201
    run = response.json(); assert len(run['assets']) == 8
    body = {'command_id': str(uuid4()), 'expected_version': 0, 'action': 'call_support', 'target': 'support'}
    url = f"/api/v1/cyber-lab/runs/{run['id']}/commands"
    result = client.post(url, json=body)
    assert result.status_code == 200 and result.json()['budget'] == 32
    assert client.post(url, json=body).json() == result.json()
    assert post_command(client, run, 'inspect', 'app').status_code == 409
    assert client.post(url, json={**body, 'target': 'app'}).status_code == 409
    user.id = 2
    assert client.get('/api/v1/cyber-lab/runs/'+str(run['id'])).status_code == 404
    assert client.post(url, json=body).status_code == 404


def test_owned_terminal_replay_reuses_private_opening_and_safe_comparison(lab_client):
    from models import StrategyRun
    client, Session, user = lab_client
    completed = win('replay', narrow=True)
    with Session.begin() as db:
        parent = StrategyRun(user_id=1, state=completed); db.add(parent); db.flush(); parent_id = parent.id
    response = client.post('/api/v1/cyber-lab/runs', json={'scenario': 'siege', 'replay_run_id': parent_id})
    assert response.status_code == 201
    replay = response.json(); assert replay['replay_of'] == parent_id and 'seed' not in replay
    assert 'comparison_baseline' not in replay and replay['status'] == 'active'
    with Session() as db:
        saved = db.get(StrategyRun, replay['id']).state
        assert saved['seed'] == completed['seed']
        assert saved['comparison_baseline'] == siege.summary(completed)
        final = {**win(saved['seed']), 'comparison_baseline': saved['comparison_baseline']}
        assert engine.public(final)['debrief']['comparison'] == siege.summary(completed)
    for scenario, parent_id_to_use in [('siege', replay['id']), ('branch', parent_id)]:
        assert client.post('/api/v1/cyber-lab/runs', json={'scenario': scenario, 'replay_run_id': parent_id_to_use}).status_code == 422
    user.id = 2
    assert client.post('/api/v1/cyber-lab/runs', json={'scenario': 'siege', 'replay_run_id': parent_id}).status_code == 404


@pytest.mark.parametrize('body', [{'scenario': 'siege', 'seed': 'chosen'}, {'scenario': 'siege', 'replay_run_id': True}, {'scenario': 'siege', 'replay_run_id': 0}, {'scenario': 'siege', 'replay_run_id': 2**100}, {'scenario': 'siege', 'budget': 999}])
def test_forged_or_invalid_replay_inputs_are_rejected(lab_client, body):
    assert lab_client[0].post('/api/v1/cyber-lab/runs', json=body).status_code == 422


@pytest.mark.parametrize('target', ['staff', 'app', 'remote'])
def test_opponent_changes_entry_with_remaining_open_paths(target):
    s = engine.new_state('adapt', 'siege')
    for a in s['assets'].values(): a['compromised'] = False
    s['mfa'] = target != 'staff'
    s['vendor_revoked'] = target != 'remote'
    s['assets']['app']['patched'] = target != 'app'
    s = step(s, 'end_turn')
    assert s['assets'][target]['compromised']
    assert s['signals'][-1]['asset'] == target


def test_prolonged_dependency_outage_loses_and_validation_is_a_goal():
    s = engine.new_state('outage', 'siege')
    for key in ('staff', 'identity'): s = step(s, 'isolate', key)
    assert siege.availability(s) == 15
    s = step(s, 'end_turn'); assert s['status'] == 'active'
    s = step(s, 'end_turn'); assert s['status'] == 'lost'
    s = win('validate')
    s['status'] = 'active'; s['turn'] = 9
    s['assets']['app']['validated_clean'] = False
    s = step(s, 'end_turn'); assert s['status'] == 'active'
    s = step(s, 'validate', 'app'); s = step(s, 'end_turn')
    assert s['status'] == 'won'


def test_isolation_stops_automatic_monitoring_but_manual_inspection_remains():
    s = engine.new_state('isolated-monitor', 'siege')
    s = step(s, 'monitor', 'database'); s = step(s, 'isolate', 'database')
    s = step(s, 'end_turn')
    database = next(a for a in engine.public(s)['assets'] if a['id'] == 'database')
    assert database['condition'] == 'Not investigated'
    s = step(s, 'inspect', 'database')
    assert next(a for a in engine.public(s)['assets'] if a['id'] == 'database')['condition'] == 'No compromise observed'


def test_replay_rejects_a_completed_legacy_run(lab_client):
    from models import StrategyRun
    from test_cyber_lab import winning
    client, Session, _ = lab_client
    with Session.begin() as db:
        parent = StrategyRun(user_id=1, state=winning()); db.add(parent); db.flush(); parent_id = parent.id
    assert client.post('/api/v1/cyber-lab/runs', json={'scenario': 'siege', 'replay_run_id': parent_id}).status_code == 422
