"""Independent V3 deadline/bot reconciliation against isolated match storage.

The caller must use an isolated Development database. Atomic SQL transactions
and PostgreSQL SKIP LOCKED avoid concurrent worker double-processing. Only
trusted server timestamps are passed into the pure pilot reducer.
"""
import time
from sqlalchemy import select
from models import RedBlueV3Match
from cyber_warfare import v3_pilot as pilot

MAX_DUE_BATCH = 40


def choose_computer(state, now):
    """Choose strictly from the computer's own filtered offers and evidence.

    Never read hidden asset truth, private control configurations or the other
    player's intentions. Decisions favour meaningful progress over repeated
    no-op reconnaissance and monitoring.
    """
    visible = pilot.project(state, "computer", now)
    choices = visible["offers"]
    if not choices:
        return None
    side = visible["side"]
    assets = {asset["id"]: asset for asset in visible["assets"]}
    evidence = visible["evidence"]
    def candidates(action):
        return [offer for offer in choices if offer["action"] == action]

    if side == "red":
        # Finish an actual permitted objective before spending time probing.
        for action in ("fraud", "escalate", "lateral"):
            permitted = candidates(action)
            if permitted:
                return min(permitted, key=lambda o: (
                    assets[o["target"]].get("kind") != "database",
                    o["target"] or "", o["source"] or "",
                ))
        already_scanned = {e["target"] for e in evidence
                           if e["kind"] == "recon" and e["target"]}
        # Scope reconnaissance to assets the bot knows about, and avoid
        # needlessly probing the same node while a new one is available.
        unscanned = [o for o in candidates("recon")
                     if o["target"] not in already_scanned]
        known_database = any(a["kind"] == "database" for a in assets.values())
        if unscanned and not known_database:
            return min(unscanned, key=lambda o: (
                {"workstation": 0, "server": 1, "cloud": 2,
                 "database": 3, "third_party": 4}.get(
                    assets[o["target"]]["kind"], 5), o["target"],
            ))
        for action in ("phish", "cloud_access"):
            permitted = candidates(action)
            if permitted:
                return min(permitted, key=lambda o: o["target"] or "")
        assessments = [o for o in candidates("assess")
                       if assets[o["target"]].get("assessment") is None]
        if assessments:
            return min(assessments, key=lambda o: (
                assets[o["target"]]["kind"] != "database", o["target"] or "",
            ))
        if unscanned:
            return min(unscanned, key=lambda o: o["target"] or "")
        return candidates("wait_red")[0]

    # Blue owns its inventory, not Red's private access or intended target.
    findings = {e["target"] for e in evidence if e["kind"] == "finding"
                and e["target"] and "confirmed" in e["message"]}
    observed = {e["target"] for e in evidence if e["kind"] == "alert" and e["target"]}
    investigated = {e["target"] for e in evidence if e["kind"] == "finding" and e["target"]}
    for target in sorted(findings):
        blocking = [o for o in candidates("isolate") if o["target"] == target
                    and not assets[target].get("isolated")]
        if blocking:
            return blocking[0]
    for target in sorted(observed - investigated):
        investigation = [o for o in candidates("investigate") if o["target"] == target]
        if investigation:
            return investigation[0]
    for action, control in (("monitor", "monitoring"), ("patch", "patched"),
                            ("segment", "segmented")):
        available = [o for o in candidates(action)
                     if control not in assets[o["target"]].get("controls", [])]
        if available:
            return min(available, key=lambda o: (
                not assets[o["target"]].get("exposed", False),
                -assets[o["target"]].get("value", 0), o["target"] or "",
            ))
    return candidates("wait_blue")[0]



def process_due_once(db, server_now=None):
    now = int(time.time()) if server_now is None else server_now
    if type(now) is not int or now < 0:
        raise ValueError("Trusted nonnegative server time required")
    query = (select(RedBlueV3Match)
             .where(RedBlueV3Match.status == "engage")
             .order_by(RedBlueV3Match.id).limit(MAX_DUE_BATCH))
    if db.bind is not None and db.bind.dialect.name == "postgresql":
        query = query.with_for_update(skip_locked=True)
    outcome = {"examined": 0, "timeouts": 0, "finished": 0, "bots": 0}
    try:
        for row in db.scalars(query).all():
            state = row.transcript
            if state.get("edition") != pilot.EDITION:
                raise ValueError("Unsupported active V3 private checkpoint")
            previous = state["version"]
            previous_event_count = state["event_count"]
            state = pilot.settle(state, now)
            outcome["examined"] += 1
            if state["phase"] == "engage":
                side = state["clock"]["active_side"]
                if state["players"][side] == "computer":
                    selection = choose_computer(state, now)
                    if selection is not None:
                        sequence = state["clock"]["turn_sequence"]
                        command_id = f"v3-bot-{side}-{sequence}"
                        state = pilot.act(
                            state, "computer",
                            {k: v for k, v in selection.items() if k != "cost"},
                            now, command_id, sequence,
                        )
                        outcome["bots"] += 1
            outcome["timeouts"] += sum(
                event.get("kind") == "timeout"
                for event in state["recent"]
                if event["sequence"] > previous_event_count
            )
            if state["phase"] == "finished":
                outcome["finished"] += 1
            if state["version"] != previous:
                row.transcript = state
                row.status = state["phase"]
        db.commit()
    except Exception:
        db.rollback()
        raise
    return outcome
