"""V2 clock boundaries and absent-heartbeat grace tests (no wall-clock sleeps)."""
from dataclasses import replace

import pytest

from cyber_warfare import v2_clock as clock


def test_blue_starts_at_ninety_seconds_and_private_presence_is_hidden():
    started = clock.begin(1, "blue", 1000)
    assert started.deadline_at == 1090
    projection = clock.public_clock(started, 1030)
    assert projection["seconds_remaining"] == 60
    assert projection["active_side"] == "blue"
    assert "last_seen_blue" not in projection
    assert "last_seen_red" not in projection
    assert clock.resolve_deadline(started, 1089, frozenset({"blue", "red"})) == (started, False)


def test_active_user_heartbeat_never_extends_deadline():
    started = clock.begin(1, "blue", 1000)
    seen = clock.heartbeat(started, "blue", 1033)
    assert seen.deadline_at == 1090
    assert seen.last_seen_blue == 1033
    assert clock.heartbeat(seen, "blue", 1090) == seen
    assert clock.heartbeat(seen, "blue", 1100) == seen


def test_expired_active_human_with_recent_presence_is_auto_passed():
    started = clock.begin(1, "blue", 1000)
    seen = clock.heartbeat(started, "blue", 1088)
    expired, should_pass = clock.resolve_deadline(seen, 1090, frozenset({"blue", "red"}))
    assert should_pass and expired == seen


def test_one_thirty_second_grace_only_for_verified_stale_human():
    started = clock.begin(1, "blue", 1000)
    seen = clock.heartbeat(started, "blue", 1020)
    grace, should_pass = clock.resolve_deadline(seen, 1090, frozenset({"blue", "red"}))
    assert not should_pass
    assert grace.deadline_at == 1120
    assert grace.grace_active
    assert grace.grace_used == frozenset({"blue"})
    assert clock.resolve_deadline(grace, 1119, frozenset({"blue", "red"}))[1] is False
    assert clock.resolve_deadline(grace, 1120, frozenset({"blue", "red"}))[1] is True
    red_turn = clock.next_turn(grace, 1, "red", 1120)
    red_seen = clock.heartbeat(red_turn, "red", 1130)
    red_grace, should_pass = clock.resolve_deadline(red_seen, 1210, frozenset({"blue", "red"}))
    assert not should_pass and red_grace.grace_used == frozenset({"blue", "red"})
    next_blue = clock.next_turn(red_grace, 2, "blue", 1240)
    next_blue = clock.heartbeat(next_blue, "blue", 1250)
    expired, should_pass = clock.resolve_deadline(next_blue, 1330, frozenset({"blue", "red"}))
    assert should_pass and expired.deadline_at == 1330


def test_no_prior_verified_heartbeat_means_no_grace():
    started = clock.begin(1, "red", 200)
    expired, should_pass = clock.resolve_deadline(started, 290, frozenset({"red", "blue"}))
    assert should_pass and expired.grace_used == frozenset()


def test_bot_seats_never_receive_grace():
    started = clock.heartbeat(clock.begin(1, "blue", 1000), "blue", 1001)
    expired, should_pass = clock.resolve_deadline(started, 1090, frozenset({"red"}))
    assert should_pass and expired == started


def test_large_worker_delay_consumes_grace_and_passes_in_one_transition():
    started = clock.heartbeat(clock.begin(1, "blue", 1000), "blue", 1005)
    expired, should_pass = clock.resolve_deadline(started, 1500, frozenset({"blue", "red"}))
    assert should_pass and expired.grace_used == frozenset({"blue"})
    assert expired.deadline_at == 1120


def test_invalid_clock_and_unknown_side_fail_closed():
    with pytest.raises(ValueError):
        clock.begin(1, "blue", -1)
    with pytest.raises(ValueError):
        clock.begin(31, "blue", 100)
    with pytest.raises(ValueError):
        clock.begin(1, "spectator", 100)
    with pytest.raises(ValueError):
        clock.resolve_deadline(clock.begin(1, "blue", 1000), 1090, frozenset({"intruder"}))
    with pytest.raises(ValueError):
        clock.heartbeat(clock.begin(1, "blue", 1000), "intruder", 1020)
    with pytest.raises(ValueError):
        replace(clock.begin(1, "red", 100), grace_active=True)
    with pytest.raises(ValueError):
        clock.public_clock(clock.begin(1, "blue", 100), -1)
