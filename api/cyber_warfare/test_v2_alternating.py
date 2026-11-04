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
