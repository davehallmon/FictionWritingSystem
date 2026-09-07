# Asset Breakdown Review Checklist

## Binding Gate (`AST-05`)

Before asset definition is complete, every downstream reference must resolve to an explicit identity entry, and each variant must be valid within the referenced plot range. Keep unresolved occurrences unresolved; never guess a plausible-looking ID merely to let prompt or storyboard work continue.

Check in this order: mechanical facts → semantic judgment → creator acceptance. The Owner may revise in response to a finding; the revision itself does not constitute a review verdict. When a verdict is required, begin a separate review action. A self-check may also truthfully record conclusions supported by evidence.

## A. Mechanical Checks (`structural_invariant`)

- [ ] Every production-relevant script segment has an asset disposition, or explicitly states that the segment contains no asset change.
- [ ] Every result points to a visible scene ID and is supported by the current `剧本.md`.
- [ ] Source location, facts explicit in the script, asset judgment, and continuity changes are not conflated.
- [ ] Every occurrence is classified as exactly one of reuse, new variant, new identity, or unresolved.
- [ ] Every new variant states its base, change, cause, effective location, and ending location; if there is no explicit endpoint, mark it ongoing.
- [ ] IDs are unique; every accepted binding resolves exactly to Character+Look, Location+View, or Prop+State.
- [ ] Unresolved items are not disguised as confirmed identities and cannot flow into image prompts or storyboards.
- [ ] Every change records its prior state, subsequent state, cause/source, effective range, and affected visible IDs.
- [ ] Linked outgoing/incoming states agree, or an explicit pending reconciliation exists.
- [ ] The readable-text policy is complete; `exact_readable` does not conflict with `no_readable_text`.

A mechanical failure identifies the exact file, heading ID, owner, and repair direction without echoing the entire creative passage.

## B. Semantic Review (`reviewed_invariant`)

Answer each item with cited script/bible evidence:

- [ ] Ambiguous pronouns, anonymous people, and multiple identical objects have not been guessed into an existing ID.
- [ ] Character identity anchors are separated from temporary states such as clothing, injuries, moisture, dirt, and poses.
- [ ] Location geography and fixed anchors have not been duplicated into a new location because of angle, time of day, weather, or lighting.
- [ ] A Prop's form/function identity has not been duplicated because of owner, open/closed state, damage, contents, or text state.
- [ ] Every new asset has persistent evidence showing why it cannot be reused; every variant states what remains unchanged from its base.
- [ ] Extraction does not invent faces, brands, doors or windows, contents, injuries, lighting, or readable text.
- [ ] Transfers, injuries, wardrobe changes, power outages, weather/light states, and knowledge changes all have sufficient plot causes.
- [ ] Each occurrence has a sensible production disposition: a mention is not mistaken for an on-screen appearance, and a key manipulated object is not demoted to ordinary set dressing.

A Reviewer finding should include the file and heading ID, evidence, impact, revision result, owner, severity, and status; it must not merely say “the assets lack detail” or “this looks AI-generated.”

## C. Craft Defaults (Overridable; Not Independently Blocking)

- [ ] Prefer reuse or a variant when identity has not changed; do not pursue “one asset per scene.”
- [ ] Leave transient pose/camera/framing to the storyboard rather than creating a Look/View/State explosion.
- [ ] The bible retains only facts needed for recognition, reuse, prompts, shots, and continuity.
- [ ] A Location establishes geography, entrances, and fixed anchors before atmosphere; a Prop establishes scale, form, material, and function; a Character has observable distinguishing anchors.
- [ ] Outgoing state is concise but sufficient for the next scene or episode to continue without filling gaps mentally.

The Creator may override a default for production reasons—for example, because background furnishings require item-by-item approval. Record the override instead of converting it into a hard rule.

## D. Taste Options (Confirm the Choice Only)

- [ ] A choice has been made to manage extras as a group or as individuals.
- [ ] The granularity used to divide spaces within the same building supports the current production.
- [ ] Boundaries have been declared for montages, dreams, and subjective discontinuities.
- [ ] The choice between keeping a temporary visible state as a delta and promoting it to a variant matches the project's reuse strategy.

Do not fail an item merely because the Reviewer prefers another option.

## E. Creator Confirmation

The creator-facing summary must list:

1. Reused items and their matching evidence;
2. New variants and each base/difference/cause/validity;
3. New assets and persistent distinguishing evidence;
4. Source-text evidence, candidates, and downstream impact of each possible choice for unresolved items;
5. Continuity deltas and cross-episode outgoing state;
6. Downstream files that must be synchronized after confirmation.

Write creator-confirmed results directly into `视觉设定.md`. Keep unconfirmed choices marked “未决” and explain their impact. Creator confirmation does not mean that structural checks passed, review passed, or production may begin; each of those actions occurs independently.

## Completion Criteria for the Current Scope

The current asset batch is complete when structural checks pass within scope, every occurrence has been decided, no unresolved references remain, continuity is ready for handoff, and the creator has confirmed all new/reused/variant/change choices that require a decision. Review and delivery are subsequent independent actions; they are not implicit prerequisites for the parallel image-prompt and storyboard branches.
