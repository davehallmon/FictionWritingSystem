# Contributing Guide

Thanks for your interest in the web-novel writing skill pack — contributions are welcome.

## Repository Structure

```
skills/
├── story/                   # Toolbox router
├── story-setup/             # Environment setup
├── story-import/            # Reverse import
├── story-long-write/        # Long-form writing
├── story-long-analyze/      # Long-form deconstruction
├── story-long-scan/         # Long-form trend scan
├── story-short-write/       # Short-form writing
├── story-short-analyze/     # Short-form deconstruction
├── story-short-scan/        # Short-form trend scan
├── story-deslop/            # De-AI-ify
├── story-review/            # Multi-perspective review
├── story-cover/             # Cover generation
└── browser-cdp/             # Browser control
scripts/                       # Dev guards / tests / code generation (full index in scripts/README.md)
```

Each skill consists of a `SKILL.md` (entry point) and a `references/` directory (knowledge base).

## Feedback & Requests

- A stably reproducible command, file, state, or runtime anomaly: open a **Bug report**.
- Voice, characters, pacing, logic, or AI-tone issues that don't meet expectations: open an **Output Quality Case**, with the minimum required context, a continuous output snippet, the specific problem location, and the desired direction.
- New capabilities or Runtime / IDE adapters: open a **Feature Request**, describing the real usage problem and a verifiable outcome; adapter requests should also link the official extension or Skills docs.
- Usage help, workflow choices, and general discussion: head to [GitHub Discussions](https://github.com/zenstory-ai/oh-story-claudecode/discussions).

Issues are actionable work input. If reproduction steps, actual output, a specific problem location, or a verifiable outcome is missing, the maintainers will ask for it; long-unfilled items will not be added to the dev roadmap. **Do not submit API keys, tokens, personal information, or book drafts you don't have the right to share or don't want to share.**

## Skill Format

Every `SKILL.md` must start with frontmatter:

```yaml
---
name: skill-name
description: "One-line description. Triggers: /skill-name, trigger word 1, trigger word 2"
metadata: {"openclaw":{"source":"https://github.com/zenstory-ai/oh-story-claudecode"}}
---
```

For OpenClaw compatibility, the frontmatter must use single-line key/value pairs: `description` must not use `|`/`>` blocks, and `metadata` must be a single-line JSON object. Put longer trigger descriptions in the body.

Files in `references/` are loaded by the skill on demand and are not all stuffed into context.

## How to Contribute

### Improving an Existing Skill

1. Fork the repo
2. Branch from `main`: `git checkout -b feat/your-feature main`
3. Edit the relevant `SKILL.md` or `references/` files
4. Open a PR describing what you changed and why

### Adding a New Skill

1. Create a directory under `skills/` containing `SKILL.md` and `references/`
2. Make sure `npx skills validate` runs clean from the repo root
3. Open a PR

## CI Checks

PRs automatically run `.github/workflows/cross-platform.yml`. The `static-check` job runs the following checks (all mandatory):

- `scripts/static-check.sh` — structured frontmatter parsing, exact Markdown paths/anchors, agent references, and reference reachability; cross-skill file references are forbidden except for the base component `browser-cdp`
- `python3 scripts/skill-numbering.py check` — workflow numbering continuity, binding of references, and fractional-label guards
- `scripts/check-current-skill-contracts.sh` — validates version / Phase / schema / primary deliverables / chapter-outline contract against `scripts/current-contract.json`, blocks legacy paths and silent-compat branches
- `python3 scripts/test-current-skill-contracts.py` — current-contract manifest vs. primary-deliverable fail-fast semantic regression
- `scripts/check-doc-budget.sh` — word-count budget (per `scripts/doc-budget.json`) for hot-path SKILL/references/agent templates, preventing silent bloat of rule text that has to be paid for every session
- `scripts/check-hook-regex-sync.sh` — hook foreshadowing-status detection behavior
- `scripts/check-shared-files.sh` — shared-runtime asset manifest + cross-skill reference copy consistency
- `scripts/check-scan-runtime-policy.sh` — scraper local-date dependency and CDP source-strategy guards
- `python3 scripts/test-scan-runtime-policy.py` — verifies that irrelevant/dead-code keywords cannot fool the scan/browser policy guards
- `scripts/check-story-setup-deployment.sh` — story-setup deployment integrity
- `scripts/check-claude-adapter.sh` — Claude marketplace vs. skill mapping
- `scripts/check-opencode-adapter.sh` — OpenCode adapter sync, commands/agents/config structure, and plugin real-behavior checks
- `scripts/check-openclaw-skills.sh` — OpenClaw single-line frontmatter, `metadata.openclaw`, and optional real-CLI discovery
- `scripts/check-codex-adapter.sh` — Codex repo-skills symlink, custom-agent TOML, hook-generation determinism, and launcher contract
- `scripts/test-codex-hooks.sh` — Codex hooks synthesized-event tests
- `scripts/check-antigravity-adapter.sh` — Antigravity project-skill materialization, Markdown agents, Always-On Rule, named-group hooks, and merge/behavior regression
- `node scripts/test-antigravity-hooks.mjs` — Antigravity official Hook I/O, artifact bridging, and Stop single-continue tests
- `scripts/check-zcode-adapter.sh` — ZCode plugin/marketplace, 13 Skills/Commands, supported hook events, and deployment anchor checks
- `scripts/test-zcode-hooks.sh` — ZCode strict JSON hook contract, prose guards, continuity, and cross-platform Node runner tests
- `python3 scripts/test-storyctl.py` — `visible_chars_v1` counting, two-layer intervals, structured CLI, and demo-same-metric evidence runtime regression
- `node --check` syntax validation for scraper scripts

The list above is representative; **the mandatory list is governed by `.github/workflows/cross-platform.yml`**, and what each script does and when it runs is in [scripts/README.md](scripts/README.md). There's also `.github/workflows/cli-compat.yml`, which on relevant PRs, weekly schedules, or manual triggers installs the official current versions and runs unauthenticated smokes against the real Claude Code, Codex, OpenCode, and OpenClaw.

There are also Windows / macOS jobs that verify `cdp-utils` loads and the setup script dry-runs.

Before committing, run the Linux CI mandatory list locally:

```bash
bash scripts/static-check.sh
python3 scripts/test-static-check.py
python3 scripts/skill-numbering.py check
bash scripts/test-skill-numbering.sh
bash scripts/check-current-skill-contracts.sh
python3 scripts/test-current-skill-contracts.py
bash scripts/check-doc-budget.sh
bash scripts/check-hook-regex-sync.sh
bash scripts/check-shared-files.sh
python3 scripts/test-shared-assets.py
python3 scripts/test-shared-references.py
node scripts/test-normalize-punctuation.js
node scripts/test-scan-runtime.js
bash scripts/check-scan-runtime-policy.sh
python3 scripts/test-scan-runtime-policy.py
bash scripts/test-ai-patterns.sh
node scripts/test-phase2-contract.js
node scripts/test-delivery-contract.js
bash scripts/check-reference-gates.js
node scripts/test-outline-contract.js
bash scripts/test-degeneration.sh
bash scripts/test-prose-backstop-hook.sh
bash scripts/test-prose-net-parity.sh
bash scripts/test-story-continuity.sh
python3 scripts/test-storyctl.py
python3 scripts/test-author-memory-commit.py
bash scripts/check-story-setup-deployment.sh
bash scripts/check-claude-adapter.sh
bash scripts/check-codex-adapter.sh
bash scripts/check-opencode-adapter.sh
bash scripts/check-openclaw-skills.sh
bash scripts/test-codex-hooks.sh
bash scripts/check-python-invocation.sh
bash scripts/check-hook-locale-safety.sh
bash scripts/test-hook-encoding-portable.sh
bash scripts/test-charcount-portable.sh
bash scripts/test-charcount-portable.sh --stub

# Optional real-CLI smokes (require each CLI installed)
CLAUDE_REAL_CHECK=1 bash scripts/check-claude-adapter.sh
bash scripts/test-codex-cli-e2e.sh
bash scripts/test-opencode-cli-e2e.sh
OPENCLAW_REAL_CHECK=1 bash scripts/check-openclaw-skills.sh
```

## Workflow Numbering

When adding or adjusting workflow steps, use continuous integers like `Step 1`, `Step 2` in explicit headings; do not create `Step 1.5` / `Phase 2.1` / `Stage 0.5` just to insert a step, and do not use `### 2.1` or `- 2.1` in `SKILL.md` in place of an explicit workflow heading. The `3.1` chapter/list numbers inside `references/` manuals themselves are not affected by this rule.

Preview number changes before writing them, then write and review:

```bash
python3 scripts/skill-numbering.py audit
python3 scripts/skill-numbering.py fix --dry-run
python3 scripts/skill-numbering.py fix --write
python3 scripts/skill-numbering.py check
```

Auto-fix only renumbers explicit `Step N` headings and unambiguously-bindable references. A fractional Step reference that cannot be bound, or a one-to-many mapping, causes the whole write to fail before touching disk. Phase, bare-numbered headings, and bullet sub-steps need to be named semantically by hand. The full algorithm and local-path usage are in [scripts/README.md](scripts/README.md#workflow-numbering-maintenance).

Any assertion about agent / skill / plugin / hook protocols must first be cross-checked against the official documentation of that project and then verified with a real-CLI output; do not infer from similar fields of other agents.

## Shared Files

Some files are shared across skills (e.g., `banned-words.md`, `anti-ai-writing.md`); modifications must be synced to all copies.

- The single source / target definitions for runtime scripts live in `scripts/shared-assets.json`; change the `source` first, then run `python3 scripts/sync-shared-assets.py sync`.
- A same-named runtime script can belong to only one canonical group, and every target must preserve the source's basename; renaming a target to bypass single-owner rules is forbidden.
- The canonical source, deployment copies, and directory mirrors of reference documents are explicitly defined in `scripts/shared-references.json`; change the source first, then run `python3 scripts/shared-references.py sync`. Reference targets may use semantic aliases, but every path must be registered in the manifest.
- `shared-references.py check` also scans for unregistered exact copies across Skills via content hash; a directory mirror's `files` must fully cover the source tree — new files cannot bypass the manifest.
- `check-reference-similarity.py` scans for near-copies across Skills; historical derived files that still need to evolve independently must register members and divergence reasons in `derived_groups`. New copies must choose between "register and sync" and "form genuinely independent content" — they cannot evade the owner by renaming.
- `analysis-short-*` in `story-short-analyze` is the source-text observation ruler, not a writing playbook; re-introducing long-form nodes, volume-level loops, recommended-structure percentages, or "every chapter must have" catchphrases is forbidden. Guarded by `check-short-analysis-scope.py`.
- Before committing, run `bash scripts/check-shared-files.sh` uniformly; unregistered same-named runtime scripts will fail directly.

### Knowledge-Base Contributions

The most valuable contribution types:

- **Real-world data** — latest charts analysis per platform, shifts in genre trends
- **New genre frameworks** — new writing formulas and structural templates
- **De-AI-ify rules** — new AI-tell patterns, rewrite examples
- **Platform rule updates** — submission requirements, recommendation-mechanism changes

## Quality Requirements

- **Actionable** — content must let an AI agent execute directly; do not write tutorials
- **Concise** — use tables and templates, not long prose
- **Self-contained** — runtime skills are forbidden from cross-skill path references. When shared references are truly needed, publish via a canonical source + manifest-managed local deployment copies so each skill installs independently
- **Chinese** — all content in Chinese

## Submission Flow

```
fork → branch → commit → PR → review → merge
```

- One PR, one focused change
- Commit messages in Chinese, format: `type: short description`
- Types: `feat` (new) / `fix` (fix) / `docs` (docs) / `refactor` (refactor)

## OpenCode Template Sync

This project also supports Claude Code, Google Antigravity, OpenCode, Codex, ZCode, OpenClaw, and Reasonix (Phase 1). The OpenCode agent templates and project-instructions templates are auto-generated from the Claude Code templates by `scripts/sync-opencode.py`.

### When to Sync

After modifying any of the following files, run the sync script:

- `skills/story-setup/references/templates/agents/*.md` (agent definitions)
- `skills/story-setup/references/templates/CLAUDE.md.tmpl` (project-instructions template)

### Sync Steps

```bash
python3 scripts/sync-opencode.py
python3 scripts/sync-opencode.py --check  # Optional: validate only, no file changes
bash scripts/check-opencode-adapter.sh
bash scripts/test-opencode-cli-e2e.sh  # Optional: requires opencode installed locally
```

The script will:
1. Convert the Claude Code agents under `templates/agents/` to opencode format and write to `opencode/agents/`
2. Copy `CLAUDE.md.tmpl` to `opencode/AGENTS.md.tmpl`, replacing `.claude/` path references
3. Print a sync-result summary
4. The optional real-CLI smoke creates a temp project to verify the 13 slash commands, 7 agents, and `story-hooks.ts` plugin can be parsed and loaded by OpenCode

### CI Detection

If a PR modifies Claude Code template files, CI automatically detects whether the opencode templates are in sync, and additionally checks `opencode.json.patch`, the 13 commands, the 7 agents' structure, and the actual guard/cleanup behavior of `plugin.ts`. If CI fails, run the local sync script and `bash scripts/check-opencode-adapter.sh`, then commit the result.

### Manually-Maintained Parts

The following files cannot be auto-generated and must be maintained by hand:

- `skills/story-setup/references/opencode/plugin.ts` — hooks logic
- `skills/story-setup/references/opencode/commands/` — slash commands
- `skills/story-setup/references/opencode/opencode.json.patch` — config snippets

### Known Limitations of sync-opencode.py

After running the sync script, the following manual checks are needed:

- **Path-resolution section** — already handled automatically by `fix_path_rules_section()`, no manual fix needed
- **Agent count** — confirm `opencode/agents/` always contains exactly 7 files

### Key OpenCode Compatibility Issues

**Glob does not search hidden directories:** opencode's Glob tool does not search the `.opencode/` directory, which led to the following design decisions:

- **agent-references** is deployed to `skills/story-setup/references/agent-references/` (non-hidden), not `.opencode/skills/`
- **agent files** are deployed twice: `.opencode/agents/` (used by the opencode system) + `agents/` (Glob-visible copy)
- **subagent detection** — every skill that spawns agents (story-review, story-long-write, story-deslop, story-import, story-long-analyze, story-short-write) only checks the current runtime's canonical directories: Claude `.claude/agents/`, OpenCode `.opencode/agents/`, Codex `.codex/agents/`, Antigravity `.agents/agents/`; do not false-positive just because other endpoints' files exist. ZCode 3.3.4 and OpenClaw Phase 1 do not deploy project agents and fall back to solo/direct.

**Plugin output is invisible:** opencode plugin's `output.extra.system` has been removed (the field does not exist in the real API). System-prompt injection now goes through `experimental.session.compacting`'s `output.context` to deliver the writing context.

**Session-start system-prompt injection is not supported:** the OpenCode public Plugin API has no `chat.message` or equivalent hook, so deployment-status detection and writing progress cannot be injected into the model context at session start. Users can run `/story-setup` manually to check status.

**Other hook differences:** `detect-gaps` (gap detection) plugin is not ported — session start does not inject prompts (only compact summaries and outline-before-prose guards are kept); `session-end` has no equivalent event in opencode and is not currently supported; `validate-commit` now uses git's native `pre-commit` hook (works for every CLI).

### OpenCode Usage Notes

- **Restart opencode after first deployment:** the slash commands in `.opencode/commands/` deployed by story-setup only take effect after opencode restarts. Exit opencode, then re-enter with `opencode -c`.
- **Use natural language to trigger first deployment:** in a new project there are no slash commands; trigger story-setup with natural language (e.g., "please use the story-setup skill to deploy the web-novel writing environment").
- **opencode does not hot-reload config:** after modifying `opencode.json`, agent files, or the plugin, you must restart opencode.
- **Long browser-cdp operations can hang:** opencode has no background-task mechanism, so long browser operations require the user to press `ESC` to interrupt (the SKILL.md already includes inline timeout-wrapping guidance).

## OpenClaw Adapter Maintenance

OpenClaw currently uses a **Phase 1 skills-only** adapter:

- The canonical source remains the repo-root `skills/`; do not maintain a second copy of skills for OpenClaw.
- All `SKILL.md` frontmatter must conform to OpenClaw/AgentSkills constraints: single-line `name`, single-line `description`, single-line JSON `metadata`, with `metadata.openclaw` present.
- `metadata.openclaw.requires.bins/env/config/anyBins` is used for OpenClaw load-time gating; e.g., `story-cover` uses `GPT_IMAGE_API_KEY` to control visibility.
- `story-setup target_cli=openclaw` only deploys the project `skills/` and `references/openclaw/AGENTS.md.tmpl`; it does not deploy OpenClaw agents / hooks / plugin.
- OpenClaw snapshots eligible skills at session start; after changes you need a fresh session or must wait for the skills watcher to refresh.

### OpenClaw Check Steps

```bash
bash scripts/check-openclaw-skills.sh
OPENCLAW_REAL_CHECK=1 bash scripts/check-openclaw-skills.sh  # Optional when openclaw is installed locally
```

`OPENCLAW_REAL_CHECK=1` creates an isolated agent with a temp profile + temp workspace to confirm the OpenClaw CLI can discover the 13 story skills from the workspace `skills/`; the script cleans up the temp profile when done.

### OpenClaw Known Boundaries

- **Agents deferred:** OpenClaw's agent/session model differs from Claude/Codex project-internal agent files; OpenClaw Gateway agents are not generated. Any skill involving agent collaboration must fall back to solo/direct.
- **Hooks deferred:** outline-before-prose guard, commit reminder, and session-start/compact injection are not migrated to OpenClaw hook/plugin; under OpenClaw they are only soft skill-flow constraints.
- **Package deferred:** OpenClaw can recognize workspace / personal / managed skill roots; we are not publishing an OpenClaw-native plugin package at this stage.

## Google Antigravity Adapter Maintenance

Antigravity 2.0 and the `agy` CLI share the `.agents/` workspace-customization mechanism, but before each release we still recommend smoke-testing the IDE and the interactive CLI separately. The supported surface is entirely deployed by `story-setup` to the writing project; the deployer does not write `~/.gemini/`:

- 13 skills are materialized to real `.agents/skills/{name}/`. `deploy-antigravity-skills.py` only replaces known names and preserves user Skills; existing symlinks default to fail-closed, only migrate after explicit user agreement, and never write through the link to the target directory.
- 7 custom subagents are generated from the Claude Markdown source into `.agents/agents/agent-name/agent.md` (where `agent-name` is the actual name) at deployment time. Tool names must come from the official list; calls use `invoke_subagent` + a matching `TypeName`; the generator only replaces the 7 known definitions and preserves other user agents.
- The Always-On Rule is fixed at `.agents/rules/oh-story.md` and the file must be under 12,000 characters. It is responsible for skill routing and re-reading `追踪/上下文.md` after compact; do not assume Antigravity has Claude's PreCompact/PostCompact.
- `.agents/hooks.json` is a top-level named-group mapping. The merger only replaces the `oh-story` group and preserves all user groups. Currently registered: `PreToolUse`, `PostToolUse`, `PreInvocation`, `Stop` — PreToolUse must output `decision`, PostToolUse must output exactly `{}`; post-write findings are stored in the session's `artifactDirectoryPath`, injected by the next PreInvocation, and Stop may force at most one continue.
- `.agents/hooks/` only manages `story_antigravity_hook.js` and the shared `story_hook_core.js`; the latter is byte-locked by `scripts/shared-assets.json` and must not be hand-edited in the copy. Hooks require Node on PATH.

Check steps:

```bash
bash scripts/check-antigravity-adapter.sh
python3 scripts/test-antigravity-skills-deploy.py
python3 scripts/test-antigravity-hook-merge.py
node scripts/test-antigravity-hooks.mjs
```

If the local machine has a current Antigravity 2.0 / `agy`, then in a temp writing project run `story-setup` once, open a new conversation, and verify discovery with `/skills`, `/agents`, `/hooks`, and verify the IDE and the interactive CLI separately. The `agy 1.1.22 -p` headless process scans the workspace before silent authentication finishes and does not reload custom agents/hooks after authentication; real testing has shown `subagent not found` or ordinary model output being written to `~/.gemini/antigravity-cli/scratch/`, so it is not currently used as a supported entry point or smoke means. Check and clean up any unexpected scratch artifacts after testing. Automation does not read or write user global customization, nor does it replace this real-machine step.

## ZCode Adapter Maintenance

ZCode uses the dual entry of "native plugin + `story-setup` workspace deployment":

- `.zcode-plugin/plugin.json` and the root `marketplace.json` expose the same 13 Skills, 13 Commands, and ZCode Hooks; the version must be in sync with `skills/story/VERSION`.
- `skills/story-setup/references/zcode/` is the workspace deployment template, containing `AGENTS.md.tmpl`, Commands, `config.json.patch`, and a Node Hook runner with no third-party dependencies.
- ZCode 3.3.4 only supports `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PostToolUseFailure`, `Stop`. Do not copy Claude's `PreCompact`, `PostCompact`, `SessionEnd`, `SubagentStop`, or `Notification`.
- Empty hook stdout means allow; whenever non-empty it must satisfy a strict JSON schema. Diagnostics only go to stderr, exceptions fail open; prefer `process` + `node` over shell/Python-launcher cross-platform branches.
- 3.3.4 does not execute project-level or plugin custom agents, and does not discover `.zcode/rules`. Do not generate `.zcode/agents/` / `.zcode/rules/` or default-write to user home; any skill involving specialist agents must explicitly report a solo/direct fallback.

### ZCode Check Steps

```bash
bash scripts/check-zcode-adapter.sh
bash scripts/test-zcode-hooks.sh
bash scripts/test-prose-net-parity.sh
```

When updating the prose lightweight deterministic net, you must sync the Claude, OpenCode, Codex, Antigravity, and ZCode endpoints, and the shared-assets / parity / Antigravity hook tests must pass.

## Reasonix Adapter Maintenance

Reasonix (DeepSeek-Reasonix CLI) currently supports skills + a native plugin manifest + a skills-only project-level `story-setup` deployment; hooks and custom agents are deferred to a later stage (skills involving specialist agents fall back to solo/direct):

- The root `reasonix-plugin.json` is the plugin manifest; `version` must be in sync with `skills/story/VERSION` (guarded by `check-reasonix-adapter.sh`).
- Reasonix natively scans project skill roots (`.agents/skills`, etc. — a symlink to `skills/`, shared with Codex) and discovers 13 skills.
- `story-setup`'s `target_cli=reasonix` runs a skills-only deployment: copy 13 skills to the project's `skills/`, write `references/reasonix/AGENTS.md.tmpl`, do not deploy hooks/agents (same shape as OpenClaw / generic, guarded by `check-story-setup-deployment.sh`). When changing the Reasonix deployment path or template, sync that guard.
- Real-CLI verification `reasonix doctor capabilities` is not in CI; you can run it manually before a release.

### Reasonix Check Steps

```bash
bash scripts/check-reasonix-adapter.sh
```

## Codex Adapter Maintenance

This project also supports Codex CLI (repo skills discovery + `$story-setup` project deployment):

- **Repo-local skills** — `.agents/skills` is a relative symlink to `skills/` (`../skills`, the agentskills.io standard path); Codex scans it to discover skills — do not copy a second copy. It must be a valid relative symlink (`check-codex-adapter.sh` guards `target=../skills`; invalid/absolute paths break discovery, see openai/codex#11314); Windows requires git `core.symlinks=true`. OpenClaw scans the workspace `skills/` natively and does not depend on it.
- **Project deployment hooks** — `skills/story-setup/references/codex/hooks/hooks.json` is intended for `$story-setup` deployment to the writing project. The POSIX `command` and Windows `commandWindows` both walk up from the current directory looking for `.codex/hooks/run-story-hook.*` and do not depend on the Git repo; once found, the shared launcher uniformly handles the event allowlist, interpreter detection, `CODEX_PROJECT_DIR` injection, and Python hook dispatch.
- **Windows hooks** — Codex on Windows uses `%COMSPEC% /C` (cmd.exe) to launch `commandWindows`. Currently registered commands use PowerShell to walk up the directory chain, then call `run-story-hook.cmd`; so nested working directories behave consistently with POSIX instead of only supporting the project root. After changing the event list or launcher you must rerun the generator and the adapter checks; do not hand-copy detection logic across the six registered entries.
- **Custom agents** — `skills/story-setup/references/codex/agents/*.toml` is generated by `scripts/generate-codex-agents.py` from `references/templates/agents/*.md`. After modifying Claude agent templates you must regenerate and commit.

### Codex Sync Steps

```bash
python3 scripts/generate-codex-agents.py
python3 scripts/generate-codex-hooks.py
bash scripts/check-codex-adapter.sh
bash scripts/test-codex-hooks.sh
```

### Key Codex Compatibility Issues

- **Hook trust threshold** — the Codex project `.codex/` config layer must be trusted; non-managed command hooks also need the user to review/trust them in `/hooks` before they run.
- **Hook JSON contract** — the plain stdout of `PreToolUse`, `PreCompact`, and `PostCompact` is ignored; you must output JSON, e.g., `hookSpecificOutput.permissionDecision = "deny"` or `hookSpecificOutput.additionalContext`.
- **PreToolUse interception is incomplete** — the Codex docs note that current shell/edit interception is not a complete security boundary; story hooks are only writing-flow guardrails, not a substitute for version control and human review.
- **Agent file format** — Codex custom agents are `.codex/agents/{name}.toml`, requiring `name`, `description`, and `developer_instructions`; read-only agents use `sandbox_mode = "read-only"`.
- **Custom-agent runtime registration** — after `$story-setup` writes `.codex/agents/*.toml`, you must trust the project `.codex/` config layer and open a fresh Codex session. If the current Codex runtime still returns `unknown agent_type` (reproducible in the local `codex exec 0.141.0` temp-project smoke), the skill must fall back to solo/direct and report the fallback; the automation hard threshold is the TOML schema and file-deployment check.
