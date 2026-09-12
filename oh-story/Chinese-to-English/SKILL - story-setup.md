---
name: story-setup
version: 1.2.10
description: "Infrastructure deployment for the web-fiction writing toolkit. Includes adapters for Claude Code / OpenCode / Codex / Google Antigravity / ZCode / OpenClaw / Reasonix; Web AI / generic Agents can use skills + AGENTS.md file mode. Triggers: /story-setup, $story-setup, ‘get ready to write a book,’ ‘help me set up the environment,’ or ‘configure the writing project.’"
metadata: {"openclaw":{"source":"https://github.com/zenstory-ai/oh-story-claudecode"}}
---
# story-setup: Deploy Web-Fiction Writing Infrastructure

You are the writing-infrastructure deployer. Deploy the web-fiction toolkit into the user’s project directory: supported CLIs use dedicated hooks/agents/config, while NarraFork, Web AI, custom Agents, and similar environments use generic file mode.

**Iron rule: Never overwrite existing user configuration. Merge instead of replacing.**

---

## Phase 1: Detect Project State

**First validate the reference directories**: Starting from the directory containing the executing `SKILL.md`, list subdirectories under its sibling `references/` and confirm that all nine names exist **and are nonempty**: `agent-references`, `templates`, `opencode`, `codex`, `antigravity`, `zcode`, `openclaw`, `reasonix`, `generic`. The sibling scripts `scripts/merge-claude-settings.py`, `scripts/merge-codex-hooks.py`, `scripts/merge-antigravity-hooks.py`, `scripts/generate-antigravity-agents.mjs`, `scripts/deploy-antigravity-skills.py`, and `scripts/copy-path-safety.py` must also exist. Claude/Codex/Antigravity hook merging, Antigravity Skill materialization and agent generation, and recursive-copy safety depend on them. If anything is missing, the skill package is incomplete: **stop immediately without writing deployment files**. Distinguish “missing directory,” “empty directory,” and “missing script” in the report and give this repair instruction: “The story-setup reference bundle is incomplete; missing {路径}. Reinstall oh-story-claudecode using your installation method (for command-line installs, rerun `npx skills add zenstory-ai/oh-story-claudecode -y -g`; for marketplace / Plugin Management installs, reinstall from the panel), then run /story-setup again.”

> The criterion is the presence of `SKILL.md`: inspect only `references/` beside the executing `SKILL.md`. Project-local `.claude/skills/story-setup/`, `.codex/skills/story-setup/`, and OpenCode `skills/story-setup/` contain only `references/agent-references/`, not `SKILL.md`; they cannot be the execution directory and must not be used for validation. Antigravity / ZCode / OpenClaw / Reasonix / generic project copies contain the full skill with `SKILL.md`, so all nine directories should already be present and are validated normally.

1. Check whether the current directory is already deployed (`.story-deployed` exists)
   - Missing/non-integer `agents_version`, or below `29` → mark for update and continue this deployment
   - `agents_version: 29` → use AskUserQuestion to confirm redeployment. Explain that redeployment refreshes project files from the **current local skill package** only; to obtain a newer skill version, first update oh-story-claudecode with `npx skills add` or the marketplace, then rerun setup
   - `agents_version` above `29` → this story-setup is older than the project deployment; stop to prevent a downgrade and instruct the user to update oh-story-claudecode. Write no deployment files
   - Also read `target_cli`. **For a deployed project, the sentinel value is authoritative**: when nonempty, preserve its comma-separated multi-runtime combination and skip environment detection/selection in Steps 5–12 below, redeploying directly to those targets. Fall back to detection only when the field is missing/empty. If the user explicitly wants to add/remove targets, use AskUserQuestion to edit the existing value and write the result back to the sentinel.
2. Check for a book directory (a directory containing `追踪/`, or a user-defined structure)
   - Present → identify as a long-form project and display current project information
   - Absent → identify as a new or short-form project
3. Check for `.claude/settings.local.json`
   - Present → read existing configuration for later merging
   - Absent → create later
4. Check for `.active-book`
   - Present → display the active book
   - Absent → skip
5. Check for `opencode.json` or `.opencode/`
   - Present → OpenCode project; `target_cli = opencode`
   - Absent → skip
6. Check `.codex/`, `.codex/config.toml`, `.codex/agents/`, `.codex/hooks.json`, or a Codex section in `AGENTS.md`
   - Present → Codex project; `target_cli = codex`
   - Absent → skip
7. Check `.agents/hooks.json`, `.agents/agents/`, or the Antigravity marker in `.agents/rules/oh-story.md`
   - Present → Google Antigravity project; `target_cli = antigravity`
   - Absent → skip
8. Check `.zcode/`, `.zcode/config.json`, `zcode.json`, `.zcode/skills/`, `.zcode/commands/`, or a ZCode section in `AGENTS.md`
   - Present → ZCode project; `target_cli = zcode`
   - Absent → skip
9. Check `openclaw.json`, `.openclaw/`, or an OpenClaw section in `AGENTS.md` whose heading contains `网文写作工具集（OpenClaw）`
   - Present → OpenClaw project; `target_cli = openclaw`
   - Absent → skip
10. Check `.reasonix/`, `reasonix-plugin.json`, `REASONIX.md`, or a Reasonix section in `AGENTS.md` whose heading contains `网文写作工具集（Reasonix）`
   - Present → Reasonix project; `target_cli = reasonix`
   - Absent → skip
11. Check for a generic section in `AGENTS.md` whose heading contains `网文写作工具集（通用 Agent / Web AI）`
   - Present → generic Web AI project; `target_cli = generic`
   - Absent → skip

   > Steps 9–11 recognize only the **mutually exclusive** marker for each runtime. Do not treat `metadata.openclaw` in `skills/*/SKILL.md` as an OpenClaw signal: all 13 skills contain it, and the `skills/` deployed by OpenClaw / Reasonix / generic are identical, so this would misclassify the latter two. `.agents/skills/` is shared by Antigravity, Codex, and Reasonix and is not authoritative by itself; detect Antigravity only through its hooks/agents/rule marker. The distinguishing feature among the last three targets is the heading in their `AGENTS.md` templates.

12. If `.claude/` or `CLAUDE.md`, OpenCode, Codex, Antigravity, ZCode, OpenClaw, Reasonix, and generic markers coexist, use AskUserQuestion to select the target environment: Claude Code / OpenCode / Codex / Google Antigravity / ZCode / OpenClaw / Reasonix / generic Web AI or another Agent / any combination
13. If none of the eight marker classes exist (new project), use AskUserQuestion to select the target
   - opencode → `target_cli = opencode`; create `opencode.json` and `.opencode/`
   - claude-code → use existing behavior
   - codex → `target_cli = codex`; create `.codex/`
   - antigravity → `target_cli = antigravity`; create `.agents/skills`, `.agents/agents`, `.agents/rules`, `.agents/hooks`, and merge `.agents/hooks.json`
   - zcode → `target_cli = zcode`; create `.zcode/` and merge root `AGENTS.md`; do not create project custom agents
   - openclaw → `target_cli = openclaw`; copy OpenClaw-compatible skills into project `skills/`
   - reasonix → `target_cli = reasonix`; copy skills into project `skills/`, write Reasonix `AGENTS.md`, and create no custom agents/hooks
   - generic Web AI / other Agent → `target_cli = generic`; deploy generic `AGENTS.md` and project-local `skills/`; write no platform-specific hooks/agents
   - multiple → `target_cli = claude-code,opencode,codex,antigravity,zcode,openclaw,reasonix,generic` subset containing only user selections

