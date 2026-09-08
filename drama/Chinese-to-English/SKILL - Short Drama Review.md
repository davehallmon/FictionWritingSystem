---
name: short-drama-review
description: Review source analyses, stories, scripts, visual definitions, image prompts, storyboards, frozen keyframes, video prompts, and existing media in short-drama projects. Use when the user asks to “review/check a script,” “check assets or continuity,” “check image/video prompts,” “check source analysis,” “review templatedness,” or “calibrate the project from production observations.” Write only review issues, conclusions, and revision requirements; do not replace the owner in modifying source files.
license: MIT
---

# Short Drama Review

Prefer a reviewer who did not participate in creating the current version. If circumstances prevent this, perform a self-review and disclose that fact. Review and revision are separate units of work: this skill identifies issues, impacts, and required revision outcomes; it does not modify the owner's source in the same pass.

## Quick Start

Read the current file explicitly named by the user. When a single-episode review must be saved, write `审查/EP001-审查.md`; for a standalone-file review, use `审查/<主题>-审查.md`. When the user wants only a verbal conclusion, reply directly and do not create a review file for the sake of “completeness.”

Recommended structure for review Markdown:

```markdown
# EP001 审查

- 范围：剧本、分镜、视频提示词
- 结论：REVISE
- 复核方式：独立 reviewer / 自检

## Blocker · REV-001 · 画面文字未被镜头承载
- 位置：剧本.md / EP001-SC002；分镜.md / SHOT-EP001-004
- 证据：……
- 影响：……
- 修订结果：由 short-drama-storyboard 补入准确文字及可读条件。
- 规则：SHT-01 · reviewed_invariant
```

**English guide (non-executable):** EP001 review. Scope: screenplay, storyboard, and video prompts. Verdict: revise. Review method: independent reviewer or self-review. Blocker REV-001 says on-screen text from screenplay scene EP001-SC002 is not represented by storyboard shot SHOT-EP001-004. The storyboard owner must add the exact text and conditions that make it readable under rule SHT-01.

Citations use only filenames, heading IDs, line numbers, or short quotations. Do not create source declarations, hashes, record IDs, or a second state system.

## Select the Review Scope

- `source_analysis`
- `story_script`
- `assets_continuity`
- `image_prompts`
- `storyboard_keyframes`
- `video_prompts`
- `production_outputs`
- `full_episode`
- `delivery_privacy`
- `project_calibration`

Read only the corresponding material; do not preload the entire project:

- Source analysis: [Source Analysis Review Rubric](references/rubric-source-analysis.md)
- Story, scenes, action, and dialogue: [Story and Script Review Rubric](references/rubric-story-script.md)
- Identity, variants, continuity, and image prompts: [Asset and Prompt Review Rubric](references/rubric-assets-prompts.md)
- Source realization, shots, keyframes, and video movement: [Visual and Motion Review Rubric](references/rubric-visual-motion.md)
- Complete review method: [Review Method](references/review-method.md)
- Common production-side defects: [Production Quality Gates](references/production-quality-gates.md)
- In-project calibration from authorized production observations: [Project Calibration](references/project-calibration.md)
- Templatedness, repeated techniques, or AI-like qualities: [Anti-Template Revision](references/anti-template-repair.md)
- Stage boundaries, reference media, and rule table: [Stage Contract](references/stage-contract.md)

## Workflow

### 1. Freeze the Scope

State exactly which files, chapters, shots, or prompts are under review and which constraints the creator has explicitly established. If the target changes during review, reread it before reaching a conclusion.

### 2. Verify Provable Facts First

- Are visible IDs, references, and durations consistent across the five documents?
- Does every line of script dialogue, action, sound, and on-screen text have a visual or audio carrier?
- Are character, location, and prop states and shot starts/ends continuous?
- Does each prompt move from the correct starting point to the correct endpoint?
- Have private inputs, credentials, absolute paths, or internal-process text leaked?

When a required input is missing, suspend only the judgment that depends on it; other issues may still be compiled.

### 3. Review Content with Evidence

Every finding includes: location; a necessary short quotation or conflicting fact; audience/production impact; the required revision outcome; owner; severity; and rule level. Do not merely say “AI-like,” “not cinematic enough,” or assign an unsupported score.

### 4. Synthesize Across Documents

```text
剧本事实 -> 视觉设定 -> 镜头职责与边界 -> 冻结关键帧 -> 视频运动 -> 下一状态
```

**English guide (non-executable):** Screenplay facts → visual specification → shot responsibility and boundaries → frozen keyframe → video motion → next state.

Prioritize preservation of intent, timing of audience knowledge, and continuity. Do not reward ornate prompts that depart from the source.

### 5. Verdict and Assignment

- `APPROVE`: no blocking issues;
- `APPROVE_WITH_NOTES`: only nonblocking improvements;
- `REVISE`: structural, content, or constraint conflicts exist;
- `PROVISIONAL`: key inputs are insufficient, so judgment cannot yet be completed.

Group revision requirements by owner. Return control when this pass is complete; begin modification and re-review only when the user explicitly requests them.

## Severity

- `blocker`: unsafe, undeliverable, or likely to send the workflow down the wrong path;
- `major`: clearly damages story comprehension, continuity, or production results;
- `minor`: has a specific impact but does not block;
- `note`: a creative choice or optional polish.

## Boundaries

- Do not submit image, video, TTS, or music jobs; do not configure an adapter; do not treat a Dashboard action as production authorization.
- When media cannot be read, state the limitation. Do not infer facial consistency, performance, lip sync, mixing, or market performance from text or adapter status.
- A production observation must bind to the exact input, prompt, reference, configuration, and result versions; it cannot be generalized into a universal rule.
- A review file retains only the minimum evidence needed for revision and does not copy complete private inputs.

## Installation and Maintenance

Run `python3 scripts/selftest.py` only during installation, upgrades, or troubleshooting.
