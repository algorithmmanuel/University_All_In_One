"""Branch Siege v1: original, bounded incident-command strategy simulation.

All transitions are fictional and server-owned. Preserve this module/revision for
saved runs. A replay reuses its private seed but never exposes it or future state.
"""
from copy import deepcopy
from hashlib import sha256

REVISION = 'branch-siege-v1'
INFO = {
    'id': 'siege', 'title': 'Branch Siege', 'difficulty': 'Advanced', 'lesson': 'recover',
    'summary': 'Command an active incident across eight assets. Investigate uncertain signals, contain existing compromise and close the remaining entry paths while keeping connected services operating.',
    'objective': 'By turn 18, close all three entry paths, clear compromise, verify recovery, validate the application and database, and retain at least 80% service. Victory can occur from turn 10.',
}
ASSETS = (
    ('remote', 'Remote-access broker', 'Supplier access', 0, 12, 24),
    ('gateway', 'Branch gateway', 'Network boundary', 10, 12, 70),
    ('staff', 'Staff workstation', 'Customer service', 20, 35, 24),
    ('identity', 'Identity service', 'Staff access dependency', 15, 35, 70),
    ('app', 'Banking application', 'Transactions: needs identity and database', 25, 58, 24),
    ('collector', 'Monitoring collector', 'Telemetry dependency', 0, 58, 70),
    ('database', 'Customer database', 'Records: needs identity and application', 25, 82, 24),
    ('backup', 'Recovery vault', 'Protected recovery', 5, 82, 70),
)
LINKS = [('remote', 'gateway'), ('gateway', 'staff'), ('gateway', 'app'),
         ('staff', 'identity'), ('identity', 'app'), ('app', 'database'),
         ('database', 'backup'), ('staff', 'collector')]
ACTIONS = {
    'inspect': {'label': 'Investigate', 'cost': 0, 'duration': 0,
        'help': 'Inspect this asset now. The finding describes this observation, not every future turn.'},
    'monitor': {'label': 'Deploy monitoring', 'cost': 4, 'duration': 0,
        'help': 'Observe this asset while it and the collector are reachable and the collector is trustworthy in this model. Does not prevent compromise.'},
    'patch': {'label': 'Patch system', 'cost': 3, 'duration': 2,
        'help': 'Two-turn maintenance outage. Blocks this model’s exploit path after completion; does not clean existing compromise.'},
    'isolate': {'label': 'Isolate asset', 'cost': 0, 'duration': 0,
        'help': 'Immediately stop links and service for this asset. Dependent services may also stop.'},
    'validate': {'label': 'Validate recovery', 'cost': 0, 'duration': 0,
        'help': 'Inspect current state and record the validation result. Required after isolation/restoration before reconnecting.'},
    'reconnect': {'label': 'Reconnect asset', 'cost': 0, 'duration': 0,
        'help': 'Requires a completed clean validation after containment. Restores connectivity; other dependencies may remain offline.'},
    'mfa': {'label': 'Strengthen sign-in', 'cost': 4, 'duration': 0,
        'help': 'Identity only: close the password entry path. Does not revoke the supplier credential or clean existing compromise.'},
    'revoke_vendor': {'label': 'Revoke supplier access', 'cost': 4, 'duration': 0,
        'help': 'Broker only: invalidate the exposed supplier credential. Existing broker compromise and network paths remain.'},
    'segment': {'label': 'Segment database', 'cost': 5, 'duration': 0,
        'help': 'Database only: restrict the modeled spread path without blocking the approved application service.'},
    'backup': {'label': 'Verify recovery copy', 'cost': 4, 'duration': 2,
        'help': 'Vault only: two-turn verification outage. Fails if the vault is affected when verification completes.'},
    'restore': {'label': 'Restore asset', 'cost': 4, 'duration': 2,
        'help': 'Requires isolation and a verified copy. Clears compromise after two turns; validation and reconnection are separate actions.'},
}


def _roll(s, context):
    return int(sha256(f"{s['seed']}:{context}".encode()).hexdigest()[:8], 16)


