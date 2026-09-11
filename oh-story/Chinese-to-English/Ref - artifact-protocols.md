# Artifact-Creation Templates

Standard templates and creation guidance for every artifact. The agent loads this file as needed during the transition from Phase 2 to Phase 3.

**Template List:**

- `设定/关系.md`
- `设定/题材定位.md` (includes reader contract, endgame trump cards/progression ladder, and comparable-title registration fields)
- `大纲/大纲.md` (whole-book overview plus total length and stage overview)
- `大纲/卷纲_第X卷.md` (includes volume contract, endgame reserves, story units, emotional arc, and reversal plan)
- `追踪/_tracking-state.json` (sole structured authoritative state)
- `追踪/逐章记录/第NNN章.md` (compact future-relevant delta)
- `追踪/伏笔.md`
- `追踪/时间线/作者真相.md` + `读者已知.md` (derived views)
- `追踪/角色状态/{角色名}.md`
- `追踪/上下文.md` (continuation-state card with seven fixed sections)
- `对标/{对标书名}/拆文报告.md`
- `对标/{对标书名}/原文/第XXX章_{章名}.md`

**Hierarchy (book › volume › story unit › chapter › plot point; storylines run horizontally across multiple story units):**

- `大纲.md` = whole-book overview, positioning each volume in one or two sentences
- `卷纲_第X卷.md` = single-volume plan covering story units, emotion, characters, foreshadowing, and reversals
- `细纲_第XXX章.md` = chapter blueprint containing the unit ID/position, protagonist’s objective/critical choice, content summary, multi-line plot arrangement, relationships/appearance order, expanded plot points, and ending setup/hook

**Terminology Mapping (use these names consistently to reduce confusion):**

- **Story unit** = one complete movement of roughly 15,000–30,000 Chinese characters or several chapters, carrying one conflict from beginning to resolution. On the analysis side, it is `剧情/{剧情单元名}.md`; on the current-book side, it is a **story-unit card** in the volume outline. Theory may call it a “first-level structure.” These are the same level; always call it a story unit.
- **Storyline** (`剧情/故事线.md`) = a line crossing multiple story units, such as the main plot, romance arc, growth arc, or treasure-acquisition arc. It sits one level above a story unit.
- Use “cycle” only in its **rhythmic sense**, such as payoff cycles, progression cycles, or small/medium/large cycles. Do not use it for planning units.

---

## `对标/{对标书名}/拆文报告.md`

> **Analysis Library/Comparable-Title Relationship**: `拆文库/` contains the analyze skill’s raw outputs and serves as the data source. `对标/` is the writing project’s reference view. On first reference, copy the material from `拆文库/` to `对标/`.

This file is produced by the `story-long-analyze` analysis pipeline as either a quick-preview report or a complete analysis report. The write skill must **read** it, not create it.

If a simplified comparable-title summary must be created manually because the analyze skill was not used:

```markdown
# {对标书名} Comparable-Title Summary

## Basic Information
- Title: {}
- Author: {}
- Genre/Type: {}
- Target Platform: {}
- Performance: {Average Subscriptions/Active Readers/Popularity}

## Core Findings
- Opening Hook: {Type + Technique}
- Payoff Density: {Approximately Once per N Chinese Characters}
- Rhythm Pattern: {Description}
- Reusable Patterns:
  1. {}
  2. {}
  3. {}

## Not Recommended for Imitation (Do Not Copy)
- {} (Learn the structure only; do not copy the plot beat)
```

Creation reference: `plot-special-topics.md` (comparable-title selection rules)

---

## `对标/{对标书名}/原文/第XXX章_{章名}.md`

The original chapter from the comparable title, placed manually by the user or imported through the analysis pipeline.

```markdown
# Chapter {N}: {章名}

{Complete Original Chapter Text}

---
> Source: {Manual Input / Imported by story-long-analyze}
> Original Length: {Approximately N Chinese Characters}
```

---

## `设定/关系.md`

