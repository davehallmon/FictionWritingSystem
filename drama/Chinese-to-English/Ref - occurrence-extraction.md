# Extracting Asset Occurrence Records from a Script

## Contents

- [Purpose](#目的保存证据不抢先下结论)
- [Check Segment by Segment](#逐段检查而不是只找名词)
- [Fact Layers](#事实分层)
- [References](#称谓代词和匿名对象)
- [Asset Judgment](#出现不等于视觉资产)
- [State](#状态摘取要点)
- [Completeness](#完整性检查)

## Purpose: Preserve Evidence Without Reaching Conclusions Prematurely

An occurrence record states “what a script segment requires at a particular point”; it is not the asset identity itself. Record the occurrence first, then determine which asset it represents. This avoids splitting several outfits worn by one character into several people or incorrectly merging two people who share the same form of address.

**`structural_invariant` AST-01**: Every occurrence judgment must point to the exact scene ID in `剧本.md` and state its basis using action, dialogue, or a necessary short quotation. Line numbers may aid reading but cannot replace a stable scene source.

## Check Segment by Segment, Not Merely for Nouns

Inspect every production-relevant script segment and answer six questions:

1. **Who or what must be seen or heard?** A character, group, animal, location, or manipulable prop.
2. **How does it appear?** `on_screen`, `voice_only`, `represented` (appearing in a photograph, screen, or portrait), or `mentioned_only`.
3. **What can be seen directly at this moment?** Extract only appearance, state, location, and action consequences already provided by the script.
4. **What must production realize?** Clothing, injuries or dirt, readable text, contents, functional state, key entrances, and similar requirements.
5. **Why does it matter?** Recognition, action, information reveal, relationship and power, handoff, atmosphere, or ordinary set dressing.
6. **Where does it come from and where does it go?** Incoming state, changes within the scene, and ending state. If a change occurs, reserve only a pointer to the continuity-change record; do not create a second fact in the occurrence record.

One action sentence often introduces several kinds of assets. For example, consider this synthetic script segment:

> Gu He pushes open the north door of the old ferry-station duty room and places the chipped white porcelain number plate into a sheet-metal box. Inside the lid are the words “Tide Level 7.”

At minimum, record: Gu He appears on screen; the old ferry-station duty room appears, and the north door may be a fixed spatial anchor; the white porcelain number plate is chipped; the sheet-metal box is opened; and the text inside its lid must be preserved. Do not create separate assets for “north door,” “chip,” and “tide level.”

## Fact Layers

Separate occurrence-record content by source:

| Content | Field purpose | Form |
|---|---|---|
| Script segment and scene location | Source | Scene ID plus action/dialogue label or necessary short quotation; do not copy the whole passage |
| Visible fact explicit in the script | Visible fact | Brief paraphrase pointing back to the same scene |
| Proposed bound asset | Asset judgment | Retain only a conclusion of reuse, new variant, new identity, or unresolved |
| Continuity change | State change | Point to the corresponding identity and before/after state in `视觉设定.md` |

Do not disguise inference as a visible fact. A directly entailed result still needs a stated basis. For example, “the box lid is pushed open” may be recorded as `open`; “Gu He feels guilty” cannot become an asset fact merely because she lowers her head.

When no decision has been reached, mark the corresponding entry “未决” and list candidates, missing evidence, and impact. For a continuity change that will occur only in the future, write only a “需要同步” note; do not create a placeholder record for a file that does not yet exist.

## Forms of Address, Pronouns, and Anonymous Objects

**`reviewed_invariant` AST-02**: Whenever two candidates are both plausible, do not bind yet.

- If the source says “she” but the segment contains no unique antecedent, preserve `surface_form: 她`, mark the decision `unresolved`, and list candidates and required confirmation.
- If “the person in the raincoat” is later named, a merge may be proposed, but evidence from both earlier and later script passages must be shown. Identical clothing alone cannot establish that they are the same person.
- “Another key” establishes that it is not the previous key, but does not establish whether it corresponds to an existing prop ID. Create a separate occurrence record first; do not reuse the previous key.
- When the same person is referred to alternately by title, relationship, and name, an alias may enter the character asset only after creator acceptance.
- Initially handle group labels according to production purpose. “Passengers waiting for a bus” with no individual continuity may be a group or ordinary set dressing. A person who later takes a key prop should receive a separate character record.

Do not make a low-confidence guess to “keep the process moving.” Preserving unresolved items prevents an incorrect identity from being amplified downstream into reference images, storyboards, and video prompts.

## An Occurrence Is Not Necessarily a Visual Asset

- `voice_only` requires character or voice facts but not necessarily a look binding in this scene.
- `represented` may require a historical look for the same character or only an unidentifiable photograph. Follow the dramatic requirement; do not assume the face is visible.
- `mentioned_only` usually remains only in story tracking and does not trigger an image asset. If dialogue requires the audience to read a document, also create a prop occurrence record.
- Ordinary tables and chairs in an environment may be marked `set_dressing`; promote them to props only when they carry action, recognition, or continuity.

**`craft_default` AST-06**: Only facts that change recognition, reuse, prompts, shots, or continuity belong in asset records. If the project has a special production reason—for example, branded set dressing requires item-by-item approval—state the reason and adjust accordingly.

## Key Points for State Extraction

### Characters

Record look clues for this occurrence, injuries/dirt/moisture, disguise, carried objects, and story function. Do not invent facial structure, age, or color combinations here; let the creator decide recognition points missing from the definition table.

### Locations

Record the location's form of address, interior/exterior status, visible zones, entrances, fixed anchors, and the time of day, weather, and light sources explicit in the script. “Low-angle view of the door” is shot intent, not a new location fact.

### Props

Record form, material, scale clues, unique marks, holder and location, which hand holds it, open/closed and on/off states, damage, contents, and readable text. Preserve text exactly and state the candidate text policy; do not privately polish dramatic evidence.

## Completeness Checks

- For every production-relevant script segment in the index, record extracted content or write `no_asset_change`.
- If an action in a script segment changes state, at least one change candidate must be discoverable.
- When the same object uses different forms of address, it has not been silently duplicated or merged.
- A noun that is only mentioned does not expand the visual asset table without cause.
- Every proposed binding remains in proposal state until the creator accepts the decision.
