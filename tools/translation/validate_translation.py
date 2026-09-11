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
URL_RE = re.compile(r"https?://[^\s)<>{}\]\[|]+")
LINK_TARGET_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
TOKEN_RE = re.compile(r"\$\{[^}]+\}|\{\{[^}]+\}\}|(?<!\w)--[\w-]+|(?<!\w)\$[\w-]+")
HEADING_RE = re.compile(r"(?m)^(#{1,6})\s+")
HEADING_TEXT_RE = re.compile(r"(?m)^#{1,6}\s+(.+?)\s*$")
LIST_ITEM_RE = re.compile(r"^(?P<indent>[ \t]*)(?P<marker>[-+*]|\d+[.)])\s+(?P<checkbox>\[[ xX]\]\s+)?")
BLOCKQUOTE_RE = re.compile(r"^[ \t]*(?P<marks>>+)(?:[ \t]+|$)")
HTML_COMMENT_TOKEN_RE = re.compile(r"<!--|-->")
ZH_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
MARKDOWN_LINK_TEXT_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
HTML_TAG_RE = re.compile(r"<[^>]+>")
MARKDOWN_PUNCT_RE = re.compile(r"[*_~]")
SLUG_PUNCT_RE = re.compile(r"[^\w\s-]", re.UNICODE)
WHITESPACE_RE = re.compile(r"\s+")
TRANSLATION_COMPANION_MARKER = "<!-- translation-companion: non-executable -->"
TRANSLATION_COMPANION_LANGUAGES = {"text", "txt", "plaintext"}
TRAILING_URL_PUNCTUATION = ".,;:!?\"'"


@dataclass
class ValidationResult:
    valid: bool
    errors: list[str]
    warnings: list[str]
    source_chinese_characters: int
    output_chinese_characters: int


@dataclass(frozen=True)
class FenceRecord:
    raw: str
    info: str
    start: int
    end: int


def fence_records(text: str) -> list[FenceRecord]:
    records: list[FenceRecord] = []
    for match in FENCE_RE.finditer(text):
        opening = match.group(1).strip()
        opener = re.match(r"(`{3,}|~{3,})(.*)$", opening)
        info = opener.group(2).strip() if opener else ""
        records.append(FenceRecord(match.group(0), info, match.start(), match.end()))
    return records


def fenced_blocks(text: str) -> list[str]:
    return [record.raw for record in fence_records(text)]


def companion_language(info: str) -> str:
    return info.split()[0].lower() if info else ""


def authoritative_fenced_blocks(text: str) -> tuple[list[str], list[str]]:
    """Return source-authoritative fences, excluding valid marked text companions."""
    authoritative: list[str] = []
    errors: list[str] = []
    previous_record: FenceRecord | None = None
    previous_was_companion = False
    companions = 0

    for record in fence_records(text):
        previous_end = previous_record.end if previous_record else 0
        between = text[previous_end : record.start]
        marker_present = TRANSLATION_COMPANION_MARKER in between

        if marker_present:
            companions += 1
            if previous_record is None or previous_was_companion:
                errors.append("Translation companion has no preceding authoritative fenced block")
            if between.strip() != TRANSLATION_COMPANION_MARKER:
                errors.append("Translation companion marker must be the only non-whitespace content between fences")
            if companion_language(record.info) not in TRANSLATION_COMPANION_LANGUAGES:
                errors.append("Translation companion must use a non-executable text fence")
            previous_was_companion = True
        else:
            authoritative.append(record.raw)
            previous_was_companion = False

        previous_record = record

    outside_fences = without_fences(text)
    marker_count = outside_fences.count(TRANSLATION_COMPANION_MARKER)
    if marker_count != companions:
        errors.append("Translation companion marker is not attached to exactly one fenced companion")

    return authoritative, errors


def without_fences(text: str) -> str:
    return FENCE_RE.sub("", text)


def normalized_urls(text: str) -> list[str]:
    """Extract URLs while ignoring adjacent prose/table punctuation."""
    urls: list[str] = []
    for match in URL_RE.finditer(text):
        value = match.group(0).rstrip(TRAILING_URL_PUNCTUATION)
        if value:
            urls.append(value)
    return urls


