"""Pure, copy-on-command resolver. Full Match state is PRIVATE server-side material.

Commit legality uses only a seat's observation. Hidden-state prerequisites are
revalidated at resolution, preventing validation errors from becoming an oracle.
The future API must bind the seat to authentication and transact each command.
"""
from copy import deepcopy
from dataclasses import dataclass, field
import hashlib
import json
from .catalog import ACTIONS, ENGINE_VERSION, catalog_digest
from .scenario import Scenario, parse_scenario

SIDES = ('red', 'blue')


@dataclass(frozen=True)
class Order:
    action: str
    target: str | None = None
    source: str | None = None

    def dump(self):
        return dict(action=self.action, target=self.target, source=self.source)


@dataclass
class Match:
    scenario: Scenario
    seed: str
    seats: dict
    assets: dict
    intelligence: dict
    budgets: dict
    turn: int = 1
    version: int = 0
    plans: dict = field(default_factory=dict)
    receipts: dict = field(default_factory=dict)
    history: list = field(default_factory=list)
    timeline: list = field(default_factory=list)
    observations: dict = field(default_factory=lambda: {'red': [], 'blue': []})
    winner: str | None = None
    held: int = 0
    rules_digest: str = field(default_factory=catalog_digest)


def new_match(scenario, seed, red_player, blue_player):
    if not isinstance(scenario, Scenario):
        raise ValueError('Validated scenario required')
    if not isinstance(seed, str) or not 1 <= len(seed) <= 128:
        raise ValueError('Seed must be a bounded private string')
    if any(not isinstance(p, str) or not 1 <= len(p) <= 128 for p in (red_player, blue_player)) or red_player == blue_player:
        raise ValueError('Two distinct seat identities required')
    assets = {a.id: {**a.model_dump(mode='json'), 'access': a.initial_access,
                       'persistent': False, 'isolated': False, 'disrupted': False,
                       'leaked': False, 'fraud': False} for a in scenario.assets}
    intel = {side: {a: {'access': assets[a]['access'], 'assessed': None,
                        'leaked': False, 'fraud': False, 'disrupted': False}
                     for a in getattr(scenario, side).known_assets} for side in SIDES}
    return Match(scenario, seed, {'red': red_player, 'blue': blue_player}, assets,
                 intel, {s: scenario.starting_budget for s in SIDES})


def _side(match, player):
    for side in SIDES:
        if match.seats[side] == player:
            return side
    raise PermissionError('Not a match participant')


def _edges(scenario):
    # Connections are directed trust permissions, not undirected physical cables.
    return {(e.source, e.target) for e in scenario.connections}


def view(match, player):
    """Only this projection may be sent to a participant or a rule-based opponent."""
    side = _side(match, player)
    assets = []
    for asset_id, belief in sorted(match.intelligence[side].items()):
        a = match.assets[asset_id]
        visible = {k: a[k] for k in ('id', 'name', 'kind', 'value', 'exposed')}
        if side == 'blue':
            # Blue owns controls/configuration and sees service health, not hidden access.
            visible.update({k: deepcopy(a[k]) for k in ('controls', 'vulnerabilities', 'isolated', 'disrupted')})
        else:
            visible.update(deepcopy(belief))
        assets.append(visible)
    known = match.intelligence[side]
    return {'engine_version': ENGINE_VERSION, 'scenario': match.scenario.id,
            'scenario_revision': match.scenario.revision, 'title': match.scenario.title,
            'side': side, 'turn': match.turn, 'version': match.version,
            'turn_limit': match.scenario.turn_limit, 'budget': match.budgets[side],
            'action_points': match.scenario.action_points, 'committed': side in match.plans,
            'committed_order': match.plans[side].dump() if side in match.plans else None,
            'winner': match.winner, 'briefing': getattr(match.scenario, side).briefing,
            'objective': match.scenario.objective.model_dump(mode='json'), 'assets': assets,
            'connections': [e.model_dump() for e in match.scenario.connections
                            if e.source in known and e.target in known],
            'observations': deepcopy(match.observations[side])}