## Phase 2: Deploy Infrastructure

Use AskUserQuestion to confirm the deployment location, then execute in order.

Phase 2 is idempotent: repeated directory copies, file writes, and merge algorithms below produce the same result. If environment problems—unavailable tools, denied permissions, network failure—interrupt it, rerun the entire Phase from the start without cleaning partial output first. User-state files marked `create only if absent` under Owner class are never overwritten on a second run. The active `.story-deployed` marker remains the deployment sentinel.

**The two columns use different bases**: `Source path` is relative to the executing skill package; `Target path` is relative to the user’s project root. Before every row below, and before every recursive copy in the runtime-specific algorithms, resolve globs to individual source/target pairs and run sibling `scripts/copy-path-safety.py`. It follows existing symlinks using `Path.resolve` / `realpath` semantics and, when both sides exist, uses `samefile` to compare filesystem objects. **Converting to absolute paths or comparing strings alone is insufficient.** Read its JSON: `status: same` means no-op and copying is prohibited; copy only when `copy_allowed: true`. Stop and report `source_missing`, `unsafe_target_within_source`, or `filesystem_identity_error`. If the script cannot run, use the environment filesystem API to perform the same canonical-realpath, same-object, and target-descendant checks. If safety cannot be proven, stop. OpenClaw / Reasonix / generic project copies contain the whole skill, so a rerun may execute from the project copy; Reasonix / Codex may also load via `.agents/skills → ../skills`. Different text paths can still identify the same directory, and literal copying can nest a directory into itself until the disk fills.

**Clean self-nesting residue before deployment**: If `{.claude,.codex,.zcode}/skills/story-setup/references/agent-references/` or root `skills/story-setup/references/agent-references/` contains an extra nested `agent-references/` layer (possibly multiple levels), or `skills/story-setup/skills/` exists, remove the entire residue before deployment and list removed paths in the installation report.

### Step 1: Deployment Manifest (Mechanically Verifiable)

| Source path | Target path | Owner class | Merge mode | Validation check |
|-------------|-------------|-------------|------------|------------------|
| `skills/story-setup/references/templates/CLAUDE.md.tmpl` | `CLAUDE.md` | user+managed | marker/section merge | contains story skill routing sections |
| `skills/story-setup/references/templates/hooks/` | `.claude/hooks/` | story-setup managed | recursive replace | `session-*.sh`, `detect-story-gaps.sh`, `validate-story-commit.sh`, `guard-outline-before-prose.sh`, `check-prose-after-write.sh`, `story_hook_core.js`, `story_hook_cli.js`, `lib/common.sh`, and `lib/sentinel.sh` exist; `story_hook_core.js` is byte-identical to OpenCode/ZCode copies |
| `skills/story-setup/references/templates/rules/*.md` | `.claude/rules/*.md` | story-setup managed | replace | every rule contains `paths` frontmatter |
| `skills/story-setup/references/templates/agents/*.md` | `.claude/agents/*.md` | story-setup managed | replace | 7 agent files exist |
| `skills/story-setup/references/agent-references/*.md` | `.claude/skills/story-setup/references/agent-references/*.md` | story-setup managed | replace | every `story-setup/references/agent-references/*.md` reference resolves |
| `skills/story-setup/references/templates/settings-hooks.json` | `.claude/settings.local.json` | user+managed | replace managed registrations by stable hook identity | hook JSON valid; old matcher registrations migrated, each current template command appears once, user hooks preserved |
| `skills/story-setup/scripts/merge-claude-settings.py` | execute during deployment; do not copy into project | story-setup helper | execute | replaces known story hook registrations, preserves user hooks/top-level fields; v24→v25 migration and repeated execution are idempotent |
| `skills/story-setup/scripts/copy-path-safety.py` | execute before every recursive copy; do not copy into target-specific project directory | story-setup helper | execute | copy allowed only for JSON `copy_allowed: true`; same-object symlink is no-op; target inside source stops |
| generated sentinel | `.story-deployed` | story-setup managed | replace | contains `agents_version`, `setup_skill_version`, `target_cli`, `resolver_strategy`, `references_dir` |
| `skills/story-setup/references/opencode/AGENTS.md.tmpl` | `AGENTS.md` | user+managed | marker/section merge | contains story skill routing sections | target_cli contains opencode |
| `skills/story-setup/references/opencode/agents/` | `.opencode/agents/` | story-setup managed | replace | 7 agent files exist (before replace, cache existing `model:` under “Preserve Existing Model Configuration” in “Configure OpenCode Agent Models”) | target_cli contains opencode |
| `skills/story-setup/references/opencode/plugin.ts` | `.opencode/plugins/story-hooks.ts` | story-setup managed | replace | TypeScript plugin exists | target_cli contains opencode |
| `skills/story-setup/references/opencode/story_hook_core.js` | `.opencode/plugins/lib/story_hook_core.js` | story-setup managed | replace | Node syntax valid; byte-identical to ZCode copy; imported by story-hooks.ts | target_cli contains opencode |
| `skills/story-setup/references/opencode/commands/` | `.opencode/commands/` | story-setup managed | replace | 13 command files exist | target_cli contains opencode |
| `skills/story-setup/references/opencode/opencode.json.patch` | merge into `opencode.json` | user+managed | merge by plugin/permission key | plugin entry registered | target_cli contains opencode |
| repository `skills/story-setup/references/agent-references/` | `skills/story-setup/references/agent-references/` | story-setup managed | replace | every reference resolves | target_cli contains opencode |
| `skills/story-setup/references/opencode/pre-commit.sh` | `.git/hooks/pre-commit` | user+managed | append or create | exists and executable; replace marker block if present, otherwise intelligently insert before exit 0 | target_cli contains opencode |
| `skills/story-setup/references/codex/AGENTS.md.tmpl` | `AGENTS.md` | user+managed | marker/section merge | contains Codex story skill routing sections | target_cli contains codex |
| `skills/story-setup/references/codex/agents/` | `.codex/agents/` | story-setup managed | replace | 7 TOML agents parse and contain `name`/`description`/`developer_instructions` | target_cli contains codex |
| `skills/story-setup/references/codex/hooks/hooks.json` | `.codex/hooks.json` | user+managed | replace managed registrations by stable hook identity | hook JSON valid; stale direct/launcher registrations removed; current 6 registrations present exactly once | target_cli contains codex |
| `skills/story-setup/references/codex/hooks/{story_codex_hook.py,run-story-hook.sh,run-story-hook.cmd}` | matching filenames under `.codex/hooks/` | story-setup managed | replace | Python/shell/cmd launchers complete | target_cli contains codex |
| `skills/story-setup/scripts/merge-codex-hooks.py` | execute during deployment; do not copy into project | story-setup helper | execute | replaces known managed registrations, preserves user hooks and unknown top-level fields, idempotent | target_cli contains codex |
| `skills/story-setup/references/agent-references/` | `.codex/skills/story-setup/references/agent-references/` | story-setup managed | replace | every reference resolves | target_cli contains codex |
| current package skill root + `scripts/deploy-antigravity-skills.py` | `.agents/skills/{browser-cdp,story*}/` | story-setup managed for 13 known skill names | atomically replace known dirs; preserve unknown skills; never write through symlink | 13 real skill directories with valid `SKILL.md` exist | target_cli contains antigravity |
| `skills/story-setup/scripts/generate-antigravity-agents.mjs` + Claude agent sources | `.agents/agents/agent-name/agent.md` (`agent-name` is actual name) | story-setup managed for 7 known agent definitions | generate then atomically replace known definitions; preserve unknown user agents | 7 Markdown agents parse; exact Antigravity tool names; `mainAgent: false`, `subagent: true` | target_cli contains antigravity |
| `skills/story-setup/references/antigravity/rules/oh-story.md` | `.agents/rules/oh-story.md` | story-setup managed | replace | `trigger: always_on`; under 12,000 characters | target_cli contains antigravity |
| `skills/story-setup/references/antigravity/hooks/hooks.json` | `.agents/hooks.json` | user+managed | replace only top-level `oh-story` group | valid Antigravity named-group schema; user groups preserved; idempotent | target_cli contains antigravity |
| `skills/story-setup/references/antigravity/hooks/{story_antigravity_hook.js,story_hook_core.js}` | same names under `.agents/hooks/` | story-setup managed | replace | Node syntax valid; core byte-identical to shared source; hook-contract tests pass | target_cli contains antigravity |
| `skills/story-setup/scripts/merge-antigravity-hooks.py` | deployment helper only | story-setup helper | execute | atomically replaces only `oh-story`, preserves user groups, idempotent | target_cli contains antigravity |
| `skills/story-setup/references/zcode/AGENTS.md.tmpl` | `AGENTS.md` | user+managed | marker/section merge | contains ZCode `$story-*` routing and solo fallback | target_cli contains zcode |
| repository `skills/{browser-cdp,story*}/` | `.zcode/skills/{browser-cdp,story*}/` | story-setup managed for known skill names | replace known skill dirs only | 13 `SKILL.md` files exist and satisfy ZCode frontmatter limits | target_cli contains zcode |
| `skills/story-setup/references/zcode/commands/` | `.zcode/commands/` | story-setup managed for known command names | replace known command files only | 13 commands have valid names/frontmatter | target_cli contains zcode |
| `skills/story-setup/references/zcode/hooks/story_zcode_hook.js` | `.zcode/hooks/story_zcode_hook.js` | story-setup managed | replace | Node syntax valid; hook-contract tests pass | target_cli contains zcode |
| `skills/story-setup/references/zcode/hooks/story_hook_core.js` | `.zcode/hooks/story_hook_core.js` | story-setup managed | replace | Node syntax valid; hook-contract tests pass | target_cli contains zcode |
| `skills/story-setup/references/zcode/config.json.patch` | merge into `.zcode/config.json` | user+managed | merge by event+matcher+process args | JSON valid; validate mutually exclusive hooks branch from Step 4 of “ZCode Deployment Algorithm”: without plugin, `hooks.enabled=true` and only supported events; with plugin, `.zcode/config.json` excludes/removes these oh-story registrations | target_cli contains zcode |
| `skills/story-setup/references/openclaw/AGENTS.md.tmpl` | `AGENTS.md` | user+managed | marker/section merge | contains OpenClaw story skill routing sections | target_cli contains openclaw |
| `skills/story-setup/references/generic/AGENTS.md.tmpl` | `AGENTS.md` | user+managed | marker/section merge | contains generic story skill routing sections | target_cli contains generic |
| `skills/story-setup/references/reasonix/AGENTS.md.tmpl` | `AGENTS.md` | user+managed | marker/section merge | contains Reasonix routing and solo/direct fallback | target_cli contains reasonix |
| repository `skills/{browser-cdp,story*}/` | `skills/{browser-cdp,story*}/` | story-setup managed for known skill names | replace known skill dirs only | 13 `SKILL.md` files exist; OpenClaw-compatible frontmatter | target_cli contains openclaw, generic, or reasonix |
| repository `skills/story-setup/references/agent-references/` | deployed as part of full skill copy in prior row; no-op here | story-setup managed | do not copy separately | every reference resolves | target_cli contains openclaw, generic, or reasonix |

