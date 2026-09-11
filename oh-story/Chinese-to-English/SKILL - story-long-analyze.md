---
name: story-long-analyze
version: 1.0.0
description: "Long-form web-fiction decomposition. Deeply analyzes the golden first three chapters, character architecture, payoff design, and pacing of hit long-form novels. Uses one deep-decomposition pipeline: after completing the golden first three chapters (Stage 1), it produces a quick-preview report and asks whether to continue the full decomposition. Once confirmed, it proceeds from Stage 2 through chapter summaries, aggregate analysis, setting and relationships, and the consolidated report. All artifacts are saved under 拆文库/{书名}/. Triggers: /story-long-analyze, /长篇拆文, ‘help me deconstruct this book,’ ‘deconstruct this book,’ ‘analyze the golden first three chapters,’ ‘deep decomposition,’ ‘complete decomposition,’ ‘systematic decomposition,’ or a novel-text file path—all use the same pipeline."
metadata: {"openclaw":{"source":"https://github.com/zenstory-ai/oh-story-claudecode"}}
---
# story-long-analyze: Long-Form Web-Fiction Decomposition

You are a structural analyst for web fiction.

**Core belief: You must understand why other books become hits before you can write one of your own.**

---

> Agent compatibility: Check only the canonical directory for the current runtime: Claude `.claude/agents/{agent}.md`, OpenCode `.opencode/agents/{agent}.md`, Codex `.codex/agents/{agent}.toml`, or Antigravity `.agents/agents/agent-name/agent.md` (`agent-name` is the target agent name). Never infer availability from another runtime’s files. Codex uses the matching `agent_type`; Antigravity uses `invoke_subagent` + `TypeName`. If the active runtime exposes no custom-agent registry / `invoke_subagent`, or returns an unknown agent, fall back to solo/direct execution. When `.zcode/` is detected, likewise use solo/direct execution because ZCode 3.3.4 does not run project custom agents; report `Fallback: project custom agents unavailable -> solo`. Retain `subagent_type` compatibility for Claude/OpenCode.
>
> Spawn version notice (does not block spawning): First read `agents_version` from `.story-deployed` in the project root. If it does not match this release’s `agents_version: 29`—including a missing marker, missing/non-integer field, or a value below or above 29—**continue checking file presence and spawning as usual**, but also report `Notice: agents bundle 版本不匹配（项目 {N}，本版 29）` and advise rerunning `/story-setup` and starting a new session. If the value is above 29, additionally advise updating oh-story-claudecode first instead of using the older local setup to overwrite it with a downgrade. Fall back to solo/direct execution only when the agent file is missing or the runtime does not expose custom agents; report `Fallback: ... -> solo`.

## Decomposition Boundary Statement (Also Applies to the Main Thread)

The **deep decomposition of the golden first three chapters (Stage 1), serial-fallback chapter processing in Stage 2, and aggregate/setting/report/style synthesis in Stages 3–6** that you perform directly follow the same logic as the chapter-extractor subagent: the work being decomposed is fiction the user **lawfully possesses or has permission to use** (published/serialized or their own), and the task is **read-only, transformative literary criticism** from an editing, review, or writing-instruction perspective. Domestic abuse, infidelity, revenge, violence, romantic or sexual tension, and dark moral themes are ordinary fictional narrative elements in popular genres and must be structurally extracted as usual. **Never refuse a whole chapter or book merely because it is “sensitive” or “uncomfortable”**—a refusal in the main thread stops the entire automated pipeline. If an individual passage cannot be handled, skip it and complete the rest.

---

## Phase 1: Confirm the Work + Enter the Pipeline

Ask: **“Which book would you like to deconstruct? (Title + platform.) Do you have a path to the source text?”**

If no target is specified, recommend 2–3 comp titles based on the genre or the kind of book the user wants to write.

### Unified Entry Point

