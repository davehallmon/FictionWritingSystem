# Private Cards and Coverage Matrix

## Contents

- Shared card discipline
- Observation card schema
- Decision card schema
- Fully synthetic example
- Genre × mechanism coverage matrix

## Shared Card Discipline

Keep cards only in the isolated workspace designated by the maintainer. Trace evidence with random internal IDs, content hashes, or abstract locators;
do not copy entire screenplay passages outside the cards. Separate observations from interpretations, and leave unknowns unknown. Read a project's complete text chain before creating cards;
never treat search hits as complete context.

`genre_axes` describes genre, audience promise, and emotional contract; `mechanism_axes` describes implementation mechanisms rather than names of plot devices.
`evidence` records verifiable locations and observations, not identifiable source wording. Even when `counterevidence` is empty, it must explain the scope searched.
First reconstruct `version_refs` from the layers that actually exist in the project, recording only version references that were read and placing absent layers in `missing_layers`.
Then identify each layer's `source_role`: a creative source,
derived projection, revision request, execution task, or result evidence cannot impersonate another role. Record `creator_overrides` separately to avoid misreading explicit creator choices
as system rules. The existence of a prompt, task success, or commit count proves only
workflow activity; it cannot be entered into `observation_evidence` as proof of effect.

`observation_kind` must match the evidence rather than serving as an arbitrary label: a text-only chain is always `none`; observation of an input reference uses
`input_reference`; observation of a generated result uses `generated_result`. The latter two require `evidence_mode` to be
`creator_reported` or `authorized_media_inspection`, with corresponding `observation_evidence`. Without that evidence,
fall back to `none`; only textual risks may be proposed, and the card cannot enter production calibration. Here, `media_observed` specifically records whether **the maintainer
agent creating the card** personally inspected the media. Because this skill consumes only text chains, it is always `false`. Whether the creator or another authorized observer
inspected the media belongs in `observer_report.observer_media_observed` with explicit attribution; it cannot support a claim that this agent inspected it.
One card cannot combine input-reference and generated-result observations. If one prompt serves multiple responsibilities, create separate cards rather than compressing
identity, style, composition, and other responsibilities into an ambiguous `prompt_role`.

## Observation Card Schema

```yaml
card_type: observation_card
card_id: obs-internal-id
source_project_ref: opaque-project-ref
chain_read:
  available_layers: [brief, story, episode_map, screenplay, assets, continuity, image_prompt_text, storyboard_text, video_prompt_text, review]
  missing_layers: []
  version_refs:
    - layer: screenplay
      ref: opaque-version-ref
    - layer: storyboard_text
      ref: opaque-version-ref
  creator_overrides: [bounded-override-or-none]
genre_axes:
  surface_genre: abstract-label
  audience_promise: abstract-promise
  emotional_contract: abstract-contract
production_axes:
  production_form: abstract-form-or-unknown
  visual_style_axes: [observable-shape-material-light-or-motion-axis]
  scene_function: abstract-scene-function
  prompt_role: identity | geography | composition | style | state | action | performance | camera | sound | none
mechanism_axes: [mechanism-label]
observation:
  setup_state: what-the-audience-can-understand
  pressure_or_question: dramatic-problem
  character_action: playable-action
  information_change: audience-state-change
  turn_or_payoff: observable-dramatic-result
  downstream_translation: how-text-production-layers-preserve-or-alter-intent
evidence:
  direct_observations:
    - locator: opaque-layer-and-record-ref
      source_role: creative_source | derived_projection | revision_request | execution_task | input_reference_observation | generated_result_observation | other_result_evidence
      note: paraphrased-observation-without-source-wording
  agent_interpretation: bounded-causal-reading
  unknowns: []
```

The shared header's `evidence.direct_observations` records only text, recorded versions, and projection chains between layers. The media fragment's
`observation_evidence.direct_observations` records only phenomena an authorized observer actually saw or heard in the listed region or interval.
Do not duplicate the same finding in both locations, and do not use the latter to store task status, prompt summaries, or causal interpretations.

After the shared header above, select **exactly one complete fragment below** according to the actual evidence. Do not append it to another fragment or retain
duplicate YAML keys. Permitted value relationships are
`evidence_mode: none | creator_reported | authorized_media_inspection`.

### none Evidence Fragment

```yaml
media_observed: false
observation_kind: none
evidence_mode: none
limitations: [text-only-chain-does-not-prove-rendered-result]
counterevidence:
  searched: what-was-checked
  findings: []
  alternate_explanations: []
privacy:
  contains_source_wording: false
  contains_identifiers: false
  public_eligible: false
confidence: tentative | supported | conflicted
```

A text-only card does not create a set of completely empty media fields.

### generated_result Evidence Fragment

```yaml
media_observed: false
observation_kind: generated_result
evidence_mode: creator_reported | authorized_media_inspection
observer_report:
  observer_ref: opaque-creator-or-authorized-observer
  observer_media_observed: true
observation_evidence:
  observed_media_ref: bounded-media-locator
  prompt_or_spec_refs: [exact-versioned-record-ref]
  reference_slot_conditions: [stable-slot-id-order-and-ref-set]
  production_configuration: bounded-project-configuration-or-unknown
  bounded_regions_or_intervals: [what-was-actually-observed]
  direct_observations: [creator-attributed-or-inspector-observation]
  limitations: [unseen-or-uncertain-content]
  valid_only_for: exact-project-prompt-reference-and-configuration-versions
counterevidence:
  searched: what-was-checked
  findings: []
  alternate_explanations: []
privacy:
  contains_source_wording: false
  contains_identifiers: false
  public_eligible: false
confidence: tentative | supported | conflicted
```

