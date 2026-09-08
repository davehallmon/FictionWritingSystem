---
name: short-drama-produce
description: After explicit creator confirmation, execute image, video, TTS/voice, or timeline-music production jobs for a short-drama project and write results plus concise run records back to the project. Use when the user asks to “generate this image/video/voice line/music,” “start generating images/videos/speech/music,” “send the confirmed prompts to production,” or requests batch execution of confirmed media jobs. Does not create prompts, shots, dialogue, lyrics, or voice identity, and never treats a preview, “continue,” budget approval, or an existing acceptance state as confirmation for the current paid production job.
license: MIT
---

# Production After Confirmation

This skill only sends completed production specifications safely to the adapter configured in the runtime. Image prompts remain owned by
`$short-drama-image-prompts`, video prompts by `$short-drama-video-prompts`, dialogue and recording sheets by
`$short-drama-write`, and voice identity by `$short-drama-assets`.

## Quick Start

Only after the user explicitly requests actual generation, extract the current prompt from `图片提示词.md`, `分镜.md`, or `视频提示词.md`
and create a bounded runtime job. A creator-first job's `source` must point to the current Markdown that owns the prompt,
and `source_entry` must name an allowed level-two heading: for `图片提示词.md`, use `IMG-*`;
for `视频提示词.md`, use `MOTION-*`; for `分镜.md`, use `SHOT-*` (with modality `image`, taking the prose from
`### 冻结关键帧提示词`). The storyboard route is the suite's only route for rendering a shot's starting image into a file, but not the creator's only way to obtain a start frame—
creating an image in another tool and placing it in the project is equally valid; if images never enter the project, use the storyboard's `PLAN-...`.
After an output reaches `剧集/<EP>/制作成果/images/`, the storyboard owner may bind it with `用途：起始帧` as a `REF-...`.
When real reference images exist, fill every `reference_bindings` entry with slot, order, path, Chinese name, purpose, and permitted/prohibited control scope.
Built-in video adapters translate the `用途` field into the vendor's role and accept only published values
(MiniMax: `first_frame`/`last_frame`/`reference_image`/`reference_video`/`reference_audio`;
Seedance: the three `reference_*` roles). A job with reference images but no bindings fails directly; it never guesses a role.
Built-in adapters send local images directly as base64 data URIs, requiring no custom upload service.
When an entry's “input reference image” uses `PLAN-...`, those images live in the creator's own tool and the project has no files to send:
`prepare` fails directly and instructs the creator to place the real files in the project and rewrite the slots as `REF-...`; it does not treat plans as inputs or silently discard references.
`references` may be omitted and generated from binding order, or supplied as an explicit mirror in the same order. Output belongs under
`剧集/<EP>/制作成果/`. The job is temporary production-tool input, not a sixth creative document:

```bash
python3 {技能目录}/scripts/production_tool.py prepare <project> --job <临时-job.json>
```

First display the complete `prepare` preview. No vendor is invoked at this point.

## Hard Gate

Every production job must follow these four steps in order; they cannot be combined:

1. Create one bounded job: one modality, explicit quantity, complete prompt/specification, reference files, parameters, output paths, and adapter profile.
2. Run `prepare` and show the creator the complete returned preview, especially quantity, prompt, source entry,
   reference bindings, references, outputs, overwrite behavior, and adapter. At this step, creator-first jobs mechanically check
   the copy-ready prompt under the selected heading and every reference slot, order, path, Chinese name, and control boundary; any drift fails closed.
3. Wait for the creator to confirm explicitly **after seeing this preview**. Run `confirm` only when they clearly approve this current job.
   “Continue,” “finish everything,” “the budget is fine,” acceptance of upstream content, or confirmation of another version does not confirm this production job.
4. Run `run`. It consumes the one-time confirmation before starting the adapter. Any execution after success or failure requires new confirmation,
   preventing an accidental second charge during failure recovery.

