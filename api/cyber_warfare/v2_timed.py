"""Pure, server-clock-governed V2 moves and automatic timeout passes.

NOT an HTTP endpoint, persistent scheduler or finished production clock.
Call only from a trusted, transactionally locked worker that supplies the
server time and the authenticated seat. The existing Beta engine is untouched.
"""
from dataclasses import dataclass

from . import engine, v2_alternating as alternate
from . import v2_clock as clock


@dataclass(frozen=True)
class TimedMatch:
    match: alternate.AlternateMatch
    clock: clock.TurnClock

    def __post_init__(self):
        if (not isinstance(self.match, alternate.AlternateMatch)
                or self.match.winner
                or self.match.active_side != self.clock.active_side
                or self.match.round != self.clock.round):
            raise ValueError("Timed match and clock disagree")


def start(match: alternate.AlternateMatch, server_now: int):
    """Start a 90-second deadline on the current, non-finished actor."""
    if not isinstance(match, alternate.AlternateMatch) or match.winner:
        raise ValueError("Active V2 match required")
    return TimedMatch(match, clock.begin(match.round, match.active_side, server_now))


def seat_heartbeat(state: TimedMatch, player: str, server_now: int):
    """Requires the caller to be authenticated by a future API/DB adapter."""
    side = engine._side(state.match.private, player)
    if side != state.clock.active_side:
        raise ValueError("Cannot heartbeat an opponent's turn")
    return TimedMatch(state.match, clock.heartbeat(state.clock, side, server_now))


def act(state: TimedMatch, player: str, order: engine.Order, command_id: str,
        server_now: int) -> TimedMatch:
    """Reject late actions; caller must first settle elapsed deadlines."""
    if type(server_now) is not int or server_now < 0:
        raise ValueError("Invalid trusted server time")
    if server_now >= state.clock.deadline_at:
        raise ValueError("Expired turn: server must settle deadline first")
    updated = alternate.commit(state.match, player, order, state.match.round, command_id)
    if updated.winner:
        # Terminal result has no next clock. The caller persists its normal
        # edition-tagged replay and finished status separately.
        return updated
    return TimedMatch(
        updated,
        clock.next_turn(state.clock, updated.round, updated.active_side, server_now),
    )


def settle(state: TimedMatch, server_now: int, human_seats: frozenset[str]):
    """One locked, idempotent expiry step, independent of browser polling.

    Return (TimedMatch | terminal AlternateMatch, action_was_passed). A missing
    heartbeat can justify one grace only when an earlier server heartbeat was
    recorded; client-supplied 'disconnected' flags are never considered.
    """
    new_clock, should_pass = clock.resolve_deadline(
        state.clock, server_now, human_seats)
    if not should_pass:
        return TimedMatch(state.match, new_clock), False
    actor = state.match.private.seats[state.clock.active_side]
    action = engine.Order("wait_" + state.clock.active_side)
    result = alternate.commit(
        state.match, actor, action, state.match.round,
        f"server-timeout-{state.match.round}-{state.clock.active_side}")
    if result.winner:
        return result, True
    return TimedMatch(
        result, clock.next_turn(new_clock, result.round, result.active_side, server_now)
    ), True
