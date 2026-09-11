---
name: output-contract
description: |
  Output contract for story-short-analyze. Defines the Stage → file mapping, the _meta.json schema,
  and downstream consumption rules (story-short-write reads the complete Markdown set + source text + _meta.json to write a new short story).
sync-policy: |
  This file must remain byte-equal between story-short-analyze and story-short-write.
  After modifying either copy, synchronize the other and verify with bash scripts/check-shared-files.sh.
  Do not add this file to the IGNORE_NAMES list—it must remain synchronized and is not an intentional difference.
---

# Output Contract: story-short-analyze ↔ story-short-write

After `story-short-analyze` deconstructs a short story, it saves the artifacts to `拆文库/{书名}/`. When
`story-short-write` writes another short story in the same genre, it reads **all** output in this directory together.

---

## Output Directory and File Tree

```
拆文库/{书名}/
├── 原文/                  # 管道前置步骤产出，存放源文件备份
├── 拆文报告.md             # 人类可读综合报告（Stage 2-6 综合）
├── 情节节点.md             # Stage 2 情节节点清单
├── 写作手法.md             # Stage 4 写作手法分析
└── _meta.json             # 管道元数据 + 结构计数（resume + 验收数值依据）
```

**Filename convention**: `拆文报告.md / 情节节点.md / 写作手法.md` are hard-coded for consumption by
`story-short-write` and cannot be renamed. Analytical narrative goes in Markdown; numbers and enums go in `_meta.json.structure_counts`.

---

## Stage → File Mapping

| Stage | Name | Output File | Primary Content |
|-------|------|----------|---------|
| 2 | Structure + plot points | `拆文报告.md` (story core / structure / synopsis sections) + `情节节点.md` | Story core / 4–6-part structure / story synopsis / plot-point list |
| 3 | Emotional arc + explosive moments | `拆文报告.md` (emotional-curve + explosive-moment sections) | Emotional curve with ≥5 nodes / six dimensions of explosive moments / anticipation |
| 4 | Reversals + writing techniques | `拆文报告.md` (reversal section) + `写作手法.md` | Preliminary reversal check / reversal analysis (setup ≥2) / ≥5 writing techniques |
| 5 | Characters + opening and ending | `拆文报告.md` (character + opening/ending sections) | Character categories + function assessment / opening analysis / ending analysis / opening-ending correspondence |
| 6 | Comprehensive evaluation | `拆文报告.md` (comprehensive section) + `_meta.json` (writes structure_counts) | Five-dimensional score / explosive potential / discussion potential / ≥3 layers of resonance / ≥3 reusable structures / pacing brief |

---

## `_meta.json` Schema

`_meta.json` contains pipeline metadata + structural counts. It **does not contain analysis**, only numbers and enums used for completeness validation during acceptance. All analytical narrative belongs in `拆文报告.md`.

```jsonc
{
  "version": "2.0",
  "word_count": 5234,                   // 源文字数（Phase 1 探针填入）
  "genre_detected": "追妻",             // Phase 1 题材识别；未识别填 "通用"
  "created_at": "{ISO8601 时间戳}",      // 拆文启动时间，写入时填当前 UTC
  "stages_completed": [2, 3, 4, 5],     // 已完成 Stage，按完成顺序 append
  "last_stage_in_progress": null,       // 当前正在执行的 Stage；空闲为 null

  "structure_counts": {                 // Stage 6 完成时一次性写入；structure_counts 数值校验依据
    "beats": 5,                         // 结构段数（结构划分，开端/发展/高潮/结局，Stage 2）
    "hooks": 4,                         // 钩子数（Stage 3）
    "setup_clues": 3,                   // 反转铺垫线索数（Stage 4）
    "character_archetypes": 3,          // 有反差人物数（Stage 5）
    "reusable_structures": 3,           // 可复用手法条数（Stage 6）
    "reversal_type": "视角反转"          // 反转类型枚举（视角/身份/动机/时间线/信息/认知/无反转）；甜宠/喜剧/报应型填「无反转」
  }
}
```

### Write Order (Crash Safety)

1. **Before Stage N starts**: Set `last_stage_in_progress = N` and write to disk.
2. **After writing the Stage N files**: Run a non-empty + minimum-reasonable-length check (for example, the new section in `拆文报告.md` is ≥ 200 Chinese characters).
3. **On success**: Clear `last_stage_in_progress` and append `N` to `stages_completed[]`.
4. **On failure**: Leave `stages_completed` unchanged and retain `N` in `last_stage_in_progress`.
5. **Additional action when Stage 6 finishes**: Calculate `structure_counts` once and write it to `_meta.json`,
   then proceed to acceptance.

### Resume Protocol

- If `last_stage_in_progress` is nonempty → the Stage was interrupted previously; rerun it **from the beginning** without reusing partial output.
- If `last_stage_in_progress` is empty → begin with `max(stages_completed) + 1`.
- If `stages_completed` contains 6 → the process is complete; ask the user whether to overwrite or cancel.

