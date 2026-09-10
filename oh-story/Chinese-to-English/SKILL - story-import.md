---
name: story-import
version: 1.0.0
description: "Reverse-import an existing novel. Parses a partially written or completed novel back into the standard project directory structure, compatible with subsequent story-long-write / story-short-write workflows. Internally reuses the story-long-analyze / story-short-analyze decomposition pipelines and routes automatically by length. Triggers: /story-import, “import a novel,” “reverse parse,” “import,” or “bring my book into the project.”"
metadata: {"openclaw":{"source":"https://github.com/zenstory-ai/oh-story-claudecode"}}
---
# story-import: Reverse-Import an Existing Novel

You are a reverse engineer for novel projects. Route imports by length: long-form fiction uses Phase 3-L; short-form fiction uses Phase 3-S.

**The deliverable is a writing project**: Rebuild the author’s existing book as a **writing project** (project structure + analytical assets in the decomposition library) that can be continued. `拆文库/{导入书名}/` is the rebuilt project’s data source. It is not disposable intermediate output and cannot replace the deliverable itself—the author must be able to continue writing directly from the delivered project. Treat “build the project” as the visible goal; do not present “text decomposition” as the endpoint or external label.

---

> Agent compatibility: Check only the canonical directory for the current runtime: Claude `.claude/agents/{agent}.md`, OpenCode `.opencode/agents/{agent}.md`, Codex `.codex/agents/{agent}.toml`, or Antigravity `.agents/agents/agent-name/agent.md` (`agent-name` is the target agent name). Never infer availability from another runtime’s files. Codex uses the matching `agent_type`; Antigravity uses `invoke_subagent` + `TypeName`. If the active runtime exposes no custom-agent registry / `invoke_subagent`, or returns an unknown agent, fall back to solo/direct execution. When `.zcode/` is detected, likewise use solo/direct execution because ZCode 3.3.4 does not run project custom agents; report `Fallback: project custom agents unavailable -> solo`. Retain `subagent_type` compatibility for Claude/OpenCode.
>
> Spawn version notice (does not block spawning): First read `agents_version` from `.story-deployed` in the project root. If it does not match this release’s `agents_version: 29`—including a missing marker, missing/non-integer field, or a value below or above 29—**continue checking file presence and spawning as usual**, but also report `Notice: agents bundle 版本不匹配（项目 {N}，本版 29）` and advise rerunning `/story-setup` and starting a new session. If the value is above 29, additionally advise updating oh-story-claudecode first instead of using the older local setup to overwrite it with a downgrade. Fall back to solo/direct execution only when the agent file is missing or the runtime does not expose custom agents; report `Fallback: ... -> solo`.

## Core Principles

### Terminology and Directory Boundaries (Hard Constraints Throughout)

- `{导入书名}`: The user’s own partially written or completed novel, now being rebuilt as a project. Its analysis source is always `拆文库/{导入书名}/`.
- `{对标书名}`: A separate external reference work selected by the user. It must be an independently decomposed artifact sourced from `拆文库/{对标书名}/`, and must not point to the current import source.
- `story-import` may reuse the decomposition pipeline to analyze `{导入书名}`, but **must not register `{导入书名}` as a primary or secondary comp title, or copy `拆文库/{导入书名}/` or the project’s `设定/` into `对标/`**.
- If the user has not explicitly selected an external comp title, do not create comp subdirectories or write `主对标书`. Let the later comp-discovery workflow in story-long-write / story-short-write handle it separately.

### Principle 1: Analyze Before Migrating

First run the full decomposition pipeline on the novel (output to `拆文库/{导入书名}/`), then migrate the results into the project structure. Preserve this directory as the imported book’s analysis; do not discard it. It is not part of the external-comp view.

### Principle 2: Reuse, Don’t Reimplement

During deep analysis, invoke an existing pipeline rather than inventing a new one: long-form fiction runs the complete `/story-long-analyze` pipeline; short-form fiction runs `/story-short-analyze`. Each analyze skill owns its methodology and output templates. story-import neither performs that methodology nor maintains those files.

---

## Phase 1: Confirm the Import Source

### Step 1: Explain the Import-to-Continuation Order First (When the User Asks About Process)

When a user asks whether to run story-setup or story-import first, how to continue an existing novel, or what the import workflow is, state the conclusion first and only then collect the source text:

1. **Recommended order**: Run `/story-setup` first (deploy hooks/agents/AGENTS), start or refresh the session, run `/story-import`, then continue with `/story-long-write 日更/写第N章`.
2. **Running `/story-import` directly is also supported**: Before deep analysis, this skill checks `.story-deployed` and the specialist agent. If not deployed, it offers “run setup first” or “continue importing (serial fallback).”
3. **Projects already imported under the current protocol** (the book directory contains `追踪/_tracking-state.json`): Do not repeat the full import. Enter the book directory, confirm `.active-book` points to the correct title, and run `/story-long-write 日更` or `/story-long-write 写第N章`.
4. **Legacy tracking projects from v0.7.2 or earlier** (contain `追踪/` and body text, but no `追踪/_tracking-state.json`): Daily writing will stop and request a re-import, but **you do not need to decompose the entire book again**. Rebuild tracking only, as described under “Legacy Tracking Project Migration.”

This conclusion must appear before any follow-up question about the import source, so a user who only wants to confirm the process is not immediately asked to paste the book.

#### Legacy Tracking Project Migration

If the book directory contains `追踪/` and body text but no `追踪/_tracking-state.json`, the project uses the tracking structure from v0.7.2 or earlier. The body text, `设定/`, `大纲/`, and `拆文库/` remain unaffected. **Rebuild only `追踪/`**; do not rerun Phase 2 or touch the body text:

1. Find the last complete chapter number `N` (the highest number among `正文/第NNN章_*.md`).
2. Reconstruct the current state from existing files under the old `追踪/` (character state, foreshadowing, timeline, and so on, using the project’s actual filenames) and the latest 3–5 chapters: core-character snapshots, unresolved foreshadowing, revealed timeline events, long-term constraints, and promises for the next chapter. See [references/character-state-reverse.md](references/character-state-reverse.md) for reverse-engineering character snapshots.
3. Build JSON in the initialization-transaction format from [references/tracking-transaction.md](references/tracking-transaction.md), set `last_chapter` to `N` (do not fabricate per-chapter records for Chapters 1–N), and run `tracking_commit.py init`.
4. `init` moves the complete old tracking structure unchanged into `追踪/_旧追踪存档/`, then creates the current protocol in place. Old content is preserved for the author but excluded from parsing.
5. Run `tracking_commit.py check` and confirm it passes, then return to `/story-long-write 日更`.

Base the reconstruction on evidence from Step 2. Leave uncertain fields blank or put them in `continuity_risks`; do not invent. Run the full Phase 2 only when the user explicitly requests a complete reanalysis.

Ask the user: **“Which book would you like to import? Provide a file path or paste the text directly.”**

### Step 2: Confirm Intent (Writing Project vs. Decomposition Library Only)

The default goal is a **complete writing project** that can be continued. If the intent is unclear—whether the user wants a continuable project or only a decomposition-library analysis—**ask proactively** rather than assuming:

> “Would you like to turn this book into a continuable writing project (setting/outline/body/tracking, ready to write Chapter N+1), or do you only need a decomposition-library analysis?”

- Wants a continuable project → run all of story-import (Phase 2 decomposition + Phase 3 migration).
- Wants only analysis / a decomposition library → use `/story-long-analyze` (or `/story-short-analyze` for short fiction) and stop at the decomposition library; do not enter Phase 3.

### Step 3: Identify the Input Method

```
用户提供路径？
├─ 单文件路径（.txt/.md）
│   └─ 按章节分隔符自动切分
├─ 目录路径
│   └─ 按文件名排序，合并处理
└─ 无路径 → 用户直接贴文本？
              ├─ 是 → 保存到临时文件后处理
              └─ 否 → 提示用户提供源文件
```

### Step 4: Confirm Basic Information

1. **Automatic detection**: Identify the book title (when present), total chapter count, total character count, and chapter format from the text.
2. **User confirmation**:
   - Imported book title: {automatically detected or supplied by user}
   - Genre: {supplied by user}
   - Target platform: {Qidian/Tomato/Jinjiang/other}
   - Complete: {yes/no (partial draft through Chapter N)}
   - **Length type**: long-form / short-form. Detect automatically according to [references/length-routing.md](references/length-routing.md) (explicit user declaration > structural signals > character-count fallback), restate the result, and ask the user to confirm it. This result determines whether Phase 3 uses the long- or short-form path.
   - **Whether the final chapter is complete**: complete chapter / partial draft. If partial, tell the user and record “partial draft through Chapter N” in context. Let the user decide whether to “continue from the partial chapter” or “finish it before importing.” story-import records the decision and does not choose for the user.
3. **External comp (optional and separate from the import source)**: If the user explicitly selected an external comp, record `{对标书名}` and confirm `拆文库/{对标书名}/` is an independent decomposition of that reference work. Never consider `{导入书名}` or the decomposition directory just created for this import. If the user did not select one, do not ask another question; record “not linked” and leave discovery to the writing skill.
4. **Output confirmation**: Show the detected chapter range, character count, length classification, status of the final chapter, and “external comp: {title/not linked}.” Begin analysis after confirmation.

### Step 5: Check the Environment Up Front

Before Phase 2, check whether story-setup infrastructure has been deployed in the project:

- First read `.story-deployed` and apply the Spawn version gate at the top. Do not reuse a legacy `chapter-extractor` file even if it remains on disk.
- Only after `agents_version: 28` passes, check the current runtime’s canonical directory for the Phase 2 `chapter-extractor`: matching Markdown for Claude/OpenCode/Antigravity, matching TOML for Codex.
- If `.story-deployed` includes `zcode` under `target_cli`, missing project agents are expected under ZCode 3.3.4. Do not suggest redeploying; enter analysis with the serial solo/direct fallback and report it.

**If the deployment marker is absent, its version is invalid/outdated, or the current runtime’s agent is unavailable—and this is not a deployed ZCode project—** tell the user:

> “The writing infrastructure has not been deployed in this project. We recommend running `/story-setup` before returning to import; otherwise, deep analysis cannot use the parallel chapter-extractor agent.”

Offer two choices:

1. **Run setup first**: Pause import, run `/story-setup`, then trigger `/story-import` again after deployment.
2. **Continue importing**: Accept serial fallback in Phase 2 (long-form chapter summaries will not run in parallel, so processing is slower, but the outputs remain complete).

Store the user’s choice in context so Phase 2 can select parallel or serial execution.

### Step 6: Back Up the Source Text

The analyze pipeline invoked in Phase 2 owns the source backup (its preprocessing copies/saves the source to `拆文库/{导入书名}/原文/`; see “Source Backup (Pipeline Preprocessing)” in story-long-analyze and story-short-analyze). Phase 1 only confirms that the source is ready—a valid path or received text. Do not create a separate backup here, which would duplicate the analyze pipeline’s logic.