def available_orders(observation):
    """No private Match access: offered choices cannot reveal hidden control changes."""
    if observation['winner'] or observation['committed']:
        return []
    side = observation['side']
    assets = {a['id']: a for a in observation['assets']}
    edges = {(e['source'], e['target']) for e in observation['connections']}
    orders = []
    for action in ACTIONS.values():
        if action.side != side or action.cost > min(observation['budget'], observation['action_points']):
            continue
        if action.id.startswith('wait_'):
            orders.append(Order(action.id))
            continue
        for a in assets.values():
            aid = action.id
            if side == 'blue':
                # Do not offer recovery without an owned, known backup.
                if aid != 'recover' or 'backup' in a['controls']:
                    orders.append(Order(aid, a['id']))
                continue
            access = a['access']
            allowed = (aid == 'recon' or
                       aid == 'phish' and a['exposed'] and a['kind'] == 'workstation' and access == 0 or
                       aid == 'cloud_access' and a['exposed'] and a['kind'] in ('server', 'cloud') and access == 0 or
                       aid == 'prompt_injection' and a['exposed'] and a['kind'] == 'cloud' and access == 0 or
                       aid == 'escalate' and access == 1 or
                       aid == 'persist' and access == 2 or
                       aid in ('exfiltrate', 'disrupt', 'fraud') and access == 2 and
                       not a[{'exfiltrate': 'leaked', 'disrupt': 'disrupted', 'fraud': 'fraud'}[aid]])
            # Prompt testing is only meaningful when starter/scouted evidence describes an AI boundary.
            if aid == 'prompt_injection' and 'instruction' not in (a['assessed'] or {}).get('vulnerabilities', []):
                allowed = False
            if allowed:
                orders.append(Order(aid, a['id']))
            if aid == 'lateral' and access == 0:
                for source in assets.values():
                    if source['access'] == 2 and (source['id'], a['id']) in edges:
                        orders.append(Order(aid, a['id'], source['id']))
    return sorted(orders, key=lambda o: (o.action, o.target or '', o.source or ''))


def _roll(match, phase):
    """Counter-based SHA256 PRNG: independent of process, hash seed, wall clock and arrival order.

    53-bit uniform fractions; pin algorithm and resolver with ENGINE_VERSION.
    Private seed prevents players predicting future outcomes.
    """
    payload = json.dumps([ENGINE_VERSION, match.seed, match.turn, phase], separators=(',', ':'))
    bits = int.from_bytes(hashlib.sha256(payload.encode()).digest()[:8], 'big') >> 11
    return bits / (1 << 53)


def _prob(value):
    return min(.98, max(.05, value))


def _feasible(match, side, order):
    if order.action.startswith('wait_'):
        return True
    a = match.assets[order.target]
    if side == 'blue':
        return order.action != 'recover' or 'backup' in a['controls']
    if a['isolated']:
        return False
    aid = order.action
    if aid == 'recon':
        return a['exposed'] or a['access'] > 0 or any(
            match.assets[s]['access'] > 0 and not match.assets[s]['isolated']
            for s, t in _edges(match.scenario) if t == a['id'])
    if aid in ('phish', 'cloud_access', 'prompt_injection'):
        return a['exposed'] and a['access'] == 0 and (aid != 'prompt_injection' or 'instruction' in a['vulnerabilities'])
    if aid == 'escalate':
        return a['access'] == 1
    if aid == 'lateral':
        source = match.assets[order.source]
        return (source['access'] == 2 and not source['isolated'] and a['access'] == 0 and
                (order.source, order.target) in _edges(match.scenario) and
                'segmented' not in a['controls'] and 'segmented' not in source['controls'])
    return a['access'] == 2


def probabilities(match, side, order):
    """PRIVATE resolver diagnostics. Never include these live truth-based values in seat views."""
    action = ACTIONS[order.action]
    if order.target is None:
        return 1., 0.
    a = match.assets[order.target]
    controls, weaknesses = a['controls'], a['vulnerabilities']
    success, detection = action.success, action.detection
    if side == 'blue':
        return (min(1., success + .15 * ('monitoring' in controls)), 0.) if order.action == 'detect' else (success, 0.)
    relevant = {'phish': 'phishing', 'cloud_access': 'configuration', 'prompt_injection': 'instruction',
                'escalate': 'privilege', 'lateral': 'access'}.get(order.action)
    if relevant in weaknesses:
        success += .20
    if order.action != 'recon':
        success -= .30 * ('hardened' in controls)
        if order.action in ('escalate', 'disrupt', 'cloud_access'):
            success -= .40 * ('patched' in controls)
        if order.action in ('lateral', 'fraud', 'exfiltrate', 'persist'):
            success -= .30 * ('access_control' in controls)
    detection += .35 * ('monitoring' in controls)
    return _prob(success), _prob(detection)