def _event(s, message):
    s['events'].append({'turn': s['turn'], 'message': message})


def _signal(s, key, message):
    # Turns, staff and entry/spread bounds cap this queue; reviewed records remain.
    s['signals'].append({'id': 'signal-' + str(len(s['signals']) + 1), 'asset': key,
        'turn': s['turn'], 'message': message, 'reviewed': False, 'finding': None})


def new_state(seed):
    s = {'revision': REVISION, 'scenario': 'siege', 'seed': seed, 'turn': 1,
        'version': 0, 'budget': 38, 'staff': 3, 'status': 'active', 'exposure': 0,
        'copy_ready': False, 'segmented': False, 'mfa': False, 'vendor_revoked': False,
        'low_service_turns': 0, 'support_used': False, 'signals': [], 'decisions': [],
        'events': [], 'assets': {key: {'isolated': False, 'patched': False,
            'monitored': False, 'compromised': False, 'known': False, 'pending': None,
            'observed': None, 'observed_at': None,
            'due_turn': None, 'validated_at': None, 'validated_clean': False}
            for key, *_ in ASSETS}}
    foothold = ('staff', 'remote')[_roll(s, 'opening') % 2]
    s['assets'][foothold]['compromised'] = True
    # Ordering varies: the first signal is not always the affected asset.
    for key in sorted(('staff', 'remote'), key=lambda key: _roll(s, 'signal:' + key)):
        _signal(s, key, 'Service desk reports an unfamiliar session. Verify context and current asset state.')
    _event(s, 'An active foothold is present, but initial signals need investigation. The opponent will reuse whichever entry paths remain reachable. You have 38 credits and three staff actions per turn.')
    s['history'] = [{'turn': 1, 'availability': availability(s), 'exposure': 0}]
    return s


def _online(s, key):
    a = s['assets'][key]
    return not a['isolated'] and not a['pending']


def availability(s):
    core = all(_online(s, key) for key in ('identity', 'app', 'database'))
    return sum(weight for key, _, _, weight, *_ in ASSETS
        if _online(s, key) and (key not in ('app', 'database') or core))


def _telemetry(s):
    return _online(s, 'collector') and not s['assets']['collector']['compromised']


def _observe(s, key, validate=False):
    a = s['assets'][key]
    a['known'] = True; a['observed'] = a['compromised']; a['observed_at'] = s['turn']
    finding = 'Compromise detected' if a['compromised'] else 'No compromise observed'
    if validate:
        a['validated_at'] = s['turn']
        a['validated_clean'] = not a['compromised']
        finding = 'Validation failed: compromise detected' if a['compromised'] else 'Clean validation recorded'
    return finding


def _reason(s, key, action):
    """Availability uses observable prerequisites, never hidden compromise flags."""
    a = s['assets'][key]
    if s['status'] != 'active': return 'This shift has ended.'
    if a['pending']: return 'Wait for the queued work to finish.'
    if action == 'monitor' and a['monitored']: return 'Monitoring is already deployed.'
    if action == 'patch' and a['patched']: return 'The patch is already applied.'
    if action == 'isolate' and a['isolated']: return 'This asset is already isolated.'
    if action == 'reconnect':
        if not a['isolated']: return 'This asset is already connected.'
        if not a['validated_clean']: return 'Record a clean validation after containment first.'
    if action == 'mfa' and s['mfa']: return 'The sign-in control is already installed.'
    if action == 'revoke_vendor' and s['vendor_revoked']: return 'The supplier credential is already revoked.'
    if action == 'segment' and s['segmented']: return 'The database boundary is already restricted.'
    if action == 'backup' and s['copy_ready']: return 'The protected recovery copy is already verified.'
    if action == 'restore':
        if not a['isolated']: return 'Isolate this asset before restoration.'
        if not s['copy_ready']: return 'Verify the recovery copy first.'
    if s['budget'] < ACTIONS[action]['cost']: return 'Not enough credits for this action.'
    if s['staff'] < 1: return 'Advance the turn or mobilise emergency support.'
    return None


