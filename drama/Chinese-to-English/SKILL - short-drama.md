---
name: short-drama
description: Initialize and continue short-drama or motion-comic projects on the filesystem, providing creator-first five-document routing, a local Dashboard, production-format decisions, and Look Development. Use when the user asks to “create/continue a short-drama project,” “check progress/next step,” “do Look Development,” “open the dashboard/short-drama creation desk,” or “export production materials,” or when a task spans multiple creative stages. Route explicit writing, asset, prompting, storyboarding, or review requests directly to the corresponding child skill.
license: MIT
---

# Short-Drama Creation Router

This skill handles project initialization, cross-stage routing, production format, and the Dashboard. The owner of each stage writes its substantive content.

## Quick Start

Every project uses the unified [creator-first workflow](references/creator-workflow.md). Maintain
`剧本.md`, `视觉设定.md`, `分镜.md`, `图片提示词.md`, and `视频提示词.md` for each episode as needed; do not establish a parallel structured source of creative truth.
See [Five Creative Documents](references/creator-documents.md) for the detailed writing conventions.

## Routing

| User intent | Owner / behavior |
|---|---|
| Develop the premise, series promise, adaptation, and episode map | `$short-drama-develop`, only when requested |
| Identify episode boundaries in existing complete multi-episode screenplays or scattered drafts | `$short-drama-develop` builds a temporary index from the actual boundaries |
| Analyze a long source work | `$short-drama-novel-analyze`, only when requested |
| Write or revise one episode’s screenplay | `$short-drama-write` → `剧本.md` |
| Break out characters, looks, locations, and props | `$short-drama-assets` → `视觉设定.md` |
| Write asset image prompts | `$short-drama-image-prompts` → `图片提示词.md` |
| Design shots and frozen keyframes | `$short-drama-storyboard` → `分镜.md` |
| Write video/timeline music prompts | `$short-drama-video-prompts` → `视频提示词.md` |
| Generate media | `$short-drama-produce`; preview first, obtain explicit confirmation, then run |
| Review or validate | `$short-drama-review`, only when explicitly requested |
| Initialize, use the Dashboard, or archive named documents | This skill |

Long-form source analysis and episode indexes under `项目开发/` are optional analysis workspaces and do not determine the layout of an individual episode. Writing any episode still maintains only that episode’s five creator-first Markdown documents.

An existing screenplay can go directly to asset breakdown. Existing visual facts can go directly to image prompting or storyboarding. An existing storyboard can go directly to video prompting.
Do not fabricate upstream work merely to complete a nominal pipeline.

## Executing Requests

1. Locate the project or materials supplied by the user and read only the direct inputs for the current task.
2. Give the complete user-named scope to the appropriate owner. Batches control only context; continue them automatically.
3. Ask only about genuine creative forks. Do not ask the creator about schemas, directories, transactions, or validators.
4. After completing the scope, report completed work, key decisions, genuine unresolved items, and optional next steps once.
5. Do not automatically begin review, archiving, or production that the user did not request.
6. When a request spans visual specifications, image prompts, storyboarding, or video prompts, reconcile visual dependencies against the current five documents before finishing.
   Although image prompting and storyboarding may proceed in parallel, do not leave whichever branch finishes later outside the other branch’s updated references.
7. If a video-prompt request encounters “input reference images: none” or still includes “reference images required,” route first to the storyboard owner to inspect project images and refresh bindings. If a matching image exists, continue within the same request; if required images are missing, list them and stop.
   When stopping, present all three options together: put existing images into the project and bind them as `REF-...`; have the creator generate images in their own tool, record a per-shot attachment plan with
   `PLAN-...` for this pass, and continue producing video prompts; or explicitly switch to text-to-video. Producing reference images with this toolkit requires an external
   adapter and credentials and is only one way to follow the first option. Do not describe it as the only entry point or offer only “generate reference images / text-to-video.”
   Do not interpret “none manually specified” as an explicit text-to-video choice. If the shots also lack “visual evidence” in this pass,
   backfill it from the completed frozen keyframes at the same time. Both evidence fields describe the same frame; do not fill only one.
8. If the user names a target video model in the conversation (“write for MiniMax H3,” “use Seedance 2.5”) while `short-drama.json` still has its `production_profile` set to `unset`, first record that choice and its native duration, reference mode, and prompt-body language in the profile, then proceed downstream.
   If a model named in conversation is not persisted in the profile, the next pass falls back to the generic path and has to guess dialect and duration again.

## Initialization and Dashboard

When project configuration is needed, run:

```bash
python3 {技能目录}/scripts/project_tool.py init ./my-drama --title "示例短剧"
```

**English guide (non-executable):** Replace `{技能目录}` with the skill directory. The sample title means “Example Short Drama.”

If the direct input already confirms the creator-facing language, prompt language, aspect ratio, episode count, or target duration per episode, the first `init` should pass the corresponding
`--language`, `--prompt-language`, `--aspect-ratio`, `--episode-count`, and `--target-seconds` options. Omit only unconfirmed values; do not leave confirmed Brief facts as `null` in configuration. When writing a confirmed production profile, always set its state to
`accepted`; `unset` means only undecided and does not imply an intermediate state.
`init` creates only configuration and empty directories. Write documents into `剧集/<EP>/` when creative work begins rather than precreating empty files.
If a project already exists and the user later selects a target video model, write the choice to the profile and show its effects on duration range, reference mode, and
prompt-body language. The profile accepts only published, accepted creator decisions, so this is a three-step process, not a single write. First write one decision record
(`accepted_value` is the object to be stored in `choices`; do not wrap it in another `choices` layer):

