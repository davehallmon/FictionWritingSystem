---
name: cross-book-recall
description: Multi-benchmark cross-book recall
---

# Cross-Book Recall

## Trigger

First identify the current work from the current project-directory name, `.active-book`, and the book's settings. Exclude `拆文库/{当前书}/` and `对标/{当前书}/` entries whose names match or whose sources point to the current manuscript, including historical entries created by mistake; these are imported analyses of the current book, not cross-book samples. After exclusion, enable this feature only when the project-root `拆文库/` or project `对标/` contains ≥2 books. Read the primary benchmark book from the “主对标书” field in `设定/题材定位.md`. If it is absent, choose the lexicographically first remaining candidate (prefer `对标/`; otherwise use `拆文库/`) and prompt the user to complete it with `gaps.main_benchmark_unspecified: true`.

> **Quantity rule**: At most one primary benchmark book may be used; it supplies prose style and final-manuscript input. There is **no limit on the number registered** as secondary/reference benchmarks. During execution, recall books one at a time according to genre relevance, citation strength, and stage budget. When the budget is exceeded, trim entries rather than deleting books from the registry.

## Three Lines of Defense

1. Do not read a secondary benchmark's `文风.md`, preventing style contamination among multiple books.
2. Character/plot/setting modules may recall from all secondary benchmarks, but results must be ordered by “same genre > weakly related > reference” and constrained by per-book and total budgets.
3. The narrative-writer manuscript prompt consumes only the primary benchmark's style/source-text anchors plus the budget-filtered `副对标召回摘要`. It neither reads nor receives a secondary benchmark's `文风.md` or source text.

## Cross-Genre Determination

For each secondary benchmark, read its “题材类型” and “引用强度” from the “对标书列表” field in the project's `设定/题材定位.md`. Treat an unregistered book as “参考” and output `gaps.benchmark_registry_missing: true`:
- Same genre + citation strength=辅: recall during every stage, up to the per-book limit.
- Same genre + citation strength=参考: take only the most relevant entries, by default no more than half the per-book limit.
- Weakly related: settings/outlining only, ≤1 entry per book.
- Unrelated: skip.

Ordering rules: first by relevance (same genre > weakly related), then citation strength (辅 > 参考), then user order in `对标书列表`. If `对标书列表` is absent or a book is not registered in it, stably order the remaining secondary books by directory/book name in Unicode lexicographic order and output `gaps.benchmark_registry_missing: true` to request completion of the registry. The number of secondary books is unlimited; when total entries exceed the stage budget, trim entries without removing book records.

## Stage Consumption

The numbers below are **per-secondary-book recall limits**. A total stage budget also prevents many secondary books from overflowing the context. A `—` row means that stage does not exist for that form and the entire row should be ignored.

| Stage | Long-form output | Short-form output | Same-genre per-book limit | Weakly related per-book limit | Total stage budget |
|------|---------|---------|----------------|----------------|------------|
| Setup | `拆文报告.md` | `拆文报告.md` + `情节节点.md` | ≤2 | ≤1 | ≤8 |
| Outline | `章节/*_摘要.md` + `剧情/*.md` | `情节节点.md` + `写作手法.md` | ≤3 | ≤1 | ≤10 |
| Module | `角色/` + `剧情/` + `设定/` | — | ≤2 | 0 | ≤8 |
| Manuscript | `文风.md` + source text | `写作手法.md` + source text | 0 | 0 | 0 |

> **Retrieve by plot unit during outlining**: The retrieval key is the plot unit's “类型” (first key; required enum), followed by “桥段标签、套路框架位置” (second key). Among same-genre results, entries matching the same type receive budget priority. This applies only when retrieving by plot unit during the outline stage; it does not change ordering or budget numbers for other stages. When no same-type result exists, fall back to the primary benchmark's source entry, output the nonblocking `gaps.similar_plot_not_found: true`, and continue.

## Output Requirements

Cross-book recall output must include:

```markdown
## 副对标召回摘要
| 书名 | 引用强度 | 相关性 | 召回阶段 | 召回条数 | 使用方式 |
|---|---|---|---|---|---|
| {书名} | 辅/参考 | 同题材/弱相关 | 设定/大纲/模块 | {n} | {用于补充某类结构，不进入文风/原文锚点} |
```

**English guide (non-executable):** Secondary-Benchmark Recall Summary. Columns: book title; reference strength (supporting or reference); relevance (same genre or weakly related); recall stage (setting, outline, or module); recalled-entry count; and use. Use secondary material to supplement a structural function, not as a style or source-text anchor.

When there are many secondary books, output only entries actually recalled during this stage. A secondary book not recalled has not been deleted; it simply did not match within this stage's budget. During the manuscript stage, the table may be passed in as a structural/emotional/setting reference, but the boundary “secondary books do not enter style or source-text anchors” must remain intact.

## Analysis Fields → Writing References

When reading `_meta.json.structure_counts`, use this table to look up the corresponding writing reference registered in the current skill. For short fiction, prefer the genre-styles genre package and short-craft; for long-form work, prefer the corresponding long-form theory files. Do not load across skills any file that is not registered in the current skill's `参考资料` table.

| Analysis field | Meaning | Writing reference |
|---------|------|---------|
| `beats` | Structural segments (opening/development/climax/ending) | `outline-methods.md` + the current `genre-prose-cards/` genre card |
| `hooks` | Number of hooks | `long-chapter-hooks.md` / `long-suspense.md` |
| `setup_clues` | Setup clues for reversals | `long-reversal.md` |
| `character_archetypes` | Contrastive characters | `character-basics.md` / `character-design-methods.md` + the current genre card |
| `reusable_structures` | Reusable techniques | `outline-methods.md` / `plot-core-methods.md`, selected by structural function |
| `reversal_type` | Reversal type (7-value enum) | Corresponding skeleton in `long-reversal.md` |