def _asset_actions(key):
    actions = ['inspect', 'monitor', 'patch', 'isolate', 'validate', 'reconnect']
    if key == 'identity': actions.append('mfa')
    if key == 'remote': actions.append('revoke_vendor')
    if key == 'database': actions.append('segment')
    if key == 'backup': actions.append('backup')
    return actions + ['restore']


def _record(s, action, target, cost, before):
    s['decisions'].append({'turn': s['turn'], 'action': action,
        'label': ACTIONS[action]['label'] if action in ACTIONS else ('Investigate signal' if action == 'investigate_signal' else 'Mobilise emergency support'), 'target': target,
        'cost': cost, 'service_before': before, 'service_after': availability(s)})


def advance(source, action, target=None):
    if source.get('revision') != REVISION or source['status'] != 'active':
        raise ValueError('This simulation is no longer active')
    s = deepcopy(source)
    before = availability(s)
    if action == 'end_turn':
        if target is not None: raise ValueError('Advance turn does not take a target')
        _tick(s)
    elif action == 'call_support':
        if target != 'support' or s['support_used'] or s['budget'] < 6:
            raise ValueError('Emergency support is unavailable')
        s['support_used'] = True; s['budget'] -= 6; s['staff'] += 2
        _event(s, 'Emergency support mobilised: six credits exchanged for two staff actions this turn only.')
        _record(s, action, target, 6, before)
    elif action == 'investigate_signal':
        signal = next((item for item in s['signals'] if item['id'] == target), None)
        if signal is None or signal['reviewed'] or s['staff'] < 1:
            raise ValueError('Signal investigation is unavailable')
        if s['assets'][signal['asset']]['pending']:
            raise ValueError('Wait for asset maintenance before investigating its current state')
        s['staff'] -= 1
        finding = _observe(s, signal['asset'])
        signal.update(reviewed=True, finding=finding, reviewed_turn=s['turn'], review_order=len(s['decisions']))
        _event(s, f"Signal investigated on {signal['asset']}: {finding}. This is an observation at turn {s['turn']}.")
        _record(s, action, target, 0, before)
    else:
        if target not in s['assets'] or action not in _asset_actions(target):
            raise ValueError('Action unavailable for this asset')
        reason = _reason(s, target, action)
        if reason: raise ValueError(reason)
        a = s['assets'][target]
        cost = ACTIONS[action]['cost']
        s['budget'] -= cost; s['staff'] -= 1
        if action == 'inspect': _event(s, target + ': ' + _observe(s, target) + '.')
        elif action == 'validate': _event(s, target + ': ' + _observe(s, target, validate=True) + '.')
        elif action == 'monitor': a['monitored'] = True
        elif action in ('patch', 'restore', 'backup'):
            a['pending'] = action; a['due_turn'] = s['turn'] + ACTIONS[action]['duration']
            a['validated_at'] = None; a['validated_clean'] = False
        elif action == 'isolate':
            a['isolated'] = True; a['validated_at'] = None; a['validated_clean'] = False
        elif action == 'reconnect': a['isolated'] = False
        elif action == 'mfa': s['mfa'] = True
        elif action == 'revoke_vendor': s['vendor_revoked'] = True
        elif action == 'segment': s['segmented'] = True
        _event(s, f"{ACTIONS[action]['label']}: {target}. Service {before}% → {availability(s)}%.")
        _record(s, action, target, cost, before)
    s['version'] += 1
    return s


def _infect(s, key, reason):
    a = s['assets'][key]
    if not _online(s, key) or a['compromised']: return
    a['compromised'] = True
    if a['monitored'] and _telemetry(s):
        _observe(s, key)
        _signal(s, key, 'Monitoring reports activity requiring investigation: ' + reason)
        _event(s, 'Monitoring detected compromise on ' + key + '.')


