---
name: story-long-analyze
version: 1.0.0
description: "Long-form web novel deconstruction. Deeply deconstructs blockbuster long novels' golden three chapters, character architecture, satisfaction design, and pacing control. Single deep deconstruction pipeline: after running the golden three chapters (Stage 1), produces a quick preview report and asks whether to continue full deconstruction. Upon confirmation, continues from Stage 2 running chapter-by-chapter summaries, aggregated analysis, setting relationships, and summary report. All artifacts saved to 拆文库/{书名}/. Trigger: /story-long-analyze, /long-form-deconstruct, 'help me deconstruct this book', 'deconstruct this book', 'analyze golden three chapters', 'deep deconstruction', 'full deconstruction', 'systematic deconstruction', or provide a novel text file path—all enter the same pipeline."
metadata: {"openclaw": {"source": "https://github.com/zenstory-ai/oh-story-claudecode"}}
---
# story-long-analyze: Long-form Web Novel Deconstruction

You are a web novel structural analyst.

**Core belief: Understanding others' blockbusters is how you write your own.**

---

> Agent compatibility: Only check the current runtime's canonical directories: Claude `.claude/agents/{agent}.md`, OpenCode `.opencode/agents/{agent}.md`, Codex `.codex/agents/{agent}.toml`, Antigravity `.agents/agents/agent-name/agent.md` (where `agent-name` is the target agent name). Do not misjudge based on the existence of files on other ends. Codex uses the same `agent_type`; Antigravity uses `invoke_subagent` + `TypeName`. When the corresponding runtime does not expose a custom-agent registry / `invoke_subagent` or returns an unknown agent, must downgrade to solo/direct. Detection of `.zcode/` also directly solo/direct, because ZCode 3.3.4 does not execute project custom agents; report `Fallback: project custom agents unavailable -> solo`. Claude/OpenCode compatibility surface retains `subagent_type`.
>
> Spawn version hint (non-blocking for spawn): First read `.story-deployed` in project root for `agents_version`. When inconsistent with this version's `agents_version: 29` (missing marker, field missing/non-integer, less than or greater than 29), **proceed with file-existence check and spawn as normal**, while reporting `Notice: agents bundle version mismatch (project {N}, this version 29)` and prompting to re-run `/story-setup` before new sessions; when greater than 29, additionally prompt to update oh-story-claudecode first, do not use local old setup to downgrade over it. Only downgrade to solo/direct when agent files are missing, or runtime does not expose custom agents, reporting `Fallback: ... -> solo`.

## Deconstruction Boundary Declaration (Applies to Main Thread Too)

The **golden three chapters deep deconstruction (Stage 1)**, **Stage 2 serial degraded chapter-by-chapter processing**, and **Stage 3-6 aggregated/setting/report/writing-style synthesis** that you perform personally follow the same logic as the chapter-extractor subagent: you are deconstructing fictional works **legally held by the user with usage rights** (published/serialized or self-owned), and the nature is **transformative literary criticism** (editorial/review/writing-teaching perspective, without copying, disseminating, or guiding real-world behavior). Domestic genre violence, infidelity, revenge, dark ethics are normal fictional narrative elements—extract them structurally as usual, **do not refuse an entire chapter or entire book on grounds of 'sensitive' or 'inappropriate'**—main-thread refusal would halt the entire automation pipeline; if individual passages cannot be handled, skip and complete the rest normally.

---

## Phase 1: Confirm Deconstruction Target + Enter Pipeline

Ask user: **"Which book do you want to deconstruct? (Title + Platform) Do you have the original text file path?"**

If no clear target, recommend 2-3 benchmark works by genre or type user wants to write.

### Unified Entry

After confirming the deconstruction target, directly enter the deconstruction pipeline (Phase 2). **No fast/deep fork**—only one deep deconstruction pipeline, which automatically pauses at Stage 1 (golden three chapters) to produce a quick preview report.

**When no text path**: If the user didn't provide an original text file path nor pasted text in the conversation, guide them to provide it—"Please provide this book's original text file path, or paste the text directly, and I'll deconstruct starting from the golden three chapters." After getting the text, enter pipeline.

