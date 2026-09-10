# Structure Migration Mapping Rules (Long-Form)

Detailed mapping rules and templates for Phase 3-L long-form structure migration. Convert analysis results from `拆文库/{导入书名}/` into the long-form project structure under `{导入书名}/`.

> For short-form migration rules, see `structure-mapping-short.md`.

> **Naming boundary**: `{导入书名}` is the user's own novel to be continued; `{对标书名}` is a separately selected external reference work. Their data sources must remain separate. Never write analysis results for `{导入书名}` or the project's `设定/` data into `对标/`.

---

## Mapping Overview

| Deconstruction-Library Path | Project Path | Conversion Method |
|-----------|---------|---------|
| `原文/` | `正文/第XXX章_章名.md` | Split by chapter and standardize filenames |
| `快速预览.md` | — | Use as a reference for proposed volume divisions and plot direction; do not migrate directly |
| `角色/{角色名}.md` | `设定/角色/{角色名}.md` | Add character-template fields |
| `角色/角色关系.md` | `设定/关系.md` | Convert the format |
| `设定/世界观/*.md` | `设定/世界观/*.md` | Synchronize unchanged by topic |
| `设定/势力/*.md` | `设定/势力/*.md` | Synchronize unchanged by faction |
| `剧情/故事线.md` | `大纲/大纲.md` | Reverse-engineer the volume-level structure (user must confirm volume divisions; see below) |
| `剧情/{标题}.md` | `大纲/卷纲_第X卷.md` | Aggregate into volume outlines |
| `剧情/节奏.md` | `设定/题材定位.md` (pacing summary) | Distill the established pacing of the written portion and retain it as the import baseline for this book; do not copy it into `对标/` |
| `剧情/情绪模块.md` | `设定/题材定位.md` (emotion summary) | Distill the written portion's reader needs and emotional engine; do not copy it into `对标/` |
| `章节/第N章_摘要.md` | `大纲/细纲_第N章.md` | Reverse-engineer detailed chapter outlines |
| — | `设定/题材定位.md` | Generate from the deconstruction report |
| — | `追踪/_tracking-state.json.imported_through_chapter` | Record the final imported chapter N; do not fabricate daily-writing records for Chapters 1..N |
| — | `追踪/伏笔.md` | Keep exactly one current-status row for each genuinely planted/resolved foreshadowing ID |
| — | `追踪/_tracking-state.json.timeline` | Record objective fact, reader understanding, and actual reveal state for each event; the Markdown timeline is only a derived reading view |
| — | `追踪/时间线/作者真相.md`, `读者已知.md` | Derive from `_tracking-state.json.timeline`; the reader view must never expose author-only secrets |
| — | `追踪/角色状态/{角色名}.md` | Reverse-engineer the current snapshot for each central character using `character-state-reverse.md` |
| — | `追踪/逐章记录/` | Create an empty directory; do not fabricate daily-writing records for imported chapters, and begin generating them with Chapter N+1 |
| `剧情/散落情节.md` | Appendix in `大纲/大纲.md` or the relevant volume outline | Merge into the outline for the relevant volume |
| — | `追踪/上下文.md` | Generate a continuation status card through the initialization transaction (exactly seven sections), ≤12,288 bytes |

---

## Manuscript Standardization Rules

### Naming Format

Source filename → standard format: `第{零填充三位}章_{章名}.md`

| Source Filename | Standardized Filename |
|---------|---------|
| 第一章_初入江湖.txt | 第001章_初入江湖.md |
| 第1章.md | 第001章_无题.md |
| chapter01.md | 第001章_无题.md |
| 01_觉醒.md | 第001章_觉醒.md |

### Recognizing Chapter Separators

When the source is a single large file, split it using the following separators (the same recognition table used by priority 2 in `length-routing.md`):