def protected_tokens(text: str) -> list[str]:
    """Extract protected CLI/template tokens without treating URL text as tokens."""
    outside = without_fences(text)
    outside = URL_RE.sub("", outside)
    return TOKEN_RE.findall(outside)


def _pipe_positions(line: str) -> list[int]:
    """Return structural pipe positions, ignoring escaped pipes and inline-code pipes."""
    positions: list[int] = []
    code_delimiter: int | None = None
    index = 0
    while index < len(line):
        char = line[index]
        if char == "`":
            end = index
            while end < len(line) and line[end] == "`":
                end += 1
            run = end - index
            if code_delimiter is None:
                code_delimiter = run
            elif code_delimiter == run:
                code_delimiter = None
            index = end
            continue
        if char == "|" and code_delimiter is None:
            backslashes = 0
            scan = index - 1
            while scan >= 0 and line[scan] == "\\":
                backslashes += 1
                scan -= 1
            if backslashes % 2 == 0:
                positions.append(index)
        index += 1
    return positions


def table_row_cells(line: str) -> int | None:
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return None
    positions = _pipe_positions(stripped)
    if len(positions) < 2 or positions[0] != 0 or positions[-1] != len(stripped) - 1:
        return None
    return len(positions) - 1


def table_signatures(text: str) -> list[tuple[int, ...]]:
    """Return one cell-count tuple per contiguous Markdown table."""
    tables: list[tuple[int, ...]] = []
    current: list[int] = []
    for line in without_fences(text).splitlines():
        cells = table_row_cells(line)
        if cells is None:
            if current:
                tables.append(tuple(current))
                current = []
            continue
        current.append(cells)
    if current:
        tables.append(tuple(current))
    return tables


def table_dimensions(text: str) -> list[int]:
    """Backward-compatible flattened table row dimensions."""
    return [cells for table in table_signatures(text) for cells in table]


def list_signature(text: str) -> list[tuple[int, str, bool]]:
    """Compare list nesting/type while allowing bullet glyph/ordinal renumbering."""
    signature: list[tuple[int, str, bool]] = []
    for line in without_fences(text).splitlines():
        match = LIST_ITEM_RE.match(line)
        if not match:
            continue
        indent = len(match.group("indent").expandtabs(4))
        marker = match.group("marker")
        kind = "ordered" if marker[0].isdigit() else "unordered"
        checkbox = bool(match.group("checkbox"))
        signature.append((indent, kind, checkbox))
    return signature


def blockquote_signature(text: str) -> list[int]:
    """Compare blockquote line count and nesting depth, not translated contents."""
    signature: list[int] = []
    for line in without_fences(text).splitlines():
        match = BLOCKQUOTE_RE.match(line)
        if match:
            signature.append(len(match.group("marks")))
    return signature


def html_comment_framing(text: str) -> list[str]:
    """Compare comment framing while ignoring the approved translation marker."""
    outside = without_fences(text).replace(TRANSLATION_COMPANION_MARKER, "")
    return HTML_COMMENT_TOKEN_RE.findall(outside)


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
    output_authoritative_fences, companion_errors = authoritative_fenced_blocks(output)
    errors.extend(companion_errors)

    comparisons = {
        "fenced code blocks": (fenced_blocks(source), output_authoritative_fences),
        "inline code": (INLINE_CODE_RE.findall(without_fences(source)), INLINE_CODE_RE.findall(without_fences(output))),
        "URLs": (normalized_urls(source), normalized_urls(output)),
        "protected link destinations": (protected_link_destinations(source), protected_link_destinations(output)),
        "link structure": (link_kinds(source), link_kinds(output)),
        "protected tokens": (protected_tokens(source), protected_tokens(output)),
        "heading levels": (HEADING_RE.findall(without_fences(source)), HEADING_RE.findall(without_fences(output))),
        "table structure": (table_signatures(source), table_signatures(output)),
        "list structure": (list_signature(source), list_signature(output)),
        "blockquote structure": (blockquote_signature(source), blockquote_signature(output)),
        "HTML comment framing": (html_comment_framing(source), html_comment_framing(output)),
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
