"""PostgreSQL integration regression for concurrent mission decisions.

Run only against a disposable PostgreSQL database: tests create and delete rows.
Set TEST_DATABASE_URL to a separate database, never the development database.
"""
import os
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

from mission_data import MISSIONS


@pytest.mark.integration
def test_concurrent_mission_decisions_are_serialized():
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.skip("Set TEST_DATABASE_URL to an isolated PostgreSQL test database")
    parsed_url = make_url(url)
    if not parsed_url.drivername.startswith("postgresql"):
        pytest.fail("Concurrency test requires PostgreSQL")
    if parsed_url.database != "educyber_test":
        pytest.fail("Refusing to run: TEST_DATABASE_URL must target educyber_test")
    if parsed_url.host not in ("localhost", "127.0.0.1"):
        pytest.fail("Refusing to run: test database must be on localhost")
    # Import database-bound models only after the test database is explicitly configured.
    # database.py requires DATABASE_URL at import time; avoid collection-time failure.
    previous_url = os.environ.get("DATABASE_URL")
    if previous_url and previous_url != url:
        pytest.fail("DATABASE_URL differs from TEST_DATABASE_URL; refusing to risk the application database")
    os.environ["DATABASE_URL"] = url
    from models import Base, MissionRun, User
    engine = create_engine(url, pool_size=5, max_overflow=5)
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    Base.metadata.create_all(engine)
    with Session.begin() as db:
        user = User(full_name="Concurrency Test", email="phase8-concurrency@example.invalid",
                    password_hash="not-a-real-password", role="student", is_active=True,
                    is_approved=True)
        db.add(user)
        db.flush()
        user_id = user.id
        mission_id = next(iter(MISSIONS))
        run = MissionRun(user_id=user_id, mission_id=mission_id,
                         step_index=0, score=0, choices=[])
        db.add(run)
        db.flush()
        run_id = run.id

    barrier = Barrier(2)

    def advance():
        # Mirror the transaction and lock contract of the mission decision endpoint.
        with Session.begin() as db:
            barrier.wait(timeout=10)
            run = db.scalar(select(MissionRun).where(
                MissionRun.id == run_id, MissionRun.user_id == user_id
            ).with_for_update())
            if run.step_index != 0:
                return "conflict"
            run.step_index += 1
            run.score += 10
            run.choices = [*run.choices, {"step": 0, "points": 10}]
            return "advanced"

    try:
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(advance) for _ in range(2)]
            outcomes = [f.result(timeout=20) for f in futures]
        assert sorted(outcomes) == ["advanced", "conflict"]
        with Session() as db:
            saved = db.get(MissionRun, run_id)
            assert saved.step_index == 1
            assert saved.score == 10
            assert len(saved.choices) == 1
    finally:
        with Session.begin() as db:
            db.query(MissionRun).filter(MissionRun.id == run_id).delete()
            db.query(User).filter(User.id == user_id).delete()
        engine.dispose()
