# Contracts and Ownership

## The Workflow Is Not a Waterfall

```text
开发? -> 剧本 -> 视觉设定 -> 图片提示词
                    \-> 分镜 -> 视频提示词
                    \-> 明确确认后的媒体生产
```

**English guide (non-executable):** Optional development → screenplay → visual specification → image prompts; then branch to storyboard → video prompts, or to media production only after explicit confirmation.

Work may begin from any existing material. Look Development and review occur when needed. Each owner modifies only its own Markdown, may reference visible upstream facts, and must not silently rewrite them.

## Output Language

| Content | With project configuration | Standalone-task default |
|---|---|---|
| Creator-facing explanations and reviews | `short-drama.json#/language` | User's current language |
| Copyable image and keyframe prompt text | `short-drama.json#/format/prompt_language` | `en` |
| Copyable video prompt text | Target video-model profile's `production_profile.choices.video_prompt_language`; fall back to `format.prompt_language` when unspecified | Confirm based on the target video model; use the user's current language when unspecified |

The language of creator-facing explanations, general prompts, and video-model prompts are independent. Dialogue and readable on-screen text come from script and visual facts; do not infer them from the descriptive language.

## Stable Identity and References

Entries in creative documents use creator-visible stable IDs: `EP001-SC001`, `IMG-...`, `SHOT-...`, and `MOTION-...`. An `IMG-...` ID belongs exclusively to a prompt heading in 图片提示词.md and does not indicate that an image already exists. Display names may change without changing identity. Cross-document entries reference these IDs directly; do not write hashes, internal paths, hidden state, or a second record ID.

Actual input reference images are not image-prompt entries, so give each image a separate stable `REF-...` slot. Within the slot, record explicit order, a visible project-relative path, a Chinese name, purpose, and scope of control. Do not use `IMG-...`; use only `/` path separators, and never write absolute paths, Windows drive or network paths, or paths outside the project.

When a creator prepares an image outside the project and attaches it only during generation, there is no in-project path to record. Use a `PLAN-...` slot instead. Its other fields match `REF-...`, while its locator names the corresponding `IMG-...` board or `SHOT-...` frozen keyframe. Here, `IMG-...` does not treat a prompt entry as an image; it answers “which decided fact does this image depict?” A `PLAN-...` slot does not claim that a file exists in the project and therefore cannot serve as production input.

## Rule Levels

- `structural_invariant`: A reference, ID, arithmetic condition, or explicit contradiction that can be proved locally.
- `reviewed_invariant`: An obligation requiring judgment from semantic evidence.
- `craft_default`: Usually effective, but a creator may override it with a stated reason.
- `taste_option`: An expressive choice that cannot block work on its own.

Character count, shot count, emotional curves, and formulas from individual cases are not universal structural thresholds.

## Trust and File Safety

Ordinary creative work does not access the network. Actual media production permits only an external adapter to read environment credentials and always follows `preview -> explicit confirm -> run`. Do not place private inputs, credentials, absolute paths, or nonpublic observations in deliverable documents.
