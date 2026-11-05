"""V3-only expanded Microfinance network: existing V2 JSON is never modified.

Sixteen connected assets support meaningful reconnaissance progression, Blue
policy/patch decisions and separate business impact. The graph is validated
by the existing strict scenario schema and deterministically versioned.
"""
from copy import deepcopy
from .scenario import load_scenario, parse_scenario


EXTRA_ASSETS = (
    ("branch_router", "Branch network gateway", "server", 20, False, ("configuration", "access"), ()),
    ("staff_email", "Staff messaging service", "cloud", 30, True, ("configuration",), ("monitoring",)),
    ("app_server", "Mobile application server", "server", 65, False, ("privilege", "configuration"), ("backup",)),
    ("payment_switch", "Payments switching service", "server", 85, False, ("access", "privilege"), ("monitoring",)),
    ("customers_db", "Customer identity database", "database", 90, False, ("access", "privilege"), ("backup",)),
    ("analytics_store", "Risk analytics platform", "cloud", 40, False, ("configuration", "instruction"), ("monitoring",)),
    ("backup_vault", "Recovery and backup vault", "server", 55, False, ("configuration",), ("backup", "segmented")),
    ("audit_logs", "Audit and security log collector", "server", 30, False, ("access",), ("monitoring",)),
    ("vendor_portal", "External vendor integration", "third_party", 22, True, ("access",), ()),
    ("card_processor", "Payment processor connection", "third_party", 50, False, ("access",), ()),
    ("core_banking_server", "Core banking application", "server", 100, False, ("privilege", "access"), ("backup",)),
)

EXTRA_EDGES = (
    ("identity", "branch_router"),
    ("identity", "core_banking_server"),
    ("branch_router", "staff_email"),
    ("branch_router", "audit_logs"),
    ("gateway", "app_server"),
    ("gateway", "payment_switch"),
    ("app_server", "ledger"),
    ("app_server", "analytics_store"),
    ("payment_switch", "card_processor"),
    ("core_banking_server", "customers_db"),
    ("core_banking_server", "ledger"),
    ("core_banking_server", "payment_switch"),
    ("ledger", "backup_vault"),
    ("ledger", "analytics_store"),
    ("ledger", "audit_logs"),
    ("vendor_portal", "app_server"),
    ("bureau", "vendor_portal"),
    ("backup_vault", "audit_logs"),
    ("staff_email", "identity"),
    ("audit_logs", "analytics_store"),
)


def load_v3_microfinance():
    base = deepcopy(load_scenario("microfinance").snapshot())
    base["revision"] = 2
    base["title"] = "Ledger Under Pressure — Advanced Microfinance"
    # Retained only to satisfy the legacy schema validator; V3 never uses it
    # to end or restrict the engagement.
    base["turn_limit"] = 30
    for aid, name, kind, value, exposed, weaknesses, controls in EXTRA_ASSETS:
        base["assets"].append({
            "id": aid, "name": name, "kind": kind,
            "value": value, "exposed": exposed,
            "vulnerabilities": list(weaknesses),
            "controls": list(controls), "initial_access": 0,
        })
        base["blue"]["known_assets"].append(aid)
    base["connections"].extend(
        {"source": a, "target": b} for a, b in EXTRA_EDGES
    )
    return parse_scenario(base)
