"""Participant-only, post-match V2 coaching with symmetrical seeded alternatives.

This module reads private resolved match truth only after the authenticated
participant has been authorized and the winner is final. Nothing generated here
is included in live seat views. Hypotheticals replay one action from its actual
opening state, not a guaranteed alternative future.
"""
from copy import deepcopy

from . import engine, v2_alternating as alternate


def _ranking(event, side):
    """Promote consequential actions and own-side decisions, with stable ties."""
    action = event["action"]
    weight = 0 if action.startswith("wait_") else 2
    if event["success"]:
        weight += 2
    if event["detected"]:
        weight += 1
    if action in ("exfiltrate", "fraud", "disrupt", "recover", "contain", "lateral", "escalate"):
        weight += 3
    if event["side"] == side:
        weight += 2
    return weight


def _alternatives(opening, actual, event, index):
    """Measure at most two alternatives available to this seat at this moment."""
    actor = opening.private.seats[event["side"]]
    options = alternate.available_orders(opening, actor)
    current = engine.Order(event["action"], event["target"], event["source"])
    # Prefer an affordable change on the same asset before unrelated choices.
    candidates = sorted(
        (o for o in options if o != current and not o.action.startswith("wait_")),
        key=lambda o: (o.target != current.target, o.action, o.target or ""),
    )
    out = []
    for candidate in candidates[:16]:
        trial = alternate.commit(
            opening, actor, candidate, opening.round,
            f"debrief-candidate-{index}-{len(out)}",
        )
        observed = trial.private.timeline[-1]
        # Report only measured one-move outcomes; no final-winner claims.
        effect = observed["after"] != observed["before"]
        if not effect and not observed["success"]:
            continue
        statement = (
            "In this one-action replay with the same deterministic starting state, the alternative "
            + ("achieved its immediate aim" if observed["success"] else "did not achieve its immediate aim")
            + (" and changed the selected asset state." if effect else " without changing the selected asset state.")
            + " It does not establish a different final winner."
        )
        out.append({
            "turn": event["turn"], **candidate.dump(),
            "side": event["side"], "explanation": statement,
            "framework": observed["framework"],
        })
        if len(out) == 2:
            break
    return out


def debrief(match, player):
    """Return a bounded pivotal summary and the complete optional transcript."""
    side = engine._side(match.private, player)
    if not match.winner:
        raise ValueError("Debrief is only available after completion")
    events = match.private.timeline
    timeline = [
        {k: deepcopy(event[k]) for k in (
            "turn", "side", "action", "target", "source",
            "success", "detected", "framework",
        )} for event in events
    ]
    ranked = sorted(
        range(len(events)),
        key=lambda index: (-_ranking(events[index], side), index),
    )
    substantive = [i for i in ranked if not events[i]["action"].startswith("wait_")]
    # Present the strongest measured decisions first, not chronological order.
    # A passive training match still gets a limited review of its actual passes.
    indices = (substantive or ranked)[:5]
    selected = set(indices)
    opening = alternate.new_match(
        match.private.scenario, match.private.seed,
        match.private.seats["red"], match.private.seats["blue"],
    )
    opportunities = {}
    for index, move in enumerate(match.moves):
        if index in selected:
            opportunities[index] = _alternatives(opening, None, events[index], index)
        opening = alternate.commit(
            opening, opening.private.seats[move["side"]],
            engine.Order(move["action"], move["target"], move["source"]),
            move["round"], move["command_id"],
        )
    pivotal = []
    alternatives = []
    for index in indices:
        event = events[index]
        measured = opportunities.get(index, [])[:2]
        alternatives.extend(measured)
        pivotal.append({
            **timeline[index],
            "reason": (
                "This decision directly affected the incident or exposed a detection opportunity."
                if event["success"] or event["detected"] else
                "This decision illustrates an attempted action, resource cost or defensive trade-off."
            ),
            "alternatives": measured,
        })
    return {
        "winner": match.winner,
        "objective": match.private.scenario.objective.model_dump(mode="json"),
        "timeline": timeline,
        "pivotal": pivotal,
        "missed": [],
        "alternatives": alternatives,
        "explanation": (
            "Top decisions are ranked using visible action impact, detections and your role; "
            "the complete transcript is available below. Alternatives are bounded "
            "one-action deterministic replays, not predictions of a different final winner."
        ),
    }
