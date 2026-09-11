#!/usr/bin/env python3
"""Audit Markdown/technical invariants across every translation pair."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from tools.translation.build_manifest import DEFAULT_ROOTS, build_manifest
from tools.translation.validate_translation import (
    BLOCKQUOTE_RE,
    HEADING_RE,
    INLINE_CODE_RE,
    blockquote_signature,
    html_comment_framing,
    list_signature,
    normalized_urls,
    protected_tokens,
    table_signatures,
    validate,
    without_fences,
)


def _line_number(text: str, needle: str, start: int = 0) -> tuple[int, int]:
    at = text.find(needle, start)
    if at < 0:
        return 0, start
    return text.count("\n", 0, at) + 1, at + len(needle)


def _occurrences(text: str, values: list[str]) -> list[dict]:
    records: list[dict] = []
    cursor = 0
    for value in values:
        line, cursor = _line_number(text, value, cursor)
        records.append({"value": value, "line": line})
    return records


def pair_details(source: str, output: str) -> dict:
    source_outside = without_fences(source)
    output_outside = without_fences(output)
    source_inline = INLINE_CODE_RE.findall(source_outside)
    output_inline = INLINE_CODE_RE.findall(output_outside)
    source_headings = HEADING_RE.findall(source_outside)
    output_headings = HEADING_RE.findall(output_outside)
    source_tokens = protected_tokens(source)
    output_tokens = protected_tokens(output)

    details: dict[str, object] = {}
    if source_inline != output_inline:
        details["inline_code"] = {
            "source": _occurrences(source_outside, source_inline),
            "output": _occurrences(output_outside, output_inline),
        }
    if source_tokens != output_tokens:
        details["protected_tokens"] = {"source": source_tokens, "output": output_tokens}
    if source_headings != output_headings:
        details["heading_levels"] = {"source": source_headings, "output": output_headings}
    if table_signatures(source) != table_signatures(output):
        details["table_structure"] = {
            "source": table_signatures(source),
            "output": table_signatures(output),
        }
    if list_signature(source) != list_signature(output):
        details["list_structure"] = {
            "source": list_signature(source),
            "output": list_signature(output),
        }
    if blockquote_signature(source) != blockquote_signature(output):
        details["blockquote_structure"] = {
            "source": blockquote_signature(source),
            "output": blockquote_signature(output),
        }
    if html_comment_framing(source) != html_comment_framing(output):
        details["html_comment_framing"] = {
            "source": html_comment_framing(source),
            "output": html_comment_framing(output),
        }
    if normalized_urls(source) != normalized_urls(output):
        details["urls"] = {
            "source": normalized_urls(source),
            "output": normalized_urls(output),
        }
    return details


def audit(repo: Path) -> dict:
    manifest = build_manifest(repo, DEFAULT_ROOTS)
    findings: list[dict] = []
    passing = 0
    expanded_passing = 0
    error_counts: Counter[str] = Counter()
    expanded_counts: Counter[str] = Counter()
    files_by_error: dict[str, list[str]] = defaultdict(list)

    for record in manifest["files"]:
        source_path = repo / record["source"]
        output_path = repo / record["destination"]
        if not output_path.is_file():
            findings.append({
                "source": record["source"],
                "destination": record["destination"],
                "errors": ["Missing output"],
                "expanded": {},
            })
            error_counts["Missing output"] += 1
            files_by_error["Missing output"].append(record["destination"])
            continue

        source = source_path.read_text(encoding="utf-8")
        output = output_path.read_text(encoding="utf-8")
        result = validate(source, output)
        expanded = pair_details(source, output)
        if result.valid:
            passing += 1
        if not expanded:
            expanded_passing += 1
        for error in result.errors:
            error_counts[error] += 1
            files_by_error[error].append(record["destination"])
        for key in expanded:
            expanded_counts[key] += 1
        if result.errors or expanded:
            findings.append({
                "source": record["source"],
                "destination": record["destination"],
                "errors": result.errors,
                "expanded": expanded,
            })

    return {
        "schema_version": 1,
        "summary": {
            "pairs": len(manifest["files"]),
            "validator_passing": passing,
            "validator_failing": len(manifest["files"]) - passing,
            "expanded_passing": expanded_passing,
            "expanded_failing": len(manifest["files"]) - expanded_passing,
            "validator_error_counts": dict(sorted(error_counts.items())),
            "expanded_mismatch_counts": dict(sorted(expanded_counts.items())),
        },
        "files_by_error": dict(sorted(files_by_error.items())),
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
