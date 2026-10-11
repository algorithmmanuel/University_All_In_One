from game_catalog import game_catalog
from mission_data import MISSIONS
from mission_contract import build_manifest


def test_exactly_ten_games_per_pathway():
    catalog = game_catalog()
    assert catalog["version"] == 2
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
