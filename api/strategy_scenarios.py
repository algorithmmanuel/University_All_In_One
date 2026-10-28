"""Build B scenarios. Reuse v1 controls without altering its stored-run rules."""
from copy import deepcopy
from hashlib import sha256
import strategy_v1 as base

REVISION = 'branch-scenarios-v2'
SCENARIOS = {
    'branch': {'id': 'branch', 'title': 'Defend the branch', 'difficulty': 'Beginner',
        'summary': 'Prepare controls before stolen-password and application entry attempts.',
        'objective': 'Clear all compromise, verify recovery and retain at least 80% service from turn 8, by turn 18.',
        'lesson': 'protect'},
    'supplier': {'id': 'supplier', 'title': 'Supplier Access Crisis', 'difficulty': 'Intermediate',
        'summary': 'A supplier service credential provides a recurring entry path. Staff MFA alone will not revoke it.',
        'objective': 'Revoke supplier access, clear compromise, verify recovery and retain at least 80% service from turn 10, by turn 18.',
        'lesson': 'defend'},
    'ransomware': {'id': 'ransomware', 'title': 'Recovery Under Pressure', 'difficulty': 'Intermediate',
        'summary': 'Workstation compromise and encrypted application/database services are already present. Contain and restore safely. Exposure is a scripted risk indicator; encryption alone does not prove data theft.',
        'objective': 'Recover encrypted services, clear compromise, verify recovery and retain at least 80% service from turn 8, by turn 18.',
        'lesson': 'recover'},
}
REVOKE = {'id': 'revoke_vendor', 'label': 'Revoke supplier access', 'cost': 4,
          'help': 'Gateway only: close the recurring supplier credential entry path. Existing compromise still needs containment and restoration.'}


def new_state(seed, scenario):
    if scenario not in ('supplier', 'ransomware'): raise ValueError('Unknown scenario')
    s = base.new_state(seed)
    s.update(revision=REVISION, scenario=scenario, vendor_revoked=False)
    for a in s['assets'].values(): a['encrypted'] = False
    if scenario == 'ransomware':
        for key in ('staff', 'app', 'database'):
            s['assets'][key].update(compromised=True, known=True)
        for key in ('app', 'database'): s['assets'][key]['encrypted'] = True
        s['events'] = [{'turn': 1, 'message': 'Application and database services are encrypted. Workstation compromise is confirmed. Contain affected assets, protect recovery and preserve remaining service.'}]
    else:
        s['events'] = [{'turn': 1, 'message': 'Supplier remote access remains enabled on the gateway. A service credential may be exposed. Revocation and existing compromise are separate problems.'}]
    return s


def availability(s):
    return sum(weight for key, _, _, weight, *_ in base.ASSETS if not (
        s['assets'][key]['isolated'] or s['assets'][key]['pending'] or s['assets'][key]['encrypted']))


