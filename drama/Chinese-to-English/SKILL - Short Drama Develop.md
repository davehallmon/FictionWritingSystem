---
name: short-drama-develop
description: Develop Chinese novels, short-drama or motion-comic ideas, synopses, adaptation materials, existing series notes, or complete multi-episode screenplays into traceable adaptation plans, dramatic directions, creative briefs, director's statements, story engines, and episode maps, selecting approaches by genre and production form (visual style). Use when the user asks to “adapt a novel into a short drama,” “generate/complete an episode map from a full multi-episode script,” “develop a short drama/motion comic,” “create story settings/series outlines/episode plans,” “write a director's statement,” “explain how to write this genre,” “choose an art style/production form,” “turn this idea into a short drama,” or needs character conflicts and episode handoffs organized. An existing single-episode screenplay may proceed directly to writing, assets, or review without mandatory development files.
license: MIT
---

# Short-Drama Development

Turn the creator's intent into a story system that can continually generate **choices, costs, and state changes**. Preserve the creator's genre, ending, and scale decisions; do not use popular conventions as plot answers.

## Quick Start

Offline validation for precise indexing, slicing, and source-file change detection in complete multi-episode scripts:

```bash
python3 {技能目录}/scripts/selftest.py
python3 {技能目录}/scripts/episode_intake.py index <多集整稿> --out <episode-intake-index.json>
```

## Before Starting

This skill may be installed and run independently. First read materials explicitly supplied by the user and inputs directly relevant to the task. If the current directory is a
`short-drama` project and project tools are available, it may read `status` and use the release lifecycle, but the absence of the core
or any other skill does not block development work. [Stage Contract](references/stage-contract.md) provides this stage's boundaries, production-form inputs, and rule table; no other skill files need to be read.

## First Determine the Entry Point

1. **Only an idea, genre, or emotional target exists**: explore directions, then establish a creative brief and story engine.
2. **A synopsis, novel, adaptation material, or series notes exist**: preserve the source and first list committed facts, editable scope,
   source spans, and items requiring confirmation. For long material, first create semantic segments, a function ledger, and episode candidates. Do not publish episodes or assets
   directly from regex name/noun matches; do not alter the source meaning.
3. **Direction is established and only episode planning is needed**: read the existing brief and engine, then create or revise the episode map directly.
4. **A single-episode screenplay exists**: do not invent development material merely for workflow completeness. Route screenplay writing/revision to `$short-drama-write`; assets and later production may begin from the relevant skill.
5. **A complete multi-episode screenplay exists and an episode map must be generated or completed**: preserve the source file and load only
   [Multi-Episode Intake and Resumption](references/multi-episode-intake.md). The Agent determines boundaries and the current batch from the file's actual structure.
   Tools perform only exact indexing, single-episode slicing, validation, and resumption—not creative judgment.

Work directly when information is sufficient. Ask questions only when a gap would change the protagonist, conflict engine, ending promise, or adaptation boundary.

## Every Execution

### 1. Lock the Creator Contract

Read creator inputs and accepted files, distinguishing:

- Immutable facts, themes, characters, and ending promises;
- Gaps open to exploration;
- Format constraints and production boundaries;
- Emotional, informational, or power payoffs the target audience can receive repeatedly.

For a new project, copy [creative-brief.md](assets/creative-brief.md). If changing accepted facts, first display the semantic delta and downstream impact rather than overwriting directly.

### 2. Explore Genuinely Different Directions

When direction is undecided, propose a small number of candidates with **different mechanisms**: change the protagonist's strategy, source of opposition, cost, or means of sustaining conflict—not merely title, profession, or wording. When direction is clear, deepen it directly; do not manufacture false alternatives to fill a list.

For each candidate, explain the dramatic promise, protagonist's pursuit, opposition mechanism, recurring payoff, state that can escalate, long-term termination condition, and main production burden. Let the creator choose or combine candidates and record the reason; rejected directions do not become established facts.

When the full method is needed, read [story-craft.md](references/story-craft.md). When the genre is established, retrieve **one** genre card by index from
[genre-cards.md](references/genre-cards.md) to calibrate common pressure sources, scene granularity, and production burden. It is reference material the creator may override in one sentence; it neither replaces direction selection nor enters deliverables.

If the protagonist begins with an experience that already happened or receives powers from an externally authorized rule system, that is a
**premise device** layered over the genre. Also read [premise-devices.md](references/premise-devices.md)—because a device removes resistance,
it needs boundaries and costs first. A device does not replace the genre card or create its own genre.

### 3. Establish the Story Engine

Copy [story-engine.md](assets/story-engine.md) and specify:

- How pressure appears and how the protagonist normally responds;
- How an opponent or system counters, and why the protagonist cannot leave easily;
- What changes in each conflict cycle, rather than how the same conflict becomes louder;
- Each character's goals, leverage, boundaries, and relationship pressure;
- Which character change or factual revelation will terminate the engine;
- Visual, sound, scene-scale, and content boundaries.

