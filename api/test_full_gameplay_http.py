"""Integration: every game can be started, advanced and completed over HTTP.

Requires an isolated localhost PostgreSQL database named educyber_test.
"""
import os
import uuid
import pytest

@pytest.mark.integration
def test_thirty_game_http_journeys():
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.skip("TEST_DATABASE_URL is required")
    from sqlalchemy.engine import make_url
    parsed = make_url(url)
    if (not parsed.drivername.startswith("postgresql") or
        parsed.database != "educyber_test" or
        parsed.host not in ("localhost", "127.0.0.1") or
        os.getenv("DATABASE_URL") not in (None, url)):
        pytest.fail("Only isolated localhost educyber_test is permitted")
    os.environ["DATABASE_URL"] = url
    pytest.importorskip("httpx")
    from fastapi.testclient import TestClient
    from sqlalchemy import create_engine, delete, select
    from sqlalchemy.orm import sessionmaker
    from auth import issue_session
    from database import Base
    from game_catalog import game_catalog
    from main import app
    from models import AuthSession, MissionRun, User

    engine = create_engine(url)
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    Base.metadata.create_all(engine)
    user_id = None
    try:
        with Session.begin() as db:
            user = User(full_name="Gameplay Integration Test",
                email=f"phase10-{uuid.uuid4().hex}@example.invalid",
                password_hash="test-only", role="student",
                is_active=True, is_approved=True)
            db.add(user)
            db.flush()
            user_id = user.id
        with Session() as db:
            token = issue_session(db, db.get(User, user_id))
        headers = {"Authorization": f"Bearer {token}"}
        games = game_catalog()["games"]
        assert len(games) == 30
        with TestClient(app) as client:
            for game in games:
                assert game["status"] == "playable"
                started = client.post(
                    f"/api/v1/missions/{game['mission_ids'][0]}/start",
                    headers=headers)
                assert started.status_code == 201
                state = started.json()
                run_id = state["run_id"]
                for stage in range(3):
                    assert client.get(
                        f"/api/v1/missions/runs/{run_id}",
                        headers=headers).json()["score"] == state["score"]
                    response = client.post(
                        f"/api/v1/missions/runs/{run_id}/decide",
                        headers=headers,
                        json={"option_index": 0, "finding_index": 0,
                              "expected_step": stage})
                    assert response.status_code == 200, response.text
                    state = response.json()
                    assert state["step_index"] == stage + 1
                    assert client.post(
                        f"/api/v1/missions/runs/{run_id}/decide",
                        headers=headers,
                        json={"option_index": 0, "finding_index": 0,
                              "expected_step": stage}).status_code == 409
                assert state["completed"] and 0 <= state["score"] <= 45
        with Session() as db:
            runs = db.scalars(select(MissionRun).where(
                MissionRun.user_id == user_id)).all()
            assert len(runs) == 30
            assert all(r.step_index == 3 and len(r.choices) == 3 for r in runs)
    finally:
        if user_id is not None:
            with Session.begin() as db:
                db.execute(delete(MissionRun).where(MissionRun.user_id == user_id))
                db.execute(delete(AuthSession).where(AuthSession.user_id == user_id))
                db.execute(delete(User).where(User.id == user_id))
        engine.dispose()
