"""Fail-closed checks for the draft-course publication boundary.

No database connection or publication occurs in these tests.
"""
import hashlib
import json
import unittest
from unittest.mock import patch

import publish_production_learning as publisher


class EditorialPublicationGateTests(unittest.TestCase):
    def test_missing_approval_file_blocks_release(self):
        with patch("pathlib.Path.is_file", return_value=False):
            with self.assertRaisesRegex(RuntimeError, "Editorial approvals file missing"):
                publisher.require_editorial_approvals()

    def test_stale_approval_hash_blocks_release(self):
        approvals = {
            course["key"]: {
                "sha256": "0" * 64,
                "reviewer": "Review Team",
                "approved_at": "2026-10-30",
            }
            for course in publisher.COURSES
        }
        with patch("pathlib.Path.is_file", return_value=True), patch(
            "pathlib.Path.read_text", return_value=json.dumps(approvals)
        ):
            with self.assertRaisesRegex(RuntimeError, "stale editorial approval"):
                publisher.require_editorial_approvals()

    def test_incomplete_approvals_block_release(self):
        with patch("pathlib.Path.is_file", return_value=True), patch(
            "pathlib.Path.read_text", return_value="{}"
        ):
            with self.assertRaisesRegex(RuntimeError, "Every course"):
                publisher.require_editorial_approvals()

    def test_duplicate_paragraph_blocks_release(self):
        duplicated = " ".join(["repeated"] * 40)
        fixture = [
            {"key": "a", "lessons": [{"position": 1, "content": duplicated}]},
            {"key": "b", "lessons": [{"position": 1, "content": duplicated}]},
        ]
        with patch.object(publisher, "COURSES", fixture):
            with self.assertRaisesRegex(RuntimeError, "repeated substantive paragraphs"):
                publisher.validate_editorial_uniqueness()

    def test_duplicate_sequence_across_paragraphs_blocks_release(self):
        words = " ".join("token" + str(i) for i in range(75))
        fixture = [
            {"key": "a", "lessons": [{"position": 1, "content": words}]},
            {"key": "b", "lessons": [{"position": 1, "content": "Introduction.\n\n" + words}]},
        ]
        with patch.object(publisher, "COURSES", fixture):
            with self.assertRaisesRegex(RuntimeError, "repeated 70-word sequences"):
                publisher.validate_editorial_uniqueness()


if __name__ == "__main__":
    unittest.main()
