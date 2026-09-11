---
name: short-drama-write
description: Write or revise producible Chinese short-drama or motion-comic episode screenplays in Markdown, and normalize existing screenplays while preserving the author's original text. Use when the user asks to “write/revise a short-drama episode,” “turn an outline into a screenplay,” “improve scenes/dialogue,” “remove templated writing,” “polish away AI-like writing,” “continue with the next episode,” or provides a screenplay that must enter subsequent production. Does not handle assets, storyboards, media prompts, or final review.
license: MIT
---

# Short-Drama Writing

Turn an episode's intent into a performable, producible `剧集/<EP>/剧本.md` that changes story state.

## Quick Start

Maintain one screenplay Markdown file only; do not create a separate episode card, beats, block index, recording sheet, QA record, or acceptance record.
Use `# EP001 集名` for the level-one heading and `## EP001-SC001 内 · 地点 · 时间/天气` for scene headings.
Write dialogue as `角色（可选表演提示）：台词`; production tags use `[VO]`, `[OS]`, `[SFX]`, `[画面文字]`,
`[连续性]`, and `[转场]`. Do not misclassify action narration containing a colon as dialogue.

## Entry Points

- Episode plan available: read this episode's entry state, objective, turn, payoff, and handoff facts.
- Only an idea/outline available: form the smallest episode contract and causal beats in context, then write the screenplay directly.
- Existing screenplay available: preserve the author's language and make only the targeted revisions named by the user.
- Nonstandard text entering production: preserve the original and normalize only the necessary scenes, actions, dialogue, and production tags.

Development outlines and long-form analysis are optional upstream inputs. Write directly when the current material is sufficient.

## Workflow

1. Lock the promised viewing experience, who wants what now, the resistance, the episode payoff, and the exit state.
2. Identify only engines that actually exist in this episode. If the primary engine is a difficult choice, inspect the value on both sides; if a judgment turn depends on disputed evidence, inspect the proof boundary; if an exact deadline is foregrounded, inspect action capacity; if the task constrains counts, rounds, breaths, or beats, inspect whether every unit completes its required state within the boundary. Do not force these mechanisms into an episode that lacks them. When an input already uses one as its primary engine, make it truly change action, relationship, or outcome rather than merely naming it in dialogue.
3. Arrange “because → action → result → next pressure” in context without saving a beat sheet. Let objects, dialogue, silence, space, or sound do the necessary work according to the episode's genre; do not prescribe one carrier.
4. For each scene, define its irreplaceable function, visible change, and end state. For scenes organized around pursuit or conflict, also define the focal agenda and resistance. Supporting characters who carry a major dramatic function need their own strategies; keep transactional or environmental characters concise.
5. Write actions, dialogue, voice-over, sound facts, and on-screen text into the same screenplay.
6. If the user requests a complete episode, write the complete episode; continue scene batches automatically.
7. Before delivery, silently inspect whether the screenplay alone communicates the episode promise, whether character actions are causal, and whether genre tone is consistent. Then perform targeted checks for any choice, evidence, finite units, or exact deadline genuinely used by the episode. If self-review makes the screenplay grow mechanisms the input did not require, remove the mechanisms rather than inventing justifications.
8. Preserve unrelated passages during local revisions. Correct explicit problems directly; ask the user only about genuine plot branches.

## Writing Requirements

- First obey facts already supplied by the input, `必须/禁止`, the genre's viewing contract, and the exit state. This skill's review items and craft defaults only help realize those requirements; they cannot be used to invent exact numbers, records, resources, procedures, relationships, or mechanisms absent from the task.
- Every scene changes information, power, relationship, emotion, physical state, or risk; delete or merge scenes with no change. A turn in the central resistance requires a traceable fact, leverage, permission, cost, or character action; it cannot rely solely on the opponent ceasing to react.
- Dialogue must pursue, evade, probe, pressure, or redefine a relationship. Express state through visible, audible, or tangible behavior; do not substitute explanation for action or verbally restate a mechanism already dramatized clearly.
- Stakes required for the audience to understand the current action must enter the screenplay, but the carrier follows the genre. Enable specialized rules for choices, evidence, finite units, exact deadlines, and similar mechanisms only when the input genuinely uses one as its engine; read [Dramatic Craft](references/script-craft.md) on demand. Do not upgrade ordinary decisions, objects, or vague time pressure into the same mechanism.
- When compressing process, retain only nodes that change strategy, relationship, risk, or outcome. Resources and external reactions must come from the input or prior setup and cannot perform the most difficult dramatic action for the character.
- Characters carrying the primary conflict must retain proportionate goals, judgment, or strategy. Keep transactional and environmental characters concise; do not add secrets, reversals, or arcs merely for a checklist.
- Established costs, irreversible consequences, key held objects, spaces, and knowledge states must enter a traceable exit state. The ending may advance, omit, use irony, close quietly, or leave resonance; do not require an extra external event.
- `[连续性]` hands off only a state established by prior action that downstream work could easily lose. An author tag cannot prove that something never occurred offscreen, and it must not repeat a result already shown clearly in the text.
- Before delivery, silently perform an economy check: did the screenplay add exact figures or record chains absent from the input; do tags/dialogue duplicate actions; are several consequences with the same direction stacked after the payoff? Delete content with no new function; do not delete know-how itself.
- When the input gives a target runtime, read the draft aloud with real performance, action, and pauses, then compress it by first removing repeated verification, explanation, and synonymous endings. Do not fill a template with uniform word, shot, or beat counts.
- The user's original text takes priority. “Remove AI-like writing” means targeted revision, not flattening the author's voice.

