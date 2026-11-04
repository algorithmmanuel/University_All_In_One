"""Independent V2 deadline worker core: durable JSON snapshot + PG row locks.

No HTTP request, browser poll or user time is required. This is a development
building block, not a production scheduler. A future supervised process must
invoke it periodically with the isolated, validated database configuration.
"""
import time

from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from models import RedBlueMatch
from cyber_warfare import v2_timed, v2_alternating
from cyber_warfare.opponent import choose_order


MAX_DUE_BATCH = 50


def process_due_once(db: Session, server_now: int | None = None):
    """Atomically reconcile due matches in an existing database transaction.

    The SELECT FOR UPDATE SKIP LOCKED lock protects against duplicate server
    workers on PostgreSQL. SQLite can exercise sequential logic but does not
    establish concurrent lock safety. Persisting a grace and making a timeout
    move are handled in the SAME transaction.
    """
    now = int(time.time()) if server_now is None else server_now
    if type(now) is not int or now < 0:
        raise ValueError("Invalid trusted server time")
    transcript = RedBlueMatch.transcript
    side = transcript["clock"]["active_side"].as_string()
    is_bot_turn = or_(
        and_(side == "red", transcript["game"]["seats"]["red"].as_string() == "computer"),
        and_(side == "blue", transcript["game"]["seats"]["blue"].as_string() == "computer"),
    )
    due = (
        select(RedBlueMatch)
        .where(
            RedBlueMatch.status == "active",
            transcript["edition"].as_string() == v2_timed.TIMED_EDITION,
            or_(transcript["clock"]["deadline_at"].as_integer() <= now, is_bot_turn),
        )
        .order_by(RedBlueMatch.id)
        .limit(MAX_DUE_BATCH)
    )
    if db.bind is not None and db.bind.dialect.name == "postgresql":
        due = due.with_for_update(skip_locked=True)
    rows = db.scalars(due).all()
    outcome = {"processed": 0, "passes": 0, "graces": 0, "finished": 0, "bots": 0}
    try:
        for row in rows:
            # Damaged or unsupported private checkpoints fail CLOSED. The
            # transaction is rolled back; no partially applied timeout.
            state = v2_timed.restore_snapshot(row.transcript)
            if not isinstance(state, v2_timed.TimedMatch):
                raise ValueError("Active timed match cannot be terminal")
            owners = state.match.private.seats
            current_actor = owners[state.match.active_side]
            if current_actor == "computer" and now < state.clock.deadline_at:
                # Authoritative bot uses ONLY the computer seat projection;
                # never read its opponent's private decisions.
                action = choose_order(
                    v2_alternating.view(state.match, "computer"),
                    row.difficulty,
                )
                updated = v2_timed.act(
                    state, "computer", action,
                    f"computer-{state.match.round}-{state.match.active_side}", now,
                )
                passed = False
                outcome["bots"] += 1
            else:
                humans = frozenset(side for side, actor in owners.items()
                                   if actor.startswith("user:"))
                updated, passed = v2_timed.settle(state, now, humans)
            outcome["processed"] += 1
            if passed:
                outcome["passes"] += 1
            if isinstance(updated, v2_timed.TimedMatch):
                if updated.clock.grace_used != state.clock.grace_used:
                    outcome["graces"] += 1
                row.transcript = v2_timed.export_snapshot(updated)
            else:
                row.transcript = v2_timed.export_terminal(updated)
                row.status = "finished"
                outcome["finished"] += 1
        db.commit()
    except Exception:
        db.rollback()
        raise
    return outcome
