---
name: short-drama-storyboard
description: Turn a Chinese short-drama screenplay and its visual specifications into a Markdown storyboard with dramatic responsibilities, continuity boundaries, and frozen-keyframe prompts. Use when the user asks to “break down/design shots/create a shot list,” “plan scene visuals/block a storyboard,” “compare directing approaches,” “write first-frame/keyframe prompts,” or check axis, blocking, eyeline, and prop-holding continuity; does not generate media.
license: MIT
---

# Short-Drama Storyboards and Frozen Keyframes

Turn the screenplay and visual facts into `剧集/<EP>/分镜.md`, with clear shot responsibilities, spatial continuity, and a starting state that can be frozen.
Use a level-two heading, `## SHOT-...`, for each shot, and place the starting-frame text under `### 冻结关键帧提示词` within that shot.

## Quick Start

```text
用 $short-drama-storyboard 完成 EP001 的正式分镜和每镜冻结关键帧
```

**English guide (non-executable):** Use $short-drama-storyboard to complete EP001's production storyboard and frozen keyframe for every shot.

## Entry Point

The current screenplay plus the required visual facts are enough to begin. Asset image prompts and storyboarding are sibling branches; neither waits for the other. Compare coverage approaches in context only when a key scene genuinely supports multiple viable directing approaches. Design ordinary scenes directly.

Creator-facing explanations follow the project language. Copy-ready frozen-keyframe text follows
`short-drama.json#/format/prompt_language`. If there is no `short-drama.json`, default the text to `en`.
Before assigning shot durations, read
`short-drama.json#/creator_authority/production_profile/choices/native_duration_seconds`. If a target model has been declared but its native duration has not, obtain that one choice first. If no target model has been declared either, design to the narrative rhythm as usual without guessing vendor constraints.

Who will appear in a given frame is not settled until its frozen keyframe has been written. Therefore, backfill all three evidence fields after the keyframe, reading the finished image rather than the shot intent.

The user’s not manually naming a reference image does not mean they have chosen text-to-video. After freezing the keyframe, first determine the consistency requirements from the people, location, key props, and starting composition visible in the shot, then inspect the actual images already present in the project. Bind an image automatically only when it is currently readable and its content and purpose can be verified. If its filename resembles a character’s name but its content has not been checked, treat it as not ready.

If the project contains no images at all, the creator has three options. Explain all three at once before asking them to choose; do not offer only “generate reference images first” and “switch to text-to-video”: place images already on hand into the project and bind them as `REF-...`; create images in the creator’s own tool and, for this pass, record the attachment plan as `PLAN-...`; or explicitly switch to text-to-video. Generating images with this toolkit’s production skill is only one way to follow the first option. It requires an external adapter and credentials and is not the only entry point.

Before storyboarding, read the current contents of `剧集/<EP>/剧本.md`. When the creator says “the screenplay has been approved for use,” they mean that file, not an earlier draft in the conversation. If the two differ, use the file and call out the difference.

## Workflow

1. Read the accepted native-duration range for the target model, then confirm which shots carry every scene action, line of dialogue, sound, piece of on-screen text, and turn.
2. Decide when the audience learns each fact, whose perspective it aligns with, how space is revealed, and which visible action carries each turn.
   When the screenplay or Brief uses relative timing such as “first half / second half / first third / final N seconds” to constrain when something may first appear, be released, or is prohibited, convert it to an explicit time boundary using the accepted episode duration before storyboarding. For example, in a 60-second work, something that “first appears in the second half” may not appear before 30 seconds.
3. For each shot, state its single responsibility, source, duration, shot size/camera position, starting state, single primary action, ending state, and sound. Use
   `起点 → 唯一动作 → 终点` to state directly how the characters, both hands, and held objects complete the state transition in that shot. Leave the three evidence fields until Step 6.