def _tick(s):
    s['turn'] += 1; s['staff'] = 3
    for key, a in s['assets'].items():
        a['known'] = False
        if a['pending'] and a['due_turn'] <= s['turn']:
            pending = a['pending']; a['pending'] = None; a['due_turn'] = None
            if pending == 'patch': a['patched'] = True
            elif pending == 'restore':
                a['compromised'] = False; _observe(s, key)
                _event(s, 'Restoration completed for ' + key + '; validate it before reconnecting.')
            elif pending == 'backup':
                if a['compromised']: _event(s, 'Recovery verification failed: investigate the affected vault.')
                else: s['copy_ready'] = True; _event(s, 'Protected recovery copy verified.')
            _event(s, f'{pending} work completed on {key}.')
    # The opponent picks among currently reachable, unprotected entry paths.
    # Stored seeds make identical decisions reproducible without public forecasts.
    if s['turn'] % 2 == 0:
        candidates = []
        if not s['mfa'] and _online(s, 'staff'): candidates.append('staff')
        if not s['assets']['app']['patched'] and _online(s, 'app'): candidates.append('app')
        if not s['vendor_revoked'] and _online(s, 'remote'): candidates.append('remote')
        if candidates:
            target = candidates[_roll(s, str(s['turn']) + ':entry') % len(candidates)]
            _infect(s, target, 'entry path reused')
            _signal(s, target, 'An unfamiliar session was reported. Verify whether access was authorised and assess the current asset.')
            _event(s, 'The opponent attempted a remaining entry path. Review the signal queue.')
        else: _event(s, 'The opponent found no reachable open entry path in this model. Existing compromise can still persist.')
    infected = {key for key, a in s['assets'].items() if a['compromised'] and _online(s, key)}
    chance = 35 if s['turn'] < 6 else (50 if s['turn'] < 10 else 65)
    for left, right in LINKS:
        for origin, destination in ((left, right), (right, left)):
            a = s['assets'][destination]
            blocked = (a['patched'] or (destination == 'identity' and s['mfa'])
                or (set((origin, destination)) == {'app', 'database'} and s['segmented'])
                or (destination == 'backup' and s['copy_ready']))
            if origin in infected and not blocked and _roll(s, f'{s["turn"]}:{origin}:{destination}') % 100 < chance:
                _infect(s, destination, 'connected asset activity')
    if _telemetry(s):
        for key, a in s['assets'].items():
            if a['monitored'] and _online(s, key): _observe(s, key)
    if s['turn'] in (3, 7):
        _signal(s, 'collector', 'A collector service restart was reported. Verify current state before escalating.')
    if s['assets']['database']['compromised'] and _online(s, 'database'):
        s['exposure'] = min(100, s['exposure'] + 20)
        _event(s, 'Database exposure indicator increased by 20 points.')
    service = availability(s)
    s['history'].append({'turn': s['turn'], 'availability': service, 'exposure': s['exposure']})
    s['low_service_turns'] = s['low_service_turns'] + 1 if service < 25 else 0
    controls = s['mfa'] and s['vendor_revoked'] and s['assets']['app']['patched']
    validated = all(s['assets'][key]['validated_clean'] for key in ('app', 'database'))
    if s['exposure'] >= 100 or s['low_service_turns'] >= 2:
        s['status'] = 'lost'; _event(s, 'Incident limits exceeded: exposure or sustained service loss.')
    elif (s['turn'] >= 10 and controls and s['copy_ready'] and validated and service >= 80
            and not any(a['compromised'] for a in s['assets'].values())):
        s['status'] = 'won'; _event(s, 'Incident goals met: entry closed, threats cleared, validated recovery and service available.')
    elif s['turn'] >= 18:
        s['status'] = 'lost'; _event(s, 'Turn limit reached before incident goals were met.')


def summary(s):
    """Safe terminal metrics for replay comparison; no seed or private state."""
    service_values = [item['availability'] for item in s['history']]
    service_values += [item['service_after'] for item in s['decisions']]
    return {'status': s['status'], 'turns': s['turn'], 'exposure': s['exposure'],
        'lowest_service': min(service_values), 'credits_spent': 38 - s['budget'],
        'actions_used': len(s['decisions']),
        'signals_reviewed': sum(item['reviewed'] for item in s['signals'])}


