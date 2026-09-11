
# Source-Story Quality Evaluation Checklist

> **Purpose**: A quality self-check checklist for story-short-analyze (short-story deconstruction), used item by item when evaluating the writing quality of the **source material being analyzed**.
> For quality checks on the deconstruction pipeline itself, see “Required Quality-Check Fields” in output-templates.md. The sole authoritative definitions of all numerical thresholds are “Quality Standards” and “Pacing Analysis” in material-decomposition.md; this checklist defines no numerical thresholds of its own.
>
> **Division of responsibility among three kinds of quality (do not mix them up)**:
>
> 1. **Deconstruction-pipeline quality checks** (during execution) → [“Required Quality-Check Fields” in output-templates.md](output-templates.md). Every item carries a `[BLOCK]` / `[WARN]` label; a missing `[BLOCK]` item → the “BLOCK Item Scan” stops the process.
> 2. **Quality of the material being evaluated (the source story)** (what kind of material is being deconstructed) → this file. It answers, “Is this source story well written?”
> 3. **Quality of the deconstruction report itself** (what kind of report is being written) → [analysis-report-style.md](analysis-report-style.md). The report is gated by the “Deconstruction Report Expression Self-Check.” Clichés and AI-like prose in the source remain objects of analysis and are not filtered from the input.

## Table of Contents