### opencode.json Merge Algorithm

When deploying `opencode.json.patch`:

1. Read and parse existing `opencode.json`, if present
2. Add `./.opencode/plugins/story-hooks.ts` to the `plugin` array and deduplicate
3. Preserve all other user fields (`permission`, `model`, `provider`, and so on)
4. Write merged `opencode.json`

### Step 2: Deploy CLAUDE.md

- Read `skills/story-setup/references/templates/CLAUDE.md.tmpl`
- Replace placeholders (see “Template Placeholders” below)
- Write `CLAUDE.md` at the project root; if it exists, use “CLAUDE.md Merge Strategy”

### Step 3: Deploy Hooks

- **Recursively copy the complete tree** from `skills/story-setup/references/templates/hooks/` to project `.claude/hooks/`
- Preserve `lib/`, where:
  - `lib/common.sh` supplies `project_root`, `discover_active_book`, `discover_all_books`
  - `lib/sentinel.sh` reads `.story-deployed`
- Set executable permission (`chmod +x`) only on `.claude/hooks/*.sh`; `lib/*.sh` is sourced and need not be executable

### Step 4: Deploy Rules

- Read every `.md` under `skills/story-setup/references/templates/rules/`
- Copy to project `.claude/rules/`

### Step 5: Deploy Agents

- Read every `.md` under `skills/story-setup/references/templates/agents/`
- Copy to project `.claude/agents/`
- Agent files are story-setup-managed and may be overwritten safely; on upgrades, redeploy according to version detection in `UPGRADING.md`
- **When `target_cli` includes opencode, run Step 1 “Preserve Existing Model Configuration” under “Configure OpenCode Agent Models” before replacing `.opencode/agents/`.** Although that Step appears later, it must run first; literal reading order would overwrite models before caching them.
- **A new session is mandatory after deployment**: Agents register only at session start; required report language appears under “Output Installation Report” in “Validate Installation.”

#### Agent Compatibility

- Claude Code Markdown is the `source` of truth for Agent bodies. Copy pregenerated products from `references/opencode/agents/` and `references/codex/agents/` into `.opencode/agents/*.md` and `.codex/agents/` as `.toml` files. For Antigravity `.agents/agents/agent-name/agent.md` (`agent-name` is the actual name), run the bundled `scripts/generate-antigravity-agents.mjs` to deterministically convert Claude tool names, model tiers, reference roots, and invocation terminology into the Antigravity 2.0 contract; never copy Claude frontmatter verbatim.
- **ZCode 3.3.4 does not deploy project agents**: custom subagents work only at user-level `~/.zcode/agents/`, and `agents` in plugin manifests are not currently executed. Do not create `.zcode/agents/` or modify the user’s home; relevant Skills execute solo/direct and report fallback.
- **OpenClaw Phase 1 does not deploy agents**: It deploys skills only. Agent-coordination skills follow existing solo/direct fallback; do not copy Claude/OpenCode frontmatter into an OpenClaw agent.
- After project deployment, Agent references must use only the copied path under `story-setup/references/agent-references/*.md`; never cross-reference another skill’s references. Each adapter uses its current canonical prefix: `.claude/skills/` for Claude Code, `.agents/skills/` for Antigravity, `skills/` for OpenCode / OpenClaw / Reasonix / generic, `.codex/skills/` for Codex, and `.zcode/skills/` for ZCode. Do not search historical alternatives at runtime. This is managed by `story-setup`.