def _add_control(a, control):
    if control not in a['controls']:
        a['controls'].append(control)
        a['controls'].sort()


def _reveal(match, asset_id):
    if asset_id not in match.intelligence['red']:
        match.intelligence['red'][asset_id] = dict(access=0, assessed=None, leaked=False, fraud=False, disrupted=False)


def _effect(match, side, order):
    a, aid = match.assets[order.target], order.action
    if side == 'blue':
        control = {'monitor': 'monitoring', 'patch': 'patched', 'harden': 'hardened',
                   'segment': 'segmented', 'access_review': 'access_control'}.get(aid)
        if control:
            _add_control(a, control)
        removed = {'patch': {'privilege'}, 'harden': {'configuration', 'instruction'}}.get(aid, set())
        a['vulnerabilities'] = [v for v in a['vulnerabilities'] if v not in removed]
        if aid in ('access_review', 'recover'):
            a['access'], a['persistent'] = 0, False
        if aid == 'contain':
            a['isolated'], a['access'] = True, 1 if a['persistent'] else 0
        if aid == 'recover':
            a['isolated'], a['disrupted'] = False, False
        return
    belief = match.intelligence['red'][order.target]
    if aid == 'recon':
        belief['access'] = a['access']
        belief['disrupted'] = a['disrupted']
        belief['assessed'] = {k: deepcopy(a[k]) for k in ('controls', 'vulnerabilities')}
        belief['assessed']['turn'] = match.turn
        for s, t in sorted(_edges(match.scenario)):
            if s == order.target:
                _reveal(match, t)
    if aid in ('phish', 'cloud_access', 'prompt_injection', 'lateral'):
        a['access'] = belief['access'] = 1
    if aid == 'escalate':
        a['access'] = belief['access'] = 2
    if aid == 'persist':
        a['persistent'] = True
    flag = {'exfiltrate': 'leaked', 'disrupt': 'disrupted', 'fraud': 'fraud'}.get(aid)
    if flag:
        a[flag] = belief[flag] = True


def _resolve_action(match, side, order):
    action = ACTIONS[order.action]
    match.budgets[side] -= action.cost
    feasible = _feasible(match, side, order)
    success_probability, detection_probability = probabilities(match, side, order)
    roll = _roll(match, side + ':success')
    success = feasible and roll < success_probability
    target = match.assets.get(order.target)
    # Detection is evaluated even for failed attempts, provided the target was reachable.
    detection_roll = _roll(match, side + ':detection')
    detected = side == 'red' and feasible and detection_roll < detection_probability
    before = deepcopy(target)
    if success and target is not None:
        _effect(match, side, order)
    if side == 'red' and target is not None and not feasible and order.action in ('escalate', 'persist', 'exfiltrate', 'disrupt', 'fraud'):
        # Failed connectivity check updates own access, without revealing the Blue order.
        match.intelligence['red'][order.target]['access'] = 0
    message = 'Action completed.' if success else 'Action did not achieve its aim; access or conditions may have changed.'
    if side == 'blue' and order.action == 'detect':
        found = bool(success and target['access'])
        message = 'Investigation found suspicious account access.' if found else 'No conclusive evidence found; this does not establish safety.'
        if found:
            match.observations['blue'].append(dict(turn=match.turn, type='finding', target=order.target, message=message))
    match.observations[side].append(dict(turn=match.turn, type='own_action', **order.dump(), message=message))
    if detected:
        # An alert is evidence of suspicious activity, never confirmation of Red's success or exact order.
        match.observations['blue'].append(dict(turn=match.turn, type='alert', target=order.target,
                                               message='Telemetry recorded suspicious activity. Investigate the asset; impact is unconfirmed.'))
    alternatives = []
    if side == 'red':
        # Include disrupted business services even when Red waits this round.
        targets = {key for key, asset in match.assets.items() if asset['isolated'] or asset['disrupted']}
        if target is not None:
            targets.add(order.target)
        blue_order = match.plans['blue']
        original_budget = match.budgets['blue'] + ACTIONS[blue_order.action].cost
        for target_id in sorted(targets):
            for candidate in ('monitor', 'patch', 'harden', 'segment', 'access_review', 'contain', 'recover', 'detect'):
                cost = ACTIONS[candidate].cost
                if cost <= min(original_budget, match.scenario.action_points) and (candidate != 'recover' or 'backup' in match.assets[target_id]['controls']):
                    alternatives.append(Order(candidate, target_id).dump())
    match.timeline.append(dict(turn=match.turn, side=side, **order.dump(), feasible=feasible,
                               success=success, detected=detected, success_probability=success_probability,
                               detection_probability=detection_probability, roll=roll, detection_roll=detection_roll,
                               before=before, after=deepcopy(target), framework=action.public(),
                               alternatives=alternatives))


