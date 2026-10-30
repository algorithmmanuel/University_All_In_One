"""Content-manifest tests: do not require a database or change learner progress."""
import unittest
from production_learning.explorers_discover import COURSE
from production_learning.academy_discover import COURSE as ACADEMY
from production_learning.command_discover import COURSE as COMMAND
from production_learning.explorers_understand import COURSE as EXPLORERS_UNDERSTAND
from production_learning.explorers_check import COURSE as EXPLORERS_CHECK
from production_learning.explorers_investigate import COURSE as EXPLORERS_INVESTIGATE
from production_learning.explorers_defend import COURSE as EXPLORERS_DEFEND
from production_learning.explorers_command import COURSE as EXPLORERS_COMMAND
from production_learning.explorers_opponent import COURSE as EXPLORERS_OPPONENT
from production_learning.explorers_compete import COURSE as EXPLORERS_COMPETE
from production_learning.academy_understand import COURSE as ACADEMY_UNDERSTAND
from production_learning.academy_check import COURSE as ACADEMY_CHECK
from production_learning.academy_investigate import COURSE as ACADEMY_INVESTIGATE
from production_learning.academy_defend import COURSE as ACADEMY_DEFEND
from production_learning.academy_command import COURSE as ACADEMY_COMMAND
from production_learning.academy_opponent import COURSE as ACADEMY_OPPONENT
from production_learning.academy_compete import COURSE as ACADEMY_COMPETE
from production_learning.command_understand import COURSE as COMMAND_UNDERSTAND

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
            self.assertGreaterEqual(len(lesson["content"].split()), 600)
            self.assertTrue("Worked example:" in lesson["content"] or "Reflection:" in lesson["content"])
        self.assertIn("Further reading", COURSE["lessons"][-1]["content"])

    def test_explorers_understand_full_length_manuscript(self):
        course = EXPLORERS_UNDERSTAND
        self.assertEqual((course["pathway"], course["stage"]), ("secondary", "understand"))
        self.assertEqual(len(course["lessons"]), 8)
        self.assertEqual([row["position"] for row in course["lessons"]], list(range(1, 9)))
        for lesson in course["lessons"]:
            self.assertGreaterEqual(len(lesson["content"].split()), 600)
            self.assertIn("Worked example:", lesson["content"])
        self.assertIn("Further reading", course["lessons"][-1]["content"])

    def test_academy_capstone_and_command_governance_manuscripts(self):
        for course, pathway, stage in ((ACADEMY_COMPETE,"university","compete"),(COMMAND_UNDERSTAND,"professional","understand")):
            with self.subTest(stage=stage):
                self.assertEqual((course["pathway"],course["stage"]),(pathway,stage))
                self.assertEqual(len(course["lessons"]),8)
                self.assertEqual([x["position"] for x in course["lessons"]],list(range(1,9)))
                self.assertEqual(len({x["title"] for x in course["lessons"]}),8)
                for lesson in course["lessons"]:
                    self.assertGreaterEqual(len(lesson["content"].split()),600)
                    self.assertIn("Worked example:",lesson["content"])
                self.assertIn("Further reading",course["lessons"][-1]["content"])

    def test_academy_command_and_opponent_manuscripts(self):
        for course,stage in ((ACADEMY_COMMAND,"command"),(ACADEMY_OPPONENT,"opponent")):
            with self.subTest(stage=stage):
                self.assertEqual((course["pathway"],course["stage"]),("university",stage))
                self.assertEqual(len(course["lessons"]),8)
                self.assertEqual([x["position"] for x in course["lessons"]],list(range(1,9)))
                self.assertEqual(len({x["title"] for x in course["lessons"]}),8)
                for lesson in course["lessons"]:
                    self.assertGreaterEqual(len(lesson["content"].split()),600)
                    self.assertIn("Worked example:",lesson["content"])
                self.assertIn("Further reading",course["lessons"][-1]["content"])

    def test_academy_investigate_and_defend_are_full_length(self):
        for course,stage in ((ACADEMY_INVESTIGATE,"investigate"),(ACADEMY_DEFEND,"defend")):
            with self.subTest(stage=stage):
                self.assertEqual((course["pathway"],course["stage"]),("university",stage))
                self.assertEqual(len(course["lessons"]),8)
                self.assertEqual([x["position"] for x in course["lessons"]],list(range(1,9)))
                self.assertEqual(len({x["title"] for x in course["lessons"]}),8)
                for lesson in course["lessons"]:
                    self.assertGreaterEqual(len(lesson["content"].split()),600)
                    self.assertIn("Worked example:",lesson["content"])
                self.assertIn("Further reading",course["lessons"][-1]["content"])

    def test_academy_understand_and_check_are_full_length(self):
        for course,stage in ((ACADEMY_UNDERSTAND,"understand"),(ACADEMY_CHECK,"check")):
            with self.subTest(stage=stage):
                self.assertEqual((course["pathway"],course["stage"]),("university",stage))
                self.assertEqual(len(course["lessons"]),8)
                self.assertEqual([x["position"] for x in course["lessons"]],list(range(1,9)))
                self.assertEqual(len({x["title"] for x in course["lessons"]}),8)
                for lesson in course["lessons"]:
                    self.assertGreaterEqual(len(lesson["content"].split()),600)
                    self.assertIn("Worked example:",lesson["content"])
                self.assertIn("Further reading",course["lessons"][-1]["content"])

    def test_final_two_explorers_manuscripts_have_required_structure(self):
        for course, stage in ((EXPLORERS_OPPONENT,"opponent"),(EXPLORERS_COMPETE,"compete")):
            with self.subTest(stage=stage):
                self.assertEqual((course["pathway"],course["stage"]),("secondary",stage))
                self.assertEqual(len(course["lessons"]),8)
                self.assertEqual([x["position"] for x in course["lessons"]],list(range(1,9)))
                self.assertEqual(len({x["title"] for x in course["lessons"]}),8)
                for lesson in course["lessons"]:
                    self.assertGreaterEqual(len(lesson["content"].split()),600)
                    self.assertIn("Worked example:",lesson["content"])
                self.assertIn("Further reading",course["lessons"][-1]["content"])

    def test_two_new_explorers_manuscripts_have_required_structure(self):
        for course, stage in ((EXPLORERS_DEFEND,"defend"),(EXPLORERS_COMMAND,"command")):
            with self.subTest(stage=stage):
                self.assertEqual((course["pathway"],course["stage"]),("secondary",stage))
                self.assertEqual(len(course["lessons"]),8)
                self.assertEqual([lesson["position"] for lesson in course["lessons"]],list(range(1,9)))
                self.assertEqual(len({lesson["title"] for lesson in course["lessons"]}),8)
                for lesson in course["lessons"]:
                    self.assertGreaterEqual(len(lesson["content"].split()),600)
                    self.assertIn("Worked example:",lesson["content"])
                self.assertIn("Further reading",course["lessons"][-1]["content"])

    def test_explorers_investigate_full_length_manuscript(self):
        course = EXPLORERS_INVESTIGATE
        self.assertEqual((course["pathway"], course["stage"]), ("secondary", "investigate"))
        self.assertEqual(len(course["lessons"]), 8)
        for lesson in course["lessons"]:
            self.assertGreaterEqual(len(lesson["content"].split()), 600)
            self.assertIn("Worked example:", lesson["content"])
        self.assertIn("Further reading", course["lessons"][-1]["content"])

    def test_explorers_check_full_length_manuscript(self):
        course = EXPLORERS_CHECK
        self.assertEqual((course["pathway"], course["stage"]), ("secondary", "check"))
        self.assertEqual(len(course["lessons"]), 8)
        self.assertEqual([x["position"] for x in course["lessons"]], list(range(1,9)))
        self.assertEqual(len({x["title"] for x in course["lessons"]}),8)
        for lesson in course["lessons"]:
            self.assertGreaterEqual(len(lesson["content"].split()), 600)
            self.assertIn("Worked example:", lesson["content"])
        self.assertIn("Further reading", course["lessons"][-1]["content"])

    def test_all_discover_courses_are_distinct(self):
        courses = [COURSE, ACADEMY, COMMAND]
        self.assertEqual(len({c["pathway"] for c in courses}), 3)
        self.assertEqual(len({c["title"] for c in courses}), 3)
        for course in courses:
            self.assertEqual(course["stage"], "discover")
            self.assertEqual(len(course["lessons"]), 8)
            for lesson in course["lessons"]:
                self.assertGreaterEqual(len(lesson["content"].split()), 600)
                self.assertIn("Worked example:", lesson["content"])
            self.assertIn("Further reading", course["lessons"][-1]["content"])

if __name__ == "__main__":
    unittest.main()