Any change to the job, prompt, parameters, output path, or direct input immediately invalidates the old confirmation. Never fill in confirmation for the creator.
The currently confirmed job is the only work unit for this cycle. After it finishes, report the result and return control; do not prepare another batch or start review automatically.

Paths in “input reference image” in `分镜.md` are human-readable evidence and intended use from the creative stage, not a production-input snapshot. At production time,
the creator-first job must create bindings from the corresponding entry in `图片提示词.md` or `视频提示词.md`. The `prepare` preview's
`reference_bindings`, `references`, and confirmed job authoritatively determine which file bytes the adapter actually reads and what each may influence.
Non-creator structured specifications may omit `source_entry`/`reference_bindings` and continue using explicit `references` only. But any new image/video job whose
`source` points to canonical `图片提示词.md` or `视频提示词.md` must use the corresponding selector; omitting fields cannot downgrade or bypass the rule.
Jobs prepared and saved before the upgrade may still be read by their original fingerprints.
New production results do not automatically backfill or refresh the storyboard. To use one as later input, the storyboard owner revises the document, then creates a new job
and repeats preview and confirmation.

## Commands

Only after crossing the production boundary, write the current prompt and runtime parameters to temporary JSON. For video and image jobs,
`parameters.prompt_language` follows the language parsed from the current copy-ready prose, so adapter-appended reference constraints
use the same language rather than reverting to fixed English. Do not pre-create a job for every prompt during the creative stage.
For format and adapter contracts, see
[adapter-contract.md](references/adapter-contract.md). Commands are provided by
[production_tool.py](scripts/production_tool.py):

```text
python3 <本技能目录>/scripts/production_tool.py prepare <project> --job <job.json>
python3 <本技能目录>/scripts/production_tool.py confirm <project> --job-id <id> --confirmation "CONFIRM <id> <code>"
python3 <本技能目录>/scripts/production_tool.py run <project> --job-id <id> --adapter-config <outside-project-config.json>
python3 <本技能目录>/scripts/production_tool.py status <project> --job-id <id>
python3 <本技能目录>/scripts/production_tool.py audit <project>
```

`prepare` validates and previews only; it does not produce. `confirm` stores only a one-time confirmation bound to the current job fingerprint.
`run` starts the adapter. `audit` reconciles only local job history, recovery after failure, repeated-content attempts, and current output bytes.
It neither invokes a vendor nor presents technical success, file existence, or matching hashes as a media-quality verdict. When a job has an unresolved
`running` attempt, preparing, confirming, or running it again is prohibited; wait for completion or investigate the residual attempt first.

## Input Selection

- **image**: read from `图片提示词.md` the current `IMG-*` copy-ready prose, or from `分镜.md` the current `SHOT-*`
  frozen-keyframe prose, adding necessary references and explicit output dimensions/quantity. A creator-first job uses `source_entry`
  to lock the entry. Asset boards use `IMG-*`; a shot's starting image uses `SHOT-*`. They do not replace each other.
- **video**: read from `视频提示词.md` the current `MOTION-*` copy-ready prose and verify the corresponding shot,
  frozen keyframe, duration, and aspect ratio in `分镜.md`. A creator-first job uses `source_entry` to lock the entry. When a continuous segment
  continues from the generated result of a previous segment, the next job binds both the actual previous video and its actual extracted tail frame, preserving
  distinct `continuity_video` and `actual_tail_frame` responsibilities; the target-model adapter translates the vendor role. H3 translates this pair uniformly as
  `reference_video + reference_image`, never `reference_video + first_frame`; a planned tail frame or prose description cannot replace real files.
- **tts**: read the original line and performance requirements from `剧本.md`; the user or existing media explicitly supplies the voice reference. Do not change wording inside the production job
  or create a sixth creative document for TTS.
- **music**: read the creator-confirmed timeline-music section in `视频提示词.md`. A theme song uses confirmed lyrics; instrumental music
  carries no lyrics. When the vendor cannot promise exact duration, generate a source track and let editing implement the documented landing points, loops,
  fades, and dialogue ducking.