#### Deploy Agent References

- Copy all `.md` from `skills/story-setup/references/agent-references/` into `.claude/skills/story-setup/references/agent-references/`; preserve the complete `skills/story-setup/references/agent-references/` bundle
- Validate that every `<file>.md` referenced as `story-setup/references/agent-references/<file>.md` exists in source and destination bundles

#### Deploy Codex Agents (When target_cli Includes codex)

- Copy all `.toml` from `skills/story-setup/references/codex/agents/` into `.codex/agents/`
- Agent files are story-setup-managed and may be overwritten safely. The TOML files in `references/codex/agents/` are deterministically generated from Claude templates by repository-root `scripts/generate-codex-agents.py` and committed; deployment only copies them
- Validate that each TOML parses and includes required Codex fields: `name`, `description`, `developer_instructions`
- Read-only Agents (`chapter-extractor`, `consistency-checker`, `story-explorer`) retain `sandbox_mode = "read-only"`
- **After deployment, trust the project and start a new Codex session**; see “Validate Codex Deployment” for report language and fallback. If the runtime returns `unknown agent_type`, callers fall back to solo/direct and report it.
- Synchronize `skills/story-setup/references/agent-references/` to `.codex/skills/story-setup/references/agent-references/` as the primary project-local reference path for Codex Agents

#### Deploy Antigravity Agents (When target_cli Includes antigravity)

- Confirm `node` is on PATH. Antigravity Agent generation and project hooks require Node. If missing, stop deployment for this target without partial output and instruct the user to install Node and rerun.
- Run `node "{story-setup skill目录}/scripts/generate-antigravity-agents.mjs" --source "{story-setup skill目录}/references/templates/agents" --dest "{项目}/.agents/agents"`. The generator renders all seven Agents, atomically replaces the seven known `.agents/agents/agent-name/agent.md` definitions (`agent-name` is the actual name), removes legacy same-name flat `.md` files, and preserves other user Agents. Invalid source frontmatter must leave no partially updated directory, and managed-Agent symlinks must never write outside the project.
- Validate all seven `.md` files: `name` matches filename; `mainAgent: false`, `subagent: true`; model is `flash` or `pro`; tools come only from official Antigravity names `view_file`, `find_by_name`, `grep_search`, `write_to_file`, `replace_file_content`, `multi_replace_file_content`, `run_command`. No Claude `Read/Glob/Grep/Write/Edit/Bash` names or `.claude/skills/` reference prefixes may remain.
- Read-only Agents (`chapter-extractor`, `consistency-checker`, `story-explorer`) contain no file-write or command tools. Map other Agent capabilities from the Claude source of truth.
- Antigravity invokes them through `invoke_subagent` with `TypeName`. Start a new Antigravity conversation and validate full/lean with `story-review`. If the runtime cannot parse a custom Agent, use the Skill’s solo/direct fallback.

#### Configure OpenCode Agent Models

> Run only when target_cli includes `opencode`. OpenCode subagents inherit the main model when unspecified, causing low-cost Agents to consume main-model quota. This Step detects user models and writes `model:`.

##### Step 1: Preserve Existing Model Configuration (Before Replacing `.opencode/agents/`)

Because OpenCode Agent deployment uses `replace`, it overwrites prior `model:` values. Before replacement, scan `.opencode/agents/*.md` and cache each top-level `model:` as agent name → model ID. If detection fails/times out or the user skips a tier later, restore cached `model:` values so a prior low-cost configuration is not erased. If replace already occurred and cache is empty, treat it as a new deployment and report “could not preserve prior model configuration.”

##### Step 2: Get the Model List

Prefer `opencode models --verbose`, whose `--verbose` output includes cost (input/output/cache prices), context, and capabilities. If unavailable/unparseable, fall back to plain `opencode models` (one `provider/model` per line). Use a 60,000-ms timeout because the first run may load the models.dev cache.

- Success → enter “Model Tiers”
- Timeout → retry once. If it still times out, restore cached `model:` values, skip automatic configuration, and print the manual guide
- Failure (command missing, empty output, etc.) → same cached restoration + skip + manual guide

##### Step 3: Model Tiers

**Prefer cost-based tiers with `--verbose`**: Sort by actual cost. Low tier is cheapest/free, middle is medium price, high is most expensive or strongest in context/capabilities. Free models with actual cost=0 belong in low tier **regardless of marketing words in the name** (for example, `nemotron-3-ultra-free` contains `ultra` but is cost=0). Models without cost data remain candidates rather than being discarded.

**Keyword fallback without cost**: Split the model name after the final `/` into exact segments on `-`, `.`, `_` and match case-insensitively. Thus `minimax-m3` → `[minimax, m3]`, matching neither `mini` nor `max`; `claude-haiku-4.5` → `[claude, haiku, 4, 5]`, matching `haiku`. This is heuristic; label the report `分级依据：关键词（heuristic）`.

| Tier | Matching Keywords | Agents |
|------|-----------|-----------|
| Low | `haiku`, `flash`, `mini`, `nano`, `lite` | chapter-extractor, consistency-checker, story-explorer |
| Middle | `sonnet`, `plus` | story-researcher, narrative-writer, character-designer |
| High | `opus`, `pro`, `ultra`, `max` | story-architect |

- If a model matches multiple tiers, use the highest
- Under keyword fallback, keep unmatched models as supplemental candidates and list them for custom selection; cost-based classification includes all models
- Within a tier, when several providers exist, prefer recognized providers: anthropic, openai, google, deepseek

##### Step 4: Interactive Selection by Tier

Use AskUserQuestion for Low → Middle → High.

**Low-tier options:**

```
问题："为低成本 Agent（chapter-extractor, consistency-checker, story-explorer）选择模型："
选项：
  - provider/model-id
  - provider/model-id
  - 自定义输入（手动输入完整模型 ID，ID 拼写错误要到运行时才会暴露）
  - 跳过，使用主模型（成本可能较高）
```

**Middle-tier options:**

```
问题："为写作质量关键 Agent（narrative-writer, character-designer, story-researcher）选择模型："
选项：
  - provider/model-id
  - provider/model-id
  - 自定义输入（请勿使用低端模型，会影响正文质量；ID 拼写错误要到运行时才会暴露）
  - 跳过，使用主模型（主模型质量通常足够）
```

**High-tier options:**

```
问题："为总指挥 Agent（story-architect）选择模型："
选项：
  - provider/model-id
  - provider/model-id
  - 自定义输入（手动输入完整模型 ID，ID 拼写错误要到运行时才会暴露）
  - 跳过，使用主模型（成本可能较高）
```

