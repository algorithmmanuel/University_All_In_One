"""Advanced Microfinance V3 pilot: deterministic, isolated, seat-filtered domain.

This module is a *pure domain engine*; no HTTP client may pass a trusted server
clock, private seed or arbitrary outcome directly. A future API adapter must
lock/persist matches and authorize user accounts before calling these functions.
V1/V2 engines, stored matches and catalogue are deliberately unchanged.
"""
from copy import deepcopy
from hashlib import sha256
import json

from . import v3_clock, v3_score
from .scenario import load_scenario

EDITION = "red-blue-microfinance-v3-pilot-1"
BLUE_POLICIES = {"monitoring": 2, "patched": 2, "segmented": 3, "hardened": 2}
RED_STRATEGIES = frozenset({"surface_mapping", "quiet_investigation"})
POLICY_LIBRARY = frozenset({"patch_management", "network_segmentation", "security_monitoring", "access_governance"})
ACTION_COST = {
    "recon": 1, "assess": 1, "phish": 2, "cloud_access": 2,
    "escalate": 2, "lateral": 2, "fraud": 3,
    "monitor": 2, "patch": 2, "segment": 3,
    "isolate": 2, "restore": 2, "investigate": 1,
    "wait_red": 0, "wait_blue": 0,
}
MAX_RECENT = 120


