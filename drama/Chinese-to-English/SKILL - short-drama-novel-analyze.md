---
name: short-drama-novel-analyze
description: Break a long novel, serialized web novel, or scattered multi-episode drafts into traceable source analysis: a chapter index, rapid adaptation-value triage, chapter-by-chapter functional extraction, story-unit and pacing aggregation, and consolidated characters and settings. Finish with an adaptation-value judgment and episode candidates to hand off to $short-drama-develop for contract creation. Use when the user says “import this novel,” “break down this book,” “analyze the source,” “can this book become a short drama,” “first see whether it is worth breaking down,” or “turn this long work into episode candidates,” or directly provides a novel file path. Performs read-only structured analysis only; does not write screenplays, create assets, generate media, or decide the adaptation approach for the creator.
license: MIT
---

# Long-Form Source Analysis

Turn a long source work into an analysis layer that **can be cited, challenged, and used downstream**. The goal is not to retell the plot, but to identify the dramatic function of each passage and explain its value in a vertical short drama.

The analysis always produces candidates. The creator decides which threads to preserve, which characters to merge, and where to begin. `$short-drama-develop` formalizes those decisions as the adaptation contract. This skill neither makes those decisions for it nor approves its own output.

## Quick Start

Validate the chapter index, sampling, and source-file change detection offline:

```bash
python3 {技能目录}/scripts/selftest.py
python3 {技能目录}/scripts/novel_index.py index <原著.txt> --out <chapter-index.json>
```

**English guide (non-executable):** Replace `{技能目录}` with the skill directory and `<原著.txt>` with the source-novel text file.

## Before Starting

This skill can be installed and run independently. First read the source work explicitly supplied by the user and the direct inputs to this task. If the current directory is a `short-drama` project and the project tools are available, you may read `status` and use its publishing lifecycle, but missing core or any other skill does not block analysis. See the [Stage Contract](references/stage-contract.md) for the full boundaries and rules; no files from other skills need to be read.

## Material Requirements

Analyze only works the creator **lawfully possesses or has the right to use**. Analysis is a read-only transformative activity: extract structure and function without reproducing source passages or carrying original sentences into downstream outputs.

Violence, revenge, betrayal, romantic tension, and dark ethical material are ordinary fictional narrative elements in popular genres; extract their structure normally. If an individual passage cannot be processed, skip and record it rather than stopping the chapter or the whole book. Stopping would give every downstream stage an analysis with invisible holes.

## Determine the Entry Point First

1. **Title only, no source text**: ask the creator for a file path or pasted text. Do not reconstruct the plot from the title—without bytes there is no span, and analysis without spans can neither be cited nor challenged.
2. **Source text exists, project does not**: create a workspace owned by this skill containing at least the read-only input directory
   `输入/` and output directory `项目开发/source-analysis/_work/`. Copy the original bytes into `输入/`, record the original file location, and build the index with this skill’s `novel_index.py`. If `$short-drama` is available, it may optionally initialize the same directories and publishing lifecycle, but core installation must not become a prerequisite for beginning analysis.
3. **Source text and project both exist**: enter the pipeline directly.
4. **Partial analysis already exists**: read `项目开发/source-analysis/_progress.md` and resume from the checkpoint without rerunning completed stages.

## Pipeline

`输入/` contains immutable creator inputs and is read-only during this stage. All outputs go under `项目开发/source-analysis/`.
Independent workspaces and full projects use the same relative paths, so installing core later does not require migrating analysis artifacts.

| Stage | Work | Output | Gate |
|---|---|---|---|
| S0 | Build chapter index (script) | `_index.json`, `_progress.md` | Stop if the index has problems |
| S1 | Rapid adaptation-value triage (sampled) | `triage.md` | **Pause and ask the creator** |
| S2 | Extract chapter functions | `chapters/ch-<N>-extract.md` | Stop if coverage is insufficient |
| S3 | Aggregate story units and pacing | `story-units.md`, `rhythm-and-emotion.md` | Recheck when thresholds fail |
| S4 | Consolidate characters and settings | `characters.md`, `world.md` | — |
| S5 | Adaptation value and episode candidates | `adaptation-value.md`, `episode-candidates.jsonl` | Hand off to develop |