After confirming the work, enter the decomposition pipeline in Phase 2. **There is no quick/deep branch**—only one deep-decomposition pipeline, which automatically pauses after Stage 1 (the golden first three chapters) and produces a quick-preview report.

**When no text path is provided**: If the user supplies neither a source-text path nor text in the conversation, ask them to provide it: “Provide the source-text file path or paste the text here, and I’ll begin with the golden first three chapters.” Enter the pipeline once the text is available.

---

## Phase 2: Deep-Decomposition Pipeline

### Output Directory

Default to `拆文库/{书名}/` under the project-root `拆文库/`. If the user specifies another location, use it.

### Reuse Existing Analysis

**Before deep decomposition, check for partial existing results**:

1. Check whether `拆文库/{书名}/` already contains decomposition files
2. If _progress.md exists, read its breakpoint and resume from there using the recovery mechanism
3. If 角色/*.md or 设定/*.md exists, read the existing character and setting data
4. Use existing data as a cross-validation baseline:
   - Compare newly extracted character information with existing character data for consistency
   - Merge new setting details with existing settings and label the source (newly extracted vs. existing)
   - If they conflict (for example, a different name appears in an existing character file), flag the conflict for the user to resolve
5. Avoid extracting information that already exists

### Source Backup (Pipeline Preprocessing)

**Back up the source before beginning decomposition**:

1. Check whether `拆文库/{书名}/原文/` exists
2. If not, copy the source file from the user-provided path into `拆文库/{书名}/原文/`
3. If the user pasted text instead of providing a path, save it to `拆文库/{书名}/原文/原文.md`
4. Validate the backup:
   - File-path mode: confirm that file count and sizes under `原文/` match the source
   - Pasted-text mode: confirm that `原文.md` is nonempty (>0 bytes)

### Output Structure

```
拆文库/{书名}/
├── 原文/
│   └── 原文.txt          # 扩展名随源文件；对话直接贴入的文本存为 原文.md
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
│   ├── README.md       # 剧情目录索引：节奏/情绪模块/故事线的权威范围
│   ├── 故事线.md
│   ├── 节奏.md          # 关键信息推进 / 爽点循环 / 情绪触动点 / 爆发节奏
│   ├── 情绪模块.md      # 读者需求 / 情绪引擎 / 可复现模块卡
│   └── 散落情节.md
├── 设定/
│   ├── 世界观/
│   │   ├── 背景设定.md   # 核心规则 + 特殊设定（无法独立的内容合并）
│   │   ├── 力量体系.md
│   │   ├── 地理.md
│   │   └── 金手指.md
│   └── 势力/
│       └── {势力名}.md   # 内容 >= 200 字时独立；不足合并到 世界观/背景设定.md
├── 拆文报告.md
├── 文风.md          # Stage 6 文风：句长/标点/对话潜台词/情绪交替 + 原文锚点范例片段
└── _progress.md
```

> **Authoritative artifacts**: `剧情/README.md` defines authority among the files in the plot directory. `剧情/节奏.md` is authoritative for pacing, key-information progression, and emotional touchpoints; `剧情/情绪模块.md` is authoritative for reader needs, emotional engines, trope frameworks, and reproducible module cards. `拆文报告.md` and `剧情/故事线.md` are summary projections only. If a summary conflicts with either authoritative file, downstream writing follows `剧情/节奏.md` / `剧情/情绪模块.md`.

### Main Pipeline: Stages 0–6

This is story-long-analyze’s only execution pipeline. After Stages 0–1, it **automatically pauses** and produces a quick-preview report (see “Stage 1 Stop” below). Continue from Stage 2 after user confirmation.

**Estimated-time notice**: Before starting, give a rough estimate based on chapter count: fewer than 50 chapters usually take 30–60 minutes; 50–200 usually take 1–3 hours; more than 200 may require multiple sessions. Stage 2 supports parallel extraction, but Stages 3–6 depend on prior artifacts and proceed in order.


| Stage | Name | Input | Output | Completion Signal |
|------|------|------|------|----------|
| 0 | Synopsis extraction | Raw text | 概要.md (**initial 200-character thin first pass** + chapter index; Stage 5 overwrites it with a plot-aware 500–1,000-character version) + **the Stage 0 chapter-boundary substep writes its boundary table to `_progress.md`** (see below) | Chapter structure identified + boundaries saved |
| 1 | Golden first three chapters | First three chapters | 第1章_深度拆解.md / 第2章_深度拆解.md / 第3章_深度拆解.md (one file per chapter). If a nonhuman antagonist (an abstract opposition such as aura resurgence/post-apocalypse/national-fortune systems) appears in the first three chapters, analyze it here using the abstract-opposition route (central opposition / source of urgency / escalation mechanism / narrative substitute). | Three chapters decomposed → **stop and produce 快速预览.md** |
| 2 | Chapter summaries | Chunked chapter text | 章节摘要.md (plot points + characters + **key information and expansion techniques** + **chapter-specific writing formula**). Each formula must extract emotional direction, pacing ratio, structural formula, core techniques, end-of-chapter pressure point, and foreshadowing. Filter characters (exclude walk-ons, normalize aliases). Extract 10–40 plot points per chapter (one per 150–200 characters, adjusted dynamically; even when a formula yields fewer than 10, meet the hard minimum of 10 by fully decomposing key steps). **Parallel mode: spawn one chapter-extractor agent per chapter**. **Count validation: summary count == chapter count; otherwise mark failed chapters**. | All chapters processed |
| 3 | Aggregate analysis | All chapter summaries | 剧情/*.md + README.md (authority table + **plot-unit inventory** index) + 故事线.md + **节奏.md + 情绪模块.md**. **Identify story framework** first to choose aggregation strategy. **Two-step plot aggregation**: identify the plot outline from summaries, then assign plot points to it. Build a **key-information progression index** tracking how information expands by chapter/plot unit. Analyze **emotional touchpoints and release pacing** (setup → release → aftermath for payoff/pain/anticipation beats). Produce a **whole-book emotional-pacing overview** (emotional curve, payoff frequency, small/medium/large climax positions, conflict-escalation route, cross-chapter foreshadowing map, and small/medium/large cycle units). Extract **reader needs / emotional engines / power-fantasy trope framework** into reproducible module cards. **Merge characters** across chapters and normalize aliases. **Tier characters** as protagonist/antagonist/core supporting/functional. Apply the **loose-plot fallback** (six steps including coverage validation). Add **set-piece tags** to each plot module using the vocabulary in deconstruction-notes.md, best-effort; leave blank when none match. Run **quality checks** using thresholds in material-decomposition.md. | Quality checks pass |
| 4 | Setting + relationships (4a/4b/4c) | **4a**: Stage 2 plot points + chapter summaries (independent of Stage 3; may run in parallel); **4b/4c**: merged Stage 3 character data + plot points | 设定/*.md + 角色/*.md. **4a setting** (worldbuilding/special advantage/factions, inferred from Stage 2 mention data). **4b complete character dossiers** (two-stage model: lightweight Stage 2 mentions → full Stage 4b dossier; automatically merge aliases at confidence ≥0.85). **4c relationship extraction** (from plot points, not source text; includes evolution tracking + final-state merge + implicit inference). Analyze nonhuman antagonists fully as abstract opposition in 4a. | 4a/4b/4c all complete |
| 5 | Consolidated report | All output | 拆文报告.md, including summaries of “reader needs / emotional engines,” “key information and expansion techniques,” “whole-book emotional pacing,” “pacing and emotional touchpoints,” “cycle units,” “cross-chapter foreshadowing map,” “conflict-escalation path,” and “reproducible modules,” with links to `剧情/节奏.md` / `剧情/情绪模块.md`. Include a “writing techniques” list covering dual-purpose details/delayed revelation/viewpoint deception/contrast anchors/behavior loops/physical reactions instead of stated psychology/**cross-chapter callbacks**—objects or images serving different functions in different chapters. Also generate the **500–1,000-character whole-book version of 概要.md**, plot-aware and overwriting the 200-character Stage 0 thin pass. | Report + whole-book synopsis complete |
| 6 | Prose style | 拆文报告.md + 章节/第1-3章_深度拆解.md + 章节/*_摘要.md + 原文/原文.txt | 文风.md (whole-book writing-technique view: sentence length/punctuation/dialogue subtext/emotional alternation cycle + 4–6 source-anchored example passages + layered imitation guidance, hard limit ~4,000 Chinese characters. See [style-profile-protocol.md](references/style-profile-protocol.md) + [style-profile-generator.md](references/style-profile-generator.md)) | Style saved to `拆文库/{书名}/文风.md` |

### Stage 0 Chapter-Boundary Substep

After Stage 0 produces the synopsis + chapter index and before entering Stage 1, **write an additional “chapter boundaries” table into `_progress.md`**. This is the **single shared slicing source** for Stage 1 (golden-three source slices), Stage 2 (each chapter passed to chapter-extractor), and Stage 6 (style sampling). Do not run separate regex slicing in each Stage, which can produce inconsistent results.

Procedure:
- Use the chapter regex from Step 4 of `style-profile-generator.md` (including 千/两 and 1,000+ chapters) to grep all chapter line numbers
- **Remove the table of contents first**: Many source files begin with a contents block whose line-leading `第N章` entries duplicate body chapter headings. If untreated, this produces two “Chapter 1” slices. Detect it by line spacing: adjacent matches in the contents are only one or two lines apart, whereas body chapters are separated by a full chapter. Calculate line-number differences between adjacent matches and discard the initial continuous block whose spacing remains far below the overall median.
- **If chapter numbers still repeat after removal, do not choose one yourself**: Multi-volume works may legitimately restart at “第一章” in every volume. Preserve the volume number in the title column for disambiguation (for example, `卷二 第一章`) and renumber the chapter-number column sequentially across the book.
- Write four columns, `| 章号 | 标题 | 起始行 | 字数 |`, into the “章节边界” section of `_progress.md` (see the template in [pipeline-ops.md](references/pipeline-ops.md)).
- Before saving, validate that chapter numbers are contiguous, unique, and have no gaps. If not, stop and report it rather than entering Stage 1 with a bad table. Stages 1/2/6 all treat this table as the slicing source of truth; one error propagates through the pipeline.
- Also write `schema_version: 2` at the top of `_progress.md`.

**Recovery prerequisite**: Resume only from an `_progress.md` with `schema_version: 2` and a complete “章节边界” table. If either is missing or malformed, stop and instruct the user to rebuild the progress file from the Stage 0 boundary substep so different Stages never use different slicing sources.

### Stage 1 Stop

After Stages 0+1, the pipeline **automatically pauses**, produces a quick-preview report, and asks whether to continue the full decomposition:

1. **Create the checkpoint deliverable**: Write `拆文库/{书名}/快速预览.md` using “Quick Preview Report” in [output-templates.md](references/output-templates.md). At this point `概要.md`, `章节/第1章_深度拆解.md`, `章节/第2章_深度拆解.md`, `章节/第3章_深度拆解.md`, and `原文/` are all saved.
2. **Write checkpoint state**: Set “最终状态” in `_progress.md` to `paused_after_stage1`; in “断点,” record “下一操作：Stage 2 逐章摘要”.
3. **Ask the user** with an explicit two-choice AskUserQuestion:
   > “The golden first three chapters are complete; see `快速预览.md` for the quick-preview report. Continue the full decomposition (Stages 2–6: chapter summaries / aggregate analysis including `剧情/节奏.md` and `剧情/情绪模块.md` / setting and relationships / consolidated report / prose style)? Estimated time: {rough estimate based on chapter count}.”
   - Choose “continue full decomposition” → read `_progress.md` and resume from **Stage 2** without rerunning Stages 0/1.
   - Choose “stop here” → end the pipeline with `_progress.md` still set to `paused_after_stage1`, and tell the user: “Run `/story-long-analyze` on the same book at any time to resume automatically from Stage 2.”
4. **Skip the question when**: If the user initially says “complete decomposition / all at once / systematic decomposition / don’t ask,” still generate `快速预览.md` as the early-analysis snapshot, but continue directly through Stage 6 without pausing.

### After Stage 5: Backfill Topic Decisions (Optional)

Run after `拆文报告.md` is produced at the end of Stage 5. This is independent of Stage 6; a Stage 6 failure does not affect it.

First locate `选题决策.md`: use the project-root copy if present. Otherwise, search by filename from the project root and its parent, no deeper than three levels, skipping hidden directories; take the three most recently modified candidates. Backfilling writes a file, so obtain confirmation before writing outside the project root: if one candidate is found, report its path and ask, “Backfill this book’s decomposition evidence into this file?” If multiple are found, use AskUserQuestion to list candidates (path + `扫榜日期` + “do not backfill any”). If the user does not choose, record “not backfilled,” skip, and change nothing.

**Only when** `选题决策.md` is located (project-root copy directly, or an external copy confirmed above), match this book’s genre against the recommended topics:
- Exactly one match → Change that topic’s “reason it can break out” from `待拆文验证` to sourced support: “Evidence from this book’s decomposition: {reader needs/emotional engine from `拆文报告.md` + top reproducible modules from `剧情/情绪模块.md` + payoff/touchpoint pacing summary from `剧情/节奏.md`} (`拆文库/{书名}/拆文报告.md`, `剧情/情绪模块.md`, `剧情/节奏.md`).” This remains a hypothesis—decomposing one book does not prove it.
- Multiple or uncertain matches → Ask which direction in the topic decision corresponds to 《{书名}》.
- No matches → Record “no matching topic; not backfilled” and do not edit.
- If `选题决策.md` lacks the currently required “能爆的原因” field → report `invalid_topic_decision_contract`, instruct the user to rerun `story-long-scan` Phase 5 to generate a current file, and do not guess or silently backfill. The main decomposition may still complete.
- Repeated decompositions do not overwrite: backfill only values still marked `待拆文验证`; leave completed entries unchanged.

If no `选题决策.md` exists in the workspace, skip this step without affecting decomposition.

### Stage 6 Prose Style

`文风.md` covers expression-level style only. Emotional and pacing intent remains authoritative in `剧情/情绪模块.md` and `剧情/节奏.md`.
If source text is missing or chapter separators cannot be identified, write `文风可用：否：{原因}` under “生成记录” in `文风.md`. A Stage 6 failure does not block the pipeline.

### Parallel Execution of Stages 3–4

**Parallel execution graph**:
```
Stage 3（剧情聚合 + 角色合并）       ──┐
                                       ├── 4a 与 Stage 3 可并行
Stage 4a（设定：世界观/金手指/势力）  ──┘
              │
              ▼（Stage 3 + 4a 都完成后）
Stage 4b（角色完整档案）— 串行，依赖 Stage 3 合并后的角色实体
              │
              ▼
Stage 4c（角色关系提取）— 串行，依赖 4b 角色实体存在
```

4a uses Stage 2 summaries and can run alongside Stage 3. 4b/4c depend on Stage 3’s merged character entities and must run serially.

### Partial-Failure Tolerance

A failed chapter or Stage does not block the pipeline. Record failures in the “失败记录” table in `_progress.md` (`| 类型 | 章节/阶段 | 错误信息 | 重试状态 |`). Final status may be `completed_with_errors`; include failure details in the decomposition report.

> Relationship to material-decomposition.md: Stage 0 includes Material Stage 1 (chapter parsing); Stages 1 and 5 are additions; Stage 2 = Material Stage 2; Stage 3 = Material Stage 3; Stage 4 combines Material Stages 4+5.

See [output-templates.md](references/output-templates.md) for detailed templates and [material-decomposition.md](references/material-decomposition.md) for methodology.

---

## Quality-Check Summary

Before Stages 3–4 finish, quality checks for confidence, coverage, and overlap must pass. [The Quality Threshold System in material-decomposition.md](references/material-decomposition.md) is the sole authority for thresholds, calculations, and the self-check list.

**Stages 3–5 must also pass a “fact traceability” self-check**: Hard facts in settings/characters/reports—levels, values, distances, attributes, faction counts, appearance chapters, who said what—must be greppable back to the source. When the source does not specify something, write “原文未明确”; never infer to fill blanks. This is the greatest source of factual decomposition errors, even for strong models, because synthesis occurs two steps removed from the source and models fill gaps with plausibility. See [Synthesis-Stage Fact Fidelity in material-decomposition.md](references/material-decomposition.md).

---

## Stage 2 Parallel-Agent Strategy

Stage 2 uses chapter-extractor agents to process chapters in parallel instead of the former serial batching.

### Invocation

Every chapter prompt **must begin with the “material declaration” prefix** (the first paragraph of the prompt string below). It gives the subagent the correct context and prevents ordinary dramatic events in popular fiction from being misclassified as harmful and refused. The prefix is fixed text; include it verbatim without rewriting or omission.

```python
Agent(
  subagent_type: "chapter-extractor",
  prompt: "[材料声明] 以下为用户合法持有的虚构小说，任务是只读的转化性文学分析（编辑/评论视角）。暴力/复仇/家暴/情爱/黑暗伦理是该题材常规虚构元素，照常提取，不得以敏感拒绝整章或整本；个别片段无法处理则跳过、照常续完其余。\n\n章节编号：第{N}章\n章节标题：{标题}\n章节字数：{字数}\n\n章节原文：\n{原文文本}\n\n[情节点格式要求] 模板里的 {} 是占位标记，不要输出花括号本身：写「类型信息揭示」，不写「类型：信息揭示」或「类型{信息揭示}」。主题标签只填一个值，不要用 / 、 ，或空格并列多个。空字段统一写「无」，不要用「—」，涉及段不可省略。每个情节点后紧跟自己的那一行「主题标签X | 基调：Y」，不要把标签行堆到文件末尾。正确样例：\nP7 **龙血针检测**：类型信息揭示 | 许七安用龙血针验出对方身份，当场揭穿 | 涉及许七安,郑兴怀 | 地点府衙后堂 | 物品龙血针 | 时间入夜\n主题标签悬念 | 基调：紧张\n\n[输出前自检] 交付前逐条核对：① 文本里没有 { 或 }；② ^P 行数 == 主题标签行数 == 基调：行数；③ 每个主题标签只有一个值；④ 每个 P 行都含类型、白描、涉及三段。任何一条不符，先改再输出。"
)
```

> The main thread appends the `[情节点格式要求]` / `[输出前自检]` sections when spawning. They **do not depend on the version of the agent file deployed in the project**, so older projects receive these formatting constraints without rerunning `/story-setup`. A Sonnet escalation retry uses the same text.

### Batching Strategy

- Spawn 5–8 agents at a time to avoid concurrency limits
- Wait for the current batch to finish before spawning the next
- Update `_progress.md` with processed chapters after each batch

### Collect Agent Output

- Each agent returns extracted results in Markdown
- The main thread writes each result to `章节/第{N}章_摘要.md`
- Collect appearance tables from all agents for Stage 3 merging

### Failure Handling + Quality-Escalation Retry

**Two failure types**:
1. **Execution failure** (agent crash / timeout / empty output) → retry once with the same model (Haiku)
2. **Quality failure** (after saving, any of the 12 checks in chapter-extractor.md “Quality Check” fail—for example: fewer than 10 plot points, a P line without direct description, an overview written as itemized notes or one long “because…therefore…” chain, out-of-enum type/tone/theme tags, missing full-width colon in `基调：`, or names given as nicknames/generic labels) → **escalate once to Sonnet**

**Mechanically verifiable hard checks** (the main thread runs these directly after saving; any match is a quality failure regardless of the agent’s self-report):
- Plot-point count `N = grep -cE '^P[0-9]+ '`; `grep -c '基调：'` must equal N. Fewer means a plot point omitted `基调：` or its full-width colon; downstream Stage 6 style sampling greps the full-width `基调：` and would silently miss the chapter.
- Direct-description content: `grep -cE '^P[0-9]+ [^|]+\|[^|]*[^|[:space:]][^|]*\|[^|]*涉及'` must equal N. There must be two `|` marks before `涉及`, so the type and direct-description fields each occupy a segment, and the latter is not blank. Fewer means a plot point lacks direct description or uses the wrong field order/separator. Direct description is the principal evidence now that quotations are selective.
- Unique values from `grep -hoE '基调：[^ |]+'` must be a subset of {紧张, 轻松, 悲伤, 热血, 爽, 甜, 温馨, 恐怖, 压抑, 其他}
- Unique values from `grep -hoE '主题标签[：]?[^ |]+'`, after removing the `主题标签`/colon prefix, must be a subset of {爱情, 亲情, 友情, 权力, 金钱, 成长, 复仇, 悬念, 搞笑, 热血, 日常, 其他}. A colon in `主题标签：` or a tone word used as the value is a failure.

> **Those four items are the complete hard-check set; there are no others.** Prevent format drift through the constraints in the spawn prompt and agent template, **not by adding more post hoc validation**. Variants such as leftover braces, tag-line placement, or empty-field markers affect readability only and have no downstream consumer (Stage 6 only greps `基调：`). **Existing `章节/*_摘要.md` files do not become “invalid” because of this updated formatting explanation and need not be regenerated**. Legacy forms such as `类型{行动}` and `物品—` remain usable; Stages 3–6 read them as before.

**Escalation retry** (run after validation failure):

```python
Agent(
  subagent_type: "chapter-extractor",
  model: "sonnet",            # 显式覆盖 frontmatter 的 haiku
  prompt: "章节编号：第{N}章\n...（同首次 prompt，含开头的「材料声明」前缀，可追加：'上次校验失败原因：{自检失败项}'）"
)
```

**Final save rules**:
- Haiku passes first attempt → write `章节/第{N}章_摘要.md`; mark `success` in `_progress.md`
- Haiku fails + same-model retry passes → same, with `retry_same_model`
- Quality failure + Sonnet retry passes → same, with `retry_sonnet`
- Sonnet retry still fails → mark chapter `⚠️ 跳过`, record the reason in the “失败记录” table in `_progress.md`, and mention it in the decomposition report
- A single chapter failure does not block the pipeline; decide whether to enter Stage 3 only after all agents in the batch finish

### Fallback When Agents Are Unavailable

If either condition below applies, Stage 2 automatically falls back to serial processing in the main thread. Quality remains the same; only execution becomes serial and somewhat slower. **Both paths share the same requirements**: in serial mode, overview style, plot-point direct description, selective source quotations, and output self-checks follow “Stage 2 Chapter Summary + Plot Points” in [output-templates.md](references/output-templates.md). Run the same mechanical hard checks above. Serial mode has no Sonnet escalation path; on a hard-check failure, the main thread rewrites that chapter summary once according to the failed item. If it still fails, record `⚠️ 跳过` in the “失败记录” table in `_progress.md`.

- **Agent not deployed**: No `chapter-extractor.md` or matching Codex TOML exists in the current runtime’s canonical agent directory. Project agents are not normally bundled with the writing repository; rerun `/story-setup` to deploy the current adapter. Do not read template sources across Skills.
- **Environment cannot spawn subagents**: This skill is already running inside a subagent and cannot create another nested layer.

### End of Stage 2: Merge Chapter Summaries (_章节摘要汇总.md)

After all `章节/*_摘要.md` files are saved and before Stage 3, the main thread **losslessly concatenates** them in chapter order into `拆文库/{书名}/_章节摘要汇总.md` without compression or rewriting:

```bash
ls 章节/*_摘要.md | sed -E 's/.*第([0-9]+)章.*/\1 &/' | sort -n | cut -d' ' -f2- | while read -r f; do cat "$f"; echo; done > _章节摘要汇总.md
```

**Lossless checks** (if either fails, delete `_章节摘要汇总.md` and fall back to scanning individual files as before):
- `grep -cE '^P[0-9]+ ' _章节摘要汇总.md` == sum of `^P` lines across summaries
- `grep -cE '^\*\*概要\*\*' _章节摘要汇总.md` == summary-file count. Each chapter has one `**概要**` line in both parallel chapter-extractor output and the serial summary template. Do not use a `## 第N章` heading because the serial template lacks one and would be miscounted.

