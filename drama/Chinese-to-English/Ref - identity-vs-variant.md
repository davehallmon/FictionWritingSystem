# Identity, Versions, and Reuse Decisions

## Table of Contents

- [Three Questions](#三个问题)
- [Identity and State](#持续身份与可变状态)
- [Decision Procedure](#判断步骤)
- [Common Misclassifications](#容易误判的情况)
- [Composite Example](#合成判断例)
- [Decision Records](#决定记录要说明理由)
- [Production Examples](#制作案例说明)

## Three Questions

Do not begin by asking, “Should we create a new file?” Ask these questions in order:

1. **Is the persistent identity the same?** After removing temporary state, is the character, space, or object still the same entity?
2. **Does downstream work need to distinguish a reusable state?** Will the change persist, appear again, or affect reference images,
   storyboard binding, and continuity?
3. **If no new version is created, is a change log sufficient?** Momentary actions, poses, expressions, or camera angles
   normally belong in appearance logs, continuity, or shots; do not create large numbers of asset combinations for them.

The result must be `reuse`, `new_variant`, `new_asset`, or `unresolved`.
**`structural_invariant`**: Do not substitute “handled” for these four outcomes, and do not let unresolved items flow downstream with fabricated IDs.

## Persistent Identity and Variable State

| Category | What usually distinguishes persistent identity | Usually a version or state | Usually does not require a new version |
|---|---|---|---|
| Character | Same person, stable face and body type, permanent features, narrative identity | Clothing, hair arrangement, makeup, injuries, dirt or wetness, age stage, disguise | Momentary expression, pose, gaze, shot size |
| Location | Same spatial geography, relationships among zones, entrances, fixed anchors, principal materials | Reusable viewpoint, dressing phase, time of day, weather, lighting state | One shot angle, focal length, actor position |
| Prop | Form, scale, material, function, and unique markings of the same object or reusable model | Holder, holding hand, location, open/closed state, damage, contents, text, on/off state | The instant it is lifted, left/right position in frame |

This table is a **`craft_default`**, not a formula that creates a record whenever a term appears. Whether a change deserves a new version depends on
duration, reuse, narrative recognizability, and downstream binding needs.

## Decision Procedure

### A. First Exclude Facts That Belong Only to a Shot

“Profile,” “seen from behind,” “high-angle view of the counter,” and “the cup is on the right side of the frame” do not change an asset. If a fact holds only for
one instant in one shot, assign it to the storyboard boundary or keyframe.

### B. Find Evidence of the Same Identity

Align against stable identifiers in an existing ID, narrative continuity, provenance and destination, and unique markings—not display names alone.
Two people both called “attendant” are not necessarily the same person; the same person does not become someone else merely because their form of address changes.

### C. Decide Whether the Change Deserves a New Version

Ask all of the following:

- Does it have a clear cause and source, such as a wardrobe change, injury, power outage, unsealing, or handoff?
- Does it have a clear validity range—from which screenplay passage, scene, or episode does it apply, and where does it expire or remain unknown?
- Must downstream work select it precisely? If a character remains injured across three scenes, a look version is worthwhile; if a finger gets one drop of water on it and immediately wipes it away,
  one change-log entry may be enough.
- Can it be expressed only as a delta without corrupting the base identity? A new version records only the change; it does not rewrite the entity as a different identity.

In `视觉设定.md`, keep the base identity and current variant under the same project entry. A variant records only changes relative to the base identity.
When another document needs to cite a visual fact, use that entry's title directly; use a stable `IMG-...` ID only when citing a visible prompt entry in 《图片提示词.md》.
`IMG-...` does not represent a real image and does not create a hidden provenance claim.

### D. Create a New Asset Only When Persistent Identity Differs

- The screenplay confirms another person, even if they wear identical clothing.
- A space has different geography, entrances, or fixed anchors, even if it belongs to the same building.
- Two identical objects must be tracked independently, or their form, function, or material identity is genuinely different.

When evidence is insufficient, choose `unresolved`; do not fill gaps with common sense.

## Common Misclassifications

### Age, Doubles, and Disguises

- The adolescent and adult stages of one character are usually different look versions. Even if different actors portray them, they may
  retain one character identity, with performance or actor constraints recorded in the look version.
- Twins, clones, and impostors in the story are different characters even when their visual identifiers are similar.
- Prosthetic disguise or uniform disguise is a look version; do not record a “disguised identity” as the person's true identity. When the audience does not yet know,
  the display name may be restricted, but internal facts must remain intact.

### Spaces at the Same Address

If the “transfer-station lobby” and “transfer-station duty room” each have producible geography and entrances, create two locations and connect them
with relationship references; do not force every room in the building into one set of viewpoints. Conversely, the same duty room before and after a power outage remains
the same location; a lighting change does not create a new location.

### Multiple Identical Props

Two visually identical number plates that are kept by different characters and exchanged require two prop identities. Ten white cups with no
continuity requirements can remain one ordinary set-dressing class. Story-tracking needs—not visual similarity—determine whether to create identities for individual items.

### Damage and Modification

Cracks, bloodstains, and inserted documents normally belong to prop state. If an object is irreversibly remade for another function—for example, a door plate
is melted into a key and then used as a new object—a new asset may be proposed while preserving its derivation relationship to the original.
The creator must accept this decision.

## Composite Decision Example

`CHAR-GUHE` and `LOOK-GUHE-WORK` already exist. In this episode, Gu He puts on an orange raincoat to enter the transfer station; in Scene 3, the raincoat's
right shoulder becomes wet.

- The orange raincoat spans two scenes and will be used in reference images: choose `new_variant`. The base identity remains Gu He; this is not a new character.
- The wet mark on the right shoulder lasts only half a scene: first record a continuity change; do not automatically generate a third look version.
- If the next episode must reproduce the wet mark precisely and bind it to a reference image, the creator may then accept a wet-raincoat look version.

If the text says only “the person in the orange raincoat” and cannot prove that this is Gu He, the decision must remain `unresolved`.

## Decision Records Must Explain the Reason

Every decision must show at least the source scene, selection, stable evidence, delta, cause, validity range, and downstream impact.

- `new_asset` must explain why an existing asset cannot be reused.
- `new_variant` must identify what remains unchanged in the base identity.
- `reuse` must explain how the existing version covers the current fact.

Write facts that can be determined directly from the screenplay and existing visual facts into `视觉设定.md`. When multiple choices are genuinely valid, mark the item
“unresolved” and list the downstream impacts that would change; revise the main text only after the creator chooses. Do not fabricate decision IDs, acceptance states, or separate decision files.

**`reviewed_invariant` AST-04**: The reviewer checks whether identity markers and temporary states have been conflated; “fewer assets is better”
is not an evaluation standard.

## Production Example Notes

Qualitative examples across a complete production pipeline show that the following naming and separation practices can reduce duplicated assets caused by wardrobe changes, injuries, and
viewpoint changes. These are adjustable common practices, not fixed formats:

- **Version-suffix naming**: place the same character's state or look after the identity name—for example, “Su—uninjured after the fire”
  or “Qi—red evening gown.” Downstream workers can immediately see the identity and current version.
- **Distinguish spaces by viewing direction**: the same location may be named by direction or zone—for example, “hospital corridor (north)” and
  “office (east).” Each viewpoint can bind an independent reference image.
- **Stable identification fields**: gender, age range, and character category may support production tracking. A large span such as adolescent to adult
  is usually handled with separate look versions.
- **Reference-image binding**: bind reference images individually for characters and spaces that require stable recognition. Treat extras without individual continuity
  as ordinary set dressing; they do not require identities.
- **Layered naming**: protagonists may use full names; functional characters may use surname + role; background-only figures may use type + number.
  Asset names and names inside descriptions must agree; never write A's name while describing B.
- **Large states spanning multiple episodes**: if captivity or severe injury persists across multiple episodes, create a new look reference directly. If the state occurs
  within one shot only, keep it in shot boundaries or the change log first; do not expand the asset table prematurely.
