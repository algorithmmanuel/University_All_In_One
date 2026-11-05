"""Authenticated V3 API, isolation, and worker persistence.

Uses real sessions, separate accounts, ordinary FastAPI dependencies and
isolated SQLite/PostgreSQL test databases, never the owner's saved matches.
"""
import os
import json
from uuid import uuid4
from datetime import datetime, timezone
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, delete, event, select
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database import Base
from auth import issue_session
from models import User, AuthSession, RedBlueV3Match, RedBlueV3Seat
import red_blue_v3_routes as routes
from cyber_warfare import v3_timeout_worker as worker


@pytest.fixture(params=("sqlite", "postgres"))
def arena(request, monkeypatch):
    monkeypatch.setenv("EDUCYBER_ENV", "development")
    if request.param == "postgres":
        url = os.getenv("TEST_DATABASE_URL")
        if not url:
            pytest.skip("Isolated PostgreSQL required")
        parsed = make_url(url)
        if (not parsed.drivername.startswith("postgresql")
                or parsed.database != "educyber_test"
                or parsed.host not in ("localhost", "127.0.0.1")
                or os.getenv("DATABASE_URL") != url):
            pytest.fail("Refusing non-isolated PostgreSQL")
        db_engine = create_engine(url)
    else:
        db_engine = create_engine("sqlite://", poolclass=StaticPool,
                                  connect_args={"check_same_thread": False})
        @event.listens_for(db_engine, "connect")
        def foreign_keys(connection, _):
            connection.execute("PRAGMA foreign_keys=ON")
    Base.metadata.create_all(db_engine)
    Session = sessionmaker(bind=db_engine, expire_on_commit=False)
    headers, ids = [], []
    for _ in range(2):
        with Session() as db:
            u = User(full_name="Synthetic V3 participant", email=uuid4().hex+"@example.invalid",
                     password_hash="disabled", role="student", age_band="adult",
                     is_active=True, is_approved=True)
            db.add(u); db.flush()
            ids.append(u.id)
            headers.append({"Authorization": "Bearer "+issue_session(db, u)})
    app = FastAPI(); app.include_router(routes.router)
    def test_db():
        with Session() as db:
            yield db
    app.dependency_overrides[routes.get_db] = test_db
    with TestClient(app) as client:
        yield client, headers, ids, Session
    with Session.begin() as db:
        db.execute(delete(RedBlueV3Match).where(RedBlueV3Match.creator_id.in_(ids)))
        db.execute(delete(AuthSession).where(AuthSession.user_id.in_(ids)))
        db.execute(delete(User).where(User.id.in_(ids)))
    db_engine.dispose()


def new_match(arena, mode="computer", side="blue"):
    client, headers, *_ = arena
    response = client.post("/api/v1/red-blue-v3/matches", headers=headers[0], json={
        "side": side, "mode": mode, "match_minutes": 30, "turn_seconds": 90,
    })
    assert response.status_code == 201, response.text
    return response.json()


def test_v3_requires_student_login_and_development_mode(arena, monkeypatch):
    client, headers, *_ = arena
    assert client.get("/api/v1/red-blue-v3/catalog").status_code == 401
    assert client.get("/api/v1/red-blue-v3/catalog", headers=headers[0]).status_code == 200
    monkeypatch.setenv("EDUCYBER_ENV", "beta")
    assert client.get("/api/v1/red-blue-v3/catalog", headers=headers[0]).status_code == 404
    assert client.post("/api/v1/red-blue-v3/matches", headers=headers[0], json={}).status_code == 404


def test_v3_computer_prep_and_worker_turns_are_account_scoped(arena):
    client, headers, ids, Session = arena
    match = new_match(arena)
    mid = match["id"]
    assert match["phase"] == "prepare"
    assert len(match["assets"]) == 16
    assert "seed" not in json.dumps(match)
    assert client.get(f"/api/v1/red-blue-v3/matches/{mid}", headers=headers[1]).status_code == 404
    p = client.post(f"/api/v1/red-blue-v3/matches/{mid}/prepare",
                    headers=headers[0], json={"control": "monitoring", "target": "teller"})
    assert p.status_code == 200
    ready = client.post(f"/api/v1/red-blue-v3/matches/{mid}/ready",
                        headers=headers[0], json={})
    assert ready.status_code == 200
    assert ready.json()["phase"] == "engage"
    with Session() as db:
        out = worker.process_due_once(db)
        assert out["examined"] == 1 and out["bots"] == 0
    live = client.get(f"/api/v1/red-blue-v3/matches/{mid}", headers=headers[0]).json()
    assert live["clock"]["active_side"] == "blue"
    cmd = client.post(f"/api/v1/red-blue-v3/matches/{mid}/commands",
                      headers=headers[0], json={
                        "command_id": str(uuid4()), "expected_sequence": 1,
                        "action": "wait_blue", "target": None, "source": None,
                      })
    assert cmd.status_code == 200, cmd.text
    with Session() as db:
        result = worker.process_due_once(db)
        assert result["bots"] == 1
    after = client.get(f"/api/v1/red-blue-v3/matches/{mid}", headers=headers[0]).json()
    assert after["clock"]["turn_sequence"] == 3
    assert "players" not in after and "red_known" not in after


