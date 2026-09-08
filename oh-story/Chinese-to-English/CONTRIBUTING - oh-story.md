# Contribution Guide

Thank you for your interest in the web-fiction writing skill package. Contributions are welcome.

## Repository Structure

```
skills/
├── story/                   # 工具箱路由
├── story-setup/             # 环境部署
├── story-import/            # 逆向导入
├── story-long-write/        # 长篇写作
├── story-long-analyze/      # 长篇拆文
├── story-long-scan/         # 长篇扫榜
├── story-short-write/       # 短篇写作
├── story-short-analyze/     # 短篇拆文
├── story-short-scan/        # 短篇扫榜
├── story-deslop/            # 去AI味
├── story-review/            # 多视角审查
├── story-cover/             # 封面生成
└── browser-cdp/             # 浏览器操控
scripts/                       # 开发守卫 / 测试 / 代码生成（完整索引见 scripts/README.md）
```

Each skill consists of a `SKILL.md` entry point and a `references/` knowledge-base directory.

## Feedback and Requests

- For reliably reproducible command, file, state, or Runtime failures, submit a **bug report**.
- When style, characters, pacing, logic, or AI-like writing does not meet expectations, submit an **output-quality case** containing the minimum necessary context, a continuous output excerpt, the exact problem location, and the desired direction.
- For new capabilities or Runtime / IDE adapters, submit a **feature request** describing the real-world problem and an acceptance-testable result. Adapter requests must also provide the official extension or Skills documentation.
- For usage questions, workflow choices, and general discussion, go to [GitHub Discussions](https://github.com/zenstory-ai/oh-story-claudecode/discussions).

Issues are actionable work inputs. If reproduction steps, actual output, the exact problem location, or an acceptance result are missing, maintainers will request more information. Reports that remain incomplete will not enter the development schedule. Never submit API keys, tokens, personal information, or manuscripts that you are not authorized or willing to make public.

## Skill Format

`SKILL.md` must begin with frontmatter:

```yaml
---
name: skill-name
description: "一句话描述。触发方式：/skill-name、触发词1、触发词2"
metadata: {"openclaw":{"source":"https://github.com/zenstory-ai/oh-story-claudecode"}}
---
```

For OpenClaw compatibility, frontmatter must keep one key-value pair per line: `description` must not use a `|`/`>` block, and `metadata` must be a single-line JSON object. Put longer trigger guidance in the body.

Files under `references/` are loaded by the skill on demand rather than all being placed in context.

## How to Contribute

### Improve an Existing Skill

1. Fork the repository.
2. Create a branch from `main`: `git checkout -b feat/your-feature main`.
3. Modify the relevant `SKILL.md` or `references/` files.
4. Submit a PR explaining what changed and why.

### Add a Skill

1. Create a directory under `skills/` containing `SKILL.md` and `references/`.
2. Confirm that `npx skills validate` succeeds from the repository root.
3. Submit a PR.

## CI Checks

PRs automatically run `.github/workflows/cross-platform.yml`. The static-check job runs the following mandatory checks:

- `scripts/static-check.sh` — structurally parses frontmatter; verifies exact Markdown paths and anchors, Agent references, and references reachability; prohibits cross-Skill file references except from the foundational `browser-cdp` component
- `python3 scripts/skill-numbering.py check` — checks continuous workflow numbering, bindable references, and guards against fractional labels
- `scripts/check-current-skill-contracts.sh` — validates the current version / Phase / schema / primary artifacts / detailed-outline contracts against `scripts/current-contract.json`, and blocks historical paths and silent compatibility branches
- `python3 scripts/test-current-skill-contracts.py` — regression-tests fail-fast semantics for the current-contract manifest and primary artifacts
- `scripts/check-doc-budget.sh` — enforces word budgets for hot-path SKILL/reference/agent templates using `scripts/doc-budget.json`, preventing silent growth of rule text paid for in every session
- `scripts/check-hook-regex-sync.sh` — verifies hook behavior for tracking foreshadowing state
- `scripts/check-shared-files.sh` — checks the shared Runtime asset manifest and byte consistency of cross-skill reference copies
- `scripts/check-scan-runtime-policy.sh` — guards scraper local-date dependencies and the CDP source policy
- `python3 scripts/test-scan-runtime-policy.py` — verifies that irrelevant or dead-code keywords cannot fool scan/browser policy guards
- `scripts/check-story-setup-deployment.sh` — checks story-setup deployment completeness
- `scripts/check-claude-adapter.sh` — checks the Claude marketplace and skill mappings
- `scripts/check-opencode-adapter.sh` — checks OpenCode adapter synchronization, commands/agents/config structure, and actual plugin behavior
- `scripts/check-openclaw-skills.sh` — checks OpenClaw single-line frontmatter, `metadata.openclaw`, and optional discovery through the real CLI
- `scripts/check-codex-adapter.sh` — checks Codex repository skill symlinks, custom-agent TOML, deterministic hook generation, and the launcher contract
- `scripts/test-codex-hooks.sh` — runs synthetic-event tests for Codex hooks
- `scripts/check-antigravity-adapter.sh` — checks Antigravity project Skills materialization, Markdown agents, the Always-On Rule, named-group Hooks, and merge/behavior regressions
- `node scripts/test-antigravity-hooks.mjs` — tests official Antigravity Hook I/O, the artifact bridge, and the Stop event’s single continuation
- `scripts/check-zcode-adapter.sh` — checks the ZCode plugin/marketplace, 13 Skills/Commands, supported Hook events, and deployment anchors
- `scripts/test-zcode-hooks.sh` — tests the ZCode strict-JSON Hook contract, prose guards, continuity, and cross-platform Node runner
- `python3 scripts/test-storyctl.py` — regression-tests Runtime behavior for `visible_chars_v1` counting, two-level ranges, structured CLI output, and evidence matching the demo’s measurement method
- Collection-script `node --check` syntax validation

These are representative examples. **The mandatory list in `.github/workflows/cross-platform.yml` is authoritative**. See [scripts/README.md](scripts/README.md) for each script’s purpose and trigger conditions. A separate `.github/workflows/cli-compat.yml` installs current official versions for relevant PRs, weekly schedules, and manual runs, and performs unauthenticated smoke tests against the real Claude Code, Codex, OpenCode, and OpenClaw CLIs.

Separate Windows and macOS jobs verify cdp-utils loading and setup-script dry runs.

Before submitting, it is recommended to run the mandatory Linux CI list locally:

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
node scripts/check-reference-gates.js
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

# 可选真实 CLI smoke（需分别安装对应 CLI）
CLAUDE_REAL_CHECK=1 bash scripts/check-claude-adapter.sh
bash scripts/test-codex-cli-e2e.sh
bash scripts/test-opencode-cli-e2e.sh
OPENCLAW_REAL_CHECK=1 bash scripts/check-openclaw-skills.sh
```

## Workflow Numbering Rules

When adding or adjusting workflow steps, use consecutive integers in explicit titles such as `Step 1` and `Step 2`. Do not insert steps by creating `Step 1.5` / `Phase 2.1` / `Stage 0.5`, and do not replace explicit workflow headings in `SKILL.md` with `### 2.1` or `- 2.1`. The `references/` manuals’ own sections and list numbers, such as `3.1`, are unaffected.

Preview numbering changes before writing them, then recheck:

```bash
python3 scripts/skill-numbering.py audit
python3 scripts/skill-numbering.py fix --dry-run
python3 scripts/skill-numbering.py fix --write
python3 scripts/skill-numbering.py check
```

Automatic repair renumbers only explicit Step headings and references that can be bound unambiguously. An unbindable fractional-Step reference or one-to-many mapping causes the entire write to fail before it reaches disk. Phase headings, bare numbered headings, and bulleted substeps require semantic manual names. See [scripts/README.md](scripts/README.md#工作流编号维护) for the full algorithm and scoped-path usage.

Assertions about agent/skill/plugin/hook protocols must first be checked against the corresponding project’s official documentation and then verified with actual CLI output. Do not infer them from similar fields belonging to another agent.

## Shared-File Rules

Some files are shared across skills, including banned-words.md and anti-ai-writing.md. When editing them, synchronize every copy.

- Runtime scripts have their sole source/target definitions in `scripts/shared-assets.json`. Edit `source` first, then run `python3 scripts/sync-shared-assets.py sync`.
- A same-named Runtime script may belong to only one canonical group, and every target must preserve the source basename. Do not use renamed targets to bypass single ownership.
- Canonical sources, deployed copies, and directory mirrors for reference documents are explicitly defined in `scripts/shared-references.json`. Edit the source first, then run `python3 scripts/shared-references.py sync`. Reference targets may use semantic aliases, but every path must be registered in the manifest.
- `shared-references.py check` also scans content hashes for unregistered exact copies across Skills. A directory mirror’s `files` must cover the complete source tree; newly added files cannot bypass the manifest.
- `check-reference-similarity.py` scans for near-duplicate copies across Skills. Historical derivatives that must continue evolving independently must register their members and reason for divergence under `derived_groups`. Every new copy must either be registered for synchronization or become genuinely independent content; renaming cannot bypass ownership.
- In `story-short-analyze`, the `analysis-short-*` files are source-observation criteria, not writing playbooks. Do not reintroduce long-form nodes, volume-level loops, recommended structural percentages, or “required in every chapter” commands. `check-short-analysis-scope.py` enforces this boundary.
- Before submitting, run `bash scripts/check-shared-files.sh`. A duplicate Runtime script name not registered in the manifest fails immediately.

### Knowledge-Base Contributions

The most valuable contribution types are:

- **Field data**: current platform chart analysis and changes in genre trends
- **New genre frameworks**: formulas and structural templates for new genres
- **AI-pattern removal rules**: new AI-trace patterns and rewrite examples
- **Platform-rule updates**: changes to submission requirements and recommendation systems

## Quality Requirements

- **Actionable**: content must be directly executable by an AI agent; do not write a tutorial
- **Concise**: use tables and templates instead of long narrative explanations
- **Self-contained**: Runtime Skills may not reference cross-Skill paths. When a reference truly must be shared, publish a local deployed copy managed by a canonical source plus manifest so every Skill remains independently installable
- **Chinese**: all content must be written in Chinese

## Submission Process

```
fork → branch → commit → PR → review → merge
```

- Keep each PR focused on one change.
- Write commit messages in Chinese using the format `类型: 简短描述`.
- Types: `feat` (new feature) / `fix` (bug fix) / `docs` (documentation) / `refactor` (refactoring).

## OpenCode Template Synchronization

This project supports Claude Code, Google Antigravity, OpenCode, Codex, ZCode, OpenClaw, and Reasonix (Phase 1). OpenCode agent and project-instruction templates are generated automatically from Claude Code templates by `scripts/sync-opencode.py`.

### When Synchronization Is Required

Run the synchronization script after modifying any of these files:

- `skills/story-setup/references/templates/agents/*.md` (agent definitions)
- `skills/story-setup/references/templates/CLAUDE.md.tmpl` (project-instruction template)

### Synchronization Steps

```bash
python3 scripts/sync-opencode.py
python3 scripts/sync-opencode.py --check  # 可选：只校验，不改文件
bash scripts/check-opencode-adapter.sh
bash scripts/test-opencode-cli-e2e.sh  # 可选：需要本机已安装 opencode
```

The script:

1. Converts Claude Code agents under `templates/agents/` to OpenCode format and writes them to `opencode/agents/`.
2. Copies `CLAUDE.md.tmpl` to `opencode/AGENTS.md.tmpl`, replacing `.claude/` path references.
3. Prints a synchronization summary.
4. Optionally uses a real CLI smoke test in a temporary project to verify that OpenCode can parse and load 13 slash commands, 7 agents, and the `story-hooks.ts` plugin.

### CI Detection

If a PR modifies Claude Code template files, CI automatically checks that the OpenCode templates were synchronized. It additionally verifies the structure of `opencode.json.patch`, the 13 commands, and the 7 agents, as well as the actual guard and completion behavior of `plugin.ts`. If CI fails, run the synchronization script and `bash scripts/check-opencode-adapter.sh` locally, then submit the result.

### Manually Maintained Components

The following files cannot be generated automatically and must be maintained by hand:

- `skills/story-setup/references/opencode/plugin.ts` — hook logic
- `skills/story-setup/references/opencode/commands/` — slash commands
- `skills/story-setup/references/opencode/opencode.json.patch` — configuration fragment

### Known sync-opencode.py Limitations

After running the synchronization script, perform these manual checks:

- **Path-resolution section**: `fix_path_rules_section()` now handles this automatically; no manual correction is needed.
- **Agent count**: confirm that `opencode/agents/` always contains 7 files.

### Key OpenCode Compatibility Issues

**Glob does not search hidden directories**: OpenCode’s Glob tool does not search `.opencode/`, leading to these design decisions:

- **agent-references** are deployed to `skills/story-setup/references/agent-references/` (not hidden), not `.opencode/skills/`.
- **agent files** are deployed twice: `.opencode/agents/` for OpenCode itself and `agents/` as a Glob-visible copy.
- **subagent detection**: every skill that spawns agents (story-review, story-long-write, story-deslop, story-import, story-long-analyze, and story-short-write) checks only the canonical directory for the active Runtime: Claude `.claude/agents/`, OpenCode `.opencode/agents/`, Codex `.codex/agents/`, or Antigravity `.agents/agents/`. It must not infer availability from another platform’s files. ZCode 3.3.4 and OpenClaw Phase 1 do not deploy project agents and use solo/direct fallback.

**Plugin output is not visible**: the OpenCode plugin’s `output.extra.system` has been removed because the real API has no such field. System-prompt injection now uses `experimental.session.compacting` and passes writing context through `output.context`.

**Session-start system-prompt injection is unsupported**: OpenCode’s public Plugin API has no `chat.message` or equivalent hook, so deployment-state detection and writing progress cannot be injected into model context at session start. The user may run `/story-setup` manually to view status.

**Other hook differences**: the `detect-gaps` plugin was not ported and does not inject a session-start prompt; only the compact summary and pre-prose outline guard remain. OpenCode has no equivalent `session-end` event, so it is currently unsupported. `validate-commit` uses a native Git `pre-commit` hook, which works with every CLI.

### OpenCode Usage Notes

- **Restart OpenCode after initial deployment**: slash commands deployed by story-setup under `.opencode/commands/` become available only after OpenCode restarts. Exit OpenCode and run `opencode -c` to re-enter.
- **Use a natural-language trigger for the initial deployment**: a new project has no slash commands, so trigger story-setup in natural language—for example, “please use the story-setup skill to deploy the web-fiction writing environment.”
- **OpenCode does not hot-reload configuration**: restart after changing `opencode.json`, agent files, or the plugin.
- **Long browser-cdp operations may hang**: OpenCode has no background-task mechanism. For long browser operations, the user must press `ESC` to interrupt; SKILL.md already includes timeout-wrapper guidance.

## OpenClaw Adapter Maintenance

OpenClaw currently uses a **Phase 1 skills-only** adapter:

- The canonical source remains the repository-root `skills/`; do not maintain a second skill copy for OpenClaw.
- Every `SKILL.md` frontmatter must meet OpenClaw/AgentSkills constraints: single-line `name`, single-line `description`, single-line JSON `metadata`, with `metadata.openclaw` present.
- `metadata.openclaw.requires.bins/env/config/anyBins` provides OpenClaw load-time gating. For example, `story-cover` controls visibility through `GPT_IMAGE_API_KEY`.
- `story-setup target_cli=openclaw` deploys only the project `skills/` and `references/openclaw/AGENTS.md.tmpl`; it does not deploy OpenClaw agents, hooks, or a plugin.
- OpenClaw snapshots eligible skills at session start. After a change, start a new session or wait for the skills watcher to refresh.

### OpenClaw Check Steps

```bash
bash scripts/check-openclaw-skills.sh
OPENCLAW_REAL_CHECK=1 bash scripts/check-openclaw-skills.sh  # 本机安装 openclaw 时可选
```

`OPENCLAW_REAL_CHECK=1` creates an isolated agent using a temporary profile and workspace, verifies that the OpenClaw CLI discovers 13 story skills under the workspace `skills/`, and removes the temporary profile afterward.

### Known OpenClaw Boundaries

- **Agents deferred**: OpenClaw’s agent/session model differs from Claude/Codex project agent files, so the adapter does not yet generate OpenClaw Gateway agents. Skills involving agent collaboration must fall back to solo/direct execution.
- **Hooks deferred**: pre-prose outline guards, commit reminders, and session-start/compact injection have not been migrated to an OpenClaw hook/plugin; under OpenClaw, they remain soft skill-process constraints only.
- **Package deferred**: OpenClaw recognizes workspace, personal, and managed skill roots; the project does not yet publish a native OpenClaw plugin package.

## Google Antigravity Adapter Maintenance

Antigravity 2.0 and the `agy` CLI share `.agents/` workspace customization, but separate smoke tests on real installations are still recommended before release. The full supported surface is deployed into the writing project by `story-setup`; the deployer does not write to `~/.gemini/`:

- Thirteen Skills are materialized as real directories at `.agents/skills/{name}/`. `deploy-antigravity-skills.py` replaces only known names and preserves user Skills. Existing symlinks fail closed by default; migrate them only with explicit user consent, and never follow them to write into their targets.
- Seven custom subagents are generated at deployment time from the canonical Claude Markdown source into `.agents/agents/agent-name/agent.md` (`agent-name` is replaced by the actual name). Tool names must come from the official list; invoke them with `invoke_subagent` plus the corresponding `TypeName`. The generator replaces only the seven known definitions and preserves other user agents.
- The Always-On Rule is fixed at `.agents/rules/oh-story.md` and must be under 12,000 characters. It handles skill routing and rereads `追踪/上下文.md` after compaction; do not assume Antigravity supports Claude’s PreCompact/PostCompact events.
- `.agents/hooks.json` is a top-level named-group mapping. The merger replaces only the `oh-story` group and preserves every user group. It currently registers `PreToolUse`, `PostToolUse`, `PreInvocation`, and `Stop`: PreToolUse must output `decision`; PostToolUse must output exactly `{}`. Post-write findings are stored in the current session’s `artifactDirectoryPath` and injected by the next PreInvocation. Stop may force continuation no more than once.
- Under `.agents/hooks/`, manage only `story_antigravity_hook.js` and the shared `story_hook_core.js`. The latter is locked for byte equality by `scripts/shared-assets.json`; do not edit copies manually. Hooks require Node on PATH.

Check steps:

```bash
bash scripts/check-antigravity-adapter.sh
python3 scripts/test-antigravity-skills-deploy.py
python3 scripts/test-antigravity-hook-merge.py
node scripts/test-antigravity-hooks.mjs
```

If current Antigravity 2.0 / `agy` is installed locally, run `story-setup` once more in a temporary writing project before release, begin a new conversation, and verify discovery with `/skills`, `/agents`, and `/hooks` in both the IDE and interactive CLI. The headless process for `agy 1.1.22 -p` scans the workspace before silent authentication and does not reload custom agents or hooks afterward. Testing reproduces `subagent not found` or ordinary model output being written into `~/.gemini/antigravity-cli/scratch/`, so it is not currently a supported entry point or smoke-test method. After testing, inspect and remove accidental scratch artifacts. Automation neither reads nor writes the user’s global customization and does not replace this real-installation test.

## ZCode Adapter Maintenance

ZCode uses two entry points: a native plugin plus `story-setup` workspace deployment.

- `.zcode-plugin/plugin.json` and the root `marketplace.json` expose the same 13 Skills, 13 Commands, and ZCode Hooks. Their versions must match `skills/story/VERSION`.
- `skills/story-setup/references/zcode/` is the workspace deployment template and contains `AGENTS.md.tmpl`, Commands, `config.json.patch`, and a dependency-free Node Hook runner.
- ZCode 3.3.4 supports only `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PostToolUseFailure`, and `Stop`. Do not copy Claude’s `PreCompact`, `PostCompact`, `SessionEnd`, `SubagentStop`, or `Notification` events.
- Empty Hook stdout means allow. Any nonempty output must satisfy the strict JSON schema. Write diagnostics only to stderr and fail open on exceptions. Prefer `process` plus `node`; do not introduce cross-platform shell/Python launcher branches.
- Version 3.3.4 does not execute project-level or plugin custom agents and does not discover `.zcode/rules`. Do not generate `.zcode/agents/` / `.zcode/rules/` or write to the user’s home directory by default. Skills involving specialized Agents must explicitly report a solo/direct fallback.

### ZCode Check Steps

```bash
bash scripts/check-zcode-adapter.sh
bash scripts/test-zcode-hooks.sh
bash scripts/test-prose-net-parity.sh
```

When changing the lightweight deterministic prose net, synchronize the Claude, OpenCode, Codex, Antigravity, and ZCode implementations and make the shared-assets, parity, and Antigravity hook tests pass.

## Reasonix Adapter Maintenance

Reasonix (DeepSeek-Reasonix CLI) currently supports skills, a native plugin manifest, and skills-only project deployment through `story-setup`; hooks and custom agents are deferred to a later phase. Skills involving specialized Agents use a solo/direct fallback:

- The root `reasonix-plugin.json` is the plugin manifest. Its `version` must match `skills/story/VERSION`, enforced by `check-reasonix-adapter.sh`.
- Reasonix natively scans project skill roots such as `.agents/skills`—a symlink to `skills/`, shared with Codex—and discovers all 13 skills.
- `story-setup` with `target_cli=reasonix` performs a skills-only deployment: it copies 13 skills into project `skills/` and writes `references/reasonix/AGENTS.md.tmpl`, without deploying hooks or agents. This mirrors OpenClaw / generic behavior and is guarded by `check-story-setup-deployment.sh`. Update that guard whenever the Reasonix deployment path or template changes.
- Real-CLI verification with `reasonix doctor capabilities` is outside CI and may be run manually before release.

### Reasonix Check Steps

```bash
bash scripts/check-reasonix-adapter.sh
```

## Codex Adapter Maintenance

This project also supports Codex CLI through repository skill discovery plus `$story-setup` project deployment:

- Repository-local skills: `.agents/skills` is a relative symlink to `skills/` (`../skills`, the agentskills.io standard path). Codex scans it to discover skills; do not create a second copy. It must remain a valid relative symlink (`check-codex-adapter.sh` enforces target=`../skills`; invalid or absolute links break discovery—see openai/codex#11314). Windows requires Git `core.symlinks=true`. OpenClaw scans workspace `skills/` directly and does not depend on this link.
- Project deployment hooks: `skills/story-setup/references/codex/hooks/hooks.json` is deployed by `$story-setup` into writing projects. Both POSIX `command` and Windows `commandWindows` search upward from the current directory for `.codex/hooks/run-story-hook.*` without depending on a Git repository. The shared launcher then performs event allowlisting, interpreter detection, `CODEX_PROJECT_DIR` injection, and Python hook dispatch.
- Windows hooks: on Windows, Codex uses `%COMSPEC% /C` (cmd.exe) to launch `commandWindows`. Registered commands use PowerShell to search upward, then invoke `run-story-hook.cmd`; nested working directories therefore behave like POSIX rather than supporting only the project root. After changing the event list or launcher, rerun the generator and adapter checks. Never duplicate discovery logic manually across the six registrations.
- Custom agents: `skills/story-setup/references/codex/agents/*.toml` is generated by `scripts/generate-codex-agents.py` from `references/templates/agents/*.md`. Regenerate and commit them after modifying Claude agent templates.

### Codex Synchronization Steps

```bash
python3 scripts/generate-codex-agents.py
python3 scripts/generate-codex-hooks.py
bash scripts/check-codex-adapter.sh
bash scripts/test-codex-hooks.sh
```

### Key Codex Compatibility Issues

- **Hook trust threshold**: a project’s `.codex/` configuration layer must be trusted, and non-managed command hooks also require user review/trust through `/hooks` before they run.
- **Hook JSON contract**: ordinary stdout from `PreToolUse`, `PreCompact`, and `PostCompact` is ignored. Output JSON such as `hookSpecificOutput.permissionDecision = "deny"` or `hookSpecificOutput.additionalContext`.
- **Incomplete PreToolUse interception**: official Codex documentation states that shell/edit interception is not a complete security boundary. Story hooks are writing-workflow guardrails, not substitutes for version control and human review.
- **Agent file format**: Codex custom agents are `.codex/agents/{name}.toml` files requiring `name`, `description`, and `developer_instructions`. Read-only agents use `sandbox_mode = "read-only"`.
- **Custom-agent Runtime registration**: after `$story-setup` writes `.codex/agents/*.toml`, trust the project `.codex/` configuration layer and begin a new Codex session. If the current Codex Runtime still returns `unknown agent_type`—reproducible in a temporary project smoke test using local `codex exec 0.141.0`—the skill must fall back to solo/direct execution and report that fallback. The automated hard gate covers TOML schema and deployed files.
