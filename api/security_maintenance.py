"""Explicit maintenance routines for expired authentication records.

Call from a scheduled worker or an operations job, not on each request.
Both functions are database-portable SQLAlchemy operations.
"""
from datetime import datetime, timedelta, timezone

from sqlalchemy import delete

from models import AuthSession, LoginAttemptBucket

LOGIN_BUCKET_RETENTION = timedelta(days=1)


def purge_expired_auth_records(db, *, now=None) -> tuple[int, int]:
    """Delete expired sessions and stale login buckets in one transaction.

    The caller supplies a dedicated database session and controls scheduling.
    No user accounts or active sessions are removed.
    """
    current = now if now is not None else datetime.now(timezone.utc)
    sessions = db.execute(
        delete(AuthSession).where(AuthSession.expires_at < current)
    ).rowcount
    buckets = db.execute(
        delete(LoginAttemptBucket).where(
            LoginAttemptBucket.window_start < current - LOGIN_BUCKET_RETENTION
        )
    ).rowcount
    db.commit()
    return sessions, buckets
