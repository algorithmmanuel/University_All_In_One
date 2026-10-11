"""Isolated PostgreSQL checks for registration throttling and retention."""
import hashlib
import os
import uuid
from datetime import datetime, timedelta, timezone

import pytest


@pytest.mark.integration
def test_registration_throttle_and_retention_cleanup():
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.skip("TEST_DATABASE_URL is required")
    from sqlalchemy.engine import make_url
    parsed = make_url(url)
    if (not parsed.drivername.startswith("postgresql")
            or parsed.database != "educyber_test"
            or parsed.host not in ("localhost", "127.0.0.1")
            or os.getenv("DATABASE_URL") not in (None, url)):
        pytest.fail("Requires isolated localhost educyber_test")
    os.environ["DATABASE_URL"] = url
    from fastapi import HTTPException
    from sqlalchemy import create_engine, delete
    from sqlalchemy.orm import sessionmaker
    from database import Base
    from login_limiter import REGISTRATION_MAX_ATTEMPTS, record_attempt
    from models import LoginAttemptBucket
    from security_maintenance import purge_expired_auth_records

    engine = create_engine(url)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    email = f"phase8-registration-{uuid.uuid4().hex}@example.com"
    key = hashlib.sha256(("registration:" + email).encode()).hexdigest()
    try:
        with Session() as db:
            for _ in range(REGISTRATION_MAX_ATTEMPTS):
                record_attempt(db, email, purpose="registration")
            with pytest.raises(HTTPException) as error:
                record_attempt(db, email, purpose="registration")
            assert error.value.status_code == 429
            bucket = db.get(LoginAttemptBucket, key)
            assert bucket.attempts == REGISTRATION_MAX_ATTEMPTS + 1
            bucket.window_start = datetime.now(timezone.utc) - timedelta(days=2)
            db.commit()
            sessions_deleted, buckets_deleted = purge_expired_auth_records(db)
            assert sessions_deleted >= 0
            assert buckets_deleted >= 1
            assert db.get(LoginAttemptBucket, key) is None
    finally:
        with Session.begin() as db:
            db.execute(delete(LoginAttemptBucket).where(LoginAttemptBucket.key_hash == key))
        engine.dispose()