```jsonl
{"decision_id":"CD-H3","status":"accepted","target_locators":[{"src":"short-drama","field":"/creator_authority/production_profile/choices"}],"accepted_value":{"target_video_model":"minimax-h3","video_prompt_dialect":"minimax-h3","video_prompt_language":"en","native_duration_seconds":{"min":4,"max":15},"supported_generation_modes":["text","first_frame","first_last_frame","reference"],"audio_generation":"same_pass"}}
```

Then publish, accept, and set the authority:

```bash
python3 {技能目录}/scripts/project_tool.py publish <project> --owner short-drama \
  --artifact-id AR-PROFILE --output "创作者决策/production-profile.jsonl=输入/profile.jsonl"
python3 {技能目录}/scripts/project_tool.py accept <project> --artifact-id AR-PROFILE --decision accepted
python3 {技能目录}/scripts/project_tool.py set-authority <project> \
  --field /creator_authority/production_profile/choices \
  --decision-ref "创作者决策/production-profile.jsonl#CD-H3"
```

**English guide (non-executable):** The protected paths use `创作者决策/` for creator decisions and `输入/` for input files; retain them exactly.

The matching model dialect defines each field’s value. The MiniMax H3 and Seedance dialect files in `$short-drama-video-prompts` both contain recommended profiles.
After writing, use `status` to verify that `video_model_profile` appears.

See [Runtime Preflight](references/runtime-preflight.md) for project discovery and safe writes. When the user explicitly asks for the Dashboard, run:

```bash
python3 {技能目录}/scripts/dashboard_server.py --workspace <workspace> --port 0 --detach --open
```

`--detach` separates the server process from the current shell so it survives the end of the session, terminal closure, or agent exit.
The link therefore remains available throughout the creative process. The live address, port, and pid are recorded in
`<workspace>/.short-drama/dashboard.json` (readable only by its owner), with logs in `dashboard.log` in the same directory:

```bash
python3 {技能目录}/scripts/dashboard_server.py --workspace <workspace> --status   # 打印当前链接
python3 {技能目录}/scripts/dashboard_server.py --workspace <workspace> --stop     # 停止
```

**English guide (non-executable):** The comments mean “print the current link” and “stop.”

If a Dashboard is already running for the same workspace, starting it again prints the same link rather than opening a second port. Add `--restart` only when the port or token truly must change. Without `--detach`, behavior is unchanged: it runs in the foreground and Ctrl-C stops it.

The Dashboard displays and edits creative files; it does not orchestrate workflow or produce media.

## Project-Level Creative Decisions

When production format, visual direction, display surface, or episode-duration targets genuinely constrain several stages, show the options and their effects, then let the user decide.
Look Development is an optional branch, not a mandatory gate before image prompting or storyboarding.

Read only one relevant knowledge file for the question:

- Rule levels and owner routing: [Rules and Routing Index](references/knowhow-index.md)
- Output language, stable IDs, ownership, and safety boundaries: [Contracts and Ownership](references/contract-and-ownership.md)
- Differences among live action, 2D, 3D, ink wash, chibi, and Chinese animation: [Production Formats](references/production-form-profiles.md)
- When representative frames need comparison: [Look Development](references/look-development.md)
- What reference images can control: [Reference Roles](references/reference-roles.md)
- Occlusion, delayed reveal, and when the audience learns information: [Audience Reveal](references/audience-reveal.md)
- Responsibilities of masters, pickups, and alternates: [Pickups and Alternates](references/pickup-and-alternate.md)

## Production and Delivery Boundaries

External production always preserves `preview -> explicit confirm -> run`. Archiving copies only the current documents and finished assets explicitly named by the user, excluding
private inputs, credentials, absolute paths, and hidden runtime state. Do not fabricate approvals, hashes, or a second content system for an archive.

When the user asks “how do I export/deliver the completed work?”, use `export` to package the current state:

```bash
python3 {技能目录}/scripts/project_tool.py export <project> --out <项目外目录>
```

**English guide (non-executable):** Replace `<项目外目录>` with a directory outside the project.

It copies the five existing creative documents from every episode and `剧集/<EP>/制作成果/` into `--out`, adds `manifest.json` and
`checksums.sha256`, and excludes `输入/`, `交付/`, and `.short-drama/`. To include only some episodes, repeat
`--episode EP001`; to include only text, add `--no-media`; to replace an old output directory, add `--overwrite`.
`--out` must be outside the project.

`export` is a **snapshot of current state**. Its manifest always sets `asserts_approval` to `false`; it does not claim that any review or creator acceptance occurred.
The only formal delivery path carrying approval evidence remains `package`/`verify`.

## Installation and Maintenance

Run `python3 scripts/selftest.py` only during installation, upgrades, or troubleshooting.
