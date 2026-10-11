"""PostgreSQL-backed, atomic login attempt limiting.

One bucket per normalized account identifier. This protects accounts across
multiple API instances; add trusted-proxy IP limits at the deployment edge.
"""
import hashlib
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import insert
from models import LoginAttemptBucket

WINDOW = timedelta(minutes=5)
MAX_ATTEMPTS = 10


def record_attempt(db, email: str) -> None:
    """Atomically count login requests, including unknown accounts.

    PostgreSQL ON CONFLICT serializes updates to a bucket across workers.
    The current request is blocked when it exceeds the permitted attempts.
    """
    key = hashlib.sha256(email.strip().lower().encode("utf-8")).hexdigest()
    now = datetime.now(timezone.utc)
    stmt = insert(LoginAttemptBucket).values(
        key_hash=key, attempts=1, window_start=now
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=[LoginAttemptBucket.key_hash],
        set_={
            "attempts": (
                # Restart the counter once the prior window has expired.
                __import__("sqlalchemy").case(
                    (LoginAttemptBucket.window_start <= now - WINDOW, 1),
                    else_=LoginAttemptBucket.attempts + 1,
                )
            ),
            "window_start": __import__("sqlalchemy").case(
                (LoginAttemptBucket.window_start <= now - WINDOW, now),
                else_=LoginAttemptBucket.window_start,
            ),
        },
    ).returning(LoginAttemptBucket.attempts)
    count = db.scalar(stmt)
    db.commit()
    if count > MAX_ATTEMPTS:
        raise HTTPException(
            status_code=429,
            detail="Too many login attempts; please try again later",
            headers={"Retry-After": "300"},
        )


def clear_attempts(db, email: str) -> None:
    """Remove a successful account's bucket after a completed login."""
    from sqlalchemy import delete
    key = hashlib.sha256(email.strip().lower().encode("utf-8")).hexdigest()
    db.execute(delete(LoginAttemptBucket).where(LoginAttemptBucket.key_hash == key))
    db.commit()
