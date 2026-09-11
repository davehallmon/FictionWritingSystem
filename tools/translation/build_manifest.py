#!/usr/bin/env python3
"""Build a restartable manifest for Chinese-to-English Markdown translation."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ZH_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
LATIN_RE = re.compile(r"[A-Za-z]")
DEFAULT_ROOTS = ("oh-story", "drama")
DESTINATION = "Chinese-to-English"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


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
    """Include .md files and extensionless repository documents."""
    return path.is_file() and (path.suffix.lower() == ".md" or not path.suffix)


def destination_for(repo: Path, source: Path) -> Path:
    relative = source.relative_to(repo)
    project, *remainder = relative.parts
    return repo / project / DESTINATION / Path(*remainder)


def build_manifest(repo: Path, roots: tuple[str, ...]) -> dict:
    records: list[dict] = []
    by_hash: dict[str, list[str]] = defaultdict(list)

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
            chinese = len(ZH_RE.findall(text))
            latin = len(LATIN_RE.findall(text))
            if chinese < 20:
                continue
            source_hash = digest(data)
            destination = destination_for(repo, source)
            output_hash = digest(destination.read_bytes()) if destination.is_file() else None
            status = "translated" if output_hash else "discovered"
            record = {
                "source": source.relative_to(repo).as_posix(),
                "destination": destination.relative_to(repo).as_posix(),
                "category": category(source),
                "source_sha256": source_hash,
                "source_bytes": len(data),
                "chinese_characters": chinese,
                "latin_characters": latin,
                "language_class": "chinese-dominant" if chinese > latin else "mixed",
                "status": status,
                "output_sha256": output_hash,
            }
            records.append(record)
            by_hash[source_hash].append(record["source"])

    duplicate_groups = [paths for paths in by_hash.values() if len(paths) > 1]
    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "roots": list(roots),
        "destination_directory": DESTINATION,
        "summary": {
            "targets": len(records),
            "translated": sum(r["status"] == "translated" for r in records),
            "remaining": sum(r["status"] == "discovered" for r in records),
            "duplicate_groups": len(duplicate_groups),
        },
        "duplicate_groups": duplicate_groups,
        "files": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path("translation-manifest.json"))
    parser.add_argument("--roots", nargs="+", default=list(DEFAULT_ROOTS))
    args = parser.parse_args()
    repo = args.repo.resolve()
    manifest = build_manifest(repo, tuple(args.roots))
    output = args.output if args.output.is_absolute() else repo / args.output
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
