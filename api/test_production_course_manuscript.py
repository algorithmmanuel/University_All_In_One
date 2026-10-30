"""Content-manifest tests: do not require a database or change learner progress."""
import unittest
from production_learning.explorers_discover import COURSE

class ProductionCourseManuscriptTests(unittest.TestCase):
    def test_approved_structure(self):
        self.assertEqual(COURSE["pathway"], "secondary")
        self.assertEqual(COURSE["stage"], "discover")
        self.assertEqual(COURSE["revision"], "v1")
        self.assertEqual(len(COURSE["lessons"]), 8)
        self.assertEqual([x["position"] for x in COURSE["lessons"]], list(range(1, 9)))

    def test_unique_and_substantive_lessons(self):
        titles = [x["title"] for x in COURSE["lessons"]]
        self.assertEqual(len(set(titles)), len(titles))
        for lesson in COURSE["lessons"]:
            self.assertGreaterEqual(len(lesson["content"].split()), 90)
            self.assertTrue("Worked example:" in lesson["content"] or "Reflection:" in lesson["content"])
        self.assertIn("Further reading", COURSE["lessons"][-1]["content"])

if __name__ == "__main__":
    unittest.main()