Stage 3 / 4a / 4c / loose-plot fallback should **read `_章节摘要汇总.md` once** and reuse it in context instead of repeatedly running `glob 章节/*_摘要.md` in every Stage, reducing 4–5 cold reads of the same corpus to one.

**Generate the merged file only when the corpus fits in context**. For more than 500 chapters, or when `_章节摘要汇总.md` is too large for context, **skip this step** and use “Processing Batches → A. Parallel Subagent Mode” in [material-decomposition.md](references/material-decomposition.md): spawn subagents for 10–20 chapters per batch; each reads its summaries in its own context and returns only a ≤8K-token reduced aggregate. The main thread merges only these aggregates, using hierarchical pairwise merging if needed. **The main thread must not read raw summaries chapter by chapter**—skipping the merged file does not mean returning to per-file scanning, which also will not fit for a large book. `_章节摘要汇总.md` does not replace `章节/*_摘要.md`; single-chapter files remain the persisted source of truth and are used by Stage 6 style sampling and human review. Delete `_章节摘要汇总.md` after Stage 6; it is a derived temporary file and is not delivered with `拆文库/` (which story-import preserves as part of the writing project).

See [material-decomposition.md](references/material-decomposition.md) for authoritative Stage 3–5 chunking rules.

---

## Recovery

