"""Pure V2 event simulations: not yet an authenticated multiplayer test."""
from dataclasses import replace

from cyber_warfare.v2_events import ResolvedOutcome, apply_outcome
from cyber_warfare.v2_scenario import scenario_initial_v2
from cyber_warfare.scenario import list_scenarios
from cyber_warfare.v2_state import project_for_seat


def start():
    scenario = list_scenarios()[0]
    return scenario_initial_v2(scenario)


def test_two_seat_visibility_after_monitored_compromise():
    # Use a synthetic asset from one real scenario, independently of scenario story.
    state = start()
    target = state.assets[0].id
    state = apply_outcome(state, ResolvedOutcome("blue_monitor", target, True))
    state = apply_outcome(state, ResolvedOutcome("red_compromise", target, True, True))
    blue = project_for_seat(state, "blue")
    red = project_for_seat(state, "red")
    blue_asset = next(a for a in blue["assets"] if a["id"] == target)
    assert any(e["kind"] == "alert" and e["certainty"] == "suspected"
               for e in blue_asset["events"])
    assert not any(e["kind"] == "access" for e in blue_asset["events"])
    assert "access" not in blue_asset
    red_asset = next(a for a in red["assets"] if a["id"] == target)
    assert red_asset["access"] == 1
    assert red_asset["knowledge"] == "confirmed"
    assert not any(e["kind"] == "alert" for e in red_asset["events"])


def test_unmonitored_detection_does_not_appear_retroactively():
    state = start()
    target = state.assets[0].id
    # Remove initial sensors so detection without monitoring is not published.
    state = replace(state, capabilities=())
    state = apply_outcome(state, ResolvedOutcome("red_compromise", target, True, True))
    assert not any(e.kind == "alert" for e in state.evidence)
    state = apply_outcome(state, ResolvedOutcome("blue_monitor", target, True))
    assert not any(e.kind == "alert" for e in state.evidence)


def test_blue_containment_marks_red_access_as_stale():
    state = start()
    target = state.assets[0].id
    state = apply_outcome(state, ResolvedOutcome("red_compromise", target, True))
    state = apply_outcome(state, ResolvedOutcome("blue_contain", target, True))
    blue = next(a for a in project_for_seat(state, "blue")["assets"] if a["id"] == target)
    red = next(a for a in project_for_seat(state, "red")["assets"] if a["id"] == target)
    assert blue["available"] is False
    assert red["knowledge"] == "stale"
    assert "controls" not in red


def test_investigation_reveals_finding_not_red_plan():
    state = start()
    target = state.assets[0].id
    state = apply_outcome(state, ResolvedOutcome("red_compromise", target, True))
    state = apply_outcome(state, ResolvedOutcome("blue_investigate", target, True))
    blue = next(a for a in project_for_seat(state, "blue")["assets"] if a["id"] == target)
    assert any(e["kind"] == "finding" for e in blue["events"])
    assert not any(e["kind"] == "access" for e in blue["events"])


def test_all_six_scenarios_accept_deterministic_transitions():
    for scenario in list_scenarios():
        state = scenario_initial_v2(scenario)
        target = state.assets[0].id
        initial = state
        state = apply_outcome(state, ResolvedOutcome("blue_monitor", target, True))
        state = apply_outcome(state, ResolvedOutcome("red_compromise", target, True, True))
        assert initial.assets[0].red_access == scenario.assets[0].initial_access
        assert len(project_for_seat(state, "blue")["assets"]) == len(scenario.assets)
        assert any(a["id"] == target for a in project_for_seat(state, "red")["assets"])
