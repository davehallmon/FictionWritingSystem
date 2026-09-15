#!/usr/bin/env python3
"""Build the canonical, deterministic Chinese-to-English translation manifest.

Schema v2 separates inventory from quality acceptance. A destination file merely
being present is not sufficient for `translated: true`: the output must be
non-empty, pass the structural translation validator, pass the residual-language
review, and not be detected as stale relative to the previous v2 manifest.

The manifest intentionally omits wall-clock generation timestamps. Provenance is
reproducible from the canonical translation branch, the latest commit that changed
any source document, and content-derived snapshot hashes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

try:  # Package import in tests and tooling.
    from .validate_translation import validate
except ImportError:  # Direct CLI execution from tools/translation/.
    from validate_translation import validate

ZH_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
LATIN_RE = re.compile(r"[A-Za-z]")
DEFAULT_ROOTS = ("drama", "oh-story")
DESTINATION = "Chinese-to-English"
CANONICAL_BRANCH = "translation/chinese-to-english"
SCHEMA_VERSION = 2


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_json(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return digest(payload)


def category(path: Path) -> str:
    name = path.name.lower()
    if name.startswith("skill"):
        return "skill"
    if name.startswith("ref"):
        return "reference"
    if name.startswith("template"):
        return "template"
    if "readme" in name:
        return "readme"
    if name.startswith("evaluation"):
        return "evaluation"
    return "documentation"


def is_markdown_source(path: Path) -> bool:
    return path.is_file() and (path.suffix.lower() == ".md" or not path.suffix)


def destination_for(repo: Path, source: Path) -> Path:
    relative = source.relative_to(repo)
    project, *remainder = relative.parts
    return repo / project / DESTINATION / Path(*remainder)


def discover_sources(repo: Path, roots: tuple[str, ...]) -> list[Path]:
    sources: list[Path] = []
    for root_name in roots:
        root = repo / root_name
        if not root.is_dir():
            continue
        for source in sorted(root.rglob("*")):
            if DESTINATION in source.relative_to(root).parts or not is_markdown_source(source):
                continue
            data = source.read_bytes()
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                continue
            if len(ZH_RE.findall(text)) < 20:
                continue
            sources.append(source)
    return sorted(sources, key=lambda p: p.relative_to(repo).as_posix())


def git_source_commit(repo: Path, sources: list[Path]) -> str:
    """Return the latest commit that changed any current source document."""
    if not sources:
        return "none"
    relpaths = [p.relative_to(repo).as_posix() for p in sources]
    command = ["git", "-C", str(repo), "log", "-1", "--format=%H", "--", *relpaths]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"
    return result.stdout.strip() or "unavailable"


def load_json(path: Path, default: Any) -> Any:
    if not path.is_file():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def previous_entries(previous_manifest: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if not previous_manifest or previous_manifest.get("schema_version") != SCHEMA_VERSION:
        return {}
    return {entry["source"]: entry for entry in previous_manifest.get("files", [])}


def residual_index(ledger: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    by_path: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in ledger.get("entries", []):
        path = entry.get("path")
        if path:
            by_path[path].append(entry)
    return by_path


def residual_state(
    destination: str,
    destination_text: str,
    ledger: dict[str, Any],
    by_path: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    entries = by_path.get(destination, [])
    classifications = Counter(e.get("classification", "unknown") for e in entries)
    approved = sum(e.get("review_status") == "approved" for e in entries)
    rejected = len(entries) - approved
    contains_chinese = bool(ZH_RE.search(destination_text))
    ledger_complete = ledger.get("summary", {}).get("accepted") is True
    # A wholly English output needs no residual-language exception ledger. Any
    # retained Chinese requires the complete approved ledger produced by #5.
    status = "pass" if rejected == 0 and (ledger_complete or not contains_chinese) else "fail"
    return {
        "status": status,
        "approved_exceptions": approved,
        "rejected_exceptions": rejected,
        "contains_chinese": contains_chinese,
        "classifications": dict(sorted(classifications.items())),
    }


def stale_state(
    source_hash: str,
    destination_hash: str | None,
    previous: dict[str, Any] | None,
) -> bool:
    """Detect a source change whose destination content was not updated."""
    if not previous:
        return False
    previous_source = previous.get("integrity", {}).get("source_sha256")
    previous_destination = previous.get("integrity", {}).get("destination_sha256")
    if not previous_source:
        return False
    source_changed = previous_source != source_hash
    destination_unchanged = previous_destination == destination_hash
    return bool(source_changed and destination_unchanged)


def derived_status(
    destination_present: bool,
    translation_complete: bool,
    validator_status: str,
    residual_status: str,
    stale: bool,
) -> str:
    if not destination_present:
        return "missing"
    if not translation_complete:
        return "incomplete"
    if validator_status != "pass":
        return "validation_failed"
    if residual_status != "pass":
        return "residual_review_failed"
    if stale:
        return "stale"
    return "translated"


def derive_summary(records: list[dict[str, Any]], duplicate_groups: list[list[str]]) -> dict[str, int]:
    return {
        "targets": len(records),
        "destination_present": sum(r["state"]["destination_present"] for r in records),
        "translation_complete": sum(r["state"]["translation_complete"] for r in records),
        "translated": sum(r["state"]["translated"] for r in records),
        "remaining": sum(not r["state"]["translated"] for r in records),
        "validation_pass": sum(r["state"]["validator"] == "pass" for r in records),
        "validation_fail": sum(r["state"]["validator"] == "fail" for r in records),
        "residual_review_pass": sum(r["state"]["residual_review"] == "pass" for r in records),
        "residual_review_fail": sum(r["state"]["residual_review"] == "fail" for r in records),
        "stale_translations": sum(r["state"]["stale_source"] for r in records),
        "reviewer_approved": sum(r["state"]["reviewer"] == "approved" for r in records),
        "reviewer_not_recorded": sum(r["state"]["reviewer"] == "not_recorded" for r in records),
        "duplicate_groups": len(duplicate_groups),
    }


def snapshot_hash(records: list[dict[str, Any]], key: str) -> str:
    material = [[record["source"], record["integrity"].get(key)] for record in records]
    return digest_json(material)


def build_manifest(
    repo: Path,
    roots: tuple[str, ...] = DEFAULT_ROOTS,
    *,
    previous_manifest: dict[str, Any] | None = None,
    source_branch: str = CANONICAL_BRANCH,
    source_commit: str | None = None,
    residual_ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    roots = tuple(sorted(roots))
    sources = discover_sources(repo, roots)
    if source_commit is None:
        source_commit = git_source_commit(repo, sources)

    if residual_ledger is None:
        residual_ledger = load_json(repo / "translation-residual-exceptions.json", {"summary": {"accepted": False}, "entries": []})
    residuals = residual_index(residual_ledger)
    old_entries = previous_entries(previous_manifest)

    records: list[dict[str, Any]] = []
    by_hash: dict[str, list[str]] = defaultdict(list)

    for source in sources:
        source_bytes = source.read_bytes()
        source_text = source_bytes.decode("utf-8")
        source_hash = digest(source_bytes)
        destination = destination_for(repo, source)
        destination_present = destination.is_file()
        destination_bytes = destination.read_bytes() if destination_present else b""
        destination_text = destination_bytes.decode("utf-8") if destination_present else ""
        destination_hash = digest(destination_bytes) if destination_present else None
        translation_complete = bool(destination_present and destination_text.strip())

        if destination_present:
            validation = validate(source_text, destination_text)
            validator_status = "pass" if validation.valid else "fail"
            validator_errors = validation.errors
            validator_warnings = validation.warnings
        else:
            validator_status = "fail"
            validator_errors = ["Destination is missing"]
            validator_warnings = []

        source_rel = source.relative_to(repo).as_posix()
        destination_rel = destination.relative_to(repo).as_posix()
        residual = residual_state(destination_rel, destination_text, residual_ledger, residuals)
        stale = stale_state(source_hash, destination_hash, old_entries.get(source_rel))
        status = derived_status(
            destination_present,
            translation_complete,
            validator_status,
            residual["status"],
            stale,
        )
        translated = status == "translated"

        record = {
            "source": source_rel,
            "destination": destination_rel,
            "category": category(source),
            # Compatibility field retained from schema v1, but its meaning is
            # now quality-derived rather than destination-exists.
            "status": status,
            "integrity": {
                "source_sha256": source_hash,
                "destination_sha256": destination_hash,
            },
            "metrics": {
                "source_bytes": len(source_bytes),
                "destination_bytes": len(destination_bytes) if destination_present else 0,
                "source_chinese_characters": len(ZH_RE.findall(source_text)),
                "source_latin_characters": len(LATIN_RE.findall(source_text)),
            },
            "validation": {
                "status": validator_status,
                "errors": validator_errors,
                "warnings": validator_warnings,
            },
            "residual_review": residual,
            "review": {
                "status": "not_recorded",
                "note": "Independent/human PR review is not encoded by the translation-content manifest; issue #7 owns the release review gate.",
            },
            "state": {
                "destination_present": destination_present,
                "translation_complete": translation_complete,
                "validator": validator_status,
                "residual_review": residual["status"],
                "reviewer": "not_recorded",
                "stale_source": stale,
                "translated": translated,
                "status": status,
            },
        }
        records.append(record)
        by_hash[source_hash].append(record["source"])

    duplicate_groups = sorted(
        (sorted(paths) for paths in by_hash.values() if len(paths) > 1),
        key=lambda paths: paths[0],
    )
    summary = derive_summary(records, duplicate_groups)

    return {
        "schema_version": SCHEMA_VERSION,
        "roots": list(roots),
        "destination_directory": DESTINATION,
        "provenance": {
            "source_branch": source_branch,
            "source_commit": source_commit,
            "source_snapshot_sha256": snapshot_hash(records, "source_sha256"),
            "destination_snapshot_sha256": snapshot_hash(records, "destination_sha256"),
        },
        "quality_policy": {
            "translated_requires": [
                "destination_present",
                "translation_complete",
                "validator_pass",
                "residual_review_pass",
                "not_stale",
            ],
            "reviewer_state": "reported separately and does not silently imply human approval",
            "residual_ledger": "translation-residual-exceptions.json",
        },
        "summary": summary,
        "duplicate_groups": duplicate_groups,
        "files": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path("translation-manifest.json"))
    parser.add_argument("--roots", nargs="+", default=list(DEFAULT_ROOTS))
    parser.add_argument("--source-branch", default=CANONICAL_BRANCH)
    parser.add_argument("--source-commit", default=None)
    parser.add_argument(
        "--no-previous-manifest",
        action="store_true",
        help="Ignore the existing v2 manifest when establishing a fresh baseline; normal regeneration should not use this flag.",
    )
    args = parser.parse_args()

    repo = args.repo.resolve()
    output = args.output if args.output.is_absolute() else repo / args.output
    previous = None if args.no_previous_manifest else load_json(output, None)
    manifest = build_manifest(
        repo,
        tuple(args.roots),
        previous_manifest=previous,
        source_branch=args.source_branch,
        source_commit=args.source_commit,
    )
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest["summary"], ensure_ascii=False, indent=2))
    return 0 if manifest["summary"]["remaining"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
