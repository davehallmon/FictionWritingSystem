import unittest

from tools.translation.validate_translation import validate


class Issue4TokenParserTests(unittest.TestCase):
    def test_markdown_table_separator_dashes_are_not_cli_tokens(self):
        source = "# 表格\n\n| 字段 | 值 |\n|-----|-----------|\n| A | B |\n"
        output = "# Table\n\n| Field | Value |\n|------|---------|\n| A | B |\n"
        self.assertTrue(validate(source, output).valid)

    def test_chinese_double_dash_prose_separator_is_not_cli_token(self):
        source = "# 层级\n\n家庭--村--镇--县--市--省--本国--本州\n"
        output = "# Hierarchy\n\nfamily → village → town → county → city → province → country → state\n"
        self.assertTrue(validate(source, output).valid)

    def test_ascii_cli_flag_remains_protected(self):
        source = "# 命令\n\nRun --output result.md.\n"
        output = "# Command\n\nRun result.md.\n"
        result = validate(source, output)
        self.assertFalse(result.valid)
        self.assertIn("Changed protected tokens", result.errors)


if __name__ == "__main__":
    unittest.main()
