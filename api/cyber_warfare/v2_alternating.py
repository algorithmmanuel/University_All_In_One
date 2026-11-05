"""Versioned, deterministic alternating Red/Blue domain engine.

This is an isolated V2 edition. It does NOT replace the existing sealed-order
engine, authenticated routes, PostgreSQL model or replay. Only a future
authenticated and transactionally locked adapter may accept live commands.
"""
from copy import deepcopy
from dataclasses import dataclass, field

from . import engine
from .catalog import ACTIONS, catalog_digest
from .scenario import Scenario, parse_scenario

EDITION = "red-blue-alternating-v2-1"
MAX_COMMAND_ID = 80


@dataclass
class AlternateMatch:
    private: engine.Match
    active_side: str = "blue"
    version: int = 0
    receipts: dict = field(default_factory=dict)
    moves: list = field(default_factory=list)
    edition: str = EDITION
    rules_digest: str = field(default_factory=catalog_digest)

    @property
    def winner(self):
        return self.private.winner

    @property
    def round(self):
        return self.private.turn


def new_match(scenario: Scenario, seed: str, red_player: str, blue_player: str):
    return AlternateMatch(engine.new_match(scenario, seed, red_player, blue_player))


def view(match: AlternateMatch, player: str):
    """Strictly project the seat's existing bounded knowledge, not private truth."""
    side = engine._side(match.private, player)
    observation = engine.view(match.private, player)
    observation.update({
        "engine_version": EDITION,
        "active_side": match.active_side if not match.winner else None,
        "round": match.round,
        "version": match.version,
        "committed": bool(not match.winner and side != match.active_side),
        "committed_order": None,
    })
    # Never show a prior Blue move as a still-sealed pending order.
    return observation


def available_orders(match: AlternateMatch, player: str):
    if match.winner:
        return []
    return engine.available_orders(view(match, player))


def commit(match: AlternateMatch, player: str, order: engine.Order,
           expected_round: int, command_id: str):
    """Resolve *one* authorised move immediately, returning a new match.

    The next actor observes the resulting private network projection. The
    original engine's resolution probabilities and effects are reused, but its
    simultaneous sealed commit/replay format is not mutated.
    """
    if not isinstance(match, AlternateMatch) or match.edition != EDITION:
        raise ValueError("Unsupported alternating match")
    if match.rules_digest != catalog_digest():
        raise ValueError("Unsupported rules digest")
    side = engine._side(match.private, player)
    if (not isinstance(order, engine.Order) or type(expected_round) is not int
            or not isinstance(command_id, str) or not 1 <= len(command_id) <= MAX_COMMAND_ID):
        raise ValueError("Invalid command")
    fingerprint = (expected_round, order.action, order.target, order.source)
    receipt_key = side + ":" + command_id
    if receipt_key in match.receipts:
        if tuple(match.receipts[receipt_key]) != fingerprint:
            raise ValueError("Command identifier reused for a different move")
        return deepcopy(match)
    if match.winner or expected_round != match.round or side != match.active_side:
        raise ValueError("Inactive, stale or finished turn")
    if order not in available_orders(match, player):
        raise ValueError("Order not available to this seat")
    result = deepcopy(match)
    core = result.private
    if side == "blue":
        core.plans["blue"] = order
        engine._resolve_action(core, "blue", order)
        result.active_side = "red"
    else:
        # Blue's resolved plan is kept internally until this round closes.
        # The legacy effect/timeline helper needs it for counterfactual context.
        if "blue" not in core.plans:
            raise ValueError("Missing Blue opening action")
        core.plans["red"] = order
        engine._resolve_action(core, "red", order)
        engine._finish_round(core)
        result.active_side = "blue"
    result.receipts[receipt_key] = list(fingerprint)
    result.moves.append({"side": side, "round": expected_round,
                         "command_id": command_id, **order.dump()})
    result.version += 1
    return result


def export_replay(match: AlternateMatch):
    """Private event-sourced record. Never return this from a seat endpoint."""
    return {
        "edition": EDITION, "rules_digest": match.rules_digest,
        "scenario": match.private.scenario.snapshot(),
        "scenario_digest": match.private.scenario.digest(),
        "seed": match.private.seed, "seats": deepcopy(match.private.seats),
        "moves": deepcopy(match.moves),
    }


def replay(record):
    if not isinstance(record, dict) or set(record) != {
        "edition", "rules_digest", "scenario", "scenario_digest",
        "seed", "seats", "moves"
    } or record["edition"] != EDITION or record["rules_digest"] != catalog_digest():
        raise ValueError("Invalid or unsupported V2 replay")
    scenario = parse_scenario(record["scenario"])
    if record["scenario_digest"] != scenario.digest():
        raise ValueError("Scenario digest mismatch")
    seats = record["seats"]
    if not isinstance(seats, dict) or set(seats) != {"red", "blue"}:
        raise ValueError("Invalid V2 seats")
    moves = record["moves"]
    if not isinstance(moves, list) or len(moves) > scenario.turn_limit * 2:
        raise ValueError("Invalid V2 move count")
    match = new_match(scenario, record["seed"], seats["red"], seats["blue"])
    for entry in moves:
        if not isinstance(entry, dict) or set(entry) != {
            "side", "round", "command_id", "action", "target", "source"
        } or entry["side"] not in ("red", "blue"):
            raise ValueError("Invalid V2 move record")
        if entry["side"] != match.active_side:
            raise ValueError("Invalid V2 move sequence")
        order = engine.Order(entry["action"], entry["target"], entry["source"])
        match = commit(match, seats[entry["side"]], order,
                       entry["round"], entry["command_id"])
    if export_replay(match) != record:
        raise ValueError("Noncanonical V2 replay")
    return match