```markdown
# Character-Relationship Map

## Relationship Overview

| Character A | Character B | Relationship Type {Family/Romance/Friendship/Hostile/Mentor-Student/Master-Servant/Interest-Based} | Emotional Direction {Positive/Negative/Neutral/Complex} | Current Status | Starting Chapter | Change Point |
|--------|--------|---------------------------------------------|-----------------------------|---------|---------|---------|
| {名} | {名} | {类型} | {倾向} | {描述} | Chapter {N} | {事件} |

## Relationship Evolution

{角色A}<->{角色B}:
- Starting Point: {初始关系}
- Turning Point: {章节·事件·变化}
- Current: {现状}

## Core Conflict Relationships

{List Two or Three Core Adversarial or Cooperative Relationships Driving the Plot}
```

Creation reference: `character-relations.md` (relationship types and relationship-map creation)

---

## `设定/题材定位.md`

```markdown
# Genre Positioning

## Basic Information
- Genre Type: {Fantasy/Urban/System/...}
- Target Platform: {Qidian/Tomato Novel/Jinjiang/Other; story-review selects the platform rubric from this field}
- Central Hook: {One-Sentence Selling Point}
- Incremental Innovations: {Differences from Similar Works}

## Reader Contract (see `reader-contract-and-progression.md`)
- Core Reader Promise: {The payoff/emotion/relationship/career experience readers follow}
- Protagonist Agency Promise: {The protagonist’s irreplaceable judgment, critical choice, or contribution}
- Interest Safety Line: {Boundary preventing core assets/selling points from being confiscated, transferred, or exposed without exchange}
- Expectation Debt: {Promises established in the opening/current volume, when and how they will be repaid}
- Genre Boundary: {Individual rise/ensemble/mentor/institutional cooperation, etc.; verify before introducing high-level institutions}

## Endgame Trump Cards and Progression Ladder (prevents exhausting the story; fill once at project creation and consult during daily writing. See “Endgame Reserves and Progression Rhythm” in `reader-contract-and-progression.md`)
- Endgame Trump Cards (one-time resources; mark earliest unlock volume): Primary Archenemy={}·Volume {X}; Ultimate Truth/Origin={}·Volume {X}; Special-Advantage Limit={}·Volume {X}; Final Identity/Status={}·Volume {X}; Core Romantic Commitment={Delete if no main romance}·Volume {X}
- Progression Ladder: Main System {Realm/Level/Map/Faction Tier} has {N} tiers × approximately {W} ten-thousand Chinese characters per tier and should equal or exceed the whole-book target. If insufficient, lengthen the system or add maps. Unlock enemies/objectives in ascending tiers; never skip directly to the highest tier.
- Depletion Red Lines: ① Using an endgame trump card before its unlock volume ② A progression line approaches its ceiling with no later step available

## Three-Part Central Hook
- Surface Selling Point: {Immediate Attraction Readers See}
- Deep Payoff: {Emotional Driver of Continued Reading}
- Long-Term Hook: {Suspense/Objective Supporting the Whole Book}

## Comparable-Title Analysis (Summary)
> See the `对标/` directory for complete data. This table is only a quick overview.

| Comparable Title | Similarities | Differences | Reusable Elements |
|--------|-------|-------|-------|
| {书名} | {点} | {点} | {点} |

## Comparable-Title Registration (required for multiple titles; cross-book-recall uses this for sorting and budget)
- Primary Comparable Title: {书名; optional for one title, required for multiple titles}
- Comparable-Title List:

| Title | Genre Type | Reference Strength {Secondary/Reference} | Purpose |
|------|---------|-----------------|------|
| {书名} | {类型} | {辅/参考} | {Primary Style Comparable/Structural Reference/...} |

## Genre Framework
- Eight-Node Position: {Current Node}
- Critical Turning Points: {List}
```

Creation reference: `long-genre-mechanics.md` (central-hook analysis/application and incremental innovation/differentiation)

---

## `大纲/大纲.md`