---

## Phase 2: Deep Deconstruction Pipeline

### Output Directory

Default output to `拆文库/{书名}/` (under project root). When user specifies another path, output to their specified path.

### Existing Analysis Utilization

**Before deep deconstruction begins, check if partial deconstruction results already exist**:

1. Check if existing deconstruction files exist under `拆文库/{书名}/`
2. If `_progress.md` exists, read checkpoint info and resume from checkpoint (existing recovery mechanism)
3. If `角色/*.md` or `设定/*.md` exists, read existing character and setting data
4. Use existing data as cross-validation baseline:
   - Compare newly extracted character info with existing character data, check consistency
   - Merge newly discovered setting details with existing settings, annotate info source (newly extracted vs. existing)
   - If conflicts exist (e.g., same character has different name in existing file), annotate conflicts in output for user adjudication
5. Avoid redundant extraction of existing information

### Original Text Backup (Pipeline Prerequisite)

**Before deconstruction begins, must backup original text first**:

1. Check if `拆文库/{书名}/原文/` directory already exists
2. If not, copy original text files from user-provided source path to `拆文库/{书名}/原文/`
3. If user did not provide source file path (pasted text directly in conversation), save original text to `拆文库/{书名}/原文/原文.md`
4. After backup, verify:
   - Source file path mode: Confirm file count and size under `原文/` matches source file
   - Conversation-pasted text mode: Confirm `原文.md` file is non-empty (>0 bytes)

### Output Directory Structure

```
拆文库/{书名}/
├── 原文/
│   └── 原文.txt          # Extension follows source file; text pasted in conversation saved as 原文.md
├── 概要.md
├── 章节/
│   ├── 第1章_深度拆解.md
│   ├── 第2章_深度拆解.md
│   ├── 第3章_深度拆解.md
│   ├── 第1章_摘要.md
│   └── ...
├── 快速预览.md
├── 角色/
│   ├── {角色名}.md
│   └── 角色关系.md
├── 剧情/
│   ├── {剧情标题}.md
│   ├── README.md       # Plot catalog index: authoritative scope of rhythm/emotion modules/story lines
│   ├── 故事线.md
│   ├── 节奏.md          # Key info advancement / satisfaction loop / emotion trigger points / burst rhythm
│   ├── 情绪模块.md      # Reader needs / Emotion engine / Replicable module cards
│   └── 散落情节.md
├── 设定/
│   ├── 世界观/
│   │   ├── 背景设定.md   # Core rules + special settings (non-independent content merged)
│   │   ├── 力量体系.md
│   │   ├── 地理.md
│   │   └── 金手指.md
│   └── 势力/
│       └── {势力名}.md   # Content >= 200 words when independent; insufficient merged into 世界观/背景设定.md
├── 拆文报告.md
├── 文风.md          # Stage 6 writing style: sentence length/punctuation/dialogue subtext/emotion alternation + original text anchor sample passages
└── _progress.md
```

> **Authoritative artifacts**: `剧情/README.md` explains the authoritative scope of each file within the plot catalog; `剧情/节奏.md` is the authoritative index for rhythm/key info advancement/emotion trigger points; `剧情/情绪模块.md` is the authoritative index for reader needs, emotion engine, template frameworks, and replicable module cards. `拆文报告.md` and `剧情/故事线.md` only produce summary projections; if summaries conflict with these two files, downstream writing follows `剧情/节奏.md` / `剧情/情绪模块.md`.

### Pipeline Body: Stage 0-6

This is the only execution pipeline for story-long-analyze. After Stages 0-1 complete, **automatically pause** to produce quick preview report (see "Stage 1 Pause Point" below). User confirms, then continues from Stage 2.

**Estimated time hint**: Before starting, give users a rough estimate based on chapter count: <50 chapters usually 30-60 minutes; 50-200 chapters usually 1-3 hours; >200 chapters may require multiple sessions. Stage 2 can be parallel extracted, but Stages 3-6 still depend on prior artifacts and must proceed by phase.