For serialized stories, long-form adaptations, or substantial longitudinal character change, also read
[serial-character-and-memory.md](references/serial-character-and-memory.md). First create a backstory reserve used only for author decisions, choose the narrative entry window where an old strategy begins imposing costs, then record each character's
defended belief, pressure tests, information permissions, and cross-episode memory. Do not pour the backstory reserve directly into Episode 1 dialogue.

### 4. Translate Series Movement into Episodes

Read [episode-design.md](references/episode-design.md), then copy [episode-map.jsonl](assets/episode-map.jsonl). For every episode, record entry state, opening, episode pursuit, resistance, directional turn, episode outcome, information release, outgoing pressure, and facts the next episode must inherit.

First ensure that every episode produces a local dramatic result and adjacent episodes hand off precisely; only then discuss dual-track
rhythm between external pressure and emotional load. Episode count, hook type, use of reversal, and climax position are creator/project choices.

### 5. Perform Owner Checks and Handoff

Before presenting the commit preview, verify:

- Referenced episodes, setups, and payoff records can be found, and unresolved items are explicit;
- Candidates genuinely change mechanisms, and the selected direction runs through the brief, engine, and episode map;
- Every escalation identifies a change in power, information, relationship, exposure, resources, time, or cost;
- Every episode first pays off part of its local promise, then leaves a specific decision, danger, or question;
- Formatting preferences have not been presented as universal rules.

These are owner self-checks, not final review. Display a creator-readable summary of additions/changes and request acceptance before using them as downstream sources.
When a quality verdict is needed, request `$short-drama-review` separately, preferably executed by a reviewer uninvolved in creating the current version.

If the project needs a director's statement, this skill creates only a `项目开发/director-brief.md` candidate and identifies the
`visual_direction` / `production_profile` semantic delta it proposes. After creator acceptance,
`$short-drama` routes the selection into creator authority; the development skill does not directly rewrite that authoritative configuration.

## Rule Levels

- **`structural_invariant`**: locally provable references, IDs, and explicit-state contradictions; validators may block.
- **`reviewed_invariant`**: semantic obligations such as whether escalation is real or a promise is paid off; reviewers judge using cited evidence.
- **`craft_default`**: practices that usually help; the creator may override them with an explanation.
- **`taste_option`**: choices such as hooks, arcs, viewpoint, and ending tone; these must not block by themselves.

Do not replace causal judgment with fixed plot points, turn timing, length percentages, or count formulas.

## Artifacts and Boundaries

This skill owns only:

- `项目开发/creative-brief.md`
- `项目开发/story-engine.md`
- `项目开发/director-brief.md` (when required by the project; candidate for creator authority only)
- `项目开发/adaptation-map.jsonl` (for long-material adaptations; retains only input locators/spans,
  de-quoted functional summaries, candidate destinations, and unresolved items without copying source text; see
  [adaptation-map.example.jsonl](assets/adaptation-map.example.jsonl))
- `项目开发/series-arc.json` (when required by the project)
- `项目开发/episode-intake-index.json` (when ingesting a complete multi-episode screenplay; a rebuildable mechanical index, not creative truth)
- `项目开发/episode-map.jsonl`

It does not write scene action or dialogue, extract assets, write image/video prompts, generate media, or issue final-review conclusions. `$short-drama-write` owns screenplay semantics.

## Load on Demand

- **Promise, engine, character pressure, escalation, setup, and payoff**: [story-craft.md](references/story-craft.md)
- **Episode contract, causal beats, inter-episode handoff, and map revision**: [episode-design.md](references/episode-design.md)
- **An existing complete multi-episode screenplay/scattered drafts that must not enter context all at once and must support interruption/resumption**:
  [multi-episode-intake.md](references/multi-episode-intake.md)
- **Character drive, backstory and entry point, cross-episode change, information permissions, dual-track rhythm, and memory recovery**:
  [serial-character-and-memory.md](references/serial-character-and-memory.md)
- **Source material requiring compression/character or scene merging/information visualization**:
  [adaptation-craft.md](references/adaptation-craft.md)
- **A creator-supplied benchmark work, sample screenplay, or prompt whose mechanism should be learned without imitating expression**:
  [creative-reference-intake.md](references/creative-reference-intake.md)
- **A unit story repeatedly runs the same mechanism, or its middle begins repeating and thinning**:
  [mechanism-loop.md](references/mechanism-loop.md)
- **Distinguishing revelation, reversal, payoff, and hook, or selecting pressure mechanisms by genre**:
  [reveal-reversal-payoff.md](references/reveal-reversal-payoff.md)
- **Qualitative case methods for selecting conflict progression, designing openings, or planning episode-ending hooks by genre**:
  [genre-and-hook-playbook.md](references/genre-and-hook-playbook.md)
- **An established genre requiring common pressure, scene granularity, hook direction, and production challenges**:
  [genre-cards.md](references/genre-cards.md) (index and retrieval specification; read one card only)
- **The protagonist begins with a known outcome or receives an externally authorized ability**:
  [premise-devices.md](references/premise-devices.md) (device layer, added over the genre card)
- **Drafting project-level visual direction and production rules (director's statement)**:
  [director-brief-craft.md](references/director-brief-craft.md)
- **What this stage owns, inherits, and must not overreach**: [stage-contract.md](references/stage-contract.md)
