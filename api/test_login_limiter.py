"""PostgreSQL integration coverage for shared login attempt throttling."""
import os
import uuid
from concurrent.futures import ThreadPoolExecutor

import pytest


@pytest.mark.integration
def test_shared_login_throttle_and_window_reset():
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.skip("Requires TEST_DATABASE_URL")
    from sqlalchemy.engine import make_url
    parsed = make_url(url)
    if (not parsed.drivername.startswith("postgresql")
            or parsed.database != "educyber_test"
            or parsed.host not in ("localhost", "127.0.0.1")
            or os.getenv("DATABASE_URL") not in (None, url)):
        pytest.fail("Refusing to use a non-isolated test database")
    os.environ["DATABASE_URL"] = url

    from fastapi import HTTPException
    from sqlalchemy import create_engine, delete
    from sqlalchemy.orm import sessionmaker
    from database import Base
    from login_limiter import MAX_ATTEMPTS, record_attempt
    from models import LoginAttemptBucket

    engine = create_engine(url)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    email = f"limit-{uuid.uuid4().hex}@example.com"
    import hashlib
    key = hashlib.sha256(email.encode()).hexdigest()

    def attempt():
        with Session() as db:
            try:
                record_attempt(db, email)
                return 200
            except HTTPException as exc:
                return exc.status_code

    try:
        with ThreadPoolExecutor(max_workers=5) as pool:
            statuses = list(pool.map(lambda _: attempt(), range(MAX_ATTEMPTS + 3)))
        assert statuses.count(200) == MAX_ATTEMPTS
        assert statuses.count(429) == 3
        with Session() as db:
            bucket = db.get(LoginAttemptBucket, key)
            assert bucket.attempts == MAX_ATTEMPTS + 3
    finally:
        with Session.begin() as db:
            db.execute(delete(LoginAttemptBucket).where(LoginAttemptBucket.key_hash == key))
        engine.dispose()
