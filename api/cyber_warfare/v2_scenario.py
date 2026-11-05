"""Build an isolated V2 starting snapshot from an existing validated scenario.

This adapter does not change live matches or create simulated events. It allows
the six current scenario configurations to exercise the V2 state contract.
"""
from .scenario import Scenario
from .v2_state import AssetTruth, Capability, MatchTruth, SeatKnowledge
from .v2_validation import validate_match


def scenario_initial_v2(scenario: Scenario) -> MatchTruth:
    if not isinstance(scenario, Scenario):
        raise ValueError("Validated scenario required")
    capabilities = tuple(
        Capability(id=f"sensor_{index}", owner="blue", asset_id=asset.id,
                   evidence_kinds=frozenset({"endpoint"}))
        for index, asset in enumerate(scenario.assets, start=1)
        if "monitoring" in asset.controls
    )
    start = MatchTruth(
        edition="red-blue-v2", turn=1,
        assets=tuple(
            AssetTruth(id=a.id, name=a.name, kind=a.kind, value=a.value,
                       available=True, blue_controls=tuple(a.controls),
                       red_access=a.initial_access)
            for a in scenario.assets
        ),
        capabilities=capabilities,
        evidence=(),
        blue_inventory=frozenset(a.id for a in scenario.assets),
        red_known=frozenset(scenario.red.known_assets),
        red_knowledge=tuple(
            SeatKnowledge(asset_id=a.id,
                          status="confirmed" if a.initial_access else "unknown",
                          last_observed_turn=1 if a.initial_access else None,
                          red_access=a.initial_access if a.initial_access else None)
            for a in scenario.assets if a.id in scenario.red.known_assets
        ),
    )
    validate_match(start)
    return start