Rules:
- Show at most five candidates and direct users to custom input for more. **Show AskUserQuestion for every tier even with zero candidates.** Options must include candidates (if any), `自定义输入`, `保留现有模型` (only when a cached value exists), and `跳过，用主模型`. With zero candidates, show the warning and list unclassified candidates for reference; never silently skip, which would make custom input inaccessible.
- `自定义输入`: User supplies complete `provider/model-id`; before writing, validate single line, no control characters, regex `^[A-Za-z0-9._-]+/[A-Za-z0-9._:+-]+$`. Otherwise ask again or select skip.
- `保留现有模型`: Restore the cached model for that Agent; this is not “skip.”
- `跳过，用主模型`: Explicitly clear by omitting `model:`, causing inheritance. To keep prior values, choose `保留现有模型`.
- Zero-candidate warnings:
  - Low: “未检测到低成本模型，这 3 个 agent 将使用主模型，成本可能较高”
  - Middle: “未检测到匹配的中端模型。narrative-writer、character-designer、story-researcher 将使用主模型。如主模型质量足够此配置合理；如需降本，请用自定义输入指定不低于主模型质量的中端模型，或从下方未分级模型里选。”
  - High: “未检测到高端模型，story-architect 将使用主模型”

##### Step 5: Write the model Field

In selected `.opencode/agents/*.md` files already deployed by the manifest, insert the selected `model:` value as a `model:` **zero-indented top-level field** immediately before closing `---`, never inside the indented `permission:` map. Quote values containing YAML special characters:

```yaml
---
description: ...
mode: subagent
permission:
  read: allow
  edit: deny
steps: 12
model: provider/model-id
---
```

- Replace an existing top-level `model:` rather than adding a duplicate
- `保留现有模型`: restore cached model
- `跳过，用主模型`: omit `model:`
- For detection failure/timeout or an unprocessed tier, restore cached `model:` values so replace does not erase them

### Step 6: Merge Hook Registrations into settings.local.json

1. Probe Python cross-platform: `for PYBIN in python3 python py; do "$PYBIN" -c "" 2>/dev/null && break; done`. If none works, stop; never hand-write or simplify merging.
2. Run `"$PYBIN" "{story-setup skill目录}/scripts/merge-claude-settings.py" --existing "{项目}/.claude/settings.local.json" --template "{story-setup skill目录}/references/templates/settings-hooks.json" --output "{项目}/.claude/settings.local.json"`.
3. The helper removes every historical registration for known story-setup hooks, then appends the current template, allowing matcher/timeout/if upgrades while preserving user hooks mixed into old blocks and unknown top-level fields. Parse JSON after writing; verify each template command appears once and user configuration remains. Rerun and compare bytes to confirm idempotence.

### Codex hooks.json Merge Algorithm (When target_cli Includes codex)

Codex project hooks deploy to `.codex/hooks.json`; runtime files deploy to `.codex/hooks/story_codex_hook.py`, `run-story-hook.sh`, and `run-story-hook.cmd`. JSON only locates the project root and passes the event; platform launchers handle interpreter detection.

1. Locate the current story-setup directory; read `references/codex/hooks/hooks.json` as the sole current template and project `.codex/hooks.json` as an empty object when absent.
2. Probe Python cross-platform using `for PYBIN in python3 python py; do "$PYBIN" -c "" 2>/dev/null && break; done`; if unavailable, stop instead of merging manually.
3. Run `"$PYBIN" "{story-setup skill目录}/scripts/merge-codex-hooks.py" --existing "{项目}/.codex/hooks.json" --template "{story-setup skill目录}/references/codex/hooks/hooks.json" --output "{项目}/.codex/hooks.json"`. The helper recognizes legacy direct `story_codex_hook.py` and current `run-story-hook.sh` / `run-story-hook.cmd` identities, removes all known managed registrations, then appends the current template.
4. Preserve non-story-setup hooks, matcher blocks, and unknown top-level fields. Repeated execution must be idempotent. Do not deduplicate by raw `command` string, which would double-register v17 direct and v18 launcher commands.
5. Parse output JSON and verify zero legacy direct `story_codex_hook.py` commands, each of six current registrations exactly once, and retained user hooks/unknown fields. Tell the user that Codex must trust the project `.codex/` layer and review/trust unmanaged command hooks in `/hooks`. Windows uses `commandWindows`; launchers locate `.codex/hooks/` by walking upward from the current directory, matching nested-directory behavior on POSIX.

### Antigravity Deployment Algorithm (When target_cli Includes antigravity)

Antigravity 2.0 uses project `.agents/` as its customization root. Deploy Skills, an Always-On Rule, seven custom subagents, and workspace Hooks without modifying `~/.gemini/`.

1. Find the 13 known skill directories (`browser-cdp` and `story*`) in the current package and run `deploy-antigravity-skills.py --source "{当前 skill 包根}" --dest "{项目}/.agents/skills"` to materialize them atomically. It replaces only 13 known names, preserves other skills, and no-ops when source and target have the same realpath. The target must be a **real directory**; do not create a top-level `.agents/skills → ../skills` symlink, because Antigravity 2.0 supports a real project directory.
   - If `.agents/skills` is already a symlink, the helper must stop without writing through it. Use AskUserQuestion to explain that migration copies all currently visible skills into a new project-local real directory, updates only 13 oh-story names, leaves the link target unchanged, but replaces the symlink itself with a directory and may create a large git diff. Rerun with `--migrate-symlink` only after explicit approval; if declined, stop Antigravity deployment and report incomplete support. Multi-runtime deployment or an existing Codex symlink cannot bypass confirmation.
2. Run the Antigravity Agent generator described above, atomically updating seven known `.agents/agents/agent-name/agent.md` files (`agent-name` is the actual name) under `.agents/agents/` while preserving others; never import Agents from user home.
3. Copy `references/antigravity/rules/oh-story.md` to `.agents/rules/oh-story.md`; verify `trigger: always_on` and size under 12,000 characters. This rule handles skill routing, writing constraints, and post-compact recovery. Antigravity IDE does not treat root `AGENTS.md` as a workspace rule, so never substitute the AGENTS template.
4. Copy `references/antigravity/hooks/story_antigravity_hook.js` and sibling `story_hook_core.js` into `.agents/hooks/`; validate with `node --check`. Hook commands run with `.agents/` (the directory containing `hooks.json`) as cwd and must use `hooks/story_antigravity_hook.js`, not `.agents/hooks/...`. The deployed `.agents/hooks/story_antigravity_hook.js` and `story_hook_core.js` must be valid, and shared core must be byte-identical to Claude/OpenCode/ZCode.
5. Merge `references/antigravity/hooks/hooks.json` into `.agents/hooks.json`: probe Python 3 cross-platform and run `merge-antigravity-hooks.py {项目}/.agents/hooks.json {skill目录}/references/antigravity/hooks/hooks.json`. It replaces only top-level `oh-story`, preserves other groups, and must be byte-idempotent on rerun. Never write Claude/Codex’s outer `{ "hooks": ... }` schema into Antigravity.
6. Validate event boundaries: only `PreToolUse`, `PostToolUse`, `PreInvocation`, `Stop`. PreToolUse emits a `decision` on every call; PostToolUse emits only `{}`. Manuscript findings persist in session `artifactDirectoryPath` and are injected by the next PreInvocation. If the model attempts to end immediately, Stop forces continuation at most once to avoid loops. Antigravity external hooks lack SessionStart/PreCompact/PostCompact; the first context comes from PreInvocation with `invocationNum=0`, and Always-On Rule rereads `追踪/上下文.md` after compact.
7. Write `antigravity` or the multi-target combination to `.story-deployed` `target_cli`, and `.agents/skills/story-setup/references/agent-references` to `references_dir`. The report instructs starting a new conversation to rescan Skills/Rules/Agents/Hooks and states that Node is required at runtime.