def test_v3_distinct_accounts_invitation_and_role_secrecy(arena):
    client, h, *_ = arena
    original = new_match(arena, mode="human", side="blue")
    mid = original["id"]
    invite = client.post(f"/api/v1/red-blue-v3/matches/{mid}/invite", headers=h[0]).json()["token"]
    assert client.post("/api/v1/red-blue-v3/join", headers=h[0],
                       json={"token": invite}).status_code == 409
    joined = client.post("/api/v1/red-blue-v3/join", headers=h[1],
                         json={"token": invite})
    assert joined.status_code == 200, joined.text
    red = joined.json()
    assert len(red["assets"]) == 2 and "ledger" not in json.dumps(red)
    assert client.post("/api/v1/red-blue-v3/join", headers=h[1],
                       json={"token": invite}).status_code == 404
    one = client.post(f"/api/v1/red-blue-v3/matches/{mid}/ready", headers=h[0], json={})
    assert one.status_code == 200 and one.json()["phase"] == "prepare"
    two = client.post(f"/api/v1/red-blue-v3/matches/{mid}/ready", headers=h[1], json={})
    assert two.status_code == 200 and two.json()["phase"] == "engage"
    assert two.json()["clock"]["active_side"] == "blue"
    command = {"command_id": str(uuid4()), "expected_sequence": 1,
               "action": "wait_blue", "target": None, "source": None}
    assert client.post(f"/api/v1/red-blue-v3/matches/{mid}/commands", headers=h[1],
                       json=command).status_code == 409
    assert client.post(f"/api/v1/red-blue-v3/matches/{mid}/commands", headers=h[0],
                       json=command).status_code == 200
    command = {"command_id": str(uuid4()), "expected_sequence": 2,
               "action": "recon", "target": "teller", "source": None}
    moved = client.post(f"/api/v1/red-blue-v3/matches/{mid}/commands",
                        headers=h[1], json=command)
    assert moved.status_code == 200, moved.text
    assert "identity" in [a["id"] for a in moved.json()["assets"]]
    assert "ledger" not in [a["id"] for a in moved.json()["assets"]]
    assert "seed" not in json.dumps(moved.json())
    assert "monitoring" not in json.dumps(moved.json())


def test_v3_worker_reconciles_expired_match_once(arena):
    client, h, ids, Session = arena
    match = new_match(arena)
    mid = match["id"]
    client.post(f"/api/v1/red-blue-v3/matches/{mid}/ready", headers=h[0], json={})
    with Session() as db:
        row = db.get(RedBlueV3Match, mid)
        state = dict(row.transcript)
        from copy import deepcopy
        state = deepcopy(state)
        deadline = state["clock"]["match_deadline_at"]
        result = worker.process_due_once(db, deadline)
        assert result["finished"] == 1
    with Session() as db:
        assert db.get(RedBlueV3Match, mid).status == "finished"
        assert worker.process_due_once(db, deadline)["finished"] == 0
    final = client.get(f"/api/v1/red-blue-v3/matches/{mid}", headers=h[0]).json()
    assert final["winner"] == "blue"


def test_v3_isolated_schema_additive_migration_round_trip():
    import importlib.util
    from pathlib import Path
    from alembic.migration import MigrationContext
    from alembic.operations import Operations
    from sqlalchemy import inspect, text
    path = Path(__file__).parent / "migrations/versions/0014_red_blue_v3_pilot.py"
    spec = importlib.util.spec_from_file_location("v3_migration", path)
    migration = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migration)
    engine = create_engine("sqlite://")
    with engine.begin() as connection:
        connection.execute(text("CREATE TABLE users(id INTEGER PRIMARY KEY)"))
        connection.execute(text("CREATE TABLE red_blue_matches(id INTEGER PRIMARY KEY, saved TEXT)"))
        connection.execute(text("INSERT INTO red_blue_matches VALUES(1,'preserved')"))
        before = set(inspect(connection).get_table_names())
        with Operations.context(MigrationContext.configure(connection)):
            migration.upgrade()
        assert set(inspect(connection).get_table_names()) - before == {
            "red_blue_v3_matches", "red_blue_v3_seats"}
        assert connection.execute(text("SELECT saved FROM red_blue_matches")).scalar_one() == "preserved"
        with Operations.context(MigrationContext.configure(connection)):
            migration.downgrade()
        assert set(inspect(connection).get_table_names()) == before
    engine.dispose()
