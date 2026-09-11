# Short-Story Deconstruction Output Templates

> Load this when producing deconstruction output. First use the decision guide to select a Stage, then complete the corresponding template. See material-decomposition.md for methodological details.
>
> **Output-contract SSOT**: The Stage→file mapping, `_meta.json` fields (including `structure_counts`),
> downstream consumption rules, and acceptance checks are authoritatively defined in [output-contract.md](output-contract.md).
> Template content completed here is ultimately written to Markdown files such as `拆文报告.md`; see the HTML comment
> at the end of each Stage for its destination. Required quality-check fields are marked `[BLOCK]` / `[WARN]` at the end of each section:
> a failed BLOCK item → the “BLOCK item scan” blocks progress; a failed WARN item → add it to the “待补” list without blocking.

## Decision Guide

| Stage Being Executed | Template to Load | Required Fields |
|---------------|-------------|---------|
| Phase 1: Confirm the subject | No template (user interaction; see SKILL.md) | User has provided text + deconstruction direction |
| Stage 2: Structure + plot points | Stage 2 full-story structure + Stage 2B plot points | Story core + at least four structural segments + nodes covering the full text |
| Stage 3: Emotional arc + explosive moments | Stage 3 emotional curve + explosive-moment analysis | At least five nodes + six dimensions of explosive moments |
| Stage 4: Reversals + writing techniques | Stage 4 reversal analysis + writing techniques | Preliminary reversal check + ≥2 setup clues + ≥5 techniques |
| Stage 5: Characters + opening and ending | Stage 5 characters + opening/ending | Every named character + quotation of the first three sentences + ending type |
| Stage 6: Evaluation report | Stage 6 comprehensive evaluation | Five-dimensional score + explosive potential + ≥3 layers of resonance + ≥3 reusable structures |
| Same-type comparison (optional) | Same-type comparison | Differentiating strengths |
| Platform fit (optional) | Platform-fit evaluation | Fit for three platforms |
| Detailed pacing (optional) | Detailed pacing analysis | Pacing metrics + anomaly detection |

## Contents

