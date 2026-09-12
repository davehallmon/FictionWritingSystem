---
paths:
  - "**/拆文库/**"
  - "**/对标/**"
  - "**/设定/**"
---

# Story Narrative Rules

Narrative rules for story decomposition, benchmark analysis, and specification files.

## Rules

1. **Cross-check specifications:** When adding or changing a specification, check it against existing specifications for contradictions. Use grep to search existing specification files for relevant keywords and confirm compatibility.

2. **Maintain a consistent language style:** Each character's dialogue must match the language-style profile in that character's specification, including tone, habitual vocabulary, and frequency of exclamation marks.

3. **Define worldbuilding rules explicitly:** Record what is and is not possible under power systems, social rules, and similar constraints. Apply those rules consistently in the manuscript.

4. **Every mystery requires a documented true answer:** Record a clear true answer for every planted mystery or question in the tracking or specification files. Do not leave the answer ambiguous.

5. **Keep character motives and relationships internally consistent:** A character's behavior must follow from established motives, and every relationship change must have a credible triggering event.

6. **Apply the three-function dialogue test:** Remove each exchange and ask: Can the plot still advance? Does the expectation remain? Does the emotion still land? Three “no” answers mean the dialogue is padding; delete it.

## Examples

### Correct — Cross-Checking a Specification
```
新增设定：灵力等级分为九层，最高为第九层"破境"。
执行动作：
1. grep 设定/ 目录中所有文件，确认没有其他灵力体系描述
2. grep 追踪/伏笔.md 中"灵力"关键词，确认无矛盾伏笔
3. 本章追踪事务里带上这条裁定：写进 `delta.constraints`，并同步进 `context.long_term_constraints` 的完整当前值；由 `tracking_commit.py` 生成 追踪/逐章记录/ 与 追踪/上下文.md，不手写这两个文件
```

<!-- translation-guide: non-executable -->
**English guide (non-executable):**

> New rule: spiritual power has nine tiers; the ninth and highest is the “Breakthrough Realm.”  
> Actions: search every file in `设定/` for another description of the power system; search `追踪/伏笔.md` for “spiritual power” to confirm that no foreshadowing conflicts; then record the ruling in the chapter transaction's `delta.constraints` and complete `context.long_term_constraints`. Let `tracking_commit.py` generate the chapter record and continuation context instead of editing those files manually.
<!-- /translation-guide -->

Before adding a specification, proactively search existing specifications and foreshadowing records to prevent contradictions.

### Wrong — Specification Added Without a Cross-Check
```
直接在设定/世界规则.md 中添加"灵力等级分为十层"。
结果：已有设定文件中记载"灵力最高为九层"，两处矛盾。
且追踪/伏笔.md 中有一条伏笔依赖"九层"设定。
```

<!-- translation-guide: non-executable -->
**English guide (non-executable):**

> Add “spiritual power has ten tiers” directly to `设定/世界规则.md`. The existing specification already says that nine is the highest tier, creating a contradiction. A foreshadowing record in `追踪/伏笔.md` also depends on the nine-tier rule.
<!-- /translation-guide -->

Adding new material without checking existing specifications creates contradictory worldbuilding.

### Correct — A Mystery Has a Documented True Answer
```
正文第15章写到：密室中的古镜映出一个陌生人的脸。
本章事务登记：`foreshadow_changes` 埋下 F012（古镜陌生人，第15章埋、计划第38章回收）；
作者侧真相「是沈栀前世记忆的残留投影」写进 `timeline_events.objective_fact`（派生到 时间线/作者真相.md），
或长期设定写进 `设定/`。伏笔.md 是工具渲染的当前状态视图，没有「真实答案」列，不手写。
```

<!-- translation-guide: non-executable -->
**English guide (non-executable):**

> Chapter 15 shows an ancient mirror reflecting a stranger's face. Register foreshadowing item F012, planted in Chapter 15 and planned for payoff in Chapter 38. Store the author-side truth—“the image is a residual projection of Shen Zhi's past-life memory”—in `timeline_events.objective_fact`, or store a durable rule under `设定/`. Do not manually edit the tool-rendered current-state view.
<!-- /translation-guide -->

Every mystery has a clear true answer and planned resolution point in the tracking files.

### Wrong — A Mystery Has No Documentation
```
正文第15章写到：密室中的古镜映出一个陌生人的脸。
追踪/伏笔.md 中无任何记录。
写作到第40章时，后续正文遗忘这个悬念，或给出与既有追踪记录矛盾的解释。
```

<!-- translation-guide: non-executable -->
**English guide (non-executable):**

> Chapter 15 shows the ancient mirror reflecting a stranger's face, but no tracking record is created. By Chapter 40, the manuscript may forget the mystery or resolve it in a way that contradicts established tracking data.
<!-- /translation-guide -->

An undocumented mystery is easily forgotten or resolved inconsistently.
