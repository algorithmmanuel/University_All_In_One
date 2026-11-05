"""V3 wall-clock and per-turn planning policy (pure, additive pilot contract).

No V1/V2 game or live route uses this yet. This module models one shared,
immutable engagement deadline and a capped deadline for each alternating move.
The durable adapter will own authenticated actions, persistence, pass events,
scoring and worker scheduling. All timestamps are trusted integer UTC seconds.
"""
from dataclasses import dataclass, replace

MATCH_MINUTES = frozenset((15, 30, 60, 120))
TURN_SECONDS = frozenset((30, 60, 90, 180, 300))
DEFAULT_MATCH_MINUTES = 30
DEFAULT_TURN_SECONDS = 90
SIDES = frozenset(("red", "blue"))


@dataclass(frozen=True)
class Config:
    match_minutes: int = DEFAULT_MATCH_MINUTES
    turn_seconds: int = DEFAULT_TURN_SECONDS

    def __post_init__(self):
        if (type(self.match_minutes) is not int
                or self.match_minutes not in MATCH_MINUTES
                or type(self.turn_seconds) is not int
                or self.turn_seconds not in TURN_SECONDS):
            raise ValueError("Unsupported V3 match clock configuration")


@dataclass(frozen=True)
class Clock:
    config: Config
    started_at: int
    match_deadline_at: int
    turn_started_at: int
    turn_deadline_at: int
    active_side: str
    turn_sequence: int

    def __post_init__(self):
        if (not isinstance(self.config, Config)
                or any(type(x) is not int or x < 0 for x in (
                    self.started_at, self.match_deadline_at,
                    self.turn_started_at, self.turn_deadline_at,
                    self.turn_sequence))
                or self.active_side not in SIDES
                or self.turn_sequence < 1
                or self.match_deadline_at != self.started_at + self.config.match_minutes * 60
                or not self.started_at <= self.turn_started_at < self.match_deadline_at
                or self.turn_deadline_at != min(
                    self.turn_started_at + self.config.turn_seconds,
                    self.match_deadline_at,
                )):
            raise ValueError("Invalid V3 server clock")


def begin(config: Config, server_now: int, first_side: str = "blue") -> Clock:
    if type(server_now) is not int or server_now < 0 or first_side not in SIDES:
        raise ValueError("Invalid V3 clock start")
    deadline = server_now + config.match_minutes * 60
    return Clock(config, server_now, deadline, server_now,
                 min(server_now + config.turn_seconds, deadline),
                 first_side, 1)


def status(clock: Clock, server_now: int) -> str:
    """Game expiry wins precedence over a turn expiry at identical seconds."""
    if type(server_now) is not int or server_now < clock.turn_started_at:
        raise ValueError("Invalid authoritative server time")
    if server_now >= clock.match_deadline_at:
        return "match_expired"
    if server_now >= clock.turn_deadline_at:
        return "turn_expired"
    return "active"


def next_turn(clock: Clock, server_now: int) -> Clock:
    """Advance after one resolved action/pass; never restart the game clock."""
    if status(clock, server_now) == "match_expired":
        raise ValueError("Overall match has expired")
    side = "red" if clock.active_side == "blue" else "blue"
    return replace(
        clock, active_side=side, turn_sequence=clock.turn_sequence + 1,
        turn_started_at=server_now,
        turn_deadline_at=min(server_now + clock.config.turn_seconds,
                             clock.match_deadline_at),
    )


def remaining(clock: Clock, server_now: int) -> dict:
    state = status(clock, server_now)
    return {
        "state": state, "active_side": clock.active_side,
        "turn_sequence": clock.turn_sequence,
        "match_deadline_at": clock.match_deadline_at,
        "turn_deadline_at": clock.turn_deadline_at,
        "match_seconds_remaining": max(0, clock.match_deadline_at - server_now),
        "turn_seconds_remaining": max(0, clock.turn_deadline_at - server_now),
    }