def advance(source, action, target=None):
    if source['revision'] != REVISION or source['scenario'] not in ('supplier', 'ransomware'):
        raise ValueError('Unsupported scenario revision')
    if source['status'] != 'active': raise ValueError('This simulation is no longer active')
    if action == 'revoke_vendor':
        if (source['scenario'] != 'supplier' or target != 'gateway' or source['vendor_revoked']
                or source['budget'] < REVOKE['cost'] or source['staff'] < 1):
            raise ValueError('Supplier revocation is unavailable')
        s = deepcopy(source); s['vendor_revoked'] = True
        s['budget'] -= REVOKE['cost']; s['staff'] -= 1; s['version'] += 1
        base.event(s, 'Supplier service credential revoked. Existing compromised assets still require investigation and recovery.')
        return s
    if action == 'reconnect' and target in source['assets'] and source['assets'][target]['pending'] == 'restore':
        raise ValueError('Wait for restoration to finish before reconnecting')
    if action != 'end_turn':
        # v1 remains unchanged. Its non-turn controls preserve additional fields.
        editable = deepcopy(source); editable['revision'] = base.REVISION
        s = base.advance(editable, action, target); s['revision'] = REVISION
        return s
    s = deepcopy(source); s['turn'] += 1; s['staff'] = 3
    for key, a in s['assets'].items():
        if not a['monitored']: a['known'] = False
        pending = a['pending']; a['pending'] = None
        if pending == 'patch': a['patched'] = True
        elif pending == 'restore':
            a.update(compromised=False, encrypted=False, known=True)
            base.event(s, 'Recovery completed for ' + key + '; validate before reconnecting.')
        elif pending == 'backup':
            if a['compromised']: base.event(s, 'Recovery verification failed: the vault is affected.')
            else: s['copy_ready'] = True; base.event(s, 'Protected recovery copy verified.')
    assets = s['assets']
    def infect(key, reason):
        a = assets[key]
        if not a['isolated'] and not a['compromised']:
            a['compromised'] = True
            if s['scenario'] == 'ransomware': a['encrypted'] = True
            if a['monitored']:
                a['known'] = True; base.event(s, 'Monitoring detected activity on ' + key + ': ' + reason)
    if s['scenario'] == 'supplier' and s['turn'] in (3, 6, 9):
        if not s['vendor_revoked']: infect('gateway', 'supplier credential reused')
        else: base.event(s, 'Revoked supplier credential blocked a repeat entry attempt.')
    infected = {key for key, a in assets.items() if a['compromised'] and not a['isolated']}
    for left, right in base.LINKS:
        for origin, destination in ((left, right), (right, left)):
            a = assets[destination]
            blocked = (a['isolated'] or a['patched'] or (destination == 'identity' and s['mfa'])
                or (set((origin, destination)) == {'app', 'database'} and s['segmented'])
                or (destination == 'backup' and s['copy_ready']))
            roll = int(sha256(f"{s['seed']}:{s['turn']}:{origin}:{destination}".encode()).hexdigest()[:8], 16) % 100
            if origin in infected and not blocked and roll < 55: infect(destination, 'connected asset activity')
    if assets['database']['compromised'] and not assets['database']['isolated']:
        s['exposure'] = min(100, s['exposure'] + 25); base.event(s, 'Database exposure indicator increased.')
    service = availability(s)
    s['low_service_turns'] = s['low_service_turns'] + 1 if service < 25 else 0
    earliest = 10 if s['scenario'] == 'supplier' else 8
    revoked = s['scenario'] != 'supplier' or s['vendor_revoked']
    if s['exposure'] >= 100 or s['low_service_turns'] >= 2:
        s['status'] = 'lost'; base.event(s, 'Scenario limit exceeded: exposure or prolonged service loss.')
    elif s['turn'] >= earliest and revoked and s['copy_ready'] and service >= 80 and not any(a['compromised'] for a in assets.values()):
        s['status'] = 'won'; base.event(s, 'Scenario goals met: containment, recovery and service validated.')
    elif s['turn'] >= 18:
        s['status'] = 'lost'; base.event(s, 'Turn limit reached before all scenario goals were met.')
    s['version'] += 1
    return s


def public(s):
    result = base.public(s)
    result['availability'] = availability(s)
    result.update(scenario=s['scenario'], scenario_info=SCENARIOS[s['scenario']], vendor_revoked=s['vendor_revoked'])
    for item in result['assets']:
        a = s['assets'][item['id']]
        if a['pending'] == 'restore': item['actions'] = [action for action in item['actions'] if action['id'] != 'reconnect']
        # Encryption is operationally visible, unlike private compromise state.
        item['encrypted'] = a['encrypted']
        if a['encrypted']: item['condition'] = 'Service encrypted'
        for action in item['actions']:
            if action['id'] == 'mfa': action['help'] = 'Reduce identity spread in this model; supplier service credentials need separate revocation. Existing compromise remains.'
        if (s['status'] == 'active' and s['scenario'] == 'supplier' and item['id'] == 'gateway'
                and not s['vendor_revoked'] and s['budget'] >= REVOKE['cost']): item['actions'].append(REVOKE)
    if s['status'] != 'active':
        result['debrief']['availability'] = availability(s)
        result['debrief']['lessons'].insert(0, 'Supplier service access and human MFA are separate controls.' if s['scenario'] == 'supplier' else 'Restore operational service from a verified copy after containing affected assets; reconnecting alone does not remove encryption.')
    return result