1. [Stage 2 Full-Story Structure](#stage-2-full-story-structure)
2. [Stage 2B Plot-Point Extraction](#stage-2b-plot-point-extraction)
3. [Stage 3 Emotional Arc + Explosive Moments](#stage-3-emotional-arc-explosive-moments)
4. [Stage 4 Reversals + Writing Techniques](#stage-4-reversals-writing-techniques)
5. [Stage 5 Characters + Opening and Ending](#stage-5-characters-opening-and-ending)
6. [Stage 6 Comprehensive Evaluation](#stage-6-comprehensive-evaluation)
7. [Detailed Pacing Analysis](#detailed-pacing-analysis)
8. [Short-Story Structure Quick-Reference Library](#short-story-structure-quick-reference-library)
9. [Required Quality-Check Fields](#required-quality-check-fields)

---

## Stage 2 Full-Story Structure

<!-- output to: 拆文报告.md (story core + story synopsis + structural division + narrative timeline sections) -->

Length {X} Chinese characters | Sections {N} | Platform {平台} | Type {题材/情绪类型} | Ending {HE/BE/开放式} | POV {第一/第三人称}

### Story Core

**Premise**: {故事前提/触发条件，如"重生三次被母弟杀害"}
**Theme**: {核心矛盾/价值观冲突，如"极端重男轻女"}
**Central action**: {主角做了什么，如"放任母弟自毁"}
**One sentence**: {合并，如"重生三次被母弟杀害的女孩，第四世放任她们自毁"}

### Story Synopsis

{200-500字概括全文}

### Structural Division (4–6 Segments; Must Include Opening / Development / Climax / Ending)

| Segment | Character Range | Share | Function | Corresponding Section |
|------|----------|------|------|--------|
| Opening | {X}-{Y} | {Z%} | {功能} | {节号} |
| Development | {X}-{Y} | {Z%} | {功能} | {节号} |
| {转折/过渡（可选）} | {X}-{Y} | {Z%} | {功能} | {节号} |
| Climax | {X}-{Y} | {Z%} | {功能} | {节号} |
| Ending | {X}-{Y} | {Z%} | {功能} | {节号} |

### Narrative Timeline

| Feature | Description |
|------|------|
| Timeline type | {线性/插叙/倒叙/双线交叉} |
| Time span | {故事内时间跨度} |
| Key time jumps | {如有，标注位置和跨度} |
| Purpose of time manipulation | {制造信息差/压缩无聊/制造对比} |

---

## Stage 2B Plot-Point Extraction

<!-- output to: 情节节点.md (standalone document) + 拆文报告.md (mirrored plot-point-list section) -->

> See “Plot-Point Extraction Rules” in material-decomposition.md for the extraction methodology and node boundaries (the sole authority).

### Node Template

```markdown
N{序号} **{事件概括}**：类型{情绪/信息/冲突/转折/对话/氛围} | 情绪{类型}{强度-9~+9} | 涉及{全名} | 手法{如有时}

原文引用（≤300字）
```

### Output Example

```markdown
## 情节节点清单

N1 **偷听到对话**：类型{信息} | 情绪{震惊}{-7} | 涉及{沈暮月} | 手法{信息差}

> "霍总还不打算让沈暮月母子进门吗？"
> "没必要，私生子而已。"
> 我正准备推门而入，听到这话，手停在了半空。

N2 **自我认知**：类型{转折} | 情绪{心酸}{-5} | 涉及{沈暮月}

> 我是沈家的私生女，生了个儿子，也是私生子。
> 霍庭煜对我没有爱。
> 我默然抽回了手。
```

### Quality Self-Check

- [ ] Node count falls within the density guidance
- [ ] Every node uses objective, plain description without narrative-framework terms or subjective judgment
- [ ] Every node has an emotion marker (type + intensity)
- [ ] Nodes are arranged in strict chronological order
- [ ] Source quotation is continuous and ≤300 Chinese characters

---

## Stage 3 Emotional Arc + Explosive Moments

<!-- output to: 拆文报告.md (emotional curve + explosive-moment analysis + anticipation analysis sections) -->

### A. Emotional Curve

Use at least five nodes, placed where emotional alignment, anticipation, or pressure actually changes. Include the character-count position and label each node’s hook type:

| Position | Character Count | Node Number | Emotion | Intensity and Direction | Triggering Event | Hook Type |
|------|------|----------|------|------------|----------|----------|
| Opening | {X} | N{N} | {好奇/心酸/震惊} | {虐-9~爽+9} | {事件} | {悬念/冲突/反差/代入/信息差/无} |
| Low point | {X} | N{N} | {心疼/绝望/愤怒} | {虐-9~爽+9} | {事件} | {钩子类型} |
| Reversal point | {X} | N{N} | {震惊/心疼} | {虐-9~爽+9} | {事件} | {钩子类型} |
| Climax | {X} | N{N} | {情绪} | {虐-9~爽+9} | {事件} | {钩子类型} |
| Ending | {X} | N{N} | {满足/意难平/治愈} | {虐-9~爽+9} | {事件} | {钩子类型} |

Hook-type reference: suspense (wanting to know what follows), conflict (escalating contradiction), contrast (overturned perception), identification (shared feeling), information gap (readers know what the character does not)

Curve characteristics: Start {...} | Direction {上行/下行/波浪/V形/倒V/阶梯/断崖/压缩弹簧} | Extremes {最高%X 最低%Y} | Directional difference {从X到Y} | Number of reversals {N}

### B. Explosive-Moment Analysis

| Dimension | Analysis |
|------|------|
| Setup | {什么让读者开始在意}，前{X}字完成 |
| Accumulation | {什么在积累情绪势能}，积累{X}字 |
| Delay | {延迟释放机制：信息差/误解/悬念} |
| Eruption | {哪个瞬间释放全部情绪}，精确到句子："{引用}" |
| Aftermath | {释放后的余震：角色反应} |
| Impression | {情绪释放后留下什么，读者记住什么} |

**Layered explosive moments** (if applicable): Surface {X}→deeper {Y}→combined effect {1+1>2在哪}

**Linked explosive moments** (if applicable): Moment ① {事件+位置} | Moment ② {事件+位置} | Moment ③ {事件+位置} → Linkage {递进/并列}

### C. Anticipation Analysis

Track the reader’s expectation state section by section:

| Section | Anticipation Created | Satisfied / Escalated / Suspended | Remaining Anticipation |
|----|-----------|---------------|---------|
| 1 | {期待A} | {制造} | {A} |
| 2 | {期待B} | {升级A} | {A+, B} |
| ... | | | |

Anticipation rules: Never go more than two sections without creating new anticipation or more than one section without advancing the central expectation.

---

## Stage 4 Reversals + Writing Techniques

<!-- output to: 拆文报告.md (reversal-analysis section) + 写作手法.md (standalone document: POV / dialogue / time / information / other / imagery) -->

### A. Reversal Analysis

#### Preliminary Reversal Check

> Did a lie or mistaken judgment already exist before the story’s timeline began?

| Preliminary Reversal | Who Was Deceived / Kept in the Dark | When Revealed | Method of Revelation | Effect on Main Reversal |
|----------|--------------|----------|----------|--------------|
| {如：三年前的"灌醉"事件实为做局} | {霍庭煜} | {第9章} | {沈暮月当面驳斥} | {铺垫：证明判断基于错误前提} |

If none exists, write “无.”

#### Retribution Design (For Stories Without Reversals / Retribution Stories)

> When the story has no traditional reversal, skip the reversal-mechanism breakdown and analyze retribution design instead.

| Stage | Villain’s Wrongdoing | Retribution | Source of Satisfaction |
|------|-----------|----------|----------|
| {如：虐待妻女} | {具体行为} | {对应惩罚} | {以彼之道还施彼身/自食恶果} |

Retribution-chain effect: {递进/一一对应/连锁反应}

#### Reversal Chain (For Multi-Reversal Stories)

> If the story contains multiple consecutive reversals, such as public-opinion or nested-reversal fiction, list them in order:

| Number | Reversal Type | Triggering Event | Change in Reader Perception | Causal Relationship to Previous Layer |
|------|----------|----------|-------------|---------------|
| 1 | {类型} | {事件} | {从A认知变为B认知} | — |
| 2 | {类型} | {事件} | {从B认知变为C认知} | {反转1如何解释/加深反转2} |

Reversal-chain effect: {递进/叠加/出其不意}
Causal-chain strength: {强/中/弱——删除任一层反转，其他是否仍成立？}

**Foreshadowed reversal**: If an opening sentence completely changes meaning after the truth is revealed, record:
- Original sentence + location
- Initial reading vs. retrospective reading
- Event that triggers the perceptual upgrade

For a single-reversal story, skip this table and use the main/secondary reversal analysis below.

#### Main / Secondary Reversal Analysis (For Single-Reversal Stories)

**Reversal type**: {视角反转/身份反转/动机反转/时间线反转/信息反转/认知反转}

> **Perceptual reversal**: The reader’s overall understanding of a character or relationship is overturned (for example, “the mother actually loved her all along”). Unlike an information reversal, which changes one fact, a perceptual reversal changes the emotional character of the entire person or relationship.

**Reversal mechanism**:
- Setup clues: {文本埋了哪些线索，含位置}
- Misdirection: {文本把读者往哪个方向引}
- Truth revealed: {反转怎么揭开的}
- Plausibility: {反转是否经得起回看}

**Timing**: At {X}% of the full text | Setup:release = {X:1}

**Effect**: Surprise {1-5} | Plausibility {1-5} | Emotional impact {1-5}

### B. Writing Techniques

> See “Writing-Technique Analysis” in material-decomposition.md for the methodology.

#### POV Strategy

| Dimension | Analysis |
|------|------|
| POV type | {第一/第三人称/全知/其他} |
| Effect of choice | {亲密感/信息控制/距离感} |
| Information control | {不可靠叙述者/选择性回忆/隐瞒} |
| POV switches | {如有：切换位置、切换方式、效果评价。如无：填"无"} |
| POV cost | {丧失了什么视角/信息} |

#### Dialogue Techniques

> Dialogue share describes only this text. Judgment must cite specific scene functions and compare with benchmark samples from the same genre and platform; do not apply a universal range.

| Metric | Value | Assessment |
|------|------|------|
| Dialogue share | {X%} | {该文本倾向/相对对标偏高/相对对标偏低，并说明场景功能} |
| Subtext rate | {X%} | {结合告知/求救/试探/回避等具体场景说明效果，不以越高越好} |
| Dialogue mode | {审判式/压制式/信息差式/推拉式/称呼变化} | {具体说明} |

#### Time Manipulation

| Technique | Location | Effect |
|------|------|------|
| {时间跳跃/场景压缩/倒叙/闪回/实时展开} | {节N} | {具体效果} |

#### Information Control

| Moment | What Readers Know | What the Protagonist Knows | What the Opponent Knows | Information Gap |
|------|-----------|-----------|-----------|--------|
| Opening | | | | |
| Middle | | | | |
| Ending | | | | |

#### Other Techniques

| Technique | Location | Effect | Reusability |
|------|------|------|----------|
| {感官锚定/句式节奏/对比设计/意象物件/留白/首尾呼应} | {节N} | {具体效果} | {高/中/低} |

#### Image / Object Tracking

| Object / Image | Appearances | Meaning at Each Appearance | Evolution |
|-----------|---------|---------------|---------|
| {物件名} | {节1, 节5, 节9} | {含义变化} | {从A到B} |

If no object or image repeats, write “无明显意象重复.”

**Thematic image group**: If several objects point to one theme, note the common theme, each object’s angle, and the overall effect.

**Technique total**: {N} items | Core techniques {Top3} | Innovative technique {如有}

---

## Stage 5 Characters + Opening and Ending

<!-- output to: 拆文报告.md (character analysis + opening analysis + ending analysis + opening-ending correspondence + hook-resolution check sections) -->

### A. Character Analysis

> See “Character-Extraction Rules” in material-decomposition.md for the methodology.

**Character overview**: {N} named characters

| Character | Narrative Role | Action Role | Function Label | Internal Conflict | Arc | Key Line |
|------|----------|----------|----------|----------|------|----------|
| {主角名} | {主人公/重要配角} | {主动型/被动型/转变型} | {情绪承载者/...} | {核心心理冲突} | {始→转→终} | "{最具代表性的台词}" |
| {配角名} | {重要配角/功能人物} | {主动型/被动型} | {压迫源/...} | {矛盾} | {弧线/扁平} | "{台词}" |

> If a dual-protagonist structure is identified, mark both people as “主人公” in the character-overview table and note below the table which chapter range each primarily drives.

**Character-function assessment**:

| Character | Appearance Efficiency | Function Density | Removability | Dialogue Contribution |
|------|----------|----------|----------|----------|
| {名} | {高/中/低} | {承担N项功能} | {不可删/可删} | {每句都推动/部分推动} |

**Character relationships**:

| Pair | Essence of Relationship | Evolution | Contribution to Emotional Arc |
|--------|----------|----------|---------------|
| A ↔ B | {如：单向依附→对等拒绝} | {节N:状态A → 节M:状态B} | {制造了什么情绪} |

### B. Opening Analysis

**First three sentences**: {原文引用}

| Dimension | Analysis |
|------|------|
| Hook type | {悬念/冲突/反差/代入/信息差} |
| First 50 Chinese characters | {有无冲突/异常？有/无} |
| First 100 Chinese characters | {读者是否知道核心矛盾？是/否} |
| Information density | {高/中/低} |
| Identification | {强/中/弱} |
| Distinctiveness of voice | {强/中/弱} |
| Opening emotional intensity | {1-10，绝对强度量表，非情感曲线的-9~+9} |

### C. Ending Analysis

**Final paragraph**: {原文引用或概括}

| Dimension | Analysis |
|------|------|
| Ending type | {HE满足/BE遗憾/开放式/反转余韵/留白} |
| Emotional landing | {读者离开时在想什么} |
| Aftertaste design | {有/无，具体描述} |
| Sharing impulse | {读者是否会推荐，为什么} |
| Completeness of resolution | {所有钩子是否回收，未回收的列出} |
| Values conveyed | {这篇故事最终想说什么？} |
| Ending emotional intensity | {1-10，绝对强度量表（非情感曲线的-9~+9）。参考标准：虐≥8/爽≥7/治愈≥6/通透满足≥5/震惊反转≥7/BE意难平≥8} |

### D. Opening-Ending Correspondence

| Echoed Element | Opening Location | Ending Location | Method | Effect |
|----------|----------|----------|----------|------|
| {元素} | {如：第1节"私生子而已"} | {如：结尾终身未娶} | {对比/反转/升级} | {形成闭环/制造遗憾} |

**Discovery on rereading**: If an opening sentence changes meaning completely after the truth is revealed, list the original sentence + location + initial understanding vs. understanding after learning the truth.

### E. Hook-Resolution Check

| Hook | Placement | Type | Resolution Location | Method of Resolution | Status |
|------|----------|------|----------|----------|------|
| {描述} | {节N} | {悬念/冲突/信息差} | {节M} | {如何回收} | {已回收/留白/遗漏} |

---

## Stage 6 Comprehensive Evaluation

<!-- output to: 拆文报告.md (comprehensive section: five-dimensional score + explosive potential + discussion potential + resonance + core techniques + reusable structures + same-type writing actions + pacing brief) + _meta.json.structure_counts (numeric metadata; see "_meta.json.structure_counts Output Template" below) -->

**One-sentence assessment**: {成功核心原因——具体指出成功机制，避免泛泛赞美}

### Five-Dimensional Score

| Dimension | Score | Explanation |
|------|------|------|
| Opening appeal | 1-5 | {具体说明：钩子类型+效果+改进空间} |
| Emotional push and pull | 1-5 | {具体说明：曲线形态+极值+翻转} |
| Reversal design | 1-5 | {具体说明：反转类型+铺垫质量+合理性} |
| Pacing control | 1-5 | {具体说明：密度分布+异常检测+节奏匹配} |
| Ending aftertaste | 1-5 | {具体说明：结尾类型+落点+传播欲} |

### Explosive Potential

{核心爆点是什么？铺垫是否充分？释放是否到位？传播性如何？}

### Discussion Potential

{读者会讨论什么？争议点？代入式自省？"如果是我会怎样"的讨论空间？}

### Resonance Analysis

| Layer of Resonance | Strength | Trigger |
|----------|------|--------|
| Emotional resonance | {强/中/弱/无} | {具体触发点} |
| Values resonance | {强/中/弱/无} | {具体触发点} |
| Experiential resonance | {强/中/弱/无} | {具体触发点} |
| Social-phenomenon resonance | {强/中/弱/无} | {具体触发点} |
| Cultural resonance | {强/中/弱/无} | {具体触发点} |
| Universal-value resonance | {强/中/弱/无} | {具体触发点} |
| Philosophical resonance | {强/中/弱/无} | {具体触发点} |
| Deep emotional resonance | {强/中/弱/无} | {具体触发点} |
| Deep character resonance | {强/中/弱/无} | {具体触发点} |

### Core Techniques

Reversal type {...} | Emotional-curve shape {...} | Key hooks {...} | Top 3 core techniques {...}

### Reusable Structures

1. **{手法名}**: {用法} — Best for: {什么类型的短篇}
2. **{手法名}**: {用法} — Best for: {...}
3. **{手法名}**: {用法} — Best for: {...}

### Same-Type Writing Action

{具体行动——可直接进入下一份 artifact 的操作，避免只写"多练习"}

### Pacing Brief

| Metric | Value | Judgment |
|------|------|------|
| Event density | {X个/千字} | {文本分布与真实状态变化} |
| Dialogue density | {Y%} | {文本倾向、对白功能与无对白推进方式} |
| Conflict density | {Z%} | {直接冲突与其他压力来源的关系} |

### _meta.json.structure_counts Output Template

> When Stage 6 is complete, write this section’s structural counts to `_meta.json.structure_counts` as the basis for
> numeric “structure_counts validation.” Write the analytical narrative to the corresponding section in `拆文报告.md`; do not repeat it in JSON.
> See [output-contract.md](output-contract.md) for field definitions and thresholds.

```jsonc
"structure_counts": {
  "beats": 5,                    // 来自 Stage 2 结构段数（开端/发展/高潮/结局，≥4）
  "hooks": 4,                    // 来自 Stage 3 钩子数（≥3）
  "setup_clues": 3,              // 来自 Stage 4 反转铺垫数（≥3；无反转题材填 0 并跳过该阈值）
  "character_archetypes": 3,     // 来自 Stage 5 有反差人物数（≥2）
  "reusable_structures": 3,      // 来自 Stage 6 可复用条数（≥3）
  "reversal_type": "视角反转"     // 枚举: 视角/身份/动机/时间线/信息/认知/无反转
}
```

---

## Optional Module: Same-Type Comparison

> See “Optional Module: Same-Type Comparison” in material-decomposition.md for the methodology.

| Dimension | This Text | Comparable Work A | Comparable Work B |
|------|------|----------|----------|
| Emotional-curve shape | {如：压缩弹簧} | {如：V形} | {如：波浪} |
| Core technique | {如：假死+信息差} | {如：时间线反转} | {如：套娃反转} |
| Opening-hook strength | {1-5} | {1-5} | {1-5} |
| Reversal surprise | {1-5} | {1-5} | {1-5} |
| Ending aftertaste | {1-5} | {1-5} | {1-5} |

**Differentiating strength**: {本文与同类作品的关键差异，是优势还是劣势}

---

## Optional Module: Platform-Fit Evaluation

> See “Optional Module: Platform-Fit Evaluation” in material-decomposition.md for the methodology.

| Platform | Fit | Reason | Adjustment |
|------|--------|------|----------|
| Zhihu Salt Selection | {高/中/低} | {原因} | {如有} |
| Fanqie Short Stories | {高/中/低} | {原因} | {如有} |
| Qimao Short Stories | {高/中/低} | {原因} | {如有} |

---

## Detailed Pacing Analysis

> Optional module. See “Pacing Analysis” in material-decomposition.md for the methodology.

### Pacing Metrics

> Values in each dimension describe this text only. Judgment must return to specific nodes, state changes, and consequences, and compare them with same-genre, same-platform samples when comparables exist.

| Dimension | Value | Judgment |
|------|------|------|
| Event density | {N}个/千字 | {文本分布与真实状态变化} |
| Dialogue density | {X%} | {文本倾向、对白功能与无对白推进方式} |
| Conflict density | {X%} | {直接冲突与任务/证据/空间/关系压力的关系} |
| Information density | {X%} | {读者模型变化与消化效果} |

### Section-by-Section Pacing Distribution

| Section | Length | Event Density | Dialogue Share | Conflict Share | Pacing Judgment |
|----|------|----------|----------|----------|----------|
| 1 | {N} | {X/千字} | {Y%} | {Z%} | {快/中/慢/过渡} |

### Pacing Anomalies

| Anomaly Type | Location | Explanation |
|----------|------|------|
| {节奏塌陷/压力过载/信息洪峰/对白失效/对白挤压场景/反转过载} | {节N} | {具体说明} |

If none exist, write “节奏无明显异常.”

---

## Short-Story Structure Quick-Reference Library

> See “Structure-Type Quick Reference” in material-decomposition.md for the complete version, including matching analysis points.

---

## Required Quality-Check Fields

Check every item before completing a Stage; any omission makes the output incomplete. **Node density, dialogue share, and similar values are structured descriptions only. Quality judgments must cite specific scene functions, state changes, and same-genre comparables; do not set universal numeric thresholds.**

**Marking conventions**:

- `[BLOCK]`: Quantitative or mandatory artifact. Missing → the “BLOCK item scan” blocks progress; do not write `_meta.json.stages_completed[6]`; instruct the user to return to the corresponding Stage and complete it.
- `[WARN]`: Qualitative or supporting item. Missing → write it to the “待补” list at the end of `拆文报告.md` and **do not block** the next stage.

**Stage 2 (structure + plot points)**:
- [ ] Story core extracted (one-sentence central hook) `[BLOCK]`
- [ ] Structure divided into 4–6 segments (must include opening / development / climax / ending), each with character range, share, and function `[BLOCK]`
- [ ] Ending type labeled `[WARN]`
- [ ] POV identified `[WARN]`
- [ ] Narrative timeline labeled `[WARN]`
- [ ] Plot points cover genuine changes across the full text without duplicating one event to meet a quota (see “Plot-Point Extraction Rules” in material-decomposition.md) `[BLOCK]`
- [ ] Every node has an emotion marker (type + intensity) `[BLOCK]`

**Stage 3 (emotional arc + explosive moments)**:
- [ ] At least five emotional nodes cover every change in alignment, anticipation, or pressure, each with a character-count position, intensity, and direction (虐-9~爽+9) `[BLOCK]`
- [ ] Every node has a hook type, including “无” `[WARN]`
- [ ] All five curve characteristics are complete (start / direction / extremes / directional difference / reversal count) `[BLOCK]`
- [ ] All six dimensions of explosive-moment analysis are complete (setup / accumulation / delay / eruption / aftermath / impression) `[BLOCK]`
- [ ] Anticipation table completed `[WARN]`

**Stage 4 (reversals + writing techniques)**:
- [ ] Preliminary reversal check performed (exists / does not exist) `[WARN]`
- [ ] Reversal type identified `[BLOCK]`
- [ ] At least two setup clues included with source locations `[BLOCK]`
- [ ] Misdirection explained `[WARN]`
- [ ] Writing-technique analysis covers ≥5 dimensions `[BLOCK]`
- [ ] POV strategy analyzed (effect of choice + cost + switching) `[WARN]`
- [ ] Dialogue metrics quantified (share + subtext rate) `[WARN]`

**Stage 5 (characters + opening and ending)**:
- [ ] Every named character extracted with a two-dimensional classification (narrative role: 主人公/重要配角/功能人物 + action role: 主动型/被动型/转变型) `[BLOCK]`
- [ ] Character-function assessment completed `[BLOCK]`
- [ ] Relationship evolution marked `[WARN]`
- [ ] Original first three sentences quoted `[BLOCK]`
- [ ] First-50 / first-100-Chinese-character checks completed `[WARN]`
- [ ] Opening emotional intensity labeled (1–10) `[WARN]`
- [ ] Ending type and emotional landing explained `[WARN]`
- [ ] Hook-resolution check completed `[WARN]`
- [ ] Opening-ending correspondence analyzed `[WARN]`
- [ ] Resolution status labeled for every hook (已回收/留白/遗漏) `[WARN]`

**Stage 6 (comprehensive evaluation)**:
- [ ] One-sentence assessment identifies a specific mechanism rather than offering generic praise `[WARN]`
- [ ] Every item in the five-dimensional score has a specific explanation rather than a general statement `[BLOCK]`
- [ ] Explosive potential analyzed `[BLOCK]`
- [ ] Discussion potential analyzed `[BLOCK]`
- [ ] At least three layers of resonance analyzed `[BLOCK]`
- [ ] At least three reusable structures, each with a use case `[BLOCK]`
- [ ] Same-type writing action is concrete `[WARN]`
- [ ] `_meta.json.structure_counts` written and every field meets the “structure_counts numeric validation” thresholds (see the corresponding table in [output-contract.md](output-contract.md)) `[BLOCK]`

**Acceptance integration**: The `[BLOCK]` items above and the “minimum field count” table in [output-contract.md](output-contract.md) jointly form the checklist for the “BLOCK item scan.” The “Acceptance” section of SKILL.md invokes it after the Stage 6 content is complete and before appending `stages_completed[6]`.
- [ ] Pacing brief included
