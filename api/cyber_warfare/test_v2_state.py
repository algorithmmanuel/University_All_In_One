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