### input_reference Evidence Fragment

```yaml
media_observed: false
observation_kind: input_reference
evidence_mode: creator_reported | authorized_media_inspection
observer_report:
  observer_ref: opaque-creator-or-authorized-observer
  observer_media_observed: true
observation_evidence:
  observed_media_ref: bounded-media-locator
  input_reference_refs: [exact-versioned-reference-record-ref]
  bounded_regions_or_intervals: [what-was-actually-observed]
  direct_observations: [creator-attributed-or-inspector-observation]
  limitations: [occlusion-resolution-or-unseen-content]
  valid_only_for: exact-reference-version
counterevidence:
  searched: what-was-checked
  findings: []
  alternate_explanations: []
privacy:
  contains_source_wording: false
  contains_identifiers: false
  public_eligible: false
confidence: tentative | supported | conflicted
```

## Decision Card Schema

```yaml
card_type: decision_card
decision_id: dec-internal-id
observation_refs: [obs-internal-id]
candidate_claim:
  problem: transferable-dramatic-or-production-problem
  heuristic: conditional-option-not-command
  expected_observable_effect: text-level-effect
  preserve_set: [upstream-fact-or-non-target-field]
classification: bounded_pattern | craft_option | rejected_generalization | conflict_pending
applies_when:
  genre_axes: [abstract-axis]
  audience_state: required-state
  character_state: required-state
  production_constraints: [text-production-constraint]
fails_or_changes_when:
  counterexample_refs: [obs-counterexample-id]
  warning_signals: [signal]
  alternatives: [alternative-mechanism]
conflicts:
  competing_claims: []
  resolution_or_open_question: explanation
sampling_role:
  matrix_cells: [genre-axis-x-mechanism-axis]
  next_contrast_to_read: abstract-sampling-intent
decision:
  status: hold | synthesize | narrow | reject | propose
  rationale: semantic-judgment-not-frequency
review:
  reviewer_ref: null
  reviewed_at: null
  notes: []
```

## Fully Synthetic Example

The following example was created from scratch. It demonstrates only the level of abstraction and corresponds to no source project:

```yaml
card_type: observation_card
card_id: obs-synthetic-001
source_project_ref: synthetic-only
chain_read:
  available_layers: [brief, story, episode_map, screenplay, assets, continuity, image_prompt_text, storyboard_text, video_prompt_text, review]
  missing_layers: []
  version_refs:
    - layer: project
      ref: synthetic-project-v1
    - layer: screenplay
      ref: synthetic-script-v1
    - layer: storyboard_text
      ref: synthetic-board-v1
  creator_overrides: [none]
genre_axes:
  surface_genre: community-workplace-comedy
  audience_promise: overlooked-newcomer-earns-agency
  emotional_contract: embarrassment-turns-into-earned-recognition
mechanism_axes: [public-misreading, delayed-capability-proof]
observation:
  setup_state: the-audience-knows-the-newcomer-notices-a-routing-error
  pressure_or_question: speaking-up-risks-looking-incompetent
  character_action: the-newcomer-quietly-reroutes-one-delivery
  information_change: coworkers-see-the-result-before-the-reason
  turn_or_payoff: ridicule-reverses-only-after-a-specific-consequence
  downstream_translation: shots-preserve-who-knows-what-and-prompts-stage-the-action-before-the-reaction
evidence:
  direct_observations:
    - locator: synthetic-screenplay-scene-03
      source_role: creative_source
      note: action-causes-visible-result-before-explanation
  agent_interpretation: withholding-the-reason-keeps-the-proof-dramatic-rather-than-verbal
  unknowns: [whether-a-warmer-genre-needs-a-softer-public-reaction]
media_observed: false
observation_kind: none
evidence_mode: none
limitations: [synthetic-text-only-example]
counterevidence:
  searched: synthetic-alternate-scene
  findings: [early-explanation-removes-the-misreading-but-improves-closeness]
  alternate_explanations: [specific-consequence-may-matter-more-than-information-order]
privacy:
  contains_source_wording: false
  contains_identifiers: false
  public_eligible: false
confidence: tentative
```

The corresponding decision card should constrain the conclusion to an optional mechanism: when the audience already understands the character's ability, characters within the scene still misread them, and the consequence can be performed,
the action's result may be shown before its cause is explained. If the genre promises intimate cooperation or the misunderstanding would damage character affinity, use shared discovery instead. Never turn this into
“comeback stories must delay explanation.”

## Genre × Mechanism Coverage Matrix

Each matrix cell uses the following record; do not substitute counts for judgment:

```yaml
cell_id: genre-axis-x-mechanism-axis
genre_and_promise: abstract-genre-plus-audience-promise
mechanism: dramatic-or-production-mechanism
supporting_observation_refs: []
opposing_observation_refs: []
boundary_notes: []
conflicts_or_alternatives: []
chain_gaps: []
confidence: empty | tentative | supported | conflicted
next_sample_intent: contrast-or-gap-to-seek
```

The sampling dashboard may show whether each axis is empty, which project chains lack layers, and which cards conflict with one another. It may only trigger the next round of qualitative reading.
Never convert the number of projects in a cell, genre proportions, mean ratings, or high-frequency terms directly into writing formulas, mandatory thresholds, or quality rankings.
