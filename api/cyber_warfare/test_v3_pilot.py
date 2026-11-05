"""V3 Microfinance domain acceptance: no changes to V1/V2 games."""
from copy import deepcopy
import json
import pytest

from cyber_warfare import v3_pilot as pilot
from cyber_warfare import v3_clock


def game():
    return pilot.new("fixed-private-seed", "blue-account", "red-account",
                     v3_clock.Config(30, 90))


def start(state=None):
    s = state or game()
    s = pilot.ready(s, "blue-account", 1000)
    return pilot.ready(s, "red-account", 1000)


def take(state, side, action, target, now, source=None):
    clock = state["clock"]
    return pilot.act(
        state, side + "-account",
        {"action": action, "target": target, "source": source},
        now, f"{side}-{clock['turn_sequence']}", clock["turn_sequence"])


def test_blue_owns_every_asset_red_starts_with_partial_inventory():
    g = game()
    b = pilot.project(g, "blue-account")
    r = pilot.project(g, "red-account")
    assert len(b["assets"]) == 16
    assert len(r["assets"]) == 2
    assert "ledger" not in json.dumps(r)
    assert "seed" not in json.dumps(r)
    assert "weaknesses" not in json.dumps(r)
    assert r["discovery_hint"] and "five" not in r["discovery_hint"]
    with pytest.raises(PermissionError):
        pilot.project(g, "stranger")


def test_preparation_is_private_but_control_effect_is_real():
    g = game()
    g = pilot.prepare(g, "blue-account", control="monitoring", target="teller")
    g = pilot.prepare(g, "blue-account", control="segmented", target="ledger")
    g = pilot.prepare(g, "red-account", strategy="quiet_investigation")
    red = pilot.project(g, "red-account")
    assert "segmented" not in json.dumps(red)
    assert "monitoring" not in json.dumps(red)
    assert "quiet_investigation" == red["strategy"]
    assert "monitoring" in next(a for a in pilot.project(g, "blue-account")["assets"] if a["id"] == "teller")["controls"]
    with pytest.raises(ValueError):
        pilot.prepare(g, "red-account", control="hardened", target="teller")
    assert pilot.ready(g, "blue-account", 1000)["phase"] == "prepare"
    started = start(g)
    assert started["phase"] == "engage"
    assert started["clock"]["match_deadline_at"] == 2800


def test_progressive_discovery_and_monitored_probe_no_hidden_defence_leak():
    g = pilot.prepare(game(), "blue-account", control="monitoring", target="teller")
    g = start(g)
    g = take(g, "blue", "wait_blue", None, 1001)
    red = pilot.project(g, "red-account", 1001)
    assert any(o["action"] == "recon" for o in red["offers"])
    assert not any(o["target"] == "ledger" for o in red["offers"])
    g = take(g, "red", "recon", "teller", 1002)
    red = pilot.project(g, "red-account", 1002)
    blue = pilot.project(g, "blue-account", 1002)
    assert "identity" in {a["id"] for a in red["assets"]}
    assert "ledger" not in {a["id"] for a in red["assets"]}
    assert "seed" not in json.dumps(red)
    assert "weaknesses" not in json.dumps(red)
    assert not any("Red" in e["message"] for e in blue["evidence"])
    # A separate assessed asset does not disclose internal Blue telemetry.
    g = take(g, "blue", "wait_blue", None, 1003)
    g = take(g, "red", "recon", "identity", 1004)
    assert "ledger" in {a["id"] for a in pilot.project(g, "red-account", 1004)["assets"]}
    assert "bureau" not in {a["id"] for a in pilot.project(g, "red-account", 1004)["assets"]}


def test_high_value_assessment_and_blue_policy_staleness():
    g = start()
    g = take(g, "blue", "wait_blue", None, 1001)
    g = take(g, "red", "recon", "teller", 1002)
    g = take(g, "blue", "wait_blue", None, 1003)
    g = take(g, "red", "recon", "identity", 1004)
    g = take(g, "blue", "wait_blue", None, 1005)
    g = take(g, "red", "assess", "ledger", 1006)
    ledger = next(a for a in pilot.project(g, "red-account", 1006)["assets"] if a["id"] == "ledger")
    assert ledger["business_value"] == 80
    assert ledger["assessment"]["weaknesses"]
    assert ledger["assessment"]["estimated_patch_age_days"] == 94
    g = take(g, "blue", "patch", "ledger", 1007)
    ledger = next(a for a in pilot.project(g, "red-account", 1007)["assets"] if a["id"] == "ledger")
    assert "privilege" in ledger["assessment"]["weaknesses"]  # Stale, not omniscient
    assert ledger["assessment"]["estimated_patch_age_days"] == 94
    blue_ledger = next(a for a in pilot.project(g, "blue-account", 1007)["assets"] if a["id"] == "ledger")
    assert blue_ledger["patch_age_days"] == 0


