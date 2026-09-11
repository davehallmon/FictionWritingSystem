#!/usr/bin/env python3
"""Validate invariant Markdown structures in a translated file."""

from __future__ import annotations

import argparse
import html
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import unquote

FENCE_RE = re.compile(r"(?ms)^([ \t]*(`{3,}|~{3,})[^\n]*\n).*?^[ \t]*\2[ \t]*$")
INLINE_CODE_RE = re.compile(r"(?<!`)`[^`\n]+`(?!`)")
URL_RE = re.compile(r"https?://[^\s)<>{}\]\[|]+")
LINK_TARGET_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
IMAGE_TARGET_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
TOKEN_RE = re.compile(r"\$\{[^}]+\}|\{\{[^}]+\}\}|(?<!\w)--[\w-]+|(?<!\w)\$[\w-]+")
HEADING_RE = re.compile(r"(?m)^(#{1,6})\s+")
HEADING_TEXT_RE = re.compile(r"(?m)^#{1,6}\s+(.+?)\s*$")
LIST_ITEM_RE = re.compile(r"^(?P<indent>[ \t]*)(?P<marker>[-+*]|\d+[.)])\s+(?P<checkbox>\[[ xX]\]\s+)?")
BLOCKQUOTE_RE = re.compile(r"^[ \t]*(?P<marks>>+)(?:[ \t]+|$)")
HTML_COMMENT_TOKEN_RE = re.compile(r"<!--|-->")
HORIZONTAL_RULE_RE = re.compile(r"^[ \t]*(?:\*\s*){3,}$|^[ \t]*(?:-\s*){3,}$|^[ \t]*(?:_\s*){3,}$")
FENCE_LINE_RE = re.compile(r"^[ \t]*(?P<marker>`{3,}|~{3,})(?P<info>.*)$")
ZH_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
MARKDOWN_LINK_TEXT_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
HTML_TAG_RE = re.compile(r"<[^>]+>")
MARKDOWN_PUNCT_RE = re.compile(r"[*_~]")
SLUG_PUNCT_RE = re.compile(r"[^\w\s-]", re.UNICODE)
WHITESPACE_RE = re.compile(r"\s+")
TRANSLATION_COMPANION_MARKER = "<!-- translation-companion: non-executable -->"
TRANSLATION_COMPANION_LANGUAGES = {"text", "txt", "plaintext"}
TRANSLATION_GUIDE_START = "<!-- translation-guide: non-executable -->"
TRANSLATION_GUIDE_END = "<!-- /translation-guide -->"
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


def strip_translation_guides(text: str) -> tuple[str, list[str]]:
    """Remove explicitly authorized non-executable guide regions from invariant comparison."""
    errors: list[str] = []
    output: list[str] = []
    cursor = 0
    while True:
        start = text.find(TRANSLATION_GUIDE_START, cursor)
        end = text.find(TRANSLATION_GUIDE_END, cursor)
        if start < 0:
            if end >= 0:
                errors.append("Translation guide end marker has no start marker")
            output.append(text[cursor:])
            break
        if end >= 0 and end < start:
            errors.append("Translation guide end marker appears before its start marker")
            output.append(text[cursor:end])
            cursor = end + len(TRANSLATION_GUIDE_END)
            continue
        output.append(text[cursor:start])
        end = text.find(TRANSLATION_GUIDE_END, start + len(TRANSLATION_GUIDE_START))
        if end < 0:
            errors.append("Translation guide start marker is not closed")
            output.append(text[start:])
            break
        body_start = start + len(TRANSLATION_GUIDE_START)
        body = text[body_start:end]
        if TRANSLATION_GUIDE_START in body:
            errors.append("Translation guide regions must not be nested")
        if fence_records(body):
            errors.append("Translation guide must not contain fenced blocks")
        output.append("\n")
        cursor = end + len(TRANSLATION_GUIDE_END)
    return "".join(output), errors


def comparison_text(text: str) -> tuple[str, list[str]]:
    return strip_translation_guides(text)


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


def inline_code_literals(text: str) -> list[str]:
    return INLINE_CODE_RE.findall(without_fences(text))


def is_protected_inline_literal(literal: str) -> bool:
    """Distinguish technical literals from localized linguistic examples in backticks."""
    value = literal[1:-1] if literal.startswith("`") and literal.endswith("`") else literal
    if re.search(r"[A-Za-z0-9_$]", value):
        return True
    if re.fullmatch(r"\[[^\]]+\]", value):
        return True
    if any(char in value for char in ("{", "}", "<", ">", "\\")):
        return True
    if value.startswith(("/", "./", "../")):
        return True
    return False


def protected_inline_literals(text: str) -> list[str]:
    return [literal for literal in inline_code_literals(text) if is_protected_inline_literal(literal)]


def counter_contains(required: Counter[str], actual: Counter[str]) -> bool:
    return all(actual[value] >= count for value, count in required.items())


def inline_code_preservation(source: str, output: str) -> tuple[bool, int, bool]:
    """Protect technical inline literal values; localized/additional backticks are formatting-only."""
    before_all = inline_code_literals(source)
    after_all = inline_code_literals(output)
    before = protected_inline_literals(source)
    after = protected_inline_literals(output)
    required = Counter(before)
    actual = Counter(after)
    preserved = counter_contains(required, actual)
    additions = max(0, len(after_all) - len(before_all))
    reordered = preserved and before != [value for value in after if value in required][: len(before)]
    return preserved, additions, reordered