One job never mixes modalities. Split large batches into jobs whose quantity and cost boundaries the creator can understand; do not hide an entire season inside one confirmation.

## Adapter Boundaries

Adapter configuration must remain outside the project and contain only argv commands and timeout. The adapter reads credentials from the process environment or system credential
store. Project jobs, confirmation records, run records, and the Dashboard must never store secrets.

The script invokes argv arrays through JSON stdin without using a shell or concatenating commands. The adapter returns local temporary files; the tool accepts only
results matching confirmed targets exactly and atomically copies complete files into the project's `剧集/<EP>/制作成果/` directory.
The project and upstream skills do not hard-code vendors, models, or fast-changing APIs.

Built-in image/video compilers append a deterministic reference-semantics statement to the vendor prompt from confirmed `reference_bindings`, in order,
including Chinese name, purpose, permitted control, and prohibited control. They do not mistake slot names for text to render in the image.
External adapters must also preserve these semantics or reject the job explicitly; they cannot merely upload files while silently dropping control boundaries.

This skill optionally includes four standard-library adapters, selected through an adapter config outside the project, with credentials read only from the runtime:

- [Seedance](references/providers/seedance.md): the account must explicitly configure model/Endpoint ID. The compiler supports official image, video, and audio reference roles;
  the built-in runtime still rejects local reference files when trusted upload is not configured.
- [GPT Image 2](references/providers/gpt-image-2.md): uses generation without references and edit with reference images;
  enforces high-fidelity references and validates size, format, and transparency constraints.
- [MiniMax Music](references/providers/minimax-music.md): uses `music-3.0` and hex results, distinguishes theme songs
  from instrumentals, and does not fabricate a duration request field.
- [MiniMax H3 Video](references/providers/minimax-h3-video.md): the account must explicitly configure model ID, allowed resolutions, and duration range.
  Prompt text enters the `content` text item; reference images bind by explicit role, and local references fail closed without trusted upload.
  This model generates audio with the image in one pass; see the target-model capability profile in the video-prompt skill for writing implications.

These adapters are validated request contracts, not guarantees of account access or output quality. Formal production must still pass the current confirmation gate above,
and the Review skill judges artifact quality.

The repository's `fixture_adapter.py` is only for offline tests; it does not represent real generation quality or the default production adapter.

## Results and Verification

After success, report actual output paths, media types, and runtime status. Do not present “adapter returned success” as a quality conclusion.
After multiple jobs or retries, run `audit` first. Route terminal failures according to `retryable`; retry still requires new explicit confirmation. If output is missing or
its hash/size no longer matches the run record, verify the current bytes or reproduce. `repeated_content` is only a cost and diagnostic signal;
it cannot automatically decide whether retrying identical content is reasonable. `running_attempt` is an unresolved operational state and audit must return attention.
Failures take three routes. Technical failures such as timeouts, rate limits, and server errors may receive bounded retries. If the failure identifies which
input was rejected—prompt text, reference image, or audio—change that input before resubmitting: if text is rejected, rewrite that sentence, replacing “a punch smashes
into the opponent's face, blood dripping down his chin” with “a punch misses as the opponent sidesteps, knocking over a cup on the table”; if a reference image is rejected, replace it with
an image consistent with composition and character that is itself compliant; if audio is rejected, re-record that line. Write the change into a new job and run prepare again so the
creator sees exactly which input changed before confirming. Confirming an identical resubmission creates no repair—only another charge. Repeated-content
defects return to the responsible prompt/specification owner.
For quality verification, the report may pass existing results to `$short-drama-review` as a separate request; do not start review automatically inside a production call.
The Dashboard displays files and runtime summaries only; it provides no adapter settings or production buttons.

## Installation Maintenance

Run offline self-tests only during installation, upgrade, or troubleshooting—not during ordinary creative work or production preparation:

```bash
python3 scripts/selftest.py
python3 scripts/provider_adapters.py --selftest
```
