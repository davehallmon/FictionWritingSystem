#!/usr/bin/env python3
"""Validate invariant Markdown structures in a translated file."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

FENCE_RE = re.compile(r"(?ms)^([ \t]*(`{3,}|~{3,})[^\n]*\n).*?^[ \t]*\2[ \t]*$")
INLINE_CODE_RE = re.compile(r"(?<!`)`[^`\n]+`(?!`)")
URL_RE = re.compile(r"https?://[^\s)>\]]+")
LINK_TARGET_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
TOKEN_RE = re.compile(r"\$\{[^}]+\}|\{\{[^}]+\}\}|(?<!\w)--[\w-]+|(?<!\w)\$[\w-]+")
HEADING_RE = re.compile(r"(?m)^(#{1,6})\s+")
ZH_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")


@dataclass
class ValidationResult:
    valid: bool
    errors: list[str]
    warnings: list[str]
    source_chinese_characters: int
    output_chinese_characters: int


def fenced_blocks(text: str) -> list[str]:
    return [match.group(0) for match in FENCE_RE.finditer(text)]


def without_fences(text: str) -> str:
    return FENCE_RE.sub("", text)


def table_dimensions(text: str) -> list[int]:
    dimensions: list[int] = []
    for line in without_fences(text).splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            dimensions.append(len(stripped.split("|")) - 2)
    return dimensions


def frontmatter_keys(text: str) -> list[str]:
    if not text.startswith("---\n"):
        return []
    end = text.find("\n---", 4)
    if end < 0:
        return ["<unclosed>"]
    keys = []
    for line in text[4:end].splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):", line)
        if match:
            keys.append(match.group(1))
    return keys


def validate(source: str, output: str) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    comparisons = {
        "fenced code blocks": (fenced_blocks(source), fenced_blocks(output)),
        "inline code": (INLINE_CODE_RE.findall(without_fences(source)), INLINE_CODE_RE.findall(without_fences(output))),
        "URLs": (URL_RE.findall(source), URL_RE.findall(output)),
        "link destinations": (LINK_TARGET_RE.findall(source), LINK_TARGET_RE.findall(output)),
        "literal tokens": (TOKEN_RE.findall(without_fences(source)), TOKEN_RE.findall(without_fences(output))),
        "heading levels": (HEADING_RE.findall(without_fences(source)), HEADING_RE.findall(without_fences(output))),
        "table dimensions": (table_dimensions(source), table_dimensions(output)),
        "frontmatter keys": (frontmatter_keys(source), frontmatter_keys(output)),
    }
    for label, (before, after) in comparisons.items():
        if before != after:
            errors.append(f"Changed {label}")
    if not output.strip():
        errors.append("Output is empty")
    source_zh = len(ZH_RE.findall(source))
    output_zh = len(ZH_RE.findall(output))
    if output_zh:
        warnings.append(f"Output retains {output_zh} Chinese characters; review intentional exceptions")
    return ValidationResult(not errors, errors, warnings, source_zh, output_zh)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = validate(args.source.read_text(encoding="utf-8"), args.output.read_text(encoding="utf-8"))
    print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    return 0 if result.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
