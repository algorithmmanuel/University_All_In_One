"""Regression tests for the shared 2D/3D mission contract and safe catalog."""
from game_catalog import game_catalog
from mission_data import MISSIONS
from mission_routes import public_step
from mission_contract import build_manifest


def test_all_playable_games_have_complete_client_safe_steps():
    for game in game_catalog()["games"]:
        if game["status"] != "playable":
            continue
        for mission_id in game["mission_ids"]:
            mission = MISSIONS[mission_id]
            manifest = build_manifest(mission_id)
            assert manifest.step_count == len(mission["steps"])
            assert manifest.max_score == len(mission["steps"]) * 15
            for stage in mission["steps"]:
                client = public_step(stage)
                assert set(client) == {"scene", "story", "evidence", "question", "options"}
                assert all(isinstance(option, str) for option in client["options"])
                assert "points" not in str(client)
                assert "feedback" not in str(client)
                assert all("points" in option and "feedback" in option for option in stage["options"])


def test_new_game_finding_keys_are_server_only():
    for game in game_catalog()["games"]:
        if game["pathway"] != "secondary":
            continue
        for mission_id in game["mission_ids"]:
            mission = MISSIONS[mission_id]
            if "finding_key" not in mission:
                continue
            assert len(mission["finding_key"]) == len(mission["steps"])
            manifest = build_manifest(mission_id).model_dump(mode="json")
            assert "finding_key" not in manifest
            for stage in mission["steps"]:
                assert "finding_key" not in public_step(stage)


def test_all_explorer_games_remain_distinct():
    explorer = [game for game in game_catalog()["games"] if game["pathway"] == "secondary"]
    assert len(explorer) == 10
    assert len({game["id"] for game in explorer}) == 10
    assert len({MISSIONS[game["mission_ids"][0]]["summary"] for game in explorer}) == 10
