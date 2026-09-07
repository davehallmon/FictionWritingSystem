# De-Identification, Synthesis, and Knowledge Lifecycle

## Content Navigation

- From observation to candidate
- Counterexamples, conflicts, and boundaries
- De-identification and de-copy
- Public candidate package
- Promotion gate
- Retirement and traceability

## From Observation to Candidate

First use the complete project chain to explain once how the mechanism works, then seek meaningful comparisons. A candidate describes the problem, conditions, optional action, expected text-observable effect, and signals for discontinuing use. It is neither a summary of the source project nor a “hit formula.”

Use agent semantic judgment to distinguish:

- Genre surface from audience promise;
- Plot-device names from actual dramatic mechanisms;
- Co-occurrence from causal function;
- Screenwriting intent from downstream production translation;
- Effectiveness in one project from transferability across contexts.

Use statistics only to find unread matrix cells, version anomalies, comparison gaps, or records awaiting review. Frequency cannot prove causality, rarity cannot prove ineffectiveness, and a practice from a high-scoring project does not automatically become a standard.

Identify source roles before interpreting results: a `prompt` may be only an input; `userPrompt` / `reSubmit` may be revision requests; `task success` proves only that one execution completed. None proves the quality of a creative or media result or replaces bounded `observation_evidence`. Without an authorized media inspection or credible evidence of creator/audience outcomes, a conclusion may claim only text-level executability, continuity, or preservation of intent—not attractive visuals, effective performance, or a successful finished production.

## Counterexamples, Conflicts, and Boundaries

Actively ask of every candidate:

1. In which adjacent genre or character relationship would it damage the existing audience promise?
2. Could the same result instead arise from another factor in performance action, information order, character relationships, or shot continuity?
3. When the upstream drama works, does the downstream prompt overinterpret it, turn it into narration, or create an unfilmable requirement?
4. Might an apparent failure result from a missing layer, version mismatch, or execution deviation rather than the mechanism itself?
5. Does new evidence refute the candidate, or require narrower conditions?

Do not resolve contradictions by majority vote. When the difference can be explained, record it in `applies_when` and `fails_or_changes_when`. When it cannot, retain `conflict_pending`, continue purposeful sampling, or decline promotion.

## De-Identification and De-Copy

Process candidates in this order:

1. Remove connection information, machine locations, source names, internal IDs, people, projects, roles, organizations, and proprietary settings.
2. Remove original sentences and consecutive phrasing; retain only the agent's abstract explanation of causality, audience state, action, and production constraints.
3. Break apart rare combinations of genre × character relationship × scene × prop × turn to prevent combinational fingerprints.
4. Replace numbers with functional descriptions unless a number is itself a public format contract.
5. Design from scratch a synthetic example with another genre, relationship, space, and performance action.
6. Compare the candidate back against the private cards. If the source remains recognizable through unique order, wording, or combinations, abstract further or abandon it.
7. Store the mapping in isolation for authorized review only; the public candidate carries no mapping.

De-identification is not renaming. Changing only personal names, place names, gender, or era remains reproduction. The surface implementation must change; only the explainable creative problem, conditions, mechanism, and boundaries may remain.

## Public Candidate Package

One proposal contains the smallest mutually aligned set:

- `reference_proposal`: the problem to solve, conditional heuristic, applicable/failure boundaries, and alternatives;
- `rubric_proposal`: positive and negative evidence the Reviewer can locate in public text, false-positive protections, and severity recommendation;
- `synthetic_fixture_proposal`: entirely new characters, genre, scene, and phrasing, including valid, boundary, or failure variants;
- `evaluation_brief`: expected baseline/candidate differences, possible side effects, and genre transfers to test;
- `privacy_attestation`: a statement that there are no source names, original sentences, connection details, combinational fingerprints, or unnecessary exact values;
- `rollback_note`: how to reverse, narrow, or replace the proposal without damaging other public rules.

The proposal remains in the maintainer staging area until blind testing and independent review are complete. The public runtime may consume only promoted static, de-identified material. It cannot look back into nonpublic sources or use a fixture to request media services.

## Promotion Gate

Promotion requires all of the following:

- Evidence comes from qualitative reading of the complete project chain, not search fragments or aggregate statistics;
- Counterexamples capable of challenging the candidate, conflict analysis, and explicit applicability boundaries exist;
- The candidate has undergone semantic abstraction, de-identification, and de-copy, and the synthetic example cannot be traced back to its source;
- The reference, rubric, and synthetic fixture describe the same observable behavior;
- A fresh-agent blind forward eval shows actual benefit without conspicuous templating or genre contamination;
- The version chain, creator overrides, source roles, `media_observed`, and applicable `observation_evidence` are all declared, and prompt, task success, userPrompt, or reSubmit has not been treated as quality evidence;
- The independent reviewer and candidate author roles are separate, and the independent Reviewer explicitly approves the minimal change;
- Public execution requires no connection, credential, private card, or media generation.

Do not set thresholds for project count, occurrence rate, or average score. Evidence sufficiency is jointly determined by diversity, falsifiability, chain completeness, and evaluation performance, and must be explained by the independent Reviewer rather than released by a counter.

## Retirement and Traceability

When a new counterexample reveals that a rule is too broad, blind testing no longer shows a benefit, a rubric frequently raises false positives, a candidate induces mechanical application, or a production boundary changes:

1. Freeze further promotion or use of the old candidate;
2. Record the publicly visible failure mode and affected scope without attaching private evidence;
3. Decide whether to narrow it, have another heuristic supersede it, or retire it;
4. Rerun blind testing and independent review using new synthetic tasks;
5. Retain the version, rationale, and rollback relationship so the same problem is not reintroduced later.

Retirement does not mean deleting unfavorable evidence. Handle private cards under the maintainer retention policy; the public decision record retains only reasoning that does not leak its source.
