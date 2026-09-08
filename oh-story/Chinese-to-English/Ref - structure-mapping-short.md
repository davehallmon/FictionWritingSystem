# Structural Migration Mapping Rules (Short Fiction)

Detailed mapping rules for Phase 3-S short-fiction structural migration. Converts short-fiction analysis artifacts from `拆文库/{导入书名}/` into the `{短篇标题}/` short-fiction project structure, enabling a seamless handoff to Phase 3 continuation writing in `story-short-write`.

> For long-fiction migration rules, see `structure-mapping-long.md`.

> **Naming boundary**: `{导入书名}` is the user's own short story to be continued; `{对标书名}` is a separately selected external reference work. Never copy this story's analysis results into its own `对标/` directory, and never present analysis of this story as a “benchmark summary.”

---

## Key Differences from Long Fiction

| Dimension | Short fiction | Long fiction |
|------|------|------|
| Manuscript | Single `正文.md` file, **not divided into chapters** | Multiple `正文/第XXX章_章名.md` files |
| Tracking directory | **Do not produce** `追踪/` | Produce `追踪/` (`_tracking-state.json`, continuation state cards, chapter-by-chapter records, character snapshots, foreshadowing views, and dual-perspective timelines) |
| Character state | **Do not produce** character tracking | Produce `追踪/角色状态/{角色名}.md` for each core character, inferred by `character-state-reverse.md` |
| Outline system | **Do not produce** volume outlines or detailed chapter outlines | Produce `大纲/卷纲_第X卷.md` + `大纲/细纲_第N章.md` |
| Outline directory | **Do not produce** a `大纲/` directory | Produce it |
| Continuation handoff | story-short-write Phase 3 (scene-by-scene writing) | story-long-write daily-update loop |

---

## Mapping Overview

| Analysis artifact | Short-fiction project file | Conversion method |
|---------|------------|---------|
| Full source text (`拆文库/{导入书名}/原文/`) | `{标题}/正文.md` | Migrate to a single file and normalize it according to “正文.md Format Specification” below; do not rewrite its content |
| Story core / genre / structure fields in `拆文报告.md` | `{标题}/设定.md` (core-framework section) | Infer the book's core framework; do not inherit any self-benchmark registration that may appear in the report |
| Functional segments in `情节节点.md` | `{标题}/小节大纲.md` | Infer the section outline (opening/setup/escalation/reversal/ending segments; mark hook fields `[待补充]`) |
| `拆文报告.md` + `写作手法.md` | `{标题}/设定.md` (continuation-baseline section for this book) | Organize the existing structure, emotion, reversals, and established techniques into internal continuation context |
| `拆文库/{对标书名}/` | `{标题}/对标/{对标书名}/` | Optional: synchronize only an external reference work explicitly bound by the user |

---

## Rules for Inferring 设定.md

The target file uses the current core-framework template defined here, divided into two sections:

### Section One: Core Framework

Extract the story core, structural divisions, character analysis, and other fields from `拆文报告.md`, and populate this template:

```markdown
## 短篇核心框架

### 基本信息
- 标题：{导入书名}
- 目标字数：{原文实际字数} 字
- 目标平台：{从拆文报告提取，无则填 [待补充]}
- 情绪目标：{从拆文报告「情感线/爆点分析」提取读者预期感受}

### 一句话梗概
{主角 + 困境 + 反转 + 情绪落点（从拆文报告故事核提取）}

### 核心反转
- 反转类型：{从拆文报告反转分析提取：身份反转/视角反转/动机反转/时间线反转}
- 反转内容：{一句话描述}
- 铺垫线索：{从情节节点中的「铺垫」类节点提取，至少 3 个；不足时标 [待补充]}

### 情绪设计
- 开头情绪：{从情感曲线第一个节点提取}（强度 {1-10}）
- 中段情绪：{中段情感节点}（强度 {1-10}）
- 反转情绪：{反转节情感峰值}（强度 {1-10}）
- 结尾情绪：{结尾节情感}（强度 {1-10}）

### 人设速写
- 主角：{一句话人设，从人物分析提取}
- 关键角色：{一句话人设}
- 关系：{他们之间的关系}
```

> Add the `[待补充]` marker to every uncertain field; do not leave fields blank.

### Section Two: Continuation Baseline for This Book

Extract information from `拆文库/{导入书名}/拆文报告.md` and `写作手法.md`, then consolidate it into the internal continuation baseline for this book:

```markdown
## 本书续写基线

### 故事结构
{从拆文报告「功能分段」字段提取，概述各段功能}

### 情绪节奏
{从情感曲线/爆点分析提取，描述情绪走势与峰值位置}

### 核心反转机制
{从反转机制分析提取，含铺垫路径}

### 可复用写作手法
{从写作手法.md 或拆文报告「可复用结构」字段提取，≥3 条}
```

---

## Rules for Inferring 小节大纲.md

Extract the functional segmentation structure from `情节节点.md` and map it to the short-fiction segment-and-section structure.

### Segment-Level Mapping

| Short-fiction segment | Corresponding plot-node functional segment | Description |
|---------|----------------|------|
| Opening segment | Beginning (introduce protagonist/world/predicament) | Usually 1–2 sections |
| Setup segment | Early development (accumulate conflict / plant foreshadowing) | Usually 2–4 sections |
| Escalation segment | Late development (escalate conflict / deepen misunderstanding) | Usually 2–3 sections |
| Reversal segment | Climax (detonate the central reversal) | Usually 1–2 sections; emotional peak |
| Ending segment | Resolution (closure / emotional landing) | Usually 1–2 sections |

### Section-Entry Template

```markdown
## 开头段

### 小节 1
- 核心事件：{从情节节点提取该分段的主要情节点}
- 情绪目标：{对应情感曲线节点的情绪词}
- 章首钩子：[待补充]
- 章尾钩子：[待补充]
- 参考字数：{按原文对应段落字数估算}
```

> Mark hook fields `[待补充]`—they cannot be extracted reliably, so leave them for the user or for continuation writing.

### Estimating the Number of Sections

Use the source text's actual section markers and scene transitions. If the source has no explicit sections, divide it by plot phase and scene transition. Use `总字数 ÷ 1000` only as a rough reference, never as the basis for division. Agreement between the section count and the manuscript's actual paragraph structure is a mandatory quality-check item.

---

## 正文.md Format Specification

Migrate the source text into a single `正文.md` file and normalize it according to `format-and-structure.md`:

| Specification item | Requirement |
|--------|------|
| Section markers | `###1.` `###2.` `###3.` (general short-fiction format; when the user specifies a platform, switch according to the platform override table in `format-and-structure.md`) |
| Paragraph division | Break naturally by dramatic unit, shot, or completed event; do not force breaks at a fixed character count. Complete reasoning, atmosphere, and emotional chains may remain in somewhat longer paragraphs; avoid making every paragraph the same length or fragmenting prose into an outline |
| Spacing between paragraphs | Adjacent manuscript paragraphs permit **exactly one newline character `\n`**; do not use blank lines or `\n\n` |
| Dialogue quotation marks | Default to ASCII double quotation marks `""`; the Zhihu Yanyan platform may use `「」` |
| Indentation | No indentation; do not use full-width or half-width spaces |
| Markdown | Do not use Markdown syntax such as `**` `*` `#` `---` inside manuscript paragraphs (except for section markers) |

**Do not alter the source content**; perform formatting normalization only (paragraph breaks, quotation-mark unification, and addition of section markers).

---

## External Benchmark Reference View (Optional)

Only when the user explicitly binds an independent external `{对标书名}`, copy `拆文库/{对标书名}/` to `{标题}/对标/{对标书名}/` (skip `_archive_*/`; archived snapshots do not enter the benchmark view) for loading during continuation writing:

```
{标题}/对标/{对标书名}/
├── 原文/
├── 拆文报告.md
├── 情节节点.md
├── 写作手法.md
└── _meta.json
```

This view is optional and must not be created when there is no external benchmark. Before copying, confirm that the source is `拆文库/{对标书名}/`; never use `拆文库/{导入书名}/` or this story's `设定.md` to populate it.

---

## Quality Checklist

Run these checks after completing Phase 3-S migration:

- [ ] A single `正文.md` file exists and conforms to `format-and-structure.md` (section markers, paragraph division/subject rhythm, exactly one newline between paragraphs, and quotation-mark format)
- [ ] `设定.md` contains both the core-framework section and the continuation-baseline section for this book, and the core framework conforms to this file's template
- [ ] The number of sections in `小节大纲.md` matches the manuscript's actual paragraph structure
- [ ] All required `[待补充]` markers have been added (uncertain fields are not blank)
- [ ] Long-fiction-only directories such as `追踪/`, `大纲/`, and `正文/` were not created accidentally
- [ ] `拆文库/{导入书名}/` was not copied to this story's `对标/`; if an external benchmark is bound, its source matches the `对标/{对标书名}/` directory name
