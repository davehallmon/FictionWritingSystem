# workflow-daily.md: Daily Continuation Workflow

This file provides the complete guidance for “daily continuation.” After SKILL.md routes here, follow this process.

> **Daily preparation**: The four steps before writing each chapter—state filtering + genre prose-card retrieval + style retrieval + intent confirmation—are embedded in the per-chapter loop in Step 2.
>
> For the prewriting material list, comparable-title path resolution, genre prose cards, custom-style mode, fail-fast behavior for missing style, stopping for missing modules/pacing, authoritative conflict rules, and projects without comparables, always follow “Missing-File Handling” and “Authority Priority for Comparable Analysis” in Phase 4 of `SKILL.md`, plus prewriting preparation (a)–(g) in workflow-chapter.md. This file does not establish a separate system. For reader contracts, protagonist agency, expectation debt, and endgame reserves, see `reader-contract-and-progression.md`.
>
> **Multiple comparable titles**: Read the `主对标书` field from `设定/题材定位.md`; if it points to the current work, treat it as missing (legacy projects may have registered the book itself as the primary comparable). When absent, use the alphabetically first book under `对标/` and tell the user to add the field—first identify the current work using the project directory name, `.active-book`, and the book information in `设定/题材定位.md`, then exclude any same-name `对标/{当前书}/` or comparable whose source points to the current manuscript. If none remain, handle it as no comparable.

---

## Applicability

- The project already contains `正文/` and `追踪/` directories
- The user explicitly says “daily update,” “continue the story,” “continue writing,” or specifies “write Chapters N–M”
- Target: Write 2–3 chapters per session (4,000–9,000 Chinese characters)

> **A bare invocation does not enter daily mode**: If the user only invokes `/story-long-write` / `$story-long-write` without saying “daily update/continue the story/continue writing/write Chapter N/write only one chapter/confirm chapter by chapter,” do not enter this workflow. Return to “Bare Invocation and Parking Point” in `SKILL.md` and show only current progress and available commands, preventing an automatic three-chapter run when a session restarts.

---

## Step 1: Rapid Context Loading

**Optional: Use the story-explorer agent to load context in bulk**. If story-explorer is deployed in the project (check whether `.claude/agents/story-explorer.md` exists), run `Agent(subagent_type: "story-explorer", prompt: "项目目录：{dir}\n查询类型：context_load\n查询参数：准备写第 {N} 章\n追踪状态：last_committed_chapter={上一步 check 的值}，state_revision={上一步 check 的值}")` for a `context_load` query and retrieve the entire writing context at once. After spawn returns, use its results and skip the manual-loading steps below. If the agent is unavailable or its response is incomplete, fall back to manual loading.

Manual loading (default):

| No. | File | Purpose | If Absent |
|------|------|------|-----------|
| 1 | `tracking_commit.py check` | Validate the sole structured state and every derived view, and obtain the last committed chapter and revision; do not put full state into the prompt | If state is absent and a new book has no manuscript, initialize it; if manuscript exists, stop and require `story-import` to reimport it as a standard project |
| 2 | `追踪/上下文.md` | Continuation status card (≤12 KB, fixed seven sections, read in full every chapter) | Do not handwrite it; initialization/chapter transactions generate it |
| 3 | `大纲/细纲_第{N}章.md` | Writing plan for this chapter | **Must be built first**; never skip it |
| 4 | `大纲/卷纲_第X卷.md` | Volume contract, current plot unit, endgame reserves, and future reveal plan | Complete required fields first; never modify a locked volume outline automatically |
| 5 | `设定/角色/{角色名}.md` | Static original characterization for characters involved in this chapter | Build only for central reusable characters under Phase 3 rules |
| 6 | `追踪/角色状态/{角色名}.md` | Derived current snapshot for a long-absent central character; load only characters involved according to the outline | Absence means a damaged derived view: First run `tracking_commit.py check`, then rerun the complete transaction that produces current state; if manuscript exists without state, run `story-import` again |

Do not read all of `追踪/伏笔.md`, `追踪/时间线/`, or `追踪/逐章记录/` by default. Only when the continuation card lacks older information should you query it narrowly through “Old-Information Lookup” below.

**Load on demand**: When constraints for anticipation, payoffs, or information gaps are needed, load `references/plot-emotion-system.md`, `references/plot-core-methods.md`, or the current genre card under `references/genre-prose-cards/`. Do not load all of them by default.

