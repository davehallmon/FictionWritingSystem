# Agent Reference Profile Contract

> This file is story-architect's sole reference inventory. The story-architect definition describes only task capabilities and does not duplicate the file list. After selecting `long` or `short` for a task, load only `Common + 当前 profile`. Do not read files outside the table even when they exist. Other agents use the reference tables in their own templates and rely on this file only for long/short selection rules and quality-coverage tables.

## Selection Rules

1. Select `long` when the parameters explicitly say “long-form,” “serialization,” “chapter outline,” or “daily update.”
2. Select `short` when they explicitly say “short-form,” “single story,” “section outline,” “Salt Selection,” or “mini-program short story.”
3. When the parameters are unclear, infer the profile from project artifacts: `大纲/细纲_第XXX章.md` and `追踪/` indicate long; `小节大纲.md` and a single-file `正文.md` indicate short.
4. When a new project has no artifacts, use the caller: genre positioning, core specifications, and outline tasks from story-long-write are `long`; ideation tasks from story-short-write are `short`.
5. If the profile remains unclear, return `Reference Profile: unresolved`. Never load both reference sets as a fallback.
6. Begin the output with `Reference Profile: long|short`. For reviews, select the profile of the work under review.

## Common

| File | Read when |
|---|---|
| [agent-quality.md](agent-quality.md) | Reviewing, scoring, or performing a pre-delivery check; provides only cross-genre quality standards, so also load the current profile's quality coverage |
| [genre-readers.md](genre-readers.md) | Determining the target reader, platform, and expectations |
| [emotional-arc-design.md](emotional-arc-design.md) | Designing or reviewing emotional arcs, expectation management, and payoffs |
| [plot-core-methods.md](plot-core-methods.md) | The writer is stuck, a plot cycle fails, or a five-step climax, transition, or daily outline lacks progression; for short-form work, use only methods compatible with the total length |

## Long Profile

| File | Read when |
|---|---|
| [long-genre-catalog.md](long-genre-catalog.md) | Positioning a long-form genre or checking frameworks |
| [long-genre-mechanics.md](long-genre-mechanics.md) | Extracting the core long-form hook, recurring mechanism, career line, or special advantage |
| [genre-prose-cards.md](genre-prose-cards.md) | Establishing long-form genre voice and long-range constraints |
| [outline-methods.md](outline-methods.md) | Building a master outline, volume outline, or chapter blueprint |
| [outline-conflict.md](outline-conflict.md) | Designing main and supporting plotlines, A/B plots, and conflict structure |
| [outline-rhythm.md](outline-rhythm.md) | Designing serialization rhythm, a sense of progression, and cross-chapter payoffs |
| [opening-design.md](opening-design.md) | Designing a new book's opening or opening three chapters |
| [long-emotional-methods.md](long-emotional-methods.md) | Designing the emotional engine and payoff chain for a cross-chapter story unit |
| [long-chapter-hooks.md](long-chapter-hooks.md) | Designing chapter openings, chapter endings, and cross-chapter expectations without fixed hundred-character quotas |
| [long-suspense.md](long-suspense.md) | Arranging short-, medium-, and long-term suspense and resolution cycles |
| [long-reversal.md](long-reversal.md) | Designing story-unit, volume-level, or complete-book reversals without rigid whole-story percentages |
| [long-quality.md](long-quality.md) | Reviewing the opening three chapters, serialization rhythm, reader contract, and endgame reserves |

The Long profile must not read `short-*` files or apply short-form defaults such as “six chapters,” “500–800 Chinese characters per section,” “one hook every two sections,” or “the climax must occur at 70–85% of the complete story.”

## Short Profile

| File | Read when |
|---|---|
| [short-genre-formulas.md](short-genre-formulas.md) | A structural skeleton for a short-form genre is needed |
| [short-paragraph-hooks.md](short-paragraph-hooks.md) | Designing paragraph retention, paywall breaks, and hooks within sections |
| [short-chapter-hooks.md](short-chapter-hooks.md) | Designing section-opening and section-ending hooks with high-density handoffs |
| [short-emotional-methods.md](short-emotional-methods.md) | Designing attachment, rupture, emotional tension, and resonance within one story |
| [short-suspense.md](short-suspense.md) | Arranging the central mystery, secondary mysteries, inter-section hooks, and complete-story resolution |
| [short-reversal.md](short-reversal.md) | Designing short-form clues, misdirection, reveal placement, and two-layer reversals |
| [short-quality.md](short-quality.md) | Reviewing complete-story density, paywall placement, reversal evidence chains, and ending payoffs |

The Short profile must not read `long-*`, `outline-*`, `opening-design.md`, or `genre-prose-cards.md`. Never apply volume-level, daily-update, or multi-dozen-chapter metrics as hard thresholds.
