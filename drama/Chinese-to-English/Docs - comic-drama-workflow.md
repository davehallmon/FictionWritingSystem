# Creator-First End-to-End Motion-Comic Workflow

The goal is to spend creative time on story, visual choices, and prompts—not on maintaining pipeline files. Maintain no more than five
Markdown files per episode as needed, and use them directly as the creative source of truth.

## At a Glance

```text
点子 / 原著 / 现成剧本
        │
        ├─ 原著分析、故事开发（都可选）
        ▼
      剧本.md
        ▼
    视觉设定.md
      ├──────────────┐
      ▼              ▼
图片提示词.md       分镜.md
                      ▼
                 视频提示词.md（动态漫剧）
                      │
                      └─ 静态漫剧：关键帧切换 + 配音，可跳过
      └──────────────┬──────────────┘
                     ▼
              预览 → 明确确认 → 生产
```

**English guide (non-executable):** Idea, source work, or existing screenplay → optional source analysis and story development → `剧本.md` (screenplay) → `视觉设定.md` (visual specification) → image prompts and storyboard → video prompts for animated motion comics. Static motion comics may skip video-motion prompting and use keyframe changes plus voice-over. Production begins only after preview and explicit confirmation.

The default location recognized by existing tools is `剧集/<EP>/`:

1. `剧本.md`
2. `视觉设定.md`
3. `分镜.md`
4. `图片提示词.md`
5. `视频提示词.md`

Each request creates only the documents it needs; do not pre-create empty files. Scenes, asset groups, and shot groups are internal batches that continue automatically. Do not
wait for “continue” after every batch, and do not save JSON/JSONL, indexes, fingerprints, coverage tables, QA, review sheets, or handoff capsules.

## 0. Source-Novel Analysis and Story Development (Optional)

Use `$short-drama-novel-analyze` only when a long-form source novel is available and its adaptation value must be assessed. Use `$short-drama-develop` only when a series promise, adaptation contract, or episode
map is needed. If a usable episode idea, outline, or screenplay already exists, proceed directly to writing; do not backfill these two steps merely to complete the workflow.

## 1. Initialization (As Needed)

When project-level language, aspect ratio, duration, or production configuration is required:

```text
用 $short-drama 初始化一个都市逆袭竖屏漫剧项目，9:16
```

**English guide (non-executable):** Use $short-drama to initialize a 9:16 vertical motion-comic project about an urban underdog's rise.

Initialization does not generate story content. Decide the production format, visual direction, or Look Development only when it genuinely constrains multiple stages.
Look Development is an optional branch, not a prerequisite for writing prompts or storyboarding.

## 2. Write `剧本.md`

```text
用 $short-drama-write 写完 EP001：外卖员在高档餐厅被经理羞辱，亮出集团董事身份
```

**English guide (non-executable):** Use $short-drama-write to complete EP001: a delivery worker is humiliated by a manager at an upscale restaurant, then reveals that he is a group-company director.

Complete an entire episode in one request when the request covers the whole episode. Arrange causal beats in context first, then write scenes, actions, dialogue, voice-over, and necessary sound facts into
the single screenplay. Do not create a separate episode card, beats, block index, or recording sheet. The screenplay must be performable and producible; every scene changes
information, power, relationship, emotion, physical state, or risk.

## 3. Write `视觉设定.md`

```text
用 $short-drama-assets 从 EP001 拆完人物、造型、地点、道具和本集状态
```

**English guide (non-executable):** Use $short-drama-assets to extract EP001's characters, looks, locations, props, and episode state.

Save only visual facts that downstream generation must preserve. First determine whether identity is the same, then decide whether to reuse, create, or create a variant. Clothing, injuries,
weather, lighting state, open/closed state, and possession are usually variants; pose, gaze, and blocking are usually transient storyboard facts. Do not turn every appearance, decision process,
and continuity check into separate ledgers.

## 4. Write `图片提示词.md`

```text
用 $short-drama-image-prompts 为 EP001 的角色、地点和关键道具写可直接复制的图片提示词
```

**English guide (non-executable):** Use $short-drama-image-prompts to write copy-ready image prompts for EP001's characters, locations, and key props.

For each item, state its purpose, stable anchors, current variant, composition/viewpoint, lighting and color/material, reference boundaries, and prohibitions, followed by copy-ready
prompt text. Image prompts and storyboards are sibling branches; either can begin once visual facts exist, without waiting for the other.

## 5. Write `分镜.md`

```text
用 $short-drama-storyboard 完成 EP001 的正式分镜和每镜冻结关键帧
```

**English guide (non-executable):** Use $short-drama-storyboard to complete EP001's production storyboard and frozen keyframe for every shot.

First confirm how the source text is realized in shots. Then, for every shot, record its responsibility, source scene, shot size/camera position, duration, spatial and asset bindings,
`起点 → 唯一动作 → 终点`, and sound responsibility. By default, include one frozen-keyframe prompt in the same entry.
Compare directing options in context only when a key scene genuinely permits multiple valid treatments. Do not generate audition, coverage, or
scene-plan files for ordinary scenes.

After the keyframe is written, backfill three forms of evidence by reading the completed image rather than the shot intent. The required “visual evidence” lists the characters, locations, and props
whose identity, look, or geography must be recognized in that frame. “Image prompt item” records an existing `IMG-...`; “input reference image” records real images
available in the project and labels each with `用途`.

