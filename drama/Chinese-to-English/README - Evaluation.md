# Evaluation

`examples/` answers, “What do the artifacts look like?” This section answers a different question:

> If a real long-form novel is handed to this skill suite and the documentation is followed from beginning to end, does the workflow still run successfully?

The difference is not scale but **provenance**. The examples under `examples/` were shaped by hand, so they cover only cases we anticipated.
All three defects fixed after v0.4.2 slipped past them for the same reason—**the examples did not contain that kind of input**:

| Defect | Why the examples did not expose it |
|---|---|
| Duration estimation counted voice-over as zero seconds | `[VO]` / `[OS]` appeared zero times across the eight-episode screenplay |
| The voice-script structure could not represent voice-over | There was no voice script at all |
| Rebuilding the index silently renumbered blocks | There was no revised screenplay |

## Let You Manage the Account

Fixed input: `让你管账号/reference-run/输入/长篇-让你管账号，你高燃混剪炸全网.txt`
(147,010 bytes / 52,552 Chinese characters / 20 chapters). Copyright belongs to the repository owner; inclusion is limited to use as an evaluation benchmark and workflow example.

`reference-run/` is a complete artifact set recorded from one actual run of the documented workflow. All 21 artifacts are `accepted`;
EP001 runs 94.8 seconds against a 90-second target. It is a **regression benchmark**, not a model example.

| Stage | Scale |
|---|---|
| novel-analyze S0–S5 | 437 plot points / 14 story units / 24 episode candidates |
| develop | EP001–EP003 episode maps; 13 adaptation mappings with exact spans |
| write | EP001: 44 blocks / 18 spoken lines / complete voice script |
| assets · image-prompts | 2 characters / 2 locations / 2 props; 7 image-prompt specifications |
| storyboard · video-prompts | 20 shots / 20 keyframes / 20 motion specifications / 2 containers / 2 music cues |

It contains all three items named in the opening table: eight voice-over lines, a voice script covering all 18 spoken lines,
and a screenplay index with real revision history.

`reference-run/RUN-LOG.md` records manual interventions and checker errors from that run.
Compare the next live run against it to determine whether an issue is old or new.

## Cross-Genre Content-Quality Gate

`content-quality-corpus.json` v3 freezes 16 synthetic cases covering 16 genres. All 12 cases whose results have already been inspected or used for revision
belong to development. After candidate writing instructions, scales, prompts, thresholds, and the replication plan are frozen, create
four separate holdouts that run only once. The four negative controls include ordinary tasks that do not directly reveal the evaluation target, exposing whether the Skill
spontaneously turns local craft into a universal template. As soon as a holdout result causes any input above to change, retire it to development.
The next conclusion requires a newly created, never-run case; do not repeatedly tune against the same questions until they pass.

Candidate and baseline use the same creative model, task, neutral creation template, and isolated sessions. The generator must not run directly inside
either complete repository worktree. Every invocation uses a sanitized temporary root with no `.git` and no `evaluations/`, materializing only the
`skills/short-drama-write/` bundle bound by the current arm's seal; the prompt is supplied through standard input. The receipt must declare
`workspace_policy: source-bundle-only`, and `workspace_bundle_sha256` must equal the current arm's source bundle;
otherwise the gate fails closed. This constraint prevents the candidate from seeing new tasks, scales, or historical reports that the baseline cannot see.

For each case and each arm, predefine three independent creation replicates and include all with equal weight—no best-of-N and no selective reruns of low-scoring works. Each
replicate is then blind-reviewed independently by Codex and Kimi with swapped A/B positions, producing four reports. One complete round therefore contains 96 creative works and 192
blind-review reports. Kimi CLI provides no independent reasoning-effort switch, so configurations and receipts truthfully record
`provider-default` rather than inventing a setting never passed to the provider.

Blind review likewise must not run in a complete repository or run directory. Every judge invocation uses an empty temporary root containing no `.git` and no files.
The complete task, A/B works, scale, and fixed JSON template are passed only in the invocation prompt and are not materialized in the workspace. The receipt must declare `workspace_policy: prompt-only`
and use the fixed bundle SHA for an empty workspace. Codex can read the prompt from stdin; Kimi uses the noninteractive `--prompt` option.
Neither may write the prompt or evaluation files into the workspace. The judge therefore cannot recover version identity from a manifest, filename, another report, or historical output.
A report missing this identity cannot enter formal aggregation even if its JSON and scores are complete.

