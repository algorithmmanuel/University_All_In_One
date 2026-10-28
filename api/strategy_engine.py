"""Branch Defender v1: deterministic fictional strategy rules, no live targets.

Keep v1 available for saved runs. Public state is an allowlist: the simulation's
seed, compromise flags and future events are never sent while a run is active.
"""
from copy import deepcopy
from hashlib import sha256

REVISION = 'branch-defender-v1'
ASSETS = (
    ('gateway', 'Branch gateway', 'Network boundary', 10, 12, 46),
    ('staff', 'Staff workstation', 'Customer service', 20, 31, 27),
    ('identity', 'Identity service', 'Staff access', 15, 31, 70),
    ('app', 'Banking application', 'Branch transactions', 25, 57, 27),
    ('database', 'Customer database', 'Transaction records', 25, 80, 46),
    ('backup', 'Recovery vault', 'Protected recovery', 5, 57, 70),
)
LINKS = [('gateway', 'staff'), ('gateway', 'app'), ('staff', 'identity'),
         ('identity', 'app'), ('app', 'database'), ('database', 'backup')]
ACTIONS = {
    'inspect': {'label': 'Investigate', 'cost': 0, 'help': 'Reveal this asset’s current condition; uses one staff action.'},
    'monitor': {'label': 'Deploy monitoring', 'cost': 4, 'help': 'Reveal future compromise here. Monitoring detects; it does not prevent.'},
    'patch': {'label': 'Patch system', 'cost': 3, 'help': 'Reduce simulated exploit risk next turn; maintenance interrupts service until then.'},
    'isolate': {'label': 'Isolate asset', 'cost': 0, 'help': 'Stop links to this asset immediately; its service becomes unavailable.'},
    'reconnect': {'label': 'Reconnect asset', 'cost': 0, 'help': 'Restore connectivity. Unresolved compromise can spread again.'},
    'mfa': {'label': 'Strengthen sign-in', 'cost': 4, 'help': 'Identity service only: stop the scenario’s stolen-password entry path. Existing compromise remains.'},
    'segment': {'label': 'Segment database', 'cost': 5, 'help': 'Database only: block the application-to-database spread path, with no service outage in this simplified model.'},
    'backup': {'label': 'Verify recovery copy', 'cost': 4, 'help': 'Recovery vault only: prepare a protected copy next turn. Recovery still requires containment.'},
    'restore': {'label': 'Restore asset', 'cost': 3, 'help': 'Requires an isolated asset and verified copy. Clears compromise next turn, leaving it isolated.'},
}


def new_state(seed):
    return {'revision': REVISION, 'seed': seed, 'turn': 1, 'version': 0,
            'budget': 30, 'staff': 3, 'status': 'active', 'exposure': 0,
            'copy_ready': False, 'segmented': False, 'mfa': False,
            'low_service_turns': 0, 'assets': {key: {'isolated': False,
                'patched': False, 'monitored': False, 'compromised': False,
                'known': False, 'pending': None} for key, *_ in ASSETS},
            'events': [{'turn': 1, 'message': 'Your shift starts. Protect access, improve visibility and prepare recovery. Three staff actions per turn.'}]}


def availability(s):
    return sum(weight for key, _, _, weight, *_ in ASSETS
               if not s['assets'][key]['isolated'] and not s['assets'][key]['pending'])


def event(s, message):
    s['events'].append({'turn': s['turn'], 'message': message})


def allowed(s, key):
    a = s['assets'][key]
    result = ['inspect']
    if not a['monitored']: result.append('monitor')
    if not a['pending'] and not a['patched']: result.append('patch')
    result.append('reconnect' if a['isolated'] else 'isolate')
    if key == 'identity' and not s['mfa']: result.append('mfa')
    if key == 'database' and not s['segmented']: result.append('segment')
    if key == 'backup' and not s['copy_ready'] and not a['pending']: result.append('backup')
    if a['isolated'] and s['copy_ready'] and not a['pending']: result.append('restore')
    return [name for name in result if ACTIONS[name]['cost'] <= s['budget']]


def advance(source, action, target=None):
    """Return a new state or reject an illegal command without changing input."""
    s = deepcopy(source)
    if s['revision'] != REVISION or s['status'] != 'active':
        raise ValueError('This simulation is no longer active')
    if action == 'end_turn':
        tick(s)
    else:
        if target not in s['assets'] or action not in allowed(s, target):
            raise ValueError('Action unavailable for this asset')
        if s['staff'] < 1: raise ValueError('Advance the turn to refresh staff actions')
        a = s['assets'][target]
        s['budget'] -= ACTIONS[action]['cost']; s['staff'] -= 1
        if action == 'inspect': a['known'] = True
        elif action == 'monitor': a['monitored'] = True; a['known'] = True
        elif action in ('patch', 'restore', 'backup'): a['pending'] = action
        elif action == 'isolate': a['isolated'] = True
        elif action == 'reconnect': a['isolated'] = False
        elif action == 'mfa': s['mfa'] = True
        elif action == 'segment': s['segmented'] = True
        label = next(label for key, label, *_ in ASSETS if key == target)
        event(s, ACTIONS[action]['label'] + ': ' + label + '.')
    s['version'] += 1
    return s


