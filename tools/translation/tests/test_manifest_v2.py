import json
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from build_manifest import build_manifest


SOURCE_TEXT = "# 标题\n\n这是一个用于测试翻译清单的中文源文件。它包含足够多的中文字符，以确保会被发现和处理。\n"
TARGET_TEXT = "# Title\n\nThis is an English translation used to test the translation manifest. It is complete and non-empty.\n"
LEDGER = {"schema_version": 1, "summary": {"accepted": True}, "entries": []}


class ManifestV2Tests(unittest.TestCase):
    def make_repo(self):
        temp = tempfile.TemporaryDirectory()
        repo = Path(temp.name)
        (repo / "drama" / "Chinese-to-English").mkdir(parents=True)
        return temp, repo

    def write_pair(self, repo: Path, name: str = "doc.md", source: str = SOURCE_TEXT, target: str = TARGET_TEXT):
        source_path = repo / "drama" / name
        destination = repo / "drama" / "Chinese-to-English" / name
        source_path.parent.mkdir(parents=True, exist_ok=True)
        destination.parent.mkdir(parents=True, exist_ok=True)
        source_path.write_text(source, encoding="utf-8")
        destination.write_text(target, encoding="utf-8")
        return source_path, destination

    def build(self, repo: Path, previous=None):
        return build_manifest(
            repo,
            ("drama",),
            previous_manifest=previous,
            source_branch="translation/chinese-to-english",
            source_commit="test-source-commit",
            residual_ledger=LEDGER,
        )

    def test_deterministic_regeneration(self):
        temp, repo = self.make_repo()
        self.addCleanup(temp.cleanup)
        self.write_pair(repo)
        first = self.build(repo)
        second = self.build(repo, previous=first)
        self.assertEqual(first, second)
        self.assertEqual(
            json.dumps(first, ensure_ascii=False, indent=2) + "\n",
            json.dumps(second, ensure_ascii=False, indent=2) + "\n",
        )
        self.assertEqual(first["summary"]["translated"], 1)
        self.assertEqual(first["summary"]["remaining"], 0)

    def test_missing_output_is_not_translated(self):
        temp, repo = self.make_repo()
        self.addCleanup(temp.cleanup)
        source = repo / "drama" / "missing.md"
        source.write_text(SOURCE_TEXT, encoding="utf-8")
        manifest = self.build(repo)
        entry = manifest["files"][0]
        self.assertFalse(entry["state"]["destination_present"])
        self.assertFalse(entry["state"]["translation_complete"])
        self.assertEqual(entry["state"]["validator"], "fail")
        self.assertFalse(entry["state"]["translated"])
        self.assertEqual(entry["state"]["status"], "missing")
        self.assertIsNone(entry["integrity"]["destination_sha256"])
        self.assertEqual(manifest["summary"]["remaining"], 1)

    def test_stale_source_is_detected_when_destination_does_not_change(self):
        temp, repo = self.make_repo()
        self.addCleanup(temp.cleanup)
        source, destination = self.write_pair(repo)
        baseline = self.build(repo)
        source.write_text(SOURCE_TEXT + "\n新增的源内容。\n", encoding="utf-8")
        current = self.build(repo, previous=baseline)
        entry = current["files"][0]
        self.assertTrue(entry["state"]["stale_source"])
        self.assertEqual(entry["state"]["stale_detection_basis"], "previous_manifest")
        self.assertEqual(entry["state"]["status"], "stale")
        self.assertFalse(entry["state"]["translated"])
        self.assertEqual(current["summary"]["stale_translations"], 1)
        self.assertEqual(destination.read_text(encoding="utf-8"), TARGET_TEXT)

    def test_invalid_output_is_not_translated(self):
        temp, repo = self.make_repo()
        self.addCleanup(temp.cleanup)
        self.write_pair(repo, target="## Wrong heading level\n\nEnglish text.\n")
        manifest = self.build(repo)
        entry = manifest["files"][0]
        self.assertEqual(entry["validation"]["status"], "fail")
        self.assertIn("Changed heading levels", entry["validation"]["errors"])
        self.assertEqual(entry["state"]["status"], "validation_failed")
        self.assertFalse(entry["state"]["translated"])
        self.assertEqual(manifest["summary"]["validation_fail"], 1)

    def test_duplicate_sources_are_reported_and_summary_is_derived(self):
        temp, repo = self.make_repo()
        self.addCleanup(temp.cleanup)
        self.write_pair(repo, "one.md")
        self.write_pair(repo, "two.md")
        manifest = self.build(repo)
        self.assertEqual(manifest["summary"]["targets"], 2)
        self.assertEqual(manifest["summary"]["destination_present"], 2)
        self.assertEqual(manifest["summary"]["translation_complete"], 2)
        self.assertEqual(manifest["summary"]["validation_pass"], 2)
        self.assertEqual(manifest["summary"]["residual_review_pass"], 2)
        self.assertEqual(manifest["summary"]["translated"], 2)
        self.assertEqual(manifest["summary"]["reviewer_not_recorded"], 2)
        self.assertEqual(manifest["summary"]["duplicate_groups"], 1)
        self.assertEqual(
            manifest["duplicate_groups"],
            [["drama/one.md", "drama/two.md"]],
        )
        for entry in manifest["files"]:
            self.assertRegex(entry["integrity"]["source_sha256"], r"^[0-9a-f]{64}$")
            self.assertRegex(entry["integrity"]["destination_sha256"], r"^[0-9a-f]{64}$")
            self.assertEqual(entry["review"]["status"], "not_recorded")


if __name__ == "__main__":
    unittest.main()