def _hash(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _actor(state, player):
    for side in ("red", "blue"):
        if state["players"][side] == player:
            return side
    raise PermissionError("Not an authorised match participant")


def _asset(state, asset_id):
    try:
        return state["assets"][asset_id]
    except KeyError:
        raise ValueError("Unknown asset") from None


def _append(state, event):
    """Append to a hash-chained bounded recent transcript, retaining event count."""
    clean = deepcopy(event)
    state["event_count"] += 1
    state["event_digest"] = _hash([state["event_digest"], state["event_count"], clean])
    state["recent"].append({"sequence": state["event_count"], **clean})
    if len(state["recent"]) > MAX_RECENT:
        state["recent"] = state["recent"][-MAX_RECENT:]


def new(seed, blue_player, red_player, config=None):
    """Create a separate V3 Microfinance match; Blue owns all assets at preparation."""
    if not isinstance(seed, str) or not 1 <= len(seed) <= 128:
        raise ValueError("Invalid private seed")
    if (not isinstance(blue_player, str) or not isinstance(red_player, str)
            or not blue_player or not red_player or blue_player == red_player):
        raise ValueError("Two distinct bound player identities required")
    cfg = config or v3_clock.Config()
    if not isinstance(cfg, v3_clock.Config):
        raise ValueError("Validated V3 clock configuration required")
    scenario = load_scenario("microfinance")
    assets = {}
    for a in scenario.assets:
        assets[a.id] = {
            "id": a.id, "name": a.name, "kind": a.kind, "value": a.value,
            "exposed": a.exposed, "controls": list(a.controls),
            "weaknesses": list(a.vulnerabilities),
            "access": 0, "isolated": False, "fraud": False, "disrupted": False,
        }
    known = {
        a_id: {"confidence": "observed", "assessment": None, "observed_at": None,
               "believed_access": 0}
        for a_id in scenario.red.known_assets
    }
    return {
        "edition": EDITION, "phase": "prepare",
        "seed": seed, "players": {"blue": blue_player, "red": red_player},
        "scenario": scenario.id, "scenario_digest": scenario.digest(),
        "config": {"match_minutes": cfg.match_minutes, "turn_seconds": cfg.turn_seconds},
        "assets": assets,
        "edges": [e.model_dump() for e in scenario.connections],
        "red_known": known, "blue_credits": 12, "red_credits": 24,
        "red_strategy": "surface_mapping", "blue_policies": [],
        "prepared": {"blue": False, "red": False},
        "clock": None, "winner": None, "reason": None, "score": None,
        "version": 0, "event_count": 0, "event_digest": _hash(["v3", scenario.digest()]),
        "recent": [], "receipts": {}, "alerts": [],
    }


def prepare(state, player, *, control=None, target=None, strategy=None, policy=None):
    """Spend bounded Blue setup credits or select Red strategy before lock-in."""
    updated = deepcopy(state)
    side = _actor(updated, player)
    if updated["phase"] != "prepare" or updated["prepared"][side]:
        raise ValueError("Preparation unavailable")
    if side == "blue":
        if policy is not None:
            if strategy is not None or control is not None or target is not None or policy not in POLICY_LIBRARY:
                raise ValueError("Invalid security policy declaration")
            if policy in updated["blue_policies"]:
                raise ValueError("Policy already declared")
            updated["blue_policies"].append(policy)
            updated["blue_policies"].sort()
            _append(updated, {"kind": "policy_declared", "side": "blue", "policy": policy})
            updated["version"] += 1
            return updated
        if strategy is not None or control not in BLUE_POLICIES or target not in updated["assets"]:
            raise ValueError("Invalid defensive preparation")
        cost = BLUE_POLICIES[control]
        if updated["blue_credits"] < cost:
            raise ValueError("Insufficient preparation credits")
        asset = _asset(updated, target)
        if control in asset["controls"]:
            raise ValueError("Control already deployed")
        asset["controls"].append(control)
        asset["controls"].sort()
        if control == "patched":
            asset["weaknesses"] = [w for w in asset["weaknesses"] if w != "privilege"]
        if control == "hardened":
            asset["weaknesses"] = [w for w in asset["weaknesses"] if w != "configuration"]
        updated["blue_credits"] -= cost
        _append(updated, {"kind": "policy_deployment", "side": "blue",
                          "target": target, "control": control})
    else:
        if control is not None or target is not None or policy is not None or strategy not in RED_STRATEGIES:
            raise ValueError("Invalid Red preparation")
        updated["red_strategy"] = strategy
        _append(updated, {"kind": "recon_strategy", "side": "red",
                          "strategy": strategy})
    updated["version"] += 1
    return updated


def ready(state, player, server_now):
    """Begin the immutable shared clock only after both roles are ready."""
    updated = deepcopy(state)
    side = _actor(updated, player)
    if updated["phase"] != "prepare" or updated["prepared"][side]:
        raise ValueError("Seat already ready or match started")
    updated["prepared"][side] = True
    updated["version"] += 1
    if all(updated["prepared"].values()):
        cfg = v3_clock.Config(**updated["config"])
        clock = v3_clock.begin(cfg, server_now)
        updated["clock"] = _clock_dict(clock)
        updated["phase"] = "engage"
        _append(updated, {"kind": "engagement_started", "side": "system"})
    return updated


def _clock_dict(clock):
    return {
        "started_at": clock.started_at,
        "match_deadline_at": clock.match_deadline_at,
        "turn_started_at": clock.turn_started_at,
        "turn_deadline_at": clock.turn_deadline_at,
        "active_side": clock.active_side,
        "turn_sequence": clock.turn_sequence,
    }


def _clock(state):
    return v3_clock.Clock(
        v3_clock.Config(**state["config"]), **state["clock"],
    )


def _roll(state, action, target, label):
    data = [EDITION, state["seed"], state["event_count"], action, target, label]
    return int(_hash(data)[:13], 16) / float(16 ** 13)


def _event_for(state, side, *, target=None, message, kind):
    """Events are created exclusively by the trusted reducer, never the caller."""
    _append(state, {"side": side, "target": target, "message": message, "kind": kind})


def _evidence(state, side):
    """Blue sees alerts, Red sees only own actions, both see public match status."""
    visible = []
    for event in state["recent"]:
        if event.get("side") == side and event.get("kind") not in ("policy_deployment", "recon_strategy"):
            visible.append({
                "sequence": event["sequence"], "kind": event["kind"],
                "target": event.get("target"), "message": event.get("message", ""),
            })
    return visible[-40:]


def _red_assets(state):
    results = []
    for asset_id, info in sorted(state["red_known"].items()):
        truth = _asset(state, asset_id)
        item = {
            "id": asset_id, "name": truth["name"], "kind": truth["kind"],
            "exposed": truth["exposed"],
            # The value is assessed only after investigating the asset; do not
            # leak private business valuations from Blue's inventory.
            "business_value": truth["value"] if info["assessment"] is not None else None,
            "knowledge": info["confidence"], "observed_at": info["observed_at"],
            "assessment": deepcopy(info["assessment"]),
            "believed_access": info["believed_access"],
        }
        results.append(item)
    return results


def project(state, player, server_now=None):
    """Only this server-side projection may reach a participant or the computer."""
    side = _actor(state, player)
    base = {
        "edition": EDITION, "phase": state["phase"], "side": side,
        "version": state["version"], "prepared": dict(state["prepared"]),
        "match_minutes": state["config"]["match_minutes"],
        "turn_seconds": state["config"]["turn_seconds"],
        "winner": state["winner"], "reason": state["reason"],
        "event_count": state["event_count"],
        "score": deepcopy(state["score"]) if state["phase"] == "finished" else None,
    }
    if side == "blue":
        base.update(assets=[
            {k: deepcopy(v) for k, v in a.items() if k not in ("access",)}
            for _, a in sorted(state["assets"].items())
        ], connections=deepcopy(state["edges"]), credits=state["blue_credits"],
                    evidence=_evidence(state, side),
                    policies=deepcopy(state["blue_policies"]))
    else:
        known = state["red_known"]
        base.update(assets=_red_assets(state),
                    connections=[deepcopy(edge) for edge in state["edges"]
                                 if edge["source"] in known and edge["target"] in known],
                    credits=state["red_credits"], evidence=_evidence(state, side),
                    discovery_hint="Additional assets or connections may remain undiscovered.")
    if state["phase"] == "engage":
        if server_now is None:
            raise ValueError("Trusted server time required for a live projection")
        base["clock"] = v3_clock.remaining(_clock(state), server_now)
        base["offers"] = offers(state, player)
    elif state["phase"] == "prepare":
        base["offers"] = []
        if side == "red":
            base["strategy"] = state["red_strategy"]
    else:
        base["offers"] = []
    return base


def offers(state, player):
    """Permitted targets are computed from seat knowledge, never private truth."""
    side = _actor(state, player)
    if state["phase"] != "engage" or state["winner"] is not None:
        return []
    if state["clock"]["active_side"] != side:
        return []
    budget = state["red_credits"] if side == "red" else state["blue_credits"]
    ids = sorted(state["red_known"] if side == "red" else state["assets"])
    choices = [{"action": f"wait_{side}", "target": None, "source": None, "cost": 0}]
    for target in ids:
        a = state["red_known"].get(target) if side == "red" else state["assets"][target]
        if side == "blue":
            actions = ("monitor", "patch", "segment", "isolate", "restore", "investigate")
        else:
            access = a["believed_access"]
            actions = ["recon", "assess"]
            if state["assets"][target]["exposed"] and access == 0:
                kind = state["assets"][target]["kind"]
                if kind == "workstation":
                    actions.append("phish")
                if kind in ("server", "cloud"):
                    actions.append("cloud_access")
            if access == 1:
                actions.append("escalate")
            if access == 2 and target == "ledger":
                actions.append("fraud")
            # Only an already discovered trust link from an own privileged
            # foothold may unlock lateral movement.
            for edge in state["edges"]:
                if edge["target"] == target and edge["source"] in state["red_known"]:
                    if state["red_known"][edge["source"]]["believed_access"] == 2:
                        actions.append(("lateral", edge["source"]))
        for action in actions:
            source = None
            if isinstance(action, tuple):
                action, source = action
            if ACTION_COST[action] <= budget:
                choices.append({"action": action, "target": target,
                                "source": source, "cost": ACTION_COST[action]})
    return choices


def _resolve(state, side, order):
    """Apply the chosen permitted action to private truth and filtered evidence."""
    aid, target, source = order["action"], order["target"], order["source"]
    if aid.startswith("wait_"):
        _event_for(state, side, kind="pass", message="Turn passed.")
        return
    asset = _asset(state, target)
    if side == "blue":
        if aid == "monitor":
            if "monitoring" not in asset["controls"]:
                asset["controls"].append("monitoring")
            _event_for(state, side, target=target, kind="control", message="Monitoring deployed.")
        elif aid == "patch":
            if "patched" not in asset["controls"]:
                asset["controls"].append("patched")
            asset["weaknesses"] = [w for w in asset["weaknesses"] if w != "privilege"]
            _event_for(state, side, target=target, kind="control", message="Pending privilege patch applied.")
        elif aid == "segment":
            if "segmented" not in asset["controls"]:
                asset["controls"].append("segmented")
            _event_for(state, side, target=target, kind="control", message="Trust path segmentation enabled.")
        elif aid == "isolate":
            asset["isolated"] = True
            _event_for(state, side, target=target, kind="availability", message="Asset isolated; service availability reduced.")
        elif aid == "restore":
            asset["isolated"] = False
            _event_for(state, side, target=target, kind="availability", message="Isolation lifted; service restored.")
        else:
            found = bool(asset["access"])
            _event_for(state, side, target=target, kind="finding",
                       message="Suspicious simulated account access confirmed." if found
                       else "No conclusive access evidence found; absence of proof is not safety.")
        return
    # Red receives no private controls unless it has actually assessed them.
    belief = state["red_known"][target]
    if aid in ("recon", "assess"):
        if asset["isolated"]:
            _event_for(state, side, target=target, kind="recon",
                       message="Probe could not establish reachability; earlier information may be outdated.")
        else:
            if aid == "recon":
                # A probe can reveal one adjacent asset in canonical order,
                # without exposing unknown node count or IDs beforehand.
                edges = sorted(edge["target"] for edge in state["edges"]
                               if edge["source"] == target and edge["target"] not in state["red_known"])
                if edges:
                    nxt = edges[0]
                    state["red_known"][nxt] = {
                        "confidence": "suspected", "assessment": None,
                        "observed_at": state["clock"]["turn_sequence"],
                        "believed_access": 0,
                    }
                    _event_for(state, side, target=nxt, kind="discovery",
                               message="Additional connected service discovered; further assessment needed.")
            else:
                belief["assessment"] = {
                    "weaknesses": deepcopy(asset["weaknesses"]),
                    "controls": ["Possible boundary restriction"] if "segmented" in asset["controls"] else [],
                }
                belief["confidence"] = "assessed"
                belief["observed_at"] = state["clock"]["turn_sequence"]
            _event_for(state, side, target=target, kind="recon",
                       message="Asset investigation complete; results may become stale.")
    else:
        chance = {"phish": .65, "cloud_access": .65, "escalate": .65,
                  "lateral": .60, "fraud": .60}[aid]
        if aid == "phish":
            feasible = asset["exposed"] and "phishing" in asset["weaknesses"]
        elif aid == "cloud_access":
            feasible = asset["exposed"] and "configuration" in asset["weaknesses"]
        elif aid == "escalate":
            feasible = asset["access"] == 1 and "privilege" in asset["weaknesses"]
        elif aid == "lateral":
            upstream = _asset(state, source)
            feasible = (upstream["access"] == 2 and not upstream["isolated"]
                        and {"source": source, "target": target} in state["edges"]
                        and "segmented" not in upstream["controls"]
                        and "segmented" not in asset["controls"])
        else:
            feasible = asset["access"] == 2 and target == "ledger"
        feasible = feasible and not asset["isolated"]
        if "hardened" in asset["controls"]:
            chance -= .25
        if "patched" in asset["controls"]:
            chance -= .20
        success = feasible and _roll(state, aid, target, "success") < chance
        if success:
            if aid in ("phish", "cloud_access", "lateral"):
                asset["access"] = belief["believed_access"] = 1
            elif aid == "escalate":
                asset["access"] = belief["believed_access"] = 2
            else:
                asset["fraud"] = True
                state["winner"] = "red"
                state["reason"] = "The simulated high-value ledger integrity objective was achieved."
        elif not feasible:
            # Treat failed access as a stale-belief signal, never report which
            # private defensive control caused it.
            belief["confidence"] = "stale"
            belief["believed_access"] = 0
        _event_for(state, side, target=target, kind="attack_result",
                   message="Action met its immediate objective." if success
                   else "Action did not succeed; access or conditions may have changed.")
    # An alarm is generated only with existing monitored asset coverage.
    # An alarm is a *suspicion*, never a claim of successful compromise.
    if "monitoring" in asset["controls"] and not asset["isolated"]:
        detection_threshold = .55 if state["red_strategy"] == "quiet_investigation" else .80
        if _roll(state, aid, target, "detection") < detection_threshold:
            _event_for(state, "blue", target=target, kind="alert",
                       message="Monitoring observed suspicious activity; investigate for confirmation.")


def _expire(state):
    state["phase"] = "finished"
    if state["winner"] is None:
        state["winner"] = "blue" if not state["assets"]["ledger"]["fraud"] else "red"
        state["reason"] = (
            "Match deadline reached; the high-value ledger objective remained protected."
            if state["winner"] == "blue" else
            "Match deadline reached with the ledger integrity objective compromised."
        )
    state["score"] = v3_score.calculate(state)
    _event_for(state, "system", kind="terminal", message="The overall match deadline ended engagement.")


def settle(state, server_now):
    """Advance overdue turns at actual persisted deadlines, without browser polls.

    The API/worker must call this inside a locked transaction. A delayed worker
    can recover missed timeouts deterministically without moving the game deadline.
    """
    updated = deepcopy(state)
    if updated["phase"] != "engage":
        return updated
    clock = _clock(updated)
    if v3_clock.status(clock, server_now) == "active":
        return updated
    # At most one automatic pass per 30 seconds; 120-minute sessions can
    # accumulate <=240 overdue turns without introducing a gameplay cap.
    while server_now >= clock.turn_deadline_at and clock.turn_deadline_at < clock.match_deadline_at:
        expired_at = clock.turn_deadline_at
        side = clock.active_side
        _event_for(updated, side, kind="timeout", message="Turn expired and was automatically passed.")
        clock = v3_clock.next_turn(clock, expired_at)
        updated["clock"] = _clock_dict(clock)
        updated["version"] += 1
    if server_now >= clock.match_deadline_at:
        _expire(updated)
        updated["version"] += 1
    return updated


def act(state, player, order, server_now, command_id, expected_sequence):
    """Validate caller's authorised projection and resolve exactly one V3 move."""
    updated = settle(state, server_now)
    side = _actor(updated, player)
    if not isinstance(command_id, str) or not 1 <= len(command_id) <= 80:
        raise ValueError("Invalid command identifier")
    if type(expected_sequence) is not int or expected_sequence < 1:
        raise ValueError("Invalid expected turn")
    if not isinstance(order, dict) or set(order) != {"action", "target", "source"}:
        raise ValueError("Invalid order body")
    receipt = side + ":" + command_id
    fingerprint = [expected_sequence, order]
    if receipt in updated["receipts"]:
        if updated["receipts"][receipt] != fingerprint:
            raise ValueError("Command identifier reused for another order")
        return updated
    if updated["phase"] != "engage":
        raise ValueError("No active match turn")
    clock = _clock(updated)
    if (v3_clock.status(clock, server_now) != "active"
            or clock.active_side != side or clock.turn_sequence != expected_sequence):
        raise ValueError("Inactive or stale turn")
    if order not in [{k: v for k, v in offer.items() if k != "cost"}
                     for offer in offers(updated, player)]:
        raise ValueError("Order unavailable for this seat")
    cost = ACTION_COST[order["action"]]
    updated["red_credits" if side == "red" else "blue_credits"] -= cost
    _resolve(updated, side, order)
    updated["receipts"][receipt] = fingerprint
    updated["version"] += 1
    if updated["winner"] is not None:
        updated["phase"] = "finished"
        updated["score"] = v3_score.calculate(updated)
    else:
        updated["clock"] = _clock_dict(v3_clock.next_turn(clock, server_now))
    return updated
