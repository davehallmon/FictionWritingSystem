---
paths:
  - "**/设定/**"
  - "**/大纲/**"
  - "**/追踪/**"
---

# Story Consistency Rules

Follow these consistency rules whenever modifying specification, outline, or tracking files.

## Rules

1. **Specification changes require a tracking check:** Whenever a character specification or world rule changes, run `tracking_commit.py check` to confirm that `_tracking-state.json` agrees with every derived view. Then inspect the current foreshadowing table, relevant character snapshots, and the author and reader timelines to ensure that the change creates no conflict or premature disclosure.

2. **Every new character requires a separate file:** Give each major character an independent specification file and update 关系.md if it exists.

3. **Timeline changes must use a transaction:** If a change affects chronology, objective facts, or reader knowledge, update the event through a `mode=revision` transaction for the corresponding chapter. Let the tool derive `作者真相.md` and `读者已知.md` consistently.

4. **Submit a specification change through one semantic transaction:** Store permanent rulings in the transaction's `delta.constraints` and the current complete `context.long_term_constraints`. Store requirements that must be fulfilled in the next chapter in `delta.next_chapter_commitments`. The tool generates the compact delta and the fixed seven-section continuation-state card. Do not directly edit `逐章记录/`, `上下文.md`, character snapshots, the foreshadowing table, timeline views, or summaries.

5. **Consistency checks must use grep:** Do not rely on memory; verify by searching. Common checks:
   - Character attributes: `grep -rn "角色名" 设定/ 正文/ | grep "属性关键词"`
   - Timeline: `grep -rn "第.*天\|.*日后\|过了.*时" 正文/`, then compare against `追踪/时间线/作者真相.md` and `读者已知.md`
   - Power system: `grep -rn "体系关键词" 设定/ 正文/`
   - Foreshadowing status: `grep -rn "F[0-9]" 追踪/伏笔.md`

6. **Padding-warning signals** (warn whenever found): an entire chapter of dialogue adds no new information; the same emotion continues for three or more consecutive paragraphs; more than 500 Chinese characters of scene description produce no progression; a character recalls prior events without a new perspective; or two consecutive chapters contain no conflict.

## Examples

### Correct
```
修订 demo 第 10 章“专业团队拍得还不如他拍得好？”后：
1. 检查 F027、江晨快照以及第 10 章相关时间线事件
2. 构造第 10 章 `mode=revision` 事务，保留“专业重拍版缺了灵魂、张耀祖决定继续用手机原版”的正文事实
3. 作者真相可保留钟嘉嘉未公开的培养安排；读者视图只保留看片会已经揭示的结论
4. 提交后运行 `tracking_commit.py check`，确认逐章增量、角色快照、伏笔与双时间线视图一致
```

**English guide (non-executable):**

> After revising Chapter 10 of the demo, inspect F027, Jiang Chen's snapshot, and the Chapter 10 timeline events. Submit a Chapter 10 `mode=revision` transaction that preserves the manuscript facts: the professional remake lacked the original's spirit, and Zhang Yaozu chose to continue using the phone-shot version. The author timeline may retain Zhong Jiajia's unrevealed development plan, but the reader view may contain only conclusions revealed at the screening. Run `tracking_commit.py check` after submission to verify that chapter deltas, character snapshots, foreshadowing, and both timeline views agree.

### Wrong
```
直接在 `伏笔.md` 末尾追加第二条 F027，并分别手改 `作者真相.md`、`读者已知.md` 和 `上下文.md`。
结果：同一伏笔出现多个“当前状态”，读者视图泄露钟嘉嘉的未公开安排，检查点却无法知道哪些派生文件已经失效。
```

**English guide (non-executable):**

> Append a second F027 directly to `伏笔.md`, then manually edit `作者真相.md`, `读者已知.md`, and `上下文.md`. This creates multiple “current states” for the same foreshadowing item, leaks Zhong Jiajia's unrevealed plan into the reader view, and leaves the checkpoint unable to determine which derived files are stale.
