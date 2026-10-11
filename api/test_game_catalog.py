from game_catalog import game_catalog
from mission_data import MISSIONS
from mission_contract import build_manifest


def test_exactly_ten_games_per_pathway():
    catalog = game_catalog()
    assert catalog["version"] == 5
    assert len(catalog["games"]) == 30
    for pathway in catalog["pathways"]:
        games = [game for game in catalog["games"] if game["pathway"] == pathway]
        assert len(games) == 10
        assert len({game["id"] for game in games}) == 10


def test_game_status_matches_playability_and_valid_missions():
    games = game_catalog()["games"]
    assert len({game["id"] for game in games}) == len(games)
    for game in games:
        if game["status"] == "planned":
            assert game["mission_ids"] == []
            assert game["mission_count"] == 0
        else:
            assert game["status"] == "playable"
            assert game["mission_count"] == len(game["mission_ids"]) > 0
            for mission_id in game["mission_ids"]:
                assert mission_id in MISSIONS
                assert build_manifest(mission_id).pathway == game["pathway"]


def test_existing_game_ids_remain_playable():
    games = {game["id"]: game for game in game_catalog()["games"]}
    for game_id in ("scholarship-detective", "password-fortress",
                    "midnight-alerts", "operation-firewall", "branch-resilience"):
        assert games[game_id]["status"] == "playable"


def test_password_fortress_three_stages():
    mission = MISSIONS["password-fortress"]
    assert len(mission["steps"]) == 3
    assert all(len(s["options"]) >= 2 and s["evidence"] for s in mission["steps"])


def test_all_ten_explorer_games_are_playable():
    games = [g for g in game_catalog()["games"] if g["pathway"] == "secondary"]
    assert len(games) == 10
    assert all(g["status"] == "playable" and g["mission_count"] == 1 for g in games)
    assert len([g for g in game_catalog()["games"] if g["status"] == "planned"]) == 0


def test_new_explorer_missions_have_three_distinct_scored_stages():
    new_ids = ("privacy-patrol", "scam-spotter", "safe-social", "device-defender",
               "wifi-wise", "digital-footprints", "mfa-guardian", "backup-buddy")
    for mission_id in new_ids:
        mission = MISSIONS[mission_id]
        assert len(mission["steps"]) == len(mission["finding_key"]) == 3
        assert len({step["scene"] for step in mission["steps"]}) == 3
        for stage, step in enumerate(mission["steps"]):
            assert len(step["evidence"]) == len(step["options"]) == 3
            assert 0 <= mission["finding_key"][stage] < len(step["evidence"])
            assert sorted(option["points"] for option in step["options"]) == [0, 0, 10]
            assert all(option["feedback"] for option in step["options"])
            assert all(option["text"] for option in step["options"])
        assert build_manifest(mission_id).max_score == 45


def test_all_ten_academy_games_are_playable():
    games = [game for game in game_catalog()["games"] if game["pathway"] == "university"]
    assert len(games) == 10
    assert all(game["status"] == "playable" and game["mission_count"] == 1 for game in games)
    assert len([game for game in game_catalog()["games"] if game["status"] == "planned"]) == 0


def test_new_academy_missions_are_complete_and_server_scored():
    ids = ("network-watch", "web-defense", "cloud-perimeter", "forensics-desk",
           "malware-clues", "identity-lab", "secure-code-review", "threat-hunter")
    for mission_id in ids:
        mission = MISSIONS[mission_id]
        assert len(mission["steps"]) == len(mission["finding_key"]) == 3
        assert len({stage["scene"] for stage in mission["steps"]}) == 3
        for index, stage in enumerate(mission["steps"]):
            assert len(stage["evidence"]) == len(stage["options"]) == 3
            assert 0 <= mission["finding_key"][index] < 3
            assert sorted(option["points"] for option in stage["options"]) == [0, 0, 10]
            assert all(option["text"] and option["feedback"] for option in stage["options"])
        assert build_manifest(mission_id).pathway == "university"
        assert build_manifest(mission_id).max_score == 45
