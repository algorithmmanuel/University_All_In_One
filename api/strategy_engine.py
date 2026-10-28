"""Version dispatcher. Saved Build A runs retain the unchanged v1 rule module."""
import strategy_v1 as v1
import strategy_scenarios as scenarios

REVISION, ASSETS, LINKS, ACTIONS = v1.REVISION, v1.ASSETS, v1.LINKS, v1.ACTIONS


def new_state(seed, scenario='branch'):
    if scenario == 'branch': return v1.new_state(seed)
    return scenarios.new_state(seed, scenario)


def _rules(state):
    if state.get('revision') == v1.REVISION: return v1
    if state.get('revision') == scenarios.REVISION: return scenarios
    raise ValueError('Unsupported saved scenario revision')


def advance(state, action, target=None):
    return _rules(state).advance(state, action, target)


def availability(state):
    return _rules(state).availability(state)


def public(state):
    result = _rules(state).public(state)
    if state['revision'] == v1.REVISION:
        result.update(scenario='branch', scenario_info=scenarios.SCENARIOS['branch'])
    return result
