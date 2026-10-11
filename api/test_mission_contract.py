"""Phase 7 mission manifest regression and non-disclosure checks."""
import unittest
from mission_contract import MissionManifest, build_manifest, public_manifest_catalog
from mission_data import MISSIONS

class MissionContractTests(unittest.TestCase):
    def test_every_legacy_mission_has_manifest(self):
        self.assertEqual(
            {m["id"] for m in public_manifest_catalog()["missions"]},
            set(MISSIONS),
        )

    def test_max_score_and_steps_match_existing_engine(self):
        for mission_id, mission in MISSIONS.items():
            manifest = build_manifest(mission_id)
            self.assertEqual(manifest.step_count, len(mission["steps"]))
            self.assertEqual(manifest.max_score, 15 * len(mission["steps"]))
            self.assertEqual(manifest.version, 1)

    def test_public_catalog_does_not_expose_answers_or_points(self):
        for manifest in public_manifest_catalog()["missions"]:
            self.assertNotIn("steps", manifest)
            self.assertNotIn("correct_index", manifest)
            self.assertNotIn("options", manifest)
            self.assertNotIn("feedback", manifest)

    def test_invalid_manifest_rejected(self):
        with self.assertRaises(ValueError):
            MissionManifest(id="x", version=0, pathway="secondary",
                            title="x", summary="x", difficulty="Beginner",
                            scene_type="decision", step_count=1, max_score=15)

if __name__ == "__main__":
    unittest.main()
