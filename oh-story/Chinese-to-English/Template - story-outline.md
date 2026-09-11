---
paths:
  - "**/大纲/**"
---

# Story Outline Rules

Standards for outline files.

## Rules

1. **Required volume-outline content**: Every volume outline (卷纲_*.md) must include the following sections. For field templates, see the volume-outline and “plot unit card” field templates in the story-long-write skill; for contract/progression rules, see its reader-contract and progression references; for handling missing content in legacy volume outlines, see Rule 8:
   - Core information (chapter range / target word count / purpose of this volume)
   - Volume contract and endgame reserves (volume contract / primary progression line for this volume / results achieved in this volume / endgame milestone unlocked by this volume / protected endgame trump card that this volume must not touch / contract risk)
   - Plot unit cards (10,000–30,000 Chinese characters is an adjustable empirical range; write cards inside the volume outline rather than creating separate files. Plot unit cards govern gratification pacing, with no fixed “one major gratification beat every N chapters” cycle. Set chapter-level minimums by platform/genre tier: fast-paced platforms retain the minimum that “every chapter must advance a visible event or gratification beat.”)
   - Core conflict (one sentence: what problem must this volume solve or what goal must it reach?)
   - Emotional arc (the overall emotional direction of the volume)
   - Character arcs (growth/change of major characters within the volume)
   - Foreshadowing in this volume (foreshadowing planted in this volume and planned payoff timing)
   - Reversals in this volume (if any: type / characters involved / misdirection path / reveal chapter)

2. **Required detailed-outline content**: Every detailed outline (细纲_*.md) must include the current “chapter blueprint”:
   - Stage position: current volume/stage, stage objective, this chapter's progress, and connections to adjacent chapters
   - Chapter structure formula: the emotional and conflict-development formula used in this chapter
   - Prohibited early release: truths, trump cards, relationship conclusions, or endgame conflicts this chapter must not reveal prematurely
   - Basic execution fields: core event, target word count, target emotion, unit ID/position, protagonist goal/key choice, opening hook, gratification beat, closing hook, and contract risk. Complete these after reviewing each chapter under items ⑥ and ⑦ of the seven outline-safety checks.
   - Content summary (five-part): inciting cause / development / turn / climax / ending. The ending states the action or image on which the chapter finally lands, not a state judgment.
   - Plot arrangement (multiple lines): main-plot progress / secondary-line progress / event or task line / romantic or relationship line / logic line
   - Character relationships and order of appearance: list characters/factions/key objects in actual order of appearance and state relationship changes
   - Plot refinement: write the plot-point sequence as a table, `# | 情节点（谁做了什么） | 功能标签 | 执行边界`. Do not assign word counts to individual points or predict capacity by beat count. Also state action cost (optional) / ownership of benefit—an action cost is optional; do not manufacture one.
   - Ending definition and hook: closing state (as a concrete final action or image), unresolved question, force driving the next chapter, and closing hook

3. **Incremental writing**: Outlines must be written incrementally—first the skeleton (key events and gratification beats), then details section by section. Do not write every detail at once.

4. **Synchronize with the manuscript**: After completing a chapter's manuscript, return and update the “actual completion” section of its detailed outline.

5. **The opening hook must use one of these types** (for complete techniques, see `story-setup/references/agent-references/long-chapter-hooks.md`):
   Suspenseful-dialogue opening | flash-forward fragment | countdown opening | mysterious monologue | contrastive scene | unfinished-action opening | symbolic foreshadowing

6. **The closing hook must use one of these types** (for complete techniques, see `story-setup/references/agent-references/long-chapter-hooks.md`):
   Sudden revelation | urgent crisis | unfinished action | identity reversal | dilemma | mysterious object/clue | countdown | promise/threat | strange disappearance | hidden meaning | image hook | echo hook | negative-space hook

7. **Every chapter must contain an emotional change**: The detailed outline must mark the emotional start→end (for example, “calm→shock→anger”). Two consecutive chapters with no emotional change require adjustment.

