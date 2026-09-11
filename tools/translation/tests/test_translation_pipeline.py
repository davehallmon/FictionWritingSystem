import tempfile
import unittest
from pathlib import Path

from tools.translation.build_manifest import build_manifest
from tools.translation.validate_translation import heading_slugs, validate


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

    def test_validator_accepts_marked_text_companion_after_unchanged_fence(self):
        source = "# 示例\n\n```\n动作 → 对话 → 反应\n```\n"
        output = (
            "# Example\n\n```\n动作 → 对话 → 反应\n```\n\n"
            "<!-- translation-companion: non-executable -->\n"
            "```text\nAction → dialogue → reaction\n```\n"
        )
        self.assertTrue(validate(source, output).valid)

    def test_validator_rejects_in_place_natural_language_fence_translation(self):
        source = "# 示例\n\n```\n动作 → 对话 → 反应\n```\n"
        output = "# Example\n\n```\nAction → dialogue → reaction\n```\n"
        result = validate(source, output)
        self.assertFalse(result.valid)
        self.assertIn("Changed fenced code blocks", result.errors)

    def test_validator_rejects_unmarked_extra_fence(self):
        source = "# 示例\n\n```\n中文示例\n```\n"
        output = "# Example\n\n```\n中文示例\n```\n\n```text\nEnglish example\n```\n"
        result = validate(source, output)
        self.assertFalse(result.valid)
        self.assertIn("Changed fenced code blocks", result.errors)

    def test_validator_rejects_structured_translation_companion(self):
        source = '# 示例\n\n```json\n{"name": "角色"}\n```\n'
        output = (
            '# Example\n\n```json\n{"name": "角色"}\n```\n\n'
            '<!-- translation-companion: non-executable -->\n'
            '```json\n{"name": "Character"}\n```\n'
        )
        result = validate(source, output)
        self.assertFalse(result.valid)
        self.assertIn("Translation companion must use a non-executable text fence", result.errors)

    def test_validator_rejects_detached_translation_companion(self):
        source = "# 示例\n\n```\n中文示例\n```\n"
        output = (
            "# Example\n\n```\n中文示例\n```\n\n"
            "English explanation follows.\n\n"
            "<!-- translation-companion: non-executable -->\n"
            "```text\nEnglish example\n```\n"
        )
        result = validate(source, output)
        self.assertFalse(result.valid)
        self.assertIn(
            "Translation companion marker must be the only non-whitespace content between fences",
            result.errors,
        )

    def test_validator_accepts_localized_same_page_fragment(self):
        source = "# 文档\n\n- [章节](#章节一)\n\n## 章节一\n"
        output = "# Document\n\n- [Section](#section-one)\n\n## Section One\n"
        self.assertTrue(validate(source, output).valid)

    def test_validator_rejects_unresolved_same_page_fragment(self):
        source = "# 文档\n\n- [章节](#章节一)\n\n## 章节一\n"
        output = "# Document\n\n- [Section](#章节一)\n\n## Section One\n"
        result = validate(source, output)
        self.assertFalse(result.valid)
        self.assertIn("Unresolved same-page fragments: #章节一", result.errors)

    def test_heading_slugs_handle_duplicates(self):
        text = "# Document\n\n## Item\n\n## Item\n"
        self.assertEqual(heading_slugs(text), ["document", "item", "item-1"])

    def test_heading_slugs_handle_punctuation(self):
        text = "# What's New? v2.0\n"
        self.assertEqual(heading_slugs(text), ["whats-new-v20"])

    def test_heading_slugs_handle_mixed_chinese_and_english(self):
        text = "# API 接口: v2\n"
        self.assertEqual(heading_slugs(text), ["api-接口-v2"])

    def test_validator_preserves_external_urls_and_file_paths(self):
        source = "# 文档\n\n[External](https://example.com/a)\n[File](guide.md#section)\n"
        unchanged = "# Document\n\n[External](https://example.com/a)\n[File](guide.md#section)\n"
        changed = "# Document\n\n[External](https://example.com/b)\n[File](guide.md#other)\n"
        self.assertTrue(validate(source, unchanged).valid)
        result = validate(source, changed)
        self.assertFalse(result.valid)
        self.assertIn("Changed URLs", result.errors)
        self.assertIn("Changed protected link destinations", result.errors)


if __name__ == "__main__":
    unittest.main()