### S0 Chapter Index

The index is the **single source of truth for slicing**, built by the [chapter-index script](scripts/novel_index.py). If every stage runs its own regular expression, chapter boundaries will disagree: Chapter 47 will be analyzed using one boundary and aggregated using another, and nobody will notice.

```bash
python3 {技能目录}/scripts/novel_index.py index 输入/{原文文件} \
  --out 项目开发/source-analysis/_work/_index.next.json
python3 {技能目录}/scripts/novel_index.py verify \
  项目开发/source-analysis/_work/_index.next.json 输入/{原文文件}
# 项目工具可用时可选：
python3 {core 技能目录}/scripts/project_tool.py publish {项目根} \
  --owner short-drama-novel-analyze --artifact-id source-analysis:index \
  --output 项目开发/source-analysis/_index.json=项目开发/source-analysis/_work/_index.next.json \
  --input 输入/{原文文件}
```

**English guide (non-executable):** The protected paths mean: source file under `输入/`; temporary and accepted indexes under `项目开发/source-analysis/`; project root at `{项目根}`. The comment marks the `project_tool.py publish` step as optional when the project tool is available.

The script recognizes Arabic and Chinese chapter numbers—including 千 / 两 for serials exceeding a thousand chapters—and recognizes **only one numbering unit**: whichever of 章/回/节 occurs most often. It records the others under `ignored_heading_units`. It treats only **short standalone lines** as headings, records prose paragraphs beginning with chapter numbers in `long_heading_lines_skipped`, removes opening table-of-contents blocks, and validates numbering separately by volume. It **does not make editorial judgments** about which chapter matters or what happens in it; those belong to later stages.

If `problems` is nonempty, stop and report it rather than carrying a bad table into S1. The four common problems are skipped chapter numbers (a missing chapter or false heading match), duplicate numbers within one volume, chapters with very little body text (usually residual table-of-contents entries or volume title pages), and unparseable chapter numbers.
Also verify three counts: `chapter_unit` and `ignored_heading_units`. A book divided by `第N章` with subsections marked `第N节` should report `chapter_unit: 章` and count `节` as ignored; the reverse result indicates that the chapter unit was inferred incorrectly. If `long_heading_lines_skipped` is unusually high, the book probably has genuinely long chapter headings; confirm with the creator before writing boundaries manually.

If the source has no chapter headings, the index will return an empty table. Confirm the slicing method with the creator, write the boundaries into
`_work/_index.next.json`, and publish them through the lifecycle above after they pass `verify`. Manually authored rows must still contain
`sequence` / `line_start` / `line_end`; `verify` checks each row and reports missing fields.

Whenever the source text changes, rebuild the index rather than reusing old spans. `verify` checks numbering, order, and line-number coverage, so inserted and deleted lines are detected. It cannot detect an in-place rewrite that keeps the same line count; the person changing the source must rebuild the index, because the toolkit does not compare bytes.

```bash
python3 {技能目录}/scripts/novel_index.py verify \
  项目开发/source-analysis/_index.json 输入/{原文文件}
```

### S1 Rapid Adaptation-Value Triage

Answer **whether this book warrants the cost of a full breakdown**. The criterion is its overall adaptation density: how much is `screen_ready`, how much is `prose_only`, and where the production burden is concentrated. The triage therefore spans the entire book using script-based sampling:

```bash
python3 {技能目录}/scripts/novel_index.py sample \
  项目开发/source-analysis/_index.json --count 12
```

The sample is deterministic and reproducible, always includes the beginning and end, and cites the same chapters when run again. Following
[Adaptation-Value Triage](references/adaptation-triage.md), write `triage.md` covering six items: story framework, proportions of the three classifications, opening replacement point, scale of the production burden, the three largest adaptation risks, and the approximate number of episode candidates.
The first line states coverage using the script’s `coverage_ratio`; limit every conclusion to the sampled scope.