def public(s):
    result = {key: s[key] for key in ('revision', 'turn', 'version', 'budget', 'staff',
        'status', 'exposure', 'copy_ready', 'segmented', 'mfa', 'vendor_revoked')}
    result.update(scenario='siege', scenario_info=INFO, availability=availability(s), links=LINKS,
        assets=[], events=deepcopy(s['events'][-160:]))
    for key, label, role, weight, x, y in ASSETS:
        a = s['assets'][key]
        actions = []
        if s['status'] == 'active':
            for action in _asset_actions(key):
                reason = _reason(s, key, action)
                actions.append({**ACTIONS[action], 'id': action, 'available': reason is None,
                                'reason': reason, 'staff_cost': 1})
        result['assets'].append({'id': key, 'label': label, 'role': role, 'weight': weight,
            'x': x, 'y': y, 'isolated': a['isolated'], 'patched': a['patched'],
            'monitored': a['monitored'], 'pending': a['pending'], 'due_turn': a['due_turn'],
            'validated_at': a['validated_at'], 'observed_at': a['observed_at'],
            'condition': ('Compromise detected' if a['observed'] else 'No compromise observed') if a['known'] else 'Not investigated',
            'actions': actions})
    jobs = [{'asset': key, 'action': a['pending'], 'due_turn': a['due_turn']}
            for key, a in s['assets'].items() if a['pending']]
    result['tactics'] = {
        'pressure': 'Intense' if s['turn'] >= 10 else ('Elevated' if s['turn'] >= 6 else 'Building'),
        'signals': deepcopy(s['signals']), 'jobs': jobs, 'history': deepcopy(s['history']),
        'support_used': s['support_used'], 'support_available': s['status'] == 'active' and not s['support_used'] and s['budget'] >= 6,
        'objectives': [
            {'label': 'Close password, supplier and application entry paths', 'met': bool(s['mfa'] and s['vendor_revoked'] and s['assets']['app']['patched'])},
            {'label': 'Verify a protected recovery copy', 'met': s['copy_ready']},
            {'label': 'Record clean application and database validations', 'met': all(s['assets'][key]['validated_clean'] for key in ('app', 'database'))},
            {'label': 'Keep at least 80% current service available', 'met': availability(s) >= 80}],
        'rules': [
            'There is an active foothold at the opening. Signals can also describe benign activity. Investigation costs one staff action.',
            'Every second turn the opponent chooses a reachable open entry path. Spread pressure rises at turns 6 and 10; spread advances at most one hop per turn.',
            'Patch, restore and backup verification each take two turns. Pending work and isolation remove the asset’s service.',
            'Application and database service require identity, application and database to be online together. The collector and broker have no direct service weight.',
            'Monitoring depends on the collector. A quiet collector is not a clean-state guarantee. Manual investigation remains available.',
            'After isolation or restoration, validate before reconnecting. Revocation, patching and monitoring do not clean existing compromise.',
            'Lose at 100 exposure or after two turn advances below 25% service. Exposure is a fictional indicator, not a claim of actual data theft.'],
    }
    if s.get('replay_of'): result['replay_of'] = s['replay_of']
    if s['status'] != 'active':
        result['debrief'] = {'remaining_compromise': [key for key, a in s['assets'].items() if a['compromised']],
            'lessons': [
                'Compare the service-before/service-after entries: containment and maintenance can stop dependent services.',
                'Review which signals were investigated and when; a benign finding is bounded to its observation.',
                'Entry controls prevent specified paths while existing footholds still require recovery.',
                'Compare another strategy against the same private opening; this simulation is not a measure of professional mastery.'],
            'metrics': summary(s), 'decisions': deepcopy(s['decisions']),
            'history': deepcopy(s['history']), 'comparison': deepcopy(s.get('comparison_baseline'))}
    return result
