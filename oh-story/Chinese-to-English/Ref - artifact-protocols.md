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
# {对标书名} 对标摘要

## 基本信息
- 书名：{}
- 作者：{}
- 题材/类型：{}
- 目标平台：{}
- 成绩：{均订/在读/热度}

## 核心发现
- 开篇钩子：{类型 + 手法}
- 爽点密度：{约 N 字/次}
- 节奏模式：{描述}
- 可借鉴套路：
  1. {}
  2. {}
  3. {}

## 不建议模仿（禁止照搬）
- {}（只学结构，不抄桥段）
```

Creation reference: `plot-special-topics.md` (comparable-title selection rules)

---

## `对标/{对标书名}/原文/第XXX章_{章名}.md`

The original chapter from the comparable title, placed manually by the user or imported through the analysis pipeline.

```markdown
# 第{N}章 {章名}

{本章完整原文内容}

---
> 来源：{手动输入 / story-long-analyze 导入}
> 原始字数：{约N字}
```

---

## `设定/关系.md`

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

Creation reference: `character-relations.md` (relationship types and relationship-map creation)

---

## `设定/题材定位.md`

```markdown
# 题材定位

## 基本信息
- 题材类型：{玄幻/都市/系统/...}
- 目标平台：{起点/番茄/晋江/其他；story-review 据此选平台 rubric}
- 核心梗：{一句话卖点}
- 微创新点：{与同类题材的差异}

## 读者契约（参 `reader-contract-and-progression.md`）
- 核心读者承诺：{读者来追什么爽感/情绪/关系/事业}
- 主角代理权承诺：{主角不可替代的判断、关键选择或贡献}
- 利益安全线：{核心资产/卖点不得被没收、转赠、无交换暴露的边界}
- 期待债：{开篇/本卷已承诺，何时以什么形式偿还}
- 题材边界：{个人逆袭/群像/导师/制度合作等；高层级机构出现时先核对}

## 终局底牌与升级台阶（防写无可写；开书填一次，日更只查。参 `reader-contract-and-progression.md`「终局储备与推进节奏」）
- 终局底牌（一次性资源，标最早解锁卷）：头号宿敌={}·第{X}卷；终极真相/身世={}·第{X}卷；金手指上限={}·第{X}卷；身份/地位终点={}·第{X}卷；核心情感确定={无感情主线可删}·第{X}卷
- 升级台阶：主体系{境界/等级/地图/势力层级}共{N}档 × 每档约{W}万字 应 ≥ 全书目标字数（不足则拉长体系/加地图层）；敌人/目标成梯队逐级解锁，禁止越级秒顶级
- 透支红线：① 未到解锁卷就动用终局底牌 ② 某条升级线逼近天花板、后面没台阶接

## 核心梗三分法
- 表层卖点：{读者一眼看到的吸引力}
- 深层爽点：{持续追读的情绪驱动力}
- 长线钩子：{支撑全书的悬念/目标}

## 对标分析（概要）
> 完整对标数据见 `对标/` 目录。此表仅做快速概览。

| 对标书 | 相似点 | 差异点 | 可借鉴 |
|--------|-------|-------|-------|
| {书名} | {点} | {点} | {点} |

## 对标登记（多对标时必填；cross-book-recall 跨书召回按此排序与预算）
- 主对标书：{书名；单对标可省，多对标必填}
- 对标书列表：

| 书名 | 题材类型 | 引用强度{辅/参考} | 用途 |
|------|---------|-----------------|------|
| {书名} | {类型} | {辅/参考} | {文风主对标/结构参考/…} |

## 题材框架
- 八节点位置：{当前处于哪个节点}
- 关键转折节点：{列出}
```

Creation reference: `long-genre-mechanics.md` (central-hook analysis/application and incremental innovation/differentiation)

---

## `大纲/大纲.md`

Whole-book overview. Begin with “Total Book Length and Stage Overview”—total chapters, target length, whole-book emotional curve, stage divisions, each stage’s rhythm formula, critical nodes, and hook chain, structured according to [Phase 3: Outline Construction](workflow-setup.md#phase-3大纲搭建). Follow it with one-paragraph volume summaries:

```markdown
# 大纲

## 全书体量与阶段总览
{按 Phase 3「全书体量与阶段总览」结构填写}

## 卷级大纲
### 第一卷：{卷名}（约 {X} 万字，{Y} 章）
- 功能 / 所属阶段 / 卷契约 / 终局储备 / 阶段边界 / 核心事件 / 起始状态 → 结束状态
（一段式汇总；展开见各卷 卷纲_第X卷.md）
```

---

## `大纲/卷纲_第X卷.md`

The volume outline expands the main outline: The main outline determines direction; the volume outline determines rhythm. It contains all creative planning for the volume.

```markdown
# {卷名} 卷纲

## 核心信息
- 章节范围：第{X}-{Y}章
- 字数目标：{W}万字
- 本卷定位：{铺垫/发展/高潮/转折/收尾}

## 卷契约与终局储备（参 `reader-contract-and-progression.md`）