- [I. General Checks](#i-general-checks)
- [II. General Five-Dimension Evaluation](#ii-general-five-dimension-evaluation)
- [III. Short-Fiction Checks](#iii-short-fiction-checks)

## I. General Checks

### Chapter Structure
- [ ] The opening has a hook (it does not begin with weather/scenery/daily routine)
- [ ] The middle advances (an event occurs)
- [ ] The situation changes (after this chapter, the world is different from before)
- [ ] The ending lands on that change (it is not a summary)

### Opening Check (First 300–500 Chinese Characters)
- [ ] A hook captures attention
- [ ] It does not begin with weather/scenery/daily routine
- [ ] The protagonist appears quickly
- [ ] The selling point or crisis is visible

### Chapter Progression
- [ ] There is a central event
- [ ] The situation changes
- [ ] It is not filler (would deleting this chapter affect comprehension? If not = filler)
- [ ] It advances at least one of the main plot, relationships, or worldbuilding

### Information Delivery
- [ ] There are no long expository passages explaining the setting
- [ ] Information follows conflict (worldbuilding is conveyed through events)
- [ ] The amount of worldbuilding is controlled (no more than three new concepts in one chapter)

### Scene Check
- [ ] The scene has an objective (what the character wants)
- [ ] The scene has an obstacle (what stands in the way)
- [ ] The scene creates change (the ending differs from the beginning)
- [ ] Characters do things rather than merely feel things
- [ ] No paragraph can be deleted without loss

### Chapter Ending
- [ ] The ending lands on a change
- [ ] It contains at least one crisis/decision/discovery/twist
- [ ] It is not a summary ending
- [ ] It pulls readers onto the next page

### Language
- [ ] There are no empty lyrical passages
- [ ] The same emotion does not continue across several consecutive paragraphs
- [ ] Dialogue fits each character's identity (different people speak differently)
- [ ] Emotion is grounded in action (rather than stated directly as “he was very sad”)

### Serialization Continuity
- [ ] Earlier promises/foreshadowing have not been forgotten
- [ ] A large amount of new worldbuilding does not appear abruptly
- [ ] Foreshadowing advances
- [ ] The story engine is still running

### Filler Detection
The following signals indicate possible filler:
- The entire chapter's dialogue contains no new information
- The same emotion is described for more than three paragraphs
- A scene description exceeds 500 Chinese characters without advancing the plot
- A character recalls earlier events without offering any new perspective
- More than two consecutive chapters contain no conflict

---

## II. General Five-Dimension Evaluation

### Five-Dimension Scoring Standard

Score each dimension from 0–100 and choose a revision strategy based on the results.

### Dimension 1: Core Consistency
Check whether key conflicts, actions, and character motivations remain consistent.

| Problem | Severity | Fix |
|------|--------|------|
| A character's motivation changes suddenly without setup | critical | Add the event that triggers the motivational shift |
| The central conflict is inconsistent | high | Review and revise the conflict premise |
| A key action contradicts the character's personality | high | Adjust the action or add an explanation |
| A secondary conflict is forgotten | medium | Resolve or deemphasize it |

### Dimension 2: Surface-Level Originality
Check whether sentence structures and wording are original enough to avoid formulaic expression.

| Problem | Severity | Fix |
|------|--------|------|
| Copying source sentences produces an unnatural voice | medium | Rewrite only when the line genuinely sounds AI-generated; retain normal source wording |
| Heavy use of AI-signaling words | high | Replace them with concrete description |
| The same sentence pattern recurs | medium | Vary the expression |
| Description is overly literary (ornament piled up, formal tone, chains of metaphors) | medium | Make it more conversational/action-based; action-based does not mean chopping prose into strings of three-to-five-character fragments—the revision should still rely mainly on longer, comma-linked sentences |

### Dimension 3: Format Consistency
Check whether paragraph structure, length allocation, and opening/ending formats are consistent.

| Problem | Severity | Fix |
|------|--------|------|
| Paragraph lengths differ too greatly | medium | Adjust paragraph breaks |
| Chapter length misses the target | **high** | During writing/outline repair, return to the detailed outline first and add planned plot beats before expanding them; when removing AI-like qualities from an existing draft, do not add new plot |
| Formatting is inconsistent (dialogue/description styles differ) | low | Standardize the format |

### Dimension 4: Readability
Check for verbosity, AI-like prose, empty summaries, and formulaic rhetoric.

| AI-Like Trait | How to Identify It | How to Fix It |
|-----------|----------|----------|
| Empty summary | “He finally understood” / “Everything went without saying” | Delete it and use action instead |
| Formulaic rhetoric | “It was as though fate were playing a joke on him” | Delete it or replace it with concrete description |
| Emotion label | “A wave of sadness came over him” | Express it through behavior |
| Circular interiority | Interior monologue adds no new information, repeats the same emotion, or restates what readers already know | Compress only the circular portion; do not shorten monologue that supplies new information, a decision, or an emotional turn merely because of sentence count |

### Dimension 5: Logical Coherence
Check whether sentences and paragraphs flow and whether any worldbuilding conflicts exist.

| Problem | Severity | Fix |
|------|--------|------|
| Worldbuilding contradicts itself | critical | Locate and standardize the premise |
| Timeline error | high | Mark and correct the timeline |
| Character information is inconsistent | high | Build and consult a character dossier |
| The causal chain breaks | medium | Add a transition |

### Revision Strategies

Choose a revision strategy based on the five-dimension scores:

| Primary Problem | Strategy | Description |
|----------|------|------|
| Low core consistency | rewrite | Rewrite the relevant passages around the central conflict |
| Excessive length | compress | Cut material that does not advance the plot |
| Heavy AI-like prose | de_ai | Replace prohibited words and rewrite sentence patterns |
| Many minor problems | polish | Refine the language details |

---

## III. Short-Fiction Checks

### Suffering-to-Satisfaction Pacing Check

A short-fiction-specific check: Are painful beats and satisfying beats distributed effectively?

```
理想分布：虐1 → 虐2 → 虐3 → 爽1(小) → 虐4 → 爽2(大)
禁忌分布：虐1 → 虐2 → 虐3 → 虐4 → 虐5（无爽点，读者流失）
禁忌分布：爽1 → 爽2 → 爽3 → 爽4（无铺垫，爽感疲劳）
```

Analysis rules:
- Mark whether each scene or section materially changes risk, information, relationships, resources, decisions, actions, or reader understanding, and where the consequences of the previous choice land
- Distinguish direct conflict from pressure created by tasks, evidence, waiting, craft, space, relationships, and other sources; do not judge quality by fixed word-count intervals
- Record which causes, choices, and evidence converge to create the greatest satisfying payoff, and how much space remains afterward for consequences; do not judge it by a fixed percentage
- Record whether the ending uses an emotional landing point, partial payoff, clear aftermath, or another form of closure, and assess its effect

### Dialogue-Density Check

| Analysis Item | What to Record | Misjudgment to Avoid |
|--------|----------|----------|
| Dialogue function | Whether it changes information, strategy, power, relationships, or the next action | Do not substitute a whole-text percentage for scene-by-scene functional analysis |
| Scenes without dialogue | Which of task, object, evidence, space, waiting, or craft drives the scene | Do not automatically judge dialogue-free scenes as “too dry” |
| Dialogue rhythm | How turn length expresses character power and immediate pressure | Distinguish effective brevity from fragmented micro-Q&A |
| Dialogue percentage/line count | Descriptive data for this text and samples in the same genre and on the same platform | Do not set a pass threshold across genres |

### Protagonist Leverage and Emotion Analysis (For Comeuppance/Revenge Fiction)

| Analysis Item | What to Record |
|--------|----------|
| How is the protagonist's composure made visible? | Record evidence gathering, choices, delayed responses, or resource allocation; do not treat holding a glass, straightening a suit, or spinning a pen as universal standards |
| What consequences follow emotional loss of control? | Record the accumulated pressure, its placement, and how it changes action, relationships, or cost; do not judge by frequency or percentage |
| What creates the contrast between protagonist and antagonist? | Record leverage, judgment, consequences of action, or information gaps; do not assume the antagonist must become hysterical |
| How does line length express power? | Analyze it alongside interruptions, silence, evasion, and leverage within the scene; do not impose a fixed ratio |
| Is courtroom-style dialogue effective? | Record whether questions force choices, expose contradictions, or change relationships; do not judge by count |

### Evidence-Chain Integrity Check (For Revenge/Comeuppance Fiction)

| Check | Standard |
|--------|------|
| How is evidence released? | Record how every release changes action or the reader's model; a complete evidence chain delivered all at once can also work |
| Is every piece of evidence set up? | Its clue must appear earlier |
| Are the antagonist's reactions causal? | Record their leverage, misjudgments, and losses; identify whether the pattern mechanically repeats “smug first, humiliated next” |
| Is the final piece of evidence the most devastating? | The final evidence must transform the overall understanding |
| Is “time-bomb” evidence used? | Analyze whether advance preparation fits the protagonist's capabilities, timeline, and conditions for obtaining evidence; it is not mandatory |

### Quick Reference: Pitfalls/Identification/Shock/Opening/Ending/Emotion/Anticipation

> **This table evaluates the source story** (whether the object of deconstruction is well written). Any judgment of a harmful trope must cite evidence from the source rather than rewriting it.
> **Do not use this table to evaluate the deconstruction report itself**: The report follows the “Deconstruction Report Expression Self-Check” + [analysis-report-style.md](analysis-report-style.md).
> **Deconstruction-pipeline completeness** follows the `[BLOCK]` / `[WARN]` checklist under [“Required Quality-Check Fields” in output-templates.md](output-templates.md).

| Check | Standard |
|--------|------|
| An unsatisfying power fantasy | The special advantage's effect must be demonstrated clearly |
| Suppression without purpose | Every instance of suppression must serve a later eruption |
| The antagonist's fate is unrelated to the protagonist | The antagonist's death must result from the protagonist's actions |
| Economic/power-scale collapse | Keep the premise internally consistent, anchored to ordinary people |
| Dumbing down the heroine/supporting woman | Normal characterization is acceptable; avoid stale formulas |
| Reader expectations remain unmet too long | Deliver satisfaction at the right time or introduce a new expectation |
| The protagonist's behavior is incomprehensible | It must be understandable and relatable |
| A jarring gag breaks the atmosphere | Atmosphere > jarring gag (except in gag-driven fiction) |
| Hooks never pay off | Unresolved hooks = a failed ending |
| Layering shock | Point→network→depth; do not show only point shock |
| Escalating the shock ladder | Rise in steps, not a straight line |
| Breadth of shock | The entire relationship network should react |
| Conflict/anomaly within the first 50 Chinese characters | It cannot be background setup |
| Central conflict known within the first 100 Chinese characters | It must be clear |
| Opening emotional intensity | ≥7 (1–10) |
| The ending is concrete | Action/dialogue/image; no summary/reflection |
| The ending has resonance | Readers still want to continue |
| Ending emotional intensity | Suffering≥8, satisfaction≥7, healing≥6 |
| Emotionally equivalent release | Repay as much suffering as was inflicted; the antagonist's fate must connect to the protagonist |
| Anticipation management | Keep two long-term and one short-term expectation active; sustain the central selling point |