def test_no_fixed_round_end_and_automatic_pass_preserves_absolute_clock():
    g = start()
    g["red_credits"] = 0
    g["blue_credits"] = 0
    for i in range(80):
        side = g["clock"]["active_side"]
        g = take(g, side, "wait_" + side, None, 1001 + i)
    assert g["phase"] == "engage" and g["clock"]["turn_sequence"] == 81
    assert g["clock"]["match_deadline_at"] == 2800
    g = pilot.settle(g, 2800)
    assert g["winner"] == "blue" and g["phase"] == "finished"
    assert pilot.settle(g, 2900) == g
    assert len(g["recent"]) <= 120
    assert g["event_count"] > 80


def test_expired_turn_advances_without_client_poll_and_restarts_are_deterministic():
    g = start()
    once = pilot.settle(g, 1090)
    assert once["clock"]["active_side"] == "red"
    assert once["clock"]["match_deadline_at"] == 2800
    assert pilot.settle(once, 1090) == once
    recovered = pilot.settle(deepcopy(g), 1400)
    assert recovered == pilot.settle(deepcopy(g), 1400)
    assert recovered["clock"]["match_deadline_at"] == 2800
    with pytest.raises(ValueError):
        take(recovered, "blue", "wait_blue", None, 1091)


def test_duplicate_request_idempotence_and_seat_authorization():
    g = start()
    order = {"action": "wait_blue", "target": None, "source": None}
    moved = pilot.act(g, "blue-account", order, 1001, "once", 1)
    assert pilot.act(moved, "blue-account", order, 1002, "once", 1) == moved
    with pytest.raises(ValueError):
        pilot.act(moved, "blue-account", {"action": "monitor", "target": "teller", "source": None},
                  1002, "once", 1)
    with pytest.raises(PermissionError):
        pilot.act(g, "intruder", order, 1001, "intruder", 1)


def test_legacy_matches_are_not_modified():
    from cyber_warfare import engine
    from cyber_warfare.scenario import load_scenario
    s = load_scenario("microfinance")
    assert s.turn_limit == 12
    legacy = engine.new_match(s, "old-match", "red", "blue")
    assert engine.view(legacy, "red")["turn_limit"] == 12


def test_unsupported_scenario_or_forged_discovery_does_not_enter_projection():
    g = game()
    before = deepcopy(g)
    with pytest.raises(ValueError):
        pilot.prepare(g, "blue-account", control="magic", target="ledger")
    assert before == g
    g = start(g)
    with pytest.raises(ValueError):
        pilot.act(g, "red-account", {"action": "fraud", "target": "ledger", "source": None},
                  1000, "wrong", 1)


def test_policy_patch_does_not_magically_remove_existing_access():
    g = game()
    g["assets"]["teller"]["access"] = 1
    patched = pilot.prepare(g, "blue-account", control="patched", target="teller")
    assert patched["assets"]["teller"]["access"] == 1
    assert "privilege" not in patched["assets"]["teller"]["weaknesses"]


def test_final_score_explains_availability_tradeoffs_but_not_premature_intelligence():
    g = start()
    live = pilot.project(g, "red-account", 1000)
    assert live["score"] is None
    # Blue isolation has an availability cost even without a proven Red breach.
    g = take(g, "blue", "isolate", "ledger", 1001)
    g = pilot.settle(g, 2800)
    blue = pilot.project(g, "blue-account")
    red = pilot.project(g, "red-account")
    assert blue["winner"] == red["winner"] == "blue"
    assert blue["score"] == red["score"]
    assert blue["score"]["service_value_unavailable"] >= 80
    assert blue["score"]["service_value_available"] < blue["score"]["asset_value_total"]
    assert blue["score"]["victory_rule"] == "microfinance_ledger_integrity_v1"


def test_policies_are_declarations_only_and_red_cannot_inspect_them():
    g = game()
    before = pilot.project(g, "blue-account")
    declared = pilot.prepare(g, "blue-account", policy="patch_management")
    after = pilot.project(declared, "blue-account")
    assert after["policies"] == ["patch_management"]
    assert after["assets"] == before["assets"]
    assert "patch_management" not in json.dumps(pilot.project(declared, "red-account"))
    deployed = pilot.prepare(declared, "blue-account", control="patched", target="teller")
    teller = next(a for a in pilot.project(deployed, "blue-account")["assets"]
                  if a["id"] == "teller")
    assert "patched" in teller["controls"]
    with pytest.raises(ValueError):
        pilot.prepare(declared, "blue-account", policy="patch_management")
    with pytest.raises(ValueError):
        pilot.prepare(declared, "red-account", policy="patch_management")
