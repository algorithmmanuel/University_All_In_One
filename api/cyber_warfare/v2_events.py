"""V2 trusted-effect adapter: evolve truth and create side-scoped evidence.

ONLY the future authoritative V2 resolver may call apply_outcome, after checking
legality, cost, success, detection and actor seat. HTTP input MUST NOT construct
outcomes. The current v1 engine/API are deliberately not connected to this code.
"""
from dataclasses import dataclass, replace
from typing import Literal

from .v2_state import Capability, Evidence, MatchTruth, SeatKnowledge
from .v2_validation import validate_match

OutcomeKind = Literal[
    "red_compromise", "red_recon", "red_disrupt",
    "blue_monitor", "blue_contain", "blue_recover", "blue_investigate",
]
ACTOR = {
    "red_compromise": "red", "red_recon": "red", "red_disrupt": "red",
    "blue_monitor": "blue", "blue_contain": "blue",
    "blue_recover": "blue", "blue_investigate": "blue",
}


@dataclass(frozen=True)
class ResolvedOutcome:
    """Private, already resolved and authorised engine event (not an API body)."""
    kind: OutcomeKind
    asset_id: str
    success: bool
    detected: bool = False
    access_level: int = 1

    def __post_init__(self):
        if (self.kind not in ACTOR or not isinstance(self.asset_id, str)
                or type(self.success) is not bool or type(self.detected) is not bool
                or type(self.access_level) is not int
                or self.access_level not in (1, 2)):
            raise ValueError("Invalid resolved outcome")
        if self.detected and self.kind not in ("red_compromise", "red_disrupt"):
            raise ValueError("Detection is only meaningful for hostile actions")


def apply_outcome(match: MatchTruth, result: ResolvedOutcome) -> MatchTruth:
    """Produce an immutable new truth and generated evidence from a trusted result.

    This is a domain adapter, NOT a secure command interface. The future
    resolver must verify eligibility and probabilities before invoking it.
    """
    validate_match(match)
    if result.asset_id not in match.blue_inventory:
        raise ValueError("Unknown outcome asset")
    asset = next(a for a in match.assets if a.id == result.asset_id)
    assets = list(match.assets)
    caps = list(match.capabilities)
    events = list(match.evidence)
    red_known = set(match.red_known)
    knowledge = {k.asset_id: k for k in match.red_knowledge}

    def record(kind, text, sides, certainty, required=None):
        index = len(events) + 1
        events.append(Evidence(
            id=f"evt_{index}", turn=match.turn, asset_id=asset.id,
            kind=kind, text=text, visible_to=frozenset(sides),
            certainty=certainty, required_capability=required))

    if result.success:
        if result.kind == "red_compromise":
            assets[assets.index(asset)] = replace(
                asset, red_access=max(asset.red_access, result.access_level))
            red_known.add(asset.id)
            knowledge[asset.id] = SeatKnowledge(
                asset.id, "confirmed", match.turn,
                max(asset.red_access, result.access_level))
            record("access", "Your access to this asset was established.",
                   ("red",), "confirmed")
        elif result.kind == "red_recon":
            red_known.add(asset.id)
            knowledge[asset.id] = SeatKnowledge(
                asset.id, "confirmed", match.turn, asset.red_access)
            record("recon", "Reconnaissance updated your knowledge of this asset.",
                   ("red",), "confirmed")
        elif result.kind == "red_disrupt":
            assets[assets.index(asset)] = replace(asset, available=False)
            record("impact", "Your action disrupted the selected service.",
                   ("red",), "confirmed")
        elif result.kind == "blue_monitor":
            controls = tuple(sorted(set(asset.blue_controls) | {"monitoring"}))
            assets[assets.index(asset)] = replace(asset, blue_controls=controls)
            if not any(c.owner == "blue" and c.asset_id == asset.id
                       and "endpoint" in c.evidence_kinds for c in caps):
                sensor_index = 1
                used_ids = {c.id for c in caps}
                while f"sensor_{sensor_index}" in used_ids:
                    sensor_index += 1
                caps.append(Capability(id=f"sensor_{sensor_index}",
                                       owner="blue", asset_id=asset.id,
                                       evidence_kinds=frozenset({"endpoint"})))
            record("control", "Endpoint monitoring enabled on this asset.",
                   ("blue",), "confirmed")
        elif result.kind == "blue_contain":
            assets[assets.index(asset)] = replace(asset, available=False)
            if asset.id in red_known:
                old = knowledge.get(asset.id)
                knowledge[asset.id] = SeatKnowledge(
                    asset.id, "stale", old.last_observed_turn if old else None,
                    old.red_access if old else None)
            record("control", "Asset isolated; service is unavailable.",
                   ("blue",), "confirmed")
        elif result.kind == "blue_recover":
            assets[assets.index(asset)] = replace(asset, available=True)
            record("control", "Service availability restored.",
                   ("blue",), "confirmed")
        elif result.kind == "blue_investigate":
            if asset.red_access:
                record("finding", "Investigation found suspicious account access.",
                       ("blue",), "confirmed")
            else:
                record("finding", "No conclusive evidence of access was found.",
                       ("blue",), "suspected")

    if result.detected and any(
        c.owner == "blue" and c.asset_id == asset.id and
        "endpoint" in c.evidence_kinds for c in caps
    ):
        # Generate only alerts observable at event time. Retrofitting monitoring
        # must not reveal a previously invisible historic alarm.
        record("alert", "Endpoint telemetry recorded suspicious activity.",
               ("blue",), "suspected", "endpoint")
    if not result.success:
        record("own_action", "Your action did not achieve its aim.",
               (ACTOR[result.kind],), "confirmed")

    updated = replace(
        match, assets=tuple(assets), capabilities=tuple(caps),
        evidence=tuple(events), red_known=frozenset(red_known),
        red_knowledge=tuple(sorted(knowledge.values(), key=lambda k: k.asset_id)))
    validate_match(updated)
    return updated
