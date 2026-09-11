# Translating Visual Direction into Production Form

Visual style is not a label prepended to a prompt. First decompose the creator-accepted `visual_direction` and
`production_profile` into observable, reviewable choices; then let each owner project only what its stage needs.
The same story fact may have multiple production forms. This document supplies decision dimensions, compositional differences, and responsibility boundaries—not fixed style packages.
Execution details for individual forms live in six cards under `references/form-cards/`; this document covers only how to choose,
what form changes in prompt composition, and what each stage carries forward.

## Table of Contents

- [Rule Level of Form Cards](#rule-level-of-form-cards)
- [Production-Form Card](#first-write-a-production-form-card)
- [Environmental Physics and Identity Form](#first-lock-environmental-physics-and-identity-form)
- [Executable Vocabulary and Form Cards](#select-executable-vocabulary-by-form)
- [Form Differences in Prompt Composition](#how-prompt-composition-changes-with-form)
- [Cross-Stage Transmission](#transmitting-the-same-intent-across-stages)

## Rule Level of Form Cards

Form cards have the same standing as genre cards: **they are `craft_default` by default** and the creator may override them with an explanation. A form card
does not create IDs or new `structural_invariant` rules. Items called “hard rules/constraints” in a card mean that it projects an **already registered**
identity or continuity invariant (see [knowhow-index.md](knowhow-index.md)) and follows that original rule's level. Proportions, rig capabilities, head-to-body ratio, and similar constraints
are **project production constraints** that take effect only after the creator writes them into “Project Visual Direction” in `视觉设定.md`; they are not suite-level rules.
A reviewer must not block delivery based solely on a form card.

## First Write a Production-Form Card

Record nine items for the current series or a local variant. Every item must map to an executable field at some stage.
If it cannot, it is aesthetic conversation; delete it before filling the card:

- **Narrative responsibility**: what this form helps the audience understand or feel faster; not merely “premium” or “cinematic.”
- **Carrier of identity anchors**: what keeps characters recognizable across shots—silhouette, line, proportion, structural difference, or material.
- **Carrier of continuity**: which fields must pass through every shot and which may be omitted; answers vary greatly by form.
- **Layer separation**: what belongs to identity, environment, movable, and effects layers, and who owns each shared fact.
- **Form and recognition**: permanent identity anchors in silhouette, proportion, line/surface, clothing, and props; which may vary by shot.
- **Material, light, and color**: how physical or illustrated materials respond to light and what information color relationships carry; do not list quality adjectives.
- **Motion budget**: what requires full animation and what may use a hold pose, local loop, parallax, effects layer, or editing.
- **Sound and text**: what performance, sound sources, narration, and on-screen text each carry; readable text still follows the asset text policy.
- **Variable and invariant**: stable cross-episode items, scene-variable items, creator overrides, and unknowns requiring an experiment first.

A style name, model code, vendor field, or style code cannot replace this card. Different upstream codes may describe the same presentation direction,
and one code may be redefined by project notes. If the creator provides only a style label, the owner requests the smallest observable clarification
or retains unresolved items as candidates rather than inventing an aesthetic system.

To determine whether a form description contains substance, ask only: **Which field does it change?** If deleting it
leaves the prompt byte-for-byte unchanged, it is only a label.

## First Lock Environmental Physics and Identity Form

For heterogeneous bodies, identity swaps, transformation, underwater or zero-gravity settings, miniaturization, or nonhuman characters, first write a physics card that style language cannot override:

- **Body topology**: which limbs/forms currently exist, what explicitly does not exist, and where contact and force points are;
- **Identity occupancy**: whose consciousness/personality occupies which body or appearance, how others currently recognize them, and when changes are permitted;
- **Environmental medium**: how current, buoyancy, gravity, wind, viscosity, and scale change stillness, movement, clothing/hair, and props;
- **Motion grammar**: select hovering, tail propulsion, clinging, gliding, and other actions appropriate to the current body; remove terrestrial action terms that conflict with physics;
- **Hard continuity items**: how identity form, breathing/load state, holding method, language locks, and adjacent boundaries carry across shots;
- **Soft presentation items**: temperature, brushwork, depth of field, and light effects may vary but cannot erase the hard items above.

These constraints belong first to creator/story and asset facts, then are projected by storyboards and video prompts. Do not let the prompt stage
invent body rules locally. Ordinary emotional or clothing changes do not require a heterogeneous-physics card.

## Select Executable Vocabulary by Form

A form card is selected, not inherited from genre or an upstream label. Use the table to locate one card, then write fields according to it.
One project may use different cards for different segments, but exactly one card applies to each segment.

| Form | Form card | What this form determines first | What is easiest to lose |
|---|---|---|---|
| Live action | [Live Action](form-cards/实拍.md) | Buildable space, real light sources, performable action, and recordable sound sources | Shot-to-shot comparability of look state |
| 2D motion comic (limited animation) | [2D Motion Comic](form-cards/二维动态漫.md) | Shape language, color-block and shadow regions, movable layers per shot | Silhouette-level identity anchors |
| Stylized 3D | [Stylized 3D](form-cards/风格化三维.md) | Proportions, rig pose limits, contact, and camera space | Contact points and weight results |
| Ink-wash brushwork | [Ink-Wash Brushwork](form-cards/水墨笔触.md) | Value hierarchy, negative-space position, and edges that must not dissolve | Required geography and held objects |
| Chibi expression (including chibi educational/explainer shorts) | [Chibi Expression](form-cards/Q版表达.md) | Proportion system, one cause per shot, symbol layer, and text reserve | Causal precision and scale relationships |
| Chinese anime | [Chinese Anime](form-cards/国漫二次元.md) | Enumerable structural differences among characters, atmospheric-color boundaries, and lip-sync strategy | Distinction among characters |

For hybrid forms—for example, 3D characters with painted backgrounds or live action with brushwork post-processing—do not create a seventh card. Use two cards and
**declare item by item which owns identity, depth, edges, light, and motion**. Two layers determining the same fact is the most expensive hybrid-form error.

## How Prompt Composition Changes with Form

Form does not change prompt section order. It changes **which sections expand, which may collapse, and the default values of certain sections**.
When applying the same recipe to different forms, make these three adjustments.

**1. Different carriers require different identity writing.** Live action records look state rather than facial appearance; 2D records silhouettes and color blocks;
3D records proportions and rig boundaries; ink wash records edges that must not dissolve; chibi records head-to-body ratio and amplified markers. Chinese anime must describe
structural differences from other characters in the same work—the only form requiring comparative writing, because polished style tends to flatten character differences.

**2. Continuity carries different fields.** Choose mandatory shot-to-shot fields by form; not every project carries the same state list:

| Form | Mandatory continuity | Usually omittable |
|---|---|---|
| Live action | Look layers and neatness, wetness/dirt/injury, held objects, light-source time and direction | Hidden inner layers, dressing that cannot be compared |
| 2D motion comic | Silhouette color blocks, shadow regions, outline rules, movable-layer list for the shot | Realistic materials, exact lighting angle |
| Stylized 3D | Proportional silhouette, material regions, contact points, axes, and camera height | Secondary deformation, unseen rear surfaces |
| Ink-wash brushwork | Silhouettes that must not dissolve, value hierarchy, held objects, required geography, negative-space position | Exact light direction, texture details |
| Chibi expression | Head-to-body ratio and relative scale, primary color blocks, amplified markers, reserved text area | Realistic materials, background detail |
| Chinese anime | Face/eye/hair structure, iris color and highlight shape, fixed accessories, atmospheric color and light-source temperature | Background depth, non-load-bearing decoration |

**3. Motion defaults differ.** Live action defaults to full action, so write constraints. 3D can default to full action,
but the camera is its most expensive layer. 2D motion comic and ink wash default to holds, so specify **which layer is the exception**.
Chibi defaults to one cause per shot. Chinese anime concentrates its full-animation budget on emotional-turn shots and sustains the rest with loops and effects layers.
Omitting this section has predictable consequences: hold-default forms become full-frame drifting, while full-action forms become lists of action words with no contact points.

Do not handle form differences by “adding a style prefix.” A prefix changes retrieval labels; form changes
required and omittable fields. Only the latter is executable downstream and reviewable.

## Transmitting the Same Intent Across Stages

| Stage | Added by this stage | Must inherit | Must not overreach |
|---|---|---|---|
| develop / directing brief | Narrative responsibility, form hypothesis, motion budget, and unresolved experiments | Creator direction, genre, and audience promise | Vendor fields, shot-level facts |
| assets | Silhouette, materials, layer separation, stable proportions, and version differences | Identity, geography, text policy | Shot composition and action endpoint |
| image-prompts | Single-frame projection of form/material/layers/light and color | Accepted assets and current purpose | Sequential action |
| storyboard / keyframe | Attention, hierarchy, occlusion, movable layers, and frozen boundary | Screenplay information permissions and asset bindings | Rewriting character state with style terms |
| video-prompts | Motion layers, contact, rhythm, sound sources, and result | shot purpose, start/end boundaries, form budget | Writing back into shot or asset authority |
| review | Check whether narrative responsibility reached visible fields | Exact artifact refs and creator overrides | Replacing evidence with personal preference |

This table applies to every form. Each form card's “cross-stage transmission” section records the one additional item a stage must write for that form.
Read only the current form's card rather than loading all six into context.

During review, do not ask whether a style name appears. Ask whether narrative responsibility was projected into executable form, layers, material, light, action, or sound;
whether mandatory continuity fields were selected for this form rather than copied from another; whether one owner writes each decision;
and whether the agent reselects rather than copying the entire vocabulary when the genre or project changes.
The reviewer cites source facts, selected production intent, and target artifact locations separately, then distinguishes contract breach, implementation deviation, and personal taste.
If an accepted per-shot/form budget is infeasible, return to its owner for approval; do not treat splitting the shot or changing form as already authorized.
