#!/usr/bin/env python3
"""One-time repair for issue #3 fenced-content policy migration."""

from __future__ import annotations

from pathlib import Path

from tools.translation.validate_translation import (
    TRANSLATION_COMPANION_MARKER,
    authoritative_fenced_blocks,
    fence_records,
    fenced_blocks,
)

NATURAL_LANGUAGE_FILES = (
    "Ref - analysis-writing-techniques.md",
    "Ref - anti-ai-writing.md",
    "Ref - long-emotional-methods.md",
)
ARTIFACT_TEMPLATE_FILE = "Ref - artifact-protocols.md"
CHARACTER_STATE_FILE = "Ref - character-state-reverse.md"


def fence_body(raw: str) -> str:
    first_break = raw.find("\n")
    last_break = raw.rfind("\n")
    if first_break < 0 or last_break <= first_break:
        return ""
    return raw[first_break + 1 : last_break]


def text_companion(raw: str) -> str:
    body = fence_body(raw)
    return f"{TRANSLATION_COMPANION_MARKER}\n```text\n{body}\n```"


def replace_fences(target: str, replacements: list[str]) -> str:
    records = fence_records(target)
    if len(records) != len(replacements):
        raise ValueError(f"target has {len(records)} fences; expected {len(replacements)}")
    for record, replacement in reversed(list(zip(records, replacements, strict=True))):
        target = target[: record.start] + replacement + target[record.end :]
    return target


def repair_natural_language(source: str, target: str) -> str:
    source_records = fence_records(source)
    target_records = fence_records(target)
    if len(source_records) != len(target_records):
        raise ValueError(
            f"natural-language fence count differs: source={len(source_records)} target={len(target_records)}"
        )
    replacements = []
    for source_record, target_record in zip(source_records, target_records, strict=True):
        if source_record.raw == target_record.raw:
            replacements.append(source_record.raw)
        else:
            replacements.append(
                source_record.raw + "\n\n" + text_companion(target_record.raw)
            )
    return replace_fences(target, replacements)


def repair_artifact_templates(source: str, target: str) -> str:
    source_records = fence_records(source)
    target_records = fence_records(target)
    if len(source_records) != len(target_records):
        raise ValueError(
            f"artifact-template fence count differs: source={len(source_records)} target={len(target_records)}"
        )
    return replace_fences(target, [record.raw for record in source_records])


def repair_character_state(source: str, target: str) -> str:
    source_records = fence_records(source)
    target_records = fence_records(target)
    if len(source_records) != 1 or len(target_records) < 1:
        raise ValueError(
            f"unexpected character-state fence counts: source={len(source_records)} target={len(target_records)}"
        )
    first = target_records[0]
    if first.raw != source_records[0].raw:
        raise ValueError("character-state authoritative JSON is not byte-identical")
    anchor = "\n\nThe generated file always contains:"
    anchor_at = target.find(anchor, first.end)
    if anchor_at < 0:
        raise ValueError("character-state post-example anchor not found")
    return target[: first.end] + target[anchor_at:]


def assert_fence_policy(name: str, source: str, output: str) -> None:
    authoritative, errors = authoritative_fenced_blocks(output)
    if errors:
        raise SystemExit(f"{name} companion-policy errors: {errors}")
    if fenced_blocks(source) != authoritative:
        raise SystemExit(f"{name} authoritative fenced blocks differ from source")


def main() -> int:
    repo = Path(".").resolve()
    project = repo / "oh-story"
    translated = project / "Chinese-to-English"
    repaired = 0

    for name in NATURAL_LANGUAGE_FILES:
        source_path = project / name
        target_path = translated / name
        source = source_path.read_text(encoding="utf-8")
        target = target_path.read_text(encoding="utf-8")
        output = repair_natural_language(source, target)
        assert_fence_policy(name, source, output)
        target_path.write_text(output, encoding="utf-8")
        repaired += 1

    source_path = project / ARTIFACT_TEMPLATE_FILE
    target_path = translated / ARTIFACT_TEMPLATE_FILE
    source = source_path.read_text(encoding="utf-8")
    target = target_path.read_text(encoding="utf-8")
    output = repair_artifact_templates(source, target)
    assert_fence_policy(ARTIFACT_TEMPLATE_FILE, source, output)
    target_path.write_text(output, encoding="utf-8")
    repaired += 1

    source_path = project / CHARACTER_STATE_FILE
    target_path = translated / CHARACTER_STATE_FILE
    source = source_path.read_text(encoding="utf-8")
    target = target_path.read_text(encoding="utf-8")
    output = repair_character_state(source, target)
    assert_fence_policy(CHARACTER_STATE_FILE, source, output)
    target_path.write_text(output, encoding="utf-8")
    repaired += 1

    print(f"Repaired and fence-validated {repaired} issue #3 file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
