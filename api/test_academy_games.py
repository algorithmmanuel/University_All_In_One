"""Cyber Academy defensive game contract checks."""
from game_catalog import game_catalog
from mission_contract import build_manifest
from mission_data import MISSIONS
from mission_routes import public_step


def test_academy_has_ten_distinct_playable_games():
    games = [game for game in game_catalog()["games"] if game["pathway"] == "university"]
    assert len(games) == 10
    assert len({game["id"] for game in games}) == 10
    assert all(game["status"] == "playable" for game in games)


def test_academy_scoring_answers_never_leak_in_public_steps():
    ids = ("network-watch", "web-defense", "cloud-perimeter", "forensics-desk",
           "malware-clues", "identity-lab", "secure-code-review", "threat-hunter")
    for mission_id in ids:
        mission = MISSIONS[mission_id]
        manifest = build_manifest(mission_id)
        assert manifest.pathway == "university"
        assert manifest.step_count == 3
        assert manifest.max_score == 45
        assert len(mission["finding_key"]) == 3
        for index, stage in enumerate(mission["steps"]):
            safe = public_step(stage)
            assert set(safe) == {"scene", "story", "evidence", "question", "options"}
            assert len(safe["options"]) == 3
            assert all(isinstance(option, str) for option in safe["options"])
            assert sorted(option["points"] for option in stage["options"]) == [0, 0, 10]
            assert 0 <= mission["finding_key"][index] < len(safe["evidence"])
            assert "finding_key" not in safe
            assert "feedback" not in safe
            assert "points" not in safe


def test_no_games_remain_planned():
    planned = [game for game in game_catalog()["games"] if game["status"] == "planned"]
    assert len(planned) == 0
    assert all(game["pathway"] == "professional" for game in planned)