def _finish_round(match):
    objective = match.scenario.objective
    flag = {'leak': 'leaked', 'fraud': 'fraud', 'disruption': 'disrupted'}[objective.kind]
    score = sum(match.assets[t]['value'] for t in objective.targets
                if match.assets[t][flag] or objective.kind == 'disruption' and match.assets[t]['isolated'])
    match.held = match.held + 1 if score >= objective.threshold else 0
    if match.held >= objective.hold_turns:
        match.winner = 'red'
    elif match.turn >= match.scenario.turn_limit:
        match.winner = 'blue'
    match.history.append({side: match.plans[side].dump() for side in SIDES})
    match.plans = {}
    if not match.winner:
        match.turn += 1


def commit(match, player, order, expected_turn, command_id):
    """Immutable domain command, with actor-scoped idempotency and round preconditions.

    The future adapter must lock/CAS the whole match, validate UUIDs at its HTTP
    boundary, and persist command receipts. This function does not claim DB locking.
    """
    side = _side(match, player)
    if match.rules_digest != catalog_digest():
        raise ValueError('Unsupported rules revision')
    if not isinstance(order, Order) or type(expected_turn) is not int:
        raise ValueError('Invalid command')
    if not isinstance(command_id, str) or not 1 <= len(command_id) <= 80:
        raise ValueError('Bounded command id required')
    receipt_key = side + ':' + command_id
    fingerprint = dict(turn=expected_turn, **order.dump())
    if receipt_key in match.receipts:
        if match.receipts[receipt_key] != fingerprint:
            raise ValueError('Command id reused with different content')
        return deepcopy(match)
    if match.winner or expected_turn != match.turn or side in match.plans:
        raise ValueError('Finished, stale or already committed round')
    if order not in available_orders(view(match, player)):
        raise ValueError('Order unavailable in this seat’s current information')
    result = deepcopy(match)
    result.plans[side] = order
    result.receipts[receipt_key] = fingerprint
    result.version += 1
    if len(result.plans) == 2:
        for acting_side in ('blue', 'red'):
            _resolve_action(result, acting_side, result.plans[acting_side])
        _finish_round(result)
    return result


def export_replay(match):
    """PRIVATE export; contains seed and sealed orders. No public endpoint exists."""
    return dict(engine_version=ENGINE_VERSION, rules_digest=match.rules_digest,
                scenario=match.scenario.snapshot(), scenario_digest=match.scenario.digest(),
                seed=match.seed, seats=deepcopy(match.seats), rounds=deepcopy(match.history),
                pending={side: order.dump() for side, order in match.plans.items()},
                commands=deepcopy(match.receipts))