---

## Phase 2: Deep Analysis

Based on the length type selected in Phase 1, invoke the corresponding analyze skill’s **complete decomposition pipeline**. Do not run an incomplete process that merely “reuses the methodology”; drive the entire pipeline to completion and obtain all structured artifacts.

| Length | Decomposition Pipeline | Output Directory |
|------|--------------|---------|
| Long-form | Complete story-long-analyze pipeline (Stages 0–6) | `拆文库/{导入书名}/` |
| Short-form | story-short-analyze pipeline (Stages 2–6) | `拆文库/{导入书名}/` |

### Invocation Contract

#### Long-Form: Automatically Continue Past the Stage 1 Stop

After Stage 0+1 (the golden first three chapters), story-long-analyze **automatically pauses** and uses AskUserQuestion to ask whether to continue the full decomposition (its “Stage 1 Stop”). Importing, however, requires the complete Stage 2–6 artifact set—chapter summaries / aggregate analysis / `剧情/节奏.md` / `剧情/情绪模块.md` / setting and relationship files / consolidated report / prose style. If any are missing, Phase 3 receives only a partial project.

**Current decomposition contract**: `_progress.md` must use `schema_version: 2`, and `剧情/节奏.md` plus `剧情/情绪模块.md` are authoritative required import artifacts. If any are missing, repair or rerun the relevant Stage first; never assemble a seemingly complete imported project from summary files.

Therefore, invoke story-long-analyze from the outset in **“complete decomposition, run all at once, do not pause to ask” mode**, activating its skip-question path (when the user says “complete decomposition / all at once / systematic decomposition / don’t ask” at the start), so the pipeline continues automatically from Stage 2 through Stage 6.

- Example wording: When starting deep analysis, state, “Decompose this book in ‘complete decomposition, run all at once, do not pause to ask’ mode, ensuring all Stage 2–6 outputs are produced.”
- **Fallback**: If the runtime still stops at the Stage 1 question, story-import automatically chooses “continue full decomposition” and **never sends that checkpoint question to the user**.
- If the Phase 1 environment check finds no deployed chapter-extractor agent and the user chooses “continue importing,” Stage 2 chapter summaries fall back to serial processing. Outputs remain complete; only speed changes.

#### Short-Form: One Complete Pipeline

The story-short-analyze pipeline (Stages 2–6) has **no Stage 1 stop** and should run to completion in one pass. Run all four Phase 1 Steps, applying the import-specific values below; do not skip the section wholesale:

| Phase 1 Step | Handling During Import |
|-------------|----------------|
| Step 1: Obtain source text | Use the source already confirmed in story-import Phase 1; do not ask again |
| Step 2: Character-count check (length routing) | Length was classified and confirmed in story-import Phase 1; answer “continue as short-form” directly without rerouting |
| Step 3: Detect genre | **Run normally**; the genre rubric must be loaded. Substitute the genre confirmed in story-import Phase 1 Step 4 without asking again |
| Step 4: Resume check (when `拆文库/{导入书名}/_meta.json` exists, choose one of three) | First see whether old outputs can be reused directly: if `stages_completed` includes 6, `拆文报告.md` / `情节节点.md` / `写作手法.md` / `原文/` are all nonempty, and the source matches this import → enter Phase 3 directly without rerunning or archiving. Otherwise, on the first Phase 2 entry in this run → choose (a) overwrite: archive old output to `拆文库/{导入书名}/_archive_{时间戳}/`, then rerun from Stage 2. For a retry of the same book within the same import run → choose (b) resume. Do not send the three-way choice to the user and do not skip archiving. |

`genre_detected` in `_meta.json` is a blocking required field produced by Step 3. Downstream story-short-write uses it to select the genre rubric. **Do not skip Step 3 and begin at source backup.**

- Example wording: “《{导入书名}》 has been confirmed as short-form (genre: {题材类型}, approximately {N} characters). Step 2 will continue as short-form; Step 4 will overwrite after archiving; genre detection will still run; produce all Stage 2–6 outputs.”
- **Fallback**: If the runtime still asks “This text is {N} characters and may be too long; use `/story-long-analyze` instead?” or “This falls between short and long; decompose as short or long?”, respond exactly “按短篇继续” based on the locked Phase 1 classification and **never pass the routing question to the user**.

### Output Directories

#### Long-Form Decomposition-Library Structure

Long-form analysis outputs to `拆文库/{导入书名}/`, exactly matching the story-long-analyze pipeline:

```
拆文库/{导入书名}/
├── 原文/
│   └── 原文.txt          # 扩展名随源文件；对话直接贴入的文本存为 原文.md
├── 概要.md
├── 章节/
│   ├── 第1章_深度拆解.md
│   ├── 第1章_摘要.md
│   └── ...               # 每章同时有 第N章_深度拆解.md 和 第N章_摘要.md
├── 快速预览.md
├── 角色/
│   ├── {角色名}.md
│   └── 角色关系.md
├── 剧情/
│   ├── {剧情标题}.md
│   ├── 故事线.md
│   ├── 节奏.md          # 关键信息推进 / 情绪触动点 / 爆发节奏
│   ├── 情绪模块.md      # 读者需求 / 情绪引擎 / 可复现模块
│   └── 散落情节.md
├── 设定/
│   ├── 世界观/         # 背景设定.md / 力量体系.md / 地理.md / 金手指.md（子目录形态）
│   └── 势力/           # {势力名}.md（每势力一文件）
├── 拆文报告.md
├── 文风.md          # Stage 6 文风：写作技法视图 + 原文范例锚点
└── _progress.md
```