4. Lock character orientation, position, eyeline, held objects, entrances and exits, screen direction, and necessary states. If an established upstream relationship constrains the available movement, project that relationship into both the starting and ending states of the shot.
5. The frozen keyframe represents only the shot’s starting state. Remove text, actions, poses, or prop states that appear only at the ending state.
6. After the keyframe text is complete, read it to identify the people, locations, and props in that frame whose identity, styling, or geography must remain consistent. Then use the same list to fill all three evidence fields at once:

   - **Visual evidence**: write every list item as an entry reference to 《视觉设定.md》; this field is required;
   - **Image-prompt items**: include any suitable existing `IMG-...` entries from the list; otherwise write “none”;
   - **Input reference images**: search for matching images from the user’s inputs, `剧集/<EP>/制作成果/`, and other visible media already referenced by the documents. On a match, record it as `REF-...`. If none match, write “none (reference images required: <missing starting frame, people, location, and props for this shot>)”. If only some match, append “; reference images still required: <remaining images>” after the existing `REF-...` entries, separating gaps only with `、`.
     If the creator says they will prepare the images elsewhere, record this list in `PLAN-...` slots and treat the shot as ready. Write “none (creator explicitly chose text-to-video)” only when the creator explicitly declines to use images.

   All three evidence fields describe the same frame and therefore must not contradict one another. Any character or prop named in the keyframe must appear in the visual evidence.
7. When asked for the full episode, complete the full episode, then report coverage, pacing, and genuine unresolved choices once at the end.

## Shot Requirements

- Every shot has one responsibility, an explicit source, visible starting and ending states, and a reasonable duration. “Source” begins with a scene ID that actually exists in 《剧本.md》.
  After the ID, it may include a necessary short quotation. For a shot spanning scenes, join multiple entries with `、`; `creator_markdown_check.py` verifies that every ID resolves.
- Every scene in the screenplay must be covered by a shot. When deliberately deciding not to film a scene, add one line at the beginning of the body of 《分镜.md》:
  `- 未拍场次：<场景 ID>（理由：……）`, joining multiple entries with `；`. SHT-01 has always allowed justified omissions,
  but an omission and accidental missing coverage look identical in the finished document, so record the reason instead of leaving it only in the conversation.
- When a native duration has been declared, every one-shot-per-generation shot must fall within its minimum and maximum duration. If a narrative action is shorter than the minimum, complete it within a valid shot duration and then hold the ending state. If an action exceeds the maximum, split it at visible state-completion points; every resulting shot must still have one responsibility and a credible boundary.
- “Single action” is the visible state chain from the shot’s start to its end. For a handoff, change of hands, placement, or retrieval, state the person making contact, the mode of contact, and the object’s resting position in the same chain. Do not let an object teleport off-screen between otherwise valid endpoints.
- A cut must change information, power, emotion, space, or rhythm. Delete shots that repeat the same meaning.
- Relative time expressions constrain when an event first becomes visible or audible; completing preliminary action does not release it early. Write the boundary directly on the storyboard timeline rather than using narrative ordering such as “later” or “after the handoff” as a substitute for numeric time.
- Do not repeat the same action across shots. An ending state should be able to serve as a credible starting state for the next shot.
- The readability of essential information takes priority over decorative camera movement. In vertical compositions, keep the subject and reactions visible.
- For complex ensemble scenes, lock spatial anchors and screen direction before choosing changes in shot size.
- In addition to each person’s pose, starting and ending boundaries must state the body–object–space relationships on which the shot depends. If a relationship remains unchanged within the shot, preserve it at both ends. If it must change, both the process and ending state require screenplay support.
- A frozen keyframe includes only what is visible at that instant. Text, fingers, reflections, and occlusion must be generatable.
- Copy continuity locks from 《视觉设定.md》 verbatim into the frozen-keyframe text of every applicable shot. Do not omit a locked surface on the assumption that “the reference image will convey it.”
- If checking reveals an omission, correct the document directly. Do not generate a coverage table merely to prove that a check was performed. The “visual evidence” inside a shot block is an evidence field for that shot, not the coverage table prohibited here.

## Visual Evidence and Images

- `IMG-...` is an **image-prompt entry ID** in 《图片提示词.md》. It does not mean that an image has been generated, provided, or is usable.
- If 《图片提示词.md》 exists and the shot needs one of its entries, populate “image-prompt items.” The ID must match a visible level-two heading in that document, and the entry must include its Chinese name and the identity, styling, geography, composition, or other boundary it controls. The ID is only for lookup; do not force an English slug to carry its meaning.
- If 《图片提示词.md》 does not exist or contains no suitable entry, write “image-prompt items: none,” then point in Chinese to the people, locations, or props in 《视觉设定.md》 and state the scope they control. This is a normal direct entry point. Do not invent an ID or fabricate another stage merely to continue storyboarding.
- “Visual evidence” is required for every shot. After the frozen keyframe has been written, inspect the actual image and express every visible person, location, and prop whose identity, styling, or geography must remain stable as
  `《视觉设定.md》·<人物|造型|地点|道具>「<名称>」（控制：<范围>）`, joining multiple items with `；`. Each name must match an identically titled entry in 《视觉设定.md》.
  Small or background figures remain in scope if their identity must be recognizable. Off-screen voices and unrecognizable body fragments do not. If the shot genuinely contains no such entries, write “visual evidence: none.”
