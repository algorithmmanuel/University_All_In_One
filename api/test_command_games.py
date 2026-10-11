"""Phase 9.5: all thirty playable games and professional defensive scoring contracts."""
from game_catalog import game_catalog
from mission_contract import build_manifest
from mission_data import MISSIONS
from mission_routes import public_step

NEW_COMMAND_IDS = (
    "risk-command", "zero-trust-briefing", "cloud-incident", "supply-chain-watch",
    "ransomware-recovery", "identity-crisis", "boardroom-breach", "ai-governance",
    "audit-trail",
)

def test_every_pathway_has_ten_playable_games():
    catalog = game_catalog()
    assert catalog["version"] == 5
    assert len(catalog["games"]) == 30
    assert all(game["status"] == "playable" for game in catalog["games"])
    for pathway in ("secondary", "university", "professional"):
        games = [game for game in catalog["games"] if game["pathway"] == pathway]
        assert len(games) == 10
        assert all(game["mission_count"] == 1 for game in games)


def test_professional_cases_are_three_stage_and_server_scored():
    for mission_id in NEW_COMMAND_IDS:
        mission = MISSIONS[mission_id]
        manifest = build_manifest(mission_id)
        assert manifest.pathway == "professional"
        assert manifest.step_count == 3
        assert manifest.max_score == 45
        assert len(mission["finding_key"]) == 3
        assert len({stage["scene"] for stage in mission["steps"]}) == 3
        for index, stage in enumerate(mission["steps"]):
            safe = public_step(stage)
            assert set(safe) == {"scene", "story", "evidence", "question", "options"}
            assert len(safe["evidence"]) == len(safe["options"]) == 3
            assert all(isinstance(option, str) for option in safe["options"])
            assert sorted(option["points"] for option in stage["options"]) == [0, 0, 10]
            assert 0 <= mission["finding_key"][index] < 3
            assert "finding_key" not in safe
            assert "points" not in safe
            assert "feedback" not in safe
