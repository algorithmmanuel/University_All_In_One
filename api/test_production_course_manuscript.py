"""Content-manifest tests: do not require a database or change learner progress."""
import unittest
from production_learning.explorers_discover import COURSE
from production_learning.academy_discover import COURSE as ACADEMY
from production_learning.command_discover import COURSE as COMMAND

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

    def test_all_discover_courses_are_distinct(self):
        courses = [COURSE, ACADEMY, COMMAND]
        self.assertEqual(len({c["pathway"] for c in courses}), 3)
        self.assertEqual(len({c["title"] for c in courses}), 3)
        for course in courses:
            self.assertEqual(course["stage"], "discover")
            self.assertEqual(len(course["lessons"]), 8)
            for lesson in course["lessons"]:
                self.assertGreaterEqual(len(lesson["content"].split()), 90)
                self.assertIn("Worked example:", lesson["content"])
            self.assertIn("Further reading", course["lessons"][-1]["content"])

if __name__ == "__main__":
    unittest.main()
