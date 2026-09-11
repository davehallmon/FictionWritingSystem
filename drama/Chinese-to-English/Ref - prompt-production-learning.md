# Learning Genre, Visual Style, Scene, and Prompt Know-How

This workflow extends full-project-chain review to accumulate knowledge about which prompt mechanism might solve a particular problem under a given genre promise, production form, visual direction, and scene responsibility. It does not analyze prompt-term frequency, rank style codes, or calculate task success rates.

## Sampling Matrix

Purposeful sampling records five dimensions simultaneously. Mark missing dimensions as unknown:

1. **Genre or audience promise:** Gratification, suspense, intimacy, comedy, observations of life, narrated commentary, and similar promises.
2. **Production form or visual language:** The project's own description—live action, 2D, 3D, illustration, and so on—plus observable form, materials, light and color, edges, density, and motion budget. A style code or vendor name is not a conclusion.
3. **Scene function:** Introduction, negotiation, evidence reveal, intimate conflict, action task, ensemble scene, transition, ending beat, and similar functions.
4. **Prompt responsibility:** Identity, location geography, composition, style, state, hand-object contact, action, performance, cinematography, and sound.
5. **Version role:** Creative source, derived projection, revision request, external execution text, authorized observation, or operational state.

Each matrix cell stores supporting cards, counterexample cards, failure boundaries, unknowns, and the intent for the next sample. It does not store a “best template” or frequency-based win rate.

## Read Prompts Across the Full Chain

Track one project and version through: story and scene intent → script facts → asset identity, geography, and state → scene-direction choices → keyframe and image specifications → prompts for action, performance, cinematography, and sound → creator revision requests → authorized textual observations, when available.

Determine separately what upstream material must preserve and what execution choices the prompt adds. Identify whether description protects identity, geography, and boundaries or merely accumulates generic quality terms. Determine whether a revision changes viewing rhythm, space, amount of action, performance signals, lighting, or reference strategy, and why the same mechanism would fail under another genre, visual style, or scene function.

Do not replace close reading with batch keyword matches. The agent must explain audience state, character strategy, spatial consequences, and prompt tradeoffs.

## Evidentiary Strength of Production Observations

- `input_reference` supports only reference admission, visible text or watermarks, cropping, identity, or geographic facts.
- `generated_result` can support candidate calibration within the project's conditions only when bound to the exact prompt or specification hash, stable reference `slot_id/order`, production config, observation method, region and time window, and limitations.

A successful task, URL, commit count, retry field, moderation error, or the existence of a prompt does not prove content quality. Without credible media observation, write `media_observed: false` and study only the textual chain and revision intent.

## Form Transferable Candidates

Compress surface wording into:

`观众状态 → 场景问题 → 提示词/导演机制 → 可观察信号 → preserve_set → 失效边界`

For example, “multiple people perform simultaneously” can be compressed into an attention-competition problem. One candidate mechanism retains only one primary action, gives other characters distinct receive/mask/choice behaviors, and declares an attention handoff. Do not turn this into a rule that every ensemble scene may contain only one action.

Public candidates must use entirely new characters, genres, scenes, and wording, and must enter blind evaluation with a counterexample. Do not transfer vendor parameters, identifiers, original sentences, rare combinations, or source paths. Do not promote one project's preference for “many empty shots, few wide shots, and no BGM” directly into a rule.

## Revision and Promotion

For within-project calibration, change only the variables required by the diagnosis and state linked variables and the `preserve_set`. Cross-project know-how continues through de-identification, de-copying, synthetic fixtures, fresh-agent blind evaluation, and an independent reviewer. Narrow, hold, or retire a candidate when it produces no gain, induces formulaic output, or encounters a counterexample. The process does not add a database crawler, semantic matcher, or quality-scoring script.
