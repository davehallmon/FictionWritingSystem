---
name: story-import
version: 1.0.0
description: "Reverse-import an existing novel. Parse a finished or half-written novel back into a standard project directory structure, compatible with story-long-write / story-short-write subsequent writing flow; internally reuses story-long-analyze / story-short-analyze decomposition pipeline, auto-routes by length. Triggers: /story-import, \"import novel\", \"reverse parse\", \"import\", \"import my book\"."
metadata: {"openclaw":{"source":"https://github.com/zenstory-ai/oh-story-claudecode"}}
---
# story-import: Reverse-Import Existing Novel

You are a novel project reverse-engineer. Import routes by length: long-form goes to Phase 3-L, short-form goes to Phase 3-S.

**The deliverable is a writing engineering project**: rebuild the author's existing book into a **writing engineering project** (project structure + deconstruction library analysis assets). `拆文库/{导入书名}/` is the reconstructed engineering data source — it must not be treated as a disposable intermediate product, nor as the deliverable itself. The deliverable must let the author continue writing directly. Execution treats "build engineering project" as the visible goal — do not treat "deconstruction" as the endpoint or external label.

---

> **Agent compatibility**: Only inspect the current runtime's canonical directory: Claude `.claude/agents/{agent}.md`, OpenCode `.opencode/agents/{agent}.md`, Codex `.codex/agents/{agent}.toml`, Antigravity `.agents/agents/agent-name/agent.md` (where `agent-name` is the target agent name). Must not misjudge based on other-runtime files. Codex uses same-name `agent_type`; Antigravity uses `invoke_subagent` + `TypeName`. When runtime doesn't expose custom-agent registry / `invoke_subagent` or returns unknown agent, must downgrade to solo/direct. When `.zcode/` is detected, also directly solo/direct — ZCode 3.3.4 doesn't execute project custom agents; report `Fallback: project custom agents unavailable -> solo`. Claude/OpenCode compatibility retains `subagent_type`.

> **Spawn version hint (non-blocking to spawn)**: First read `.story-deployed`'s `agents_version` from project root. If it doesn't match this version `agents_version: 29` (missing, field missing/non-integer, less than or greater than 29), **still check file existence and spawn as normal**, while reporting `Notice: agents bundle version mismatch (project {N}, this version 29)` and suggesting to re-run `/story-setup` and open a new session; for > 29, additionally suggest updating oh-story-claudecode first, don't overwrite with local old setup. Only downgrade to solo/direct when agent files are missing or runtime doesn't expose custom agent, report `Fallback: ... -> solo`.

## Core Principles

### Noun & Directory Boundaries (Hard Constraint Throughout)

- `{导入书名}` (imported title): The novel the user has already written halfway or finished, now being rebuilt into an engineering project; its analysis source is fixed at `拆文库/{导入书名}/`.
- `{对标书名}` (benchmark title): An external reference work chosen separately by the user; must be an independent deconstruction product, source fixed at `拆文库/{对标书名}/`, must not point to this import source.
- `story-import` can reuse the deconstruction pipeline to analyze `{导入书名}`, but **must not register `{导入书名}` as main/benchmark target, must not copy `拆文库/{导入书名}/` or project `设定/` into `对标/`**.
- When user has not explicitly chosen an external benchmark, do not create benchmark subdirectory, do not write `主对标书`; subsequent benchmark discovery is handled by story-long-write / story-short-write separately.

### Principle 1: Analyze First, Migrate Second

First fully deconstruct the novel via the decomposition pipeline (output to `拆文库/{导入书名}/`), then migrate the analysis results into project structure. That directory preserves this book's import analysis — keep, don't discard — but it's not part of the external benchmark view.

### Principle 2: Reuse, Don't Repeat

The deep-analysis phase calls the existing deconstruction pipeline — don't re-invent: long-form runs `/story-long-analyze`'s full decomposition pipeline, short-form runs `/story-short-analyze`'s decomposition pipeline. Decomposition methodology and output templates are carried by the corresponding analyze skill; story-import doesn't execute decomposition methodology or maintain these files.

---

## Phase 1: Confirm Import Source

### Step 1: Import Continuation Entry Sequence (Answer User's Flow Question First)

When user asks "should import continuation go through story-setup or story-import", "how to continue an existing novel", "import flow" — give conclusion first, then continue collecting source text:

1. **Recommended order**: First `/story-setup` (deploy hooks/agents/AGENTS), then after new/refreshed session run `/story-import`, finally continue with `/story-long-write 日更/写第N章`.
2. **Can also go directly `/story-import`**: This skill detects `.story-deployed` and professional agents before deep analysis; when not deployed, gives two options: "go to setup first" or "continue import (serial downgrade)".
3. **Already-imported current-protocol project** (has `追踪/_tracking-state.json` in title directory): Don't re-run full import; go directly to the title directory, confirm `.active-book` points to the right book, then use `/story-long-write 日更` or `/story-long-write 写第N章`.
4. **Old-tracking project (v0.7.2 and earlier)** (has `追踪/` and body text, but no `追踪/_tracking-state.json`): Daily continuation will stop and ask to re-import, but **no need to re-run full book deconstruction**. Only rebuild tracking — see "Old Tracking Project Migration" below.

This conclusion must appear before any import-source follow-up questions, to avoid user only wanting to confirm flow but being immediately asked to paste source text.

#### Old Tracking Project Migration

When the title directory has `追踪/` and body text but no `追踪/_tracking-state.json`, the project is on v0.7.2-and-earlier tracking structure. Body text and `设定/`, `大纲/`, `拆文库/` are unaffected — **only `追踪/` needs rebuilding**, don't re-run Phase 2 decomposition, don't touch body text:

1. Count the last complete chapter number `N` (maximum of `正文/第NNN章_*.md`).
2. Rebuild current state from existing old `追踪/` files (character state, foreshadowing, timeline etc., filenames per project actual) and the most recent 3-5 chapters of body text: core character snapshot, unrecovered foreshadowing, revealed timeline events, long-term constraints, next-chapter commitments. The reverse-engineering method for character snapshots is in [references/character-state-reverse.md](references/character-state-reverse.md).
3. Construct JSON per the initialization transaction format in [references/tracking-transaction.md](references/tracking-transaction.md), write `last_chapter` as `N` (chapters 1..N don't get fake per-chapter records), execute `tracking_commit.py init`.
4. `init` moves old tracking structure as-is into `追踪/_旧追踪存档/` before building current protocol — old content isn't deleted, doesn't participate in parsing, left for author reference.
5. Run `tracking_commit.py check` to confirm pass, then back to `/story-long-write 日更` for continuation.

Rebuild results are based on step 2 evidence; leave uncertain fields empty or write into `continuity_risks`, don't fabricate. If user explicitly requests full re-deconstruction, proceed through complete Phase 2.

Ask user: **"Which book do you want to import? Please provide the file path or paste the text directly."**

### Step 2: Confirm Intent (Engineering Project vs Deconstruction Only)

Default goal is **complete engineering project** (continuable). If user intent is unclear — want a continuable engineering project, or just a deconstruction analysis — **ask proactively**, don't default:

> "Do you want to make this book into a continuable writing engineering project (设定/大纲/正文/追踪, can continue writing chapter N+1), or just a deconstruction analysis?"

- Want continuable engineering project → full story-import (Phase 2 deconstruct + Phase 3 migrate).
- Just want analysis / deconstruction → directly use `/story-long-analyze` (short-form `/story-short-analyze`), stop at deconstruction library, don't enter Phase 3 migration.

### Step 3: Input Mode Identification

```
Did user provide a path?
├─ Single file path (.txt/.md)
│   └─ Auto-split by chapter delimiter
├─ Directory path
│   └─ Sort by filename, merge and process
└─ No path → user pasted text directly?
              ├─ Yes → save to temp file then process
              └─ No → prompt user to provide source file
```

### Step 4: Basic Information Confirmation

1. **Auto-detect**: Identify title (if any), total chapters, total characters, chapter format from text
2. **User confirmation**:
   - Import title: {auto-detected or user input}
   - Genre: {user-provided}
   - Target platform: {起点/番茄/晋江/other}
   - Is complete: {Yes / No (half-written to chapter N)}
   - **Length type**: Long / Short — auto-detect per [references/length-routing.md](references/length-routing.md) (user explicit declaration > structural signals > character-count fallback), and recite detection result back to user for confirmation. Determination decides whether Phase 3 goes long-form or short-form path.
   - **Is last chapter complete**: Complete chapter / Draft (written halfway). If draft, prompt user and record "draft to chapter N" in context, let user decide between "continue from draft" or "finish first then import". story-import only records user decision, doesn't choose for them.
3. **External benchmark (optional, separated from import source)**: When user has explicitly specified an external benchmark, record `{对标书名}` and confirm `拆文库/{对标书名}/` is an independent deconstruction product of that reference work; must not treat `{导入书名}` or the just-generated deconstruction directory as candidates. When user hasn't specified, don't add questions, record as "unbound", later handed to writing skill's benchmark discovery flow.
4. **Output confirmation**: Show user the detected chapter range, character count, determined length type, last-chapter status, and "external benchmark: {benchmark title / unbound}", confirm before starting analysis.

### Step 5: Pre-Environment Detection

Before entering Phase 2, detect whether project already has story-setup infrastructure:

- First read `.story-deployed` and execute top-level Spawn version gate; old `chapter-extractor` files even if still on disk are not reusable.
- Only after `agents_version: 28` passes, check Phase 2 `chapter-extractor` in current runtime's canonical directory: Claude/OpenCode/Antigravity are same-name Markdown, Codex is same-name TOML.
- If `.story-deployed`'s `target_cli` includes `zcode`, project agents missing is ZCode 3.3.4's expected state: don't prompt re-deployment, directly enter analysis as serial solo/direct and report fallback.

**When deployment marker is missing, version invalid/expired, or current-end agent is unavailable, and it's not a deployed ZCode project**, prompt user:

> "Detected current project hasn't deployed writing infrastructure. Suggest running `/story-setup` first then come back to import, otherwise deep analysis phase can't use parallel chapter-extractor agent."

Give user two choices:

1. **Go to setup first**: Pause import, run `/story-setup`, deploy, then re-trigger `/story-import`;
2. **Continue import**: Accept Phase 2 downgrade to serial processing (long-form per-chapter summaries not parallel, slower but products complete).

User's choice is recorded in context, Phase 2 decides whether to use parallel mode based on this.

### Step 6: Source Text Backup

Source text backup is handled by the analyze decomposition pipeline called in Phase 2 (the analyze pipeline's pre-step copies/saves source text to `拆文库/{导入书名}/原文/`, corresponding to story-long-analyze and story-short-analyze's "Source Text Backup (Pipeline Pre-step)"). Phase 1 only needs to confirm source is ready (path valid or text obtained), no separate backup here to avoid duplicating analyze pipeline backup logic.

---

## Phase 2: Deep Analysis

Per length type determined in Phase 1, call the corresponding analyze skill's **full decomposition pipeline**; don't do "reuse methodology"-style half-flow — drive the whole pipeline to completion and get the full set of structured products.

| Length | Decomposition Pipeline Called | Product Directory |
|:------|:------------------------------|:------------------|
| Long-form | story-long-analyze full pipeline (Stage 0-6) | `拆文库/{导入书名}/` |
| Short-form | story-short-analyze decomposition pipeline (Stage 2-6) | `拆文库/{导入书名}/` |

### Calling Contract

#### Long-form: Auto-continue past Stage 1 stop point

story-long-analyze **automatically stops** at Stage 0+1 (golden three chapters) and uses AskUserQuestion to ask whether to continue full deconstruction (corresponding to story-long-analyze's "Stage 1 Stop Point"). But import scenario requires Stage 2-6 full products (per-chapter summaries / aggregate analysis / `剧情/节奏.md` / `剧情/情绪模块.md` / character relations / summary report / writing style), none can be missing — otherwise Phase 3 migration gets half-products.

**Current deconstruction contract**: `_progress.md` must be `schema_version: 2`, and `剧情/节奏.md` + `剧情/情绪模块.md` are mandatory authoritative products for import. Any missing must be fixed or re-run corresponding Stage before proceeding — can't piece together seemingly-complete import engineering from summary files.

Therefore when calling story-long-analyze, **must drive "full deconstruction, run once, don't stop to ask" mode from the very beginning**, hitting its "skip asking" path (when user says "full deconstruction / run once / systematic deconstruction / don't ask" at start, don't stop), letting pipeline auto-continue from Stage 2 to Stage 6.

- Example phrasing: When starting deep analysis, declare "Deconstruct this book in 'full deconstruction, run once, don't stop to ask' mode, ensuring Stage 2-6 all produce output".
- **Fallback**: If the runtime actually stops at Stage 1 asking point, story-import automatically chooses "continue full deconstruction", **never push the stop question to user**.
- When Phase 1 environment detection finds chapter-extractor agent not deployed and user chooses "continue import", Stage 2 per-chapter summaries downgrade to serial processing — products still complete, just slower.

#### Short-form: Single Full Pipeline

story-short-analyze's decomposition pipeline (Stage 2-6) itself **has no Stage 1 stop point**, runs once to completion. All 4 Phase 1 steps must run, executed per the following import-scenario handling without skipping entirely:

| Phase 1 Step | Import-Scenario Handling |
|:-------------|:------------------------|
| Step 1: Get source text | Use source file already confirmed in story-import Phase 1, don't re-ask |
| Step 2: Character count check (long/short routing) | Length already determined in story-import Phase 1 and confirmed by user — answer "continue as short-form", don't re-route |
| Step 3: Genre identification | **Run as normal**, genre standard must be loaded; genre type confirmed in story-import Phase 1 Step 4 is substituted directly, no re-asking |
| Step 4: Continue check (when `拆文库/{导入书名}/_meta.json` already exists, 3-way choice) | First see if old output can be reused directly: `stages_completed` contains 6 AND `拆文报告.md` / `情节节点.md` / `写作手法.md` / `原文/` are all non-empty and source matches this import → proceed directly to Phase 3, don't re-run or archive. Otherwise this is first time entering Phase 2 → (a) overwrite: archive old output to `拆文库/{导入书名}/_archive_{timestamp}/` first, then re-run from Stage 2; same round re-import of same book → (b) continue. Don't present 3-way choice to user, don't skip archiving |

`_meta.json`'s `genre_detected` is output from Step 3, is a blocking mandatory field for the deconstruction contract — downstream story-short-write depends on it to select genre standard — **don't skip Step 3 and start from source backup directly**.

- Example phrasing: "《{导入书名}》length confirmed as short-form (genre {genre type}, ~{N} characters total), Step 2 continues as short-form, Step 4 handled by overwrite and archive, genre identification runs as normal, ensuring Stage 2-6 all produce output".
- **Fallback**: If runtime still throws "this text {N} chars is too long, suggest using `/story-long-analyze`" or asks gray-zone question "between short/long, deconstruct as short or long?", always answer character-by-character "continue as short-form" per Phase 1's locked determination, **never push the routing question to user**.

### Output Directory

#### Long-Form Deconstruction Library Structure

Long-form analysis outputs to `拆文库/{导入书名}/`, exactly consistent with story-long-analyze decomposition pipeline:

```
拆文库/{导入书名}/
├── 原文/
│   └── 原文.txt          # Extension follows source file; text pasted directly from conversation saved as 原文.md
├── 概要.md
├── 章节/
│   ├── 第1章_深度拆解.md
│   ├── 第1章_摘要.md
│   └── ...               # Each chapter has both 第N章_深度拆解.md and 第N章_摘要.md
├── 快速预览.md
├── 角色/
│   ├── {角色名}.md
│   └── 角色关系.md
├── 剧情/
│   ├── {剧情标题}.md
│   ├── 故事线.md
│   ├── 节奏.md          # Key info advancement / emotional trigger points / burst rhythm
│   ├── 情绪模块.md      # Reader needs / emotional engine / reproducible modules
│   └── 散落情节.md
├── 设定/
│   ├── 世界观/         # 背景设定.md / 力量体系.md / 地理.md / 金手指.md (subdirectory form)
│   └── 势力/           # {势力名}.md (one file per faction)
├── 拆文报告.md
├── 文风.md          # Stage 6 writing style: writing technique view + source text example anchors
└── _progress.md
```

#### Short-Form Deconstruction Library Structure

Short-form analysis outputs to `拆文库/{导入书名}/`, consistent with story-short-analyze decomposition pipeline:

```
拆文库/{导入书名}/
├── 原文/
│   └── 原文.txt          # Extension follows source file; text pasted directly from conversation saved as 原文.md
├── 拆文报告.md
├── 情节节点.md
├── 写作手法.md
└── _meta.json           # Pipeline metadata + structural count (downstream story-short-write must read)
```

### Long-Form Complete Pipeline (Stage 0-6)

> Pipeline details see story-long-analyze (run `/story-long-analyze`), here only summary.

| Stage | Name | Input | Output | Completion Mark |
|:------|:-----|:------|:-------|:----------------|
| 0 | Summary Extraction | Raw text | 概要.md + chapter index | Chapter structure identified |
| 1 | Golden Three Chapters | First 3 chapters original | 第1章_深度拆解.md / 第2章_深度拆解.md / 第3章_深度拆解.md → **produces quick-preview.md as stop output** (import scenario auto-continues, doesn't stop to ask) | 3 chapters deconstructed |
| 2 | Per-Chapter Summary | Chunked chapter text | Chapter summaries (with plot point + character + **key info and expansion techniques**). 10-40 plot points per chapter (density 150-200 chars/point, dynamically adjusted by character count). Character filtering (extras not extracted, aliases consolidated). **Parallel chapter-extractor agent mode** (not deployed → serial downgrade). **Count verification: summary count == chapter count**. | All chapters processed |
| 3 | Aggregate Analysis | All chapter summaries | `剧情/*.md` + `剧情/README.md` + `剧情/故事线.md` + **`剧情/节奏.md` + `剧情/情绪模块.md`**. **Story framework identification** (pre-step). **Two-step plot aggregation** (first identify plot outline from summaries, then allocate plot points per outline). **Key info advancement index**, **emotional trigger points and burst rhythm**, **reader needs / emotional engine / reproducible modules**. **Character consolidation** (cross-chapter dedupe + alias normalization). **Character grading** (protagonist/antagonist/core supporting/functional). **Scattered plot fallback** (6 steps, including coverage verification). **Quality check** (confidence >=0.85 / coverage 85%-95% / overlap <=35%). | Quality check passes |
| 4 | Setting + Relations | Stage 3 merged character data + plot points | Setting/*.md + Character/*.md. **Two-phase character model**. **Alias resolution** (auto-merge when confidence ≥0.85). | Setting and relation extraction complete |
| 5 | Summary Report | All output | 拆文报告.md (including "Reader Needs / Emotional Engine", "Key Info and Expansion Techniques Overview", "Rhythm and Emotional Trigger Points", "Reproducible Modules", and pointing to `剧情/节奏.md` / `剧情/情绪模块.md`) | Report generated |
| 6 | Writing Style | 拆文报告.md + chapters/第1-3章_深度拆解.md + chapters/*_摘要.md + 原文/原文.txt | 文风.md (this book's historical writing analysis) | Landed at `拆文库/{导入书名}/文风.md`, preserved as import analysis, not copied to book's `对标/` |

### Short-Form Deconstruction Pipeline

> Pipeline details see story-short-analyze (run `/story-short-analyze`), here only summary.

Short-form is a single full pipeline (Stage 2-6 strictly serial), products landed at `拆文库/{导入书名}/`: Stage 2 structure + plot nodes → Stage 3 emotional line + climax → Stage 4 reversal + writing techniques → Stage 5 characters + opening/ending → Stage 6 comprehensive evaluation, finally summarized into `拆文报告.md`, `情节节点.md`, `写作手法.md`, with `_meta.json` recording pipeline metadata and structural count.

Long-form chunking follows story-long-analyze: Stage 2 uses chapter-extractor agent in parallel, other stages follow that skill's "chunking strategy" chapter-count threshold — story-import doesn't define its own.

### Recovery Mechanism

- Progress tracked via progress file when interrupted
- New session reads progress file to locate break point
- Resume from starting chapter of block where break point occurred
- Long-form progress file format follows story-long-analyze decomposition pipeline's progress section convention, including current stage, last processed chapter, completed stage list, update time

### Quality Check

Before stages 3-4 of long-form completes, execute quality check (confidence >= 0.85, coverage 85%-95%, overlap <= 35%) — quality check is handled by story-long-analyze decomposition pipeline itself. Short-form quality check per story-short-analyze's stage completion marks.

---

## Phase 3: Structure Migration

Migrate `拆文库/{导入书名}/` analysis results into project structure consumable by writing skills.

### Routing

Per length type determined in Phase 1, two paths produce completely different engineering structures:

| Length | Migration Path | Mapping Rules | Writing Skill Handoff |
|:------|:-------------|:-------------|:---------------------|
| Long-form | **3-L: Long-form Structure Migration** | [references/structure-mapping-long.md](references/structure-mapping-long.md) | story-long-write daily loop |
| Short-form | **3-S: Short-form Structure Migration** | [references/structure-mapping-short.md](references/structure-mapping-short.md) | story-short-write Phase 3 per-scene writing |

---

## Phase 3-L: Long-Form Structure Migration

Migrate `拆文库/{导入书名}/` analysis results into `{导入书名}/` long-form project structure. Migration rules see [references/structure-mapping-long.md](references/structure-mapping-long.md).

### Migration Steps

#### Step 1: Create Project Skeleton

```
{导入书名}/
├── 设定/
│   ├── 世界观/
│   ├── 角色/
│   └── 势力/
├── 大纲/
├── 正文/
├── 追踪/
│   └── 逐章记录/
├── 对标/                       # Optional; only created when external benchmark explicitly bound
└── 参考资料/
```

#### Step 2: Body Text Standardization

Migrate original text to `正文/`, unify naming format: `第XXX章_章名.md`.

- Identify chapter delimiters (Chapter X, Chapter X, etc.)
- Extract chapter titles
- Zero-pad for alignment (Chapter 1 → Chapter 001)
- Preserve original content unchanged

#### Step 3: Character File Migration

Migrate `拆文库/{导入书名}/角色/{角色名}.md` to `设定/角色/{角色名}.md`.

When migrating, supplement with story-long-write character template fields per [structure-mapping-long.md](references/structure-mapping-long.md)'s "Character File Migration Template".

Character grading (per story-long-analyze standard):

| Level | Standard | Migration Strategy |
|:------|:---------|:-------------------|
| Protagonist | Appears ≥50% of chapters + drives main plot + complete growth arc | Full migration |
| Antagonist | Opposes protagonist + drives core conflict + clear motivation | Full migration |
| Core supporting | Appears ≥20% of chapters or drives important subplot | Full migration |
| Functional | Appears <20% + limited role | Simplified migration |

#### Step 4: Relation File Migration

Convert `拆文库/{导入书名}/角色/角色关系.md` to `设定/关系.md`, output per [structure-mapping-long.md](references/structure-mapping-long.md)'s "Relation File Conversion Rules" target format template.

#### Step 5: Sync Worldview Settings

Current deconstruction contract already outputs theme-based directories — import stage only does pass-through, no longer parses or splits flat `世界观.md`.

| Source Path | Target Path | Current Contract |
|:-----------|:-----------|:----------------|
| `拆文库/{导入书名}/设定/世界观/*.md` | `{项目}/设定/世界观/*.md` | Sync as-is; `背景设定.md` must exist |
| `拆文库/{导入书名}/设定/势力/*.md` | `{项目}/设定/势力/*.md` | Sync independent faction files as-is |

`力量体系.md`, `地理.md` or small faction materials under 200 chars are merged into `背景设定.md` by upstream, so these independent files can be omitted. If `背景设定.md` is missing, or current content points to independent power system but corresponding file wasn't produced, **stop import and prompt to re-run story-long-analyze Stage 4**. Don't split flat files on-site.

#### Step 6: Outline Generation

**大纲.md** (volume-level structure): Reverse-engineered from `剧情/故事线.md`, `剧情/*.md` and `快速预览.md`. **Volume division uses user confirmation system**, rules see [structure-mapping-long.md](references/structure-mapping-long.md) "Outline Reverse-Engineering Rules":

- **Original has explicit volume boundaries** (contains "Volume 1", "卷一" etc.) → divide per original volume boundaries, no need to ask user.
- **Original has no explicit volume boundaries** → **don't mechanically cut "20-40 chapters per volume"**. Detect candidate volume boundaries via storyline/scene switch/large time-jump, show candidate division plan to user, **wait for user confirmation** before writing volume outline; before confirmation `大纲/大纲.md` only records candidate plan.

```markdown
# 全书大纲

## 卷级大纲

### 第一卷：{卷名}（约 {X} 万字，{Y} 章）
- Function: {inferred from plot analysis}
- Core event: {one sentence}
- Starting state → ending state: {inferred from character arc}
```

**Volume outline**: After volume division confirmed, aggregate from plot files to generate `大纲/卷纲_第X卷.md`, per [structure-mapping-long.md](references/structure-mapping-long.md) "Volume Outline Reverse-Engineering" template format.

**Detailed outline**: Reverse-engineer from chapter summaries to generate `大纲/细纲_第XXX章.md`:

Each chapter first runs `wordcount measure` via story-long-write's Wordcount Core, use JSON's `actual` as historical length snapshot for already-written chapters. Here recorded is original's actual length under `visible_chars_v1`, not letting model re-decide creative target. Detect Python 3 in order: `python3` → `python` → `py -3`; when Python 3 or CLI not found, return `TOOL_UNAVAILABLE` and stop import — don't estimate with model or silently skip.

```bash
{PYTHON} {story-long-write skill root}/scripts/storyctl.py wordcount measure \
  --file "{原文章节文件}" \
  --chapter {N}
```

```markdown
## 细纲（第 N 章）

### 第 N 章：{章名}
- Core event: {extracted from summary}
- Character count target: {actual returned by storyctl}
- Character count metric: visible_chars_v1
- Target emotion: {extracted from chapter tone/emotional curve; unknown write [待补充]}
- Chapter opening hook: [待补充]
- Payoff: {inferred from plot points; no clear evidence write [待补充]}

#### Content Summary (Five-Part Structure)
- Cause: {summarized from plot point; unknown write [待补充]}
- Development: {summarized from plot point; unknown write [待补充]}
- Turning point: {summarized from plot point; unknown write [待补充]}
- Climax: {summarized from plot point; unknown write [待补充]}
- Ending: {what the original ends on in action/image/dialogue; unknown write [待补充]}

#### Plot Arrangement (Multi-line)
- Main plot progression: {reverse-engineered from plot unit index/summary}
- Sub-plot progression: {write "none" or [待补充] when no evidence}
- Event line / task line: {external event chain}
- Romance / relationship line: {only write when evidence exists; otherwise "no explicit" or [待补充]}
- Logic line: Cause → Action → Result → Consequence/New Problem

#### Character Relationships & Appearance Order
- Appearance order: {order of characters/forces/key objects appearing in summary}
- Character relationship changes: {before this chapter → after this chapter; unknown write [待补充]}
- POV/information gap: {who knows what; what reader knows; what protagonist misjudges; unknown write [待补充]}

#### Plot Refinement
- Plot point sequence (fill table row by row from summary plot points):

| # | Plot point (who did what) | Function tag | Execution boundary |
|---|---|---|---|
| 1 | {} | {write [待补充] when function unclear} | {confirm from original what's not released here; unknown write [待补充]} |
- Action cost (can be none) / benefit attribution: {only write when evidence exists; action cost can be none, don't fabricate; unknown write [待补充]}

#### Ending Setting and Hook
- Ending setting: {what the original ends on in action or image; unresolved issues; next chapter driving force; unknown write [待补充]}
- Chapter-end hook: [待补充]
```

> For fields like hooks, character relationship changes, sub-plots/romance lines, action cost/benefit attribution that can't be stably judged from original summary, uniformly mark `[待补充]`; story-import only reverse-engineers evidence-backed blueprints, doesn't fabricate relationships or sub-plots to fill fields.

#### Step 7: Tracking File Generation

Import project must generate tracking status through this skill's own `scripts/tracking_commit.py init` in one transaction — model must not write final files separately. Complete fields and commands see [references/tracking-transaction.md](references/tracking-transaction.md). Semantic preparation order:

1. **Import cut-off chapter**: Write last complete chapter N into initialization transaction's `last_chapter`. Tool records `imported_through_chapter=N` in meta; import's old chapters don't get fake per-chapter incremental records, don't generate extra narrative baseline duplicating current state.
2. **Core character current snapshot**: Reverse-engineer from deconstruction products — protagonist, antagonist, core supporting characters' status through chapter N, written into initialization JSON's `character_snapshots` per character. Output generated by tool to `追踪/角色状态/{角色名}.md`; algorithm in [references/character-state-reverse.md](references/character-state-reverse.md).
3. **Current foreshadowing state**: Generate `foreshadow` from foreshadowing/recovery events with original text evidence. Each ID retains only one current-state row; future designs not yet actually planted stay in outline, not written to `伏笔.md`.
4. **Facts & reader cognition**: Generate key events into `timeline_events`. Same event records objective facts, what reader knows through chapter N, and actual reveal status; future planned reveal chapters must not be disguised as already-occurred facts.
5. **Continuation status card input**: Prepare current position, long-term constraints, active core characters, last 3 chapters shorthand, next-chapter commitments and coherence risks. `上下文.md` generated by tool with fixed 7 columns, don't stuff writing style, file index, ordinary to-do or quality-check counts into continuation status card.
6. **Execute initialization**: Detect Python 3 in order (`python3` → `python` → `py -3`), execute:

   > When project's `追踪/` already contains early files not belonging to current protocol, no need to manually clean: `init` moves them as-is to `追踪/_旧追踪存档/` first, then builds current protocol in place. Old content preserved for author reference, doesn't participate in parsing, current state entirely determined by this import's input; `init` that fails validation doesn't move any files.

   ```text
   {PYTHON} {story-import skill root}/scripts/tracking_commit.py init --project {项目根} --input {初始化事务.json}
   {PYTHON} {story-import skill root}/scripts/tracking_commit.py check --project {项目根}
   ```

Using demo《让你管账号，你高燃混剪炸全网》imported through chapter 10 as example: Continuation status card should clearly state that Jiang Chen's phone original 《诸君，且听龙吟》 was professionally remade by team in high definition, but after executives watched the film they judged the new version "lacked soul", ultimately decided to continue using original; Jiang Chen's quick response should reflect his military propaganda creation value being confirmed by Zhou Bosen and Zhang Yaozu; reader timeline only records conclusions readers have already seen from the viewing session, Zhong Jiajia's "only guessed half right" underlying cultivation arrangements if not yet revealed can only appear in author's truth, can't leak into reader view.

After initialization succeeds, should get:

```text
追踪/
├── _tracking-state.json
├── 上下文.md
├── 逐章记录/                 # Import old chapters don't fabricate files, continuation starts from chapter N+1
├── 角色状态/{角色名}.md
├── 伏笔.md
├── 时间线/
│   ├── 作者真相.md
│   └── 读者已知.md
```

When last chapter is a draft, `last_chapter`, character snapshots and other current semantic checkpoints all count through last complete chapter; draft handling strategy written into coherence risks, don't register incomplete actions as established facts.

#### Step 8: Genre Positioning Generation

Extract core findings from deconstruction report, generate `设定/题材定位.md` (per [structure-mapping-long.md](references/structure-mapping-long.md) "Genre Positioning Generation" template format).

`设定/题材定位.md`'s book genre, core hook, emotion and rhythm summary come from `拆文库/{导入书名}/`, but these fields are not benchmark registration. Only when Phase 1 explicitly bound external benchmark, append "Benchmark Book List + Main Benchmark Book" section; main benchmark at most 1 book, secondary/reference benchmarks unlimited. When unbound, omit entire benchmark registration section, don't use `{导入书名}` as fill. That section format see above "Genre Positioning Generation" template's "Benchmark Book List".

For quick overview later, can also write "Benchmark Analysis (Derived Summary)" table; that table is not authoritative registry, can't replace `主对标书` and complete `对标书列表`. All registration items must trace back to corresponding `拆文库/{对标书名}/`, can't reference book's root `设定/`.

#### Step 9: Benchmark Structured Asset Sync

This step only handles externally referenced works explicitly bound in Phase 1. Sync `拆文库/{对标书名}/`'s structured analysis assets to project reference view `{项目}/对标/{对标书名}/`, for story-long-write to read preferentially. No benchmark bound → skip this step, don't create empty directory; **strictly forbidden** to use `拆文库/{导入书名}/` or project `设定/` as copy source. Full sync mapping source→target see [structure-mapping-long.md](references/structure-mapping-long.md) "Benchmark Reference View Sync Rules".

**Missing handling**:

- Bound external benchmark missing `剧情/节奏.md` or `剧情/情绪模块.md` → Don't register, don't generate half benchmark view; report `module_or_rhythm_required_missing` and prompt to re-run `/story-long-analyze` Stage 3+ for `{对标书名}`. This book's core engineering migration doesn't roll back because of it.
- Other structured subdirectories missing → Prompt per existing import missing items, don't block project creation

#### Step 10: Writing Style Sync

When external benchmark passes Step 9 verification, copy `拆文库/{对标书名}/文风.md` to `{项目}/对标/{对标书名}/文风.md`. Pure copy, don't regenerate; when no external benchmark bound, skip.

**Missing handling**:

- Deconstruction library has no style file (analyze didn't run Stage 6) → Import report prompts user to re-run `/story-long-analyze` before sync; style missing will be fail-fast blocked before daily continuation
- Project benchmark has old style file → Overwrite (latest deconstruction product takes priority), inform in import report

---

## Phase 3-S: Short-Form Structure Migration

Migrate `拆文库/{导入书名}/` short-form deconstruction products into `{短篇标题}/` short-form engineering structure, for story-short-write Phase 3 per-scene writing to seamlessly take over. Migration rules see [references/structure-mapping-short.md](references/structure-mapping-short.md).

> **Short-form engineering is completely different from long-form**: Short-form body is single file `正文.md` (no chapter splitting), **doesn't produce** `追踪/`, `大纲/`, `正文/` etc. long-form directories. Must not mistakenly create these long-form-exclusive directories during migration.

### Short-Form Target Engineering Structure

```
{短篇标题}/
├── 设定.md              ← Contains core framework + this book's continuation baseline
├── 小节大纲.md          ← Reverse-engineered by beat-section structure
├── 正文.md              ← Single-file full body text
└── 对标/{对标书名}/     ← Optional: only external benchmark reference view
    ├── 拆文报告.md
    ├── 情节节点.md
    └── 写作手法.md
```

### Migration Steps

#### Step 1: Body Text Migration

Migrate `拆文库/{导入书名}/原文/` full text as single file `{标题}/正文.md`, normalized per [format-and-structure.md](references/format-and-structure.md) (section markers `###1.`, single newline between paragraphs, dialogue quotes unified per project/platform convention). **Original already is finished text — don't rewrite content, only normalize format.**

#### Step 2: Setting Generation

Reverse-engineer from `拆文报告.md` and `写作手法.md` to generate `{标题}/设定.md`, containing two blocks:

- **Core framework**: Align to story-short-write core framework template (basic info, one-sentence hook, core reversal, emotion design, character sketch).
- **This book's continuation baseline**: Organize structure, emotion rhythm, core reversal mechanism, existing writing techniques of already-written content into continuation baseline section; this is internal context for this book, not a benchmark summary.

#### Step 3: Section Outline Generation

Reverse-engineer from `情节节点.md`'s functional segmentation to generate `{标题}/小节大纲.md`, mapping to short-form beat-section structure by 开头段/铺垫段/升级段/反转段/结尾段; short-form only does light blueprint: each section writes `structure beat/five-part function`, main event, one or more real advancements, target emotion, character/relationship changes, cause/logic chain, ending continuation/hook. Plot points can be fulfilled by same action chain or dialogue simultaneously, don't split into multiple sub-events to pad count. Hook or relationship can't be determined → mark `[待补充]`, don't apply long-form complete chapter blueprint.

#### Step 4: External Benchmark Reference View (Optional)

Only when Phase 1 explicitly bound external `{对标书名}`, sync `拆文库/{对标书名}/` to `{标题}/对标/{对标书名}/`; when not bound, skip. Must not copy `拆文库/{导入书名}/` as whole into `对标/`.

---

## Phase 4: Project Activation

### Step 1: Quality Check

Per length type, check against corresponding quality check list:

- **Long-form**: Complete import quality list see [references/structure-mapping-long.md](references/structure-mapping-long.md) end (including body file count comparison, core character independent snapshot, author/reader timeline isolation, `tracking_commit.py check` passing, volume division already user-confirmed etc.)
- **Short-form**: Quality list see [references/structure-mapping-short.md](references/structure-mapping-short.md) end (including `正文.md` single file exists and format compliant, `设定.md` contains core framework + book continuation baseline, no long-form-exclusive directories mistakenly created etc.)

### Step 2: Missing Items Prompt

Output import result summary and pending items, per length branch.

**Long-form import completion report**:

```
=== Import Completion Report (Long-form) ===
Title: {imported title}
Source: {X} chapters, {Y} wan characters
Project directory: {path}

## Generated Files
- Body text: {N} chapters
- Character files: {M}
- Outline: 大纲.md + {V} volume outlines + {N} detailed outlines
- Tracking: Unique structured state + core character independent derived snapshot + foreshadowing current view + dual-perspective timeline + empty per-chapter record directory + fixed 7-column context
- Setting: {worldview file count} files
- External benchmark: {unbound / synced from `拆文库/{对标书名}/` to `对标/{对标书名}/` / bind failed with repair actions}

## Pending Items
- [ ] Chapter-opening/chapter-end hooks in detailed outlines need supplementing
- [ ] Genre positioning's core hook three-part needs confirmation
- [ ] Foreshadowing tracking items confirmed
- [ ] `追踪/时间线/读者已知.md` must not leak `追踪/时间线/作者真相.md` facts not yet revealed
- [ ] Volume division confirmed (when original has no explicit volume boundaries)
- [ ] `拆文库/{导入书名}/` not copied to project `对标/`, book not registered as its own benchmark
- [ ] If external benchmark bound, `设定/题材定位.md`'s `主对标书` and `对标书列表` only contain independent `{对标书名}`, sync source matches directory name

## Next Actions
- Run `/story-review lean` to review import results
- Run `/story-long-write` + "daily" to begin continuation
```

**Short-form import completion report**:

```
=== Import Completion Report (Short-form) ===
Title: {short-form title}
Source: {Y} characters
Project directory: {path}

## Generated Files
- 正文.md (single file, {Y} chars)
- 设定.md (core framework + book continuation baseline)
- 小节大纲.md ({N} sections)
- External benchmark: {unbound / `对标/{对标书名}/` synced / bind failed with repair actions}

## Pending Items
- [ ] All [待补充] marked files reviewed
- [ ] Section outline chapter-opening/chapter-end hooks need supplementing
- [ ] Core reversal's foreshadowing clues confirmed

## Next Actions
- Run `/story-short-write` Phase 3 to begin continuation
```

### Step 3: Project Activation

- Set `.active-book` to point to imported book title/title directory
- Confirm project can be recognized by corresponding writing skill (long-form → story-long-write, short-form → story-short-write)
- Optional verification: If current runtime's canonical directory has story-explorer agent deployed, can spawn to cross-verify migration data integrity; Antigravity checks `.agents/agents/story-explorer/agent.md` and uses `invoke_subagent` + `TypeName: "story-explorer"`. Prompt: `Project directory: {dir}\nQuery type: progress\nQuery parameters: import verification`

> Setup environment detection already completed in Phase 1 "Pre-Environment Detection", won't repeat here.

---

## Large Work Handling (>200 Chapters)

> This section applies only to long-form import. Short-form is single-file full migration, no incremental import needs.

For works over 200 chapters, **deconstruction can be batched but tracking initialization must cover all written chapters at once**:

1. **Deconstruction batched**: First phase only deep-deconstruct first 50 chapters + full-book summary, then add more chapters as needed into `拆文库/`.
2. **Tracking done at once**: Initialization transaction's `last_chapter` writes **last finished chapter number N**, not first phase's 50. `imported_through_chapter` written once by `init`, doesn't advance afterward; per-chapter transactions only accept chapters starting from N+1; chapters 1..N don't get fake per-chapter records, continuation starts from N+1. If `init` mistakenly wrote 50, chapters 51..N can still `append` one per chapter (one transaction per chapter, chapter numbers must be continuous), just need to construct transaction for each already-written old chapter; don't delete `追踪/` and start over — `_旧追踪存档/` is in there too.
3. **Context summary**: Chapters not deep-deconstructed generate simplified summaries (200 chars/chapter) for reverse-engineering current status.

---

## References Index

Load per stage, not all at once.

All this skill's own reference files are in `references/`, loaded by scenario. When methodology/templates from other skills are involved, story-import doesn't load their files directly — runs corresponding `/command` for that skill to load itself.

### Phase 1: Confirm Import Source

| Scenario | Load File |
|:---------|:----------|
| Length routing determination | `references/length-routing.md` |
| Chapter format identification | Handled by story-long-analyze decomposition pipeline (run `/story-long-analyze`) Stage 1 |

### Phase 2: Deep Analysis

| Scenario | Load File / Related Skill |
|:---------|:-------------------------|
| Long-form deep analysis (methodology, quality check, output templates all self-carried) | Run `/story-long-analyze` calling long-form decomposition pipeline |
| Short-form deep analysis (methodology, quality check, output templates all self-carried) | Run `/story-short-analyze` calling short-form decomposition pipeline |

### Phase 3: Structure Migration

| Scenario | Load File |
|:---------|:----------|
| Long-form migration mapping rules | `references/structure-mapping-long.md` |
| Short-form migration mapping rules | `references/structure-mapping-short.md` |
| Character state reverse-engineering rules (long-form) | `references/character-state-reverse.md` |
| Character state rules (dependencies of character-state-reverse.md) | `references/state-tracking.md` |
| Short-form body text format norms | `references/format-and-structure.md` |

> Long-form detailed outline template format see story-long-write (Phase 3 detailed outline section); short-form core framework template see story-short-write (core framework section). These are pure text guides, story-import doesn't load corresponding skill's files.

### Phase 4: Project Activation

| Scenario | Description |
|:---------|:-----------|
| Long-form project structure norms | See story-long-write (Phase 4 project file structure) |
| Short-form project structure norms | See story-short-write (Phase 3 project structure) |
| Environment deployment | Deployment templates provided by `/story-setup`, story-import doesn't handle deployment |

---

## Pipeline Connection

**Pipeline:** Long-form / Short-form
**Position:** Import (before opening book)

| Timing | Jump To | Command |
|:------|:-------|:--------|
| After import want to continue writing (long-form) | story-long-write | `/story-long-write` + "daily" |
| After import want to continue writing (short-form) | story-short-write | `/story-short-write` |
| After import want to review quality | story-review | `/story-review` |
| Want deep analysis of benchmark (long-form) | story-long-analyze | `/story-long-analyze` |
| Want deep analysis of benchmark (short-form) | story-short-analyze | `/story-short-analyze` |
| Open new book from scratch (long-form) | story-long-write | `/story-long-write` + "open book" |
| Open new book from scratch (short-form) | story-short-write | `/story-short-write` |
| Project not deployed | story-setup | `/story-setup` |

---

## Language

- Reply in user's language — whatever language user uses, reply in that language
- Chinese replies follow the "Chinese Copywriting Layout Guide"