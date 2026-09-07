# Fresh-Agent Blind Forward Eval Protocol

## Content Navigation

- Objective and role isolation
- Prepare evaluation packages
- Run the blind test
- Blind-review rubric
- Independent reviewer handoff
- Results and lifecycle

## Objective and Role Isolation

Verify whether a candidate helps a new agent make better creative judgments in an unfamiliar genre, not whether it can recite learning material. Keep three roles separate: candidate author, fresh-agent executor, and independent reviewer. Any agent involved in extraction, card synthesis, or candidate writing is ineligible to serve as the final reviewer.

The Fresh agent must not read private sources, observation/decision cards, de-identification mappings, author diagnostics, expected answers, or the other arm's output. It receives only a user-style task, publicly available context, one anonymous skill version, and necessary synthetic input.

## Prepare Evaluation Packages

Create anonymous `baseline` and `candidate` packages for the same objective. Keep the task, upstream constraints, and delivery format identical except for the candidate reference/rubric/fixture. The task set should cover a context where the candidate claims to apply, one boundary context, one possible counterexample, and textual transfer from screenwriting to storyboard/prompts. Do not use source characters, sentences, plot order, or rare combinations of settings.

Provide the following for every task:

- A creative or review request a user could naturally make;
- Fully synthetic story constraints and existing textual artifacts;
- Boundaries on what may and may not be changed;
- The story, script, asset/continuity, storyboard, or prompt text that must be submitted;
- Requirements for handling missing information;
- A declaration prohibiting connections to nonpublic sources and prohibiting media generation or inspection.

The candidate author writes the tasks but not model answers. A coordinator who does not know the anonymous mapping assigns versions and preserves raw outputs.

## Run the Blind Test

1. Start a fresh agent with a clean context for each task.
2. In the voice of a real user, ask it to complete the task using the assigned anonymous skill; do not reveal which rule is under test.
3. Do not add explanations from the candidate author. If the agent asks a question, provide only pre-authorized information that is identical for both versions.
4. Preserve the prompt, skill-version hash, input hash, raw output, tool-call summary, and reason for noncompletion. The coordinator stores this run provenance separately; it is not attached directly to the reviewer-facing creative output.
5. Run the comparison in a new context so results, files, or reviewer opinions from the prior run cannot contaminate it.
6. Create a reviewer-facing anonymous copy: remove absolute paths, package directories, tool-read lists, arm identity, and version mappings. Retain only the creative artifacts required by the task and a scope declaration that does not leak the role. Path attestation must not enter the blind-review text.
7. Hash and scan the anonymous copy for leaks, then complete criterion-by-criterion review and preference reasoning before unblinding.

Deterministic tools may verify hashes, file isolation, formatting, and leak scans. Plot causality, genre fit, character action, shot intent, and templatedness require reviewer judgment and must not be replaced by keyword scoring.

## Blind-Review Rubric

The Reviewer compares specific evidence; an overall score does not automatically determine the winner:

- `dramatic_reasoning`: Do anticipation, obstacles, action, information changes, and payoff form an explainable causal sequence?
- `character_agency`: Do characters advance events through performable actions that fit their circumstances, rather than being transported by a mechanism?
- `genre_transfer`: Does the output serve the current genre/audience promise rather than copying the surface features of one genre?
- `boundary_judgment`: In counterexamples or inapplicable contexts, can it change methods, narrow the approach, or refuse to apply the pattern?
- `production_translation`: Is script intent preserved as it moves into assets, continuity, storyboards, keyframes, and prompts?
- `creative_variance`: Do different tasks exhibit meaningful variations in mechanism rather than repeating the same phrasing, beats, and shot template?
- `instruction_cost`: Does the candidate add irrelevant process, excessive explanation, or impediments to creation?
- `privacy_and_scope`: Does it use only synthetic/public material, with no source fingerprint, connection attempt, or media call?

For every criterion, record the relevant output location, impact, preference, and confidence. If each version has advantages, state the conditions to which the candidate should be narrowed. If a difference arises from incidental prose style or execution failure, keep the result inconclusive rather than forcing promotion by vote count.

## Independent Reviewer Handoff

Before unblinding, give the independent reviewer only the reviewer-facing anonymous outputs, synthetic tasks, anonymous-package hashes, leak-scan results, and public rubric. Freeze the review and unblind only after the Reviewer has written criterion-level preferences, boundary issues, and a preliminary verdict.

After unblinding, provide the version mapping, public candidate package, nonsensitive evidence summary, and conflict/boundary list. Use these to verify that the packages differ only in the target change and that the public diff matches the material reviewed. Absolute paths, tool calls, and run evidence stored separately by the coordinator still must not be copied into the public evaluation record. View the mapping in an isolated area only when privacy evidence requires review and the Reviewer has equivalent authorization. Never copy private cards into a public evaluation record.

The Reviewer must answer:

- Does the task genuinely test the candidate rather than hinting at the answer?
- Are baseline and candidate equivalent except for the target change?
- Does the candidate's benefit fall within its claimed scope?
- Does the boundary task show that the agent exercises judgment rather than matching mechanically?
- Is there leakage, near-reproduction, genre contamination, or dependence on a public run?
- Should the result be promotion, narrow-and-retest, hold, or retire, and what evidence supports that decision?

## Results and Lifecycle

`promotion` requires explicit independent approval and a minimal, reversible public diff. `narrow-and-retest` returns to the candidate boundary and synthetic tasks. `hold` preserves the issue and intent for the next comparison. `retire` records why the candidate provided no benefit, overfit, misled, or failed at a boundary. No outcome may replace the Reviewer's evidence-based explanation with frequency, an average score, or a single preference number.