### Continuation Status Card and Tracking Transactions

`追踪/上下文.md` is not a historical archive but the continuation status card in the current semantic checkpoint. It may contain only these seven top-level sections: `当前位置 / 长期约束 / 核心角色状态 / 活跃伏笔 / 近三章速记 / 下一章承诺 / 连贯性风险`. Target 8,192 bytes, hard limit 12,288 bytes. Read style each chapter from `设定/文风.md` / comparable style. Do not place quality counts, ordinary to-dos, file-line indexes, reference-chapter usage records, or AI-like-prose statistics in the continuation card.

See [tracking-transaction.md](tracking-transaction.md) for the common schema, transaction JSON, initialization, and failure recovery for every tracking file. Submit only one structured transaction to the tool per chapter; `scripts/tracking_commit.py` deterministically generates the chapter delta, character snapshots, current foreshadowing view, author/reader timelines, and continuation card. Neither the main session nor subagents may edit these final files separately and directly.

**First initialization**:

1. `_tracking-state.json` absent and the project has no manuscript: Construct an initialization transaction with `last_chapter=0` and run `tracking_commit.py init`.
2. `_tracking-state.json` absent but manuscript exists: Stop daily writing. The directory still uses a legacy tracking structure; use “Legacy Tracking Project Migration” in `/story-import` to rebuild `追踪/`—**do not rerun the entire book deconstruction**. Construct the initialization transaction only from the last complete chapter number and existing tracking files. This workflow neither parses legacy structures nor infers state. `init` moves the complete legacy structure unchanged into `追踪/_旧追踪存档/` before creating the current protocol; old content is neither deleted nor parsed.
3. `tracking_commit.py check` reports that derived views differ from state: Resubmit that chapter's `mode=revision` transaction so the tool rebuilds everything (`expected_state_revision` comes from the `state_revision` field in `追踪/_tracking-state.json`—when `check` fails, it writes only ERROR to stderr and returns no JSON). Never edit Markdown manually or continue to the next chapter. A handwritten chapter record causes same-chapter append to fail permanently with `chapter delta N already exists with different content`; delete the handwritten file and rerun the original transaction.

**Long-term constraint overflow**: The tool accepts at most six items. Before submitting a seventh, merge semantically overlapping items or ask the user to choose. Never delete an old constraint automatically or put to-dos into a derived view.

**Retirement must be declared explicitly**: Submit the full current values of `context.long_term_constraints` and `context.continuity_risks` every chapter. List every prior item no longer submitted in `delta.retired_context_items`; omission is not deletion and the tool rejects it before writing. Likewise, list central characters no longer in use under `delta.retired_characters`. When a character dies/exits in this chapter, still write `character_changes` but do not submit a new snapshot that would be immediately deleted. Both kinds of retirement are allowed only in `mode=append`—a revision transaction belongs to a rewritten old chapter and would falsely identify the retirement chapter, so revisions must resubmit every current context item unchanged. Both retirement categories remain archived in this chapter's record for later lookup.

**Relationship to project rules**: Permanently effective worldbuilding decisions go into transaction `context.long_term_constraints`; short-term hard commitments go into `delta.next_chapter_commitments`; completed or chapter-only process decisions do not enter the continuation card.

> **Determine next chapter N and state revision**: Run `tracking_commit.py check`, take `last_committed_chapter + 1` and `state_revision` from its compact JSON, and cross-check the current position in `上下文.md`. The chapter transaction must write that revision into `expected_state_revision`; if state changes before submission, the tool rejects the stale transaction before any write, so reread current state and reconstruct it. Never load the ever-growing full state into the prompt. If chapter numbers disagree, repair them rather than scanning manuscript files to guess.

After determining the writing range, enter Step 2 directly without asking “continue?” K defaults to 2–3 chapters; follow the user's explicit request for “only one chapter” / “daily three chapters” / “confirm chapter by chapter.” If the user requests N>3, write only the first three this run and state in the Step 4 progress summary that “remaining chapters continue next run.” Pause only for conflicting chapter numbers, missing detailed outlines, a requested range beyond existing outlines, a user change that would alter outline/tracking, or other blocking information that could cause incorrect writing.

---

## Step 2: Serial Batch Writing