## On-Demand Knowledge

By default, read only this SKILL and direct inputs. When one of the following explicit signals appears, read the corresponding knowledge before drafting.
Multiple references may be read for distinct problems in the same input, but do not traverse unrelated references:

- Stage boundaries and rule levels: [Stage Contract](references/stage-contract.md)
- Scene-heading, dialogue, and production-tag syntax, or [normalizing](references/screenplay-format.md#7-现有文本的规范化入口) an existing screenplay supplied by the creator: [Screenplay Format](references/screenplay-format.md)
- Project-specific production-script dialect: [Production Format Dialect](references/production-format-dialect.md)
- Input contains a [core choice](references/script-craft.md#35-把一拍写成艰难选择时两个方向都要活着), [finite counts/rounds/breaths/beats](references/script-craft.md#64-有限单位按完成状态计数), [exact countdown](references/script-craft.md#63-倒计时先算动作不要只写数字), or [critical physical evidence that changes a character's judgment](references/script-craft.md#53-证据先改变判断再改变关系): [Dramatic Craft](references/script-craft.md)
- A past relationship must enter through dialogue, or a key character risks becoming merely expository: [Dialogue Craft](references/dialogue-craft.md)
- Sound sources, silence, and sound bridges: [Scene Sound Dramaturgy](references/scene-sound-dramaturgy.md)
- Different producible implementations of the same story obligation: [Substitutable Realization](references/substitutable-realization.md)
- Minimum handoff for a long episode spanning context windows: [Scene Handoff Capsule](references/scene-handoff-capsule.md), retained only in context

## Runtime Estimation (On Demand)

Only when the user asks about runtime, write the index to the system's temporary directory. First use Python to query the cross-platform temporary directory, then replace
the first command's complete printed path verbatim inside the quotation marks in the following two commands. Each line below is one complete command and does not depend on shell variables or continuation characters. On Windows,
when `python3` is unavailable, use `py -3`. Replace the example values for `--speaker` with actual speakers in this episode; add `--project short-drama.json` only when a project
configuration exists:

```text
python3 -c "from pathlib import Path; import tempfile, uuid; print(Path(tempfile.gettempdir()) / ('short-drama-' + uuid.uuid4().hex + '.jsonl'))"
python3 "{技能目录}/scripts/screenplay_index.py" "剧集/EP001/剧本.md" --output "粘贴第一条命令输出的完整路径" --speaker "本集角色一" --speaker "本集角色二"
python3 "{技能目录}/scripts/duration_estimate.py" "剧集/EP001/剧本.md" --index "粘贴第一条命令输出的完整路径"
```

**English guide (non-executable):** Replace `{技能目录}` with the skill directory. The screenplay is `剧集/EP001/剧本.md`. Paste the complete temporary path printed by the first command into `--output` and `--index`; replace “episode character one/two” with the actual speaker names.

The estimate is advisory, not a gate. When speaking rate or action-passage rate is absent, report only countable facts rather than guessing seconds. But when a task supplies a target runtime,
the writer must still judge capacity through real reading and action review, then directly compress repeated beats; “seconds cannot be estimated precisely” is not a reason to ignore the target.

## Completion

The work is complete when the named scope has been written, scene causality is coherent, dialogue and actions are performable, the promise is paid off or intentionally deferred, and the ending fulfills the episode's intended dramatic or emotional function. The final beat may advance events, close quietly, create resonance, or change the meaning of an existing action; judge whether it works rather than replacing that judgment with “did another event occur?”
Start assets, storyboards, review, and production only when the user explicitly names them.
Once the five creative documents exist, the work may pass to `$short-drama` for a mechanical cross-document check; content quality remains subject to creator review.

## Installation Maintenance

Run `python3 scripts/selftest.py` only during installation, upgrade, or troubleshooting.
