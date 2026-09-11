# Core Quality Standards for All Agents

> Contains only judgments that apply to both long- and short-form fiction. During review, use `agent-reference-profiles.md` to load the quality-coverage file for the current profile. This file does not define thresholds for length, density, or reveal placement.

## Narrative-Unit Progression

- [ ] The unit changes at least one of the following: objective, risk, information, relationship, resources, identity, or emotional position.
- [ ] Removing the unit causes an identifiable loss of causality, characterization, or expectation. Classify it as possible padding only when no such loss can be identified.
- [ ] The opening continues the current objective or introduces a meaningful anomaly; it does not use functionless weather, scenery, or routine as padding.
- [ ] The ending lands on a decision, discovery, consequence, relationship change, or unfinished action rather than substituting authorial summary for change.
- [ ] The strength of progression follows the current profile, genre, and established payoff rhythm. Do not impose a fixed character count across genres.

## Information and Scenes

- [ ] Every scene has an objective, an obstacle, and a changed state at its conclusion.
- [ ] Worldbuilding emerges through action, conflict, or evidence rather than consecutive explanatory passages.
- [ ] Characters make choices, act, or endure consequences instead of repeating the same feeling across several paragraphs.
- [ ] The number of new concepts matches the current scene's cognitive load. Give necessary concepts verifiable boundaries of use.

## Language and Format

- [ ] Dialogue reflects identity, relationships, and the current balance of power; individual characters remain distinguishable.
- [ ] Choices, dialogue, objects, or actual consequences support abstract emotions. State an emotion directly when that is more accurate.
- [ ] The prose contains no empty summaries, consecutive formulaic rhetoric, or stacked physical reactions used merely to appear polished.
- [ ] Outside the title line, do not mix writing-engineering metadata such as “this chapter,” “detailed outline,” “foreshadowing,” or “reader” into the manuscript. Genuine in-world uses are exempt.

## Five-Dimension Scoring

Score every dimension from 0 to 100. Every score requires evidence and a description of the consequence of failure; do not score from overall impression.

### Core Consistency

Check whether central conflicts, actions, character motives, and ownership of rewards remain consistent.

| Problem | Severity | Fix |
|---|---|---|
| A character's motive changes suddenly without a trigger | critical | Add a trigger or revise the action |
| The central conflict changes inconsistently | high | Trace back and unify the conflict definition |
| A crucial action contradicts established characterization | high | Revise the action or add a visible cause |
| A secondary conflict is forgotten | medium | Resolve it, defer it with a traceable marker, or explicitly reduce its importance |

### Surface Rewrite Quality

Check whether wording is natural, copies the shape of the input, or relies on generic phrasing. Do not force changes to sound source sentences merely to increase a “rewrite rate.”

| Problem | Severity | Fix |
|---|---|---|
| Copying outline or reference sentences produces an unnatural voice | medium | Preserve the facts while restructuring the narrative form |
| AI-signaling words, isomorphic sentences, or explanatory tails appear in clusters | high | Replace them with concrete actions, evidence, or relationship consequences |
| Diction, metaphors, or physical reactions accumulate | medium | Remove nonfunctional material and preserve character-specific detail |

### Format Consistency

Check whether paragraphs break naturally by dramatic unit, quotation marks and chapter markers follow project conventions, and target length uses the current workflow's deterministic measurement standard.

### Readability

Check for verbosity, disordered information, circular interiority, or ornate phrasing that obscures important causality. Do not compress a monologue by sentence count when it delivers new information, a decision, or an emotional turn.

### Logical Coherence

Check whether worldbuilding, chronology, character knowledge, the evidence chain, and “cause → action → result → consequence” form closed loops. Mark insufficient evidence explicitly rather than inventing specifications for the author.

## Severity and Remediation Strategy

| Level | Determination | Action |
|---|---|---|
| blocking / critical | The central contract, causality, or facts cannot hold | Fix before continuing downstream writing |
| high | Clearly damages continued reading, character credibility, or the central appeal | Fix in the current pass |
| medium | Creates local delay, repetition, or unclear expression | Fix in order of expected benefit |
| low / optional | The work remains valid; this could only enhance it | Do not present it as a mandatory threshold |