[`content-quality-rubric.md`](content-quality-rubric.md) evaluates screenplays only. `content_quality_gate.py` v5
first averages within each replicate, then aggregates cases with equal weight, and finally calculates macro-averages for development, holdout, and the full corpus. It rejects
missing, duplicate, extra, or selectively included replicates. The gate does not trust the run manifest's self-reported genre and split; it verifies each case against the public
corpus and binds the baseline commit, candidate Skill bundle, creation/review templates, scale, model configuration, corpus JSON,
the bundle containing every full task, each work, report, invocation receipt, and external private term list. It separately reports model family, A/B
position, scoring dimension, and per-case changes, and rejects duplicate tasks or reuse of a work across cases, arms, or replicates.

Actual works, receipts, reports, private term lists, and the trusted seal live in ignored `.omx/`. The seal in the manifest is only a copy carried
with the evidence; the gate requires it to match field-for-field the trusted seal separately saved by the maintainer at freeze time and never regenerated by the run script.
At runtime, the maintainer-controlled term list and trusted seal must be supplied explicitly:

```bash
python3 evaluations/content_quality_gate.py path/to/manifest.json \
  --trusted-leakage-terms path/to/maintainer-terms.txt \
  --trusted-seal path/to/maintainer-seal.json
```

Manifest schema v5, corpus schema v3, config schema v3, and receipt schema v2 are all incompatible with earlier formats. This is
an intentional fail-closed change with no compatibility branch. Historical runs that lack a sanitized-workspace identity may serve only as directional diagnostics;
they cannot be recognized retroactively as formal gate evidence.

This evaluation cannot be replaced by asserting that the documentation contains a particular sentence. Generalization of the writing guidance is demonstrated by real cross-genre outputs, one-time holdouts, negative controls, and
blind-review diagnostics. Unit tests verify only the gate's behavior when facing synthetic input, tampering, missing/reused replicates, and fabricated metadata.

## Before Every Release

Use two layers because they can determine different things.

**Regression gate** (script, runs with tests):

```bash
python3 -m unittest tests.test_workflow_evaluation
```

Run the recorded execution through the checkers used by the main workflow again—assets, image prompts, storyboard coverage,
delivery containers, motion duration, music, voice script, and screenplay duration—and verify that each derived layer can still be rebuilt from its source:
can the chapter index be recalculated from the novel into the same table; do block numbers remain byte-for-byte unchanged after rebuilding the screenplay index; are all 21 artifacts still `accepted`?
**This layer determines “no regression”; it does not evaluate dramatic quality.**

Two stages are outside its coverage: `$short-drama-review` is a separately requested review stage,
and `$short-drama-produce` requires a generation backend unavailable locally.

**Live run of the main workflow** (human or Agent, once on the release candidate): the gate runs the recorded result;
this step runs the workflow itself. Create a new project, provide only that novel, and follow each skill's SKILL.md through
EP001 video prompts. Then compare against `reference-run/`—not for identical text (creative artifacts differ every time),
but for **which step requires a person to solve a system problem**, **which checker reports an error**,
and **whether the documented procedure actually works from end to end**.

**Before starting, pin the suite to one commit.** A live run takes several hours, during which skill files must not change:

```bash
git rev-parse HEAD                      # 记下来，写进这次实跑的报告
git worktree add /tmp/eval-run <commit> # 在这份固定副本上跑，不要用正在改的工作区
```

**English guide (non-executable):** Record the current `HEAD` in the real-run report, then create `/tmp/eval-run` at that fixed commit. Run the evaluation in the fixed copy, not in the worktree being edited.

Without pinning, the run is not reproducible: while friction is being recorded, the documented version under observation may already have changed,
making it impossible to identify which version owns the reported issue. This is not theoretical: the v0.5.0 live run crossed
three HEADs, and one finding had to be withdrawn because the defect was fixed at the same time it was encountered.

The third requirement cannot be omitted: one of the most serious defects in the previous round was disagreement between the rebuild procedure documented in `SKILL.md` and the script's actual behavior,
even though every test was green. Classify discovered issues according to `CONTRIBUTING.md` and record them in `CHANGELOG.md`.

The `让你管账号` section still answers only whether the main workflow runs smoothly. Content A/B testing uses the independent cross-genre corpus above;
do not pass off a regression run as evidence of screenplay quality.
