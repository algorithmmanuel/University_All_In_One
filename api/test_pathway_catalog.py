"""Phase 7 catalogue contract tests. Run: python -m unittest test_pathway_catalog"""
import unittest
from pathway_catalog import PATHWAYS, pathway_catalog
from mission_data import MISSIONS

class PathwayCatalogTests(unittest.TestCase):
    def test_only_three_cybersecurity_audiences(self):
        self.assertEqual([p.id for p in PATHWAYS], ["secondary", "university", "professional"])
        self.assertEqual(pathway_catalog()["domain"], "cybersecurity")

    def test_missions_exist(self):
        for pathway in PATHWAYS:
            self.assertTrue(pathway.learning_objectives)
            self.assertTrue(pathway.sample_missions)
            for mission_id in pathway.sample_missions:
                self.assertIn(mission_id, MISSIONS)

    def test_no_duplicate_ids(self):
        self.assertEqual(len({p.id for p in PATHWAYS}), len(PATHWAYS))

if __name__ == "__main__":
    unittest.main()
