"""Regression tests for grouped editorial duplication reports (no DB needed)."""
import unittest
from audit_production_learning import audit


def course(key, contents):
    return {"key": key, "lessons": [
        {"position": i, "title": f"Example {i}", "content": content}
        for i, content in enumerate(contents, 1)
    ]}


class AuditProductionLearningTests(unittest.TestCase):
    def test_overlapping_windows_collapse_into_single_cluster(self):
        common = " ".join("word" + str(i) for i in range(80))
        report = audit([course("explorers-demo", [
            "intro one " + common + " end one",
            "intro two " + common + " end two",
        ])], window=70)
        self.assertEqual(report["duplicated_window_signatures"], 11)
        self.assertEqual(report["passage_cluster_count"], 1)
        self.assertEqual(report["clusters"][0]["lesson_count"], 2)

    def test_different_lessons_do_not_get_false_duplicates(self):
        report = audit([course("a", ["apple pear orange sky river"]),
                        course("b", ["rock stone road train clock"])], window=3)
        self.assertEqual(report["duplicated_window_signatures"], 0)
        self.assertEqual(report["passage_cluster_count"], 0)

    def test_distinct_duplicated_regions_remain_separate(self):
        first = " ".join("first" + str(i) for i in range(9))
        second = " ".join("second" + str(i) for i in range(9))
        report = audit([course("a", [first + " uniqueA " + second]),
                        course("b", [first + " uniqueB " + second])], window=5)
        self.assertEqual(report["passage_cluster_count"], 2)

    def test_duplicate_lesson_identifier_fails_closed(self):
        fixture = [course("x", ["alpha beta"]), course("x", ["gamma delta"])]
        with self.assertRaisesRegex(ValueError, "Duplicate lesson identity"):
            audit(fixture, window=2)


if __name__ == "__main__":
    unittest.main()
