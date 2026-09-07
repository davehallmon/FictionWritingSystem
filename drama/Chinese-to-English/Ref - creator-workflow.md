# Creator-First Workflow

## The Only Persisted Artifacts

Maintain five creator-readable Markdown files per episode as needed:

| Stage | owner | File |
|---|---|---|
| Script | `short-drama-write` | `剧集/<EP>/剧本.md` |
| Visual assets | `short-drama-assets` | `剧集/<EP>/视觉设定.md` |
| Storyboard and frozen keyframes | `short-drama-storyboard` | `剧集/<EP>/分镜.md` |
| Image prompts | `short-drama-image-prompts` | `剧集/<EP>/图片提示词.md` |
| Video prompts | `short-drama-video-prompts` | `剧集/<EP>/视频提示词.md` |

Do not precreate empty files when there is no content. A request creates only the documents it actually needs. It is valid to enter directly at the script, visual-definition, storyboard, or prompt stage; do not fabricate upstream work merely to complete a nominal pipeline.

Do not persist JSON/JSONL, indexes, fingerprints, coverage tables, QA reports, review forms, handoff capsules, or recovery state for the main single-episode creative chain. When IDs are needed, write them into Markdown headings. Structural checks and batch state remain in the current context and do not become a sixth creative document. See [Five Creative Documents](creator-documents.md) for the recommended form.

Long-form source breakdown or multi-episode material identification may use machine indexes in `项目开发/`. These are optional analysis workspaces created only when the user explicitly requests them, not sources of truth for single-episode creation. Their presence does not change the five-document layout under `剧集/<EP>/` and cannot require a single-episode owner to fabricate parallel structured artifacts.

Creator-facing explanation follows the project language. Image and keyframe bodies follow `prompt_language`. Video bodies preferentially follow the target video-model profile's `video_prompt_language` and `video_prompt_dialect`; when undeclared, fall back to `prompt_language` and general natural language. `native_duration_seconds` takes effect during storyboard planning; do not wait until production submission to discover that a shot is invalid. Without `short-drama.json`, image and keyframe bodies default to `en`. Confirm the target model for video bodies; if the target is also undeclared, use the user's current language. Descriptive language, spoken-dialogue language, and in-frame text are independent; never infer one from another.

Project-level facts the user has already supplied in the Brief or current request must be synchronized to `short-drama.json` during initialization. These include at least the confirmed episode count, target duration per episode, aspect ratio, and target production profile. A production profile has only two project-level states: `unset` and `accepted`. Downstream work reads only an accepted profile and does not substitute a temporary state for a creator decision.
When consecutive segments of the same scene are produced and the target model supports continuation, the production profile declares the continuity route as “previous actual video + actual ending-frame relay.” `one-shot-per-generation`, a single-shot container, or a multishot container describes only packaging granularity and cannot cancel this continuity route.

## Request Scope

The scope named by the user is the scope for the current pass. “Finish this episode” completes the entire episode. “From script through video prompts” completes each named stage in sequence. Scenes, asset groups, and shot groups are only internal context batches; after they pass, continue automatically. Do not return control after each batch or open separate acceptance, review, or QA rounds for every intermediate file.

Stop only in three places:

1. The named scope is complete;
2. Missing facts create a genuine creative branch that would materially change the plot or visual direction;
3. The next step would invoke external production, requiring the exact job to be shown and explicitly confirmed first.

### State the Scope in One Sentence

Requests require no fixed wording, and skills do not depend on keyword matching. The examples below merely show which facts a single sentence should convey; they may be copied or rewritten:

```text
写 EP001 的分镜和每镜冻结关键帧。目标视频模型是 MiniMax H3，先把它写进项目档案。
```

```text
EP001 分镜确认采用，按 MiniMax H3 写视频提示词。人物、场景、道具要跨镜一致，
所以先在项目里找已有的角色图、场景图、道具图和本镜起始帧并绑成参考；缺哪张就列出来，别改成文生视频。
```

```text
EP001 的角色图和场景图在 输入/参考图/ 下，本镜起始帧在 剧集/EP001/制作成果/images/ 下，
请按这些图写 MiniMax H3 的图生视频提示词，逐镜说明送哪一张起始帧、哪些人物/道具/场景图。
```

```text
参考图我自己在 MiniMax 的界面里出，不进项目。EP001 按 H3 写视频提示词，
逐镜告诉我要挂哪几张图、按什么顺序挂、每张管什么。
```

```text
这一集没有也不打算做参考图，明确走文生视频，静态视觉锚点写足。
```

Four facts are worth stating in one request: **which stage of which episode to perform**, **the target video model**, **where reference images are or that they do not yet exist**, and **what to do when no images exist**. If one of the first three is missing, the skill asks or proceeds under the accepted profile. It never assumes the final fact for the creator. That fourth fact has three possible answers: wait for images; have the creator produce them elsewhere and attach them (written as `PLAN-...`); or explicitly use text-to-video. If none is specified, treat the project as still waiting for images.

Structural checks exist to find errors, not to gate creation. Correct issues that can be fixed directly in the current document. Begin review, archiving, and media production only when named by the user. Installation selftests, full QA, and demo validation belong to skill maintenance, not ordinary creative requests.

## Creative Quality

Reducing the file count does not lower content standards. Each owner reads its own craft references for the specific problem and checks plot causality, character voice, asset identity, spatial continuity, shot responsibility, generatability, and prompt boundaries. See [knowhow-index.md](knowhow-index.md) for the complete rule and routing table. The final report states only the completed scope, key creative decisions, genuine unresolved issues, and optional next step; it does not report internal pipeline noise.

## Production Boundary

Image, video, TTS, and music production still follows `preview -> explicit confirm -> run`. Production tools may store jobs, confirmations, and audit records in a hidden runtime directory. These records are necessary boundaries around paid/external side effects; they do not require the model to recopy creative content into long-lived JSON/JSONL. A job must write the Markdown owning the current prompt into `source`, with output written to `剧集/<EP>/制作成果/`. Any change to a prompt, parameter, input, or output path requires a new preview and confirmation.