8. **Handling missing content**: Missing chapter-blueprint fields in a legacy detailed outline do not block continued writing. Fall back to legacy fields (core event, plot-point sequence, target emotion, opening/closing hooks, target word count), infer within the current turn's memory, and write back only when the user explicitly asks to supplement or revise the outline. A newly created, supplemented, or revised detailed outline must be completed under the current chapter-blueprint template before manuscript writing begins. A legacy volume outline is likewise nonblocking. If it lacks some Rule 1 sections (for example, it contains only the volume objective/gratification pacing) or uses legacy field names (such as loop ID), fall back by field structure. Upgrade it to the current structure only when the user explicitly asks to supplement or revise the outline; do not automatically rewrite a volume outline for a locked written range. Write `[待补充]` for secondary lines, relationship changes, or cost/benefit that cannot be confirmed from the materials; do not invent them.

## Examples

### Correct — Complete Volume Outline
```
# 卷纲_第一卷.md
## 核心信息
- 章节范围：第1-30章
- 字数目标：9万字
- 本卷定位：铺垫
## 卷契约与终局储备
- 卷契约：沈栀从被欺压到进入暗卫的逆袭爽感；期待债：身世之谜
- 本卷主推线：战力线（灵力第三层→第五层）
- 本卷战果：身份线（拿到暗卫编制）、关系线（与师父建立信任）
- 本卷解锁的终局里程碑：接触暗卫体系
- 本卷禁碰的终局底牌：师父真实身份、古镜完整体
- 契约风险：契约安全
## 剧情单元卡
### 剧情单元 L1-1
- 单元ID：L1-1
- 章节范围：第1-12章
- （其余字段按 story-long-write 技能的「剧情单元卡」字段模板填写）
## 核心矛盾
沈栀要在家族清洗前拿到进入暗卫的资格。
## 情绪弧线
压抑→低谷→觉醒→爆发→余韵
## 人物弧线
沈栀：从隐忍到主动反击
## 本卷伏笔
- F003：古镜碎片（第8章埋，第二卷回收）
- F007：师父真实身份（第12章埋，第三卷回收）
## 本卷反转
第18章：暗卫首领竟是沈栀失散多年的兄长（身份反转，误导路径：首领屡次针对沈栀）
```

#### English guide (non-executable)

- **Volume Outline — Volume One**
- **Core information:** Chapters 1–30; target length 90,000 Chinese characters; purpose: setup.
- **Volume contract and endgame reserves:** Shen Zhi rises from oppression and earns entry into the covert guard, while her mysterious origins remain an expectation debt.
- **Primary progression:** combat strength advances from spiritual-power tier three to tier five.
- **Results:** she receives an official covert-guard position and establishes trust with her mentor.
- **Protected endgame material:** the mentor's true identity and the complete ancient mirror must not be revealed.
- **Plot unit L1-1:** Chapters 1–12; complete its remaining fields from the `story-long-write` plot-unit-card template.
- **Core conflict:** Shen Zhi must qualify for the covert guard before the family purge.
- **Emotional arc:** oppression → low point → awakening → eruption → afterglow.
- **Character arc:** Shen Zhi moves from endurance to active resistance.
- **Foreshadowing:** the ancient-mirror fragment is planted in Chapter 8 for Volume Two; the mentor's identity is planted in Chapter 12 for Volume Three.
- **Reversal:** in Chapter 18, the covert-guard leader is revealed as Shen Zhi's long-lost brother.

All required items are present, endgame trump cards have explicit boundaries, and every setup has a clear payoff plan.

### Wrong — Volume Outline Missing Required Items
```
# 卷纲_第一卷.md
## 本卷目标
沈栀加入暗卫。
## 爽点节奏
每5章一个大爽点。
```

#### English guide (non-executable)

The protected example says only:

- **Volume goal:** Shen Zhi joins the covert guard.
- **Payoff rhythm:** one major payoff every five chapters.

The volume contract and endgame reserves, plot unit cards, and other required items are absent. Plot unit cards govern gratification pacing; do not impose a fixed “one major gratification beat every N chapters” cycle. Fast-paced platforms retain only the chapter-level minimum that “every chapter must advance a visible event or gratification beat.” For existing projects, a legacy volume outline in this form falls back under Rule 8 without blocking or automatic rewriting.