| Separator Pattern | Example |
|-----------|------|
| `第X章` / `第X章 ` / `第X章：` / `第X章 XXX` | 第1章 初入江湖 |
| `Chapter X` | Chapter 1 |
| Number only + title | 1. 觉醒 |

### Content Handling

- Preserve source text exactly; do not modify it
- Standardize encoding as UTF-8
- Remove unrelated material from the beginning and end of the file (such as advertisements and notices)

---

## Character-File Migration Template

```markdown
---
name: {角色名}
---

# {角色名}

## 基本信息
- 身份：{从拆文库角色文件提取}
- 核心特质：{}
- 当前能力：{}
- 核心动机：{}
- 弱点/缺陷：{}

## 外在表现
{身份/言行/外貌}

## 内在分析
{性格/目标/秘密}

## 出场记录
| 章节 | 关键事件 | 状态变化 |
|------|---------|---------|
| 第{N}章 | {事件} | {变化} |

## 别名
{如有别名，列出}
```

---

## Relationship-File Conversion Rules

Deconstruction-library format (角色关系.md) → project format (设定/关系.md):

```
拆文库格式：
A<->B：关系类型 | 情感 | 描述（50-200字）| 演变轨迹

项目格式：
| 角色 A | 角色 B | 关系类型 | 情感倾向 | 当前状态 | 起始章节 | 变化节点 |
```

Conversion rules:
- Relationship-type mapping: family→familial bond, lovers→romance, friends→friendship, etc.
- Reuse emotional orientation directly: positive/negative/neutral/complex
- Extract the relationship trajectory into the “change beats” column

### Target-Format Template (设定/关系.md)

```markdown
# 角色关系图

## 关系总览

| 角色 A | 角色 B | 关系类型{亲情/爱情/友情/敌对/师生/主从/利益} | 情感倾向{正面/负面/中性/复杂} | 当前状态 | 起始章节 | 变化节点 |
|--------|--------|---------------------------------------------|-----------------------------|---------|---------|---------|
| {名} | {名} | {类型} | {倾向} | {描述} | 第{N}章 | {事件} |

## 关系演变

{角色A}<->{角色B}：
- 起点：{初始关系}
- 转折：{章节·事件·变化}
- 当前：{现状}

## 核心冲突关系

{列出推动剧情的2-3对核心对立/合作关系}
```

---

## Worldbuilding Synchronization Rules

The current `story-long-analyze` output already uses topic-based directories. The import stage performs a pass-through only and no longer parses or splits a flat `世界观.md`.

| Source Path | Target Path | Current Contract |
|---------|---------|---------|
| `拆文库/{导入书名}/设定/世界观/*.md` | `{项目}/设定/世界观/*.md` | Synchronize unchanged; `背景设定.md` must exist |
| `拆文库/{导入书名}/设定/势力/*.md` | `{项目}/设定/势力/*.md` | Synchronize already-separated faction files unchanged |

When `力量体系.md`, `地理.md`, or minor-faction material contains fewer than 200 Chinese characters, the upstream process merges it into `背景设定.md`, so those standalone files may be omitted. If `背景设定.md` is absent, or if the current content points to an independent power system but its corresponding file was not produced, stop the import and instruct the user to rerun Stage 4 of `story-long-analyze`.

---

## Reverse-Engineering Outline Rules

### 大纲.md (Volume-Level Structure) and Volume-Division Rules

Reverse-engineer it from `剧情/故事线.md`, `剧情/*.md`, and `快速预览.md`. **Volume divisions must follow these decision rules**:

**Case A: The source has explicit volume boundaries**

The source contains explicit volume-level markers (such as “第一卷 XXXX,” “卷一,” or other chapter-level headings) → follow the source's volume boundaries directly without asking the user.

**Case B: The source has no explicit volume boundaries**

Do not divide it mechanically. Follow this process:

1. Detect proposed volume boundaries based on story threads, setting changes, and major time jumps (see “Proposed-Boundary Detection Reference” below);
2. Show the user a proposed division in this format:

   ```
   候选卷划分（供参考，非定论）：
   - 候选卷一：第 1-18 章（世界观建立 + 初步成长，场景：城郊学院）
   - 候选卷二：第 19-45 章（主线冲突爆发，场景：帝都议事堂）
   - 候选卷三：第 46-XX 章（最终对决，场景切换：上古遗迹）
   以上为故事线/场景切换自动检测结果，请确认或调整。
   ```

3. **Wait for the user to confirm the volume divisions** before generating the volume-level structure in `大纲/大纲.md` and the corresponding `大纲/卷纲_第X卷.md` files;
4. Before confirmation, record only the proposal in `大纲/大纲.md`; do not write finalized volume outlines.

> **Never** mechanically split a source without volume boundaries using a rule such as “20–40 chapters per volume by default.” Proposals are references only; the user makes the final decision.

### Proposed-Boundary Detection Reference

| Signal Type | Example | Likelihood of a Volume Boundary |
|---------|------|------------|
| Consecutive chapters + same story thread | Same city/same faction perspective | Same volume |
| Major setting change (new map/new faction) | Moving from the suburban academy into the imperial capital | Proposed start of a new volume |
| Major time jump (months/years) | “Three years later…” | Proposed start of a new volume |
| Major stage objective completed + new objective begins | Defeat a stage boss → a new crisis appears | Proposed start of a new volume |
| The story-thread summary already includes stage divisions | Sections within `剧情/故事线.md` | Prioritize as a reference |

### Reverse-Engineering the Volume Outline

#### Target-Format Template (大纲/卷纲_第X卷.md)

A volume outline expands the master outline—the master outline determines direction; the volume outline determines pacing. It contains the complete creative plan for the volume.

```markdown
# {卷名} 卷纲

## 核心信息
- 章节范围：第{X}-{Y}章
- 字数目标：{W}万字
- 本卷定位：{铺垫/发展/高潮/转折/收尾}

## 核心矛盾
{一句话：本卷要解决什么问题或达到什么目标}

## 情绪弧线
- 模板：{V形/倒V形/W形/渐进形/延迟满足形/急转弯形}
- 选择理由：{结合题材和本卷定位}

| 章节 | 情绪基调{紧张/轻松/悲伤/热血/温馨/震惊} | 强度{1-10} | 触发事件 |
|------|-----------------------------------------|-----------|---------|
| 第{N}章 | {基调} | {N} | {事件} |

## 卷契约与终局储备（反推）
- 卷契约：{从本卷剧情归纳读者期待与主角高光；证据不足写 `[待补充]`}
- 本卷主推线：{从情节点归纳承担本卷最大高潮的线}
- 本卷战果：{其余顺带兑现的线；证据不足写 `[待补充]`}
- 本卷解锁的终局里程碑：`[待补充]`
- 本卷禁碰的终局底牌：`[待补充]`
- 契约风险：{契约安全 / 需补强 / 契约破坏；无法判断写 `[待补充]`}

## 剧情单元（反推）
| 单元ID | 章节范围 | 单元节拍（铺垫→释放→反应层→衔接） | 主推线/战果 | 下一单元因果钩子 |
|------|---------|---------|-------|---------|
| L{卷}-1 | {章X-Y} | {从爽点/情节点分布归纳} | {线} | {方式} |

（导入反推只填有证据的字段，未知写 `[待补充]`、不杜撰；后续补纲/改纲时按 story-long-write 技能的「剧情单元卡」完整字段模板升级。）

## 人物弧线
| 角色 | 本卷起点 | 本卷终点 | 关键转变 |
|------|---------|---------|---------|
| {名} | {状态} | {状态} | {事件} |

## 本卷反转（如有）
| 类型{身份/动机/阵营/信息/命运} | 涉及角色 | 误导路径 | 揭示章节 | 影响范围 |
|------|---------|---------|---------|---------|
| {类型} | {名} | {如何误导读者} | 第{N}章 | {影响哪些线} |

## 本卷伏笔
| 伏笔 | 埋设章节 | 预计回收 | 类型{短期/中期/长期} |
|------|---------|---------|---------------------|
```

