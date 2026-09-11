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
    protected_inline_literals,
    protected_link_destinations,
    protected_token_preservation,
    protected_tokens,
    table_signatures,
    validate,
    without_fences,
)


def sequence_summary(before: list | tuple, after: list | tuple, radius: int = 3) -> dict:
    """Compact first-difference diagnostic for ordered structural sequences."""
    limit = min(len(before), len(after))
    first = next((index for index in range(limit) if before[index] != after[index]), limit)
    start = max(0, first - radius)
    stop = first + radius + 1
    return {
        "source_count": len(before),
        "output_count": len(after),
        "first_difference_index": first,
        "source_near_difference": list(before[start:stop]),
        "output_near_difference": list(after[start:stop]),
    }


def multiset_summary(before: list[str], after: list[str]) -> dict:
    """Show missing and unexpected literal multiplicities."""
    source_counts = Counter(before)
    output_counts = Counter(after)
    missing = {
        value: count - output_counts[value]
        for value, count in source_counts.items()
        if output_counts[value] < count
    }
    unexpected = {
        value: count - source_counts[value]
        for value, count in output_counts.items()
        if count > source_counts[value]
    }
    return {
        "source_count": len(before),
        "output_count": len(after),
        "missing": missing,
        "unexpected": unexpected,
    }


def pair_details(source: str, output: str) -> dict:
    source_compare, source_guide_errors = comparison_text(source)
    output_compare, output_guide_errors = comparison_text(output)
    source_outside = without_fences(source_compare)
    output_outside = without_fences(output_compare)

    details: dict[str, object] = {}

    inline_ok, inline_additions, inline_reordered = inline_code_preservation(source_compare, output_compare)
    if not inline_ok:
        details["protected_inline_literals"] = {
            "classification": "mutation",
            **multiset_summary(
                protected_inline_literals(source_compare),
                protected_inline_literals(output_compare),
            ),
        }
    elif inline_additions or inline_reordered:
        details["inline_code_formatting"] = {
            "classification": "formatting-only",
            "added_spans": inline_additions,
            "grammar_reordered": inline_reordered,
        }

    tokens_ok, token_additions, token_reordered = protected_token_preservation(source_compare, output_compare)
    if not tokens_ok:
        details["protected_tokens"] = {
            "classification": "mutation",
            **multiset_summary(protected_tokens(source_compare), protected_tokens(output_compare)),
        }
    elif token_additions or token_reordered:
        details["protected_token_formatting"] = {
            "classification": "formatting-only",
            "repeated_tokens": token_additions,
            "grammar_reordered": token_reordered,
        }

    source_headings = HEADING_RE.findall(source_outside)
    output_headings = HEADING_RE.findall(output_outside)
    if source_headings != output_headings:
        details["heading_levels"] = sequence_summary(source_headings, output_headings)

    source_tables = table_signatures(source_compare)
    output_tables = table_signatures(output_compare)
    if source_tables != output_tables:
        details["table_structure"] = sequence_summary(source_tables, output_tables)

    source_lists = list_signature(source_compare)
    output_lists = list_signature(output_compare)
    if source_lists != output_lists:
        details["list_structure"] = sequence_summary(source_lists, output_lists)

    source_quotes = blockquote_signature(source_compare)
    output_quotes = blockquote_signature(output_compare)
    if source_quotes != output_quotes:
        details["blockquote_structure"] = sequence_summary(source_quotes, output_quotes)

    source_comments = html_comment_framing(source_compare)
    output_comments = html_comment_framing(output_compare)
    if source_comments != output_comments:
        details["html_comment_framing"] = sequence_summary(source_comments, output_comments)

    source_urls = normalized_urls(source_compare)
    output_urls = normalized_urls(output_compare)
    if source_urls != output_urls:
        details["urls"] = sequence_summary(source_urls, output_urls)

    source_links = protected_link_destinations(source_compare)
    output_links = protected_link_destinations(output_compare)
    if source_links != output_links:
        details["protected_link_destinations"] = {
            **sequence_summary(source_links, output_links),
            **multiset_summary(source_links, output_links),
        }

    source_images = image_destinations(source_compare)
    output_images = image_destinations(output_compare)
    if source_images != output_images:
        details["image_targets"] = {
            **sequence_summary(source_images, output_images),
            **multiset_summary(source_images, output_images),
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
        "schema_version": 3,
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