#### Short-Form Decomposition-Library Structure

Short-form analysis outputs to `拆文库/{导入书名}/`, matching the story-short-analyze pipeline:

```
拆文库/{导入书名}/
├── 原文/
│   └── 原文.txt          # 扩展名随源文件；对话直接贴入的文本存为 原文.md
├── 拆文报告.md
├── 情节节点.md
├── 写作手法.md
└── _meta.json           # 管道元数据 + 结构计数（下游 story-short-write 必读）
```

### Complete Long-Form Pipeline (Stages 0–6)

> See story-long-analyze (run `/story-long-analyze`) for detailed pipeline instructions. Only a summary appears here.

| Stage | Name | Input | Output | Completion Signal |
|------|------|------|------|----------|
| 0 | Synopsis extraction | Raw text | 概要.md + chapter index | Chapter structure identified |
| 1 | Golden first three chapters | First three chapters | 第1章_深度拆解.md / 第2章_深度拆解.md / 第3章_深度拆解.md → **pause output 快速预览.md** (import continues automatically without asking) | Three chapters decomposed |
| 2 | Chapter summaries | Chunked chapter text | 章节摘要.md (plot points + characters + **key information and expansion techniques**). 10–40 plot points per chapter (one per 150–200 characters, adjusted dynamically). Character filtering (exclude walk-ons, normalize aliases). **Parallel chapter-extractor agent mode** (serial fallback when undeployed). **Count validation: summaries == chapters**. | All chapters processed |
| 3 | Aggregate analysis | All chapter summaries | `剧情/*.md` + `剧情/README.md` + `剧情/故事线.md` + **`剧情/节奏.md` + `剧情/情绪模块.md`**. **Story-framework identification** first. **Two-step plot aggregation** (identify the plot outline from summaries, then assign plot points to it). **Key-information progression index**, **emotional touchpoints and release pacing**, and **reader needs / emotional engines / reproducible modules**. **Character merging** (deduplicate across chapters + normalize aliases). **Character tiers** (protagonist/antagonist/core supporting/functional). **Loose-plot fallback** (six steps, including coverage validation). **Quality checks** (confidence ≥0.85 / coverage 85%–95% / overlap ≤35%). | Quality checks pass |
| 4 | Setting + relationships | Merged Stage 3 character data + plot points | 设定/*.md + 角色/*.md. **Two-stage character model**. **Alias resolution** (automatically merge at confidence ≥0.85). | Setting and relationships extracted |
| 5 | Consolidated report | All output | 拆文报告.md (including “reader needs / emotional engines,” “key information and expansion techniques overview,” “pacing and emotional touchpoints,” and “reproducible modules,” with links to `剧情/节奏.md` / `剧情/情绪模块.md`) | Report generated |
| 6 | Prose style | 拆文报告.md + 章节/第1-3章_深度拆解.md + 章节/*_摘要.md + 原文/原文.txt | 文风.md (historical analysis of this book’s writing techniques) | Style saved to `拆文库/{导入书名}/文风.md`; retain as import analysis and do not copy into this book’s `对标/` |

### Short-Form Decomposition Pipeline

> See story-short-analyze (run `/story-short-analyze`) for detailed pipeline instructions. Only a summary appears here.

Short-form uses one complete, strictly serial Stage 2–6 pipeline saved under `拆文库/{导入书名}/`: Stage 2 structure + plot points → Stage 3 emotional arc + high-impact moments → Stage 4 reversals + writing techniques → Stage 5 characters + opening/ending → Stage 6 overall evaluation. The final outputs are `拆文报告.md`, `情节节点.md`, and `写作手法.md`, plus `_meta.json` containing pipeline metadata and structure counts.

For long-form chunking, reuse story-long-analyze: Stage 2 runs chapter-extractor agents in parallel, while later Stages apply that skill’s chapter-count thresholds from “Chunking Strategy.” story-import does not define another system.

### Recovery

- Track progress in the progress file if interrupted
- Read the progress file in a new session to locate the breakpoint
- Resume from the first chapter in the interrupted block
- Long-form progress uses the paragraph conventions from the story-long-analyze pipeline and includes the current Stage, last processed chapter, completed-Stage list, and update time

### Quality Checks

Before completing long-form Stages 3–4, run the quality checks built into story-long-analyze (confidence ≥0.85, coverage 85%–95%, overlap ≤35%). See the completion criteria in each story-short-analyze Stage for short-form quality checks.

---

## Phase 3: Structural Migration

Migrate the analysis from `拆文库/{导入书名}/` into a project structure that the writing skills can consume.

### Routing

Route according to the length classification from Phase 1. The two paths produce completely different project structures:

| Length | Migration Path | Mapping Rules | Continued By |
|------|---------|---------|---------|
| Long-form | **3-L: Long-Form Structural Migration** | [references/structure-mapping-long.md](references/structure-mapping-long.md) | story-long-write daily-writing loop |
| Short-form | **3-S: Short-Form Structural Migration** | [references/structure-mapping-short.md](references/structure-mapping-short.md) | story-short-write Phase 3 scene-by-scene writing |

---

## Phase 3-L: Long-Form Structural Migration

Migrate `拆文库/{导入书名}/` into the long-form project structure under `{导入书名}/`. See [references/structure-mapping-long.md](references/structure-mapping-long.md) for detailed mapping rules.

### Migration Steps

#### Step 1: Create the Project Skeleton

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
├── 对标/                       # 可选；仅在显式绑定外部对标时创建子目录
└── 参考资料/
```

#### Step 2: Normalize Body Text

Migrate the source into `正文/` and normalize filenames to `第XXX章_章名.md`.

- Recognize chapter separators (第X章, Chapter X, and so on)
- Extract chapter titles
- Zero-pad chapter numbers (第1章 → 第001章)
- Preserve body text unchanged

#### Step 3: Migrate Character Files

Migrate `拆文库/{导入书名}/角色/{角色名}.md` to `设定/角色/{角色名}.md`.

During migration, complete the story-long-write character-template fields according to the “Character File Migration Template” in `references/structure-mapping-long.md`.

Character tiers (reuse story-long-analyze standards):

| Tier | Standard | Migration Strategy |
|------|------|---------|
| Protagonist | Appears in ≥50% of chapters + advances main plot + complete growth arc | Full migration |
| Antagonist | Opposes protagonist + drives central conflict + clear motive | Full migration |
| Core supporting character | Appears in ≥20% of chapters or advances a major subplot | Full migration |
| Functional character | Appears in <20% of chapters + limited function | Simplified migration |

#### Step 4: Migrate Relationship Files

Convert `拆文库/{导入书名}/角色/角色关系.md` into `设定/关系.md`, using the target template under “Relationship File Conversion Rules” in [structure-mapping-long.md](references/structure-mapping-long.md).

#### Step 5: Synchronize Worldbuilding

The current decomposition contract already outputs themed files under `拆文库/{导入书名}/设定/世界观/*.md` and `设定/势力/*.md`. Copy them unchanged into the project. `世界观/` must contain `背景设定.md`. `力量体系.md` may be omitted when it is under 200 characters and has already been merged into `背景设定.md`; otherwise, stop on a missing required current artifact and instruct the user to rerun story-long-analyze Stage 4. Do not split flat files during import.

#### Step 6: Generate Outlines

**大纲.md** (volume-level structure): Reverse-engineer it from `剧情/故事线.md`, `剧情/*.md`, and `快速预览.md`. **Volume divisions require user confirmation**, according to “Outline Reverse-Engineering Rules” in [structure-mapping-long.md](references/structure-mapping-long.md):

- **Source has explicit volume boundaries** (volume-level headings such as “第一卷” or “卷一”) → follow them directly without asking.
- **Source has no explicit volume boundaries** → **do not mechanically split into “20–40 chapters per volume.”** Detect candidate boundaries from storylines, setting changes, and major time skips; show the candidates to the user and **wait for confirmation** before finalizing volume outlines. Until then, `大纲/大纲.md` records candidates only.

```markdown
# 全书大纲

## 卷级大纲

### 第一卷：{卷名}（约 {X} 万字，{Y} 章）
- 功能：{从剧情分析推断}
- 核心事件：{一句话}
- 起始状态 → 结束状态：{从角色弧线推断}
```

**Volume outlines**: After confirming divisions, aggregate plot files into `大纲/卷纲_第X卷.md` using the “Volume Outline Reverse Engineering” template in [structure-mapping-long.md](references/structure-mapping-long.md).

**Detailed outlines**: Reverse-engineer chapter summaries into `大纲/细纲_第XXX章.md`:

For each chapter, first run `wordcount measure` through story-long-write’s Wordcount Core and use the JSON `actual` as the historical length snapshot. This records the source chapter’s actual length under `visible_chars_v1`; it does not ask the model to choose a new writing target. Probe `python3`, `python`, then `py -3`. If Python 3 or the CLI is unavailable, return `TOOL_UNAVAILABLE` and stop the import; never estimate with the model or silently skip it.

```bash
{PYTHON} {story-long-write skill 根}/scripts/storyctl.py wordcount measure \
  --file "{原文章节文件}" \
  --chapter {N}
```

```markdown
## 细纲（第 N 章）

### 第 N 章：{章名}
- 核心事件：{从摘要中提取}
- 字数目标：{storyctl 返回的 actual} 字
- 字数口径：visible_chars_v1
- 目标情绪：{从章节基调/情绪曲线提取；未知写 [待补充]}
- 章首钩子：[待补充]
- 爽点：{从情节点推断；无明确证据写 [待补充]}

#### 内容概括（五段式）
- 起因：{从情节点归纳；未知写 [待补充]}
- 发展：{从情节点归纳；未知写 [待补充]}
- 转折：{从情节点归纳；未知写 [待补充]}
- 高潮：{从情节点归纳；未知写 [待补充]}
- 结尾：{原文最后落在什么动作/画面/台词上；未知写 [待补充]}

#### 情节安排（多线）
- 主线推进：{从剧情单元索引/摘要反推}
- 辅线推进：{无证据写“无”或 [待补充]}
- 事件线 / 任务线：{外部事件链}
- 感情线 / 关系线：{有证据才写；否则“无显性”或 [待补充]}
- 逻辑线：原因 → 行动 → 结果 → 后果/新问题

#### 人物关系和出场顺序
- 出场顺序：{摘要中角色/势力/关键物件出现顺序}
- 人物关系变化：{本章前 → 本章后；未知写 [待补充]}
- 视角/信息差：{谁知道什么；读者知道什么；主角误判什么；未知写 [待补充]}

#### 情节细化
- 情节点序列（逐行填下表；从摘要情节点反推）：

| # | 情节点（谁做了什么） | 功能标签 | 执行边界 |
|---|---|---|---|
| 1 | {} | {功能不明写 [待补充]} | {从原文确认本点没有释放什么；未知写 [待补充]} |
- 行动成本（可无）/收益归属：{有证据才写；行动成本可无、不硬造；未知写 [待补充]}

#### 结尾设定和钩子
- 结尾设定：{原文收束落在什么动作或画面；未解决问题；下一章推动力；未知写 [待补充]}
- 章尾钩子：[待补充]
```

> Mark hooks, relationship changes, subplot/romance lines, action costs/reward ownership, and any other fields that cannot be reliably inferred from source summaries as `[待补充]`. story-import reverse-engineers only evidence-backed blueprints and never invents relationships or subplots to fill fields.

#### Step 7: Generate Tracking Files

An imported project must use the bundled `scripts/tracking_commit.py init` to generate tracking state atomically. The model must not write final tracking files separately. See [references/tracking-transaction.md](references/tracking-transaction.md) for complete fields and commands. Prepare semantics in this order:

1. **Import cutoff chapter**: Set `last_chapter` in the initialization transaction to the last complete chapter, N. The tool records `imported_through_chapter=N` in metadata. Imported old chapters have no daily-writing transactions; do not fabricate per-chapter increments for Chapters 1–N or create a duplicate narrative baseline of the current state.
2. **Current core-character snapshots**: Reverse-engineer the protagonist, antagonist, and core supporting characters’ states through Chapter N from decomposition artifacts and write them by character into `character_snapshots` in the initialization JSON. The tool outputs them to `追踪/角色状态/{角色名}.md`; see [references/character-state-reverse.md](references/character-state-reverse.md) for the algorithm.
3. **Current foreshadowing rows**: Generate `foreshadow` from setup/payoff events supported by evidence in the body text. Keep one current-state row per ID. Future plans not yet planted remain in the outline and do not enter `伏笔.md`.
4. **Facts and reader knowledge**: Convert key events into `timeline_events`. For each event, record objective fact, what readers know through Chapter N, and actual reveal state. Never present a planned future reveal chapter as an event that has already occurred.
5. **Continuation-state-card input**: Prepare current location, long-term constraints, active core characters, notes on the latest three chapters, promises for the next chapter, and continuity risks. The tool generates a fixed seven-section `上下文.md`; do not put style notes, file indexes, ordinary to-dos, or QA counts in the continuation card.
6. **Run initialization**: Probe Python 3 for the current platform (`python3` → `python` → `py -3`) and run:

   > If the project’s `追踪/` already contains legacy files outside the current protocol, no manual cleanup is required. `init` first moves them unchanged into `追踪/_旧追踪存档/`, then creates the current protocol in place. The old material remains available to the author but is excluded from parsing; current state is determined entirely by this import input. A validation-failed `init` moves nothing.

   ```text
   {PYTHON} {story-import skill 根}/scripts/tracking_commit.py init --project {项目根} --input {初始化事务.json}
   {PYTHON} {story-import skill 根}/scripts/tracking_commit.py check --project {项目根}
   ```

For example, when importing the demo 《让你管账号，你高燃混剪炸全网》 through Chapter 10: the continuation-state card must state that Jiang Chen’s original mobile-phone cut of 《诸君，且听龙吟》 was remade in HD by a professional team, but senior leadership decided the remake “lacked its soul” and ultimately kept the original. Jiang Chen’s snapshot should reflect that Zhou Bosen and Zhang Yaozu have recognized the value of his military-publicity work. The reader timeline includes only the screening meeting’s conclusion already shown to readers. If the training plan behind Zhong Jiajia’s “only half right” remark has not been revealed, it may appear only in author truth and must not leak into the reader view.

After successful initialization, the result should be:

```text
追踪/
├── _tracking-state.json
├── 上下文.md
├── 逐章记录/                 # 导入旧章不补造文件，续写从第 N+1 章开始
├── 角色状态/{角色名}.md
├── 伏笔.md
├── 时间线/
│   ├── 作者真相.md
│   └── 读者已知.md
```

If the partial work’s final chapter is unfinished, `last_chapter`, character snapshots, and other current semantic checkpoints must stop at the last complete chapter. Put the partial-draft strategy under continuity risks; do not record incomplete actions as established facts.

#### Step 8: Generate Genre Positioning

Extract key findings from the decomposition report and generate `设定/题材定位.md` using the “Genre Positioning Generation” template in [structure-mapping-long.md](references/structure-mapping-long.md).

The book’s genre, core hook, emotion, and pacing summary in `设定/题材定位.md` come from `拆文库/{导入书名}/`, but these fields do not register a comp title. Append the “comp-title list + primary comp title” section only if Phase 1 explicitly linked an external comp. There may be at most one primary comp; secondary/reference comps are unlimited. If no comp was linked, omit the entire registration section and never use `{导入书名}` as a placeholder. See “Comp-Title List” under the referenced “Genre Positioning Generation” template.

If a quick overview is later needed, a separate “Comp Analysis (Derived Summary)” table may be written. It is not the authoritative registry and does not replace `主对标书` or the complete `对标书列表`. Every registered item must trace back to `拆文库/{对标书名}/`, never to the book root’s `设定/`.

#### Step 9: Synchronize Structured Comp Assets

This step handles only external reference works explicitly linked in Phase 1. Synchronize structured analysis assets from `拆文库/{对标书名}/` to the project reference view `{项目}/对标/{对标书名}/` for story-long-write to read first. If no external comp is linked, skip this step and do not create an empty directory. Never use `拆文库/{导入书名}/` or project `设定/` as the copy source. See “Comp Reference-View Synchronization Rules” in [structure-mapping-long.md](references/structure-mapping-long.md) for the complete source-to-destination mapping.

**Missing-artifact handling**:

- If a selected external comp lacks `剧情/节奏.md` or `剧情/情绪模块.md`, do not register it or generate a partial comp view. Report `module_or_rhythm_required_missing` and instruct the user to rerun `/story-long-analyze` Stage 3+ for `{对标书名}`. Do not roll back the imported book’s core-project migration.
- If other structured subdirectories are missing, report them using the existing missing-import-item guidance; do not block project creation.

#### Step 10: Synchronize Prose Style

Once the external comp passes Step 9 validation, copy `拆文库/{对标书名}/文风.md` to `{项目}/对标/{对标书名}/文风.md`. Copy only; do not regenerate. Skip when no external comp is linked.

**Missing-artifact handling**:

- If the decomposition library has no prose-style file (analyze did not run Stage 6), tell the user in the import report to rerun `/story-long-analyze` and then synchronize again. Daily writing will fail fast if style is missing.
- If the project comp directory contains an older style file, overwrite it with the latest decomposition output and note this in the import report.

---

## Phase 3-S: Short-Form Structural Migration

Migrate the short-form decomposition artifacts from `拆文库/{导入书名}/` into the short-form project under `{短篇标题}/`, ready for story-short-write Phase 3 scene-by-scene continuation. See [references/structure-mapping-short.md](references/structure-mapping-short.md) for detailed rules.

> **Short-form and long-form projects are completely different**: Short-form body text is one `正文.md` file (not split into chapters), and it **does not produce** long-form directories such as `追踪/`, `大纲/`, or `正文/`. Never create those during short-form migration.

### Target Short-Form Project Structure

```
{短篇标题}/
├── 设定.md              ← 含核心框架 + 本书续写基线
├── 小节大纲.md          ← 按段-小节结构反推
├── 正文.md              ← 单文件全文正文
└── 对标/{对标书名}/     ← 可选：仅外部对标引用视图
    ├── 拆文报告.md
    ├── 情节节点.md
    └── 写作手法.md
```

### Migration Steps

#### Step 1: Migrate Body Text

Move the complete text from `拆文库/{导入书名}/原文/` into the single file `{标题}/正文.md`. Normalize formatting according to [format-and-structure.md](references/format-and-structure.md): section markers use `###1.`, paragraphs use single line breaks only, and dialogue quotation marks follow project/platform conventions. **The source is an existing draft; do not rewrite it, only normalize formatting.**

#### Step 2: Generate the Setting File

Reverse-engineer `{标题}/设定.md` from `拆文报告.md` and `写作手法.md`, with two sections:

- **Core framework**: Match the story-short-write framework template (basic information, one-sentence premise, central reversal, emotional design, and character sketches).
- **Continuation baseline for this book**: Record the written material’s story structure, emotional pacing, central-reversal mechanism, and established writing techniques. This is internal context for the book, not a comp summary.

#### Step 3: Generate the Section Outline

Reverse-engineer `{标题}/小节大纲.md` from the functional segments in `情节节点.md`, mapping them to opening/setup/escalation/reversal/ending sections. Short-form uses a lightweight blueprint only: for each section, record `结构段/五段功能`, the main event, one or more real advances, target emotion, character/relationship change, causal/logical chain, and ending handoff/small hook. Related plot points may be fulfilled simultaneously by one action chain or conversation; do not split them into multiple subevents to meet a count. Mark uncertain hooks or relationships `[待补充]`; do not apply the full long-form chapter blueprint.

#### Step 4: External Comp Reference View (Optional)

Only when Phase 1 explicitly linked an external `{对标书名}` should `拆文库/{对标书名}/` be synchronized into `{标题}/对标/{对标书名}/`. Otherwise skip this step. Never copy all of `拆文库/{导入书名}/` into `对标/`.

---

## Phase 4: Activate the Project

### Step 1: Quality Check

Use the appropriate checklist for the detected length:

- **Long-form**: See the complete import checklist at the end of [references/structure-mapping-long.md](references/structure-mapping-long.md), including body-file count comparison, independent snapshots for core characters, separation of author/reader timelines, successful `tracking_commit.py check`, and user-confirmed volume divisions.
- **Short-form**: See the checklist at the end of [references/structure-mapping-short.md](references/structure-mapping-short.md), including existence and valid formatting of a single `正文.md`, both the core framework and continuation baseline in `设定.md`, and absence of mistakenly created long-form-only directories.

### Step 2: Report Missing Items

Output an import summary and outstanding items for the relevant length branch.

**Long-form import completion report**:

```
=== 导入完成报告（长篇）===
书名：{导入书名}
源文件：{X} 章，{Y} 万字
项目目录：{路径}

## 已生成文件
- 正文：{N} 章
- 角色文件：{M} 个
- 大纲：大纲.md + {V} 个卷纲 + {N} 个细纲
- 追踪：唯一结构化 state + 核心角色独立派生快照 + 伏笔当前视图 + 时间线双视图 + 空逐章记录目录 + 固定 7 栏上下文
- 设定：{世界观文件数} 个
- 外部对标：{未绑定 / 已从 `拆文库/{对标书名}/` 同步到 `对标/{对标书名}/` / 绑定失败及修复动作}

## 待补充项
- [ ] 细纲中的章首/章尾钩子需要补充
- [ ] 题材定位的核心梗三分法需要确认
- [ ] 伏笔追踪中的伏笔已复核
- [ ] `追踪/时间线/读者已知.md` 未泄露 `作者真相.md` 中尚未揭示的事实
- [ ] 卷划分已确认（原文无明确卷界时）
- [ ] `拆文库/{导入书名}/` 未被复制到项目 `对标/`，本书未登记为自身对标
- [ ] 若绑定外部对标，`设定/题材定位.md` 的 `主对标书` 与 `对标书列表` 只包含独立 `{对标书名}`，且同步来源与目录名一致

## 下一步操作
- 运行 `/story-review lean` 审查导入结果
- 运行 `/story-long-write` + "日更" 开始续写
```

**Short-form import completion report**:

```
=== 导入完成报告（短篇）===
标题：{短篇标题}
源文件：{Y} 字
项目目录：{路径}

## 已生成文件
- 正文.md（单文件，{Y} 字）
- 设定.md（核心框架 + 本书续写基线）
- 小节大纲.md（{N} 个小节）
- 外部对标：{未绑定 / `对标/{对标书名}/` 已同步 / 绑定失败及修复动作}

## 待补充项
- [ ] 所有 [待补充] 标记的文件已复核
- [ ] 小节大纲的章首/章尾钩子需要补充
- [ ] 核心反转的铺垫线索已确认

## 下一步操作
- 运行 `/story-short-write` Phase 3 开始续写
```

### Step 3: Activate the Project

- Set `.active-book` to the imported book/title directory
- Confirm the appropriate writing skill recognizes the project (long-form → story-long-write; short-form → story-short-write)
- Optional validation: If the current runtime’s canonical directory contains a deployed story-explorer agent, spawn it to cross-check migrated data completeness. For Antigravity, check `.agents/agents/story-explorer/agent.md` and use `invoke_subagent` + `TypeName: "story-explorer"`. Prompt: `项目目录：{dir}\n查询类型：progress\n查询参数：导入验证`

> The setup environment check already ran in Phase 1 under “Check the Environment Up Front”; do not repeat it here.

---

## Large Works (>200 Chapters)

> This section applies only to long-form imports. Short-form uses full single-file migration and has no incremental import requirement.

For works over 200 chapters, **decomposition may be batched, but tracking initialization must cover all written chapters at once**:

1. **Batch decomposition**: Initially perform deep decomposition on the first 50 chapters plus a complete synopsis; add more chapters to `拆文库/` later as needed.
2. **Initialize tracking once through the end**: Set initialization `last_chapter` to **N, the final completed chapter**, not 50, the initial decomposition batch. `init` writes `imported_through_chapter` once and never advances it later; per-chapter transactions accept only N+1 onward. Do not fabricate per-chapter records for Chapters 1–N; continuation begins at N+1. If initialization mistakenly used 50, Chapters 51–N may still be filled with sequential `append` calls (one transaction per chapter, with contiguous chapter numbers), but this requires building transactions for every already-written chapter. Do not delete `追踪/` and start over, because `_旧追踪存档/` is inside it too.
3. **Context summaries**: Generate simplified summaries (200 Chinese characters per chapter) for chapters not deeply decomposed, to support reverse-engineering the current state.

---

## Reference Index

Load by Phase; do not load everything at once.

All reference files bundled with this skill are under `references/` and should be loaded only for the relevant scenario. When a method/template belongs to another skill, story-import runs its `/命令` so that skill loads its own files rather than loading them directly.

### Phase 1: Confirm Import Source

| Scenario | Load |
|------|---------|
| Determine length route | `references/length-routing.md` |
| Recognize chapter formatting | Handled by Stage 1 of the story-long-analyze pipeline (run `/story-long-analyze`) |

### Phase 2: Deep Analysis

| Scenario | File / Related Skill |
|------|---------|
| Long-form deep analysis (includes methodology, quality checks, and output templates) | Run `/story-long-analyze` to invoke the long-form pipeline |
| Short-form deep analysis (includes methodology, quality checks, and output templates) | Run `/story-short-analyze` to invoke the short-form pipeline |

### Phase 3: Structural Migration

| Scenario | Load |
|------|---------|
| Long-form migration mapping | `references/structure-mapping-long.md` |
| Short-form migration mapping | `references/structure-mapping-short.md` |
| Reverse-engineering character state (long-form) | `references/character-state-reverse.md` |
| Character-state rules (dependency of character-state-reverse.md) | `references/state-tracking.md` |
| Short-form body-text formatting | `references/format-and-structure.md` |

> See story-long-write (Phase 3 detailed-outline section) for the long-form detailed-outline template and story-short-write (core-framework section) for the short-form framework template. These are textual instructions only; story-import does not load those skill files.

### Phase 4: Activate the Project

| Scenario | Description |
|------|---------|
| Long-form project structure | See story-long-write (Phase 4 project-file structure) |
| Short-form project structure | See story-short-write (Phase 3 project structure) |
| Environment deployment | `/story-setup` provides deployment templates; story-import does not deploy them |

---

## Workflow Handoff

**Pipeline:** Long-form / short-form
**Position:** Import (before starting a book)

| When | Go To | Command |
|---|---|---|
| Continue writing after import (long-form) | story-long-write | `/story-long-write` + “日更” |
| Continue writing after import (short-form) | story-short-write | `/story-short-write` |
| Review quality after import | story-review | `/story-review` |
| Deeply analyze a comp (long-form) | story-long-analyze | `/story-long-analyze` |
| Deeply analyze a comp (short-form) | story-short-analyze | `/story-short-analyze` |
| Start a new long-form book from scratch | story-long-write | `/story-long-write` + “开书” |
| Start a new short-form book from scratch | story-short-write | `/story-short-write` |
| Project environment not deployed | story-setup | `/story-setup` |

---

## Language

- Reply in the user’s language
- Chinese responses must follow the Chinese Copywriting Style Guide