**Pause here and ask the creator**: present the triage and an estimated duration for the full breakdown, roughly based on chapter count, then ask whether to proceed.
If the creator explicitly requested “run everything in one pass” at the outset, still write `triage.md` but do not pause. S5 needs it as the initial hypothesis to revisit.

At the pause, set `_progress.md` to `paused_after_triage` and record the checkpoint as “next: S2 chapter extraction.”

Agent-authored artifacts in S1–S5 likewise go first to `source-analysis/_work/`, and are published to the formal paths in the table only after the stage passes its mechanical checks. When project tools are available, use `project_tool.py publish` with a stable artifact ID; when running independently, atomically replace the formal file. Do not overwrite `_index.json`, `_progress.md`, `chapters/*.md`, or aggregate outputs with partial work.
`_work/` is a candidate workspace, not the authoritative analysis layer, and is not included in delivery packages.

**Concurrent subagents write to `_work/`; the main thread publishes to the formal paths**. Subagents write only
`_work/chapters/ch-<N>-extract.md`. After mechanical checks, the main thread publishes them to `chapters/`.
The coverage gate matches filenames under the formal `chapters/` path. If it runs before publication, every chapter appears under
`unmatched_files`; that is not a defect, merely an early check.

Every stage rewrites `_progress.md`, while publishing requires one owner per path. Therefore it uses one fixed
artifact ID, `source-analysis:progress`, owned by `short-drama-novel-analyze`, and republishes that same ID at every S0–S5 gate.

### S2 Chapter-by-Chapter Functional Extraction

Process every chapter using [Chapter Extraction](references/chapter-extraction.md). When concurrent subagents are supported, dispatch them in batches
of 5–8 chapters and wait for each batch to land before sending the next. Otherwise process them serially. Both paths use the same writing requirements and self-checks; only their speed differs.

Write each completed extraction to `chapters/ch-<N>-extract.md`, where `<N>` is the index `sequence`, not the source chapter number
(source chapter numbers can repeat across volumes; sequence values cannot). After every file has landed, run the coverage check:

```bash
python3 {技能目录}/scripts/novel_index.py coverage \
  项目开发/source-analysis/_index.json 项目开发/source-analysis/chapters
```

If `missing` is nonempty, rerun the missing chapters. A nonempty `unmatched_files` means filenames are malformed; they do not count toward coverage and are not treated as missing, so rename them rather than rerunning them. **Do not proceed to S3 with incomplete coverage**. Aggregation will still produce a result that reads as complete, while omitted chapters leave no trace anywhere.

After two consecutive failures on one chapter, mark it skipped, record the failure in `_progress.md`, and note the missing chapter in every later aggregate output. Failure is acceptable; hiding failure is not.

### S3 Story Units and Pacing

Aggregate from the chapter extractions without rereading the source. S2 has already read the source once; reading it again only creates a second, contradictory set of facts. Following [Aggregation and Entities](references/aggregation-and-entities.md), identify the story framework first
(the framework determines how units are sliced), then produce:

- `story-units.md`: group plot points into complete units and record the entering state, conflict, cost, and exiting state of each;
- `rhythm-and-emotion.md`: show how key information advances chapter by chapter, the setup → release → aftermath of emotional triggers,
  and cross-chapter foreshadowing and payoffs.

After aggregation, run the three threshold checks in the same document—assignment confidence, coverage, and overlap—and the unassigned-plot fallback.
Thresholds are not scores; they are **signals of unclear boundaries**. Excessive overlap means that two units are actually one.

### S4 Characters and Setting

Following [Aggregation and Entities](references/aggregation-and-entities.md), consolidate characters through cross-chapter deduplication, alias normalization, and tiering, then infer world rules, power systems, and factions from mention data. Merge aliases only when they are proper names or nicknames supported by coreference evidence. Descriptive labels and titles **never trigger a merge**.

