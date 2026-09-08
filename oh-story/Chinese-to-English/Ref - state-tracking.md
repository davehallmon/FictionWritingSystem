# State-Tracking Protocol

> This file defines the extraction logic for the “Current-Section Brief” and the format of “Character-State Records.” Writing skills load it during the pre-drafting state-filtering step.

---

## Current-Section Brief

Before writing each chapter or section, filter all loaded context to retain only information relevant to the current section. This prevents irrelevant information from diluting the LLM context when everything is loaded at once.

### Filtering Logic

Extract three kinds of information from context:

1. **Current state:** The latest abilities, relationship changes, and public image of characters involved in the chapter.
2. **Historical causality:** The origin and prior events of foreshadowing directly relevant to the chapter's events.
3. **World constraints:** Worldbuilding rules involved in the chapter, including power systems, social rules, and geographic limitations.

### Filtering Standard

**Retain only information whose absence would cause the chapter to be written incorrectly.**

Specific tests:
- A character appears in the detailed chapter outline → retain that character's current state.
- The chapter resolves foreshadowing → retain its planting details and prior setup.
- The chapter involves a specific location, ability, or rule → retain the relevant worldbuilding constraints.
- Pure background knowledge with no causal relationship to the chapter's events → discard it.

### Output Format

After filtering, output a concise “Current-Section Brief”:

```
## 本节速记（第{N}章）

### 角色状态
{角色A}：{一句话当前状态，含最近变化}
{角色B}：{一句话当前状态}

### 相关伏笔/前史
{伏笔1}：{埋设细节，{埋设章节}}，本章需要{回收/推进}

### 世界约束
{约束1}：{与本章相关的规则/设定}
```

**English guide (non-executable):**

| Protected heading or field | English meaning |
|---|---|
| `本节速记（第{N}章）` | Current-Section Brief (Chapter {N}) |
| `角色状态` | Character states |
| `{角色A}：{一句话当前状态，含最近变化}` | Character A: one-sentence current state, including the latest change |
| `相关伏笔/前史` | Relevant foreshadowing and prior history |
| `{埋设章节}` / `回收` / `推进` | Planting chapter / pay off / advance |
| `世界约束` | World constraints |
| `{与本章相关的规则/设定}` | Rule or setting relevant to the current chapter |

**Example (Chapter 10 of the demo *You Manage the Account—and Your High-Energy Mashup Explodes Across the Internet*):**
```
## 本节速记（第10章）

### 角色状态
江晨：火箭军文工团宣传兵，《诸君，且听龙吟》已爆红，正从军宣新人升为军内认可的创作者
钟嘉嘉：军报记者，采访稿已经过审，与江晨从采访关系转为稳定合作
周薄森：文工团副团长，已从担心江晨惹事转为认可其创作能力

### 相关伏笔/前史
五天百万粉任务：第1章发布，第10章仍未结算；本章只推进声量，留到第11章结算
专业团队重拍：本章用高清专业版“缺了灵魂”反衬江晨手机原版不可替代

### 世界约束
军宣作品采用要经过组织决策；江晨可以靠作品效果赢得认可，不能跳过军内流程直接拍板
```

**English guide (non-executable):** In Chapter 10, Jiang Chen is moving from newcomer to recognized military-publicity creator after *Gentlemen, Hear the Dragon's Roar* becomes popular. Reporter Zhong Jiajia has shifted from interviewer to reliable collaborator, and deputy troupe leader Zhou Bosen now trusts Jiang Chen's creative ability. The unresolved five-day, one-million-followers task should advance but not conclude until Chapter 11. A professional remake that “lacks the original's spirit” reinforces the phone-shot version's value. Organizational approval remains mandatory; success cannot bypass the military decision process.

---

## Character-State Record Format

> ⚠️ **This section applies only to long-form writing.** Short-form fiction usually does not require independent character-state tracking.

Split dynamic state into `追踪/角色状态/{角色名}.md` files for core characters. `tracking_commit.py` overwrites each complete file from transaction JSON; static original characterization remains in `设定/角色/{角色名}.md`. Create snapshots only for protagonists, antagonists, and core supporting characters who will recur. Do not create files for bystanders or one-time functional characters.

### Format

```markdown
# 江晨｜当前状态

- 截至章节：第10章
- 身份：火箭军文工团宣传兵；军宣爆款创作者
- 位置：火箭军文工团高层看片会
- 当前目标：完成五天百万粉任务，持续做出真正能打的军宣内容
- 身心状态：专业团队反向验证原版价值，军内认可继续抬升

## 能力与资源
- 前世 MCN 爆款运营经验
- 《中国军魂》伴奏
- 大师级导演能力

## 关键关系
- 钟嘉嘉持续提供军报资源
- 周薄森和张耀祖已明确认可其创作能力

## 已知信息
- 《军报》采访稿已经过审
- 原版视频将继续作为正式军宣内容

## 未结事项
- 五天百万粉任务尚未结算
- 钟嘉嘉所谓“只猜对一半”仍未解释
```

**English guide (non-executable):**

| Protected field | English meaning |
|---|---|
| `截至章节` | Current through chapter |
| `身份` / `位置` / `当前目标` | Identity / location / current objective |
| `身心状态` | Physical and emotional state |
| `能力与资源` | Abilities and resources |
| `关键关系` | Key relationships |
| `已知信息` | Known information |
| `未结事项` | Unresolved matters |

The sample records Jiang Chen's current status through Chapter 10: military-publicity soldier and emerging hit creator, located at a senior screening meeting, pursuing the five-day follower target, equipped with prior-life MCN experience and directing ability, supported by key collaborators, and still awaiting resolution of the follower task and Zhong Jiajia's unexplained remark.

### Update Rules

1. For each chapter, record only content that genuinely changes among identity, location, objective, physical and emotional state, abilities and resources, relationships, known information, and unresolved matters.
2. When a core reusable character changes, write the change to `character_changes` in the same transaction and submit a complete `character_snapshots` snapshot **through the latest written chapter**. The tool uses snapshot existence to distinguish core from temporary characters, overwrites the complete core-character file, and does not append history.
3. When revising an earlier chapter, recalculate current state from the revised chapter through the latest written chapter across every dimension and relationship counterpart, then submit the complete snapshot. Do not treat the most recent one-dimensional change as the character's entire state.
4. If nothing changed, the snapshot may be omitted. When a core character reenters the current scene, read the existing small file directly; the transaction tool carries necessary information into the continuation-state card.
5. Character-change history belongs in `逐章记录/第NNN章.md`; the current snapshot does not duplicate a chapter-by-chapter record.
6. For the complete JSON fields, 4,096-byte target, and 8,192-byte hard limit, see [tracking-transaction.md](tracking-transaction.md).
