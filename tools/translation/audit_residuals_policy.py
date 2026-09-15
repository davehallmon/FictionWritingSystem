#!/usr/bin/env python3
"""Issue #5 policy layer for the residual-audit engine.

Keeps the scanning/reporting engine small while applying the approved project
policy: zero unexplained Chinese prose, not zero Chinese. This layer fixes the
population-discovery character count, recognizes structured placeholders and
bilingual examples more precisely, normalizes deprecated `ranking scan`
inflections case-insensitively, and writes a compact unaccepted-findings file
for review iterations.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import audit_residuals as base

ROOT = base.ROOT


def source_pairs_v2():
    for project in base.PROJECTS:
        project_root = ROOT / project
        for src in sorted(project_root.rglob("*")):
            if not src.is_file() or base.DEST in src.relative_to(project_root).parts:
                continue
            if src.suffix.lower() != ".md" and src.suffix != "":
                continue
            try:
                text = src.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            han_chars = sum(len(m.group(0)) for m in base.HAN_RE.finditer(text))
            if han_chars < 20:
                continue
            yield src, project_root / base.DEST / src.relative_to(project_root)


def inside_braces(line: str, start: int, end: int) -> bool:
    left = line.rfind("{", 0, start + 1)
    right = line.find("}", end)
    return left >= 0 and right >= end


def english_word_count(line: str) -> int:
    return len(re.findall(r"[A-Za-z][A-Za-z'-]+", line))


def classify_v2(path, line_no, line, literal, start, end, frontmatter_lines, overrides):
    classification, reason, rule = ORIGINAL_CLASSIFY(
        path, line_no, line, literal, start, end, frontmatter_lines, overrides
    )
    if classification != "unexplained_prose":
        return classification, reason, rule

    lower = line.lower()
    han_chars = sum(len(m.group(0)) for m in base.HAN_RE.finditer(line))
    words = english_word_count(line)

    # Template placeholders and source-compatible field/value slots must remain
    # literal because downstream prompts/parsers expect the Chinese vocabulary.
    if inside_braces(line, start, end):
        return (
            "operational_chinese_output",
            "The Chinese text is inside a template placeholder/value slot and is retained as an operational source-compatible field or enumerated value.",
            "template_placeholder",
        )

    # Explicit editorial examples are intentionally bilingual even when the
    # Chinese example itself is not followed by an English gloss on that line.
    example_labels = (
        "prohibited:", "correct:", "wrong:", "right:", "bad example", "good example",
        "incorrect:", "preferred:", "anti-pattern", "counterexample", "example sentence",
    )
    if any(label in lower for label in example_labels):
        return (
            "intentional_bilingual_example",
            "The line explicitly labels the retained Chinese as a correct/incorrect/prohibited/example sentence used for source-language instruction.",
            "labeled_bilingual_example",
        )

    # A quoted Chinese token embedded in otherwise translated operational prose
    # is a literal value or source-language example, not untranslated narration.
    if base.quoted_occurrence(line, start, end) and words >= 3:
        if any(h in lower for h in base.OPERATION_HINTS) or any(
            h in lower for h in ("mark", "marked", "choice", "choices", "section", "heading", "read", "write", "field")
        ):
            return (
                "operational_chinese_output",
                "The quoted Chinese text is an explicit operational field/value/section label embedded in translated instructions and must remain literal for compatibility.",
                "quoted_operational_literal",
            )
        return (
            "intentional_bilingual_example",
            "The quoted Chinese text is intentionally retained inside otherwise translated English as a source-language example.",
            "embedded_quoted_example",
        )

    # Chinese full-width field syntax such as `输入参考图：无（...）` is often
    # intentionally un-backticked in prose. Treat it as an operational literal
    # when the surrounding English establishes a field/value contract.
    if "：" in line and words >= 3 and any(
        h in lower for h in ("field", "value", "use", "only when", "mark", "write", "output", "status", "state")
    ):
        return (
            "operational_chinese_output",
            "The Chinese text is part of an explicitly described source-language field/value contract embedded in translated prose.",
            "fullwidth_field_contract",
        )

    # Tables/lists with English labels and short Chinese literals are structured
    # operational contracts or bilingual examples. This intentionally requires
    # translated English context so wholly untranslated Chinese lines still fail.
    if base.line_is_structured(line) and words >= 2 and han_chars <= 120:
        if any(h in lower for h in ("example", "demo", "sample", "prohibited", "correct", "dialogue")):
            return (
                "intentional_bilingual_example",
                "The structured translated line contains a retained Chinese example/demo value for source-language instruction.",
                "structured_bilingual_example",
            )
        return (
            "operational_chinese_output",
            "The structured translated line contains a short Chinese field, state, label, or enumerated output value retained for source-workflow compatibility.",
            "structured_embedded_literal",
        )

    # Short Chinese tokens embedded in a clearly English sentence are retained
    # literals. Long or predominantly Chinese sentences do not qualify and stay
    # rejected for manual translation/review.
    if words >= 6 and han_chars <= 40:
        return (
            "operational_chinese_output",
            "A short source-language literal is embedded in otherwise fully translated English operational prose; the Chinese value is retained intentionally for compatibility or identification.",
            "english_context_literal",
        )

    return classification, reason, rule


def deprecated_replacements_v2(glossary):
    replacements, deprecated = ORIGINAL_DEPRECATED(glossary)

    def rankings_repl(match):
        text = match.group(0)
        plural_scan = text.lower().endswith("scans")
        replacement = "rankings scans" if plural_scan else "rankings scan"
        if text[0].isupper():
            replacement = replacement[0].upper() + replacement[1:]
        return replacement

    # Insert the case-insensitive rule first so title-case variants like
    # `Ranking scan` and `Ranking scans` are normalized too.
    rule = (re.compile(r"\branking scans?\b", flags=re.IGNORECASE), rankings_repl)
    return [rule] + replacements, deprecated


def write_outputs_v2(pairs, missing, entries, deprecated, changed_terms):
    accepted, summary = ORIGINAL_WRITE(pairs, missing, entries, deprecated, changed_terms)
    unaccepted = [
        e for e in entries
        if e.get("classification") in {"unexplained_prose", "unresolved_anchor"}
        or e.get("review_status") != "approved"
    ]
    payload = {
        "summary": summary,
        "unaccepted_count": len(unaccepted),
        "deprecated_terminology": deprecated,
        "missing_outputs": missing,
        "entries": unaccepted,
    }
    (ROOT / "translation-residual-unaccepted.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return accepted, summary


ORIGINAL_CLASSIFY = base.classify_occurrence
ORIGINAL_DEPRECATED = base.deprecated_replacements
ORIGINAL_WRITE = base.write_outputs
base.source_pairs = source_pairs_v2
base.classify_occurrence = classify_v2
base.deprecated_replacements = deprecated_replacements_v2
base.write_outputs = write_outputs_v2


if __name__ == "__main__":
    base.main()
