#!/usr/bin/env python3
"""Audit residual Chinese and terminology drift across translated artifacts."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from tools.translation.build_manifest import DEFAULT_ROOTS, build_manifest
from tools.translation.validate_translation import ZH_RE, fence_records

HAN_SPAN_RE = re.compile(
    r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]+"
    r"(?:[，。！？、；：“”‘’（）《》·…—\-+/=:%0-9A-Za-z_]*"
    r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]+)*"
)
FRAGMENT_RE = re.compile(r"\]\(#([^)]*)\)")
ALLOWED_CLASSIFICATIONS = {
    "protected_literal",
    "operational_chinese_output",
    "proper_name_or_title",
    "intentional_bilingual_example",
}
FORBIDDEN_CLASSIFICATIONS = {"unresolved_anchor", "unexplained_prose"}


def mask_range(chars: list[str], start: int, end: int) -> None:
    for index in range(start, end):
        if chars[index] != "\n":
            chars[index] = " "


def mask_inline_code_spans(chars: list[str]) -> None:
    """Mask CommonMark-style backtick spans, including spans that cross line breaks."""
    text = "".join(chars)
    opener_start: int | None = None
    opener_len = 0
    index = 0
    while index < len(text):
        if text[index] != "`":
            index += 1
            continue
        end = index
        while end < len(text) and text[end] == "`":
            end += 1
        run_len = end - index
        if run_len >= 3:
            index = end
            continue
        if opener_start is None:
            opener_start = index
            opener_len = run_len
        elif run_len == opener_len:
            mask_range(chars, opener_start, end)
            opener_start = None
            opener_len = 0
        index = end


def mask_governed_regions(text: str) -> str:
    """Mask authoritative fences and inline code while preserving line numbers."""
    chars = list(text)
    for record in fence_records(text):
        mask_range(chars, record.start, record.end)
    mask_inline_code_spans(chars)
    return "".join(chars)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def line_text(text: str, line: int) -> str:
    lines = text.splitlines()
    if 1 <= line <= len(lines):
        return lines[line - 1].strip()
    return ""


def is_unresolved_fragment_line(line: str, literal: str) -> bool:
    for fragment in FRAGMENT_RE.findall(line):
        if literal in fragment and ZH_RE.search(fragment):
            return True
    return False


def residual_occurrences(path: str, text: str) -> list[dict]:
    masked = mask_governed_regions(text)
    occurrences: list[dict] = []
    for match in HAN_SPAN_RE.finditer(masked):
        literal = match.group(0)
        line = line_number(masked, match.start())
        context = line_text(text, line)
        occurrences.append(
            {
                "path": path,
                "line": line,
                "literal": literal,
                "characters": len(ZH_RE.findall(literal)),
                "context": context,
                "auto_classification": (
                    "unresolved_anchor" if is_unresolved_fragment_line(context, literal) else None
                ),
            }
        )
    return occurrences


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def ledger_index(ledger: dict) -> tuple[dict[tuple[str, str], dict], list[str]]:
    index: dict[tuple[str, str], dict] = {}
    errors: list[str] = []
    for entry in ledger.get("entries", []):
        key = (entry.get("path", ""), entry.get("literal", ""))
        if not all(key):
            errors.append("Ledger entry is missing path or literal")
            continue
        if key in index:
            errors.append(f"Duplicate ledger entry for {key[0]} :: {key[1]}")
            continue
        index[key] = entry
    return index, errors


def classify_residuals(occurrences: list[dict], ledger: dict) -> tuple[list[dict], list[str]]:
    index, errors = ledger_index(ledger)
    observed: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for occurrence in occurrences:
        observed[(occurrence["path"], occurrence["literal"])].append(occurrence)

    results: list[dict] = []
    used_keys: set[tuple[str, str]] = set()
    for key, group in observed.items():
        entry = index.get(key)
        for occurrence in group:
            result = dict(occurrence)
            if occurrence["auto_classification"] == "unresolved_anchor":
                result["classification"] = "unresolved_anchor"
                result["reason"] = "Chinese remains inside a same-page Markdown fragment"
                result["review_status"] = "automatic_failure"
            elif entry:
                result["classification"] = entry.get("classification")
                result["reason"] = entry.get("reason", "")
                result["review_status"] = entry.get("review", {}).get("status")
            else:
                result["classification"] = "unexplained_prose"
                result["reason"] = "No reviewed residual-language exception matches this occurrence"
                result["review_status"] = "unreviewed"
            results.append(result)

        if entry:
            used_keys.add(key)
            expected = entry.get("expected_count")
            if expected != len(group):
                errors.append(
                    f"Ledger count mismatch for {key[0]} :: {key[1]}: expected {expected}, observed {len(group)}"
                )
            declared_line = entry.get("line")
            observed_lines = {item["line"] for item in group}
            if declared_line not in observed_lines:
                errors.append(
                    f"Ledger line mismatch for {key[0]} :: {key[1]}: line {declared_line} not in {sorted(observed_lines)}"
                )
            classification = entry.get("classification")
            if classification not in ALLOWED_CLASSIFICATIONS | FORBIDDEN_CLASSIFICATIONS:
                errors.append(f"Unknown ledger classification {classification!r} for {key[0]} :: {key[1]}")
            review = entry.get("review", {})
            if review.get("status") != "reviewed":
                errors.append(f"Ledger entry is not reviewed: {key[0]} :: {key[1]}")
            if classification in {"protected_literal", "operational_chinese_output"} and review.get("operationally_safe") is not True:
                errors.append(f"Operational residual is not marked safe: {key[0]} :: {key[1]}")

    for key in sorted(set(index) - used_keys):
        errors.append(f"Stale ledger entry has no observed occurrence: {key[0]} :: {key[1]}")

    return results, errors


def terminology_occurrences(path: str, text: str, glossary: dict) -> list[dict]:
    masked = mask_governed_regions(text)
    findings: list[dict] = []
    for source_term, data in glossary.get("terms", {}).items():
        preferred = data.get("preferred_english")
        for phrase in data.get("deprecated_english", []):
            for match in re.finditer(re.escape(phrase), masked, flags=re.IGNORECASE):
                line = line_number(masked, match.start())
                findings.append(
                    {
                        "path": path,
                        "line": line,
                        "phrase": match.group(0),
                        "source_term": source_term,
                        "preferred": preferred,
                        "status": "deprecated",
                        "context": line_text(text, line),
                    }
                )
        for alternative in data.get("alternatives", []):
            if not isinstance(alternative, dict) or alternative.get("review_required") is not True:
                continue
            value = alternative.get("value", "")
            usage = alternative.get("usage", "")
            if not value:
                continue
            for match in re.finditer(re.escape(value), masked, flags=re.IGNORECASE):
                line = line_number(masked, match.start())
                findings.append(
                    {
                        "path": path,
                        "line": line,
                        "phrase": match.group(0),
                        "source_term": source_term,
                        "preferred": preferred,
                        "status": "review_alternative",
                        "usage": usage,
                        "context": line_text(text, line),
                    }
                )
    return findings


def audit(repo: Path) -> dict:
    manifest = build_manifest(repo, DEFAULT_ROOTS)
    ledger_path = repo / "translation-residual-exceptions.json"
    glossary_path = repo / "translation-glossary.json"
    ledger = load_json(ledger_path)
    glossary = load_json(glossary_path)

    residuals: list[dict] = []
    terminology: list[dict] = []
    missing_outputs: list[str] = []

    for record in manifest["files"]:
        destination = repo / record["destination"]
        if not destination.is_file():
            missing_outputs.append(record["destination"])
            continue
        text = destination.read_text(encoding="utf-8")
        residuals.extend(residual_occurrences(record["destination"], text))
        terminology.extend(terminology_occurrences(record["destination"], text, glossary))

    classified, ledger_errors = classify_residuals(residuals, ledger)
    class_counts = Counter(item["classification"] for item in classified)
    files_with_residuals = sorted({item["path"] for item in classified})
    residual_characters = sum(item["characters"] for item in classified)
    deprecated = [item for item in terminology if item["status"] == "deprecated"]
    alternatives = [item for item in terminology if item["status"] == "review_alternative"]

    failing_classifications = sum(class_counts.get(name, 0) for name in FORBIDDEN_CLASSIFICATIONS)
    status_complete = ledger.get("status") == "complete"
    errors = list(ledger_errors)
    if missing_outputs:
        errors.extend(f"Missing output: {path}" for path in missing_outputs)
    if deprecated:
        errors.append(f"Deprecated terminology occurrences remain: {len(deprecated)}")
    if failing_classifications:
        errors.append(f"Unaccepted residual occurrences remain: {failing_classifications}")
    if status_complete and (failing_classifications or ledger_errors or deprecated):
        errors.append("Residual ledger is marked complete but acceptance failures remain")

    return {
        "schema_version": 1,
        "summary": {
            "pairs": len(manifest["files"]),
            "files_with_residuals": len(files_with_residuals),
            "residual_occurrences": len(classified),
            "residual_han_characters": residual_characters,
            "classification_counts": dict(sorted(class_counts.items())),
            "deprecated_terminology": len(deprecated),
            "alternative_terminology_review": len(alternatives),
            "ledger_errors": len(ledger_errors),
            "missing_outputs": len(missing_outputs),
            "ledger_status": ledger.get("status"),
            "accepted": not errors and status_complete,
        },
        "files_with_residuals": files_with_residuals,
        "errors": errors,
        "residuals": classified,
        "terminology": terminology,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    parser.add_argument("--fail", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    report = audit(repo)
    serialized = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else repo / args.output
        output.write_text(serialized, encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    if args.fail and not report["summary"]["accepted"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