Load several chapter outlines at once, but **write chapters serially in the main session**. Never assign several chapters to multiple subagents concurrently. Long-form chapters depend on the preceding chapter and tracking files; concurrency breaks continuity, overwrites tracking, and defeats title deduplication.

**Batch-continuation rule**: After entering this step, “continue” / “continue the story” / “daily update” means continue the current daily batch process only. Never interpret these words as permission to bypass “state filtering” or “comparable module/pacing/genre-card/style retrieval” and write prose directly. Do not ask whether to continue between chapters unless the user explicitly requires chapter-by-chapter confirmation or a blocker appears. Upon reaching K for this run (at most three chapters), enter Steps 3/4, close the batch, and stop; do not continue into another batch merely because later outlines exist.

1. **Read the writing plan**: Determine it in this order: **volume contract → current plot unit → chapter outline**. Written manuscript and `追踪/` remain authoritative for completed material. First read the volume contract, current plot unit (unit ID/position), unit emotional engine, primary thread/results, and endgame-trump-card boundary from `大纲/卷纲_第X卷.md`, then load the 2–3 chapter outlines for this run. If a volume or chapter outline lacks required fields under the current protocol, complete them through the established process, writing `[待补充]` for unknowns. Never alter a locked volume outline automatically. Read stage position, structural formula, prohibited early releases, content summary, plot arrangement, character relationships/order of appearance, semantic obligations/execution boundaries for plot elaboration, and ending hook from each chapter outline; never read or mentally calculate per-beat word budgets. Only outcomes that genuinely affect future continuity enter the chapter transaction.
   - **Batch positioning and stage constraints**: Before writing, extract from `大纲/大纲.md`, the relevant `大纲/卷纲_第X卷.md`, and this batch's outlines: the stage containing the chapter range, the batch progression objective, information permitted for release, information strictly prohibited from early release, and the boundary that chapter-ending hooks cannot cross. Use endgame reserves to confirm this batch's primary thread and results, and do not spend a trump card unavailable at this stage (results may advance several threads). Action cost may be absent; never invent one. Future reveal plans remain in outlines, not timeline facts; only a boundary the next chapter must consume goes into `## 下一章承诺`.
   - **Stage-progress self-check**: After writing the batch or completing its outlines, check for advancement too early, too slowly, or off-stage. Put a corrective action required in the next chapter into transaction `next_chapter_commitments`; put multi-chapter risk into `continuity_risks`. Never force faster pacing by revealing later information early.
