"""Synthetic domain tests; no application DB, network or real attack operations."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import pytest
from pydantic import ValidationError
from cyber_warfare.catalog import ACTIONS
from cyber_warfare.engine import (Order, available_orders, commit, debrief, export_replay,
                                 new_match, probabilities, replay, view)
from cyber_warfare.opponent import LEVELS, choose_order
from cyber_warfare.scenario import list_scenarios, load_scenario, parse_scenario


@pytest.fixture
def arena():
    d = load_scenario('microfinance').snapshot()
    d.update(id='test_arena', turn_limit=6, starting_budget=18)
    d['assets'] = d['assets'][:3]
    d['assets'][0]['initial_access'] = 2
    d['connections'] = d['connections'][:2]
    d['red']['known_assets'] = ['teller', 'identity', 'ledger']
    d['blue']['known_assets'] = ['teller', 'identity', 'ledger']
    return parse_scenario(d)


def start(arena, seed='test-seed'):
    return new_match(arena, seed, 'alice', 'bob')


def round_(m, red, blue=Order('wait_blue'), arrival=('red', 'blue')):
    orders = dict(red=red, blue=blue)
    for side in arrival:
        m = commit(m, m.seats[side], orders[side], m.turn, f'{side}-{m.turn}')
    return m


def with_success(arena, red, blue=Order('wait_blue')):
    for seed in range(200):
        m = round_(start(arena, str(seed)), red, blue)
        if m.timeline[-1]['success']:
            return m
    pytest.fail('No successful seeded fixture')


def test_catalog_scenarios_distinct():
    scenarios = list_scenarios()
    assert len(scenarios) >= 6
    assert len({s.industry for s in scenarios}) >= 6
    assert {s.difficulty for s in scenarios} == {'beginner', 'intermediate', 'advanced'}
    assert {s.objective.kind for s in scenarios} == {'fraud', 'leak', 'disruption'}
    assert len({s.digest() for s in scenarios}) == len(scenarios)
    assert len(ACTIONS) == 20
    for a in ACTIONS.values():
        assert a.prerequisites and a.rule and a.explanation
        assert 0 <= a.detection <= 1 and 0 < a.success <= 1
        assert a.public()['url'].startswith('https://attack.mitre.org/techniques/T')
        assert a.relation in ('represents', 'addresses', 'context')


@pytest.mark.parametrize('scenario', [s.id for s in list_scenarios()])
@pytest.mark.parametrize('level', LEVELS)
def test_complete_computer_games_replay_after_json_reordering(scenario, level):
    m = new_match(load_scenario(scenario), 'deterministic-game', 'alice', 'bob')
    while not m.winner:
        for side in ('blue', 'red'):
            projection = view(m, m.seats[side])
            order = choose_order(projection, level)
            assert order in available_orders(projection)
            m = commit(m, m.seats[side], order, m.turn, f'{side}:{m.turn}')
    assert replay(json.loads(json.dumps(export_replay(m), sort_keys=True))) == m
    assert len(m.history) <= m.scenario.turn_limit and min(m.budgets.values()) >= 0
    report = debrief(m, 'alice')
    assert len(report['timeline']) == len(m.history) * 2
    assert report == debrief(m, 'bob')
    assert all(a['framework']['relation'] == 'addresses' for a in report['alternatives'])


def test_sealed_immutable_arrival_independent(arena):
    m = start(arena)
    opening = deepcopy(m)
    before = view(m, 'bob')
    sealed = commit(m, 'alice', Order('persist', 'teller'), 1, 'command-a')
    assert m == opening and sealed.turn == 1 and not sealed.timeline
    after = view(sealed, 'bob')
    assert after.pop('version') == 1
    before.pop('version')
    assert after == before
    assert view(sealed, 'alice')['committed']
    a = round_(m, Order('persist', 'teller'), Order('monitor', 'teller'))
    b = round_(m, Order('persist', 'teller'), Order('monitor', 'teller'), ('blue', 'red'))
    assert a == b
    assert [e['side'] for e in a.timeline] == ['blue', 'red']


def test_idempotency_after_restore(arena):
    first = commit(start(arena), 'alice', Order('wait_red'), 1, 'same')
    assert commit(first, 'alice', Order('wait_red'), 1, 'same') == first
    done = commit(first, 'bob', Order('wait_blue'), 1, 'same')
    assert commit(replay(export_replay(done)), 'alice', Order('wait_red'), 1, 'same') == done
    with pytest.raises(ValueError, match='reused'):
        commit(done, 'alice', Order('recon', 'teller'), 1, 'same')
    with pytest.raises(ValueError, match='stale'):
        commit(done, 'alice', Order('wait_red'), 1, 'new')
    with pytest.raises(ValueError, match='committed'):
        commit(first, 'alice', Order('recon', 'teller'), 1, 'another')


def test_pending_replay_secrets_and_access(arena):
    m = commit(start(arena), 'bob', Order('contain', 'teller'), 1, 'seal')
    assert replay(export_replay(m)) == m
    for player in ('alice', 'bob'):
        payload = json.dumps(view(m, player))
        assert 'test-seed' not in payload and 'plans' not in payload and 'receipts' not in payload
        assert 'persistent' not in payload and 'initial_access' not in payload
    with pytest.raises(ValueError, match='after'):
        debrief(m, 'alice')
    for func in (view, debrief):
        with pytest.raises(PermissionError): func(m, 'mallory')
    with pytest.raises(PermissionError): commit(m, 'mallory', Order('wait_red'), 1, 'x')


def test_blue_revokes_sealed_attack_without_validation_oracle(arena):
    m = start(arena)
    order = Order('fraud', 'teller')
    sealed = commit(m, 'alice', order, 1, 'red')
    result = commit(sealed, 'bob', Order('access_review', 'teller'), 1, 'blue')
    assert not result.timeline[-1]['feasible'] and not result.timeline[-1]['success']
    assert result.budgets == {'red': 15, 'blue': 16}
    assert not result.assets['teller']['fraud']
    assert not any(o['type'] == 'alert' for o in view(result, 'bob')['observations'])
    assert view(result, 'alice')['assets'][-1]['access'] == 0
    blue_first = commit(m, 'bob', Order('access_review', 'teller'), 1, 'blue')
    assert available_orders(view(blue_first, 'alice')) == available_orders(view(m, 'alice'))
    assert result.timeline == round_(m, order, Order('access_review', 'teller')).timeline


def test_graph_segmentation_discovery(arena):
    m = start(arena)
    assert Order('lateral', 'identity', 'teller') in available_orders(view(m, 'alice'))
    assert Order('lateral', 'ledger', 'teller') not in available_orders(view(m, 'alice'))
    blocked = round_(m, Order('lateral', 'identity', 'teller'), Order('segment', 'identity'))
    assert blocked.assets['identity']['access'] == 0 and not blocked.timeline[-1]['feasible']
    assert with_success(arena, Order('lateral', 'identity', 'teller')).assets['identity']['access'] == 1
    for seed in range(50):
        actual = round_(new_match(load_scenario('microfinance'), str(seed), 'alice', 'bob'), Order('recon', 'teller'))
        if actual.timeline[-1]['success']: break
    visible = {a['id'] for a in view(actual, 'alice')['assets']}
    assert 'identity' in visible and 'ledger' not in visible


def test_controls_and_investigation(arena):
    m = start(arena)
    attack = Order('disrupt', 'teller')
    base = probabilities(m, 'red', attack)
    patched = round_(m, Order('wait_red'), Order('patch', 'teller'))
    assert probabilities(patched, 'red', attack)[0] < base[0]
    monitored = round_(m, Order('wait_red'), Order('monitor', 'teller'))
    assert probabilities(monitored, 'red', attack)[1] > base[1]
    assert not any(o['type'] in ('finding', 'alert') for o in view(monitored, 'bob')['observations'])
    investigated = round_(monitored, Order('wait_red'), Order('detect', 'teller'))
    assert any(o['type'] == 'finding' for o in view(investigated, 'bob')['observations'])
    assert 'access' not in view(investigated, 'bob')['assets'][-1]


def test_alert_is_not_a_success_disclosure(arena):
    outcomes = set()
    for seed in range(150):
        result = round_(start(arena, str(seed)), Order('fraud', 'teller'), Order('harden', 'teller'))
        event = result.timeline[-1]
        outcomes.add((event['success'], event['detected']))
        if event['detected']:
            alert = [o for o in view(result, 'bob')['observations'] if o['type'] == 'alert'][0]
            assert 'success' not in alert and 'action' not in alert and 'fraud' not in alert['message']
    assert (True, False) in outcomes and (False, True) in outcomes


def test_persistence_and_recovery(arena):
    persisted = with_success(arena, Order('persist', 'teller'))
    isolated = round_(persisted, Order('wait_red'), Order('contain', 'teller'))
    assert isolated.assets['teller']['persistent'] and isolated.assets['teller']['access'] == 1
    blocked = round_(isolated, Order('fraud', 'teller'))
    assert not blocked.timeline[-1]['success']
    for seed in range(100):
        candidate = deepcopy(isolated)
        candidate.seed = str(seed)
        recovered = round_(candidate, Order('wait_red'), Order('recover', 'teller'))
        if recovered.timeline[-2]['success']: break
    assert not recovered.assets['teller']['isolated'] and not recovered.assets['teller']['persistent']
    assert recovered.assets['teller']['access'] == 0


@pytest.mark.parametrize('kind,action', [('fraud', 'fraud'), ('leak', 'exfiltrate'), ('disruption', 'disrupt')])
def test_objectives_and_deadline(arena, kind, action):
    d = arena.snapshot()
    d['objective'].update(kind=kind, targets=['teller'], threshold=15)
    scenario = parse_scenario(d)
    result = with_success(scenario, Order(action, 'teller'))
    assert result.winner == 'red' and debrief(result, 'alice')['winner'] == 'red'
    with pytest.raises(ValueError): commit(result, 'alice', Order('wait_red'), result.turn, 'after')
    defended = start(scenario)
    while not defended.winner: defended = round_(defended, Order('wait_red'))
    assert defended.winner == 'blue' and defended.turn == scenario.turn_limit


def test_outage_streak_and_isolation_cost(arena):
    d = arena.snapshot()
    d['objective'].update(kind='disruption', targets=['teller'], threshold=15, hold_turns=2)
    scenario = parse_scenario(d)
    first = round_(start(scenario), Order('wait_red'), Order('contain', 'teller'))
    assert first.held == 1 and first.winner is None
    assert round_(first, Order('wait_red')).winner == 'red'
    for seed in range(100):
        opening = round_(start(scenario, str(seed)), Order('wait_red'), Order('contain', 'teller'))
        recovered = round_(opening, Order('wait_red'), Order('recover', 'teller'))
        if recovered.timeline[-2]['success']:
            assert recovered.held == 0 and recovered.winner is None
            break
    else: pytest.fail('Recovery never succeeded')


def test_recovery_preserves_historical_leak(arena):
    leaked = with_success(arena, Order('exfiltrate', 'teller'))
    recovered = round_(leaked, Order('wait_red'), Order('recover', 'teller'))
    assert recovered.assets['teller']['leaked']


@pytest.mark.parametrize('bad', [Order('recover', 'teller'), Order('fraud', 'missing'), Order('lateral', 'ledger', 'teller'), Order('wait_red', 'teller'), Order('unknown')])
def test_reject_bad_orders_immutably(arena, bad):
    m = start(arena)
    before = deepcopy(m)
    with pytest.raises(ValueError): commit(m, 'alice', bad, 1, 'bad')
    assert m == before


def test_budget_exhaustion(arena):
    m = start(arena)
    m.budgets['red'] = 0
    assert available_orders(view(m, 'alice')) == [Order('wait_red')]
    with pytest.raises(ValueError): commit(m, 'alice', Order('persist', 'teller'), 1, 'bad')


@pytest.mark.parametrize('level', LEVELS)
def test_policy_no_hidden_truth_or_enemy_plan(arena, level):
    m = start(arena)
    blue_before = view(m, 'bob')
    changed = deepcopy(m)
    changed.seed = 'secret'
    changed.assets['ledger']['access'] = 2
    changed.assets['ledger']['persistent'] = True
    changed.plans['red'] = Order('fraud', 'teller')
    assert view(changed, 'bob') == blue_before
    assert choose_order(view(changed, 'bob'), level) == choose_order(blue_before, level)
    red_before = view(m, 'alice')
    changed = deepcopy(m)
    changed.assets['teller']['controls'].append('hardened')
    changed.assets['teller']['access'] = 0
    changed.plans['blue'] = Order('access_review', 'teller')
    assert view(changed, 'alice') == red_before
    assert choose_order(view(changed, 'alice'), level) == choose_order(red_before, level)


def test_difficulty_priorities(arena):
    observation = view(start(arena), 'bob')
    assert choose_order(observation, 'easy').action == 'monitor'
    assert choose_order(observation, 'standard').action == 'harden'
    observation['observations'].append(dict(turn=1, type='alert', target='teller'))
    assert choose_order(observation, 'standard').action == 'contain'
    assert choose_order(observation, 'hard').action == 'access_review'
    with pytest.raises(ValueError): choose_order(observation, 'omniscient')


@pytest.mark.parametrize('mutation', ['unknown_key', 'duplicate_asset', 'bad_edge', 'bad_intel', 'bad_objective', 'threshold', 'string_budget', 'control', 'kind', 'hold'])
def test_strict_scenarios(mutation):
    d = load_scenario('microfinance').snapshot()
    if mutation == 'unknown_key': d['script'] = 'untrusted'
    if mutation == 'duplicate_asset': d['assets'].append(d['assets'][0])
    if mutation == 'bad_edge': d['connections'][0]['source'] = 'missing'
    if mutation == 'bad_intel': d['red']['known_assets'].append('missing')
    if mutation == 'bad_objective': d['objective']['targets'] = ['missing']
    if mutation == 'threshold': d['objective']['threshold'] = 999
    if mutation == 'string_budget': d['starting_budget'] = '24'
    if mutation == 'control': d['assets'][0]['controls'].append('execute_script')
    if mutation == 'kind': d['assets'][0]['kind'] = 'untrusted'
    if mutation == 'hold': d['objective']['hold_turns'] = 2
    with pytest.raises((ValidationError, ValueError)): parse_scenario(d)


@pytest.mark.parametrize('identifier', ['../models', '/tmp/models', '', 'hospital.json', None, 'a' * 100])
def test_loader_rejects_paths(identifier):
    with pytest.raises(ValueError): load_scenario(identifier)


@pytest.mark.parametrize('field,value', [('engine_version', 'unknown'), ('rules_digest', 'tampered'), ('scenario_digest', 'tampered'), ('pending', {'red': {}, 'blue': {}}), ('rounds', [{}])])
def test_replay_rejects_tampering(arena, field, value):
    record = export_replay(round_(start(arena), Order('wait_red')))
    record[field] = value
    with pytest.raises(ValueError): replay(record)


def test_snapshot_pinned(arena, monkeypatch):
    m = round_(start(arena), Order('recon', 'teller'))
    record = export_replay(m)
    import cyber_warfare.scenario as loader
    monkeypatch.setattr(loader, 'DIRECTORY', Path('/nonexistent'))
    assert replay(record) == m
    record['scenario']['assets'][0]['value'] = 99
    assert m.scenario.assets[0].value == 15
    with pytest.raises(ValueError): replay(record)


def test_cross_process_determinism():
    script = '''import json
from cyber_warfare.scenario import load_scenario
from cyber_warfare.engine import *
m = new_match(load_scenario('microfinance'), 'same-seed', 'alice', 'bob')
for side,order in [('red',Order('phish','teller')), ('blue',Order('monitor','teller'))]:
 m=commit(m,m.seats[side],order,1,side)
print(json.dumps(m.timeline,sort_keys=True))'''
    assert subprocess.check_output([sys.executable, '-c', script], text=True) == subprocess.check_output([sys.executable, '-c', script], text=True)


def test_seed_variation(arena):
    assert len({round_(start(arena, str(s)), Order('persist', 'teller')).timeline[-1]['roll'] for s in range(20)}) == 20


def test_debrief_tested_alternatives(arena):
    d = arena.snapshot()
    d['objective'].update(targets=['teller'], threshold=15)
    m = with_success(parse_scenario(d), Order('fraud', 'teller'))
    report = debrief(m, 'bob')
    assert any(a['action'] == 'access_review' for a in report['alternatives'])
    assert all(a['turn'] == 1 for a in report['alternatives'])
    assert report['timeline'][-1]['framework']['technique'] == 'T1565'
    assert 'seed' not in report and 'roll' not in json.dumps(report)


@pytest.mark.parametrize('scenario', [s.id for s in list_scenarios()])
def test_each_scenario_has_seeded_red_win_and_blue_survival(scenario):
    configuration = load_scenario(scenario)
    m = new_match(configuration, '0', 'alice', 'bob')
    while not m.winner:
        m = round_(m, choose_order(view(m, 'alice'), 'hard'))
    assert m.winner == 'red'
    assert replay(export_replay(m)) == m
    defended = new_match(configuration, '0', 'alice', 'bob')
    while not defended.winner:
        defended = round_(defended, Order('wait_red'), choose_order(view(defended, 'bob'), 'hard'))
    assert defended.winner == 'blue'


def test_recovery_requires_backup_and_negative_investigation_is_uncertain(arena):
    d = arena.snapshot()
    d['assets'][0]['controls'] = []
    d['assets'][0]['initial_access'] = 0
    m = start(parse_scenario(d))
    assert Order('recover', 'teller') not in available_orders(view(m, 'bob'))
    result = round_(m, Order('wait_red'), Order('detect', 'teller'))
    assert 'does not establish safety' in view(result, 'bob')['observations'][-1]['message']


def test_instruction_boundary_is_required_and_can_be_hardened():
    m = new_match(load_scenario('ai_service'), '0', 'alice', 'bob')
    assert Order('prompt_injection', 'assistant') not in available_orders(view(m, 'alice'))
    m = round_(m, Order('recon', 'assistant'))
    assert m.timeline[-1]['success']
    assert Order('prompt_injection', 'assistant') in available_orders(view(m, 'alice'))
    blocked = round_(m, Order('prompt_injection', 'assistant'), Order('harden', 'assistant'))
    assert not blocked.timeline[-1]['feasible'] and blocked.assets['assistant']['access'] == 0


def test_patch_does_not_remove_foothold_and_review_does_not_undo_fraud(arena):
    m = with_success(arena, Order('fraud', 'teller'))
    m = round_(m, Order('wait_red'), Order('patch', 'teller'))
    assert m.assets['teller']['access'] == 2
    m = round_(m, Order('wait_red'), Order('access_review', 'teller'))
    assert m.assets['teller']['access'] == 0 and m.assets['teller']['fraud']


def test_action_points_limit_one_order_even_with_budget(arena):
    m = start(arena)
    first = commit(m, 'alice', Order('recon', 'teller'), 1, 'one')
    with pytest.raises(ValueError, match='committed'):
        commit(first, 'alice', Order('persist', 'teller'), 1, 'two')
    assert first.budgets['red'] == arena.starting_budget  # reserve remains private until resolution


def test_committed_order_visible_only_to_its_owner(arena):
    m = commit(start(arena), 'alice', Order('persist', 'teller'), 1, 'sealed')
    assert view(m, 'alice')['committed_order'] == Order('persist', 'teller').dump()
    assert view(m, 'bob')['committed_order'] is None


def test_rule_revision_guard_on_live_commands(arena):
    m = start(arena)
    m.rules_digest = 'old-rules'
    with pytest.raises(ValueError, match='rules revision'):
        commit(m, 'alice', Order('wait_red'), 1, 'no')


def test_debrief_recovery_can_improve_business_availability(arena):
    d = arena.snapshot()
    d['objective'].update(kind='disruption', targets=['teller'], threshold=15, hold_turns=2)
    scenario = parse_scenario(d)
    for seed in range(40):
        m = round_(start(scenario, str(seed)), Order('wait_red'), Order('contain', 'teller'))
        m = round_(m, Order('wait_red'))
        report = debrief(m, 'bob')
        if any(a['action'] == 'recover' and a['turn'] == 2 for a in report['alternatives']):
            assert any('business unavailability' in a['explanation'] for a in report['alternatives'])
            break
    else:
        pytest.fail('Debrief missed affordable recovery alternative')


def test_missed_alert_has_later_response_opportunity(arena):
    for seed in range(50):
        m = round_(start(arena, str(seed)), Order('fraud', 'teller'))
        if m.timeline[-1]['detected']:
            while not m.winner:
                m = round_(m, Order('wait_red'))
            report = debrief(m, 'bob')
            assert any('later response opportunity' in e['reason'] for e in report['missed'])
            break
    else:
        pytest.fail('No detected fixture')


def test_config_size_and_filename(tmp_path, monkeypatch, arena):
    import cyber_warfare.scenario as loader
    monkeypatch.setattr(loader, 'DIRECTORY', tmp_path)
    (tmp_path / 'oversized.json').write_text('x' * 64001)
    with pytest.raises(ValueError): load_scenario('oversized')
    # A valid configuration with a different ID isolates the filename check.
    snapshot = arena.snapshot()
    snapshot['id'] = 'different'
    (tmp_path / 'mismatch.json').write_text(json.dumps(snapshot), encoding='utf-8')
    with pytest.raises(ValueError): load_scenario('mismatch')


def test_config_symlink_rejected(tmp_path, monkeypatch, arena):
    import cyber_warfare.scenario as loader
    monkeypatch.setattr(loader, 'DIRECTORY', tmp_path)
    snapshot = arena.snapshot()
    snapshot['id'] = 'linked'
    target = tmp_path / 'target.json'
    target.write_text(json.dumps(snapshot), encoding='utf-8')
    # Valid, correctly identified content ensures rejection depends on the link
    # boundary, rather than oversized or otherwise invalid target content.
    try:
        (tmp_path / 'linked.json').symlink_to(target)
    except OSError as error:
        if getattr(error, 'winerror', None) == 1314:
            pytest.skip('Windows account cannot create symlinks (WinError 1314); link rejection is exercised in Linux CI')
        raise  # Unexpected filesystem failures must still fail the test.
    with pytest.raises(ValueError): load_scenario('linked')


def test_duplicate_intelligence_rejected(arena):
    d = arena.snapshot()
    d['red']['known_assets'].append('teller')
    with pytest.raises(ValueError): parse_scenario(d)
