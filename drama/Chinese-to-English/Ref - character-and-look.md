# Character / Look Design

## Table of Contents

1. Division of responsibilities
2. Character: minimum stable identification set
3. Look: one compatible appearance combination
4. Optional voice direction: identity anchors are not the current scene's delivery
5. Production form and the expressibility of identity anchors
6. Synthetic example: Gu He
7. Practical checks for the character specification set

## Division of Responsibilities

- **Character** answers, “Who does this person remain, and how are they recognized again?”
- **Look** answers, “What complete appearance does this person have during a defined period?”

Separating the two preserves reusable character identity through wardrobe, injury, dirt/wetness, and age changes, while allowing image prompts
and storyboards to select one compatible look precisely.

## Character: Minimum Stable Identification Set

Select persistent anchors from the screenplay and creator reference that are sufficient to distinguish the person:

- Narrative identity and relationships (for disambiguation, not as a substitute for appearance);
- Stable face/head proportions, body silhouette, and permanent features;
- Stable elements such as baseline hair texture and hairline; specific styling may belong to Look;
- Permanent accessories only when they genuinely do not vary with Look;
- Persistent performance/voice facts may enter the specification set for later prompts or casting, but must not masquerade as visible appearance.

Anchors must be **distinctive and observable**. “Beautiful young woman,” “domineering-CEO aura,” and “cinematic feel” are all insufficient for identification.
Do not overspecify skin tone, age, facial features, or body traits the screenplay does not require; expose such gaps as
`creator_decision_needed`.

The anchor set must contain at least one feature valid in **profile** and one valid from the **back**. Many shots show only a side view, back view, or
long shot, so features readable only from the front—eye spacing, iris color, lip shape—cannot be the sole identification channel. Silhouette and center of gravity,
hairstyle silhouette and hairline shape, shoulder/back line, and the form of a fixed accessory can serve these directions. Example:
`["方额窄下颌", "后颈发际收成尖角", "右肩比左肩低约两指、起步时先出右肩"]`—the first works from the front,
the second from the back, and the third in profile and from behind.

Also record a **comparable scale ordering** for the entire cast: who is taller than whom, by what approximate magnitude, plus one absolute reference point. Example:
“A is tallest; B is about one head shorter than A; C is another half-head shorter than B; when A stands straight, the crown aligns with the top of the doorframe.” Character owns this ordering;
shoes, padded coats, and updos do not rewrite it (those belong to Look). When the screenplay gives no height
relationship, expose `creator_decision_needed` for the creator to decide; do not fill it from a character-sheet template's default body type.

Character relationships help explain who controls space, who watches whom, and who protects or attacks whom, but they **do not automatically determine attractiveness, skin tone,
body type, or moral appearance**. A protagonist does not become beautiful because of a “protagonist” field, nor does an antagonist automatically become ugly.
When visual hierarchy is needed, derive it from creator-accepted social position, occupational wear, silhouette distinctions, wardrobe function, posture, and
blocking. Aesthetic idealization, exaggeration, or counter-typing are creator choices and cannot be silently completed from relationship labels.

**`reviewed_invariant` AST-04**: Temporary bruises, uniforms, rainwater, and today's makeup must not become persistent Character
anchors; otherwise the same person will be misidentified after recovery.

## Look: One Compatible Appearance Combination

One Look contains only elements that can coexist:

- Clothing layers and footwear;
- Hair styling, makeup, and disguise;
- Injuries, bandages, stains, wetness, and weathering;
- Visible body-bound accessories; handheld props remain bound to Prop and are not absorbed into Look;
- cause, valid_from, valid_until, and source refs.

When writing a Look, first cite the Character identity, then record only the differences from the base/previous Look. Do not duplicate the full
facial description into a second authority.

## Optional Voice Direction: Identity Anchors Are Not the Current Scene's Delivery

**`AST-07 · reviewed_invariant`**: When a project must preserve a voice across episodes, Character may record `voice_direction`: language/dialect range,
an **audio-reference binding authorized by the creator**, criteria for selection and acceptance, and accepted proper-noun pronunciations. Tension, rain exposure, injury,
whispering, stress on one line, and temporary volume belong to scene/dialogue delivery and must not be fixed as voice identity. Voice changes, age spans, or
disguises that persist across segments are recorded as sourced variants with validity ranges.

