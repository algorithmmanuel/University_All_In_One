"""Inspectable policies. Input is a seat projection, never private Match state.

Easy: inventory-first and basic hygiene. Standard: objective-first attacks and
alert-led containment/recovery. Hard: also ranks exposed weaknesses and critical
trust paths. All levels have identical resources and no random choice/extra intel.
"""
from .engine import available_orders

LEVELS = ('easy', 'standard', 'hard')


def choose_order(observation, difficulty):
    if difficulty not in LEVELS:
        raise ValueError('Unknown opponent difficulty')
    options = available_orders(observation)
    if not options:
        raise ValueError('Seat cannot plan now')
    assets = {a['id']: a for a in observation['assets']}
    objective = observation['objective']
    impact = {'fraud': 'fraud', 'leak': 'exfiltrate', 'disruption': 'disrupt'}[objective['kind']]
    signals = {o['target'] for o in observation['observations']
               if o['type'] in ('alert', 'finding') and o['turn'] >= observation['turn'] - 2}

    def priority(order):
        a = assets.get(order.target, {})
        aid = order.action
        score = -100
        if observation['side'] == 'red':
            if difficulty == 'easy':
                score = {'recon': 80, 'escalate': 65, 'lateral': 60, impact: 70,
                         'phish': 50, 'cloud_access': 50, 'prompt_injection': 55}.get(aid, -100)
            else:
                score = {impact: 110, 'escalate': 85, 'lateral': 80, 'recon': 65,
                         'phish': 60, 'cloud_access': 60, 'prompt_injection': 62, 'persist': 20}.get(aid, -100)
            if aid == 'recon' and a.get('assessed') is not None:
                score = -80
            if aid == 'recon' and not (a.get('exposed') or a.get('access') or any(
                    e['target'] == order.target and assets[e['source']]['access'] > 0
                    for e in observation['connections'])):
                score = -90
            if aid in ('fraud', 'exfiltrate', 'disrupt') and (aid != impact or order.target not in objective['targets']):
                score = -90
            if difficulty == 'hard':
                if order.target in objective['targets']:
                    score += 10
                assessed = a.get('assessed') or {}
                if aid in ('cloud_access', 'escalate', 'phish', 'prompt_injection') and 'hardened' in assessed.get('controls', []):
                    score -= 30
                if aid == 'lateral' and 'segmented' in assessed.get('controls', []):
                    score = -90
        else:
            controls = a.get('controls', [])
            if aid == 'monitor' and 'monitoring' not in controls:
                score = 65
            if aid == 'patch' and 'patched' not in controls:
                score = 50
            if difficulty != 'easy':
                if aid == 'recover' and (a.get('isolated') or a.get('disrupted')):
                    score = 140
                if aid == 'contain' and order.target in signals and not a.get('isolated'):
                    score = 110
                if aid == 'detect' and order.target in signals:
                    score = 40
                if aid == 'harden' and a.get('exposed') and 'hardened' not in controls:
                    score = 75
            if difficulty == 'hard':
                if aid == 'access_review' and order.target in signals and not a.get('isolated'):
                    score = 120
                if aid == 'segment' and 'segmented' not in controls and order.target in objective['targets']:
                    score = 85
                if aid == 'harden' and set(a.get('vulnerabilities', [])) & {'instruction', 'configuration', 'phishing'} and 'hardened' not in controls:
                    score = 95
        if aid.startswith('wait_'):
            score = -50
        return (-score, -a.get('value', 0) if difficulty == 'hard' else 0,
                aid, order.target or '', order.source or '')

    return min(options, key=priority)
