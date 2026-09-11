# Asset Continuity and Change Log

## Table of Contents

- [Boundary Matching](#boundary-matching-con-01)
- [State Tables vs. Change Logs](#difference-between-state-tables-and-change-logs)
- [Responsibilities by Stage](#responsibilities-by-stage)
- [States to Track](#five-groups-of-states-to-track)
- [Logging Procedure](#steps-for-writing-a-change-log)
- [State-Chain Example](#composite-state-chain)
- [Nonlinear Time](#nonlinear-time-and-intentional-discontinuities)
- [Revision Impact](#revision-impact)
- [Handoff Checklist](#handoff-checklist)

## Boundary Matching (`CON-01`)

For adjacent shots, compare each field in the accepted end state of the preceding shot with the accepted start state of the following shot.
A discrepancy has a valid basis only when the upstream owner has already logged the change or a revision explicitly requested by the owner is still in progress;
never use motion-prompt language to quietly “bridge” the difference.

## Difference Between State Tables and Change Logs

- A **state table** answers, “What is the state at this boundary?”
- A **change log** answers, “What changed, what were the before and after states, why did it change, when did it take effect, and whom does it affect?”

Do not duplicate the full specification table in every scene. Record only states and changes that downstream work will depend on. This both exposes unsupported jumps
and allows a script revision to be marked accurately as `stale` without redoing the entire project.

## Responsibilities by Stage

The asset skill owns identity, asset versions, and scene-level asset-state changes—for example, when a look changes, when a prop changes hands,
or when scene lighting changes from normal illumination to a power outage. The story-development skill owns planned story state; the screenplay skill owns
the written changes in knowledge, beliefs, goals, relationships and power, and emotions, along with their narrative meaning. The asset state table may only cite
these sources; it must not create a separate set of story facts in `after`.

The storyboard skill owns the start and end boundaries of each shot, including pose, position, gaze, both hands, held items, and visible state.
Assets may cite these boundaries but cannot create a separate, conflicting account of hand positions or blocking.

**`structural_invariant` CON-04**: Every change must include a before state, an after state, a cause or source, an effective range, and the affected
existing `IMG-...`, `SHOT-...`, or `MOTION-...` records. When nothing changed, do not merely write “updated.”

**`structural_invariant` CON-06**: The affected-items list must cover every existing consumer. For work that has not yet been created, identify only
the responsible owner and the fact that must be synchronized; do not pre-create placeholder records.

## Five Groups of States to Track

1. **Character story state**: knowledge, beliefs, goals, relationships and power, and emotions. Track these only when they affect later
   actions or review, and point to their exact source in story development or the screenplay; these are not changes for the asset skill to invent.
2. **Character visible state**: exact look, injuries, dirt or wetness, and scene-level carried items. The storyboard owns poses within a single shot.
3. **Location state**: location, viewpoint, available entrances, time of day, weather, lighting, and key set dressing.
4. **Prop state**: exact version, responsible owner, holder, location, condition, contents, and readable text.
5. **Scene or episode handoff**: the ending state of the previous scene or episode, the entry state of the next scene or episode, and
   the prompts and shots that depend on those states.

**`craft_default` CON-03**: Track only facts that later work may reference. If the color of Gu He's shoelaces does not affect identification or
action, it need not be repeated in every scene; the unique number plate she takes away must be included in the end state.

## Steps for Writing a Change Log

1. Identify an explicit change or boundary mismatch in the asset appearance log.
2. Read the preceding explicit state in `视觉设定.md`; never infer it backward from a downstream prompt.
3. Write one clear `before` and `after`; a compound event may be split into multiple changes with the same cause.
4. Record the scene ID and action/dialogue or visual-specification entry that caused the change, so the cause can be verified directly within the current five documents.
5. State the script passage, scene, or episode where the change takes effect and where it ends; write `open_ended` when no explicit endpoint exists.
6. For consumers that already exist, list the affected `IMG-...`, `SHOT-...`, or `MOTION-...` records. For future work, state only what must
   be synchronized; do not pre-create placeholder references.
7. Compare the state with the start state of the next adjacent item: pass it when they match; explicitly request a revision when they do not.

### “Unknown” Does Not Mean “Reset to Default”

If a character is still injured at the end of the previous episode and the current episode does not mention the injury, do not automatically restore the uninjured state. Preserve the last confirmed state
and open an `unresolved` continuity question: Is the character still injured, did treatment occur during an intentional omission, or did the screenplay overlook it?

### Knowing a Fact Does Not Mean Knowing That the Other Person Also Knows

For an identity or secret scene, distinguish at minimum whether A knows the fact, whether B knows it, and whether A knows that B knows it.
If the episode entry state already says “both parties know each other's identities,” then “he confirms that the other person recognizes him” cannot be treated as a new reveal in this episode.
Either correct the entry state or restate precisely which belief or strategy actually changes in this scene.

### Having a Source Does Not Make a Change Plausible

Citing a screenplay passage proves only that the change has a textual source; it does not automatically establish causality. For example, “the light flickered once”
does not sufficiently explain a permanent power outage across the entire transfer station. **`reviewed_invariant` CON-02**: The reviewer must use screenplay
evidence to judge whether changes in injuries, knowledge, prop custody, weather, and lighting are credible; nonempty fields cannot substitute for judgment.

## Composite State Chain

At the start of SC004: Gu He wears `LOOK-GUHE-RAIN`; the metal box is closed with the number plate inside; the duty-room lights are on.

1. She opens the box and takes out the plate: the box changes from “closed, containing the number plate” to “open, empty”; the number plate moves from inside the box to Gu He's right hand.
2. She gives the number plate to Uncle Wei: the plate moves from Gu He's right hand to Uncle Wei's right hand, with the handoff action cited as the cause.
3. The distribution box trips: the scene changes from normal nighttime illumination to a power outage until repairs are made; if it remains unrepaired at the end of the episode, write `open_ended`.
4. Heavy rain blows through the broken window and soaks the right shoulder of her raincoat: the character's visible state becomes wet; create a new look version only if it will carry across episodes or requires a reference image.

The end state must declare at minimum: Uncle Wei holds the number plate, the metal box is empty and open, the duty room has no power, and the right shoulder of Gu He's raincoat is wet.
If the next episode immediately shows Gu He holding the plate, there must be a return log or a creator-approved revision; do not silently “align” it.

## Nonlinear Time and Intentional Discontinuities

Montages, ellipses, dreams, and subjective images may depart from normal chronological adjacency, but they must explicitly record the discontinuity type,
entry and exit boundaries, and which states remain reliable. This is a **`taste_option` CON-05**, not a reason to avoid logging.
A flashback does not rewrite the current timeline's state table; it uses the applicable historical version within its own temporal branch.

## Revision Impact

- When revising the screenplay passage where an injury begins, list the looks, prompts, shots, or motion prompts that directly read that passage; each owner updates them when a refresh is required.
- When only a prop's display name changes while its ID and facts remain unchanged, normally update only the display text; do not redo unrelated storyboards.
- Revising shot composition does not automatically modify asset files.
- Revising screenshot descriptions or prompt copy must not rewrite the current visual state backward.

## Handoff Checklist

- The end state of every shot matches the start state of the adjacent next shot, or the responsible owner has explicitly requested a revision.
- A handoff identifies both the person relinquishing the item and the person receiving it; the item is not duplicated into two people's hands.
- Injuries, looks, weather, and lighting do not reset without cause.
- Prop-content state and character knowledge are recorded separately.
- A change's effective range covers every dependent shot and does not begin prematurely.
- The affected-items list covers all existing prompt, shot, and motion-prompt consumers; when revising, recalculate the actual consumers rather than merely
  carrying forward the old list.
- The end state is sufficient for the next episode to continue without relying on the creator's memory.