2. **Execute chapter by chapter**: For each chapter, complete Steps 1–13 of “Single-Chapter Writing Process” in [workflow-chapter.md](workflow-chapter.md): prewriting, manuscript execution, length validation, hook/payoff review, metadata and prohibited-language scans, and tracking transaction. In batch mode, add these daily-specific actions:
   - **Previous-chapter debt check**: Before writing this chapter, confirm the previous manuscript has no unresolved blocking toxic-pattern debt (the prewrite hook blocks automatically; if unavailable, run `node scripts/check-ai-patterns.js --check --fail-on=blocking` on the prior chapter). Clear debt before writing unless the previous chapter carries `<!-- 去味:跳过 -->` (explicit user exemption)
   - **State-source discipline**: Do not load complete `_tracking-state.json` into the prompt merely to obtain state/chapter number. Query missing material narrowly through “Old-Information Lookup” below; do not substitute unsourced conversational memory or read every chapter record for convenience.
   - **Cross-check returning characters**: If the chapter outline lists a central reusable character absent from `## 核心角色状态`, read the small `追踪/角色状态/{名}.md` file directly. If nonexistent, treat the current checkpoint as damaged, run `tracking_commit.py check`, and repair through a complete transaction rather than temporarily scanning deltas and handwriting a replacement. `设定/角色/{名}.md` contains only static original characterization and cannot replace a dynamic snapshot. When the character becomes active again, put their name in transaction `context.active_character_names`, allowing the tool to update the continuation card.
   - **Branches for story-explorer retrieval gaps** (after a `benchmark_style_load` query_type returns `{style_profile_path, style_profile_summary, selected_emotion_module, rhythm_reference, module_source_path, rhythm_source_path, matched_chapter_K, matched_chapter_techniques, anchor_excerpts, gaps}`, route as follows):
     - If `gaps.no_benchmark: true` → when `custom_style` is true, enter “custom-style mode” (write with `设定/文风.md`; no comparable retrieval exists, so derive emotion/pacing targets from internal materials such as “Target Emotion” in this book's detailed outline, volume outline, and `设定/题材定位.md`; record `selected_emotion_module` / `rhythm_reference` as “none” and never claim comparable retrieval). Otherwise skip style retrieval and mark “no comparable reference” during intent confirmation
     - If `gaps.missing_primary_contract: true` → stop chapter preparation and follow `repair_action`, instructing the user to rerun Stage 3+ of `/story-long-analyze` or rerun `/story-import`. Do not enter narrative-writer (emotion/pacing axes are independent from style; **custom-style mode does not waive this stop**—supply `剧情/情绪模块.md` / `剧情/节奏.md`, not `设定/文风.md`)
     - If `gaps.benchmark_book_missing: true` → stop, compare `expected_path` with the registered name in 题材定位.md byte for byte, and check again; do not switch books
     - If `gaps.conflict` or `gaps.module_rhythm_conflict: true` → intent confirmation must state the conflict and apply the authority of `剧情/情绪模块.md` / `剧情/节奏.md`; `文风.md` must not override emotional/pacing targets
     - If `gaps.profile_missing: true` → when `custom_style` is true, continue in custom-style mode; otherwise stop through the fail-fast process above
     - If `gaps.profile_degenerate: true` (the comparable style is unusable) → when `custom_style` is true, write with `设定/文风.md`; otherwise skip the style and write with default Gates
     - If `gaps.tone_match_failed: true` → use only whole-book style and do not supply matched_chapter
     - Otherwise pass `style_profile_path`, `style_profile_summary`, `selected_emotion_module`, `rhythm_reference`, `module_source_path`, `rhythm_source_path`, `matched_chapter_K`, `matched_chapter_techniques`, `anchor_excerpts`, and `genre_prose_card` unchanged into the narrative-writer spawn prompt at the end of Step 2. `selected_emotion_module` must inform the emotional objective, `rhythm_reference` the pacing/eruption plan, `genre_prose_card` the genre tradeoffs, and `matched_chapter_techniques` the “style-retrieval instructions.” Preserve the original `gaps` values in the preparation record, especially `gaps.module_missing`, `gaps.rhythm_missing`, `gaps.conflict`, and `gaps.matched_deep_dive_missing`. If `matched_deep_dive_missing` is true, explicitly write “the matching chapter's in-depth analysis is missing; fell back to Golden Three Chapters/style techniques” in the style-retrieval instructions and never reverse it to false in a later report
     - **Direct execution without story-explorer**: The main session manually performs prewriting steps (a)–(f) in workflow-chapter.md, retrieving the emotion module, pacing, genre card, style, and matching Chapter K in sequence. When the module or pacing file is absent, set `missing_primary_contract` and stop for repair
   - **Clear post-write findings immediately**: Clear toxic-pattern findings returned by the post-write hook in the same run; do not accumulate them until Step 3.
   - **Submit one tracking transaction immediately after each chapter**:
     1. Extract `result / character_changes / foreshadow_changes / timeline_events / constraints / next_chapter_commitments` from the newly saved manuscript, outline, and prior continuation card. Record only changes that affect future chapters; exclude process logs, quality counts, reference chapters, and AI-like-prose statistics.
     2. For a central character requiring long-term reuse, place the complete dynamic snapshot in `character_snapshots` and the corresponding change in `character_changes`. A one-off background character receives only a change, not a snapshot. When an established dynamic snapshot changes again, submit a new one. Static characterization remains authoritative in `设定/角色/{名}.md`.
     3. Submit the complete current values of `context.long_term_constraints`, current volume/story time/scene, active central-character names, and continuity risks. The tool derives active foreshadowing, three-chapter recap, and next-chapter commitments from the current view/chapter delta; do not fill them manually.
     4. Run `storyctl.py chapter check` and write its `state_revision` into a transaction without `wordcount`. In band + quality pass → `chapter commit`; do not expand `under`; for `over`, perform one net deletion and recheck according to Step 8 of workflow-chapter. If still out of band, follow that step's three actions. Submission rereads, recounts, and reruns quality; delete temporary JSON after success and continue only after tracking commits.
     5. On failure, `_tracking-state.json` has not advanced. Retain temporary JSON, correct the writing environment, and rerun the same `commit`. Never write the next chapter, manually repair a derived view, or ignore the return code.

     The tool generates `追踪/逐章记录/第NNN章.md` across five change categories, with a target ≤1,536 bytes and hard limit 3,072 bytes. It is neither a complete manuscript summary nor a writing-process log. `伏笔.md` contains one current-status row per ID; character state is split into files by central character; objective timeline facts and reader knowledge are maintained within one event record, then rendered into separate author/reader views.

     State updates remain the main session's responsibility. narrative-writer writes only manuscript prose and reports necessary writing results; it never writes directly into `追踪/`. The main session likewise never bypasses the transaction tool to edit final tracking files.
   - **Quality-review prompt** (optional): This chapter is complete. For a consistency review, run `/story-review lean`. Batch mode skips this step and performs one combined review after all chapters are written.
3. **Uninterrupted but not concurrent**: Proceed to the next chapter after tracking commits (unless the user requested confirmation). For `under`, or work still outside the band after one compression, show the evidence/actions and do not advance silently. Before the next chapter, read the previous manuscript and tracking update.

**Research** (as needed): If writing requires verification of external facts (historical period, geography, professional details, etc.), pause and spawn the `story-researcher` agent to search and write into `参考资料/`. Resume only after research completes.

### Old-Information Lookup

When the state summary lacks genuinely necessary old information (foreshadowing planted 20 chapters ago, current state of a long-absent character, a time anchor), search in this order. **Every step has a read limit.** Never degrade into reading complete history files merely because it is convenient.

| Level | Method | Cost |
|------|------|------|
| 1 | Already in continuation status card → use directly | 0 |
| 2 | Foreshadowing ID: `grep -n "F007" 追踪/伏笔.md`; character: `追踪/角色状态/{名}.md`; reader knowledge: `时间线/读者已知.md`; author truth: `时间线/作者真相.md` | One current row or one bounded small file |
| 3 | When the reason/history of a change is needed, call story-explorer's `foreshadow_status / character_status / timeline`; each adapter uses its own agent-call method, or use Grep/Read directly when unavailable | Subagent/main session returns only relevant entries |
| 4 | Explorer unavailable → `grep -R -n --include='第*.md' "F007" 追踪/逐章记录/ 2>/dev/null \| tail -5`, taking only the five latest matching deltas | Read matching lines only |
| 5 | Still insufficient → `Read` the relevant delta or planting chapter's manuscript | One compact delta or one chapter manuscript |
| 6 | Read all chapter deltas/manuscript | **Prohibited in daily mode**. Allowed only during `/story-review` or a comprehensive audit explicitly requested by the user |

**Query limit**: More than three combined executions of Steps 3 and 4 within one chapter indicate that the detailed outline failed to identify which old information the chapter consumes. In that case, have story-explorer query multiple items once and mention verbally at batch end that the outline should identify resolution items more clearly; do not write a separate process log.

Only query results that still affect future chapters after this one enter the tracking transaction: update current foreshadowing through `foreshadow_changes`, central characters through snapshots, and fact/knowledge through `timeline_events`. Never edit one line of the continuation card directly.

---

## Step 3: Quality Review

Each chapter's review occurs during Step 2 through “Quality Review” in [workflow-chapter.md](workflow-chapter.md). At batch end, perform only these **cross-chapter** checks rather than repeating per-chapter items:

1. **Title deduplication**: Compare new chapter titles from this run with existing titles; if identical or clearly repetitive, rename both the corresponding outline and manuscript file consistently
2. **Bidirectional contract/outline check**: First use `reader-contract-and-progression.md` to check the reader contract, causal + resolution ownership, four key-beat questions, expectation ownership, repayment of expectation debt, and endgame reserves (two overdraft questions). Grade chapter progression under the authoritative file's seven states (fast pacing retains a visible-event/payoff floor), relative to this book's genre and comparables; allow a brief low-pressure period and a small visible gain/reward after a climax. New maps/institutions/abilities/enemies/mysteries require a book-switching-debt check. In fulfillment-driven power fantasy, also check whether the protagonist repeatedly causes preventable disasters through incompetence and leaves others to clean them up. Then verify that the manuscript consumed the outline's five-part content summary, multithread plot arrangement, relationship changes/order of appearance, action costs (optional), and ownership of gains. Add three writing-delivery checks (repair on failure): ① Is there an identifiable crisis/anticipation setup passage before the payoff? If none = hollow → return to Step 2 and add a setup beat (reverse-engineering method in plot-emotion-system); ② In a power-display/comeuppance/revelation chapter, are present supporting characters' reactions differentiated (collective shock/individual variation), or is there only protagonist action? If absent → add supporting reactions (plot-core-methods); ③ Does emphasis follow purpose (expand payoff/selling-point beats, summarize transitions, alternate information density), or is everything padded evenly? If even → cut transitions and expand payoff beats.
3. **Foreshadowing inventory (this batch's deltas only)**: Confirm each ID added/advanced/resolved in this batch has exactly one current-status row in `追踪/伏笔.md` and a matching change in the relevant `逐章记录/第NNN章.md`. Never append a second historical row or scan the entire manuscript for a full foreshadowing audit during daily writing

At batch end, rerun the three deterministic closure scripts from “Quality Review” in workflow-chapter.md across every saved manuscript file in the batch (`check-ai-patterns.js` → `normalize-punctuation.js` → `check-degeneration.js`) to confirm no regression after each chapter was cleared.

> If revision in this step changes any fact, character state, foreshadowing, timeline, or next-chapter commitment that affects later material, submit a `mode=revision` transaction for the affected chapter and pass `check` before Step 4. Its `delta` must be recalculated as the complete current record still true after revision rather than only the immediate edit; pure wording changes do not require resubmission.

---

## Step 4: Batch Closure

**Write no tracking content in this step**—each chapter's Step 2 transaction already did so. Perform only two validations:

1. Run `tracking_commit.py check` on the project; validate the state schema, chapter-record continuity/canonical names/size, the continuation card's fixed seven sections and 12,288-byte limit, and consistency between every derived view and state.
2. Confirm every chapter in the batch has a corresponding `追踪/逐章记录/第NNN章.md`, each ≤3,072 bytes. If one is missing or oversized, never repair it by hand; return to that chapter's transaction, correct it, and rerun `commit`.

Then report the batch result verbally to the user (chapter count, word count, drift, next-batch suggestion) without saving another file.

---

> **Drift handling**: aligned = progressing according to plan; adaptive = details adapted without changing the contract; structural drift / structural = manuscript has changed the volume contract, unit promise, progression thread, or ownership of fulfillment and must be repaired or future chapter outlines replanned—never merely note it in a delta. Drift that the next chapter must correct goes into `next_chapter_commitments`; cross-chapter risk goes into `continuity_risks`. Both are constrained by continuation-card limits, while complete meaning remains in compact deltas and outlines.

## Process for Building a Missing Detailed Outline

When a detailed outline is absent, never skip it. Build it as follows:

1. Load `大纲/卷纲_第{N}卷.md` (the event plan corresponding to this chapter) and read the plot-unit card containing the chapter. If the card contains a “comparable plot reference,” additionally read the one plot-unit file it identifies and use the corresponding position in its “structural distribution” as a functional reference. If the whole plot unit lacks chapter outlines beginning here, build the batch according to “Batching Detailed Outlines by Plot” in outline-structure-theory.md rather than completing only one chapter. If the volume outline lacks required fields, complete it first rather than bypassing the current template
2. Load `设定/角色/{角色名}.md` for characters involved in this chapter (character state)
3. Read the latest manuscript chapter (plot continuity)
4. Use the new detailed-outline template in Phase 3 of SKILL.md to build this chapter, supplying stage position, structural formula, prohibited early releases, content summary, plot arrangement, character relationships/order of appearance, plot elaboration, and ending design. Write `[待补充]` for anything not confirmed by the volume outline/manuscript/worldbuilding; never fabricate it
5. After completion, continue to Step 2 writing

---

## Common Problems

| Problem | Handling |
|------|------|
| Detailed outline absent | Follow “Process for Building a Missing Detailed Outline” above |
| Detailed outline lacks current blueprint fields | Complete them from the current template first, writing `[待补充]` for unknowns; do not draft before completion |
| Tracking files are empty | Continue normally and populate them during writing |
| User requests an outline change | Warn that “changing the outline affects later detailed outlines”; modify after confirmation and mark affected outlines |
| Reaching the end of a volume | Ask the user, “The current volume is complete. Open a new volume?” |
| User interrupts batch writing | Save the current chapter and updated tracking files; resume from the cutoff next time |
