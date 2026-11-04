"""Simulated server clock, no sleeps, no user-provided timestamps."""
import pytest

from cyber_warfare import engine, v2_alternating, v2_timed
from cyber_warfare.scenario import list_scenarios


def beginning():
    return v2_timed.start(
        v2_alternating.new_match(list_scenarios()[0], "clock-match", "red-user", "blue-user"),
        1000,
    )


def test_blue_opens_and_moves_before_deadline():
    state = beginning()
    assert state.clock.deadline_at == 1090
    state = v2_timed.act(state, "blue-user", engine.Order("wait_blue"), "blue1", 1050)
    assert state.match.round == 1 and state.match.active_side == "red"
    assert state.clock.deadline_at == 1140
    assert state.match.version == 1
    assert len(state.match.private.timeline) == 1


def test_red_and_blue_cannot_submit_at_or_after_deadline():
    state = beginning()
    with pytest.raises(ValueError, match="Expired turn"):
        v2_timed.act(state, "blue-user", engine.Order("wait_blue"), "too-late", 1090)
    assert state.match.version == 0
    with pytest.raises(PermissionError):
        v2_timed.seat_heartbeat(state, "spectator", 1010)
    with pytest.raises(ValueError):
        v2_timed.seat_heartbeat(state, "red-user", 1010)


def test_timeout_moves_authoritatively_without_web_poll():
    state = beginning()
    after, passed = v2_timed.settle(state, 1090, frozenset({"red", "blue"}))
    assert passed
    assert after.match.active_side == "red"
    assert after.clock.deadline_at == 1180
    assert after.match.moves[0]["action"] == "wait_blue"
    assert after.match.moves[0]["command_id"] == "server-timeout-1-blue"
    same, passed = v2_timed.settle(after, 1090, frozenset({"red", "blue"}))
    assert not passed and same.match.version == after.match.version
    result, passed = v2_timed.settle(same, 1180, frozenset({"red", "blue"}))
    assert passed
    assert result.match.round == 2 and result.match.active_side == "blue"


def test_stale_heartbeat_grants_once_and_expired_grace_forces_pass():
    state = v2_timed.seat_heartbeat(beginning(), "blue-user", 1010)
    within_grace, passed = v2_timed.settle(state, 1090, frozenset({"red", "blue"}))
    assert not passed and within_grace.clock.deadline_at == 1120
    assert within_grace.clock.grace_used == frozenset({"blue"})
    within_grace, passed = v2_timed.settle(within_grace, 1110, frozenset({"red", "blue"}))
    assert not passed
    after, passed = v2_timed.settle(within_grace, 1120, frozenset({"red", "blue"}))
    assert passed and after.match.active_side == "red"
    assert after.clock.grace_used == frozenset({"blue"})
    after = v2_timed.act(after, "red-user", engine.Order("wait_red"), "r1", 1150)
    assert after.match.round == 2
    after = v2_timed.seat_heartbeat(after, "blue-user", 1170)
    assert after.clock.deadline_at == 1240
    after, passed = v2_timed.settle(after, 1240, frozenset({"red", "blue"}))
    assert passed and after.clock.grace_used == frozenset({"blue"})


def test_one_delayed_worker_check_reconciles_grace_without_waiting_again():
    state = v2_timed.seat_heartbeat(beginning(), "blue-user", 1001)
    after, passed = v2_timed.settle(state, 1500, frozenset({"red", "blue"}))
    assert passed
    assert after.match.active_side == "red"
    assert after.clock.grace_used == frozenset({"blue"})
    assert after.clock.deadline_at == 1590


def test_bot_turn_gets_no_grace_even_if_it_was_recorded():
    state = beginning()
    state = v2_timed.seat_heartbeat(state, "blue-user", 1001)
    after, passed = v2_timed.settle(state, 1090, frozenset({"red"}))
    assert passed and after.match.active_side == "red"


def test_original_edition_cannot_be_passed_to_timed_adapter():
    scenario = list_scenarios()[0]
    legacy = engine.new_match(scenario, "seed", "red-user", "blue-user")
    with pytest.raises(ValueError):
        v2_timed.start(legacy, 1000)


def test_clock_does_not_change_private_pinned_replay_until_an_action_occurs():
    state = beginning()
    original = v2_alternating.export_replay(state.match)
    after = v2_timed.seat_heartbeat(state, "blue-user", 1010)
    after, passed = v2_timed.settle(after, 1090, frozenset({"red", "blue"}))
    assert not passed
    assert v2_alternating.export_replay(after.match) == original
    after, passed = v2_timed.settle(after, 1120, frozenset({"red", "blue"}))
    assert passed
    record = v2_alternating.export_replay(after.match)
    assert v2_alternating.export_replay(v2_alternating.replay(record)) == record


def test_private_timed_snapshot_round_trip_after_reconnect():
    import json
    state = beginning()
    state = v2_timed.seat_heartbeat(state, "blue-user", 1010)
    state, passed = v2_timed.settle(state, 1090, frozenset({"red", "blue"}))
    assert not passed
    record = json.loads(json.dumps(v2_timed.export_snapshot(state)))
    restored = v2_timed.restore_snapshot(record)
    assert v2_timed.export_snapshot(restored) == record
    assert restored.clock.deadline_at == 1120
    assert restored.clock.grace_used == frozenset({"blue"})
    restored, passed = v2_timed.settle(restored, 1120, frozenset({"red", "blue"}))
    assert passed and restored.match.active_side == "red"


def test_reject_forged_timed_record_and_legacy_transcript():
    from copy import deepcopy
    record = v2_timed.export_snapshot(beginning())
    cases = []
    changed = deepcopy(record)
    changed["edition"] = "legacy"
    cases.append(changed)
    changed = deepcopy(record)
    changed["game"]["edition"] = "legacy"
    cases.append(changed)
    changed = deepcopy(record)
    changed["clock"]["active_side"] = "red"
    cases.append(changed)
    changed = deepcopy(record)
    changed["clock"]["deadline_at"] = -1
    cases.append(changed)
    changed = deepcopy(record)
    changed["clock"]["grace_used"] = ["blue", "blue"]
    cases.append(changed)
    changed = deepcopy(record)
    changed["clock"]["grace_used"] = [["blue"]]
    cases.append(changed)
    changed = deepcopy(record)
    changed["clock"]["grace_active"] = True
    cases.append(changed)
    changed = deepcopy(record)
    changed["private_seed"] = "forged"
    cases.append(changed)
    for forged in cases:
        with pytest.raises(ValueError):
            v2_timed.restore_snapshot(forged)
