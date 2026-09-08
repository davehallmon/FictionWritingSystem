# Five Creative Documents

This is a recommended format, not a schema. Optimize for immediate human readability; stable IDs are needed only for cross-document references and production location.

## `剧本.md`

- The level-one heading must begin with the episode number, for example `# EP001 集名`.
- Each scene uses `## EP001-SC001 内 · 地点 · 时间/天气` (the spatial type may also be `外` or `内外`).
- Dialogue uses `角色（可选表演提示）：台词`. Voice-over, offscreen dialogue, sound, visible text, continuity, and transitions use `[VO]`, `[OS]`, `[SFX]`, `[画面文字]`, `[连续性]`, and `[转场]` respectively. Do not misclassify action narration containing a colon as dialogue.
- Do not generate a block ID for every line, and do not create separate beat sheets, indexes, or recording sheets unless the user explicitly needs them.

## `视觉设定.md`

Divide the document into characters, looks, locations, and props, with each item as its own level-two heading. Each item records only the identification anchors,
current state, and reason for change that downstream generation genuinely needs to preserve. Do not copy plot summaries or promote momentary poses or camera angles into new assets.

```markdown
## 人物 · 江辰
- 识别锚点：窄长眼、左眉尾旧疤、肩背略绷。
- 本集造型：深灰旧西装，右袖口有雨水深痕。
- 状态变化：EP001-SC003 后右手掌沾血。
- 画面代称：Jiangchen
- 连续性锁：LOCK-JIANGCHEN-SUIT《江辰深灰旧西装》（镜头：全集；图片提示词项：IMG-JIANGCHEN-SHEET）· 锁面：dark-grey worn wool suit
```

Level-two headings always use `## <人物|造型|地点|道具> · <名称>`; the storyboard's “visual evidence” locates entries by this heading.

**Visual alias** is the name used directly for this entry in prompt text, written in the project's prompt language. Separate multiple forms with `、`,
and match capitalization exactly. The entry's own Chinese name always counts as an alias, so Chinese-language projects usually do not need this line.
`creator_markdown_check.py` uses it to mechanically verify that “names appearing in frozen keyframes are covered by visual evidence.”

When prompt text is not Chinese, every **character** entry cited by a shot's “visual evidence” must state one conclusion: write
`画面代称：<正文里的拼写>`, or `画面代称：无` when the prose never names the character. Without this line, a Chinese entry name can never match
English prose, silently disabling the check—the exact failure pattern reported in #94. Locations and props are usually described rather than named in the prose,
so this is not mandatory for them.

Identification anchors are written for creators; **continuity locks** are carried verbatim by the execution layer. Lock only visible facts that recur across shots,
would be noticeably inconsistent, and do not change through the story (primary clothing color and form, prop color/material, hair length, wound position). Leave changing parts under
`状态变化`. Use one lock per line:

- `LOCK-...` is unique within the episode and must not be confused with `IMG-...`, `REF-...`, or `SHOT-...`;
- `镜头：` contains either `全集` or a `、`-separated list of `SHOT-...` entries, never both;
- `；图片提示词项：` is optional and contains a `、`-separated list of `IMG-...` entries;
- After `· 锁面：`, write the smallest noun phrase to carry verbatim, in the project's prompt language, without punctuation, action, or plot.

Frozen keyframes, `MOTION-...` prose, and any named `IMG-...` prose within the effective range must contain the lock phrase (case-insensitive).
`creator_markdown_check.py` verifies this mechanically. Projects with no locks are unaffected.

## `分镜.md`

Each shot is a level-two heading. Shot IDs are unique within the episode and remain stable; do not change an ID without cause when revising shot content.