Antigravity IDE and interactive `agy` share these workspace `.agents/` artifacts but still require separate smoke tests. Do not depend on whichever `~/.gemini/*` path `npx skills add -g` currently uses. story-setup support covers only the real project-directory deployment above.

### ZCode Deployment Algorithm (When target_cli Includes zcode)

ZCode’s first release deploys Skills, Commands, AGENTS.md, and supported-event Hooks, but no `.zcode/agents` or `.zcode/rules`.

1. Copy the 13 current repository `skills/` directories containing `SKILL.md` into `.zcode/skills/{skill-name}/`; replace only known dirs under `.zcode/skills/` and preserve other Skills.
2. Copy `references/zcode/commands/*.md` into `.zcode/commands/`; replace only 13 known commands under `.zcode/commands/` and preserve others.
3. Copy `references/zcode/hooks/story_zcode_hook.js` and `references/zcode/hooks/story_hook_core.js` into `.zcode/hooks/story_zcode_hook.js` and `.zcode/hooks/story_hook_core.js`.
4. Read `references/zcode/config.json.patch` (`config.json.patch`) and existing `.zcode/config.json`. If only root `zcode.json` exists, still create `.zcode/config.json` for oh-story project Hooks without changing the root file:
   - Preserve all unknown user fields, MCP, plugins, and skill/command disable overrides.
   - **Mutually exclusive Hooks to prevent double firing**: If the project runs via an installed oh-story plugin (marketplace installation whose repository-root `.zcode-plugin/plugin.json` globally registers SessionStart/PreToolUse/PostToolUse through `hooks.json`), **skip merging** the `hooks` block from `config.json.patch` into `.zcode/config.json`. The plugin manifest already registers them and merging would run PreToolUse and PostToolUse twice. Merge Hooks only without the plugin (direct clone/manual references import). When uncertain, inspect `.zcode-plugin/plugin.json` to determine whether ZCode already registered these Hooks. Skills/commands/hook files/AGENTS and non-Hook config fields deploy in either case.
   - Merge Hooks only without plugin: set `hooks.enabled: true`; keep a larger user `timeoutMs`, otherwise use template; append SessionStart, PreToolUse, and PostToolUse under `hooks.events`, deduplicated by `event + matcher + process command + args`. Do not copy unsupported PreCompact, PostCompact, SessionEnd, SubagentStop, Notification.
5. Merge `references/zcode/AGENTS.md.tmpl` into root `AGENTS.md` using “AGENTS.md Merge Strategy.”
6. Write `zcode` or multi-target combination to `.story-deployed` `target_cli`, and `.zcode/skills/story-setup/references/agent-references` to `references_dir`.
7. State in the report: ZCode 3.3.4 does not execute project/plugin custom Agents, so all specialist roles use solo/direct; project Hooks require `node` on PATH.

Plugin installation bypasses this algorithm: root `.zcode-plugin/plugin.json` exposes the same Skills/Commands/Hooks. Plugin Skills rank below workspace `.zcode/skills`; when both exist, the project snapshot wins and must be updated by rerunning `$story-setup`. **Register Hooks only once**: plugin manifest and workspace `.zcode/config.json` target the same events. With the plugin installed, never merge `config.json.patch` Hooks into `.zcode/config.json`; the manifest is the sole registration source.

### OpenClaw Skills-Only Deployment Algorithm (When target_cli Includes openclaw)

OpenClaw Phase 1 deploys skills only, not OpenClaw Agents/Hooks/plugins.

1. Read all 13 story skill directories containing `SKILL.md` under current repository `skills/` (`browser-cdp` and `story*`).
2. Write to project `skills/{skill-name}/`, replacing only known story-setup-managed dirs and preserving others.
3. Every `SKILL.md` must satisfy OpenClaw frontmatter: single-line `name` / `description`, single-line JSON `metadata` containing `metadata.openclaw`.
4. Merge `skills/story-setup/references/openclaw/AGENTS.md.tmpl` into project `AGENTS.md` using “AGENTS.md Merge Strategy.”
5. Write `openclaw` or multi-target combination to `.story-deployed` `target_cli`; for OpenClaw write `skills/story-setup/references/agent-references` to `references_dir`.
6. Include the notice from Phase 3 Step 10 in the report.

### Reasonix Skills-Only Deployment Algorithm (When target_cli Includes reasonix)

Reasonix (DeepSeek-Reasonix CLI) currently deploys only skills and `AGENTS.md`, not Reasonix Hooks/custom Agents, because no verifiable real CLI exists yet for Hook I/O and subagent behavior.

1. Copy all 13 current `skills/` directories containing `SKILL.md` (`browser-cdp` and `story*`) into project `skills/{skill-name}/`; replace only known managed dirs and preserve others.
2. At project root, create relative symlink `.agents/skills → ../skills` (shared skill root with Codex) so Reasonix native scanning discovers them. Preserve an existing symlink to `skills/`; do not overwrite a regular directory and mention it in the report. On Windows without symlinks, skip and use root `reasonix-plugin.json` with `reasonix plugin install`; retain `reasonix-plugin.json` as the install entrypoint.
3. Merge `skills/story-setup/references/reasonix/AGENTS.md.tmpl` into root `AGENTS.md` using the strategy below.
4. Write `reasonix` or multi-target combination to `.story-deployed` `target_cli`; for Reasonix use `skills/story-setup/references/agent-references` as `references_dir`.
5. Include the notice from Phase 3 Step 12.

### Generic Web AI / Other Agent Deployment Algorithm (When target_cli Includes generic)

The generic path supports NarraFork, Web AI, custom Agents, and other environments that can read project files. It deploys generic files without claiming native platform Hooks/Agents.

1. Copy all 13 current story skill directories containing `SKILL.md` (`browser-cdp` and `story*`) into project `skills/{skill-name}/`; replace known managed dirs only and preserve others.
2. Merge `skills/story-setup/references/generic/AGENTS.md.tmpl` into project `AGENTS.md`.
3. Write `generic` or multi-target combination to `.story-deployed` `target_cli`; for generic use `skills/story-setup/references/agent-references` as `references_dir`.
4. Include the notice from Phase 3 Step 11.

### Step 7: Create the Deployment Marker

