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
    """Choose strictly from the computer seat's own filtered action offers."""
    visible = pilot.project(state, "computer", now)
    choices = visible["offers"]
    if not choices:
        return None
    side = visible["side"]
    if side == "red":
        rank = ("recon", "assess", "phish", "cloud_access",
                "escalate", "lateral", "fraud", "wait_red")
    else:
        rank = ("monitor", "patch", "segment", "investigate", "wait_blue")
    return min(choices, key=lambda o: (
        rank.index(o["action"]) if o["action"] in rank else 100,
        o["target"] or "", o["source"] or "",
    ))


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
            outcome["timeouts"] += max(0, state["version"] - previous - int(
                state["phase"] == "finished" and state["reason"].startswith("Match deadline")
            ) - int(state["players"].get(state["clock"]["active_side"], "") == "computer"
                  and outcome["bots"] > 0))
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
