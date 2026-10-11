from game_catalog import game_catalog
from mission_data import MISSIONS
from mission_contract import build_manifest

def test_multiple_games_for_secondary():
    games = game_catalog()["games"]
    secondary = [g for g in games if g["pathway"] == "secondary"]
    assert len(secondary) >= 2
    assert len({g["id"] for g in secondary}) == len(secondary)

def test_all_games_reference_real_missions():
    for game in game_catalog()["games"]:
        assert game["mission_ids"]
        for mission_id in game["mission_ids"]:
            assert mission_id in MISSIONS
            assert build_manifest(mission_id).pathway == game["pathway"]

def test_password_fortress_three_stages():
    mission = MISSIONS["password-fortress"]
    assert len(mission["steps"]) == 3
    assert all(len(s["options"]) >= 2 and s["evidence"] for s in mission["steps"])