| Phase | Name | Input | Output | Completion Mark |
|-------|------|-------|--------|-----------------|
| 0 | Summary Extraction | Raw text | 概要.md (**first 200-word thin first-pass** + chapter index; full plot-aware 500-1000-word version at Stage 5 to overwrite) + **Stage 0 chapter boundary sub-step writes boundary table to `_progress.md`** (see details below) | Chapter structure identified + chapter boundaries saved |
| 1 | Golden Three Chapters | First 3 chapters original text | 第1章_深度拆解.md / 第2章_深度拆解.md / 第3章_深度拆解.md (one file per chapter). When non-human antagonists (spirit revival/end-of-world/national destiny etc. abstract conflict types) appear in first 3 chapters, also route analyze as abstract conflict type in this phase (core conflict face/urgency source/escalation mechanism/narrative alternative). | 3 chapters deconstructed → **pause to produce 快速预览.md** |
| 2 | Chapter-by-Chapter Summaries | Chunked chapter text | 章节摘要.md (containing plot points + characters + **key info and expansion techniques** + **per-chapter writing formulas**). Per-chapter writing formulas must extract emotion flow, pacing ratio, structural formula, core techniques, chapter-end cliffhangers and foreshadowing. Character filtering (extra characters not extracted, aliases normalized). 10-40 plot points per chapter (density 150-200 words each, dynamically adjusted by word count; formula below 10 still hard-minimum 10 key steps). **Parallel mode: spawn chapter-extractor agent per chapter**. **Count verification: number of summaries == number of chapters, mismatch marks failed chapters**. | All chapters processed |
| 3 | Aggregated Analysis | All chapter summaries | 剧情/*.md + README.md (containing authoritative division table and **plot unit list** index) + 故事线.md + **节奏.md + 情绪模块.md**. **Story framework identification** (prerequisite, determines aggregation strategy). **Two-step plot aggregation** (first identify plot outline from summaries, then allocate plot points by outline). **Key info advancement index** (track how information is expanded by chapter/plot unit). **Emotion trigger points and burst rhythm** (setup→release→aftermath of satisfaction/masochism/anticipation points). **Whole-book emotion rhythm overview** (emotion curve, satisfaction frequency, small/medium/large climax positions, conflict escalation path, cross-chapter foreshadowing map, small/medium/large cycle units). **Reader needs / Emotion engine / Satisfaction formula framework** (precipitated into replicable module cards). **Character merging** (cross-chapter dedup + alias normalization). **Character grading** (protagonist/antagonist/core supporting/functional). **Scattered plot fallback** (6 steps including coverage verification). **Plot label tagging** (each plot module tagged with plot keywords from deconstruction-notes.md, best-effort, leave blank if no match). **Quality check** (thresholds detailed in material-decomposition.md quality threshold system). | Quality check passed |
| 4 | Settings+Relationships (4a/4b/4c) | **4a**: Stage 2 plot points + chapter summaries (not dependent on Stage 3, parallel with 3); **4b/4c**: Stage 3 merged character data + plot points | 设定/*.md + 角色/*.md. **4a Settings** (worldview/golden finger/factions, summarized from Stage 2 mention data). **4b Complete character profiles** (two-phase model: Stage 2 light mention → Stage 4b complete profile; alias resolution confidence ≥0.85 auto-merge). **4c Character relationship extraction** (extracted from plot points, not original text; including evolution tracking + final status merging + implied inference). Non-human antagonists get full abstract conflict analysis in 4a. | 4a/4b/4c all complete |
| 5 | Summary Report | All output | 拆文报告.md (containing 'Reader Needs / Emotion Engine', 'Key Info and Expansion Techniques Overview', 'Whole-book Emotion Rhythm Overview', 'Rhythm and Emotion Trigger Points', 'Cycle Units', 'Cross-chapter Foreshadowing Map', 'Conflict Escalation Path', 'Replicable Modules' summary, pointing to `剧情/节奏.md` / `剧情/情绪模块.md`; containing 'Writing Techniques' list covering multitasking/delayed revelation/perspective deception/comparison anchor/behavior cycle/physical reaction replacing psychological description/**cross-chapter callbacks**—where items/images serve different functions across chapters) + **概要.md full 500-1000-word version** (plot-aware, overwriting Stage 0's 200-word thin first-pass) | Report + whole-book summary generated |
| 6 | Writing Style | 拆文报告.md + 章节/第1-3章_深度拆解.md + 章节/*_摘要.md + 原文/原文.txt | 文风.md (whole-book writing technique view: sentence length/punctuation/dialogue subtext/emotion alternation cycles + 4-6 original text anchor sample passages + tiered imitation suggestions, hard cap ~4000 words. See [style-profile-protocol.md](references/style-profile-protocol.md) + [style-profile-generator.md](references/style-profile-generator.md)) | Writing style saved to `拆文库/{书名}/文风.md` |

### Stage 0 Chapter Boundary Sub-step

After Stage 0 completes summary + chapter index and before entering Stage 1, **must additionally produce** a 'chapter boundary' table written to `_progress.md`. This is the **sole slice source** shared by subsequent Stage 1 (golden three chapters original text slicing) / Stage 2 (each chapter passed to chapter-extractor agent) / Stage 6 (writing style sampling)—avoid each stage running its own regex slicing which could produce inconsistent results.

Operations:
- Use chapter regex from `style-profile-generator.md` Step 4 (including 千/两, covering 1000+ chapters) to grep all chapter line numbers
- **First remove table of contents blocks**: Many original texts start with a TOC where `第N章` also appears at top-level, which would hit the same as official chapter lines. Criterion is line spacing—within TOC blocks hits are only a line or two apart, while official chapters are separated by entire chapter lengths. Calculate line number differences of adjacent hits, discard the entire continuous block at file start where 'line spacing continuously far below overall median'
- **When duplicate chapter numbers remain after removal, do not pick one yourself**: Multi-volume books restarting from 'Chapter 1' per volume is legitimate structure. In this case keep volume number in title column for disambiguation (e.g., `卷二 第一章`), renumber chapter column with continuous series-wide numbering
- Write to `_progress.md` 'Chapter Boundary' section as 4 columns: `| Chapter | Title | Start Line | Word Count |` (see [pipeline-ops.md](references/pipeline-ops.md) template)
- Before finalizing table, verify chapters are continuous, no duplicates, no skips; if not met, stop and report—do not proceed to Stage 1 with an incorrect table, since Stage 1/2/6 all use this table as the sole slice truth source
- `_progress.md` top `schema_version: 2` also saved

**Recovery prerequisite**: Resume only accepts `_progress.md` with `schema_version: 2` containing 'Chapter Boundary' table. If missing or structurally incomplete, stop resumption and prompt to rebuild progress file from Stage 0 chapter boundary sub-step, avoiding different stages using different slice truths.

### Stage 1 Pause Point

After Stages 0+1 complete, the pipeline **automatically pauses**, producing quick preview report and asking user whether to continue full deconstruction:

1. **Generate pause deliverable**: Write `拆文库/{书名}/快速预览.md` (template in [output-templates.md](references/output-templates.md) 'Quick Preview Report'). By now `概要.md`, `章节/第1章_深度拆解.md`, `章节/第2章_深度拆解.md`, `章节/第3章_深度拆解.md`, `原文/` are all saved.
2. **Write pause status**: `_progress.md` 'Final Status' field set to `paused_after_stage1`, 'Checkpoint' section records 'Next operation: Stage 2 chapter-by-chapter summaries'.
3. **Ask user** (use AskUserQuestion style clear binary choice):
   > "Golden three chapters completed, quick preview report at `快速预览.md`. Continue full deconstruction (Stage 2-6: chapter summaries / aggregated analysis (including `剧情/节奏.md`, `剧情/情绪模块.md`) / setting relationships / summary report / writing style)? Estimated time: {rough estimate based on chapter count}."
   - Choose 'Continue full deconstruction' → Read `_progress.md`, resume from **Stage 2**, **do not rerun Stage 0/1**.
   - Choose 'That's enough' → Pipeline ends, `_progress.md` status stays `paused_after_stage1`, tell user 'Can resume anytime with `/story-long-analyze` on same book, will automatically continue from Stage 2'.
4. **Skip asking circumstances**: When user explicitly says at start 'full deconstruction / run all at once / systematic deconstruction / don't ask', still generate `快速预览.md` (preserving early judgment snapshot), but **don't pause to ask**, directly continue from Stage 2 to Stage 6.

### Post-Stage 5: Topic Decision Backfill (Optional)

After `拆文报告.md` is produced (Stage 5 complete)—unrelated to Stage 6, Stage 6 failure doesn't affect this step.

First locate `选题决策.md`: use project root's if it exists. If not at project root → search down from project root and one level up, max 3 layers deep by filename (skip hidden directories), take latest 3 by mtime. Backfill is writing a file; must confirm before writing to files outside project root: found 1 → report path asking 'Backfill this book's deconstruction support into this one?'; found multiple → use AskUserQuestion to list candidates (path + `scan date` + 'none to backfill'). User doesn't choose → record 'not backfilled' and skip, don't modify any files.

**Only when** `选题决策.md` is located (project root one used directly; outside-project one must pass confirmation above): Find the one with **matching genre keywords** among its recommended topics based on this book's genre—
- Exactly one match → Change that topic's 'boom potential' from `pending deconstruction verification` to supported with source: 'This book's deconstruction support: {Reader Needs/Emotion Engine from `拆文报告.md` + Top replicable modules from `剧情/情绪模块.md` + Satisfaction/trigger rhythm summary from `剧情/节奏.md`} (`拆文库/{书名}/拆文报告.md`, `剧情/情绪模块.md`, `剧情/节奏.md`)'. Note still hypothesis (only one book deconstructed, not conclusive).
- Multiple matches / unsure → Ask user 'Which direction in topic decision for 《{书名}》?'
- No match at all → Record 'no matching topic, not backfilled', don't modify file.
- `选题决策.md` missing contract-required 'boom potential' field → report `invalid_topic_decision_contract`, prompt to re-run `story-long-scan` Phase 5 to generate current file; don't guess or silently backfill, main deconstruction flow can still complete.
- Repeated deconstruction doesn't overwrite: only backfill items still marked `pending deconstruction verification`; already-filled ones untouched.

No `选题决策.md` found in workspace → skip directly, doesn't affect deconstruction.

### Stage 6 Writing Style

`文风.md` only handles expression-layer style; emotion/rhythm intent still authoritative in `剧情/情绪模块.md` and `剧情/节奏.md`.
When original text missing or chapter delimiters unrecognizable → write in `文风.md` 'Generation Record' that `文风可用：否：{reason}`. Stage 6 failure doesn't block pipeline.

### Stage 3-4 Parallel Execution

**Parallel execution diagram**:
```
Stage 3 (plot aggregation + character merging) ──┐
                                                 ├── 4a can parallel with 3
Stage 4a (settings: worldview/golden finger/factions) ┘
                 │
                 ▼ (after Stage 3 + 4a both complete)
Stage 4b (complete character profiles) — serial, depends on merged character entities from Stage 3
                 │
                 ▼
Stage 4c (character relationship extraction) — serial, depends on 4b character entities existing
```

4a data source is Stage 2 summaries so can parallel with 3; 4b/4c depend on Stage 3 character merging so serial.

### Partial Failure Tolerance

Single chapter/phase failure doesn't block pipeline. Failure recorded to `_progress.md` 'Failure Record' table (`| Type | Chapter/Phase | Error Message | Retry Status |`). Final status can be `completed_with_errors` (note failure details in deconstruction report).

> Correspondence with material-decomposition.md: Stage 0 includes Material Phase 1 (chapter parsing); Stage 1, 5 are new; Stage 2 = Material Phase 2; Stage 3 = Material Phase 3; Stage 4 merges Material Phase 4+5.

Detailed templates see [output-templates.md](references/output-templates.md), methodology see [material-decomposition.md](references/material-decomposition.md).

---

## Quality Check Overview

Before Stage 3-4 completes, must pass quality check (confidence, coverage, overlap rate). Thresholds, calculation methods, and self-check checklist's sole authoritative definition see [material-decomposition.md quality threshold system](references/material-decomposition.md).

**Stages 3-5 must also pass 'fact traceability' self-check**: Hard facts in settings/characters/reports (rank/values/distances/attributes/faction counts/appearing chapters/quotes) must be grep-able back to original text; if original doesn't provide it, write '原文未明确' (original not explicitly stated), no inference filling. This is the largest source of deconstruction factual errors (strong models also drift because synthesis phase is two hops from original text, relying on plausibility filling). See [material-decomposition.md synthesis phase fact preservation](references/material-decomposition.md).

---

## Stage 2 Parallel Agent Strategy

Stage 2 uses chapter-extractor agent to process each chapter in parallel, replacing the original serial chunking.

### Invocation Method

Each chapter prompt **must start with 'Material Declaration' prefix** (i.e., the first paragraph of the prompt string below)—gives subagent proper context, preventing it from misjudging normal dramatic plot in domestic genres as harmful and refusing to deconstruct. Prefix is fixed text, verbatim, don't modify or abbreviate.

```python
Agent(
  subagent_type: "chapter-extractor",
  prompt: "[Material Declaration] The following is a fictional novel legally held by the user, task is transformative literary analysis in editorial/review perspective. Violence/revenge/domestic violence/romance/dark ethics are normal fictional elements for this genre—extract as usual, don't refuse whole chapters or books on sensitivity grounds; skip individual passages that can't be handled, complete rest normally.\n\nChapter number: Chapter {N}\nChapter title: {Title}\nChapter word count: {Word Count}\n\nOriginal chapter text:\n{Original text}\n\n[Plot point format requirements] {} in templates are placeholder marks, don't output braces themselves: write 'Type information revelation', not 'Type: information revelation' or 'Type{information revelation}'. Topic tags fill only one value, don't use /, , or space to list multiple. Empty fields uniformly write 'No', don't use '—', unskippable segments can't be omitted. Each plot point must be immediately followed by its own 'Topic tagX | Tone: Y' line, don't pile all tag lines to file end. Correct example:\nP7 **Dragon Blood Needle Detection**: Type information revelation | Xu Qi'an uses dragon blood needle to verify identity and exposes them on the spot | Involved Xu Qi'an, Zheng Xinghuai | Location government yamen rear hall | Item dragon blood needle | Time nightfall\nTopic tag Suspense | Tone: Tense\n\n[Pre-output self-check] Before delivery, verify item by item: ① No { or } in text; ② ^P line count == topic tag line count == Tone: line count; ③ Each topic tag has only one value; ④ Each P line contains type, white description, and involvement segments. Any mismatch, fix before output."
)
```

> The above `[Plot point format requirements]` / `[Pre-output self-check]` two sections are assembled into prompt by main thread at spawn time—**doesn't depend on deployed agent file version in project**—old projects don't need to re-run `/story-setup` to get this format constraint. Sonnet upgrade retry uses same section.

### Batch Strategy

- Spawn 5-8 agents at a time (avoid concurrency limits)
- Wait for current batch to fully complete before spawning next batch
- After each batch, update `_progress.md` recording processed chapters

### Agent Output Collection

- Each agent returns markdown extraction results
- Main thread writes agent output to `章节/第{N}章_摘要.md`
- Collect all agents' appearing character tables for Stage 3 merging

### Failure Handling + Quality Upgrade Retry

**Two failure types**:
1. **Execution failure** (agent crash / timeout / empty output) → retry 1x with same model (haiku)
2. **Quality failure** (after saving output, run chapter-extractor.md 'Quality Check' 12-item self-check, any unmet—typical: plot points <10, P lines missing white description, summary written as bullet list or entire paragraph 'because...so...' serial, type/tone/topic tags exceed enumeration, `Tone:` missing full-width colon, character names as nicknames/generic terms) → **upgrade to sonnet retry 1x**

**Mechanically verifiable hard checks** (main thread greps after saving, hit = quality failure, doesn't depend on agent self-report):
- Plot point count `N = grep -cE '^P[0-9]+ '`; `grep -c '基调：'` must == N (less than N = plot point missing `基调：` or missing full-width colon → downstream Stage 6 writing style sampling greps by full-width `基调：` and silently misses chapters)
- White description section has content: `grep -cE '^P[0-9]+ [^|]+\|[^|]*[^|[:space:]][^|]*\|[^|]*涉及'` must == N (`涉及` segment must have two `|` before it, i.e., Type and White Description each occupy a segment, and White Description can't be all whitespace; less than N = plot point missing white description, or wrong field order/separators. White description is primary evidence for plot points, quotes replaced with selections handled by it for fact re-check)
- `grep -hoE '基调：[^ |]+'` deduplicated ⊆ {tense, relaxed, sad, passionate, satisfying, sweet, warm, horror, suppressed, other}
- `grep -hoE '主题标签[：]?[^ |]+'` deduplicated (removing `主题标签`/colon prefix) ⊆ {romance, family, friendship, power, money, growth, revenge, suspense, comedy, passionate, daily, other} (having `主题标签：` with colon, or value being a tone word, counts as failure)

> **Hard checks are the 4 above, nothing more.** Format drift is mainly prevented by spawn prompt and format constraints in agent templates—post-hoc verification is not relied upon. Variants like brace residue, tag line position, empty field placeholders only affect readability; downstream has no consumer (Stage 6 writing style only greps `基调：`), so adding verification for them would only trigger unnecessary reruns for otherwise usable chapters. **Therefore already saved `章节/*_摘要.md` won't become 'unqualified' because of these format notes—no need to regenerate**; older summaries' `类型{action}`, `物品—` etc. writing remain usable, Stage 3-6 reading behavior unchanged.

**Upgrade retry invocation** (executed by main thread after verification failure):

```python
Agent(
  subagent_type: "chapter-extractor",
  model: "sonnet",            # Explicit override of frontmatter's haiku
  prompt: "Chapter number: Chapter {N}\n... (same as first prompt, including opening 'Material Declaration' prefix, can append: 'Previous verification failure reason: {self-check failure items}')"
)
```

**Final saving rules**:
- Haiku passes first time → Write to `章节/第{N}章_摘要.md`, `_progress.md` mark `success`
- Haiku fails + same model retry passes → Same as above, note `retry_same_model`
- Quality failure + sonnet retry passes → Same as above, note `retry_sonnet`
- Sonnet retry still fails → Chapter marked `⚠️ Skipped`, failure reason written to `_progress.md` 'Failure Record' table, noted in deconstruction report
- Single chapter failure doesn't block pipeline; all batches spawned before deciding whether to enter Stage 3

### Agent Unavailable Degradation

When any of the following, Stage 2 automatically reverts to serial mode, processed chapter-by-chapter by main thread (quality unaffected, just slower). **Both paths have same requirements**: when running serial, summary writing, plot point white description, original text citation selection rules and output self-check all follow [output-templates.md](references/output-templates.md) 'Stage 2 Chapter Summary + Plot Points'; the mechanical hard checks above also apply to serial. Serial has no sonnet upgrade retry path—when hard checks hit, main thread rewrites chapter summary once based on failure items, still fails mark `⚠️ Skipped` in `_progress.md` 'Failure Record' table.

- **Agent not deployed**: Current runtime's canonical agent directory doesn't find `chapter-extractor.md` or Codex same-name TOML. Project agents usually not pre-deployed with writing repos; should re-run `/story-setup` to deploy current adapter, don't read template sources across Skills.
- **Environment doesn't support spawn subagent**: This skill is running within a subagent context and can't spawn another layer of agent.

### Stage 2 Wrap-up: Merge Chapter Summaries (_章节摘要汇总.md)

After all Stage 2 `章节/*_摘要.md` are saved, before entering Stage 3, main thread concatenates them in chapter order into `拆文库/{书名}/_章节摘要汇总.md` (concatenate only, no compression, no rewriting):

```bash
ls 章节/*_摘要.md | sed -E 's/.*第([0-9]+)章.*/\1 &/' | sort -n | cut -d' ' -f2- | while read -r f; do cat "$f"; echo; done > _章节摘要汇总.md
```

**Integrity check** (after concatenation, verify, if any fails delete `_章节摘要汇总.md`, revert to per-file scanning, behavior unchanged):
- `grep -cE '^P[0-9]+ ' _章节摘要汇总.md` == sum of `^P` lines across all summaries
- `grep -cE '^\*\*概要\*\*' _章节摘要汇总.md` == number of summary files (`**概要**` one per chapter, both parallel agent and serial summary templates have; don't use `## Chapter N` header—serial template has no chapter header and would misjudge)

