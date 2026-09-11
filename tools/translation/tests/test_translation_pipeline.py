import tempfile
import unittest
from pathlib import Path

from tools.translation.build_manifest import build_manifest
from tools.translation.validate_translation import validate


class TranslationPipelineTests(unittest.TestCase):
    def test_manifest_maps_source_and_excludes_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            project = repo / "oh-story"
            target = project / "Chinese-to-English"
            target.mkdir(parents=True)
            (project / "Ref - sample.md").write_text("# 标题\n" + "中文内容" * 10, encoding="utf-8")
            (target / "Ref - sample.md").write_text("# Title\nEnglish content", encoding="utf-8")
            manifest = build_manifest(repo, ("oh-story",))
            self.assertEqual(manifest["summary"]["targets"], 1)
            self.assertEqual(manifest["files"][0]["status"], "translated")

    def test_validator_accepts_translated_prose_with_invariants(self):
        source = '# 标题\n\n运行 `tool --flag`。\n\n```bash\necho "$VALUE"\n```\n'
        output = '# Title\n\nRun `tool --flag`.\n\n```bash\necho "$VALUE"\n```\n'
        self.assertTrue(validate(source, output).valid)

    def test_validator_rejects_changed_code(self):
        source = "# 标题\n```bash\necho one\n```\n"
        output = "# Title\n```bash\necho two\n```\n"
        result = validate(source, output)
        self.assertFalse(result.valid)
        self.assertIn("Changed fenced code blocks", result.errors)


if __name__ == "__main__":
    unittest.main()
