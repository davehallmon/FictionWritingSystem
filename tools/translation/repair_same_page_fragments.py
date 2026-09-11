#!/usr/bin/env python3
"""Repair translated same-page Markdown fragments from source/target heading pairs."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from tools.translation.validate_translation import (
    FENCE_RE,
    broken_same_page_fragments,
    github_slug_base,
    heading_slugs,
)

PROJECTS = ("drama", "oh-story")
DESTINATION = "Chinese-to-English"
LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\((#[^)]+)\)")

# The audit baseline contains exactly one already-broken source TOC link. Its
# English counterpart should point to the translated section that actually
# exists, and the visible TOC label should match that section as well.
KNOWN_TARGET_REPAIRS = {
    "drama/Chinese-to-English/Ref - voice-direction.md": {
        "[Rendering Rules for voice-casting.md](#voice-castingmd-的渲染规则)":
            "[Writing to `视觉设定.md`](#writing-to-视觉设定md)",
    },
}


def outside_fence_segments(text: str) -> list[tuple[bool, str]]:
    """Return (is_fence, text) segments while preserving the original bytes."""
    segments: list[tuple[bool, str]] = []
    cursor = 0
    for match in FENCE_RE.finditer(text):
        if match.start() > cursor:
            segments.append((False, text[cursor : match.start()]))
        segments.append((True, match.group(0)))
        cursor = match.end()
    if cursor < len(text):
        segments.append((False, text[cursor:]))
    return segments


def source_to_target_slug_map(source: str, target: str) -> dict[str, str]:
    source_slugs = heading_slugs(source)
    target_slugs = heading_slugs(target)
    if len(source_slugs) != len(target_slugs):
        raise ValueError(
            f"Heading count differs: source={len(source_slugs)} target={len(target_slugs)}"
        )
    return dict(zip(source_slugs, target_slugs, strict=True))


def repair_text(source: str, target: str) -> tuple[str, int, list[str]]:
    mapping = source_to_target_slug_map(source, target)
    target_slugs = set(heading_slugs(target))
    changes = 0
    unresolved: list[str] = []

    def replace(match: re.Match[str]) -> str:
        nonlocal changes
        label = match.group(1)
        destination = match.group(2)
        fragment = destination[1:]

        # Already-correct localized fragments are authoritative.
        if fragment in target_slugs:
            return match.group(0)

        replacement = mapping.get(fragment)
        if replacement is None:
            # Fallback for a broken source fragment whose translated link label
            # exactly matches a translated heading slug.
            label_slug = github_slug_base(label)
            if label_slug in target_slugs:
                replacement = label_slug

        if replacement is None:
            unresolved.append(destination)
            return match.group(0)

        changes += 1
        return f"[{label}](#{replacement})"

    repaired_parts: list[str] = []
    for is_fence, segment in outside_fence_segments(target):
        repaired_parts.append(segment if is_fence else LINK_RE.sub(replace, segment))
    repaired = "".join(repaired_parts)
    return repaired, changes, unresolved


def iter_pairs(repo: Path):
    for project_name in PROJECTS:
        project = repo / project_name
        destination = project / DESTINATION
        if not destination.is_dir():
            continue
        for target in sorted(destination.rglob("*.md")):
            relative = target.relative_to(destination)
            source = project / relative
            if source.is_file():
                yield source, target


def apply_known_target_repairs(repo: Path, target_path: Path, target: str) -> tuple[str, int]:
    key = target_path.relative_to(repo).as_posix()
    changes = 0
    for before, after in KNOWN_TARGET_REPAIRS.get(key, {}).items():
        if before in target:
            target = target.replace(before, after)
            changes += 1
    return target, changes


def repair_repo(repo: Path, write: bool) -> tuple[int, list[str]]:
    total_changes = 0
    failures: list[str] = []

    for source_path, target_path in iter_pairs(repo):
        source = source_path.read_text(encoding="utf-8")
        original_target = target_path.read_text(encoding="utf-8")
        target, known_changes = apply_known_target_repairs(repo, target_path, original_target)

        # Heading-count differences are legitimate in some translated files.
        # They matter here only when the target actually contains a broken
        # same-page fragment that needs source-to-target mapping.
        if not broken_same_page_fragments(target):
            repaired = target
            changes = known_changes
            unresolved: list[str] = []
        else:
            try:
                repaired, mapped_changes, unresolved = repair_text(source, target)
                changes = known_changes + mapped_changes
            except ValueError as exc:
                failures.append(f"{target_path}: {exc}")
                continue

        if unresolved:
            failures.append(
                f"{target_path}: could not map fragments {', '.join(sorted(set(unresolved)))}"
            )

        broken = broken_same_page_fragments(repaired)
        if broken:
            failures.append(
                f"{target_path}: unresolved after repair {', '.join(sorted(set(broken)))}"
            )

        if write and repaired != original_target:
            target_path.write_text(repaired, encoding="utf-8")
        total_changes += changes

    return total_changes, failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    changes, failures = repair_repo(args.repo.resolve(), args.write)
    mode = "repaired" if args.write else "would repair"
    print(f"{mode} {changes} same-page fragment(s)")
    if failures:
        for failure in failures:
            print(f"ERROR: {failure}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