- If an entry’s name appears in the keyframe text but the entry genuinely is not visible in the shot—the owner has left, the name appears only in on-screen text, or the name happens to match another word—append `；画外：<类别>「<名称>」` to “visual evidence.” This records the truth; it does not pretend that an absent person is present.
- If an entry’s name cannot be matched reliably in the image text (`道具「手机」` might collide with “手机店,” and `人物「小雨」` with “下着小雨”), write `画面代称：无` in that entry in 《视觉设定.md》. The mechanical check will stop searching for it by name. “Visual evidence” must still truthfully state whether it appears in this shot.
- All three evidence fields describe the same frame, not an asset catalog for the shot. “Control” includes only what this frame can support: a close-up of the back of a hand does not control “this episode’s styling,” and a shot showing only a screen and one finger does not control “physique.” A binding from the previous shot does not carry forward merely because “the character is still in the scene.”
- Any person, location, or prop named in the keyframe text—by an entry name from 《视觉设定.md》 or its declared “image alias”—must appear in that shot’s “visual evidence.”
  `creator_markdown_check.py` checks this mechanically. It detects only a category **explicitly named** in the text: the machine stays silent when the text merely describes but does not name someone
  ("a boy in a hooded jacket"). You must still read the image to determine who is present rather than waiting for an error.
- If a visible object must remain consistent in this shot but does not yet have an entry in 《视觉设定.md》—especially common with props that recur across shots—do not treat it as unnecessary merely because it “cannot be entered as visual evidence.” A pen and a coat that appear in four shots present the same problem. Do two things:
  anchor it in every shot with exactly the same description, and name it in the end-of-pass report with a recommendation to add an entry through `$short-drama-assets`.
  Do not add an entry to 《视觉设定.md》 yourself or insert it into “visual evidence” as if an entry already existed.
- “Input reference images” is a separate axis: actual images provided by the creator, or confirmed as produced and currently readable, are cited with slots distinct from the `IMG-...` prompt IDs and stabilized as `REF-...`. Every slot includes an explicit order, a project-relative path delimited only by `/`, a Chinese name, “purpose,” “controls,” and “must not control.” If none exist, distinguish “reference images required” from “creator explicitly chose text-to-video.” If only some are ready, preserve the existing `REF-...` entries and append “; reference images still required: …”. Never write prompt entries, images not yet generated, or conversational descriptions as `REF-...`—`REF-...` means “the file is in the project now.”
  Images the creator will attach personally at generation time use the `PLAN-...` form below. It likewise does not claim that a file exists; it only states which images to attach to this shot.
- Every `REF-...` must follow exactly one format: `REF-<slot>（顺序：<n>）· <项目相对路径>《<中文名称>》（用途：<用途>；控制：<范围>；不得控制：<范围>）`. Note the full-width colon after “顺序：” and the middle dot `·` before the path; do not use `/` as a field delimiter. Join multiple images only with the Chinese semicolon `；`. When some images are missing, append `；待补参考图：<缺口>` after the final complete slot, separating gaps with `、`. Read the result back against this format before delivery.
- `用途` may be only one of `身份`, `造型状态`, `地理`, `构图`, `尺度`, `效果`, `起始帧`, `结束帧`, or `风格`. See 《参考角色》 in `$short-drama` for what each may control.
  Write `用途：起始帧` for this shot’s starting-image reference, `用途：身份` or `造型状态` for character images, `用途：地理` for location images, and the one applicable value for the state of a prop.
  If one image serves two purposes, split it into two slots. A shot may contain at most one `起始帧` image and one `结束帧` image, and an `结束帧` requires a corresponding `起始帧`.
  Downstream video prompts rely on `用途` to identify “which storyboard starting frame and which people/prop/location images are supplied for this shot,” so a slot without `用途` is not ready.
