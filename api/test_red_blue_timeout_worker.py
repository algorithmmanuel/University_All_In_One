"""Deadline worker against real SQLAlchemy storage, SQLite and isolated PG.

The imported arena fixture includes authentic user rows and the normal schema.
PostgreSQL proves row-lock execution; SQLite covers sequential semantics.
"""
import json

from test_red_blue_api import arena  # pytest fixture
from models import RedBlueMatch
from cyber_warfare import engine, v2_alternating, v2_timed
from cyber_warfare import v2_timeout_worker as worker
from cyber_warfare.scenario import load_scenario


def insert(arena, state, status="active"):
    _, _, ids, Session, *_ = arena
    with Session.begin() as db:
        row = RedBlueMatch(
            creator_id=ids[0],
            transcript=json.loads(json.dumps(state)),
            difficulty="standard", status=status)
        db.add(row)
        db.flush()
        return row.id


def test_worker_passes_expired_v2_without_touching_legacy(arena):
    _, _, ids, Session, *_ = arena
    scenario = load_scenario("microfinance")
    live = v2_timed.start(
        v2_alternating.new_match(scenario, "worker-blue", "user:111", "user:222"),
        1000)
    match_id = insert(arena, v2_timed.export_snapshot(live))
    legacy = engine.new_match(scenario, "legacy", "user:111", "user:222")
    legacy_record = engine.export_replay(legacy)
    old_id = insert(arena, legacy_record)
    with Session() as db:
        result = worker.process_due_once(db, 1090)
    assert result["passes"] == 1 and result["processed"] == 1
    with Session() as db:
        row = db.get(RedBlueMatch, match_id)
        next_state = v2_timed.restore_snapshot(row.transcript)
        assert next_state.match.active_side == "red"
        assert next_state.clock.deadline_at == 1180
        assert next_state.match.moves[0]["action"] == "wait_blue"
        assert db.get(RedBlueMatch, old_id).transcript == legacy_record
        assert db.get(RedBlueMatch, old_id).status == "active"
        again = worker.process_due_once(db, 1090)
        assert again["passes"] == 0


def test_worker_persists_grace_and_never_repeats_same_extension(arena):
    _, _, _, Session, *_ = arena
    scenario = load_scenario("microfinance")
    state = v2_timed.start(
        v2_alternating.new_match(scenario, "worker-grace", "user:111", "user:222"),
        1000)
    state = v2_timed.seat_heartbeat(state, "user:222", 1010)
    match_id = insert(arena, v2_timed.export_snapshot(state))
    with Session() as db:
        first = worker.process_due_once(db, 1090)
        assert first == {"processed": 1, "passes": 0, "graces": 1, "finished": 0}
        second = worker.process_due_once(db, 1090)
        assert second["processed"] == 0
    with Session() as db:
        saved = v2_timed.restore_snapshot(db.get(RedBlueMatch, match_id).transcript)
        assert saved.clock.grace_active and saved.clock.deadline_at == 1120
        assert saved.clock.grace_used == frozenset({"blue"})
        third = worker.process_due_once(db, 1120)
        assert third["passes"] == 1
        restored = v2_timed.restore_snapshot(db.get(RedBlueMatch, match_id).transcript)
        assert restored.clock.grace_used == frozenset({"blue"})


def test_worker_finalises_at_scenario_limit(arena):
    _, _, _, Session, *_ = arena
    scenario = load_scenario("microfinance")
    game = v2_alternating.new_match(scenario, "finished", "user:111", "user:222")
    for i in range(1, scenario.turn_limit + 1):
        game = v2_alternating.commit(game, "user:222", engine.Order("wait_blue"),
                                     i, f"blue-{i}")
        if i < scenario.turn_limit:
            game = v2_alternating.commit(game, "user:111", engine.Order("wait_red"),
                                         i, f"red-{i}")
    # At the last round, Red has yet to act; the worker's automatic pass finishes.
    state = v2_timed.start(game, 1000)
    assert state.match.active_side == "red"
    match_id = insert(arena, v2_timed.export_snapshot(state))
    with Session() as db:
        result = worker.process_due_once(db, 1090)
        assert result["finished"] == 1 and result["passes"] == 1
        row = db.get(RedBlueMatch, match_id)
        assert row.status == "finished"
        final = v2_timed.restore_snapshot(row.transcript)
        assert final.winner == "blue"
        assert row.transcript["clock"] is None