def protected_token_preservation(source: str, output: str) -> tuple[bool, int, bool]:
    """Protect token values and multiplicity while allowing explanatory repeats and grammar reordering."""
    before = protected_tokens(source)
    after = protected_tokens(output)
    required = Counter(before)
    actual = Counter(after)
    additions = max(0, len(after) - len(before))
    if not counter_contains(required, actual):
        return False, additions, False
    allowed = set(before)
    if any(value not in allowed for value in after):
        return False, additions, False
    return True, additions, before != after[: len(before)]


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
    """Compare blockquote blocks by nesting depth, allowing line reflow within a block."""
    signature: list[int] = []
    in_block = False
    max_depth = 0
    for line in without_fences(text).splitlines():
        match = BLOCKQUOTE_RE.match(line)
        if match:
            in_block = True
            max_depth = max(max_depth, len(match.group("marks")))
            continue
        if in_block:
            signature.append(max_depth)
            in_block = False
            max_depth = 0
    if in_block:
        signature.append(max_depth)
    return signature


def html_comment_framing(text: str) -> list[str]:
    """Compare comment framing while ignoring approved translation markers."""
    outside = without_fences(text)
    outside = outside.replace(TRANSLATION_COMPANION_MARKER, "")
    outside = outside.replace(TRANSLATION_GUIDE_START, "").replace(TRANSLATION_GUIDE_END, "")
    return HTML_COMMENT_TOKEN_RE.findall(outside)


def horizontal_rule_signature(text: str) -> int:
    """Count structural horizontal rules, excluding YAML frontmatter delimiters."""
    outside = without_fences(text)
    lines = outside.splitlines()
    start = 0
    if len(lines) >= 2 and lines[0].strip() == "---":
        try:
            close = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
        except StopIteration:
            close = -1
        if close > 0:
            start = close + 1
    return sum(bool(HORIZONTAL_RULE_RE.match(line)) for line in lines[start:])


def fence_balance_errors(text: str) -> list[str]:
    """Report unclosed Markdown fences without interpreting fence bodies."""
    errors: list[str] = []
    opener_char: str | None = None
    opener_len = 0
    for line in text.splitlines():
        match = FENCE_LINE_RE.match(line)
        if not match:
            continue
        marker = match.group("marker")
        char = marker[0]
        length = len(marker)
        info = match.group("info").strip()
        if opener_char is None:
            opener_char = char
            opener_len = length
            continue
        if char == opener_char and length >= opener_len and not info:
            opener_char = None
            opener_len = 0
    if opener_char is not None:
        errors.append("Unclosed fenced block")
    return errors


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


def image_destinations(text: str) -> list[str]:
    return IMAGE_TARGET_RE.findall(without_fences(text))


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
    errors.extend(fence_balance_errors(output))

    source_compare, source_guide_errors = comparison_text(source)
    output_compare, output_guide_errors = comparison_text(output)
    errors.extend(source_guide_errors)
    errors.extend(output_guide_errors)

    inline_ok, inline_additions, inline_reordered = inline_code_preservation(source_compare, output_compare)
    if not inline_ok:
        errors.append("Changed protected inline literal values")
    else:
        if inline_additions:
            warnings.append(f"Output adds {inline_additions} inline-code formatting span(s)")
        if inline_reordered:
            warnings.append("Protected inline literals are reordered by translation grammar; values and multiplicity are preserved")

    tokens_ok, token_additions, token_reordered = protected_token_preservation(source_compare, output_compare)
    if not tokens_ok:
        errors.append("Changed protected tokens")
    else:
        if token_additions:
            warnings.append(f"Output repeats {token_additions} protected token(s) in explanatory text")
        if token_reordered:
            warnings.append("Protected tokens are reordered by translation grammar; values and multiplicity are preserved")

    comparisons = {
        "fenced code blocks": (fenced_blocks(source), output_authoritative_fences),
        "URLs": (normalized_urls(source_compare), normalized_urls(output_compare)),
        "protected link destinations": (protected_link_destinations(source_compare), protected_link_destinations(output_compare)),
        "link structure": (link_kinds(source_compare), link_kinds(output_compare)),
        "image targets": (image_destinations(source_compare), image_destinations(output_compare)),
        "heading levels": (HEADING_RE.findall(without_fences(source_compare)), HEADING_RE.findall(without_fences(output_compare))),
        "table structure": (table_signatures(source_compare), table_signatures(output_compare)),
        "list structure": (list_signature(source_compare), list_signature(output_compare)),
        "blockquote structure": (blockquote_signature(source_compare), blockquote_signature(output_compare)),
        "HTML comment framing": (html_comment_framing(source_compare), html_comment_framing(output_compare)),
        "horizontal-rule structure": (horizontal_rule_signature(source_compare), horizontal_rule_signature(output_compare)),
        "frontmatter keys": (frontmatter_keys(source_compare), frontmatter_keys(output_compare)),
    }
    for label, (before, after) in comparisons.items():
        if before != after:
            errors.append(f"Changed {label}")

    broken_fragments = broken_same_page_fragments(output_compare)
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
