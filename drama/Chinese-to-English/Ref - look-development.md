# Look Development: Turning Visual Direction Into Comparable Representative Frames

Look Development does not apply one style label to an entire production or allow reference images to take control of characters and plot. It projects the creator-approved `visual_direction` and `production_profile` into a small set of **textual style-frame specifications**, allowing characters, locations, and high-pressure scenes to share an observable visual language before formal storyboarding. This stage produces only specifications and prompts. When the creator requests actual image generation, hand the work to `$short-drama-produce` and obtain explicit confirmation of its exact task preview.

## When It Is Worthwhile

- The production form has been selected, but material, lighting and color, edges, image density, or depth-of-field preferences remain only adjectives.
- Character boards, location boards, and storyboards work individually but do not appear to belong to the same production.
- A visual style works for static specification art, but its ability to preserve performance, identity anchors, or layers of conflict remains unknown.

An ordinary project may use its approved visual direction directly; this stage is optional. When needed, prioritize three kinds of comparison:

1. **Character-performance test frame:** Are identity anchors, skin or line treatment, gaze, and small performance cues still legible?
2. **Core-location test frame:** Can spatial hierarchy, material response, light-source logic, and color relationships be reused?
3. **High-pressure-scene test frame:** Can the direction carry occlusion, conflict, and a center of attention, or is it suitable only for static display?

## Write the Observable Direction First

Describe each candidate direction through:

- **Stable elements:** Shape language, material treatment, color hierarchy, shadow edges, depth-of-field tendency, or image density that must remain consistent across characters, locations, and high-pressure scenes.
- **Variables:** Warmth, contrast, negative space, lighting ratio, and motion layers that may change by scene.
- **Narrative responsibility:** What these choices help the audience recognize or feel.
- **Failure signals:** Observable risks such as swallowed identity anchors, flattened ensemble hierarchy, or conflict scenes reduced to atmosphere.

If removing the style name causes no change in descriptions of material, light, color, edges, or space, the direction is still only a label. After the creator selects a direction, record its observable stable elements, permitted variations, and failure signals under “Project Visual Direction” in `视觉设定.md`. Candidate prompts cannot rewrite character identity, location geography, or plot facts upstream.

## Permission Boundaries

`$short-drama-image-prompts` expresses an approved direction as a general-purpose image prompt with `purpose: lookdev_frame`. A style reference has the `role` of `style` and may control color hierarchy, material treatment, shadow edges, depth-of-field tendency, and image density. Its `must_not_control` field must protect character identity, fixed scene geography, plot state, prop text, and information reveals.

A character-performance frame remains bound to the exact character and look; a location frame remains bound to the exact location and viewpoint; a high-pressure scene remains bound to the approved scene, characters, and script source. A style frame has no authority to invent these facts or overwrite assets or scripts upstream.

## Comparison and Acceptance

Select one or more frame types according to current project risk. Display shared rules, local differences, expected narrative effects, and unknown risks side by side only when genuinely comparing across characters, locations, or pressure conditions. Do not impose a fixed grid, frame count, or ratio of shot sizes. If the creator later supplies authorized production observations, revise the project only within the exact direction, prompt version, reference slots, and production configuration observed. Without observations, report textual risks only; do not claim that an image succeeded or failed.

Acceptance applies to observable visual choices, not a vendor, model name, parameter, or task result. All binary media remains in the external production stage and does not enter the textual delivery package.
