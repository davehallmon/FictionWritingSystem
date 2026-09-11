#!/usr/bin/env python3
"""Validate invariant Markdown structures in a translated file."""

from __future__ import annotations

import argparse
import html
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import unquote

FENCE_RE = re.compile(r"(?ms)^([ \t]*(`{3,}|~{3,})[^\n]*\n).*?^[ \t]*\2[ \t]*$")
INLINE_CODE_RE = re.compile(r"(?<!`)`[^`\n]+`(?!`)")
URL_RE = re.compile(r"https?://[^\s)>\]]+")
LINK_TARGET_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
TOKEN_RE = re.compile(r"\$\{[^}]+\}|\{\{[^}]+\}\}|(?<!\w)--[\w-]+|(?<!\w)\$[\w-]+")
HEADING_RE = re.compile(r"(?m)^(#{1,6})\s+")
HEADING_TEXT_RE = re.compile(r"(?m)^#{1,6}\s+(.+?)\s*$")
ZH_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
MARKDOWN_LINK_TEXT_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
HTML_TAG_RE = re.compile(r"<[^>]+>")
MARKDOWN_PUNCT_RE = re.compile(r"[*_~]")
SLUG_PUNCT_RE = re.compile(r"[^\w\s-]", re.UNICODE)
WHITESPACE_RE = re.compile(r"\s+")


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


def link_destinations(text: str) -> list[str]:
    return LINK_TARGET_RE.findall(without_fences(text))


def is_same_page_fragment(destination: str) -> bool:
    return destination.strip().startswith("#")


def protected_link_destinations(text: str) -> list[str]:
    return [destination for destination in link_destinations(text) if not is_same_page_fragment(destination)]


def link_kinds(text: str) -> list[str]:
    return ["fragment" if is_same_page_fragment(destination) else "protected" for destination in link_destinations(text)]


def github_slug_base(heading: str) -> str:
    """Approximate GitHub's heading-slug rules for Markdown headings."""
    heading = re.sub(r"`([^`]+)`", r"\1", heading)
    heading = MARKDOWN_LINK_TEXT_RE.sub(r"\1", heading)
    heading = HTML_TAG_RE.sub("", heading)
    heading = MARKDOWN_PUNCT_RE.sub("", heading)
    heading = html.unescape(heading).strip().lower()
    heading = SLUG_PUNCT_RE.sub("", heading)
    heading = WHITESPACE_RE.sub("-", heading)
    return heading


def heading_slugs(text: str) -> list[str]:
    slugs: list[str] = []
    seen: dict[str, int] = {}
    for match in HEADING_TEXT_RE.finditer(without_fences(text)):
        heading = re.sub(r"\s+#+\s*$", "", match.group(1)).strip()
        base = github_slug_base(heading)
        count = seen.get(base, 0)
        slug = base if count == 0 else f"{base}-{count}"
        seen[base] = count + 1
        slugs.append(slug)
    return slugs


def broken_same_page_fragments(text: str) -> list[str]:
    valid_slugs = set(heading_slugs(text))
    broken: list[str] = []
    for destination in link_destinations(text):
        if not is_same_page_fragment(destination):
            continue
        fragment = unquote(destination.strip()[1:])
        if fragment not in valid_slugs:
            broken.append(destination)
    return broken


def validate(source: str, output: str) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    comparisons = {
        "fenced code blocks": (fenced_blocks(source), fenced_blocks(output)),
        "inline code": (INLINE_CODE_RE.findall(without_fences(source)), INLINE_CODE_RE.findall(without_fences(output))),
        "URLs": (URL_RE.findall(source), URL_RE.findall(output)),
        "protected link destinations": (protected_link_destinations(source), protected_link_destinations(output)),
        "link structure": (link_kinds(source), link_kinds(output)),
        "literal tokens": (TOKEN_RE.findall(without_fences(source)), TOKEN_RE.findall(without_fences(output))),
        "heading levels": (HEADING_RE.findall(without_fences(source)), HEADING_RE.findall(without_fences(output))),
        "table dimensions": (table_dimensions(source), table_dimensions(output)),
        "frontmatter keys": (frontmatter_keys(source), frontmatter_keys(output)),
    }
    for label, (before, after) in comparisons.items():
        if before != after:
            errors.append(f"Changed {label}")

    broken_fragments = broken_same_page_fragments(output)
    if broken_fragments:
        errors.append("Unresolved same-page fragments: " + ", ".join(broken_fragments))

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