**Character consolidation produces candidates, not assets**. Character entries here carry `unresolved` markers and source citations.
Pass them to `$short-drama-develop` for adaptation decisions; after `$short-drama-write` places them in the screenplay,
`$short-drama-assets` may establish true asset identities from the accepted screenplay. Skipping this chain and creating assets directly would let the source novel’s character list masquerade as evidence of screenplay appearances.

### S5 Adaptation Value and Episode Candidates

This is where this skill diverges from a general book breakdown. Following [Adaptation Value](references/adaptation-value.md), produce:

- `adaptation-value.md`: identify units that work directly in vertical short drama, those requiring a change of medium, and forms of purely literary pleasure
  (interiority, narrative tricks, extended setup) that cannot be realized visually; state where the production burden falls.
- `episode-candidates.jsonl`: candidates divided by **local dramatic outcome and exact handoff**, not evenly by chapter number or word count.
  Every entry includes source spans, its function, and unresolved items.

Also **revisit the triage**: at the beginning of `adaptation-value.md`, record which S1 judgments the full results overturned.
A disproven sampling conclusion is more useful than one silently forgotten; it makes the next book’s triage more accurate.

See [Episode Candidate Example](assets/episode-candidate.example.jsonl).

### Handoff

After S5, show a creator-readable summary stating how many chapters were broken down, which were skipped, how many episode candidates were created,
the three largest adaptation risks, and which triage judgments were overturned. Then hand off to `$short-drama-develop`, which converts the candidates into `项目开发/adaptation-map.jsonl` and an adaptation contract.

**This skill does not write `adaptation-map.jsonl`**; that belongs to develop. For quality conclusions, hand off to the independent
`$short-drama-review` with scope `source_analysis`.

## Rule Levels

- **`structural_invariant`**: provability of the index and spans, citation completeness, and coverage. Scripts may block on these.
- **`reviewed_invariant`**: semantic duties such as whether functional extraction is faithful to the source and consolidation preserves dramatic function.
- **`craft_default`**: normally helpful practices that the creator may override with a stated reason.
- **`taste_option`**: choices such as where to begin or which thread to retain; these must never block on their own.

Do not substitute fixed chapter-count formulas, plot-point counts, or length ratios for causal judgment.

## Artifacts and Boundaries

This skill owns only the following files under `项目开发/source-analysis/`: `_index.json`, `_progress.md`,
`chapters/*.md`, `triage.md`, `story-units.md`, `rhythm-and-emotion.md`,
`characters.md`, `world.md`, `adaptation-value.md`, and `episode-candidates.jsonl`.

It does not rewrite `输入/`, write artifacts owned by other skills under `项目开发/`, create assets, write scenes or dialogue,
write prompts, generate media, or issue final-review decisions.

**Do not copy source passages into the analysis**. Record locators, spans, and de-quoted functional summaries. When evidence is necessary, quote only the shortest required fragment. Delivery packages must not carry the original material beyond its boundary.

## Language

Analysis artifacts are creator-facing: inside a project they follow `short-drama.json#/language`; in standalone operation they follow the user’s language.
Do not hardcode a language in this skill. This skill does not produce prompt bodies and is unrelated to
`#/format/prompt_language`.

## On-Demand Loading

- **Which chapters triage reads, the six required items, and how not to impersonate full analysis**: [Adaptation-Value Triage](references/adaptation-triage.md)
- **Chapter-extraction format, the boundary between objective description and narrative-framework terms, mechanical checks, concurrent and serial execution**: [Chapter Extraction](references/chapter-extraction.md)
- **Story frameworks, story units, pacing and emotion, character consolidation, thresholds, and the unassigned fallback**: [Aggregation and Entities](references/aggregation-and-entities.md)
- **Adaptation-value assessment, medium substitution, and episode-candidate slicing**: [Adaptation Value](references/adaptation-value.md)
- **What this stage owns, inherits, and may not overstep**: [Stage Contract](references/stage-contract.md)
