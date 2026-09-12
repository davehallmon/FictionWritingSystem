import unittest

from tools.translation.audit_residuals import (
    classify_residuals,
    residual_occurrences,
    terminology_occurrences,
)


class ResidualAuditTests(unittest.TestCase):
    def test_authoritative_fence_and_inline_code_are_excluded(self):
        text = (
            "# English\n\n"
            "Visible 中文 prose.\n\n"
            "`保护字段`\n\n"
            "```text\n保留模板\n```\n"
        )
        found = residual_occurrences("sample.md", text)
        self.assertEqual([item["literal"] for item in found], ["中文"])
        self.assertEqual(found[0]["line"], 3)

    def test_unreviewed_residual_is_unexplained_prose(self):
        occurrences = residual_occurrences("sample.md", "English with 中文 here.\n")
        classified, errors = classify_residuals(occurrences, {"entries": []})
        self.assertEqual(errors, [])
        self.assertEqual(classified[0]["classification"], "unexplained_prose")

    def test_reviewed_ledger_entry_accepts_exact_count_and_line(self):
        occurrences = residual_occurrences("sample.md", "English with 中文 here.\n中文 again.\n")
        ledger = {
            "entries": [
                {
                    "path": "sample.md",
                    "line": 1,
                    "literal": "中文",
                    "classification": "intentional_bilingual_example",
                    "reason": "Demonstrates the source-language label.",
                    "expected_count": 2,
                    "review": {
                        "status": "reviewed",
                        "operationally_safe": True,
                        "review_note": "Approved bilingual example.",
                    },
                }
            ]
        }
        classified, errors = classify_residuals(occurrences, ledger)
        self.assertEqual(errors, [])
        self.assertEqual({item["classification"] for item in classified}, {"intentional_bilingual_example"})

    def test_ledger_count_mismatch_fails(self):
        occurrences = residual_occurrences("sample.md", "中文 once.\n")
        ledger = {
            "entries": [
                {
                    "path": "sample.md",
                    "line": 1,
                    "literal": "中文",
                    "classification": "proper_name_or_title",
                    "reason": "Approved title.",
                    "expected_count": 2,
                    "review": {
                        "status": "reviewed",
                        "operationally_safe": True,
                        "review_note": "Reviewed.",
                    },
                }
            ]
        }
        _, errors = classify_residuals(occurrences, ledger)
        self.assertTrue(any("count mismatch" in error for error in errors))

    def test_stale_ledger_entry_fails(self):
        ledger = {
            "entries": [
                {
                    "path": "sample.md",
                    "line": 1,
                    "literal": "旧词",
                    "classification": "proper_name_or_title",
                    "reason": "Old exception.",
                    "expected_count": 1,
                    "review": {
                        "status": "reviewed",
                        "operationally_safe": True,
                        "review_note": "Reviewed.",
                    },
                }
            ]
        }
        _, errors = classify_residuals([], ledger)
        self.assertTrue(any("Stale ledger entry" in error for error in errors))

    def test_unresolved_chinese_fragment_is_automatic_failure(self):
        text = "[Section](#中文标题)\n"
        occurrences = residual_occurrences("sample.md", text)
        classified, _ = classify_residuals(occurrences, {"entries": []})
        self.assertEqual(classified[0]["classification"], "unresolved_anchor")

    def test_deprecated_terminology_is_reported_outside_protected_regions(self):
        glossary = {
            "terms": {
                "扫榜": {
                    "preferred_english": "rankings scan",
                    "deprecated_english": ["ranking scan"],
                    "alternatives": [],
                }
            }
        }
        text = "Use a ranking scan here. `ranking scan` stays protected.\n"
        findings = terminology_occurrences("sample.md", text, glossary)
        deprecated = [item for item in findings if item["status"] == "deprecated"]
        self.assertEqual(len(deprecated), 1)
        self.assertEqual(deprecated[0]["preferred"], "rankings scan")

    def test_context_limited_alternative_is_reported_for_review(self):
        glossary = {
            "terms": {
                "剧情单元": {
                    "preferred_english": "story unit",
                    "alternatives": [
                        {
                            "value": "plot unit",
                            "usage": "Allowed only in legacy named contexts.",
                        }
                    ],
                }
            }
        }
        findings = terminology_occurrences("sample.md", "This plot unit needs review.\n", glossary)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["status"], "review_alternative")


if __name__ == "__main__":
    unittest.main()