**Stage 6 = content complete AND acceptance passed**. Until acceptance passes, `last_stage_in_progress` remains `6` and `stages_completed` does not contain `6`. On resume, the main text and structure_counts are already on disk, so rerun only the acceptance checks without rewriting the Stage 6 content.

---

## Acceptance Integration Point

After the Stage 6 content is complete but before appending `stages_completed[6]`, run three checks:

### Step 1: AI-Tone Self-Check for the Deconstruction Report

Scan all of `拆文报告.md` against the prohibited-word list and report-specific AI-tone rules loaded locally by the deconstruction workflow.
This is the quality gate for the deconstruction report. The drafting workflow maintains its own anti-AI rules inside its Skill; do not read reference files across Skills or mix the two rule sets.
On a hit → do not write `stages_completed[6]`. List the locations and ask the user to revise the **deconstruction report itself**
(source-text AI tone does not count—the scan targets the analyst-written report).

### Step 2: Numeric Validation of `_meta.json.structure_counts`

| Field | Minimum | If Below |
|------|--------|--------|
| `structure_counts.beats` | ≥ 4 (structural segments: opening / development / climax / ending) | Block |
| `structure_counts.hooks` | ≥ 3 | Block |
| `structure_counts.setup_clues` | ≥ 3 (skip this row when reversal_type=无反转) | Block |
| `structure_counts.character_archetypes` | ≥ 2 | Block |
| `structure_counts.reusable_structures` | ≥ 3 | Block |
| `structure_counts.reversal_type` | Included in the enum (including 「无反转」) | Block |
| `genre_detected` | Nonempty | Block |

> No threshold applies to the number of plot points. Extract them according to the semantic-change boundaries in `情节节点.md` (see material-decomposition.md); they do not belong in this table. `beats` counts structural segments, not plot points.

### Step 3: Scan `story-short-analyze` BLOCK Items

Scan the output templates loaded locally by the deconstruction workflow and confirm that every output section marked `[BLOCK]` appears in `拆文报告.md`.
Any omission → block. Any `[WARN]` item → write it to the “待补” list at the end of the deconstruction report without blocking.

### Step 4: Pass

Clear `_meta.json.last_stage_in_progress`, append `6` to `stages_completed[]`, and tell the
user, “Deconstruction complete. You can call `/story-short-write` to write the next story.”

---

## Downstream Consumption Rules (How story-short-write Uses the Output)

> `story-short-write` currently hard-codes reads of the three Markdown files `拆文报告.md / 情节节点.md / 写作手法.md`.
> `_meta.json` is an optional enhancement: tolerate it during reads, and do not block drafting if it is absent.

| File | Role | How to Read It |
|------|------|--------|
| `_meta.json` (optional) | Numeric summary + genre detection | Use `genre_detected` to choose the genre benchmark, read `structure_counts` to confirm deconstruction completeness, and use `structure_counts.reversal_type` to select the reversal framework |
| `拆文报告.md` | Main analytical narrative | Read the “故事核,” “结构,” “情感曲线,” “爆点,” “反转分析,” “人物,” “五维评分,” “共鸣分析,” “可复用结构,” and “同类型写作动作” sections; this is the writer’s primary input |
| `情节节点.md` | Pacing anchors | Use each node’s character-count position + function + triggering event to pace the new story |
| `写作手法.md` | Technique library | Specific techniques for POV / dialogue / time / information control and more + source examples to reuse in the new story |
| `原文/` | Source of stylistic feel | Copy the dialogue tone, pace, imagery, and tension of reversals. **Do not copy specific plot events**; copy the technique. |

### Suggested Writing Workflow

1. Use `_meta.json.genre_detected` and `structure_counts.reversal_type` to choose a framework.
2. Read the “核心手法,” “共鸣分析,” and “可复用结构” sections of `拆文报告.md` to decide what to retain or adjust.
3. Read `情节节点.md` and map its pacing anchors onto equivalent character-count positions in the new story.
4. When writing scenes, consult `写作手法.md` + `原文/` for specific techniques.
5. After writing, optionally add `derived_from: 拆文库/{书名}/` to the new document’s frontmatter for traceability.

### Local Maintainer Smoke Test

```bash
ls 拆文库/{书名}/   # 应有：原文/ 拆文报告.md 情节节点.md 写作手法.md _meta.json
/story-short-write 拆文库/{书名}/
# 通过：输出 8000+ 字同题材新短篇，prose 有源文对话节奏和画面感
# 失败：写得像填空 / 或 short-write 找不到三个 markdown
```

---

## Versioning Conventions

- `_meta.json.version` is coupled to this file’s `sync-policy`.
- A breaking change (renamed field / changed type / changed required field) must bump the major version and synchronize both
  copies; CI uses `scripts/check-shared-files.sh` to catch one-sided changes.
- An additive change (new optional field) may bump the minor version; the producer, consumer, and both copies must upgrade to the current schema in the same change.
