"""Server-authoritative 90-second V2 turn clock and bounded liveness grace.

Pure, deterministic state transitions; this module does NOT run a scheduler,
trust browser time, or infer actual transport disconnection. A future
transactional worker must persist and advance the clock independent of polls.
"""
from dataclasses import dataclass, replace

TURN_SECONDS = 90
GRACE_SECONDS = 30
PRESENCE_STALE_SECONDS = 15
SIDES = frozenset(("red", "blue"))
MAX_ROUNDS = 30


@dataclass(frozen=True)
class TurnClock:
    round: int
    active_side: str
    deadline_at: int
    last_seen_red: int | None
    last_seen_blue: int | None
    grace_used: frozenset[str] = frozenset()
    grace_active: bool = False

    def __post_init__(self):
        if (type(self.round) is not int or not 1 <= self.round <= MAX_ROUNDS
                or self.active_side not in SIDES
                or type(self.deadline_at) is not int or self.deadline_at < 0
                or not isinstance(self.grace_used, frozenset)
                or not self.grace_used <= SIDES
                or type(self.grace_active) is not bool):
            raise ValueError("Invalid V2 clock")
        if (self.grace_active and self.active_side not in self.grace_used):
            raise ValueError("Active grace must be consumed")
        for seen in (self.last_seen_red, self.last_seen_blue):
            if seen is not None and (type(seen) is not int or seen < 0 or seen > self.deadline_at):
                raise ValueError("Invalid seat liveness timestamp")


def begin(round_no: int, side: str, server_now: int,
          used: frozenset[str] = frozenset()) -> TurnClock:
    """Only trusted server logic supplies the time; never accept user timestamps."""
    if type(server_now) is not int or server_now < 0:
        raise ValueError("Invalid server time")
    return TurnClock(round_no, side, server_now + TURN_SECONDS, None, None, used)


def heartbeat(clock: TurnClock, side: str, server_now: int) -> TurnClock:
    """Record a successful, authenticated, active-seat check-in.

    A heartbeat after expiry cannot revive a completed turn, and a request
    never extends the deadline. The adapter verifies seat auth first.
    """
    if side != clock.active_side or type(server_now) is not int or server_now < 0:
        raise ValueError("Invalid active-seat heartbeat")
    if server_now >= clock.deadline_at:
        return clock
    if side == "red":
        return replace(clock, last_seen_red=server_now)
    return replace(clock, last_seen_blue=server_now)


def resolve_deadline(clock: TurnClock, server_now: int,
                     human_seats: frozenset[str]) -> tuple[TurnClock, bool]:
    """Apply one possible grace or request an automatic pass.

    Grace requires a human seat with previously verified heartbeat, and a
    missing heartbeat for at least PRESENCE_STALE_SECONDS at deadline.
    Merely failing to submit an action, or claiming disconnection in a request,
    is never enough. Returns (updated clock, must_auto_pass).
    """
    if (type(server_now) is not int or server_now < 0
            or not isinstance(human_seats, frozenset)
            or not human_seats <= SIDES):
        raise ValueError("Invalid server deadline evaluation")
    if server_now < clock.deadline_at:
        return clock, False
    seen = clock.last_seen_red if clock.active_side == "red" else clock.last_seen_blue
    eligible = (
        not clock.grace_active
        and clock.active_side in human_seats
        and clock.active_side not in clock.grace_used
        and seen is not None
        and clock.deadline_at - seen >= PRESENCE_STALE_SECONDS
    )
    if eligible:
        extended = replace(
            clock, deadline_at=clock.deadline_at + GRACE_SECONDS,
            grace_used=clock.grace_used | {clock.active_side},
            grace_active=True,
        )
        if server_now < extended.deadline_at:
            return extended, False
        return extended, True
    return clock, True


def next_turn(clock: TurnClock, round_no: int, side: str,
              server_now: int) -> TurnClock:
    """Start the next action deadline, carrying each seat's once-only budget."""
    return begin(round_no, side, server_now, clock.grace_used)


def public_clock(clock: TurnClock, server_now: int):
    """No seat presence or other private telemetry is exposed."""
    if type(server_now) is not int or server_now < 0:
        raise ValueError("Invalid server time")
    return {
        "round": clock.round,
        "active_side": clock.active_side,
        "deadline_at": clock.deadline_at,
        "seconds_remaining": max(0, clock.deadline_at - server_now),
        "grace_active": clock.grace_active,
    }
