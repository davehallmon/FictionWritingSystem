#!/usr/bin/env python3
"""Read-only population gate for the Chinese-to-English remediation release.

This is the permanent CI-facing checker introduced by issue #7. It does not
rewrite the residual ledger or translation outputs. It verifies that the
committed #5 exception ledger still exactly describes the current residual
Chinese population, that all 162 source/translation pairs pass the structural
validator, that same-page fragments resolve, and that deprecated terminology
has not reappeared.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

import audit_residuals_policy as residual_policy
from build_manifest import DEFAULT_ROOTS, destination_for, discover_sources, load_json
from validate_translation import validate

ROOT = Path(__file__).resolve().parents[2]
EXPECTED_TARGETS = 162
UNACCEPTED = {"unexplained_prose", "unresolved_anchor"}


def ledger_signature(entry: dict[str, Any]) -> tuple[Any, ...]:
    return (
        entry.get("path"),
        int(entry.get("line", 0)),
        entry.get("literal"),
        int(entry.get("count", 1)),
        int(entry.get("characters", 0)),
        entry.get("classification"),
        entry.get("review_status"),
        entry.get("rule"),
    )


def compact_entry(signature: tuple[Any, ...]) -> str:
    path, line, literal, count, characters, classification, review_status, rule = signature
    return (
        f"{path}:{line} literal={literal!r} count={count} chars={characters} "
        f"classification={classification} review={review_status} rule={rule}"
    )


def current_residual_scan() -> tuple[int, list[str], list[dict[str, Any]], list[dict[str, Any]]]:
    base = residual_policy.base
    overrides = base.load_overrides()
    pairs, missing, entries = base.scan_residuals(overrides)
    glossary = load_json(ROOT / "translation-glossary.json", {"schema_version": 2, "terms": {}})
    deprecated = base.scan_deprecated(glossary)
    return pairs, missing, entries, deprecated


def expected_residual_summary(entries: list[dict[str, Any]], deprecated: list[dict[str, Any]], missing: list[str]) -> dict[str, Any]:
    classifications = Counter(e.get("classification", "unknown") for e in entries)
    residual_entries = [e for e in entries if e.get("classification") != "unresolved_anchor"]
    paths = {
        e.get("path")
        for e in residual_entries
        if residual_policy.base.HAN_RE.search(str(e.get("literal", "")))
    }
    unaccepted = [
        e for e in entries
        if e.get("classification") in UNACCEPTED or e.get("review_status") != "approved"
    ]
    return {
        "pairs": EXPECTED_TARGETS,
        "files_with_residuals": len(paths),
        "residual_occurrences": sum(int(e.get("count", 1)) for e in residual_entries),
        "residual_han_characters": sum(int(e.get("characters", 0)) for e in entries),
        "classification_counts": dict(sorted(classifications.items())),
        "deprecated_terminology": len(deprecated),
        "missing_outputs": len(missing),
        "ledger_status": "complete" if not unaccepted and not deprecated and not missing else "review_required",
        "accepted": not unaccepted and not deprecated and not missing,
    }


def validate_population() -> tuple[list[dict[str, Any]], int]:
    failures: list[dict[str, Any]] = []
    warnings = 0
    sources = discover_sources(ROOT, tuple(DEFAULT_ROOTS))
    if len(sources) != EXPECTED_TARGETS:
        failures.append({
            "path": "<population>",
            "errors": [f"Expected {EXPECTED_TARGETS} source documents, discovered {len(sources)}"],
        })

    for source in sources:
        destination = destination_for(ROOT, source)
        source_rel = source.relative_to(ROOT).as_posix()
        destination_rel = destination.relative_to(ROOT).as_posix()
        if not destination.is_file():
            failures.append({"path": destination_rel, "source": source_rel, "errors": ["Destination is missing"]})
            continue
        result = validate(
            source.read_text(encoding="utf-8"),
            destination.read_text(encoding="utf-8"),
        )
        warnings += len(result.warnings)
        if not result.valid:
            failures.append({
                "path": destination_rel,
                "source": source_rel,
                "errors": result.errors,
            })
    return failures, warnings


def check_gate() -> tuple[bool, dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    validator_failures, validator_warnings = validate_population()
    failures.extend(validator_failures)

    ledger_path = ROOT / "translation-residual-exceptions.json"
    ledger = load_json(ledger_path, {})
    pairs, missing, current_entries, deprecated = current_residual_scan()

    if pairs != EXPECTED_TARGETS:
        failures.append({
            "path": "<residual-population>",
            "errors": [f"Expected {EXPECTED_TARGETS} residual-scan pairs, scanned {pairs}"],
        })

    if missing:
        failures.append({"path": "<residual-population>", "errors": [f"Missing outputs: {', '.join(missing[:20])}"]})

    if deprecated:
        for finding in deprecated[:20]:
            failures.append({
                "path": finding.get("path", "<terminology>"),
                "line": finding.get("line"),
                "errors": [f"Deprecated term {finding.get('term')!r}; prefer {finding.get('preferred')!r}"],
            })

    unaccepted = [
        e for e in current_entries
        if e.get("classification") in UNACCEPTED or e.get("review_status") != "approved"
    ]
    for entry in unaccepted[:20]:
        failures.append({
            "path": entry.get("path", "<residual>"),
            "line": entry.get("line"),
            "errors": [
                f"Unaccepted residual {entry.get('literal')!r}: {entry.get('classification')} ({entry.get('rule')})"
            ],
        })

    committed_entries = ledger.get("entries", [])
    current_counter = Counter(ledger_signature(e) for e in current_entries)
    committed_counter = Counter(ledger_signature(e) for e in committed_entries)
    new_or_changed = current_counter - committed_counter
    stale_or_removed = committed_counter - current_counter

    if new_or_changed:
        failures.append({
            "path": "translation-residual-exceptions.json",
            "errors": [
                "Current residual population contains ledger entries that are new or changed",
                *["NEW: " + compact_entry(sig) for sig in list(new_or_changed.elements())[:20]],
            ],
        })
    if stale_or_removed:
        failures.append({
            "path": "translation-residual-exceptions.json",
            "errors": [
                "Committed residual ledger contains stale entries no longer matching the translations",
                *["STALE: " + compact_entry(sig) for sig in list(stale_or_removed.elements())[:20]],
            ],
        })

    derived_summary = expected_residual_summary(current_entries, deprecated, missing)
    committed_summary = ledger.get("summary", {})
    summary_keys = (
        "files_with_residuals",
        "residual_occurrences",
        "residual_han_characters",
        "classification_counts",
        "deprecated_terminology",
        "missing_outputs",
        "ledger_status",
        "accepted",
    )
    summary_mismatches = [
        key for key in summary_keys if committed_summary.get(key) != derived_summary.get(key)
    ]
    if summary_mismatches:
        failures.append({
            "path": "translation-residual-exceptions.json",
            "errors": [
                "Residual ledger summary does not derive from the current population: " + ", ".join(summary_mismatches)
            ],
        })

    report = {
        "accepted": not failures,
        "targets_expected": EXPECTED_TARGETS,
        "validator": {
            "pass": EXPECTED_TARGETS - len(validator_failures),
            "fail": len(validator_failures),
            "warning_count": validator_warnings,
        },
        "residual_review": derived_summary,
        "ledger_entries": len(committed_entries),
        "current_residual_entries": len(current_entries),
        "ledger_new_or_changed": sum(new_or_changed.values()),
        "ledger_stale_or_removed": sum(stale_or_removed.values()),
        "failures": failures,
    }
    return not failures, report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, default=Path("translation-gate-report.json"))
    args = parser.parse_args()

    accepted, report = check_gate()
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"Translation gate: {'PASS' if accepted else 'FAIL'} | "
        f"validator {report['validator']['pass']}/{EXPECTED_TARGETS} | "
        f"residual accepted={report['residual_review']['accepted']} | "
        f"ledger drift={report['ledger_new_or_changed'] + report['ledger_stale_or_removed']}"
    )
    if report["failures"]:
        print("Failures:")
        for failure in report["failures"][:25]:
            location = failure.get("path", "<unknown>")
            if failure.get("line"):
                location += f":{failure['line']}"
            print(f"- {location}")
            for error in failure.get("errors", [])[:5]:
                print(f"    {error}")
    return 0 if accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
