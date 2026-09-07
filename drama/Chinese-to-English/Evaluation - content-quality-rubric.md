# Cross-Genre Blind-Evaluation Rubric for Short-Drama Scripts (v5)

This rubric evaluates only the text of a single-episode script before production. It does not evaluate file count, Schema completeness, prompts, or workflow convenience. Reviewers may see only the fixed task and works randomly labeled A/B; they must not know the version, branch, baseline/candidate identity, or previous review.

## Scoring Dimensions (Total: 100)

| Dimension | Maximum | Focus of judgment |
|---|---:|---|
| `hook_payoff` | 15 | Does the opening create interest in the promise of this task? Does the episode deliver a proportionate payoff or intentionally defer it? |
| `causality` | 15 | Do actions and turns arise from established characters, facts, and consequences, or does the script solve problems through convenient conditions? |
| `character` | 15 | Are the main characters' goals, strategies, relationships, and costs specific? Is the space given to secondary/transactional characters proportionate to their function? |
| `dialogue_action` | 15 | Does dialogue pursue, evade, test, exchange, or change relationships rather than restating visuals or task instructions? |
| `visual_drama` | 10 | Can important information be received through filmable behavior, space, objects, sound, silence, or on-screen text? |
| `pacing_retention` | 10 | Do information release, action capacity, pauses, and closure suit the specified duration and style? Does anything repeat or arrive prematurely? |
| `prompt_fidelity` | 10 | Does the script preserve the task's facts, constraints, genre contract, completion boundary for the limited unit, and explicit prohibitions? Does it invent exact numbers, records, resources, procedures, or structural devices absent from the task? |
| `genre_fit` | 10 | Does the writing serve the specified genre and viewing contract, or does it force every genre into the same choice/evidence/deadline/causal-hook template? |

Every dimension requires an integer score and at least one piece of specific evidence from each of A and B. Preference must agree with the total score; equal scores require a `TIE` verdict.

## Unified Score Anchors

First choose a band as a percentage of that dimension's maximum, then assign an integer score. Fifty percent means the function works; above 75% means clearly stronger than an ordinary completed draft. Do not award points automatically because a text is longer, correctly formatted, uses more objects/time figures, or includes more verification steps.

| Band | Percentage of dimension maximum | Applicable judgment |
|---|---:|---|
| Missing/counterproductive | 0–20% | A core obligation is absent, or the writing damages genre, causality, character, filmability, or task constraints |
| Discernible but weak | 25–40% | Relevant design exists but depends mainly on exposition, coincidence, functional characters, repetition, or mechanical rule display |
| Functional | 45–60% | The primary obligations are met and filmable, but conventionality, convenience, concentrated exposition, pacing, or tone problems remain |
| Strong | 65–80% | Specific, coherent, and genre-appropriate; key turns and constraints are handled solidly, with only local defects |
| Exceptional | 85–100% | Nearly free of substantive defects, with memorable character strategies and formal choices that are difficult to interchange |

## Overfitting Diagnostics

Record diagnostics separately from scores. Check a tag only when explicit script evidence exists, and attach one specific piece of textual evidence:

| Tag | Diagnostic condition |
|---|---|
| `forced_choice` | The task contains no conflicting obligations, but the script manufactures a binary choice; or it packages a one-way action as a false choice |
| `forced_evidence_procedure` | The task requires no evidence gathering, but the script adds authentication/counterfactual testing; or procedure overwhelms the genre experience |
| `forced_deadline` | The task provides only qualitative time pressure or no deadline, but the script adds minutes, seconds, timestamps, notifications, records, or a countdown to manufacture generic pressure |
| `case_echo` | A rare character, device, solution mechanism, or consecutive phrase from another evaluation case appears without support in the task |
| `mechanical_rule_display` | Characters/actions appear to display writing rules one by one, damaging natural behavior, genre tone, or pacing |

The candidate works for negative-control cases must receive no overfitting tags across the four reviews. Candidate tag totals must not exceed baseline totals at the full-corpus, development, or holdout level.

## Corpus and Blind-Evaluation Discipline

- Use at least 12 fixed cases across 10 genres. Every case used for tuning belongs to development. Run at least 4 additional one-time holdout cases only after candidate instructions, rubric, prompts, and thresholds are frozen.
- Include at least 3 negative-control cases. In at least one, the task should not directly say “do not use a choice/evidence/deadline”; use an ordinary-life premise to test whether the Skill spontaneously imposes a template.
- Cover each of the three specialized mechanisms—high-cost choice, disputed evidence, and a literally precise deadline—in at least 3 cases, but enable them only in annotated cases.
- Precommit 3 independent creative replicates for every case and version. Do not use best-of-N, rerun only failures, or include results selectively. Use a new session each time and weight all replicates equally.
- For every replicate, use the Codex and Kimi model families. Each family reviews twice with swapped A/B positions, producing 4 new reports. Balance A/B positions across replicates and genres.
- Use a new session for every review; do not inherit creation context, version identities, other cases, or previous review context.
- Use the same neutral creative prompt for baseline and candidate. Wrapper language must not repeat overfitting diagnostics or hint “do not apply a template.”
- Bind the fixed corpus, task, Skill bundle, baseline commit, creation/review prompts, model configuration, A/B works, reports, and invocation receipts with SHA-256. A hash proves only that evidence belongs to frozen input; it does not replace quality judgment.
- Within each replicate, first average the four reports. Then average the precommitted replicates with equal weight to obtain the case score, and separately calculate macro averages for development, holdout, and the full corpus. Cases with more reports must not receive more weight.
- The candidate must be non-degrading in both splits and the full corpus. No individual case may fall by more than 2 points.
- Report changes for both reviewer families, both A/B positions, and all eight scoring dimensions. Family/position/dimension aggregates must remain above the predeclared 1-point noninferiority margin, exposing model disagreement, positional bias, and degradation in an individual dimension.
- The candidate must not increase overfitting tags or leak rare details from earlier development cases.
- Once holdout results have been viewed, they can no longer be called “untouched.” If they cause any change to writing instructions, rubric, prompts, or thresholds, immediately retire the batch to development and create a new holdout for the next conclusion. Do not rerun it until it passes.

This gate demonstrates that “a generalization fix has not replaced an old fixed template with another fixed template.” It does not prove that any one dramatic form is universally superior.
