# Pipeline Operations Reference

Operations documentation for the story-long-analyze decomposition pipeline: the `_progress.md` template, error handling, and recovery procedures.

> For quality thresholds (confidence, coverage, and overlap), see the [quality-threshold system in material-decomposition.md](material-decomposition.md).

---

## _progress.md Template

```markdown
# 深度拆解进度：{书名}
- 小说：{标题} | 总章数：{N} | 输出目录：{路径} | 开始：{日期}
- 最终状态：{pending/paused_after_stage1/completed/completed_with_errors}
- schema_version: 2
## 管道进度
| 阶段 | 状态 | 进度 | 备注 |
|------|------|------|------|
## 章节边界（Stage 0 章节边界子步骤产物，唯一权威）
| 章号 | 标题 | 起始行 | 字数 |
|------|------|--------|------|
## 分块进度
| 块 | 章节 | 状态 |
## 失败记录
| 类型 | 章节/阶段 | 错误信息 | 重试状态 |
|------|----------|---------|---------|
## 质量检查
| 检查项 | 阶段 | 结果 | 修正 |
## 角色合并
| 合并前 | 合并后 | 依据 | 确认 |
## 断点
- 最后处理：第{N}章 | 当前阶段 | 下一操作
```

<!-- translation-guide: non-executable -->
**English guide (non-executable):**

| Protected heading or field | English meaning |
|---|---|
| `深度拆解进度：{书名}` | Deep-Decomposition Progress: {Book Title} |
| `小说` / `总章数` / `输出目录` / `开始` | Novel / total chapters / output directory / start date |
| `最终状态` | Final status |
| `管道进度` | Pipeline progress |
| `阶段` / `状态` / `进度` / `备注` | Stage / status / progress / notes |
| `章节边界` | Chapter boundaries—the sole authority produced by the Stage 0 boundary substep |
| `章号` / `标题` / `起始行` / `字数` | Chapter number / title / starting line / character count |
| `分块进度` | Chunk progress |
| `失败记录` | Failure log |
| `质量检查` | Quality checks |
| `角色合并` | Character merges |
| `断点` / `最后处理` / `下一操作` | Checkpoint / last processed / next action |
<!-- /translation-guide -->

**About schema_version:**

| Version | Meaning |
|------|------|
| 2 | Current contract: includes the Chapter Boundaries table (the output of the Stage 0 chapter-boundary substep). Stages 1, 2, and 6 all use this table as the authoritative slicing source instead of running their own regex |

The pipeline must not resume if `schema_version: 2` or the Chapter Boundaries table is missing. Rebuild `_progress.md` from the Stage 0 chapter-boundary substep before resuming.

**Final status values:**

| Status | Meaning |
|--------|------|
| `pending` | The pipeline is still running |
| `paused_after_stage1` | Paused at the Stage 1 checkpoint—Stages 0 and 1 are complete, `快速预览.md` has been produced, and the pipeline is waiting for the user to decide whether to continue through Stages 2–6. When resuming, skip Stages 0 and 1 and begin at Stage 2 |
| `completed` | The complete Stage 0–6 pipeline finished |
| `completed_with_errors` | The complete pipeline finished, but one or more chapters or stages failed (see the Failure Log table for details and note the failures in the decomposition report) |

---

## Rebuilding the Story-Unit Index for Existing Books

Trigger this operation when the user says “rebuild the story-unit index,” or when a writing-side lookup finds no Story-Unit Index table in `剧情/README.md`.

Read the Title, Type, Trope Tags, and Chapter Range fields from the header of every existing story-unit file in `拆文库/{书名}/剧情/*.md` (or `对标/{书名}/剧情/*.md`). Mechanically rebuild the index table in `剧情/README.md` using the Story-Unit Index template from output-templates.md. If the project contains a `对标/{书名}/` view, synchronize a copy there. Do not read the source manuscript, rerun any stage, change story-unit content, or modify `节奏.md` or `情绪模块.md`. If an older story unit's Chapter Range line lacks a word count, write only “{N} chapters” in the size column and record the word count as “Unknown.” Never invent a value.

Writing-side consumers automatically fall back to searching individual files when a book has no index. See step 1 of Benchmark Rhythm Transfer in story-long-write's outline-structure-theory.md. Rebuilding the index improves retrieval speed but is not a blocking requirement.

## Error Handling

| Scenario | Handling |
|------|------|
| Chapter detection fails | Ask the user to confirm the format; support a custom regular expression |
| Chunk processing is interrupted | Resume from the checkpoint in _progress.md |
| Aggregation quality is below the threshold | Reclassify isolated plot events; relax the threshold to 0.5 |
| Character merge conflict | Add it to the confirmation-required list |
| Output-directory conflict | Append instead of overwriting; mark the conflict `[重新分析]` |

---

## Recovery Procedure

1. When the pipeline starts, check whether the output directory already contains `_progress.md`.
2. Validate `schema_version: 2` and the Chapter Boundaries table. If either is missing, stop and instruct the user to rebuild the progress file from the Stage 0 chapter-boundary substep.
3. Read the checkpoint data: the last processed chapter, current stage, and final status.
4. If the checkpoint status is `paused_after_stage1` (the Stage 1 checkpoint), skip Stages 0 and 1 and resume chapter-by-chapter summarization at Stage 2. Do not rerun the completed synopsis or opening-three-chapter analysis.
5. For any other checkpoint status, resume from the first chapter of the checkpoint's current chunk and overwrite any existing output for that chunk.