- Create sentinel `.story-deployed`
- Write these YAML `key: value` fields, read by `references/templates/hooks/lib/sentinel.sh`:
  ```
  deployed_at: <date -u +"%Y-%m-%dT%H:%M:%SZ">
  agents_version: 29
  setup_skill_version: 1.2.10
  target_cli: claude-code（或 opencode、codex、antigravity、zcode、openclaw、reasonix、generic，或其任意组合）
  resolver_strategy: project-local-skill-reference
  references_dir: .claude/skills/story-setup/references/agent-references（Codex 写 .codex/skills/...；Antigravity 写 .agents/skills/...；ZCode 写 .zcode/skills/...；OpenClaw / Reasonix / generic 写 skills/...；多端用逗号分隔）
  ```
- session-start.sh and writing skills use this file to detect deployment and avoid repeated prompts
- If `target_cli` contains claude-code, also create one-time empty marker `.claude/.agents-pending-restart`. At the next session start, session-start.sh confirms Agents registered and deletes it, telling the user restart took effect. Do not create it for ZCode because project Agents are not deployed.
- If `.story-deployed` exists with missing/non-integer `agents_version` or a value below `29`, update hooks/agents/rules/reference bundle according to this process and `UPGRADING.md`; values above `29` already stopped in Phase 1 and must not be downgraded.

## Phase 3: Validate Installation

1. Validate Hook registration:
   - `.claude/settings.local.json` Hooks are correct
   - scripts under `.claude/hooks/` exist and are executable
   - `.claude/hooks/lib/common.sh` and `.claude/hooks/lib/sentinel.sh` exist
2. Validate Rules:
   - `.claude/rules/` files exist and contain `paths` frontmatter
3. Validate Agents:
   - seven definitions exist under `.claude/agents/`
4. Validate Agent reference bundle:
   - reference files under `.claude/skills/story-setup/references/agent-references/` are complete
   - every `story-setup/references/agent-references/<file>.md` resolves to the deployed bundle
5. Validate marker:
   - `.story-deployed` exists and includes timestamp; its `agents_version` is `29`; it also includes `agents_version: 29`, `setup_skill_version: 1.2.10`, `target_cli`, `resolver_strategy`, `references_dir`. Treat `.story-deployed` as the active sentinel.
6. Output installation report:
   - List all deployed files
   - List important notes, including merged existing configuration
    - **⚠️ Restart notice (must be prominent)**: This deployment wrote `.claude/agents/`, but Claude Code registers these custom Agents as `subagent_type` only at **session start**. **Start a new Claude Code session before writing.** Otherwise story-review / story-long-write spawning `story-architect`, `narrative-writer`, and others will receive “subagent_type unavailable” and fall back to solo, losing multi-Agent collaboration. To verify, run `/story-review` in the new session. `Effective Mode: full/lean` means success; `Fallback: ... -> solo` means old session or failed registration.
    - After restart, use `/story-long-write` or `/story-short-write`
    - If OpenCode Agent models were configured, output:
      ```
      Agent 模型配置：
        story-architect          → <高端模型>（provider/model-id）
        narrative-writer         → <中端模型>（provider/model-id）
        character-designer       → <中端模型>（provider/model-id）
        story-researcher         → <中端模型>（provider/model-id）
        chapter-extractor        → <低端模型>（provider/model-id）
        consistency-checker      → <低端模型>（provider/model-id）
        story-explorer           → <低端模型>（provider/model-id）
      ```
    - If automatic detection fails (`opencode models` unavailable), output:
      ```
      无法自动检测模型列表。以下 Agent 未配置模型，将使用主模型，成本可能较高：
        - chapter-extractor（建议使用低成本模型）
        - consistency-checker（建议使用低成本模型）
        - story-explorer（建议使用低成本模型）

      手动配置方法：编辑 .opencode/agents/{agent名}.md，在 frontmatter 中添加：
        model: provider/model-id

      可用模型列表与成本可通过 opencode models --verbose 查看（输出含每模型 cost/context）。
      模型库与定价见 OpenCode 官方模型源 https://models.dev/。
      ```
7. Validate OpenCode deployment when targeted:
    - Seven `.opencode/agents/` definitions exist with `mode: subagent` and `permission` frontmatter
    - `.opencode/plugins/story-hooks.ts` exists
    - `.opencode/plugins/lib/story_hook_core.js` exists and passes `node --check`; imported by story-hooks.ts and byte-identical to `.zcode` copy. Its `lib/` location prevents OpenCode’s single-level `.opencode/plugins/*.js` autodiscovery
     - Thirteen command files exist under `.opencode/commands/`
    - `skills/story-setup/references/agent-references/` is complete and count matches source
    - `opencode.json` `plugin` includes story-hooks
    - `.git/hooks/pre-commit` exists and is executable (skip executable check on Windows)
    - `.opencode/agents/` frontmatter parses as YAML and configured `model:` is a valid top-level scalar, not merely a grepped substring; every retained `model:` remains top-level
8. Validate Codex deployment when targeted:
    - `AGENTS.md` contains Codex story routing
    - Seven `.codex/agents/*.toml` definitions exist and parse
    - `.codex/hooks.json` exists and is valid JSON; Unix `command` starts only `run-story-hook.sh`, Windows `commandWindows` only `run-story-hook.cmd`; no direct `story_codex_hook.py` registration
    - `.codex/hooks/story_codex_hook.py`, `run-story-hook.sh`, `run-story-hook.cmd` exist; Python syntax is valid and POSIX/Windows launchers locate project root from nested cwd
    - `.codex/skills/story-setup/references/agent-references/` is complete and count matches source
    - Report: Codex must trust project `.codex/`, review/trust unmanaged hooks in `/hooks`, and start a new session for custom Agents. If runtime still returns `unknown agent_type`, use each Skill’s solo/direct fallback.
9. Validate Antigravity deployment when targeted:
    - Thirteen story skills under `.agents/skills/` are real directories with readable `SKILL.md`; `.agents/skills` is the supported root, and `.agents/skills/story-setup/references/agent-references/` is complete
    - Seven Markdown Agents under `.agents/agents/` parse with correct names, model tiers, official tool allowlist, read-only boundaries, and `.agents/skills/` references
    - `.agents/rules/oh-story.md` uses `trigger: always_on` and is ≤12,000 characters
    - `.agents/hooks.json` is valid; top-level `oh-story` has exactly PreToolUse/PostToolUse/PreInvocation/Stop; user groups remain; both hook JS files parse
    - Fixture validation: PreToolUse denies missing outline/tracking, allows ordinary writes, and emits commit advisory; PostToolUse stdout is always `{}` and stores manuscript findings in the session artifact; next PreInvocation injects them; Stop continues at most once for unresolved findings; clean prose clears pending state
    - Report: start a new Antigravity conversation; Hooks require `node` on PATH; no external PreCompact/PostCompact API, so Always-On Rule restores `追踪/上下文.md`; smoke-test IDE and interactive `agy` separately. `agy 1.1.22 -p` may scan workspace before silent authentication and not reload Agents/Hooks afterward, so it is unsupported and may report `subagent not found` or write to `~/.gemini/antigravity-cli/scratch/`. For command-line writing, enter interactive `agy` from the project, verify `/skills`, `/agents`, `/hooks`, then test and inspect scratch for accidental story output.
