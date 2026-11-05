"""Alternating V2 deterministic domain and legacy compatibility checks."""
from copy import deepcopy
import json
import pytest

from cyber_warfare import engine, v2_alternating as alt
from cyber_warfare.scenario import list_scenarios


def start(scenario=None):
    scenario = scenario or list_scenarios()[0]
    return alt.new_match(scenario, "fixed-v2-seed", "red-human", "blue-human")


def wait(side):
    return engine.Order("wait_" + side)


def test_blue_opens_and_red_cannot_take_first_action():
    match = start()
    assert match.active_side == "blue"
    assert alt.view(match, "red-human")["committed"] is True
    assert not alt.available_orders(match, "red-human")
    assert wait("blue") in alt.available_orders(match, "blue-human")
    with pytest.raises(ValueError):
        alt.commit(match, "red-human", wait("red"), 1, "red-first")


def test_blue_effect_resolves_before_red_and_opponent_stays_private():
    match = start()
    blue = alt.view(match, "blue-human")
    target = blue["assets"][0]["id"]
    action = engine.Order("monitor", target)
    match = alt.commit(match, "blue-human", action, 1, "blue-first")
    assert match.active_side == "red"
    assert match.round == 1
    assert match.version == 1
    assert "monitoring" in match.private.assets[target]["controls"]
    assert len(match.private.timeline) == 1
    assert len(match.private.history) == 0
    red = alt.view(match, "red-human")
    assert red["committed_order"] is None
    assert "plans" not in red and "seed" not in red and "timeline" not in red
    assert not any("monitoring" in str(a) for a in red["assets"]
                   if a["id"] == target and not a.get("assessed"))
    match = alt.commit(match, "red-human", wait("red"), 1, "red-first")
    assert match.round == 2 and match.version == 2
    assert match.active_side == "blue"
    assert len(match.private.history) == 1
    assert len(match.private.timeline) == 2



def test_monitoring_changes_alert_visibility_without_revealing_red_success():
    """Same seed and attack: monitoring changes alerts, not hidden outcomes."""
    scenario = next(s for s in list_scenarios() if s.id == "microfinance")
    attack = engine.Order("phish", "teller")
    for index in range(200):
        seed = f"monitor-visibility-{index}"
        ordinary = alt.new_match(scenario, seed, "red-human", "blue-human")
        monitored = alt.new_match(scenario, seed, "red-human", "blue-human")
        ordinary = alt.commit(ordinary, "blue-human", wait("blue"), 1, "blue-wait")
        monitored = alt.commit(monitored, "blue-human",
                               engine.Order("monitor", "teller"), 1, "blue-monitor")
        red_ordinary = alt.view(ordinary, "red-human")
        red_monitored = alt.view(monitored, "red-human")
        assert red_ordinary["assets"] == red_monitored["assets"]
        assert red_ordinary["observations"] == red_monitored["observations"]
        assert "monitoring" in next(a for a in alt.view(monitored, "blue-human")["assets"]
                                    if a["id"] == "teller")["controls"]
        assert attack in alt.available_orders(ordinary, "red-human")
        assert attack in alt.available_orders(monitored, "red-human")

        ordinary = alt.commit(ordinary, "red-human", attack, 1, "red-phish")
        monitored = alt.commit(monitored, "red-human", attack, 1, "red-phish")
        plain_event = ordinary.private.timeline[-1]
        tool_event = monitored.private.timeline[-1]
        assert plain_event["success"] == tool_event["success"]
        assert ordinary.private.assets["teller"]["access"] == monitored.private.assets["teller"]["access"]
        if plain_event["detected"] or not tool_event["detected"]:
            continue
        blue_plain = alt.view(ordinary, "blue-human")
        blue_tools = alt.view(monitored, "blue-human")
        assert not any(e["type"] == "alert" for e in blue_plain["observations"])
        alerts = [e for e in blue_tools["observations"] if e["type"] == "alert"]
        assert len(alerts) == 1 and alerts[0]["target"] == "teller"
        assert "action" not in alerts[0] and "success" not in alerts[0]
        assert "phish" not in alerts[0]["message"].lower()
        assert "access" not in next(a for a in blue_tools["assets"] if a["id"] == "teller")
        red_tools = alt.view(monitored, "red-human")
        assert not any(e["type"] == "alert" for e in red_tools["observations"])
        assert all(e["type"] == "own_action" for e in red_tools["observations"])
        for projection in (blue_plain, blue_tools, red_tools):
            assert not {"seed", "timeline", "plans", "seats"} & projection.keys()
        restored = alt.replay(json.loads(json.dumps(alt.export_replay(monitored))))
        assert alt.view(restored, "blue-human") == blue_tools
        assert alt.view(restored, "red-human") == red_tools
        break
    else:
        pytest.fail("No deterministic seed demonstrated the monitoring alert delta")



