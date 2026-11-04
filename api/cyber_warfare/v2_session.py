"""Explicit version dispatch for Red/Blue match persistence and seat projections.

Only call with a match loaded under authenticated ownership. This module is a
pure application adapter, NOT an HTTP route or a replacement for DB row locks.
The old sealed-round envelope remains unmodified and independently replayable.
"""
from copy import deepcopy

from . import engine, v2_alternating, v2_timed, v2_clock
from .opponent import choose_order


def is_alternating(record):
    """Recognise only the new tagged replay; reject malformed unknown tags."""
    if not isinstance(record, dict):
        raise ValueError("Invalid Red/Blue transcript")
    if "edition" in record:
        if record["edition"] == v2_timed.TIMED_EDITION:
            return True
        if record["edition"] != v2_alternating.EDITION:
            raise ValueError("Unsupported Red/Blue edition")
        return True
    return False


def restore(record):
    if is_alternating(record) and record["edition"] == v2_timed.TIMED_EDITION:
        return v2_timed.restore_snapshot(record)
    return v2_alternating.replay(record) if is_alternating(record) else engine.replay(record)


def export(match):
    if isinstance(match, v2_timed.TimedMatch):
        return v2_timed.export_snapshot(match)
    return (v2_alternating.export_replay(match)
            if isinstance(match, v2_alternating.AlternateMatch)
            else engine.export_replay(match))


def seats(match):
    if isinstance(match, v2_timed.TimedMatch):
        return match.match.private.seats
    return match.private.seats if isinstance(match, v2_alternating.AlternateMatch) else match.seats


def view(match, player, server_now=None):
    if isinstance(match, v2_timed.TimedMatch):
        if server_now is None:
            raise ValueError("Authoritative server time required")
        observation = v2_alternating.view(match.match, player)
        observation["clock"] = v2_clock.public_clock(match.clock, server_now)
        observation["engine_version"] = v2_timed.TIMED_EDITION
        return observation
    return (v2_alternating.view(match, player)
            if isinstance(match, v2_alternating.AlternateMatch)
            else engine.view(match, player))


def orders(match, player, server_now=None):
    observation = view(match, player, server_now=server_now)
    if (isinstance(match, v2_timed.TimedMatch)
            and server_now >= match.clock.deadline_at):
        return []
    return engine.available_orders(observation)


def join(match, side, actor):
    """Returns a fresh match with a bound previously open seat, not persisted."""
    result = deepcopy(match)
    if isinstance(result, v2_timed.TimedMatch):
        raise ValueError("Timed match must start its clock after final human joins")
    owners = seats(result)
    if side not in engine.SIDES or owners[side] != "open" or actor in owners.values():
        raise ValueError("Seat cannot be joined")
    owners[side] = actor
    return result


def advance_computer(match, difficulty):
    """Resolve the computer's current alternating action from its own projection.

    Call from the transaction holding the match row lock, before returning to
    a human or immediately after one human action. No browser/poll dependency.
    """
    if not isinstance(match, v2_alternating.AlternateMatch):
        raise ValueError("This helper requires the V2 alternating edition")
    result = match
    if result.winner or seats(result)[result.active_side] != "computer":
        return result
    observation = view(result, "computer")
    action = choose_order(observation, difficulty)
    return v2_alternating.commit(
        result, "computer", action, result.round,
        f"computer-{result.round}-{result.active_side}",
    )


def submit_alternating(match, player, order, expected_round, command_id, difficulty):
    """One player move, then at most one immediate opponent computer move."""
    if not isinstance(match, v2_alternating.AlternateMatch):
        raise ValueError("Expected V2 alternating match")
    result = v2_alternating.commit(match, player, order, expected_round, command_id)
    return advance_computer(result, difficulty)


def debrief(match, player):
    """Compatible completed-match summary; V2 counterfactuals are not yet built."""
    if isinstance(match, v2_timed.TimedMatch):
        raise ValueError("Match is still active")
    if not isinstance(match, v2_alternating.AlternateMatch):
        return engine.debrief(match, player)
    engine._side(match.private, player)
    if not match.winner:
        raise ValueError("Debrief only available after match finishes")
    timeline = [
        {key: deepcopy(event[key]) for key in (
            "turn", "side", "action", "target", "source",
            "success", "detected", "framework",
        )}
        for event in match.private.timeline
    ]
    return {
        "winner": match.winner,
        "objective": match.private.scenario.objective.model_dump(mode="json"),
        "timeline": timeline, "missed": [], "alternatives": [],
        "explanation": (
            "The complete action history is available after the match. "
            "V2 measured counterfactual alternatives remain under development."
        ),
    }
