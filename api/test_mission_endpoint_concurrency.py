"""HTTP-level concurrency regression for the real mission decision route.

Requires an isolated localhost PostgreSQL database named educyber_test.
Never run against the application's development database.
"""
import os
import uuid
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import pytest


@pytest.mark.integration
def test_mission_decision_endpoint_rejects_duplicate_concurrent_step():
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.skip("TEST_DATABASE_URL is required for PostgreSQL integration tests")

    from sqlalchemy.engine import make_url
    parsed = make_url(url)
    if (not parsed.drivername.startswith("postgresql")
            or parsed.database != "educyber_test"
            or parsed.host not in ("127.0.0.1", "localhost")):
        pytest.fail("Refusing to run outside local PostgreSQL educyber_test")
    existing = os.environ.get("DATABASE_URL")
    if existing and existing != url:
        pytest.fail("DATABASE_URL differs from TEST_DATABASE_URL")
    os.environ["DATABASE_URL"] = url

    pytest.importorskip("httpx", reason="FastAPI TestClient requires httpx")
    from fastapi.testclient import TestClient
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from auth import current_user
    from database import Base
    from main import app
    from mission_data import MISSIONS
    from mission_routes import get_db as mission_get_db
    from models import MissionRun, User

    engine = create_engine(url, pool_pre_ping=True)
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    Base.metadata.create_all(engine)
    mission_id = next(iter(MISSIONS))
    with Session.begin() as db:
        user = User(full_name="API Concurrency Test",
                    email=f"phase8-{uuid.uuid4().hex}@example.invalid",
                    password_hash="test-only", role="student",
                    is_active=True, is_approved=True)
        db.add(user)
        db.flush()
        user_id = user.id
        run = MissionRun(user_id=user_id, mission_id=mission_id,
                         step_index=0, score=0, choices=[])
        db.add(run)
        db.flush()
        run_id = run.id

    def test_db():
        with Session() as db:
            yield db

    def test_user():
        with Session() as db:
            user = db.get(User, user_id)
            db.expunge(user)
            return user

    app.dependency_overrides[mission_get_db] = test_db
    app.dependency_overrides[current_user] = test_user
    barrier = Barrier(2)

    def submit():
        with TestClient(app) as client:
            barrier.wait(timeout=10)
            return client.post(
                f"/api/v1/missions/runs/{run_id}/decide",
                json={"option_index": 0, "expected_step": 0},
            )

    try:
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(submit) for _ in range(2)]
            responses = [future.result(timeout=20) for future in futures]
        assert sorted(response.status_code for response in responses) == [200, 409]
        with Session() as db:
            saved = db.get(MissionRun, run_id)
            assert saved.step_index == 1
            assert len(saved.choices) == 1
            assert saved.score == saved.choices[0]["points"]
    finally:
        app.dependency_overrides.pop(mission_get_db, None)
        app.dependency_overrides.pop(current_user, None)
        with Session.begin() as db:
            db.query(MissionRun).filter(MissionRun.id == run_id).delete()
            db.query(User).filter(User.id == user_id).delete()
        engine.dispose()
