# Prop and State Design

## Contents

- [Props and State](#props-are-not-a-noun-list)
- [Individuals and Collections](#individuals-identical-items-and-collections)
- [Text Policy](#readable-text-policy)
- [Contents and Character Knowledge](#contents-and-knowledge-are-separate-continuity-lines)
- [Complete Process for Key Props](#key-props-with-explicit-functions)
- [Example and Checks](#synthetic-example-sheet-metal-box)

## Props Are Not a Noun List

Only an object that must be recognized, manipulated, transferred, read, revealed, or kept continuous deserves management as a prop. An ordinary background object may remain a `set_dressing` occurrence. Once a character picks it up to reveal a secret or transfers it across scenes, it must be traceable under a stable identity.

## Prop: Persistent Identity

A Prop stores identifying information that does not readily change through the current action:

- Size/scale reference, basic form, and relationships among components;
- Primary materials, surface treatment, and persistent wear;
- Original function and operating method;
- Permanent unique marks such as serial numbers, chips, or crests;
- Individual distinctions among several identical items, or the method used to manage them by category and quantity.

“Important document,” “mysterious box,” and “premium texture” are plot/atmosphere labels; they do not ensure that the same object can be recognized when generated again. Conversely, do not invent brands or decoration absent from the script.

## State: Its Condition Now

State records variable facts that require tracking:

- Responsible person, holder, left or right hand, and exact location;
- Intact/damaged, dry/wet/dirty, open/closed/locked, powered on/off;
- Contents and whether they have been seen;
- Current version of readable text/graphics;
- Assembly, seal, remaining quantity, or functional state;
- Cause and effective scope of change.

If an object continuously supports, secures, bears weight for, or conditions a character's action, state also records the **character–object relationship** and effective scope; the storyboard then projects it to starting and ending boundaries. Do not merely state that the object exists or depict it only on a character board. Sitting briefly, leaning against a wall, or reaching to touch something remains a transient shot action and does not create long-term state.

**`craft_default` AST-03**: Prefer recording state changes for transfers, opening/closing, damage, contents, and text changes involving the same object; do not create duplicate props.

## Individuals, Identical Items, and Collections

- Two visually identical white porcelain number plates are exchanged and hidden separately: create two props because their transfer histories must remain independent.
- A stack of ordinary blank notes on a counter is only background: record it by category and quantity rather than assigning every sheet an ID.
- A key moves from Gu He's hand to the attendant's hand: it remains the same prop; update only its holder and holding hand.
- “Another key” explicitly differs from the previous one, but its correspondence to an existing ID is unknown: create a new occurrence record marked `unresolved`; do not reuse the previous key for convenience.

The degree of individualization is a **`taste_option`** selected according to story-tracking and production needs, not the lowest possible count.

## Readable-Text Policy

Every Prop containing text selects one policy explicitly:

1. `exact_readable`: the plot requires the audience to read it; preserve exact characters, language, case/punctuation, and source.
2. `graphic_only`: the label/mark shape matters, but legible text does not.
3. `no_readable_text`: no legible text should appear in the image.
4. `pending_creator_text`: the script requires text but its content is undecided, blocking prompts that depend on it.

When text is a script fact, the asset stage preserves only the policy and source location; it does not polish the wording. A later prompt cannot require both `exact_readable` and global `no_text`.

When the plot displays sensitive information such as a URL, number, or contract terms, state the source, exact displayed text, and creator-approved treatment. Never carry a local reference path or internal address into delivery.

**`craft_default`**: When readable text or a mark points to a **real brand, trademark, institution, or person**, choosing among the four options is not an asset-stage default; it is the creator's decision. Adaptations often carry such proper names directly from the source. Preserving the original, retaining the form without the mark, or substituting a fictional name may each be correct depending on the creator's judgment about rights, genre realism, and delivery channel.

What remains undecided here is **the policy itself**, not the text content, so do not repurpose `pending_creator_text` (which applies when “the script requires text but its content is undecided”). Use the existing unresolved-decision structure: `decisions.jsonl` contains one `decision_kind: unresolved` entry; list the three treatments in `candidate_bindings`, each with support/conflict; use `creator_question` to ask which treatment the creator selects; list blocked downstream work in `downstream_impact`; and keep `creator_acceptance.status` at `pending_choice`. Do not rewrite `text_policy.mode` before the creator chooses, and preserve the original source location. Do not decide or rename it for the creator—unauthorized renaming also rewrites an upstream fact.

This suite does not judge compliance, issue prohibitions, or maintain a built-in brand list. It ensures only that someone makes and records the choice instead of letting the executor silently change it after generation is rejected.

## Contents and Knowledge Are Separate Continuity Lines

The number plate has always been inside the box; that is prop-content state. Gu He learns that it exists only after opening the box; that is new character knowledge. The object's earlier presence does not let the character know early. Conversely, contents do not vanish merely because a shot does not show them.

## Key Props with Explicit Functions

If a prop can protect a character, open a route, store an ability, or prove identity, do not record only appearance. Its state also records where it came from, who holds it now, whether it is enabled, what triggers it, what the audience can see when enabled, remaining uses/progress, consequences of the current use, and when it can be used again. Return an unsourced “suddenly activates at the crucial moment” to the story or asset owner. Adding glow or vibration only in the prompt cannot supply the missing process.

## Synthetic Example: Sheet-Metal Box

`PROP-TIN-CASE`: a long, flat black iron box from palm to forearm length; hinged lid; permanent dent on the front-right corner; used to store the ferry-station number plate. `“潮位 7”` appears inside the lid under policy `exact_readable`.

- `PSTATE-TIN-CLOSED-BADGE-IN`: the box is closed, with the white porcelain number plate inside, on the counter's lower shelf.
- In SC004 Gu He removes it: state changes from `closed` to `open`, and contents change from `badge` to `empty`; record the number plate's holder state separately.
- The text inside the lid becomes visible only after opening, but it is not “created” at that moment. Record audience/character knowledge in a separate reveal record and character-knowledge change.

Counterexample: create `PROP-OPEN-CASE` after opening the box, then `PROP-EMPTY-CASE` after removing the number plate. This cannot express the same box's evolving state and may cause different shots to use false duplicates.

## Check Questions

- After removing holder, open/closed state, and contents, does the prop retain a recognizable form, scale, and material?
- Can the same object's state change step by step along the source script segments rather than teleporting?
- Are several identical items distinguished correctly when story tracking requires it?
- Is readable text exact, sourced, and compatible with the no-text policy?
- Does an object held by a character appear both in prop state and in subsequent storyboard-boundary references?
- If irreversible functional modification creates a new prop, does it retain its source relationship and creator decision?

**`reviewed_invariant` AST-04**: The Reviewer should identify conflated identity and state, unsupported contents or text, and inexplicable transfers. Simple keyword matching cannot replace this judgment.