- When a shot does not yet have a starting-image reference, there are two routes. For the `用途：起始帧` image, if the creator is producing it with this toolkit, `$short-drama-produce` generates it from the shot’s frozen-keyframe text. Set the job’s `source` to `剧集/<EP>/分镜.md` and `source_entry` to this shot’s `SHOT-...`,
  write the output to `剧集/<EP>/制作成果/images/`, and bind it as `REF-...` only after the actual file exists. If the creator produces it in their own tool,
  copy the frozen-keyframe text into that tool to generate the image, then place the file in the project and bind it as `REF-...`, or record it for the current pass as
  `PLAN-SHOT-START（顺序：<n>）· <本镜 SHOT-...>《本镜冻结关键帧》（用途：起始帧；……）`.
  If neither route has been taken, the image remains an item under “reference images required.”
- For images created outside the project that will not be added to it, use `PLAN-...` slots. Their syntax is identical to `REF-...`, except that the project-relative path is replaced with an `IMG-...` or `SHOT-...` entry ID. The Chinese name of an `IMG-...` must match its title in 《图片提示词.md》.
  This form means “the creator will attach this image in this order at generation time”; it does not claim that the file is in the project, so it is not “required” and cannot be submitted for production. When the actual file enters the project, rewrite the slot as `REF-...`. Both types of slot may be combined, with one continuous `顺序` sequence.
- Automatic binding does not mean stuffing every image into a shot. Select only images for the visible people, location, key-prop state, or starting composition that genuinely require stable identity, styling, geography, state, or composition. For every image, state its purpose, what it controls, and what it must not control.
- The two axes combine independently. When a valid image-prompt item exists, input reference images may still be “required” or the creator’s explicit text-to-video choice. When the creator provides an actual reference image, image-prompt items may still be “none.”

## On-Demand Knowledge

By default, read only this SKILL, the current screenplay, and the necessary visual facts. Open only one corresponding document when needed:

- Stage boundaries and rule levels: [Stage Contract](references/stage-contract.md)
- Shot responsibilities, reasons for cuts, and boundaries: [Shot Craft](references/shot-craft.md)
- Shot grammar required for actual production: [Production Shot Grammar](references/production-shot-grammar.md)
- Comparing directing approaches for key scenes: [Scene Visual Plan](references/scene-visual-plan.md)
- Checking whether every source passage has visual coverage: [Coverage Audition](references/coverage-audition.md)
- Blocking for multiple people, groups, and complex spaces: [Blocking Playbooks](references/blocking-playbooks.md)
- Frozen instants, attention centers, and readability: [Keyframe Craft](references/keyframe-craft.md)
- Shared visual-style vocabulary for motion comics and 2D-comic formats: [Motion-Comic Keyframe Lexicon](references/comic-keyframe-lexicon.md)
- Complete example from screenplay facts to keyframes: [Screenplay to Keyframe](references/screenplay-to-keyframe-example.md)
- Splitting and combining shots and maintaining stable shot IDs: [Shot Revision Identity](references/shot-revision-identity.md)
- Continuity checks before completion: [Review and Fixtures](references/review-and-fixtures.md)

## Revision

Preserve unaffected shot IDs. When splitting or combining shots or changing their responsibilities, state which downstream video prompts need to be refreshed, but do not automatically rewrite files the user did not name.

## Completion

The task is complete when every source passage in the named scope has shot coverage; no shot duplicates another’s responsibility; space and state remain continuous; starting and ending boundaries are producible; keyframes can be frozen; every shot’s “source” resolves to a real scene in 《剧本.md》; every screenplay scene either has shot coverage or is recorded under “unfilmed scenes”; and all visible people, locations, and props in every keyframe appear in that shot’s “visual evidence.” In the final report, individually name visible objects that the image requires but 《视觉设定.md》 does not yet define. If this request modifies both
《图片提示词.md》 and 《分镜.md》, refresh the affected shot references in the same pass; do not create a separate coverage table.
Begin video prompting, production, or review only when the user explicitly requests it.
Once all five creative documents are present, hand off to `$short-drama` for one mechanical cross-document structure check. Content quality still requires creator review.

## Installation and Maintenance

Run `python3 scripts/selftest.py` only during installation, upgrades, or troubleshooting.
