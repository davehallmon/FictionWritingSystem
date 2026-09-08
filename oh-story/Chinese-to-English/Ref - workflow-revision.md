# workflow-revision.md: Major-Revision Workflow

This file provides complete instructions for major revision/reworking scenarios. After SKILL.md routes here, follow this process.

---

## Applicable Conditions

- The user says “revise Chapter X,” “rework Chapter X,” or “rewrite Chapter X.”
- Objective: revise the content of an existing chapter.

> The user must specify a chapter number or title. Do not infer automatically which chapter requires revision.

---

## Step 1: Locate the Chapter

1. Find the file from “Chapter X”: `正文/第{X}章_*.md`
2. If the user supplies a chapter title instead of a number, search with `find 正文/ -name "*{关键词}*"`
3. If it cannot be found, ask the user to confirm the exact chapter.
4. If the user specifies a paragraph range (“paragraphs 3–5,” “that fight,” or “the dialogue section”), record it as the local revision target.

---

## Step 2: Load Context

Load more context than for routine writing because revision requires understanding the connections before and after:

| No. | File | Purpose | If absent |
|------|------|------|-----------|
| 1 | `正文/第{X}章_*.md` | Chapter to revise | Must exist |
| 2 | `大纲/细纲_第{X}章.md` | Original writing plan | Skip |
| 3 | `正文/第{X-1}章_*.md` | Previous chapter (continuity) | For Chapter 1, load `设定/世界观/背景设定.md` instead |
| 4 | `正文/第{X+1}章_*.md` | Next chapter (continuity) | For the final chapter, check `大纲/细纲_第{X+1}章.md` if present to ensure continuity |
| 5 | `tracking_commit.py check` + `追踪/上下文.md` | Use the tool to confirm that the sole state agrees with its derived views; the continuation-state card supplies current continuity without adding complete state to the prompt | Stop if state is absent; an existing-manuscript project must use `story-import` to generate standard tracking state |
| 6 | `设定/角色/{相关角色}.md` + `追踪/角色状态/{相关角色}.md` | Static character definition + dynamic current snapshot | Recompute from relevant deltas if the dynamic snapshot is absent |

**Determining relevant characters**: Extract character names from `大纲/细纲_第{X}章.md`. If the detailed outline does not exist, search the chapter being revised for character-name keywords found under `设定/角色/`. Map each character name to the filename `设定/角色/{角色名}.md`.

---

## Step 3: Revise

1. **Read the original**: Read the complete chapter, run `{PYTHON} {story-long-write skill 根}/scripts/storyctl.py wordcount check`, and record the original `visible_chars_v1` result.
2. **Back up the original**: Copy it to `正文/第{X}章_章名_原稿_{YYYYMMDD}.md` to ensure rollback is possible.
3. **Confirm revision scope**: Ask whether the user wants a “complete rewrite” or “specific-paragraph revision.”
   - Complete rewrite: rewrite from the detailed outline and preserve the backup.
   - Local revision: change only the specified paragraphs (located by scene number or keyword) and leave all other content unchanged.
4. **Execute the revision**: Rewrite the file.
5. **Compare word counts**: Rerun the same counter after revision. If the difference from the original is >30% or >800 characters, whichever threshold is larger, alert the user and report `internal_pass / borderline / under / over / invalid`. Measurement status does not trigger silent overwrite or a second manuscript rewrite.

**Research as needed**: If a revision involves external facts requiring verification, such as historical era, geographic orientation, or occupational detail, spawn the `story-researcher` agent to search and verify them.

---

## Step 4: Cascade Checks

After revision, use one `mode=revision` tracking transaction to complete cascading updates. See [tracking-transaction.md](tracking-transaction.md) for the protocol:

1. **Recompute the revised-chapter delta**: Compare old manuscript/old delta with the new manuscript. Retain only the new version's `result / 角色变化 / 伏笔变化 / 时间与揭示 / 约束 / 下一章承诺` that remain valid for the future. The transaction tool rewrites all of `追踪/逐章记录/第{X}章.md`; it does not retain conclusions overturned by the new manuscript.
2. **Current foreshadowing values**: For every affected ID, inspect Chapters X through the last written chapter M and submit the revised **current state through Chapter M**. If the revision removes a setup but later text still references that ID, list it first as a manuscript conflict; do not simply delete it. Use `action=delete` only after establishing that the entire line no longer exists. `伏笔.md` always has one row per ID and does not append revision history.
3. **Time and reader knowledge**: For every affected event, submit the objective fact, the reader's current knowledge through Chapter M, and the actual reveal status/chapter. Use `action=delete` for a removed event. Future reveal plans remain in the outline. The tool merges events into `_tracking-state.json` and rebuilds author/reader views; editing them separately is prohibited.
4. **Current character snapshot**: For every affected core character, inspect X through M. Recompute identity, location, goal, capability/resources, relationship targets, known information, and unresolved matters separately, then submit one complete snapshot through M. Never let the latest one-dimensional change overwrite other dimensions.
5. **Imported-through scope**: If X ≤ `_tracking-state.json.imported_through_chapter`, the transaction adds an override record for Chapter X. The imported-through chapter remains unchanged; current structured state updates to the revision result.
6. **Commit and retry**: At revision start, run `tracking_commit.py check`; put its returned `state_revision` into `expected_state_revision`, then run `tracking_commit.py commit`. If state changes in the meantime, reread current state and reconstruct the transaction. On failure, preserve the original transaction JSON, correct the write environment, and rerun the same `commit`. Do not revise another chapter or write a new one until it succeeds and passes `check`.
7. **Downstream impact**: If the revision changes character state/relationships or worldbuilding, scan later chapter manuscripts and mark affected items:

```
⚠️ 修改第{X}章后，以下章节可能需要同步调整：
- 第{X+1}章：{原因}（建议检查）
- 第{X+3}章：{原因}（建议检查）
```

**English guide (non-executable):**

> After revising Chapter {X}, the following chapters may require synchronized changes:  
> Chapter {X+1}: {reason} (review recommended)  
> Chapter {X+3}: {reason} (review recommended)

8. **Manuscript metadata scan**: Outside the title line, check for writing-engineering terms such as `第[一二三四五六七八九十百千万两0-9]+章|上一章|上章|前一章|本章|这一章|前文|后文|伏笔|细纲|读者`. Replace a match with an event anchor or relative time perceptible to the character at that moment. Exempt genuine in-story reading/discussion of “Chapter X” or a genuine reader-identity context.
9. **Banned-word scan**: Check the revised content against `references/banned-words.md`, then run `tracking_commit.py check` to verify agreement between state and all derived views.

---

## Step 5: Quality Checks

Run Phase 5 quality checks on the revised chapter, including at least:

1. **Banned-word scan**: If Step 4 did not cover the entire chapter, scan it again.
2. **Manuscript metadata scan**: As described under “Manuscript metadata scan” in “Cascade Checks,” confirm that the full chapter is covered.
3. **Character consistency**: Does revised character behavior agree with the character definitions?
4. **Pacing check**: Has the revision damaged the chapter's pacing?

> See the [“Quality Checks” section of workflow-chapter.md](workflow-chapter.md) for the complete checklist.

---

## Common Problems

| Problem | Handling |
|------|------|
| The user does not say what to revise | Ask, “Which chapter do you want to revise, and in what respect—plot, pacing, dialogue, or description?” |
| Word count rises or falls sharply after revision | Alert the user and let the user decide whether to adjust it |
| Revising several chapters consecutively | Revise one chapter at a time, independently running Steps 2–5 for each |
| Later inconsistencies are discovered after revision | List affected chapters and let the user decide whether to revise them now |