```markdown
## SHOT-EP001-001 · 门外停步
- 来源：EP001-SC001
- 时长：4s
- 目的：先让观众看见他不敢进门，再揭示门内争吵。
- 景别/机位：中近景，门框外侧，轻微低机位。
- 起点：江辰右手悬在门把上方。
- 唯一动作：门内玻璃落地声触发江辰收回右手，视线从门把转向门缝。
- 终点：江辰右手垂回身侧，视线落在门缝。
- 图片提示词项：IMG-JIANGCHEN-SHEET《江辰角色板》（控制：身份、体态、本集造型）；IMG-CORRIDOR-NIGHT《夜间走廊场景板》（控制：空间地理、门位、光向）。
- 输入参考图：无（待补参考图：江辰本集造型、夜间走廊地理、本镜起始帧）。
- 视觉依据：《视觉设定.md》·人物「江辰」（控制：身份、体态、本集造型）；地点「旧走廊」（控制：空间地理、出入口、光向）。

### 冻结关键帧提示词
> 按项目提示词语言编写的冻结瞬间正文……
```

Write only shots with a defined responsibility. The keyframe prompt must match the shot's “start.” Text, actions, or states that appear only at the endpoint must not
enter the still frame early; do not put the entire action sequence into the still frame.

Do not conflate the three evidence types:

- **Image-prompt item**: a visible level-two `IMG-...` entry in 《图片提示词.md》; it proves only that the prompt exists;
- **Input reference image**: a real image supplied by the creator, or produced after confirmation and currently readable. Bind each image to a stable `REF-...` slot with explicit order, visible project-relative path, Chinese name, purpose, control scope, and prohibited-control scope;
- **Visual evidence**: textual facts from 《视觉设定.md》; it does not impersonate an image.

**“Visual evidence” is mandatory for every shot and is also the list of characters, locations, and props in that frame.** After writing the frozen keyframe,
backfill it item by item from the completed image using this fixed syntax:

```markdown
- 视觉依据：《视觉设定.md》·人物「江辰」（控制：身份、造型）；地点「旧走廊」（控制：空间地理、出入口、光向）。
```

- Write `《视觉设定.md》·` only once. Join entries with `；`; each entry name must match a heading in 《视觉设定.md》.
- List every character, location, and prop whose identity, look, or geography must be recognized in the image. Small or background characters remain in scope if their identity must be recognizable.
- Exclude offscreen voices, unidentifiable details, and temporary objects requiring no consistency; do not add them merely to fill the list.
- “Control” states what that entry genuinely determines in this shot, limited to what the frame can carry—a hand close-up does not control “episode look.”
- If the shot genuinely contains no visible item requiring consistency, write `无`. This is not permission to omit evidence: named entries in the keyframe are still checked mechanically.

When keyframe prose names an entry that genuinely is not visible in the shot (its owner has left, or the name appears only in screen text),
append an offscreen list to the same field and state truthfully that it is mentioned but absent:

```markdown
- 视觉依据：《视觉设定.md》·地点「教室」（控制：课桌排列、窗位）；道具「旧书包」（控制：磨损、颜色）；画外：人物「小明」。
```

When an entry name is intrinsically unreliable in prose—`道具「手机」` collides with “phone shop,” while `人物「小雨」` collides with “light rain”—
write `画面代称：无` in that entry in 《视觉设定.md》 so the mechanical check stops searching for it by name. “Visual evidence” must still answer truthfully whether the shot depicts it.

Each `REF-...` slot uses this syntax:

```markdown
REF-<slot>（顺序：<n>）· <项目相对路径>《<中文名称>》（用途：<用途>；控制：<范围>；不得控制：<范围>）
```

`用途` answers “what this image determines in this shot” and must be one of
`身份`, `造型状态`, `地理`, `构图`, `尺度`, `效果`, `起始帧`, `结束帧`, or `风格`. See
[Reference Roles](reference-roles.md) for each definition. If one image serves two purposes, split it into two slots rather than writing “complete reference.” A shot permits at most one
`起始帧` and one `结束帧`, and `结束帧` requires `起始帧`. With `用途`, the video prompt can directly answer
“which storyboard start frame and which character/prop/location images should be sent for this shot,” and production no longer has to guess each image's responsibility.

When creators make images elsewhere, those images never enter the project, so no `REF-...` can be written. Use a `PLAN-...` slot instead.
Its syntax matches `REF-...` exactly except that the locator changes from a project-relative path to an existing entry ID in the project:

```markdown
PLAN-<slot>（顺序：<n>）· <IMG-... 或 SHOT-...>《<中文名称>》（用途：<用途>；控制：<范围>；不得控制：<范围>）
```