def test_live_isolation_changes_blue_truth_but_red_sees_only_failed_followup():
    """Alternating seats react to state while Red retains stale beliefs.

    Blue containment happens immediately and changes authoritative access.
    It must not silently reveal Blue's control action to Red; the Red follow-up
    learns only the outcome of its own attempted privilege escalation.
    """
    scenario = next(s for s in list_scenarios() if s.id == "microfinance")
    for index in range(160):
        opening = alt.new_match(scenario, f"stale-access-{index}",
                                "red-human", "blue-human")
        opening = alt.commit(opening, "blue-human", engine.Order("wait_blue"),
                             1, "blue-wait")
        opening = alt.commit(opening, "red-human",
                             engine.Order("phish", "teller"), 1, "red-phish")
        if not opening.private.timeline[-1]["success"]:
            continue
        red_before = alt.view(opening, "red-human")
        blue_before = alt.view(opening, "blue-human")
        assert next(asset for asset in red_before["assets"]
                    if asset["id"] == "teller")["access"] == 1

        isolated = alt.commit(opening, "blue-human",
                              engine.Order("contain", "teller"), 2, "blue-contain")
        assert isolated.private.assets["teller"]["isolated"] is True
        assert isolated.private.assets["teller"]["access"] == 0
        blue_after = alt.view(isolated, "blue-human")
        assert next(asset for asset in blue_after["assets"]
                    if asset["id"] == "teller")["isolated"] is True
        assert next(asset for asset in blue_before["assets"]
                    if asset["id"] == "teller")["isolated"] is False

        red_after = alt.view(isolated, "red-human")
        assert red_after["assets"] == red_before["assets"]
        assert red_after["observations"] == red_before["observations"]
        assert not any("contain" in str(event).lower()
                       for event in red_after["observations"])
        assert engine.Order("escalate", "teller") in alt.available_orders(
            isolated, "red-human")

        resolved = alt.commit(isolated, "red-human",
                              engine.Order("escalate", "teller"), 2, "red-escalate")
        assert resolved.private.timeline[-1]["feasible"] is False
        assert resolved.private.timeline[-1]["success"] is False
        red_result = alt.view(resolved, "red-human")
        assert next(asset for asset in red_result["assets"]
                    if asset["id"] == "teller")["access"] == 0
        assert red_result["observations"][-1]["type"] == "own_action"
        assert "conditions may have changed" in red_result["observations"][-1]["message"]
        assert not any(event["type"] == "alert" for event in
                       alt.view(resolved, "blue-human")["observations"])
        for projection in (blue_after, red_after, red_result):
            assert not {"seed", "timeline", "plans", "seats"} & projection.keys()
        restored = alt.replay(json.loads(json.dumps(alt.export_replay(resolved))))
        assert alt.view(restored, "red-human") == red_result
        assert alt.view(restored, "blue-human") == alt.view(resolved, "blue-human")
        break
    else:
        pytest.fail("Could not find deterministic successful entry fixture")


def test_exact_uuid_retry_does_not_double_charge_or_resolve():
    first = start()
    first = alt.commit(first, "blue-human", wait("blue"), 1, "uuid-1")
    retry = alt.commit(first, "blue-human", wait("blue"), 1, "uuid-1")
    assert alt.export_replay(retry) == alt.export_replay(first)
    assert retry.version == first.version
    with pytest.raises(ValueError):
        alt.commit(first, "blue-human", engine.Order("monitor", first.private.scenario.assets[0].id), 1, "uuid-1")
    with pytest.raises(ValueError):
        alt.commit(first, "blue-human", wait("blue"), 1, "uuid-new")


def test_v2_replay_is_byte_equivalent_under_restore():
    match = start()
    match = alt.commit(match, "blue-human", wait("blue"), 1, "blue1")
    match = alt.commit(match, "red-human", wait("red"), 1, "red1")
    match = alt.commit(match, "blue-human", wait("blue"), 2, "blue2")
    record = json.loads(json.dumps(alt.export_replay(match)))
    restored = alt.replay(record)
    assert alt.export_replay(restored) == record
    assert alt.view(restored, "red-human") == alt.view(match, "red-human")
    assert alt.view(restored, "blue-human") == alt.view(match, "blue-human")


def test_forged_v2_replay_fails_closed():
    match = alt.commit(start(), "blue-human", wait("blue"), 1, "blue1")
    record = alt.export_replay(match)
    forged = deepcopy(record)
    forged["moves"][0]["side"] = "red"
    with pytest.raises(ValueError):
        alt.replay(forged)
    forged = deepcopy(record)
    forged["scenario_digest"] = "invalid"
    with pytest.raises(ValueError):
        alt.replay(forged)
    forged = deepcopy(record)
    forged["edition"] = "red-blue-legacy"
    with pytest.raises(ValueError):
        alt.replay(forged)


def test_all_six_scenarios_alternate_to_victory_and_replay():
    scenarios = list_scenarios()
    assert len(scenarios) == 6
    for scenario in scenarios:
        match = start(scenario)
        for round_number in range(1, scenario.turn_limit + 1):
            assert match.active_side == "blue"
            match = alt.commit(match, "blue-human", wait("blue"), round_number,
                               f"blue-{round_number}")
            assert match.active_side == "red"
            match = alt.commit(match, "red-human", wait("red"), round_number,
                               f"red-{round_number}")
            if match.winner:
                break
        assert match.winner == "blue"
        restored = alt.replay(json.loads(json.dumps(alt.export_replay(match))))
        assert restored.winner == match.winner


def test_legacy_engine_rounds_still_use_sealed_orders_and_old_replay():
    scenario = list_scenarios()[0]
    match = engine.new_match(scenario, "legacy-seed", "red-human", "blue-human")
    mid = engine.commit(match, "blue-human", wait("blue"), 1, "legacy-blue")
    assert mid.turn == 1 and not mid.timeline
    final = engine.commit(mid, "red-human", wait("red"), 1, "legacy-red")
    assert final.turn == 2
    saved = engine.export_replay(final)
    assert "edition" not in saved
    assert engine.export_replay(engine.replay(saved)) == saved
    with pytest.raises(ValueError):
        alt.replay(saved)


def test_outsiders_do_not_get_an_observation():
    with pytest.raises(PermissionError):
        alt.view(start(), "spectator")
