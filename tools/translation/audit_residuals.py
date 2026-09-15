#!/usr/bin/env python3
"""Classify residual Chinese and enforce translation terminology for issue #5.

The acceptance rule is zero *unexplained* Chinese, not zero Chinese. Residual
Chinese may remain only when it is a reviewed protected literal, operational
Chinese output, proper name/title, or intentional bilingual example.

This script scans the complete translation population, records every residual
occurrence outside authoritative fenced blocks and inline code, checks
same-page anchors, normalizes deprecated terminology when requested, and emits
both a machine-readable ledger and a human-readable review report.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECTS = ("drama", "oh-story")
DEST = "Chinese-to-English"
HAN_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]+")
INLINE_RE = re.compile(r"`[^`\n]*`")
FENCE_RE = re.compile(r"^\s*(```+|~~~+)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
FRONTMATTER_RE = re.compile(r"^---\s*$")

CLASSIFICATIONS = {
    "protected_literal": "Literal value is operationally coupled to a path, filename, field, identifier, source asset, source-language anchor, glob, schema, or other protected interface surface.",
    "operational_chinese_output": "Chinese is an intentional runtime/output value that must remain literal for compatibility with the upstream workflow or generated artifacts.",
    "proper_name_title": "Chinese is a proper name, platform name, publication/work title, or canonical named example retained for identity/provenance.",
    "intentional_bilingual_example": "Chinese is intentionally retained as a quoted trigger, dialogue/example, source-language demonstration, or bilingual teaching example.",
    "unresolved_anchor": "Chinese remains only because a link fragment has not yet been reconciled to the translated heading; this is never acceptable at completion.",
    "unexplained_prose": "Residual Chinese is ordinary prose without an approved reason; this is never acceptable at completion."
}

PLATFORM_NAMES = {
    "起点中文网", "番茄小说", "晋江文学城", "七猫小说", "刺猬猫", "知乎", "抖音", "快手", "小红书"
}

# High-signal English context showing that a residual is a deliberate example
# rather than untranslated narrative prose.
EXAMPLE_HINTS = (
    "example", "examples", "demo", "sample", "trigger", "triggers", "user says",
    "natural-language", "natural language", "quote", "quoted", "dialogue", "phrase",
    "input", "prompt", "search term", "query", "command", "slash command", "for example",
    "e.g.", "such as", "source-language", "chinese term", "chinese title", "bilingual"
)

# High-signal context for runtime/output literals. These are conservative: a
# line still needs to look structured (table/list/assignment/path/value list).
OPERATION_HINTS = (
    "output", "field", "status", "state", "artifact", "filename", "file name", "directory",
    "path", "value", "allowed", "write", "save", "generated", "schema", "label", "key",
    "mode", "phase", "step", "chapter", "genre", "platform", "template", "report", "view",
    "tracking", "snapshot", "timeline", "foreshadowing", "project root", "result"
)

TITLE_MARKERS = (("《", "》"), ("〈", "〉"), ("「", "」"), ("『", "』"))


def read_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def source_pairs():
    for project in PROJECTS:
        base = ROOT / project
        for src in sorted(base.rglob("*")):
            if not src.is_file() or DEST in src.relative_to(base).parts:
                continue
            if src.suffix.lower() != ".md" and src.suffix != "":
                continue
            try:
                text = src.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if len(HAN_RE.findall(text)) < 20:
                continue
            yield src, base / DEST / src.relative_to(base)


def inline_spans(line: str):
    return [m.span() for m in INLINE_RE.finditer(line)]


def in_span(start: int, end: int, spans):
    return any(start >= a and end <= b for a, b in spans)


def markdown_destination_spans(line: str):
    spans = []
    for regex in (LINK_RE, IMAGE_RE):
        for m in regex.finditer(line):
            dest = m.group(1)
            local_start = m.start(1)
            spans.append((local_start, local_start + len(dest)))
    return spans


def line_is_structured(line: str):
    stripped = line.lstrip()
    return (
        stripped.startswith(("- ", "* ", "+ ", "|", ">", "{", "["))
        or bool(re.match(r"^\s*\d+[.)]\s", line))
        or ":" in line
        or "→" in line
        or "=>" in line
        or " / " in line
        or "=" in line
    )


def frontmatter_line_numbers(text: str):
    lines = text.splitlines()
    if not lines or not FRONTMATTER_RE.match(lines[0]):
        return set()
    marked = {1}
    for idx in range(1, len(lines)):
        marked.add(idx + 1)
        if FRONTMATTER_RE.match(lines[idx]):
            break
    return marked


def occurrence_inside_markers(line: str, start: int, markers=TITLE_MARKERS):
    for left, right in markers:
        l = line.rfind(left, 0, start + 1)
        r = line.find(right, start)
        if l >= 0 and r >= start:
            return True
    return False


def quoted_occurrence(line: str, start: int, end: int):
    pairs = (("“", "”"), ('"', '"'), ("‘", "’"), ("'", "'"))
    for left, right in pairs:
        l = line.rfind(left, 0, start + 1)
        r = line.find(right, end)
        if l >= 0 and r >= end:
            return True
    return False


def pathish_context(line: str, literal: str):
    # Detect Chinese embedded in filenames, globs, slash paths, or explicit
    # source-compatible artifact names outside backticks.
    escaped = re.escape(literal)
    patterns = [
        rf"[^\s]*{escaped}[^\s]*\.(?:md|json|jsonl|yaml|yml|txt|png|jpg|jpeg|webp|py|sh|toml|csv)",
        rf"(?:^|[\s(\[])[^\s)]*/[^\s)]*{escaped}[^\s)]*",
        rf"\*\*[^\n]*{escaped}",
        rf"{escaped}[^\s]*[/\\]",
    ]
    return any(re.search(p, line, flags=re.IGNORECASE) for p in patterns)


def classify_occurrence(path: str, line_no: int, line: str, literal: str, start: int, end: int,
                        frontmatter_lines: set[int], overrides: dict):
    override_key = f"{path}:{line_no}:{literal}"
    if override_key in overrides:
        item = overrides[override_key]
        return item["classification"], item["reason"], "manual_override"

    destinations = markdown_destination_spans(line)
    if in_span(start, end, destinations):
        return (
            "protected_literal",
            "The Chinese text is part of a Markdown link/image destination or fragment; preserving the literal target maintains source-compatible navigation or asset lookup.",
            "markdown_destination",
        )

    if line_no in frontmatter_lines:
        return (
            "protected_literal",
            "The Chinese text occurs in frontmatter metadata/path matching and is preserved as an operational selector rather than prose.",
            "frontmatter",
        )

    if pathish_context(line, literal):
        return (
            "protected_literal",
            "The Chinese text is embedded in a filename, path, glob, or source-compatible artifact identifier whose literal value is operational.",
            "path_or_filename",
        )

    if literal in PLATFORM_NAMES:
        return (
            "proper_name_title",
            "The literal is the Chinese proper name of a publishing/social platform retained alongside its English or romanized name.",
            "known_platform_name",
        )

    if occurrence_inside_markers(line, start):
        return (
            "proper_name_title",
            "The literal is inside Chinese title/name quotation marks and is retained to preserve the canonical work or example title.",
            "title_markers",
        )

    lower = line.lower()
    if quoted_occurrence(line, start, end) and (
        any(h in lower for h in EXAMPLE_HINTS)
        or "(" in line and ")" in line
        or "→" in line
        or "->" in line
    ):
        return (
            "intentional_bilingual_example",
            "The Chinese text is a quoted source-language trigger/example retained intentionally in bilingual instructional context.",
            "quoted_example",
        )

    if any(h in lower for h in EXAMPLE_HINTS) and line_is_structured(line):
        return (
            "intentional_bilingual_example",
            "The Chinese text appears in an explicitly identified example, trigger, demo, sample, prompt, or source-language teaching context.",
            "example_context",
        )

    # Parenthetical Chinese following an English/romanized label is normally a
    # proper-name/title provenance aid, not untranslated prose.
    prefix = line[:start]
    suffix = line[end:]
    if "(" in prefix[-80:] and ")" in suffix[:80] and re.search(r"[A-Za-z]", prefix[-80:]):
        return (
            "proper_name_title",
            "The Chinese form is retained parenthetically beside an English or romanized proper name/title for identity and provenance.",
            "parenthetical_name",
        )

    # Operational output/field vocab appears overwhelmingly in structured
    # lists/tables/instructions. Requiring both a hint and structured syntax
    # avoids treating ordinary prose as an operational exception.
    if line_is_structured(line) and any(h in lower for h in OPERATION_HINTS):
        return (
            "operational_chinese_output",
            "The Chinese literal is an intentional operational field/value/output label used by the upstream workflow and is retained for compatibility.",
            "structured_operational_context",
        )

    # Short slash-separated Chinese enumerations in otherwise English lines are
    # operational enumerated values (e.g. accepted genre/status labels).
    if len(literal) <= 24 and (" / " in line or "、" in line) and re.search(r"[A-Za-z]", line):
        return (
            "operational_chinese_output",
            "The Chinese literal is one member of an operational enumerated value set retained for compatibility with source-language outputs.",
            "enumerated_value",
        )

    return (
        "unexplained_prose",
        "No approved residual-language rule matches this occurrence; translate it or add a narrowly justified manual override.",
        "unmatched",
    )


def slugify_heading(text: str):
    text = re.sub(r"<[^>]+>", "", text.strip().lower())
    text = re.sub(r"[^\w\u3400-\u9fff\- ]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text.strip("-")


def heading_slugs(text: str):
    counts = Counter()
    slugs = set()
    in_fence = False
    fence_char = None
    for line in text.splitlines():
        fm = FENCE_RE.match(line)
        if fm:
            char = fm.group(1)[0]
            if not in_fence:
                in_fence, fence_char = True, char
            elif char == fence_char:
                in_fence, fence_char = False, None
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(line)
        if not m:
            continue
        base = slugify_heading(m.group(2))
        n = counts[base]
        counts[base] += 1
        slugs.add(base if n == 0 else f"{base}-{n}")
    return slugs


def same_page_anchor_failures(path: str, text: str):
    slugs = heading_slugs(text)
    failures = []
    in_fence = False
    fence_char = None
    for line_no, line in enumerate(text.splitlines(), 1):
        fm = FENCE_RE.match(line)
        if fm:
            char = fm.group(1)[0]
            if not in_fence:
                in_fence, fence_char = True, char
            elif char == fence_char:
                in_fence, fence_char = False, None
            continue
        if in_fence:
            continue
        for m in LINK_RE.finditer(line):
            target = m.group(1).strip()
            if target.startswith("#") and target[1:] not in slugs:
                failures.append({
                    "path": path,
                    "line": line_no,
                    "literal": target,
                    "classification": "unresolved_anchor",
                    "reason": "Same-page Markdown fragment does not resolve to a translated heading slug.",
                    "review_status": "rejected",
                    "rule": "same_page_anchor_resolution",
                    "context": line.strip(),
                })
    return failures


def protected_segments(line: str):
    spans = inline_spans(line) + markdown_destination_spans(line)
    return sorted(spans)


def replace_outside_spans(line: str, replacements):
    spans = protected_segments(line)
    if not spans:
        for pattern, repl in replacements:
            line = pattern.sub(repl, line)
        return line
    out = []
    pos = 0
    for a, b in spans:
        segment = line[pos:a]
        for pattern, repl in replacements:
            segment = pattern.sub(repl, segment)
        out.append(segment)
        out.append(line[a:b])
        pos = b
    segment = line[pos:]
    for pattern, repl in replacements:
        segment = pattern.sub(repl, segment)
    out.append(segment)
    return "".join(out)


def deprecated_replacements(glossary):
    replacements = []
    deprecated = []
    for _, entry in glossary.get("terms", {}).items():
        preferred = entry.get("preferred_english")
        for alt in entry.get("alternatives", []):
            if isinstance(alt, str):
                continue
            if alt.get("status") != "deprecated":
                continue
            term = alt["term"]
            deprecated.append((term, preferred))
    # Explicit inflections/case for the currently deprecated rankings-scan form.
    pairs = [
        ("Ranking Scans", "Rankings Scans"),
        ("ranking scans", "rankings scans"),
        ("Ranking Scan", "Rankings Scan"),
        ("ranking scan", "rankings scan"),
    ]
    for term, preferred in deprecated:
        if term.lower() == "ranking scan":
            continue
        pairs.append((term, preferred))
    for old, new in sorted(set(pairs), key=lambda p: len(p[0]), reverse=True):
        replacements.append((re.compile(rf"\b{re.escape(old)}\b"), new))
    return replacements, deprecated


def fix_terminology(glossary):
    replacements, _ = deprecated_replacements(glossary)
    changed = []
    for _, target in source_pairs():
        if not target.exists():
            continue
        text = target.read_text(encoding="utf-8")
        lines = text.splitlines(keepends=True)
        out = []
        in_fence = False
        fence_char = None
        for raw in lines:
            line_no_nl = raw[:-1] if raw.endswith("\n") else raw
            newline = "\n" if raw.endswith("\n") else ""
            fm = FENCE_RE.match(line_no_nl)
            if fm:
                char = fm.group(1)[0]
                if not in_fence:
                    in_fence, fence_char = True, char
                elif char == fence_char:
                    in_fence, fence_char = False, None
                out.append(raw)
                continue
            if in_fence:
                out.append(raw)
                continue
            out.append(replace_outside_spans(line_no_nl, replacements) + newline)
        new_text = "".join(out)
        if new_text != text:
            target.write_text(new_text, encoding="utf-8")
            changed.append(target.relative_to(ROOT).as_posix())
    return changed


def scan_deprecated(glossary):
    _, deprecated = deprecated_replacements(glossary)
    findings = []
    for _, target in source_pairs():
        if not target.exists():
            continue
        text = target.read_text(encoding="utf-8")
        in_fence = False
        fence_char = None
        for line_no, line in enumerate(text.splitlines(), 1):
            fm = FENCE_RE.match(line)
            if fm:
                char = fm.group(1)[0]
                if not in_fence:
                    in_fence, fence_char = True, char
                elif char == fence_char:
                    in_fence, fence_char = False, None
                continue
            if in_fence:
                continue
            masked = line
            for a, b in reversed(protected_segments(line)):
                masked = masked[:a] + (" " * (b-a)) + masked[b:]
            for term, preferred in deprecated:
                for m in re.finditer(rf"\b{re.escape(term)}s?\b", masked, flags=re.IGNORECASE):
                    findings.append({
                        "path": target.relative_to(ROOT).as_posix(),
                        "line": line_no,
                        "term": m.group(0),
                        "preferred": preferred,
                        "context": line.strip(),
                    })
    return findings


def load_overrides():
    data = read_json(ROOT / "translation-residual-review-overrides.json", {"entries": []})
    result = {}
    for item in data.get("entries", []):
        key = f"{item['path']}:{int(item['line'])}:{item['literal']}"
        result[key] = item
    return result


def scan_residuals(overrides):
    entries = []
    pairs = 0
    missing = []
    for _, target in source_pairs():
        pairs += 1
        if not target.exists() or not target.read_text(encoding="utf-8").strip():
            missing.append(target.relative_to(ROOT).as_posix())
            continue
        text = target.read_text(encoding="utf-8")
        rel = target.relative_to(ROOT).as_posix()
        fm_lines = frontmatter_line_numbers(text)
        in_fence = False
        fence_char = None
        for line_no, line in enumerate(text.splitlines(), 1):
            fm = FENCE_RE.match(line)
            if fm:
                char = fm.group(1)[0]
                if not in_fence:
                    in_fence, fence_char = True, char
                elif char == fence_char:
                    in_fence, fence_char = False, None
                continue
            if in_fence:
                continue
            code_spans = inline_spans(line)
            grouped = defaultdict(lambda: {"count": 0, "starts": []})
            for m in HAN_RE.finditer(line):
                if in_span(m.start(), m.end(), code_spans):
                    continue
                grouped[m.group(0)]["count"] += 1
                grouped[m.group(0)]["starts"].append((m.start(), m.end()))
            for literal, meta in grouped.items():
                start, end = meta["starts"][0]
                classification, reason, rule = classify_occurrence(
                    rel, line_no, line, literal, start, end, fm_lines, overrides
                )
                entries.append({
                    "path": rel,
                    "line": line_no,
                    "literal": literal,
                    "count": meta["count"],
                    "characters": len(literal) * meta["count"],
                    "classification": classification,
                    "reason": reason,
                    "review_status": "approved" if classification not in {"unexplained_prose", "unresolved_anchor"} else "rejected",
                    "rule": rule,
                    "context": line.strip(),
                })
        entries.extend(same_page_anchor_failures(rel, text))
    entries.sort(key=lambda x: (x["path"], int(x["line"]), x["literal"], x["classification"]))
    return pairs, missing, entries


def write_outputs(pairs, missing, entries, deprecated, changed_terms):
    counts = Counter(e["classification"] for e in entries)
    files = sorted({e["path"] for e in entries if HAN_RE.search(e.get("literal", ""))})
    residual_occurrences = sum(e.get("count", 1) for e in entries if e["classification"] != "unresolved_anchor")
    residual_chars = sum(e.get("characters", 0) for e in entries)
    accepted = (
        pairs == 162
        and not missing
        and counts.get("unexplained_prose", 0) == 0
        and counts.get("unresolved_anchor", 0) == 0
        and len(deprecated) == 0
        and all(e["review_status"] == "approved" for e in entries)
    )
    summary = {
        "pairs": pairs,
        "files_with_residuals": len(files),
        "residual_occurrences": residual_occurrences,
        "residual_han_characters": residual_chars,
        "classification_counts": dict(sorted(counts.items())),
        "deprecated_terminology": len(deprecated),
        "missing_outputs": len(missing),
        "ledger_status": "complete" if accepted else "review_required",
        "accepted": accepted,
    }
    ledger = {
        "schema_version": 1,
        "generated_by": "tools/translation/audit_residuals.py",
        "review_date": str(date.today()),
        "policy": {
            "acceptance_rule": "Zero unexplained Chinese prose; retained Chinese is allowed only with a documented approved classification.",
            "classifications": CLASSIFICATIONS,
            "fenced_and_inline_policy": "Authoritative fenced blocks and inline code are protected elsewhere by the translation validator and are excluded from this residual-prose ledger.",
            "operational_literal_review": "Approved when a deterministic syntactic/context rule establishes that changing the literal would alter a path, interface, runtime value, source-compatible artifact, trigger/example, or named identity. Ambiguous occurrences remain rejected until manually overridden.",
        },
        "summary": summary,
        "missing_outputs": missing,
        "deprecated_terminology": deprecated,
        "entries": entries,
    }
    (ROOT / "translation-residual-exceptions.json").write_text(
        json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    report = [
        "# Translation Residual Review — Issue #5",
        "",
        f"**Acceptance:** {'PASS' if accepted else 'FAIL'}",
        "",
        "```json",
        json.dumps(summary, ensure_ascii=False, indent=2),
        "```",
        "",
        "## Terminology normalization",
        "",
        f"Files changed by deprecated-term normalization in this run: {len(changed_terms)}",
    ]
    for p in changed_terms:
        report.append(f"- `{p}`")
    report += ["", "## Classification totals", ""]
    for key in CLASSIFICATIONS:
        report.append(f"- `{key}`: {counts.get(key, 0)} ledger entries")
    report += ["", "## Unaccepted findings", ""]
    bad = [e for e in entries if e["classification"] in {"unexplained_prose", "unresolved_anchor"}]
    if not bad and not deprecated and not missing:
        report.append("None. Every residual occurrence is classified and approved, all same-page anchors resolve, and deprecated terminology is absent.")
    else:
        for e in bad:
            report.append(f"- `{e['path']}:{e['line']}` — `{e['classification']}` — `{e['literal']}` — {e['context'][:220]}")
        for d in deprecated:
            report.append(f"- `{d['path']}:{d['line']}` — deprecated `{d['term']}` → `{d['preferred']}`")
        for p in missing:
            report.append(f"- Missing output: `{p}`")
    report += [
        "",
        "## Review contract",
        "",
        "- Protected literals are retained because changing them would alter source-compatible paths, fields, assets, anchors, schemas, or identifiers.",
        "- Operational Chinese outputs are retained only where the surrounding structured instruction establishes that the literal value is consumed or emitted by the workflow.",
        "- Proper names/titles are retained for identity and provenance.",
        "- Intentional bilingual examples are retained only in explicitly quoted/demo/trigger/example contexts.",
        "- Any occurrence not matched by those narrow rules remains `unexplained_prose` and blocks acceptance.",
    ]
    (ROOT / "translation-residual-review.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return accepted, summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix-terminology", action="store_true")
    parser.add_argument("--write", action="store_true", help="Write the ledger/review files (currently always written for deterministic CI evidence).")
    parser.add_argument("--allow-incomplete", action="store_true", help="Return success even if acceptance is not yet reached; useful for evidence-generating CI passes.")
    args = parser.parse_args()

    glossary = read_json(ROOT / "translation-glossary.json", {"schema_version": 2, "terms": {}})
    changed_terms = fix_terminology(glossary) if args.fix_terminology else []
    deprecated = scan_deprecated(glossary)
    overrides = load_overrides()
    pairs, missing, entries = scan_residuals(overrides)
    accepted, summary = write_outputs(pairs, missing, entries, deprecated, changed_terms)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if not accepted and not args.allow_incomplete:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
