"""Standalone V3 clock contract; does not change the existing V2 match."""
from dataclasses import replace

import pytest
from cyber_warfare import v3_clock as clock


def test_defaults_are_30_minute_match_and_90_second_turn():
    c = clock.begin(clock.Config(), 1000)
    assert c.match_deadline_at == 2800
    assert c.turn_deadline_at == 1090
    assert c.active_side == "blue" and c.turn_sequence == 1


@pytest.mark.parametrize("minutes", [15, 30, 60, 120])
@pytest.mark.parametrize("seconds", [30, 60, 90, 180, 300])
def test_all_presets_and_deadline_caps(minutes, seconds):
    c = clock.begin(clock.Config(minutes, seconds), 500)
    assert c.match_deadline_at == 500 + minutes * 60
    assert c.turn_deadline_at == min(500 + seconds, c.match_deadline_at)
    assert clock.remaining(c, 500)["match_seconds_remaining"] == minutes * 60


@pytest.mark.parametrize("args", [(0, 90), (12, 90), (30, 91), (120, -30),
                                   (True, 90), (30, 90.0), (120, 600)])
def test_reject_unsupported_or_ambiguous_config(args):
    with pytest.raises(ValueError):
        clock.Config(*args)


def test_fast_moves_can_exceed_legacy_fixed_round_limit():
    c = clock.begin(clock.Config(30, 90), 1000)
    for n in range(100):
        c = clock.next_turn(c, 1001 + n)
    assert c.turn_sequence == 101
    assert c.active_side == "blue"
    assert c.match_deadline_at == 2800


def test_independent_turn_deadline_and_immutable_match_deadline():
    c = clock.begin(clock.Config(), 1000)
    c = clock.next_turn(c, 1040)
    assert (c.turn_deadline_at, c.match_deadline_at) == (1130, 2800)
    late = clock.next_turn(c, 2790)
    assert late.turn_deadline_at == 2800
    assert late.match_deadline_at == 2800
    assert clock.remaining(late, 2791)["turn_seconds_remaining"] == 9


def test_overall_expiry_precedes_turn_timeout_and_no_extra_turn():
    c = clock.begin(clock.Config(15, 300), 2000)
    c = clock.next_turn(c, 2890)
    assert c.turn_deadline_at == c.match_deadline_at == 2900
    assert clock.status(c, 2900) == "match_expired"
    with pytest.raises(ValueError, match="Overall match"):
        clock.next_turn(c, 2900)


def test_expired_turn_is_reported_without_mutating_clock():
    c = clock.begin(clock.Config(), 1000)
    assert clock.status(c, 1090) == "turn_expired"
    assert clock.remaining(c, 1090)["turn_seconds_remaining"] == 0
    assert clock.remaining(c, 1090)["match_seconds_remaining"] == 1710
    assert c.turn_sequence == 1


def test_clock_rejects_tampered_timestamp_and_invalid_server_inputs():
    c = clock.begin(clock.Config(), 1000)
    with pytest.raises(ValueError):
        clock.begin(clock.Config(), True)
    with pytest.raises(ValueError):
        clock.status(c, 999)
    with pytest.raises(ValueError):
        replace(c, turn_deadline_at=2000)
    with pytest.raises(ValueError):
        replace(c, match_deadline_at=2900)