#### Field Mapping

Extract the following for each volume from the plot files:
- Central conflict → central-conflict field
- Distribution of plot beats → emotional arc + plot units (reverse-engineered)
- Character appearances → character arcs
- Setup-type plot beats → foreshadowing

### Reverse-Engineering Detailed Chapter Outlines

Extract from each chapter summary (`章节/第N章_摘要.md`):

| Summary Field | Detailed-Outline Field | Conversion Method |
|---------|---------|---------|
| Key events | Central event | Reuse directly |
| Chapter length | Target length + counting method | Run `storyctl.py wordcount measure` on the source chapter and write `actual` and `visible_chars_v1` |
| Chapter tone / emotional curve | Target emotion | Extract from the summary; if absent, write `[待补充]` |
| First plot beat | Opening hook | Use only as evidence; mark the design target `[待补充]` |
| Satisfaction-type plot beats | Satisfying payoff | Infer from plot-beat type; if none, write “No explicit satisfying payoff / [待补充]” |
| Setup-development-turn-climax-resolution of plot beats | Content summary (cause/development/turn/climax/ending) | Summarize in plot-beat order; if evidence is insufficient, write `[待补充]` |
| Main/sub/task clues | Plot arrangement (main thread/supporting thread/event thread/romance thread/logic thread) | Reverse-engineer from the plot-unit index and summary; for supporting/romance threads without evidence, write “none” or `[待补充]`; never fabricate |
| Appearing characters / key objects | Character relationships and order of appearance | List in summary order; record a relationship change as “before → after” only when supported by evidence; otherwise write `[待补充]` |
| All plot beats | Plot elaboration / plot-beat sequence | Write row by row (# / plot beat / function tag / execution boundary); if function or boundary is unclear, write `[待补充]`; do not infer per-beat word-count quotas |
| Victory/defeat/twist/gain or loss | Cost of action (optional)/ownership of gains | Fill only with explicit evidence; action cost may be absent and must not be invented; otherwise write `[待补充]` |
| Final plot beat / suspense-type plot beat | Ending design and hook | The resolved state may be summarized; mark the chapter-ending hook's design target `[待补充]` |

---

## Reverse-Engineering Character State

Reverse-engineer it using character-state-reverse.md; see that file for details.

---

## Foreshadowing Extraction Rules

Identify potential foreshadowing from plot beats:

### Recognition Patterns

| Plot-Beat Type | Likelihood of Foreshadowing | Extraction Method |
|-----------|-----------|---------|
| Setup | High | Extract directly as foreshadowing |
| Information reveal (partial) | Medium | Check for a later echo |
| First appearance of an object | Medium | Check whether it is later used |
| Character secret | High | Mark as character foreshadowing |
| Unresolved suspense | High | Extract from the chapter-ending marker |

### State Inference

- A setup beat has a later “reveal” or “resolution” beat → mark “resolved”
- A setup beat has no later echo → mark “planted”
- Setup in the final chapters of an unfinished novel → mark “planted” and note “near the cutoff”

---

## Timeline Extraction Rules

### Recognizing Time Markers

Extract from plot beats and time markers:

| Marker Pattern | Example | Extraction Method |
|---------|------|---------|
| Explicit date | "天元三年春" | Record directly |
| Relative time | "三日后", "半月后" | Calculate absolute time |
| Interval between events | "翌日", "次日" | Mark as consecutive |
| Seasonal marker | "入冬", "春暖花开" | Infer the season |

### Sorting Rules

Sort by chapter order and, within a chapter, by plot-beat number. When a time marker is absent, label it `[推断]`.

---

## Generating Genre Positioning

Extract the core findings from the deconstruction report to generate `设定/题材定位.md`.

### Target-Format Template (设定/题材定位.md)

```markdown
# 题材定位

## 基本信息
- 题材类型：{玄幻/都市/系统/...}
- 目标平台：{Phase 1 向用户采集的目标平台；无则从拆文报告提取，仍无填 [待补充]。story-review 据此选平台 rubric}
- 核心梗：{一句话卖点}
- 微创新点：{与同类题材的差异}

## 核心梗三分法
- 表层卖点：{读者一眼看到的吸引力}
- 深层爽点：{持续追读的情绪驱动力}
- 长线钩子：{支撑全书的悬念/目标}

## 读者需求 / 情绪引擎
> 本段从 `拆文库/{导入书名}/剧情/情绪模块.md` 提炼，只记录本书已写内容的续写基线，不把本书登记成对标。

| 读者需求 | 情绪缺口 | 满足方式 | 可复现模块 | 来源 |
|---------|---------|---------|------------|------|
| {安全感/优越感/期待感/情感补偿/认知反转/陪伴感} | {缺什么} | {如何被满足} | {EM-001 等} | `[导入分析] 剧情/情绪模块.md` |

## 节奏与触发参考
> 本段从 `拆文库/{导入书名}/剧情/节奏.md` 提炼，只记录已写部分的节奏事实。

| 节奏模块 | 关键信息推进 | 情绪触动点 | 爆发节奏 | 来源 |
|---------|-------------|------------|----------|------|
| {RH/TR 编号} | {信息如何被扩写} | {触发什么感受} | {铺垫→爆发→冷却} | `[导入分析] 剧情/节奏.md` |

<!-- 仅当用户显式绑定独立外部对标时生成以下两节；未绑定时整段省略。 -->
## 对标书清单（canonical registry，可选）
主对标书: {对标书名}  # 最多 1 本；必须是独立外部参考作品
对标书列表:
  - 书名: {对标书名}
    引用强度: 主  # 主 / 辅 / 参考
    题材类型: {玄幻/都市/系统/...}
    相关性: 同题材
    用途: 文风+核心结构
  - 书名: {书名 B}
    引用强度: 辅
    题材类型: {题材}
    相关性: 同题材/弱相关
    用途: {补设定/大纲/模块，不进文风}
  - 书名: {书名 C}
    引用强度: 参考
    题材类型: {题材}
    相关性: 同题材/弱相关
    用途: {仅按预算召回摘要}

## 对标分析（派生概要）
> 完整对标数据见 `对标/` 目录；上方 registry 是权威清单。本表仅做快速概览，不可替代 `主对标书` + `对标书列表`。

| 对标书 | 相似点 | 差异点 | 可借鉴 |
|--------|-------|-------|-------|
| {对标书名} | {点} | {点} | {点} |

## 题材框架
- 八节点位置：{当前处于哪个节点}
- 关键转折节点：{列出}
```

### Field Mapping

- Genre type, central premise, micro-innovation → extract from the basic-information and core-findings sections of `拆文报告.md`
- Three-part central premise → extract from the surface appeal, satisfaction design, and long-term suspense sections of `拆文报告.md`
- Reader needs / emotional engine → extract from `剧情/情绪模块.md`; if absent, stop the import and provide the corrective action for rerunning Stage 3+
- Pacing and trigger reference → extract from `剧情/节奏.md`; if absent, stop the import and never substitute `拆文报告.md`, chapter summaries, or `剧情/故事线.md`
- Comparable-title registry → record only an external work explicitly selected by the user and traceable to `拆文库/{对标书名}/`; omit it when none is bound and never substitute `{导入书名}`
- Comparable-title analysis (derived summary) → summarize only registered external comparables; the genre framework still comes from the imported analysis of this book, and the two source categories must never be conflated

---

## Comparable-Reference View Synchronization Rules

This section applies only to an external `{对标书名}` explicitly bound by the user: synchronize from `拆文库/{对标书名}/` into the project's `对标/{对标书名}/`. When none is bound, do not create a comparable-title subdirectory. Never copy `拆文库/{导入书名}/`, project `设定/`, or files generated from them into `对标/`.

| Source Path | Target Path | Synchronization Semantics |
|-------|---------|----------|
| `拆文库/{对标书名}/剧情/节奏.md` | `{项目}/对标/{对标书名}/剧情/节奏.md` | Required authoritative file for the daily-writing `rhythm_reference`; if absent, do not register this comparable title |
| `拆文库/{对标书名}/剧情/情绪模块.md` | `{项目}/对标/{对标书名}/剧情/情绪模块.md` | Required authoritative file for the daily-writing `selected_emotion_module`; if absent, do not register this comparable title |
| `拆文库/{对标书名}/剧情/*.md` | `{项目}/对标/{对标书名}/剧情/*.md` | Plot assets such as plot units, story threads, and scattered events; when they conflict with authoritative pacing/emotion files, the latter prevail |
| `拆文库/{对标书名}/章节/*.md` (第N章_摘要.md + Golden Three Chapters 第1-3章_深度拆解.md)| `{项目}/对标/{对标书名}/章节/*.md` | Evidence from matching chapters, including “key information and expansion techniques” |
| `拆文库/{对标书名}/角色/*.md` | `{项目}/对标/{对标书名}/角色/*.md` | References for character functions, relationships, and reaction layers |
| `拆文库/{对标书名}/设定/` | `{项目}/对标/{对标书名}/设定/` | Constraint references for worldbuilding, factions, special advantages, and related elements |
| `拆文库/{对标书名}/拆文报告.md` | `{项目}/对标/{对标书名}/拆文报告.md` | Human-readable summary projection |
| `拆文库/{对标书名}/文风.md` | `{项目}/对标/{对标书名}/文风.md` | Required reading for daily style retrieval |

Conflict rule: For registered external comparable titles, `对标/{对标书名}/剧情/情绪模块.md` and `对标/{对标书名}/剧情/节奏.md` are authoritative for comparable retrieval; `拆文报告.md` and `剧情/故事线.md` are summary projections only. If a summary conflicts, retain a conflict note and follow the authoritative file. If either authoritative file is missing, do not generate a partial comparable view; repair the deconstruction output for that external work first.

---

## Quality Checklist

Run after Phase 3-L migration:

- [ ] Number of manuscript files = number of source chapters
- [ ] Files exist for major characters (protagonist + central supporting characters)
- [ ] 关系.md is not empty
- [ ] 大纲.md contains a volume-level structure
- [ ] A detailed outline has been generated for every chapter
- [ ] `_tracking-state.json.imported_through_chapter` equals the final fully imported chapter
- [ ] Every ID has no more than one row in `追踪/伏笔.md`, and future designs not yet planted are excluded
- [ ] `_tracking-state.json.timeline` records key facts and reader understanding, and `读者已知.md` reveals no truth-only information
- [ ] `追踪/角色状态/{角色名}.md` covers every central character and aligns with `character-state-reverse.md`
- [ ] The empty 追踪/逐章记录/ directory exists, with no fabricated daily-writing records for imported chapters
- [ ] `追踪/上下文.md` has exactly seven top-level sections and is ≤12,288 bytes
- [ ] `tracking_commit.py check` passes, with `_tracking-state.json` consistent with every derived view
- [ ] Scattered plot events have been merged into the relevant volume outline or the master-outline appendix
- [ ] The user has confirmed the volume divisions (mandatory when the source has no explicit volume boundaries)
- [ ] `拆文库/{导入书名}/` was not copied to `对标/`, and the book was not registered as its own comparable
- [ ] If an external comparable is bound, the names and origins of `拆文库/{对标书名}/` and `对标/{对标书名}/` match and both primary artifacts were synchronized; otherwise, report the corrective action without rolling back the book project