Reference audio—not a prose description—carries timbre. With no reference, retain `reference: null` and mark “awaiting selection”;
do not use adjectives as a substitute for vocal identity. A reference binding must state what is borrowed, what must not carry over
(the reference's emotion, recording space, and background content never enter identity), and the evidentiary stage reached.
See [Voice Direction](voice-direction.md). Write voice direction directly in the corresponding character entry in `视觉设定.md`; do not create
a separate voice table or second authority.

Text references can guarantee only that characters, dialogue, voice direction, and reference relationships were not rewritten. They cannot guarantee any real synthesis result,
lip synchronization, or timbre reproduction. References use visible IDs in `视觉设定.md`; do not place URLs, external task fields, or service parameters in the specification.
Reference audio itself remains under `输入/`; do not copy it into `视觉设定.md` or public delivery.

**The asset stage does not generate audio or invoke any speech, synthesis, or cloning service.** Records first enter the file and receive creator
confirmation. Actual TTS belongs to `$short-drama-produce` and requires explicit confirmation of the displayed job preview.

### When a New Look Is Worthwhile

**`craft_default` AST-03**: Propose one when any condition holds: it persists across multiple blocks/scenes; will be reused;
needs an independent character reference image; changes audience recognition/story information; or must be bound precisely downstream. Momentary expressions, poses,
gaze, and hand position are handled by shot/continuity and normally do not create a new Look.

### Looks Must Not Contaminate One Another

- If “work uniform” and “ceremonial dress” do not overlap in time and space, they cannot appear in the same Look;
- A bandage takes effect only after its source block; earlier shots cannot bind it in advance;
- Removing a coat leaves the same Character but should switch Look or record a traceable layer delta;
- If rain causes only a brief local wet mark, use a delta. If it persists across episodes and needs visual reproduction, promote it to a Look.

## Production Form and the Expressibility of Identity Anchors

Before writing the minimum stable identification set, read “Project Visual Direction” and the confirmed production form in `视觉设定.md`. If it is undecided and would
materially affect identification channels, present choices to the creator rather than inventing one from conversational memory.

The reason is direct: **form determines the channels through which the audience recognizes a person**, and therefore which anchors can be expressed at all in the project.

| Primary identification channel | Worthwhile anchors | Anchors that remain invisible |
|---|---|---|
| Facial structure | Facial proportions, relative relationships among brows/eyes/nose/lips, volume of jaw and cheekbones | Scale differences visible only in extreme long shots |
| Silhouette and line | Outline and shoulder/back center of gravity, hairstyle silhouette and hairline shape, fixed-accessory form, clothing silhouette, load-bearing gait | Subtle facial asymmetry, a small pale mole, marks dependent on realistic skin texture |
| Material and surface | Comparable surface states of skin/hair/fabric, long-term wear | Volume differences that require soft transitions to read |

### Boundary: Form Selects the Channel; Identity Determines the Facts

- **`reviewed_invariant`**: Form may change the **expression channel and granularity** of anchors but cannot rewrite identity facts.
  “Difficult to draw” cannot turn a fifty-year-old into a twenty-five-year-old or a heavy build into a slender one; nor can attractive silhouettes justify adding
  scars, heterochromia, or nonexistent accessories.
- If an accepted identity has no reliable expression channel in the current form, mark “creator decision required.” The creator decides
  whether to change the form or identity; the asset stage does not adjust it silently.
- The same applies to Look: form determines how finely clothing layers and material responses can be expressed, but not which items compose the Look or
  its cause, valid_from, and valid_until.
- Form likewise does not rewrite geography, prop ownership, readable-text policy, or story state. These belong respectively to Location/View,
  Prop/State, text policy, and the write/develop owner.

### Template Slots Must Not Override Identity Anchors

**`reviewed_invariant`**: Template slots must not override accepted identity anchors. When a template default conflicts with the current identity,
**identity takes priority and the template yields**.

Synthetic example: Character A's anchors are approximately fifty years old, heavily built, with slightly slumped shoulders. If a character-sheet template
mechanically fills every record with “nine-head ideal proportions and extremely long, slender legs,” it rewrites Character A's identity without any creator decision.
Because every character carries the same sentence, downstream work will read it as style consistency rather than a conflict. Even if Character B genuinely
is slender, that fact should come from B's current visual specification rather than a template default.

Diagnostic method: compare the same batch of character records side by side and find descriptions **repeated verbatim but unrelated to the individual character**. If a sentence cannot be traced to
a current visual specification, delete or rewrite it as the character's real anchor and explain the change in the preview.

## Synthetic Example: Gu He

Character `CHAR-GUHE` currently has these anchors: narrow long face, small notch at the tail of the left eyebrow, naturally curly black hair, and slightly forward shoulders.
These anchors do not change with this episode's wardrobe.

- `LOOK-GUHE-WORK`: gray-green work jacket, dark trousers, hair tied low; valid during duty at the transfer station.
- `LOOK-GUHE-RAIN`: old orange raincoat over the work clothes, hood down; put on before leaving in SC004
  and removed in SC006.
- Wet mark on the right shoulder in SC005: if it lasts only several shots, record it as a delta pointing to `LOOK-GUHE-RAIN`, not
  `CHAR-GUHE-WET`.

Counterexample: “woman in an orange raincoat, wet hair, injury on her face” is written directly as Character identity. Once the raincoat
is removed, the hair dries, and the wound heals, the person loses every supposed “identity anchor.”

## Practical Checks for the Character Specification Set

- After removing this episode's clothing, injuries, and dirt, can this person still be distinguished from other characters?
- Does every Look cite exactly one Character, and can all of its internal states coexist?
- Does each look change have source/cause/validity rather than an aesthetic wardrobe substitution?
- Were identical display names merged incorrectly or different forms of address split incorrectly?
- Do handheld objects remain owned by Prop/State rather than buried in the character description?
- Did the creator accept new identity anchors rather than the system silently completing them?

Extras may use a group Character according to production needs. Once an individual has dialogue, a critical handoff, or cross-shot continuity,
propose an independent identity. This granularity is a **`taste_option`**, but the choice must satisfy story tracking.
