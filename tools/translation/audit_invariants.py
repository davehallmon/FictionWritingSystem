#!/usr/bin/env python3
"""Audit Markdown/technical invariants across every translation pair."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from tools.translation.build_manifest import DEFAULT_ROOTS, build_manifest
from tools.translation.validate_translation import (
    HEADING_RE,
    blockquote_signature,
    comparison_text,
    html_comment_framing,
    image_destinations,
    inline_code_preservation,
    list_signature,
    normalized_urls,
    protected_link_destinations,
    protected_token_preservation,
    table_signatures,
    validate,
    without_fences,
)


def pair_details(source: str, output: str) -> dict:
    source_compare, source_guide_errors = comparison_text(source)
    output_compare, output_guide_errors = comparison_text(output)
    source_outside = without_fences(source_compare)
    output_outside = without_fences(output_compare)

    details: dict[str, object] = {}

    inline_ok, inline_additions, inline_reordered = inline_code_preservation(source_compare, output_compare)
    if not inline_ok:
        details["protected_inline_literals"] = {"classification": "mutation"}
    elif inline_additions or inline_reordered:
        details["inline_code_formatting"] = {
            "classification": "formatting-only",
            "added_spans": inline_additions,
            "grammar_reordered": inline_reordered,
        }

    tokens_ok, token_additions, token_reordered = protected_token_preservation(source_compare, output_compare)
    if not tokens_ok:
        details["protected_tokens"] = {"classification": "mutation"}
    elif token_additions or token_reordered:
        details["protected_token_formatting"] = {
            "classification": "formatting-only",
            "repeated_tokens": token_additions,
            "grammar_reordered": token_reordered,
        }

    source_headings = HEADING_RE.findall(source_outside)
    output_headings = HEADING_RE.findall(output_outside)
    if source_headings != output_headings:
        details["heading_levels"] = {"source": source_headings, "output": output_headings}
    if table_signatures(source_compare) != table_signatures(output_compare):
        details["table_structure"] = {
            "source": table_signatures(source_compare),
            "output": table_signatures(output_compare),
        }
    if list_signature(source_compare) != list_signature(output_compare):
        details["list_structure"] = {
            "source": list_signature(source_compare),
            "output": list_signature(output_compare),
        }
    if blockquote_signature(source_compare) != blockquote_signature(output_compare):
        details["blockquote_structure"] = {
            "source": blockquote_signature(source_compare),
            "output": blockquote_signature(output_compare),
        }
    if html_comment_framing(source_compare) != html_comment_framing(output_compare):
        details["html_comment_framing"] = {
            "source": html_comment_framing(source_compare),
            "output": html_comment_framing(output_compare),
        }
    if normalized_urls(source_compare) != normalized_urls(output_compare):
        details["urls"] = {
            "source": normalized_urls(source_compare),
            "output": normalized_urls(output_compare),
        }
    if protected_link_destinations(source_compare) != protected_link_destinations(output_compare):
        details["protected_link_destinations"] = {
            "source": protected_link_destinations(source_compare),
            "output": protected_link_destinations(output_compare),
        }
    if image_destinations(source_compare) != image_destinations(output_compare):
        details["image_targets"] = {
            "source": image_destinations(source_compare),
            "output": image_destinations(output_compare),
        }
    if source_guide_errors or output_guide_errors:
        details["translation_guide_framing"] = {
            "source": source_guide_errors,
            "output": output_guide_errors,
        }
    return details


def audit(repo: Path) -> dict:
    manifest = build_manifest(repo, DEFAULT_ROOTS)
    findings: list[dict] = []
    passing = 0
    error_counts: Counter[str] = Counter()
    classification_counts: Counter[str] = Counter()
    files_by_error: dict[str, list[str]] = defaultdict(list)
    files_by_detail: dict[str, list[str]] = defaultdict(list)

    for record in manifest["files"]:
        source_path = repo / record["source"]
        output_path = repo / record["destination"]
        if not output_path.is_file():
            findings.append({
                "source": record["source"],
                "destination": record["destination"],
                "errors": ["Missing output"],
                "warnings": [],
                "details": {},
            })
            error_counts["Missing output"] += 1
            files_by_error["Missing output"].append(record["destination"])
            continue

        source = source_path.read_text(encoding="utf-8")
        output = output_path.read_text(encoding="utf-8")
        result = validate(source, output)
        details = pair_details(source, output)
        if result.valid:
            passing += 1
        for error in result.errors:
            error_counts[error] += 1
            files_by_error[error].append(record["destination"])
        for key, detail in details.items():
            files_by_detail[key].append(record["destination"])
            if isinstance(detail, dict) and detail.get("classification"):
                classification_counts[str(detail["classification"])] += 1
        if result.errors or result.warnings or details:
            findings.append({
                "source": record["source"],
                "destination": record["destination"],
                "errors": result.errors,
                "warnings": result.warnings,
                "details": details,
            })

    return {
        "schema_version": 2,
        "summary": {
            "pairs": len(manifest["files"]),
            "validator_passing": passing,
            "validator_failing": len(manifest["files"]) - passing,
            "validator_error_counts": dict(sorted(error_counts.items())),
            "detail_classification_counts": dict(sorted(classification_counts.items())),
            "detail_file_counts": {key: len(value) for key, value in sorted(files_by_detail.items())},
        },
        "files_by_error": dict(sorted(files_by_error.items())),
        "files_by_detail": dict(sorted(files_by_detail.items())),
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    parser.add_argument("--fail", action="store_true", help="Exit nonzero when any pair fails")
    args = parser.parse_args()
    repo = args.repo.resolve()
    report = audit(repo)
    serialized = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else repo / args.output
        output.write_text(serialized, encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    if args.fail and report["summary"]["validator_failing"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
