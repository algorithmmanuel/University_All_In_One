"""Bounded, fail-closed checks for the additive V2 state contract.

Shape checks do not establish that a report is true. A future trusted reducer
must construct its events, audiences and sanitized messages from actual results.
"""
import re

ID = re.compile(r"^[a-z][a-z0-9_-]{0,47}$")
SIDES = frozenset(("red", "blue"))
KNOWLEDGE = frozenset(("confirmed", "suspected", "stale", "unknown"))
KINDS = frozenset(("workstation", "server", "database", "cloud", "third_party"))


def valid_id(value):
    return isinstance(value, str) and bool(ID.fullmatch(value))


def validate_match(match):
    if (match.edition != "red-blue-v2" or type(match.turn) is not int
            or not 1 <= match.turn <= 60
            or not isinstance(match.assets, tuple) or not 2 <= len(match.assets) <= 20
            or not isinstance(match.capabilities, tuple) or len(match.capabilities) > 100
            or not isinstance(match.evidence, tuple) or len(match.evidence) > 1200
            or not isinstance(match.red_knowledge, tuple)
            or not isinstance(match.blue_inventory, frozenset)
            or not isinstance(match.red_known, frozenset)):
        raise ValueError("Invalid V2 match bounds")
    ids = [a.id for a in match.assets]
    if (len(ids) != len(set(ids)) or match.blue_inventory != frozenset(ids)
            or not match.red_known <= match.blue_inventory):
        raise ValueError("Invalid V2 asset inventory")
    for asset in match.assets:
        if (not valid_id(asset.id) or not isinstance(asset.name, str)
                or not 1 <= len(asset.name) <= 160 or asset.kind not in KINDS
                or type(asset.value) is not int or not 1 <= asset.value <= 100
                or type(asset.available) is not bool
                or type(asset.red_access) is not int or asset.red_access not in (0, 1, 2)
                or type(asset.persistent) is not bool
                or not isinstance(asset.blue_controls, tuple)
                or len(asset.blue_controls) > 20
                or len(set(asset.blue_controls)) != len(asset.blue_controls)
                or any(not valid_id(v) for v in asset.blue_controls)):
            raise ValueError("Invalid V2 asset")
    if len({c.id for c in match.capabilities}) != len(match.capabilities):
        raise ValueError("Duplicate capability")
    for cap in match.capabilities:
        if (not valid_id(cap.id) or cap.owner not in SIDES
                or cap.asset_id not in match.blue_inventory
                or not isinstance(cap.evidence_kinds, frozenset)
                or not isinstance(cap.action_ids, frozenset)
                or len(cap.evidence_kinds) > 16 or len(cap.action_ids) > 40
                or any(not valid_id(v) for v in cap.evidence_kinds | cap.action_ids)):
            raise ValueError("Invalid V2 capability")
    if len({e.id for e in match.evidence}) != len(match.evidence):
        raise ValueError("Duplicate evidence event")
    for event in match.evidence:
        if (not valid_id(event.id) or type(event.turn) is not int
                or not 1 <= event.turn <= match.turn
                or event.asset_id not in match.blue_inventory
                or not valid_id(event.kind)
                or not isinstance(event.text, str) or not 1 <= len(event.text) <= 300
                or not isinstance(event.visible_to, frozenset)
                or not event.visible_to or not event.visible_to <= SIDES
                or event.certainty not in KNOWLEDGE
                or (event.required_capability is not None
                    and not valid_id(event.required_capability))
                or (event.kind == "alert" and "blue" in event.visible_to
                    and event.certainty == "confirmed")):
            raise ValueError("Invalid V2 evidence")
    if len({k.asset_id for k in match.red_knowledge}) != len(match.red_knowledge):
        raise ValueError("Duplicate knowledge")
    for knowledge in match.red_knowledge:
        if (knowledge.asset_id not in match.red_known
                or knowledge.status not in KNOWLEDGE
                or (knowledge.last_observed_turn is not None
                    and (type(knowledge.last_observed_turn) is not int
                         or not 1 <= knowledge.last_observed_turn <= match.turn))
                or (knowledge.red_access is not None
                    and (type(knowledge.red_access) is not int
                         or knowledge.red_access not in (0, 1, 2)))):
            raise ValueError("Invalid V2 knowledge")
