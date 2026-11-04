"""Tests for the isolated V2 projection; existing engine unchanged."""
import json
import pytest
from cyber_warfare.v2_state import (
    AssetTruth, Capability, Evidence, MatchTruth, SeatKnowledge, project_for_seat,
)


@pytest.fixture
def match():
    return MatchTruth(
        edition='red-blue-v2', turn=2,
        assets=(AssetTruth('app', 'App', 'server', 60, True, ('monitoring',), 2, True),
                AssetTruth('db', 'DB', 'database', 90, False, ('backup',))),
        capabilities=(Capability('sensor', 'blue', 'app', frozenset({'endpoint'})),
                      Capability('kit', 'red', 'app', action_ids=frozenset({'escalate'}))),
        evidence=(Evidence('r', 1, 'app', 'access', 'Confirmed foothold',
                           frozenset({'red'}), 'confirmed'),
                  Evidence('b', 1, 'app', 'alert', 'Suspicious authentication',
                           frozenset({'blue'}), 'suspected', 'endpoint')),
        blue_inventory=frozenset({'app', 'db'}),
        red_known=frozenset({'app'}),
        red_knowledge=(SeatKnowledge('app', 'stale', 1, 1),),
    )


def test_blue_does_not_see_attacker_truth(match):
    blue = project_for_seat(match, 'blue')
    encoded = json.dumps(blue)
    assert 'Confirmed foothold' not in encoded
    assert 'red_access' not in encoded and 'persistent' not in encoded
    assert 'kit' not in encoded
    assert 'Suspicious authentication' in encoded


def test_red_only_sees_discovered_assets(match):
    red = project_for_seat(match, 'red')
    assert len(red['assets']) == 1
    assert red['assets'][0]['knowledge'] == 'stale'
    assert red['assets'][0]['access'] == 1
    assert 'monitoring' not in json.dumps(red)
    assert 'Suspicious authentication' not in json.dumps(red)
    assert 'available' not in red['assets'][0]


def test_alert_requires_owned_sensor(match):
    unsensored = MatchTruth(**{**vars(match), 'capabilities': ()})
    assert project_for_seat(unsensored, 'blue')['assets'][0]['events'] == []


def test_unknown_seat_fails_closed(match):
    with pytest.raises(ValueError):
        project_for_seat(match, 'instructor')


from dataclasses import replace
from cyber_warfare.scenario import list_scenarios
from cyber_warfare.v2_scenario import scenario_initial_v2


def test_all_existing_scenarios_are_valid_v2_start_states():
    scenarios = list_scenarios()
    assert len(scenarios) == 6
    for scenario in scenarios:
        start = scenario_initial_v2(scenario)
        blue = project_for_seat(start, 'blue')
        red = project_for_seat(start, 'red')
        assert len(blue['assets']) == len(scenario.assets)
        assert len(red['assets']) == len(scenario.red.known_assets)
        assert len(start.blue_inventory) == len(scenario.assets)
        assert not any('red_access' in asset or 'persistent' in asset for asset in blue['assets'])
        assert not any('controls' in asset or 'available' in asset for asset in red['assets'])
        json.dumps(blue)
        json.dumps(red)


@pytest.mark.parametrize('change', [
    {'turn': 0},
    {'blue_inventory': frozenset({'missing'})},
    {'red_known': frozenset({'secret'})},
    {'evidence': (Evidence('r', 3, 'app', 'alert', 'Future alert',
                           frozenset({'blue'}), 'suspected', 'endpoint'),)},
    {'evidence': (Evidence('r', 1, 'missing', 'alert', 'Ghost asset',
                           frozenset({'blue'}), 'suspected', 'endpoint'),)},
    {'evidence': (Evidence('r', 1, 'app', 'alert', 'Fake confirmation',
                           frozenset({'blue'}), 'confirmed', 'endpoint'),)},
    {'evidence': (Evidence('r', 1, 'app', 'alert', 'Anomaly',
                           frozenset({'blue'}), 'suspected', 'endpoint'),) * 2},
    {'capabilities': (Capability('fake', 'blue', 'missing'),)},
    {'red_knowledge': (SeatKnowledge('db', 'confirmed', 1, 2),)},
])
def test_malformed_match_fails_closed(match, change):
    with pytest.raises(ValueError):
        project_for_seat(replace(match, **change), 'blue')


def test_monitoring_is_asset_scoped_not_global(match):
    moved = replace(match, capabilities=(Capability('sensor', 'blue', 'db',
                                                    frozenset({'endpoint'})),))
    blue = project_for_seat(moved, 'blue')
    assert blue['assets'][0]['events'] == []


def test_evidence_audience_never_expands_with_capabilities(match):
    extra = replace(match, capabilities=match.capabilities + (
        Capability('sensor2', 'red', 'app', frozenset({'endpoint'})),))
    red = project_for_seat(extra, 'red')
    assert 'Suspicious authentication' not in json.dumps(red)


def test_evidence_is_ordered_consistently(match):
    events = match.evidence + (
        Evidence('third', 1, 'app', 'alert', 'Second anomaly',
                 frozenset({'blue'}), 'suspected', 'endpoint'),)
    selected = project_for_seat(replace(match, evidence=tuple(reversed(events))), 'blue')
    ids = [event['id'] for event in selected['assets'][0]['events']]
    assert ids == ['b', 'third']