Stage 3 / 4a / 4c / scattered plot fallback now **read `_章节摘要汇总.md` once and reuse in context** instead of per-phase `glob 章节/*_摘要.md` re-scanning (4-5 cold reads of same material reduced to 1).

**Only generate summary file when corpus fits in context**: >500 chapters, or merged `_章节摘要汇总.md` too large for context → **skip this step**, use [material-decomposition.md](references/material-decomposition.md) 'Processing batch → A. Subagent parallel mode': spawn subagent per 10-20 chapter batch, subagent reads that batch's summaries in own context, returns only ≤8K tokens of reduced aggregation, main thread only merges aggregation results (if needed, pairwise merge). **Main thread doesn't read original summaries chapter-by-chapter**—skipping summary file doesn't revert to per-file scanning, same issue for large books. `_章节摘要汇总.md` doesn't replace `章节/*_摘要.md`—single-chapter files remain the saving truth source, Stage 6 writing style sampling and manual review still use single-chapter files. Pipeline ends (after Stage 6) → delete `_章节摘要汇总.md`—it's a derived temporary file, not delivered with `拆文库/` (which story-import preserves as writing engineering).

Stage 3-5 chunking see [material-decomposition.md](references/material-decomposition.md) (sole authority).

---

## Recovery Mechanism