`IMG-...` identifies a board in 《图片提示词.md》 and `SHOT-...` identifies that shot's frozen keyframe. Both must resolve within the current project,
and an `IMG-...` Chinese name must match its heading. `PLAN-...` means “this image is outside the project and the creator will attach it in this order during generation.”
It is neither “existing image” nor “pending”: it does not claim a file exists and does not mean someone is still being awaited.
`顺序` is the creator's attachment order in the generation interface and the number used for `<Picture N>` in copy-ready prose.
An image already in the project still uses `REF-...`. Both slot types may appear in one declaration, with a single continuous `顺序` across them.

“Input reference image” has four possible readiness outcomes; do not conflate them:

- Bound `REF-...`: the image truly exists in the project and may enter image/reference-to-video or be executed by the production skill;
- Declared `PLAN-...`: the creator prepares the image outside the project and attaches it manually during generation, while the video prompt is still produced normally.
  Because the suite has no file to send, these shots cannot enter the production skill. Before production, place the real file in the project and rewrite the slot as `REF-...`;
- Pending: when no images exist, write `无（待补参考图：……）`. When only some are missing, retain existing `REF-...` or `PLAN-...` entries and append `；待补参考图：……`. The video prompt is not ready;
- `无（创作者已明确选择文生视频）`: the creator understands the consistency impact and explicitly chooses not to use images; text-to-video may proceed.

`IMG-...` is used only for lookup; do not rely on an English slug to explain meaning to the creator. Every reference also gives a short Chinese name and
control scope, and its ID must exist in a current 《图片提示词.md》 heading. The Chinese name aids reading but does not replace the ID as entry identity. If the document or a suitable entry is absent, the storyboard may still
proceed directly from the screenplay and visual specification using the fallback below; do not invent an ID or fabricate the prompt stage:

```markdown
- 图片提示词项：无
- 输入参考图：无（待补参考图：江辰身份、旧走廊地理、本镜起始帧）
- 视觉依据：《视觉设定.md》·人物「江辰」（控制：身份、造型）；地点「旧走廊」（控制：空间地理、出入口、光向）。
```

A prompt entry and a real image are independent. Even when an `IMG-...` entry exists, “input reference image” may remain “none.” When the creator supplies
a real image, there is no need to invent a prompt entry:

```markdown
- 图片提示词项：无
- 输入参考图：REF-JIANGCHEN-LOOK（顺序：1）· 输入/参考图/江辰定妆.jpg《江辰定妆照》（用途：造型状态；控制：本集造型、面料质感；不得控制：镜头构图、动作、表情）
- 视觉依据：《视觉设定.md》·人物「江辰」（控制：身份、体态）。
```

When only some images are ready, do not discard verified images; retain the gap in the same field:

```markdown
- 输入参考图：REF-JIANGCHEN-LOOK（顺序：1）· 输入/参考图/江辰定妆.jpg《江辰定妆照》（用途：身份；控制：脸型、体态、本集造型；不得控制：场景地理、构图、动作）；待补参考图：夜间走廊地理、本镜起始帧
```

When creators make images in their own tools, specify which images to attach to the shot and in what order as `PLAN-...`:

```markdown
- 图片提示词项：IMG-JIANGCHEN-SHEET《江辰角色板》（控制：身份、体态）
- 输入参考图：PLAN-SHOT-START（顺序：1）· SHOT-EP001-001《本镜冻结关键帧》（用途：起始帧；控制：起始构图、站位；不得控制：尚未发生的动作、终态）；PLAN-JIANGCHEN（顺序：2）· IMG-JIANGCHEN-SHEET《江辰角色板》（用途：身份；控制：脸型、体态、本集造型；不得控制：构图、动作、表情）
- 视觉依据：《视觉设定.md》·人物「江辰」（控制：身份、体态）；地点「旧走廊」（控制：空间地理、出入口）。
```

Both may also coexist, each using its own locator:

```markdown
- 图片提示词项：IMG-JIANGCHEN-SHEET《江辰角色板》（控制：身份、体态）
- 输入参考图：REF-CORRIDOR-COMPOSITION（顺序：1）· 输入/参考图/走廊构图.jpg《走廊构图参考》（用途：构图；控制：占画比例、留白；不得控制：人物身份、动作、剧情事件）
- 视觉依据：《视觉设定.md》·人物「江辰」（控制：身份、体态）；地点「旧走廊」（控制：空间地理、出入口）。
```

## `图片提示词.md`

Each item is a production-ready character board, location board, prop board, or state image. The heading uses an `IMG-...` ID; place the prompt text
inside the blockquote under `### 可复制提示词`, retaining only purpose and reference constraints before it.
Here, `IMG-...` is a prompt-entry ID, not a record of a generated image.

```markdown
## IMG-JIANGCHEN-SHEET · 江辰角色板
- 用途：锁定身份、体态和本集造型。
- 参考：无；若有真实参考图，使用与分镜相同的完整 `REF-...` 格式，说明顺序、项目相对路径、中文名称、用途、控制与不得控制范围。

### 可复制提示词
> 按项目提示词语言编写的正文……
```

## `视频提示词.md`

When entries correspond one-to-one with storyboard shots, retain the shot number and use a `MOTION-...` ID. If every `REF-...` and `PLAN-...` under “input reference image” is ready, use image-to-video; the prose
need restate only local starting-point and anti-drift facts required for motion. Use text-to-video only when the field is 输入参考图：无（创作者已明确选择文生视频）; its prose must independently
contain the character, look, location, composition, lighting, and other static visual anchors needed for the shot. Do not substitute `preserve/保持已有外观`
for images the model never received. “Pending reference images” blocks the final video prompt. The video document's “input reference image” must match its storyboard entry verbatim.

Chinese enclosed in quotation marks or `<d>` in copy-ready prose must be found verbatim in 《剧本.md》 or 《视觉设定.md》.
The prompt carries accepted dialogue to the execution layer; it does not improve the character's line.

Unless the screenplay or creator explicitly requires otherwise, the video prose must state directly in the project's prompt language that no extradiegetic subtitles,
captions, or dialogue-text overlays appear at any time in the shot. Do not merely say abstractly that “the text layer is empty”; dialogue occurs only through sound and lip movement. Diegetic text on flags, signs,
screens, and similar surfaces follows the accepted text policy separately: `exact_readable` carries the exact
characters, language, surface, and position. Disabling subtitles must not become a global `no-text` that also erases this diegetic text.

```markdown
## MOTION-EP001-001 · 门外停步
- 分镜：SHOT-EP001-001
- 时长：4s
- 生成方式：文生视频
- 输入参考图：无（创作者已明确选择文生视频）。
- 静态视觉锚点：A lean young East Asian man in a dark-grey worn suit stands outside an old corridor door under cold overhead light.
- 起始帧：SHOT-EP001-001 的冻结关键帧
- 状态链：右手悬在门把上方 → 门内玻璃落地触发他收回右手并转移视线 → 右手收回，视线落到门缝
- 终点：右手收回；门内玻璃落地；人物视线转向门缝。

### 可复制提示词
> A lean young East Asian man in a dark-grey worn suit stands outside an old corridor door under cold overhead light. His right hand starts suspended above the handle, then withdraws……
```

With real input images, switch to “generation mode: image-to-video” and carry the storyboard's complete REF declaration verbatim. Static visual anchors record only
visible starting-point facts required to execute the action that cannot be inferred solely from reference purposes. Do not put paths or REF IDs in copy-ready prose.

## Shared Rules

- Prompt prose must be directly copyable and contain no placeholders, workflow notes, or QA conclusions.
- The blockquote under `### 可复制提示词` is **one** prompt: copy the entire passage from its first line through its last into one generation request. When a dialect divides it into sections such as `subject_definitions` / `overall_soundscape`, those sections remain part of the same prompt; they are not separate submissions, and the first section alone is not the deliverable.
- References use scene/shot/prompt IDs visible in the documents; do not write file hashes or internal paths.
- Do not invent fields the user did not request merely for “completeness.”
- After completing or revising the five documents, run `python3 {技能目录}/scripts/creator_markdown_check.py 剧集/<EP> --project-root .` to validate executable cross-document structure. Content quality still requires creator review.
