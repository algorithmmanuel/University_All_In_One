"""Versioned V3 Microfinance business-impact score, calculated only at conclusion.

The single explicit victory objective remains preservation/alteration of the
high-value loan ledger. Scores contextualise availability, access, response
and resource cost. They are not an undisclosed alternate victory mechanism.
"""
from copy import deepcopy


def calculate(state):
    assets = state["assets"]
    total = sum(asset["value"] for asset in assets.values())
    unavailable = sum(asset["value"] for asset in assets.values()
                      if asset["isolated"] or asset["disrupted"])
    accessed = sum(asset["value"] for asset in assets.values() if asset["access"] > 0)
    integrity_failed = bool(assets["ledger"]["fraud"])
    monitoring = sum("monitoring" in asset["controls"] for asset in assets.values())
    confirmed_signals = sum(event["kind"] in ("alert", "finding")
                            for event in state["recent"] if event["side"] == "blue")
    assessed = sum(info["assessment"] is not None for info in state["red_known"].values())
    return {
        "victory_rule": "microfinance_ledger_integrity_v1",
        "objective_achieved": integrity_failed,
        "asset_value_total": total,
        "service_value_unavailable": unavailable,
        "service_value_available": total - unavailable,
        "foothold_value_confirmed": accessed,
        "red_assets_identified": len(state["red_known"]),
        "red_assets_assessed": assessed,
        "blue_monitored_assets": monitoring,
        "blue_recorded_security_signals": confirmed_signals,
        "remaining_credits": {"blue": state["blue_credits"], "red": state["red_credits"]},
        "blue_score": max(0, (80 if not integrity_failed else 0) +
                          round(20 * (total - unavailable) / total)),
        "red_score": (80 if integrity_failed else 0) +
                      min(20, round(20 * accessed / total)),
        "note": (
            "The winner is determined by the ledger integrity objective. "
            "Scores describe business availability and confirmed footholds; "
            "an isolation decision can protect confidentiality while reducing service availability. "
            "Monitoring signals are suspicious activity, not confirmation of successful attacks."
        ),
    }