Check `_progress.md` on startup; `paused_after_stage1` → continue from Stage 2.
Operations see [pipeline-ops.md](references/pipeline-ops.md).

---

## Pipeline Connection

**Pipeline**: Long-form
**Position**: Deconstruction (step 2 in long-form pipeline, after story-long-scan, before story-long-write)

| When | Jump to | Command |
|---|---|---|
| Ready to write | story-long-write | `/story-long-write` |
| Need market data | story-long-scan | `/story-long-scan` |
| Better as short-form | story-short-scan → story-short-analyze | `/story-short-scan` |

---

## References

| File | When to Load |
|------|-------------|
| [references/output-templates.md](references/output-templates.md) | Throughout pipeline: output templates for each Stage + quick preview report template + `剧情/节奏.md` / `剧情/情绪模块.md` templates + general quick reference |
| [references/material-decomposition.md](references/material-decomposition.md) | Stages 2-5: material decomposition methodology + quality thresholds + batch strategy; also see writing style references for Stage 6 |
| [references/pipeline-ops.md](references/pipeline-ops.md) | Pipeline operations: `_progress.md` template, error handling, recovery steps |
| [references/deconstruction-notes.md](references/deconstruction-notes.md) | Book deconstruction methods + film breakdown + abstract deconstruction + genre practice |
| [references/style-profile-protocol.md](references/style-profile-protocol.md) | Stage 6: Writing style template + credibility/availability notes |
| [references/style-profile-generator.md](references/style-profile-generator.md) | Stage 6: Writing style generation SOP (6 steps, including Chinese-numeral chapter recognition + full-width colon tone grep) |

---

## Language

- Follow user's language to reply; reply in whatever language user uses
- Chinese replies follow 《中文文案排版指北》