def replay(record):
    """Recompute truth from a validated snapshot and transcript, never trust saved scores."""
    if set(record) != {'engine_version', 'rules_digest', 'scenario', 'scenario_digest', 'seed', 'seats', 'rounds', 'pending', 'commands'}:
        raise ValueError('Invalid replay envelope')
    if record['engine_version'] != ENGINE_VERSION or record['rules_digest'] != catalog_digest():
        raise ValueError('Unsupported rules revision; retain the original engine')
    scenario = parse_scenario(record['scenario'])
    if record['scenario_digest'] != scenario.digest():
        raise ValueError('Scenario snapshot changed')
    if set(record['seats']) != set(SIDES) or not isinstance(record['rounds'], list) or len(record['rounds']) > scenario.turn_limit:
        raise ValueError('Invalid replay seats or round count')
    match = new_match(scenario, record['seed'], record['seats']['red'], record['seats']['blue'])
    commands = record['commands']
    if not isinstance(commands, dict) or len(commands) > scenario.turn_limit * 2:
        raise ValueError('Invalid command transcript')
    for key, command in commands.items():
        if not isinstance(key, str) or ':' not in key or not isinstance(command, dict):
            raise ValueError('Invalid command transcript')
        if key.split(':', 1)[0] not in SIDES or set(command) != {'turn', 'action', 'target', 'source'} or type(command['turn']) is not int:
            raise ValueError('Invalid command transcript')
    # JSON object order (notably PostgreSQL JSONB) must not affect replay.
    for key, command in sorted(commands.items(), key=lambda item: (item[1]['turn'], item[0].split(':', 1)[0])):
        side, command_id = key.split(':', 1)
        match = commit(match, match.seats[side], Order(command['action'], command['target'], command['source']),
                       command['turn'], command_id)
    if record['rounds'] != match.history or record['pending'] != {s: o.dump() for s, o in match.plans.items()}:
        raise ValueError('Replay summaries do not match the command transcript')

    return match


def debrief(match, player):
    _side(match, player)
    if not match.winner:
        raise ValueError('Debrief is available only after the match')
    timeline, missed = [], []
    for event in match.timeline:
        clean = {k: deepcopy(event[k]) for k in ('turn', 'side', 'action', 'target', 'source', 'success', 'detected', 'framework')}
        timeline.append(clean)
        if event['side'] == 'red' and event['feasible'] and not event['detected'] and not event['action'].startswith('wait_'):
            missed.append(dict(turn=event['turn'], target=event['target'], action=event['action'],
                               success=event['success'], reason='No alert exposed this attempted activity.'))
        elif event['side'] == 'red' and event['detected'] and event['turn'] < len(match.history):
            responses = [e for e in match.timeline if e['side'] == 'blue' and e['turn'] > event['turn']
                         and e['target'] == event['target'] and e['action'] in ('detect', 'contain', 'access_review', 'recover')]
            if not responses:
                missed.append(dict(turn=event['turn'], target=event['target'], action=event['action'],
                                   success=event['success'], reason='The signal had a later response opportunity but no targeted investigation or response followed.'))
    # Re-run actual alternatives from each round's opening state, with the same
    # random stream and Red order. Report measured changes, not guaranteed wins.
    alternatives = []
    opening = new_match(match.scenario, match.seed, match.seats['red'], match.seats['blue'])
    for index, orders in enumerate(match.history):
        actual = match.timeline[index * 2 + 1]
        baseline = opening
        for side in SIDES:
            baseline = commit(baseline, baseline.seats[side], Order(**orders[side]), baseline.turn, f'debrief-{index}')
        for candidate in actual['alternatives']:
            option = Order(**candidate)
            if option == Order(**orders['blue']):
                continue
            trial = commit(opening, opening.seats['blue'], option, opening.turn, f'cf-blue-{index}')
            trial = commit(trial, trial.seats['red'], Order(**orders['red']), trial.turn, f'cf-red-{index}')
            changed = trial.timeline[-1]
            benefits = []
            if actual['success'] and not changed['success']:
                benefits.append('prevented this action')
            if not actual['detected'] and changed['detected']:
                benefits.append('produced an alert')
            if sum(a['value'] for a in trial.assets.values() if a['isolated'] or a['disrupted']) < sum(a['value'] for a in baseline.assets.values() if a['isolated'] or a['disrupted']):
                benefits.append('reduced business unavailability')
            if sum(o['type'] == 'finding' for o in trial.observations['blue']) > sum(o['type'] == 'finding' for o in baseline.observations['blue']):
                benefits.append('found evidence of account access')
            if benefits:
                alternatives.append(dict(turn=index + 1, **candidate,
                                         explanation='In this seeded round this alternative ' + ' and '.join(benefits) + '.',
                                         framework=ACTIONS[option.action].public()))
        opening = baseline
    return dict(winner=match.winner, objective=match.scenario.objective.model_dump(mode='json'),
                timeline=timeline, missed=missed, alternatives=alternatives,
                explanation='Full information is revealed after the match. Alternatives replay one round with the same seed; they do not guarantee a different final winner.')