> 单章放开密度、宏观管住终局储备。主推线之外的线按剧情自然给战果，一战多得允许；真正要守的是本卷别动用还不该解锁的终局底牌。
- 卷契约：{本卷读者期待、主角高光、主要期待债}
- 本卷主推线：{1条承担本卷最大高潮的升级线：战力线/资源线/身份线/关系线/信息线/地图线/制度线/势力线/事业线/情感确定性}
- 本卷战果：{其余顺带兑现的线，轻触到大涨皆可；一战多得是好设计}
- 本卷解锁的终局里程碑：{参 `设定/题材定位.md`「终局底牌与升级台阶」小节，本卷推进或解锁哪一个大里程碑}
- 本卷禁碰的终局底牌：{尚未到解锁卷、本卷不得动用的宿敌/真相/身份/金手指上限}
- 契约风险：{契约安全 / 需补强 / 契约破坏；需补强时写清补强方式}

## 剧情单元卡（1–3 万字为可调经验值；存于卷纲内；不另建单独文件）

> 剧情单元 = 卷纲里的一级结构单元（见 outline-structure-theory.md「对标节奏迁移」），与下方「对标结构坐标」是同一单元的不同视角，不重复编排。单元长度按本书题材、既有兑现节奏与对标调整，不是硬门槛。规划各关键节点时消费权威文件的“关键节点四问”和期待所有权；无需主角亲自执行每个动作。高潮/兑现后可留短暂低压，以小而可见的收益/奖励承接下一轮压力。引入新地图/机构/能力/敌人/谜团时先检查换书债，不得借新鲜感逃避旧承诺。

### 剧情单元 {L卷号-序号}
- 单元ID：{L卷号-序号}
- 章节范围：{第A-B章}
- 对标剧情参照：{{书名}《剧情标题》（类型/桥段标签；借什么：结构分布/情节点索引/兑现方式）；可列 2-3 条，无对标写「无」}
- 单元节拍/章功能分配：{建立期待→尝试→加压/转向→决定性行动→兑现→余波；标对应章范围，可按题材删改；建卡时可按「对标剧情参照」剧情单元提炼的共性节拍填写，见 outline-structure-theory.md「按剧情批出细纲」}
- 单元承诺：{本单元向读者建立的情绪命题/期待，以及要偿还的期待债}
- 单元情绪引擎：{核心情绪命题→承载对象/情绪缺口→受阻或缺口维持原因→本轮触发→主角不可替代的点火/转化动作→意义变化或可见兑现→题材/契约兑现；承载对象可为人物/关系/目标/规则/场景；不适用环节可写无/即时，但须保持因果闭合；机制按题材选，不强制误解/物件/反转}
- 卷级贡献：{它如何服务本卷契约、阶段节奏或卷级目标}
- 主角局部目标与核心利益：{主角本单元要保住/拿到/证明什么}
- 因果入口：{由上一单元或既有事件自然引出的入口}
- 核心阻碍：{主要敌意、限制、误判或资源缺口}
- 关键选择与决定性行动：{主角不可替代的判断、选择和行动}
- 兑现方式与归属：{核心兑现如何发生，收益归谁、如何可见}
- 本单元主推线/战果：{沿用卷契约划分——主推线1条承担高潮，其余线给战果，一战多得允许}
- 终局底牌边界：{本单元不得动用的未解锁宿敌/真相/身份/金手指上限；碰到就按权威文件透支两问改纲}
- 禁止提前释放：{本单元不能提前解决/揭露/升级的内容}
- 下一单元因果钩子：{自然推入下一单元的问题、代价、线索或新目标}
- 风险等级：{契约安全 / 需补强 / 契约破坏；需补强时写清补强方式}

## 核心矛盾
{一句话：本卷要解决什么问题或达到什么目标}

## 对标结构坐标
{有对标书时填；无则写"无对标，按八节点占比自排"。迁移步骤见 outline-structure-theory.md「对标节奏迁移」；对标关键情节优先取自被参照剧情单元的「情节点索引」}
- 主对标卷段：{对标书}第{A}-{B}章（核心矛盾对应：{一句话}）

| 归一化位置 | 本卷章区间 | 对标关键情节 | 本卷对应（换素材） | 类型{逆转/转折/激励} |
|-----------|-----------|-------------|-------------------|---------------------|
| 1/4 | 第{N}章 | {对标事件} | {本卷事件} | {类型} |
| 中点 | 第{N}章 | {对标事件} | {本卷事件} | {类型} |
| 3/4 | 第{N}章 | {对标事件} | {本卷事件} | {类型} |

## 情绪弧线
- 模板：{V形/倒V形/W形/渐进形/延迟满足形/急转弯形}
- 选择理由：{结合题材和本卷定位}

| 章节 | 章节定位{可留空} | 情绪基调{紧张/轻松/悲伤/热血/温馨/震惊} | 情绪强度{1-10} | 触发事件 |
|------|------------|-----------------------------------------|--------------|---------|
| 第{N}章 | {高压/推进/修炼试错/关系回收/低压生活/信息整理} | {基调} | {N} | {事件} |

> 章节定位可留空，留空按普通推进章处理（即退化为现状）。情绪强度是情感烈度，和章节定位的爆发压力是两回事——关系/泪目章可低压力但高情绪强度。一卷要有高低层次，低压 + 过场克制（合计不超约 15%，题材分档见 outline-structure-theory.md），别全程同一力度；逐行看相邻章情绪基调，别同一母题连超 2-3 章。章节定位与底线见 outline-structure-theory.md「章节定位与张弛」。

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