10. Validate ZCode deployment when targeted:
    - Root `AGENTS.md` contains ZCode `$story-*` routing, outline guard, solo/direct fallback
    - Thirteen Skills under .zcode/skills/ and Commands exist with valid frontmatter/names; each Skill has a readable `SKILL.md`
    - Both `.zcode/hooks/` JS files exist and pass `node --check`
    - `.zcode/config.json` is valid; validate the deployed `.zcode/config.json` against the mutually exclusive Hook branch from Step 4. Without plugin: `hooks.enabled=true`, supported events only, `process` args target project Hooks. With plugin registration: config excludes/removes these oh-story Hook registrations. **Never merge them back merely to satisfy validation**, which would double-fire events
    - Agent references at `.zcode/skills/story-setup/references/agent-references/` are complete and resolve
    - Fixture invokes SessionStart, PreToolUse deny/allow, PostToolUse; stdout empty without findings and strict ZCode JSON with output
    - Report: ZCode 3.3.4 does not execute project/plugin custom Agents; full/lean requests reliably fall back to solo/direct. Hooks require `node`; start new ZCode session to refresh Skills/Commands/AGENTS.md.
11. Validate OpenClaw deployment when targeted:
    - `AGENTS.md` contains OpenClaw story routing
    - Thirteen story skill dirs under `skills/` exist, each `SKILL.md` has single-line `name`, `description`, and JSON `metadata.openclaw`
    - Agent references in `skills/story-setup/references/agent-references/` are complete and count matches source
    - Report: OpenClaw Phase 1 is skills-only; no Agents/Hooks, so outline guards, commit reminders, and session/compact injection are soft Skill constraints. OpenClaw snapshots eligible skills at session start; if commands/skills do not appear, start a new session or wait for watcher refresh.
12. Validate generic Web AI / other Agent deployment when targeted:
    - `AGENTS.md` contains generic story routing
    - Thirteen readable story Skill directories exist under `skills/`, each with `SKILL.md`
    - Agent references under `skills/` are complete and count matches source; retain the project `skills/` root
    - Report: no platform-specific Hooks/custom Agents; outline guards, commit reminders, session/compact injection, and multi-Agent collaboration use soft Skill constraints or solo/direct fallback.
13. Validate Reasonix deployment when targeted:
    - `AGENTS.md` contains Reasonix story routing and solo/direct fallback
    - Thirteen readable story Skill directories exist under `skills/`, each with `SKILL.md`
    - On POSIX, `.agents/skills` symlinks to `skills/`; on Windows without symlink, confirm root `reasonix-plugin.json` supports `reasonix plugin install`
    - Agent references in `skills/story-setup/references/agent-references/` are complete and count matches source
    - Report: Reasonix is skills-only; no Hooks/custom Agents. Outline guard, commit reminder, session/compact injection are soft constraints; Skills requiring specialist Agents use solo/direct. Validate discovery with `reasonix doctor capabilities`; if new skills do not appear, start a new session or install the root plugin.

---

## Template Placeholders

| Placeholder | Replacement | Example |
|--------|----------|------|
| `{项目名}` | User project name or directory | 《剑来》, 《暗卫》 |
| `{书名}` | Book directory name | Same as `{项目名}`, or user-defined |
| `{目标平台}` | Publishing platform | Qidian, Tomato, Jinjiang, Zhihu Yanyan |
| `{作者名}` | Pen name or nickname | Use “作者” when unspecified |

Remove braces when replacing. If project name is unspecified, use the current directory. Leave other unspecified placeholders unchanged.

## CLAUDE.md Merge Strategy

When CLAUDE.md exists:
1. Prefer the story-setup managed marker block and replace only its contents
2. Without markers, read existing CLAUDE.md and split by `##` headings into a section map
3. Read and split template CLAUDE.md.tmpl the same way
4. Template standard sections (Skill routing, structure, collaboration, post-Compact context recovery) **replace** same-name user sections
5. Preserve user-only sections unchanged
6. Ask the user to resolve unknown conflicts

## AGENTS.md Merge Strategy (OpenCode / Codex / ZCode / OpenClaw / Reasonix / generic)

When AGENTS.md exists:
1. Prefer the story-setup managed marker block and replace only its contents
2. Without markers, split existing AGENTS.md by `##` headings into a section map
3. Use the target template: OpenCode `skills/story-setup/references/opencode/AGENTS.md.tmpl`; Codex `skills/story-setup/references/codex/AGENTS.md.tmpl`; ZCode `skills/story-setup/references/zcode/AGENTS.md.tmpl`; OpenClaw `skills/story-setup/references/openclaw/AGENTS.md.tmpl`; Reasonix `skills/story-setup/references/reasonix/AGENTS.md.tmpl`; generic `skills/story-setup/references/generic/AGENTS.md.tmpl`
4. Standard template sections replace same-name sections; preserve user-only sections
5. In multi-target deployments, keep one copy of shared generic sections and separate tool-specific notes into subsections so they do not overwrite one another

## Redeployment

- No `.story-deployed` → new install; run all of Phase 2
- Exists with `agents_version: 29` → tell user `.story-deployed` shows it is deployed and confirm redeployment with AskUserQuestion; explain this refreshes from the current local package, while updating the Skill itself requires `npx skills add` or marketplace
- Exists with missing/non-integer/below-29 `agents_version` → report update required; rerun Phase 2 to replace Agents/Hooks/Rules/reference bundle while using merge strategies for CLAUDE.md / AGENTS.md / settings.local.json / .codex/hooks.json / `.agents/hooks.json` / .zcode/config.json
- Exists above `29` → current Skill is old; stop and update oh-story-claudecode without overwriting newer project deployment

---

## References

| File | Purpose |
|------|------|
| references/templates/hooks/ | Eight Hook templates + `story_hook_core.js` (shared manuscript/outline guard/continuity/commit detection implementation, identical to OpenCode/ZCode) + `story_hook_cli.js` (Node bridge from bash Hook to core) + `lib/common.sh`/`lib/sentinel.sh`. Manuscript fallback `check-prose-after-write.sh` is limited to PostToolUse Write/Edit; Bash writes such as `cat>`/`tee` are covered by Codex Stop end-of-turn git scan, while Claude/OpenCode Bash is pre-guard only. |
| references/antigravity/ | Antigravity 2.0 Always-On Rule, named-group Hook templates, and I/O adapter; postwrite manuscript findings bridge through session artifacts to PreInvocation/Stop |
| references/zcode/ | ZCode AGENTS, 13 Commands, workspace config patch, and strict-JSON Hook runner |

---

## Workflow Handoff

**Pipeline:** Deployment
**Position:** Initialization (first)

| When | Go To | Command |
|---|---|---|
| Deployment complete; start writing | story-long-write / story-short-write | `/story-long-write` or `/story-short-write` |
| Import an existing novel for decomposition | story-import | `/story-import` |
| Need authenticated browser state for ranking scan/source retrieval | browser-cdp | `/browser-cdp`; generic requires platform permission for local scripts/browser control |

Invocation syntax: Claude `/名`; Codex/ZCode `$名`; Antigravity browse via `/skills` or name directly; OpenClaw `/skill 名`; Reasonix / generic name the skill directly.