def tick(s):
    s['turn'] += 1; s['staff'] = 3
    for key, a in s['assets'].items():
        if not a['monitored']: a['known'] = False
        pending = a['pending']; a['pending'] = None
        if pending == 'patch': a['patched'] = True
        elif pending == 'restore':
            a['compromised'] = False; a['known'] = True
            event(s, 'Recovery completed for ' + key + '; verify conditions before reconnecting.')
        elif pending == 'backup':
            if a['compromised']: event(s, 'Recovery verification failed: investigate the vault before trusting it.')
            else: s['copy_ready'] = True; event(s, 'A protected recovery copy is verified.')
    assets = s['assets']
    def infect(key, reason):
        a = assets[key]
        if not a['isolated'] and not a['compromised']:
            a['compromised'] = True
            if a['monitored']: a['known'] = True; event(s, 'Monitoring alert on ' + key + ': ' + reason)
    if s['turn'] == 2:
        if not s['mfa']: infect('staff', 'unauthorised access following a stolen-password sign-in')
        else: event(s, 'Sign-in control blocked this scenario’s stolen-password entry attempt.')
    if s['turn'] == 4:
        if not assets['app']['patched']: infect('app', 'unpatched application entry condition')
        else: event(s, 'Application patch blocked this scenario’s exploit entry attempt.')
    # Use a pre-spread snapshot: an adversary cannot traverse the entire graph in one turn.
    infected = {key for key, a in assets.items() if a['compromised'] and not a['isolated']}
    for left, right in LINKS:
        for origin, destination in ((left, right), (right, left)):
            a = assets[destination]
            blocked = (a['isolated'] or a['patched'] or
                       (destination == 'identity' and s['mfa']) or
                       (set((origin, destination)) == {'app', 'database'} and s['segmented']) or
                       (destination == 'backup' and s['copy_ready']))
            roll = int(sha256(f"{s['seed']}:{s['turn']}:{origin}:{destination}".encode()).hexdigest()[:8], 16) % 100
            if origin in infected and not blocked and roll < 55:
                infect(destination, 'correlated lateral activity')
    if assets['database']['compromised'] and not assets['database']['isolated']:
        s['exposure'] = min(100, s['exposure'] + 25)
        event(s, 'Data-loss indicator increased. Investigate the database and its connections.')
    if s['turn'] in (3, 6):
        event(s, 'Service desk reports an unusual sign-in. Investigate before deciding whether it is malicious.')
    service = availability(s)
    s['low_service_turns'] = s['low_service_turns'] + 1 if service < 25 else 0
    if s['exposure'] >= 100 or s['low_service_turns'] >= 2:
        s['status'] = 'lost'; event(s, 'Shift ended: data exposure or prolonged service loss exceeded the scenario limit.')
    elif s['turn'] >= 8 and not any(a['compromised'] for a in assets.values()) and service >= 80 and s['copy_ready']:
        s['status'] = 'won'; event(s, 'Shift secured: threats cleared, recovery verified and core service available.')
    elif s['turn'] >= 18:
        s['status'] = 'lost'; event(s, 'Shift ended: containment and recovery goals were not met by turn 18.')


def public(s):
    result = {key: s[key] for key in ('revision', 'turn', 'version', 'budget', 'staff',
                                     'status', 'exposure', 'copy_ready', 'segmented', 'mfa')}
    result['availability'] = availability(s)
    result['links'] = LINKS
    result['assets'] = []
    for key, label, role, weight, x, y in ASSETS:
        a = s['assets'][key]
        result['assets'].append({'id': key, 'label': label, 'role': role, 'weight': weight, 'x': x, 'y': y,
            'isolated': a['isolated'], 'patched': a['patched'], 'monitored': a['monitored'],
            'pending': a['pending'], 'condition': ('Compromise detected' if a['compromised'] else 'No compromise observed') if a['known'] else 'Not investigated',
            'actions': [{**ACTIONS[name], 'id': name} for name in allowed(s, key)] if s['status'] == 'active' else []})
    result['events'] = s['events'][-120:]
    if s['status'] != 'active':
        result['debrief'] = {'remaining_compromise': [key for key, a in s['assets'].items() if a['compromised']],
            'availability': availability(s), 'exposure': s['exposure'], 'budget_remaining': s['budget'],
            'lessons': ['Monitoring reveals activity; it does not remove compromise.',
                        'Patching reduces this model’s exploit paths but does not clean an existing compromise.',
                        'Isolation limits spread at an availability cost. Restore from a verified copy, then reconnect deliberately.',
                        'These simplified simulation outcomes are not a measure of professional mastery.']}
    return result
