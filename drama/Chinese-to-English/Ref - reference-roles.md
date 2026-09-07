# What a Reference Image May Determine

Binding a reference image tells downstream work “which elements should follow this image.” Without explicit boundaries, an identity reference may improperly control clothing, composition, background, or text.

## Every Reference Answers Five Questions

1. What are its stable `REF-...` slot and explicit order?
2. What are its visible locator and Chinese name? For an in-project image, write a project-relative path such as `输入/参考图/江辰定妆.jpg《江辰定妆照》`. When the creator prepares the image outside the project and attaches it during generation, name the corresponding `IMG-...` board or `SHOT-...` frozen keyframe.
3. Does this use reference identity, look state, geography, composition, scale, effect, starting frame, ending frame, or style?
4. Which visible content may follow the reference?
5. Which identities, text, number of people, props, and spatial anchors must not change with it?

Question 3 has a fixed location in creative documents: the `REF-...` slot's `用途` field, whose value must be one of the nine terms in the table's left column. It answers both the creator's question—“which storyboard starting frame and which character, prop, or location images should accompany this shot?”—and the executor's question—“which vendor role does this image map to?” When one image has two functions, use two slots rather than writing “reference everything.”

| Purpose | May control | Must not control by default |
|---|---|---|
| Identity | Stable facial structure, body type, and identifying marks | Temporary clothing, pose, scene, or text |
| Look state | Approved clothing, injury, damage, moisture, or dirt | New identity, unsourced props, or background direction |
| Geography | Entrances, zones, fixed anchors, and directional relationships | Temporary characters or plot state |
| Composition | Frame occupancy, sight-line arrangement, side of frame, and negative space | Character identity, clothing, or prop text |
| Scale | Relative scale among subjects or between subject and environment | Style, identity, quantity, or action result |
| Effect | Approved effect form, range, and material | Disappearance, duplication, or deformation of nontarget objects |
| Starting frame | Composition and state at the start of the shot | Actions and final states that have not yet occurred |
| Ending frame | The explicit endpoint of the shot | A new endpoint or a result not owned by the shot |
| Style | Color hierarchy, materials, shadow edges, depth of field, and density | Identity, fixed geography, plot, or prop text |

The boundary between `身份` and `造型状态` is whether something changes within the episode, not whether it counts as clothing. When one character board fixes both appearance and a look that remains unchanged throughout the episode, use one `身份` slot and list `本集造型` explicitly under `控制`; this is the suite's established convention. Create a separate `造型状态` slot only for a state that changes during the episode, such as a wardrobe change, becoming soaked, damage, or blood staining, and let it control that specific change. The governing authority is always the scope written in the slot's own `控制` field, not the literal meaning of its purpose label.

For a prop board, choose `身份` or `造型状态` according to whether the image determines “which object this is” or “which state it is currently in.” Persistent identifying marks—form, color scheme, cracks, or chipped corners—belong to `身份`. Story-dependent states such as screen on/off, open/closed, dirt, moisture, or degree of damage belong to `造型状态`. When both must be fixed for the same prop, use two slots.

## Observation Boundaries

A verifiable description from the creator or rights holder may serve as textual evidence. When the runtime is authorized to inspect a reference image, it may report actually visible content. Without either source, keep the reference “unverified”; do not claim that watermarks, text, cropping, or identity passed review. Negative prompts cannot erase pixels already present in a reference image.

An actual reference image uses a stable `REF-...` slot, not `IMG-...`; the latter prefix belongs exclusively to visible prompt headings in 图片提示词.md. An image the creator attaches personally uses a `PLAN-...` slot with the same syntax as `REF-...`, except that its path is replaced by the corresponding `IMG-...` or `SHOT-...` entry. All five questions still require answers; Question 2 answers “which decided fact does this image depict?” rather than “where is the file?” The table's nine purposes apply equally to both slot types. For multiple actual images, every slot binds an explicit order, project-relative path, Chinese name, purpose, controllable scope, and prohibited scope. A contact sheet is only a browsing wrapper and does not change each image's function. Start/end-frame input uses only the starting frame by default. When an ending frame is genuinely required, it may project only the endpoint already written in `SHOT-...`; it cannot invent a result.

For timing of audience knowledge, see [Audience Reveals](audience-reveal.md). For whether a pickup may replace a master, see [Pickups and Alternates](pickup-and-alternate.md).