At startup, check _progress.md. If it says `paused_after_stage1`, resume directly from Stage 2.
See [pipeline-ops.md](references/pipeline-ops.md) for the procedure.

---

## Workflow Handoff

**Pipeline:** Long-form
**Position:** Decomposition (Step 2 in the long-form pipeline, after story-long-scan and before story-long-write)

| When | Go To | Command |
|---|---|---|
| Ready to begin writing | story-long-write | `/story-long-write` |
| Need market data | story-long-scan | `/story-long-scan` |
| Better suited to short-form | story-short-scan → story-short-analyze | `/story-short-scan` |

---

## References

| File | When to Load |
|------|----------|
| [references/output-templates.md](references/output-templates.md) | Entire pipeline: Stage output templates + quick-preview report + `剧情/节奏.md` / `剧情/情绪模块.md` templates + general quick-reference tables |
| [references/material-decomposition.md](references/material-decomposition.md) | Stages 2–5: decomposition methodology + quality thresholds + chunking strategy; see separate prose-style references for Stage 6 |
| [references/pipeline-ops.md](references/pipeline-ops.md) | Pipeline operations: _progress.md template, error handling, and recovery steps |
| [references/deconstruction-notes.md](references/deconstruction-notes.md) | Book/film/abstract decomposition methods + genre-specific applications |
| [references/style-profile-protocol.md](references/style-profile-protocol.md) | Stage 6: prose-style template + reliability/usability notes |
| [references/style-profile-generator.md](references/style-profile-generator.md) | Stage 6: six-step style-generation SOP, including Chinese-numeral chapter recognition + full-width-colon tone grep |

---

## Language

- Reply in the user’s language
- Chinese responses must follow the Chinese Copywriting Style Guide