## 6. Write `视频提示词.md`

```text
用 $short-drama-video-prompts 把 EP001 的分镜逐镜写成可直接复制的视频提示词
```

**English guide (non-executable):** Use $short-drama-video-prompts to turn each EP001 storyboard shot into a copy-ready video prompt.

Starting from the confirmed initial frame, each entry implements the storyboard's `起点 → 唯一动作 → 终点` item by item: trigger, contact, landing point, secondary reaction,
camera movement, sound, and verifiable endpoint. Do not repeat appearance already locked by the still frame or cross into the next shot. When continuing a sequential segment from the preceding segment's generated
result, the second and later segments use both the actual previous video and its actual extracted final frame. When the user explicitly requests timeline music, include the music intent as
a separate section in the same document. Lyrics may use only text supplied or explicitly accepted by the user. For a static motion comic using only keyframe switching + voice-over,
this step may be skipped; storyboard keyframes and image prompts proceed directly to production preview.

## 7. Production: The Only Fixed Gate

```text
用 $short-drama-produce 预览 EP001 的这批图片/视频任务；等我确认后再执行
```

**English guide (non-executable):** Use $short-drama-produce to preview this batch of EP001 image and video jobs; wait for my confirmation before executing them.

Every production job must follow this sequence:

1. Create a bounded temporary job from the current prompt, with `source` pointing to its Markdown and output under `剧集/<EP>/制作成果/`;
2. `prepare` and display the count, prompt text, references, parameters, output, and adapter;
3. The user reviews this preview and gives explicit confirmation;
4. Only then may `run` invoke an external adapter.

Any change to content, inputs, parameters, or output requires a new preview and confirmation; failed retries also require new confirmation. The production tool's hidden job, confirmation,
and audit records are runtime state required for paid side effects, not creative content.

## 8. Review and Delivery (As Needed)

Invoke `$short-drama-review` only when the user explicitly requests review. Write conclusions to `审查/<EP>-审查.md`, using visible scene, shot, and
prompt IDs to locate issues. Correct explicit problems directly in the documents; do not add QA rounds to ordinary creative work. For delivery, directly copy or
archive the current documents and finished outputs named by the user, excluding private inputs, credentials, and the production tool's hidden runtime state.

## Common Sticking Points

| Sticking point | Resolution |
|---|---|
| Motion-comic characters look attractive but not like the same person from shot to shot | Return to `视觉设定.md` and tighten visible identity anchors. A storyboard may cite the same `IMG-...` prompt item to align intent, but shots share pixel evidence only when the production job's `references` actually passes the same image file |
| A 2D image has style but no narrative focus | Use the [Motion-Comic Keyframe Visual Lexicon](../skills/short-drama-storyboard/references/comic-keyframe-lexicon.md). Lock subject facts and the center of attention first, then project the art style |
| The storyboard omits source material or repeats the same action | Check shot coverage of dialogue, actions, sound, and on-screen text scene by scene; split, merge, or revise shots directly |
| The keyframe names a character who is missing from its visual evidence | This is the defect reported in #84/#94. Backfill “visual evidence” from the completed keyframe. When prompt text names an entity in a non-Chinese language, add a `画面代称` to its entry in 《视觉设定.md》 so `creator_markdown_check.py` can catch named omissions. Characters described but not named cannot be detected; cover them with the required field and review rubric |
| A target video model was specified, but a text-to-video prompt was returned | Naming a model does not choose text-to-video. First write the model into `production_profile`; then have the storyboard find existing project images for visible characters/locations/props/initial frame and bind them as entries labeled with `用途` under `REF-...`. If images are still missing, stop with a list rather than switching to text-to-video |
| Images were created in a web interface, but the suite asks to generate reference images first | Image-to-video prompts can be produced even when images are not in the project. Have the storyboard create `PLAN-...` slots for the images attached to the shot; use an `IMG-...` board or the shot's `SHOT-...` frozen keyframe as the locator, and use `顺序` as attachment order. Video prompts are still produced normally, but these shots cannot pass to the production skill |
| The storyboard changed an approved screenplay | Every shot's “source” must resolve to a real scene in 《剧本.md》. Every screenplay scene must have shot coverage or appear in “unfilmed scenes” in 《分镜.md》 with a reason. Chinese quotations in copy-ready text must be found verbatim in the screenplay. `creator_markdown_check.py` verifies all three |
| The initial frame prematurely contains the action result | Keep only the shot's starting point in the frozen keyframe; leave action changes and the endpoint to the video prompt |
| Prompt languages are mixed | Image and keyframe prompts follow `format.prompt_language`; video defaults to the target model profile's `video_prompt_language`; spoken language still follows the screenplay |
| A static motion comic is forced to add video-motion prompts | Keyframe switching plus voice-over can proceed directly to production preview; do not invent a useless document for workflow completeness |
| Production is imminent but task boundaries are unclear | First have `$short-drama-produce` display the count, prompt text, references, parameters, output, and adapter; then confirm explicitly |

## When to Stop

Ordinary creative work stops only in three cases: the user-named scope is complete; missing facts create a genuine creative branch that would materially change the result; or
external production is about to be invoked. All other batches continue automatically. The final report covers completed scope, key creative decisions, genuine unresolved items, and optional next steps—not
internal pipeline noise.
