"""Test edition-aware application adapter without changing the live API."""
import json
from copy import deepcopy

import pytest

from cyber_warfare import engine, v2_alternating as alternate
from cyber_warfare import v2_session as session
from cyber_warfare.scenario import list_scenarios


@pytest.fixture
def scenario():
    return list_scenarios()[0]


def test_legacy_dispatch_unchanged(scenario):
    old = engine.new_match(scenario, "legacy-dispatch", "red", "blue")
    record = json.loads(json.dumps(engine.export_replay(old)))
    restored = session.restore(record)
    assert not isinstance(restored, alternate.AlternateMatch)
    assert session.export(restored) == record
    assert session.view(restored, "blue") == engine.view(old, "blue")
    with pytest.raises(ValueError):
        session.restore({"edition": "evil", **record})


def test_v2_dispatch_has_new_edition_and_no_private_truth(scenario):
    new = alternate.new_match(scenario, "v2-dispatch", "red", "blue")
    saved = json.loads(json.dumps(session.export(new)))
    restored = session.restore(saved)
    assert isinstance(restored, alternate.AlternateMatch)
    assert session.export(restored) == saved
    blue = session.view(restored, "blue")
    red = session.view(restored, "red")
    assert blue["active_side"] == "blue"
    assert red["committed"] is True
    assert session.orders(restored, "red") == []
    for observation in (blue, red):
        for private_key in ("seed", "plans", "timeline", "receipts", "moves", "rules_digest"):
            assert private_key not in observation
    with pytest.raises(PermissionError):
        session.view(restored, "intruder")


def test_join_is_immutable_and_only_allows_open_seat(scenario):
    waiting = alternate.new_match(scenario, "waiting", "open", "user:100")
    joined = session.join(waiting, "red", "user:200")
    assert session.seats(waiting)["red"] == "open"
    assert session.seats(joined)["red"] == "user:200"
    assert session.restore(json.loads(json.dumps(session.export(joined)))).private.seats["red"] == "user:200"
    with pytest.raises(ValueError):
        session.join(joined, "blue", "user:200")
    with pytest.raises(ValueError):
        session.join(joined, "red", "user:300")


def test_computer_blue_opens_and_computer_red_responds(scenario):
    red_human = alternate.new_match(scenario, "bot-blue", "human", "computer")
    opening = session.advance_computer(red_human, "standard")
    assert opening.active_side == "red" and opening.round == 1
    assert len(opening.moves) == 1 and opening.moves[0]["side"] == "blue"
    red = session.submit_alternating(opening, "human", engine.Order("wait_red"),
                                     1, "red1", "standard")
    assert red.active_side == "red" and red.round == 2
    assert len(red.moves) == 3
    assert red.moves[-1]["side"] == "blue"
    assert session.export(session.restore(session.export(red))) == session.export(red)
    blue_human = alternate.new_match(scenario, "bot-red", "computer", "human")
    after = session.submit_alternating(blue_human, "human", engine.Order("wait_blue"),
                                       1, "blue1", "easy")
    assert after.round == 2 and after.active_side == "blue"
    assert [item["side"] for item in after.moves] == ["blue", "red"]


def test_duplicate_retry_after_bot_does_not_replay_bot(scenario):
    match = alternate.new_match(scenario, "bot-retry", "computer", "human")
    result = session.submit_alternating(match, "human", engine.Order("wait_blue"),
                                        1, "safe-id", "hard")
    retry = session.submit_alternating(result, "human", engine.Order("wait_blue"),
                                       1, "safe-id", "hard")
    assert session.export(retry) == session.export(result)
    assert len(retry.moves) == 2
    with pytest.raises(ValueError):
        session.submit_alternating(result, "human", engine.Order("wait_blue"),
                                   1, "different-id", "hard")


def test_versioned_completed_match_debrief_is_sanitized(scenario):
    match = alternate.new_match(scenario, "finished", "human-red", "human-blue")
    for round_no in range(1, scenario.turn_limit + 1):
        match = session.submit_alternating(match, "human-blue", engine.Order("wait_blue"),
                                           round_no, f"b-{round_no}", "easy")
        match = session.submit_alternating(match, "human-red", engine.Order("wait_red"),
                                           round_no, f"r-{round_no}", "easy")
    report = session.debrief(match, "human-red")
    assert report["winner"] == "blue"
    assert report["timeline"] and 1 <= len(report["pivotal"]) <= 5
    assert all(len(item["alternatives"]) <= 2 for item in report["pivotal"])
    assert {item["side"] for item in report["pivotal"]} <= {"red", "blue"}
    assert "seed" not in json.dumps(report) and "roll" not in json.dumps(report)
    with pytest.raises(PermissionError):
        session.debrief(match, "intruder")


def test_v2_debrief_is_role_aware_bounded_and_deterministic(scenario):
    match = alternate.new_match(scenario, "postmatch-learning", "red-human", "blue-human")
    for round_no in range(1, scenario.turn_limit + 1):
        match = alternate.commit(match, "blue-human",
                                 engine.Order("monitor", scenario.assets[0].id)
                                 if round_no == 1 else engine.Order("wait_blue"),
                                 round_no, f"blue-{round_no}")
        match = alternate.commit(match, "red-human", engine.Order("wait_red"),
                                 round_no, f"red-{round_no}")
        if match.winner:
            break
    blue = session.debrief(match, "blue-human")
    red = session.debrief(match, "red-human")
    for report in (blue, red):
        assert 1 <= len(report["pivotal"]) <= 5
        assert len(report["alternatives"]) <= 10
        assert all(item["side"] in ("red", "blue") for item in report["pivotal"])
        assert all(len(item["alternatives"]) <= 2 for item in report["pivotal"])
        assert "seed" not in json.dumps(report)
        assert "roll" not in json.dumps(report)
    assert session.debrief(session.restore(session.export(match)), "blue-human") == blue
    with pytest.raises(PermissionError):
        session.debrief(match, "outsider")
