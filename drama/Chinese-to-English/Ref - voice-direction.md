# Voice Direction

## Table of Contents

- [Reference Audio Is the Carrier](#参考音频是载体)
- [The Boundary Between Identity and Performance](#身份与表演的界线)
- [What One Reference Recording Can Determine](#一段参考音频可以决定什么)
- [Binding Does Not Mean Listening](#绑定不等于听过)
- [Selection Criteria](#选型判据)
- [Creating Distinction](#写出区分度)
- [Proper-Noun Pronunciation](#专名发音)
- [Variants: Disguise, Age, and Changes Across Segments](#变体伪装年龄与跨段变化)
- [Rendering Rules for voice-casting.md](#voice-castingmd-的渲染规则)

`voice_direction` is part of the Character record (`AST-07`) and remains stable across episodes. How the character speaks in a particular scene is performance,
determined line by line by the voice script from `$short-drama-write`.

## Reference Audio Is the Carrier

A short drama's vocal identity is carried by **one reference recording**: an actor's audition, an entry from a voice library, or a cloning source authorized by the creator.
Text does not carry timbre—it handles two things that reference audio cannot:

1. **Selection and acceptance**: which criteria to use when choosing a reference, and whether a cloning result qualifies as this character;
2. **Proper-noun pronunciation**: how to pronounce names absent from the reference audio.

Therefore, `voice_direction` uses `reference` as its primary field. When no reference audio exists, retain
`reference: null` and mark it “awaiting selection”—**do not use a prose description as a substitute for vocal identity**.
When downstream workers search from a string of adjectives, every returned voice differs even though the record appears complete.

## The Boundary Between Identity and Performance

One-question test: **Does this feature remain when the character sits quietly and says one inconsequential sentence?**

If yes, it is identity. If not, it is performance and belongs to the scene and dialogue.

| Part of identity | Part of performance |
|---|---|
| Pitch range, timbral texture, perceived age | Unsteady breath caused by running in this scene |
| Speaking-rate and pause habits, phrase-ending treatment | Stress placement in one particular line |
| Accent and dialect range | Lowering the voice in this scene |
| Accepted proper-noun pronunciations | Volume when emotionally agitated |

The costs of drawing the boundary incorrectly are asymmetric: put performance into identity, and every episode asks the character to speak with the previous episode's injury;
omit identity into performance, and the voice performer must guess who this person is again in every scene.

`not_voice_identity` and the identity fields must both be written. If only identity is recorded, downstream workers cannot tell whether a feature
was omitted or intentionally excluded.

## What One Reference Recording Can Determine

Every reference binding must carry a scope of use: state **what** is being referenced and what **must not** carry over
(`AST-08`). If one recording serves multiple purposes, split it into separate bindings and review each one.

| `role` | May borrow | Must not borrow by default |
|---|---|---|
| `timbre` | Timbral texture, resonance, perceived age and physical scale | Emotion, speaking rate, and recording space in this sample |
| `accent` | Accent and register range | Timbre, pitch range, and speaker identity |
| `pace` | Baseline speaking rate and pause habits | Timbre, accent, and emotion in this sample |
| `age_impression` | Perceived age | Specific timbre and accent |

Three categories **must always be written into `must_not_control`**, because they inevitably exist in every reference
and never belong to character identity:

- **Emotion in this reference**: an audition script being delivered through tears does not mean the character always cries;
- **Recording space**: reverberation, room tone, and microphone distance belong to that recording, not to the person;
- **Background content**: noise floor, accompaniment, or another speaker.

When one reference must establish both timbre and accent, create two bindings and review them separately; do not lengthen `may_control`.

## Binding Does Not Mean Listening

A filename or visible reference identifies only which material was bound; it **does not prove anyone actually listened to the audio** (`AST-09`).
Every binding must state the evidentiary stage it reached:

| `admission_status` | Situation | Permitted conclusion |
|---|---|---|
| `creator_described` | The creator or reference rights holder supplied a verifiable description of the sound | Evaluate according to the description |
| `audibly_inspected` | The runtime was authorized to inspect the audio and completed that inspection | Evaluate according to the inspection record |
| `unverified` | Only a filename or written description exists; the audio cannot be heard or no authorization exists | **Do not** claim that timbre, accent, noise floor, or number of speakers has been confirmed |

Without evidence, honestly retain `unverified` and list the risks. Negative wording cannot erase content already present in a reference—
if the reference contains background noise, writing “no background noise” does not remove it. Re-record, clean it, replace it,
or return the decision to the reference rights holder.

Reference audio and authorization notes are creator inputs and belong under `输入/`; `视觉设定.md` records only the project-relative path, purpose,
permitted and prohibited controls, and observation status. **Do not copy the media itself into the visual specification or public deliverables.**

## Selection Criteria

`selection_criteria` consists of three to five audible criteria used to **choose** a reference or **judge** whether a cloning result
qualifies as the character (`AST-12`). It does not generate a voice or replace the reference.

Choose selectively from six categories rather than filling them all: pitch range (relative position, not Hz—for example, “half a step lower than the other adult men in the drama”),
texture, perceived age and physical scale, rhythm, accent and register, and a repeatable signature habit (no more than one).

Give every criterion a `counter_example` that defines what would be excessive. Without an upper bound, each audition round becomes more exaggerated than the last,
and there is no reliable way to decide whether a cloning result still qualifies.

Emotion words are not criteria. If an anchor includes “angry,” “sad,” or “tense,” it describes performance rather than identity;
replace it with the audible feature that creates that impression.

## Creating Distinction

Select characters comparatively within the same cast (`AST-11`). For every character, answer: Who in this drama are they most likely to be confused with,
and which criterion distinguishes them?

```
CHAR-A 与 CHAR-B 最易混：两条参考同为中低音区、语速偏慢。
区分判据：A 句尾收住不拖长；B 句尾常带一段下滑的余音。
```

**English guide (non-executable):** CHAR-A and CHAR-B are easiest to confuse because both references use a low-to-mid register and slow pace. Distinguish them by sentence endings: A stops cleanly without prolonging the final sound; B often trails into a downward aftertone.

If this distinction cannot be written, the two references are effectively the same voice—the audience will not know who is speaking.
Text review cannot expose this problem; it is heard only in the finished production. Return to the creator and replace one reference
instead of pretending that stacked adjectives create a distinction.

For a large cast, select voices in batches of easily confused groups rather than appearance order.

## Proper-Noun Pronunciation

Every accepted proper-noun pronunciation must have exactly one spelling (`AST-10`).

This field is purely textual, and reference audio usually cannot help: audition scripts generally do not contain these names. Human performers pronounce them according to
their own habits, and speech-synthesis systems follow model habits; neither side reports an error. If one name has two spellings,
the pronunciation will change between episodes.

Add new pronunciations through the normal acceptance process; do not decide them locally during rendering.

## Variants: Disguise, Age, and Changes Across Segments

When a character impersonates someone else, ages ten years, or permanently loses their voice after poisoning, **do not overwrite the base identity**. Instead, record
a variant according to [Identity and Variants](identity-vs-variant.md):

- `cause`: which accepted screenplay fact caused it;
- `validity`: where it takes effect and where it expires;
- `delta`: which reference changed, or which criteria changed relative to the base identity; inherit everything else.

Do not create a variant for a brief one-scene change; leave it to performance. As with Look criteria, promote a change to a variant only when it persists across multiple scenes,
will be reused, requires an independent reference, or must be bound precisely downstream.

## Writing to `视觉设定.md`

When vocal identity must remain consistent across episodes, add “Voice Direction” under the relevant character entry and retain only:

1. **Reference**: project-relative path, purpose, permitted borrowing, and prohibited borrowing; when there is no reference, write “awaiting selection”;
2. **Selection criteria**: three to five audible criteria, each with a counterexample;
3. **Comparison character**: who is easiest to confuse with this character and which audible difference separates them;
4. **Proper-noun pronunciations**: the one confirmed reading;
5. **Variants**: disguises, age spans, or timbral changes lasting across multiple scenes, with their cause and effective range.

Temporary emotion, breathing, stress, volume, and spatial reverberation remain owned by the screenplay/shot/video prompt. Voice direction is a production input, not
a guarantee of synthesis results; actual TTS is still executed by `$short-drama-produce` only after an exact preview and explicit confirmation.