Whole-book overview. Begin with “Total Book Length and Stage Overview”—total chapters, target length, whole-book emotional curve, stage divisions, each stage’s rhythm formula, critical nodes, and hook chain, structured according to [Phase 3: Outline Construction](workflow-setup.md#phase-3大纲搭建). Follow it with one-paragraph volume summaries:

```markdown
# Outline

## Total Book Length and Stage Overview
{Complete According to the “Total Book Length and Stage Overview” Structure in Phase 3}

## Volume-Level Outline
### Volume One: {卷名} (Approximately {X} Ten-Thousand Chinese Characters, {Y} Chapters)
- Function / Stage / Volume Contract / Endgame Reserves / Stage Boundary / Core Events / Starting State → Ending State
(One-paragraph summary; expand in each `卷纲_第X卷.md`)
```

---

## `大纲/卷纲_第X卷.md`

The volume outline expands the main outline: The main outline determines direction; the volume outline determines rhythm. It contains all creative planning for the volume.

```markdown
# {卷名} Volume Outline

## Core Information
- Chapter Range: Chapters {X}–{Y}
- Target Length: {W} Ten-Thousand Chinese Characters
- Volume Position: {Setup/Development/Climax/Turn/Conclusion}

## Volume Contract and Endgame Reserves (see `reader-contract-and-progression.md`)

> Allow flexibility at the chapter level while protecting endgame reserves at the macro level. Lines other than the primary progression line may receive natural results; one victory may produce several gains. The true constraint is that this volume must not spend endgame trump cards that should remain locked.
- Volume Contract: {Reader expectations, protagonist highlights, and primary expectation debts for this volume}
- Primary Progression Line: {One line carrying the volume’s largest climax: combat/resources/identity/relationships/information/map/institution/faction/career/romantic certainty}
- Volume Gains: {Results delivered by other lines, from a light touch to a major increase; multiple gains from one victory are allowed}
- Endgame Milestone Unlocked in This Volume: {Which major milestone from “Endgame Trump Cards and Progression Ladder” in `设定/题材定位.md` advances or unlocks here}
- Endgame Trump Cards Prohibited in This Volume: {Archenemy/truth/identity/special-advantage ceiling not yet unlocked}
- Contract Risk: {Contract Safe / Needs Reinforcement / Contract Violation; specify reinforcement when needed}

## Story-Unit Cards (15,000–30,000 Chinese characters is an adjustable rule of thumb; store inside the volume outline rather than separate files)

> A story unit is the first-level structural unit in the volume outline; see “Comparable-Title Rhythm Migration” in outline-structure-theory.md. It and the “Comparable-Title Structural Coordinates” below are different views of the same unit, not duplicate plans. Adjust unit length to the book’s genre, established payoff rhythm, and comparable titles; it is not a hard threshold. When planning critical nodes, apply the authoritative file’s Four Questions for Critical Nodes and expectation ownership. The protagonist need not personally perform every action. After a climax/payoff, a brief low-pressure period may use a small visible gain or reward to bridge into the next pressure cycle. Before introducing a new map, institution, ability, enemy, or mystery, check the book-change debt; novelty cannot evade old promises.

### Story Unit {L卷号-序号}
- Unit ID: {L卷号-序号}
- Chapter Range: {Chapters A–B}
- Comparable Plot Reference: {{书名} “Plot Title” (Type/Beat Tags; Borrowed Element: Structural Distribution/Plot-Point Index/Payoff Method); may list 2–3; write “None” without a comparable}
- Unit Beats/Chapter-Function Distribution: {Establish expectation → attempt → pressure/turn → decisive action → payoff → aftermath; mark chapter ranges and adapt by genre. When creating the card, derive shared beats from the referenced comparable story units; see “Creating Detailed Outlines by Plot” in outline-structure-theory.md}
- Unit Promise: {Emotional premise/expectation established for readers and the expectation debt to repay}
- Unit Emotion Engine: {Core emotional premise → carrier/emotional gap → reason it is blocked or persists → current trigger → protagonist’s irreplaceable ignition/transformation action → change in meaning or visible payoff → genre/contract payoff. Carrier may be a character, relationship, objective, rule, or scene. Write None/Immediate for inapplicable steps while closing the causal chain. Select mechanisms by genre; misunderstandings, objects, and reversals are not mandatory}
- Volume-Level Contribution: {How the unit supports the volume contract, stage rhythm, or volume objective}
- Protagonist’s Local Objective and Core Interest: {What the protagonist must preserve, obtain, or prove}
- Causal Entry: {Natural entry from the preceding unit or an established event}
- Core Obstacle: {Primary hostility, limitation, mistaken belief, or resource gap}
- Critical Choice and Decisive Action: {The protagonist’s irreplaceable judgment, choice, and action}
- Payoff Method and Ownership: {How the core payoff occurs, who receives the benefit, and how it becomes visible}
- Unit Primary Progression Line/Gains: {Use the volume contract’s division: one primary line carries the climax; other lines receive gains; one victory may deliver several}
- Endgame Trump-Card Boundary: {Locked archenemy/truth/identity/special-advantage ceiling prohibited in this unit; if approached, revise using the authoritative file’s two depletion questions}
- Prohibited Early Release: {Content this unit cannot resolve, reveal, or upgrade early}
- Next-Unit Causal Hook: {Question, cost, clue, or new objective that naturally enters the next unit}
- Risk Level: {Contract Safe / Needs Reinforcement / Contract Violation; specify reinforcement when needed}

## Core Conflict
{One Sentence: What Problem Must This Volume Solve or What Goal Must It Reach?}

## Comparable-Title Structural Coordinates
{Complete when comparable titles exist; otherwise write “No comparable; arrange according to eight-node proportions.” See “Comparable-Title Rhythm Migration” in outline-structure-theory.md for migration steps. Prefer critical plot points from the referenced story unit’s “Plot-Point Index.”}
- Primary Comparable Volume Segment: {对标书} Chapters {A}–{B} (Core-Conflict Correspondence: {One Sentence})

| Normalized Position | This Volume’s Chapter Range | Comparable Critical Plot Point | This Volume’s Equivalent (New Material) | Type {Reversal/Turn/Incitement} |
|-----------|-----------|-------------|-------------------|---------------------|
| 1/4 | Chapter {N} | {对标事件} | {本卷事件} | {类型} |
| Midpoint | Chapter {N} | {对标事件} | {本卷事件} | {类型} |
| 3/4 | Chapter {N} | {对标事件} | {本卷事件} | {类型} |

## Emotional Arc
- Pattern: {V/Inverted V/W/Progressive/Delayed Gratification/Sharp Turn}
- Selection Rationale: {Based on Genre and This Volume’s Position}

| Chapter | Chapter Position {May Be Blank} | Emotional Tone {Tense/Relaxed/Sad/Passionate/Warm/Shocked} | Emotional Intensity {1–10} | Triggering Event |
|------|------------|-----------------------------------------|--------------|---------|
| Chapter {N} | {High Pressure/Progression/Training Trial and Error/Relationship Payoff/Low-Pressure Life/Information Organization} | {基调} | {N} | {事件} |

> Chapter position may be blank; a blank entry defaults to an ordinary progression chapter. Emotional intensity measures emotional force, not the chapter position’s explosive pressure. A relationship or tearjerker chapter may be low pressure but emotionally intense. A volume needs high and low levels. Low-pressure plus restrained transition chapters should total no more than roughly 15%; see outline-structure-theory.md for genre tiers. Review adjacent rows so the same emotional motif does not continue for more than two or three chapters. See “Chapter Positioning and Variation” in outline-structure-theory.md for positions and minimum requirements.

## Character Arcs
| Character | Starting State in This Volume | Ending State in This Volume | Critical Change |
|------|---------|---------|---------|
| {名} | {状态} | {状态} | {事件} |

## Reversals in This Volume (If Any)
| Type {Identity/Motive/Alignment/Information/Fate} | Characters | Misdirection Path | Reveal Chapter | Scope |
|------|---------|---------|---------|---------|
| {类型} | {名} | {How Readers Are Misdirected} | Chapter {N} | {Affected Lines} |

## Foreshadowing in This Volume
| Foreshadowing | Planting Chapter | Planned Payoff | Type {Short-/Medium-/Long-Term} |
|------|---------|---------|---------------------|
```

Creation references: `outline-methods.md` (three-layer outline method) + `outline-rhythm.md` (three-step progression design) + `emotional-arc-design.md` (six arc patterns) + `long-reversal.md` (reversal types and long-term levels)

---

## `大纲/细纲_第XXX章.md`

A detailed outline is the chapter blueprint for drafting, not merely a list of events and hooks. The **sole authoritative template** appears under “Detailed Outline (Every Chapter)” in [Phase 3: Outline Construction](workflow-setup.md#phase-3大纲搭建). It includes unit ID/position, protagonist objective/critical choice, task obstacle, structural formula, contract-risk line, and a four-column plot-point table without per-point word allocations. This file does not retain a duplicate template. Use the authoritative template for new files, reconstruction, and backfilling. Enter `[待补充]` for unknown fields; do not invent subplots or relationships merely to populate fields.

`目标情绪` and `主角目标/关键选择` must contain actual information and cannot remain `[待补充]`. In controlled tests, filling only these two fields reproduced all measured benefits of fully populated outlines; fully populating other fields performed no differently. Continue to mark other unknown fields as `[待补充]`.

After saving, run `node scripts/check-outline-contract.js --json --project {书目录} --chapter {N}` for structural validation. It checks only whether required fields, four subsections, five-part structure, four-column plot-point table, and chapter-length standard are present; it does not judge content quality. On exit 1, add only the fields named in `repair_scope`, then validate again, with no more than two repair rounds. If validation still fails, report the check ID and stop without modifying other chapters. On exit 2, a missing script, or unavailable Node.js, report honestly that validation was not completed; do not claim compliance. Run this check only when creating, reconstructing, or backfilling an outline. Existing projects’ older outlines do not block drafting.

---

## Tracking System

Tracking artifacts are generated only through `scripts/tracking_commit.py`. Complete schemas and transaction fields appear in [tracking-transaction.md](tracking-transaction.md). Models must not independently append to or partially edit the following files.

### `追踪/_tracking-state.json`

The sole structured authoritative state. It records the schema, last committed chapter, import cutoff chapter, `state_revision`, continuation-context structure, and current state of every character, piece of foreshadowing, and timeline item. Daily writing obtains the chapter and revision numbers from the compact output of `tracking_commit.py check`; do not place the full state in the manuscript prompt. Every Markdown file is deterministically derived from this file. The program never reconstructs state by parsing Markdown.

### `追踪/逐章记录/第NNN章.md`

A future-relevant continuity delta for the chapter, targeting no more than 1,536 bytes with a hard limit of 3,072. It contains only actual outcomes, character changes, foreshadowing changes, time/revelations, continuity constraints, and the next-chapter promise. Process logs, quality statistics, reference chapters, and prompt records do not belong here. This file alone does not promise lossless reconstruction of the complete current state; `_tracking-state.json` is authoritative for full current semantics.

### `追踪/伏笔.md`

Keep one row per ID containing only its current state: content, planting chapter, planned payoff chapter, status, importance, and most recent change chapter. The corresponding per-chapter delta contains the change history. Future foreshadowing not yet planted remains in the outline. The current table accepts only `已埋 / 已回收 / 已过期 / 放弃`.

### `追踪/角色状态/{角色名}.md`

Create dynamic snapshots only for core recurring characters. Include the current-through chapter, identity, location, objective, physical/emotional state, abilities/resources, key relationships, known information, and unresolved matters. Target no more than 4,096 bytes with a hard limit of 8,192. If the target is exceeded, consolidate obsolete abilities, old relationships, and resolved matters first; do not put a complete biography into the current snapshot. Static original character profiles remain in `设定/角色/{角色名}.md`. Do not create dynamic files for background or one-time characters.

### `追踪/时间线/`

- `_tracking-state.json.timeline`: For each event, records story time, objective fact, readers’ current understanding, and actual reveal status/chapter.
- `作者真相.md`: Derived from `_tracking-state.json.timeline`; the author-side view includes every objective fact and knowledge gap.
- `读者已知.md`: Derived from `_tracking-state.json.timeline`; displays only what readers already know or believe without revealing objective truth.

Place future reveal plans in volume and detailed outlines, not in the established-facts registry. For an `未揭示` event, `reveal_chapter` must be empty.

### `追踪/上下文.md`

A continuation-state card of no more than 12,288 bytes with seven fixed sections: `当前位置 / 长期约束 / 核心角色状态 / 活跃伏笔 / 近三章速记 / 下一章承诺 / 连贯性风险`. It is one current semantic checkpoint. Do not include style, quality counts, ordinary tasks, index statistics, or long-term summaries.
