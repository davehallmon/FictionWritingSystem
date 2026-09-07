You are the writing infrastructure deployer. Deploy the web writing tool set to the user project directory: the adapted CLI uses dedicated hooks/agents/config; NarraFork, Web AI, custom Agent and other environments use the common file mode.

**Iron rule of execution: Do not overwrite existing configurations of users, merge rather than replace. **

---

**Self-check the reference directory first**: Based on the directory where the `SKILL.md` is being executed, list the subdirectories under `references/` at the same level as it, and check the following 9 Whether all names are in ** and are not empty** - `agent-references`, `templates`, `opencode`, `codex`, `antigravity`, `zcode`, `openclaw`, `reasonix`, `generic`; same level `scripts/merge-claude-settings.py`, `scripts/merge-codex-hooks.py`, `scripts/merge-antigravity-hooks.py`, `scripts/generate-antigravity-agents.mjs`, `scripts/deploy-antigravity-skills.py` and `scripts/copy-path-safety.py` Must also exist (Claude/Codex/Antigravity hooks merging, Antigravity Skills materialization and agent generation, recursive copy safety checks depend on them). If it is missing, it means that the skill package is not fully installed. **Stop immediately without writing any deployment files**. The report distinguishes between "missing directory", "directory is empty" and "missing script", and gives repair instructions: "story-setup reference package is incomplete, missing {path}. Reinstall oh-story-claudecode according to your installation method (rerun command line installation `npx skills add zenstory-ai/oh-story-claudecode -y -g`, marketplace / Plugin Management (Reinstall it in the panel), and then execute /story-setup."

> The criterion is "whether there is `SKILL.md`": only look at the `references/` of the same level as the `SKILL.md` being executed. `.claude/skills/story-setup/`, `.codex/skills/story-setup/` and OpenCode's `skills/story-setup/` in the project only have `references/agent-references/` and do not contain `SKILL.md`. They are not execution directories, and do not check them. The project copy of Antigravity / ZCode / OpenClaw / Reasonix / generic is a copy of the entire skill and comes with `SKILL.md`. The 9 subdirectories are complete and can be checked as usual.

> Steps 9-11 only recognize the **mutually exclusive** tags on each end. The `metadata.openclaw` of `skills/*/SKILL.md` does not serve as OpenClaw signal: all 13 skills have this field, and the `skills/` deployed by the three skills-only paths of OpenClaw / Reasonix / generic looks the same, and using this method will misidentify the latter two as OpenClaw. `.agents/skills/` is shared by Antigravity, Codex and Reasonix, and is not recognized individually; Antigravity must be identified by the hooks/agents/rule-specific tag. The real distinguishing point for the last three ends is the header line of the respective `AGENTS.md` template.

12. Such as `.claude/` or `CLAUDE.md`, OpenCode, Codex, Antigravity, ZCode, OpenClaw, Reasonix, generic tags exist simultaneously → Use AskUserQuestion to let the user select the target environment (options: Claude Code / OpenCode / Codex / Google Antigravity / ZCode / OpenClaw / Reasonix / General Web AI or other Agent / any combination)
13. If none of the eight types of tags exist (new project) → Use AskUserQuestion to let the user select the target environment
- User selects opencode → `target_cli = opencode`, `opencode.json` and `.opencode/` are created when deploying
- User selects claude-code → processed according to existing logic
- User selects codex → ​​`target_cli = codex`, creates `.codex/` when deploying
- User selects antigravity → `target_cli = antigravity`, creates `.agents/skills`, `.agents/agents`, `.agents/rules`, `.agents/hooks` and merges `.agents/hooks.json` when deploying
- The user selects zcode → `target_cli = zcode`, creates `.zcode/` when deploying, merges the root `AGENTS.md`, and does not create project custom agents
- The user selects openclaw → `target_cli = openclaw`, and copies OpenClaw compatible skills to the project `skills/` when deploying
- The user selects reasonix → `target_cli = reasonix`, copies skills to the project `skills/` during deployment, writes the Reasonix version `AGENTS.md`, and does not create the project custom agents/hooks
- The user selects generic Web AI / other Agent → `target_cli = generic`, deploys the generic `AGENTS.md` and the project's local `skills/`; does not write platform-specific hooks/agents
- User-selected multi-endpoint → `target_cli = subset of claude-code,opencode,codex,antigravity,zcode,openclaw,reasonix,generic` (contains only user-selected endpoints)

## Phase 2: Deploy infrastructure

After confirming the deployment location using AskUserQuestion, execute it in sequence.

The entire Phase 2 is idempotent: directory copying, file writing, and the merging algorithms in the table below have consistent results after repeated executions. If the phase fails due to environmental reasons (tool unavailable, permission denied, network failure), rerun this Phase directly from the beginning without cleaning up the semi-finished product first; the user status file of `create only if absent` (see Owner class in the table below) will not be overwritten twice.

**The two columns of base directories are different**: `Source path` is relative to the skill package being executed, and `Target path` is relative to the user project root. Before executing each line (and each recursive copy step in the end-deployment algorithm below), the wildcard is first instantiated into a single source/destination, and then checked with the `scripts/copy-path-safety.py` sibling of this `SKILL.md`. This script follows the existing symlink according to `Path.resolve` / `realpath` semantics, and uses `samefile` to check the file system object when both sides exist; **Only converting absolute paths or comparing strings does not count as checking completion**. Read its JSON: no-op when `status: same`, copying is prohibited; copying is only possible when `copy_allowed: true`; `source_missing`, `unsafe_target_within_source` or `filesystem_identity_error` must stop this step and report it. When the script cannot be run, you can only use the file system API of the current environment to do the exact same canonical realpath, same-object and target-descendant checks; if it cannot be confirmed, stop and do not try to copy. The project copy of OpenClaw / Reasonix / generic is a copy of the entire skill, and the copy in the project will be executed when re-running; Reasonix / Codex may also be loaded through `.agents/skills → ../skills` symlink. Different path text may also point to the same directory. Literally copying will embed the directory into itself and fill the disk.

**Clean up self-nested residue before deployment**: `{.claude,.codex,.zcode}/skills/story-setup/references/agent-references/` and the project root `skills/story-setup/references/agent-references/` if there are more `agent-references/` layers (may be embedded in multiple layers), and `skills/story-setup/skills/`, delete the entire section and then deploy it, and list the deleted path in the installation report.

### Step 1: Deployment Checklist (Mechanical Checkable)

---
name: story-setup
version: 1.2.10
description: "网文写作工具集基础设施部署。为 Claude Code / OpenCode / Codex / Google Antigravity / ZCode / OpenClaw / Reasonix 提供内置适配；Web AI / 通用 Agent 可走 skills + AGENTS.md 文件模式。触发方式：/story-setup、$story-setup、「准备写书」「帮我搭一下环境」「配置写作项目」。"
metadata: {"openclaw":{"source":"https://github.com/zenstory-ai/oh-story-claudecode"}}
---
# story-setup：网文写作工具集基础设施部署

## Phase 1：检测项目状态

1. Check whether the current directory has been deployed (`.story-deployed` exists)
- `agents_version` is missing, non-integer or less than `29` → mark as pending update and continue executing the current deployment
   - `agents_version: 29` → 使用 AskUserQuestion 确认是否重新部署；提示里写明重新部署只用**当前本地 skill 包**刷新项目文件，要拿 skill 本身的新版本得先更新 oh-story-claudecode（`npx skills add` 或 marketplace），再回来重跑
- `agents_version` is greater than `29` → the current story-setup is older than the project deployment; stop to avoid downgrade coverage, prompt to update oh-story-claudecode first, do not write any deployment files
- Also read the `target_cli` field. **Deployed projects are subject to the value in sentinel**: When it is not empty (comma-separated multi-terminal combinations are retained as they are), skip the environment detection and selection in steps 5-12 below, and redeploy directly according to these terminals. Only if a field is missing or empty does it fall back to probing. When the user explicitly requests to add or delete the target, use AskUserQuestion to change the existing value, and write the changed value back to sentinel.
2. Check if there is a book title directory (a directory containing a `track/` subdirectory, or a user-defined structure)
- Yes → Identified as a long-form project, display current project information
- None → Identified as new or short project
3. Check if `.claude/settings.local.json` exists
   - 存在 → 读取现有配置，后续合并
- does not exist → create a new file later
4. Check if the `.active-book` file exists
- Exists → Shows currently active titles
- does not exist → skip
5. Check if `opencode.json` or `.opencode/` exists
   - 存在 → 识别为 opencode 项目，`target_cli = opencode`
- does not exist → skip
6. Check the Codex sections in `.codex/`, `.codex/config.toml`, `.codex/agents/`, `.codex/hooks.json`, `AGENTS.md`
   - 存在 → 识别为 Codex 项目，`target_cli = codex`
- does not exist → skip
7. Check for Antigravity tags in `.agents/hooks.json`, `.agents/agents/`, or `.agents/rules/oh-story.md`
- exists → identified as Google Antigravity project, `target_cli = antigravity`
   - 不存在 → 跳过
8. Check the ZCode sections in `.zcode/`, `.zcode/config.json`, `zcode.json`, `.zcode/skills/`, `.zcode/commands/`, `AGENTS.md`
   - 存在 → 识别为 ZCode 项目，`target_cli = zcode`
- does not exist → skip
9. Check the OpenClaw section in `openclaw.json`, `.openclaw/`, or `AGENTS.md` (the title line contains `OpenClaw`)
- exists → identified as OpenClaw project, `target_cli = openclaw`
- does not exist → skip
10. Check the Reasonix section in `.reasonix/`, `reasonix-plugin.json`, `REASONIX.md`, or `AGENTS.md` (the title line contains `Reasonix`)
- exists → identified as Reasonix project, `target_cli = reasonix`
- does not exist → skip
11. Check the general section in `AGENTS.md` (the title line contains `Web Writing Toolset (General Agent/Web AI)`)
- exists → identified as generic Web AI project, `target_cli = generic`
   - 不存在 → 跳过

| Source path | Target path | Owner class | Merge mode | Validation check |
|-------------|-------------|-------------|------------|------------------|
| `skills/story-setup/references/templates/CLAUDE.md.tmpl` | `CLAUDE.md` | user+managed | marker/section merge | contains story skill routing sections |
| `skills/story-setup/references/templates/hooks/` | `.claude/hooks/` | story-setup managed | recursive replace | `session-*.sh`, `detect-story-gaps.sh`, `validate-story-commit.sh`, `guard-outline-before-prose.sh`, `check-prose-after-write.sh`, `story_hook_core.js`, `story_hook_cli.js`, `lib/common.sh`, `lib/sentinel.sh` exist; `story_hook_core.js` is byte consistent with OpenCode/ZCode copy |
| `skills/story-setup/references/templates/rules/*.md` | `.claude/rules/*.md` | story-setup managed | replace | every rule contains `paths` frontmatter |
| `skills/story-setup/references/templates/agents/*.md` | `.claude/agents/*.md` | story-setup managed | replace | 7 agent files exist |
| `skills/story-setup/references/agent-references/*.md` | `.claude/skills/story-setup/references/agent-references/*.md` | story-setup managed | replace | every `story-setup/references/agent-references/*.md` reference resolves |
| `skills/story-setup/references/templates/settings-hooks.json` | `.claude/settings.local.json` | user+managed | replace managed registrations by stable hook identity | hook JSON valid; the old matcher registration has been migrated, one copy of the current template command, and the user hook is retained |
| `skills/story-setup/scripts/merge-claude-settings.py` | Executed during deployment, not copied to the project | story-setup helper | execute | Replace known story hook registration, retain user hooks/top-level fields, v24→v25 migration and repeated execution idempotent |
| `skills/story-setup/scripts/copy-path-safety.py` | Executed before each recursive copy step, not copied to the project-specific directory | story-setup helper | execute | JSON only allows copying when `copy_allowed: true`; symlink same object no-op; stops when target is located in source |
| generated sentinel | `.story-deployed` | story-setup managed | replace | contains `agents_version`, `setup_skill_version`, `target_cli`, `resolver_strategy`, `references_dir` |
| `skills/story-setup/references/opencode/AGENTS.md.tmpl` | `AGENTS.md` | user+managed | marker/section merge | contains story skill routing sections | target_cli contains opencode |
| `skills/story-setup/references/opencode/agents/` | `.opencode/agents/` | story-setup managed | replace | 7 agent files exist (before replacing, press "Keep existing model configuration" in "Configure OpenCode Agent Model" to cache the existing `model:` to avoid overwriting the user's configured model) | target_cli contains opencode |
| `skills/story-setup/references/opencode/plugin.ts` | `.opencode/plugins/story-hooks.ts` | story-setup managed | replace | TypeScript plugin file exists | target_cli 含 opencode |
| `skills/story-setup/references/opencode/story_hook_core.js` | `.opencode/plugins/lib/story_hook_core.js` | story-setup managed | replace | Node syntax valid; consistent with ZCode copy bytes; imported by story-hooks.ts | target_cli contains opencode |
| `skills/story-setup/references/opencode/commands/` | `.opencode/commands/` | story-setup managed | replace | 13 command files exist | target_cli 含 opencode |
| `skills/story-setup/references/opencode/opencode.json.patch` | merge into `opencode.json` | user+managed | merge by plugin/permission key | plugin entry registered | target_cli contains opencode |
| repository `skills/story-setup/references/agent-references/` | `skills/story-setup/references/agent-references/` | story-setup managed | replace | every reference resolves | target_cli with opencode |
| `skills/story-setup/references/opencode/pre-commit.sh` | `.git/hooks/pre-commit` | user+managed | append or create | file exists and is executable; if the marker block is included, the block content will be replaced, if it is not included, the exit 0 position will be detected. Smart insertion | target_cli contains opencode |
| `skills/story-setup/references/codex/AGENTS.md.tmpl` | `AGENTS.md` | user+managed | marker/section merge | contains Codex story skill routing sections | target_cli contains codex |
| `skills/story-setup/references/codex/agents/` | `.codex/agents/` | story-setup managed | replace | 7 TOML agent files parse and contain `name`/`description`/`developer_instructions` | target_cli contains codex |
| `skills/story-setup/references/codex/hooks/hooks.json` | `.codex/hooks.json` | user+managed | replace managed registrations by stable hook identity | hook JSON valid; all stale direct/launcher registrations removed, current 6 registrations present exactly once | target_cli with codex |
| `skills/story-setup/references/codex/hooks/{story_codex_hook.py,run-story-hook.sh,run-story-hook.cmd}` | `.codex/hooks/` file with the same name | story-setup managed | replace | Python/shell/cmd launcher complete files | target_cli contains codex |
| `skills/story-setup/scripts/merge-codex-hooks.py` | 部署时执行，不复制到项目 | story-setup helper | execute | 替换已知管理注册、保留用户 hooks 与未知顶层字段，结果幂等 | target_cli 含 codex |
| `skills/story-setup/references/agent-references/` | `.codex/skills/story-setup/references/agent-references/` | story-setup managed | replace | every reference resolves | target_cli 含 codex |
| current package skill root + `scripts/deploy-antigravity-skills.py` | `.agents/skills/{browser-cdp,story*}/` | story-setup managed for 13 known skill names | atomically replace known dirs; preserve unknown skills; never write through symlink | 13 real skill directories with valid `SKILL.md` exist | target_cli contains antigravity |
| `skills/story-setup/scripts/generate-antigravity-agents.mjs` + Claude agent sources | `.agents/agents/agent-name/agent.md` (`agent-name` is the actual name) | story-setup managed for 7 known agent definitions | generate then atomically replace known definitions; preserve unknown user agents | 7 Markdown agents parse; exact Antigravity tool names; `mainAgent: false`, `subagent: true` | target_cli contains antigravity |
| `skills/story-setup/references/antigravity/rules/oh-story.md` | `.agents/rules/oh-story.md` | story-setup managed | replace | `trigger: always_on`; under 12,000 characters | target_cli with antigravity |
| `skills/story-setup/references/antigravity/hooks/hooks.json` | `.agents/hooks.json` | user+managed | replace only top-level `oh-story` group | valid Antigravity named-group schema; user groups preserved; idempotent | target_cli contains antigravity |
| `skills/story-setup/references/antigravity/hooks/{story_antigravity_hook.js,story_hook_core.js}` | `.agents/hooks/` same names | story-setup managed | replace | Node syntax valid; core byte-identical to shared source; hook contract tests pass | target_cli with antigravity |
| `skills/story-setup/scripts/merge-antigravity-hooks.py` | deployment helper only | story-setup helper | execute | atomically replaces only `oh-story`, preserves user groups, idempotent | target_cli contains antigravity |
| `skills/story-setup/references/zcode/AGENTS.md.tmpl` | `AGENTS.md` | user+managed | marker/section merge | contains ZCode `$story-*` routing and solo fallback | target_cli contains zcode |
| repository `skills/{browser-cdp,story*}/` | `.zcode/skills/{browser-cdp,story*}/` | story-setup managed for known skill names | replace known skill dirs only | 13 `SKILL.md` files exist and satisfy ZCode frontmatter limits | target_cli contains zcode |
| `skills/story-setup/references/zcode/commands/` | `.zcode/commands/` | story-setup managed for known command names | replace known command files only | 13 commands have valid names/frontmatter | target_cli contains zcode |
| `skills/story-setup/references/zcode/hooks/story_zcode_hook.js` | `.zcode/hooks/story_zcode_hook.js` | story-setup managed | replace | Node syntax valid; hook contract tests pass | target_cli with zcode |
| `skills/story-setup/references/zcode/hooks/story_hook_core.js` | `.zcode/hooks/story_hook_core.js` | story-setup managed | replace | Node syntax valid; hook contract tests pass | target_cli with zcode |
| `skills/story-setup/references/zcode/config.json.patch` | merge into `.zcode/config.json` | user+managed | merge by event+matcher+process args | JSON valid; According to step 4 of "ZCode Deployment Algorithm" hooks mutually exclusive branch verification - when the oh-story plug-in is not installed `hooks.enabled=true`, only supported events; when the plug-in is installed, verify that `.zcode/config.json` does not contain (or has been removed) this batch of oh-story hooks registration | target_cli contains zcode |
| `skills/story-setup/references/openclaw/AGENTS.md.tmpl` | `AGENTS.md` | user+managed | marker/section merge | contains OpenClaw story skill routing sections | target_cli contains openclaw |
| `skills/story-setup/references/generic/AGENTS.md.tmpl` | `AGENTS.md` | user+managed | marker/section merge | contains generic story skill routing sections | target_cli contains generic |
| `skills/story-setup/references/reasonix/AGENTS.md.tmpl` | `AGENTS.md` | user+managed | marker/section merge | contains Reasonix story skill routing sections and solo/direct fallback | target_cli contains reasonix |
| repository `skills/{browser-cdp,story*}/` | `skills/{browser-cdp,story*}/` | story-setup managed for known skill names | replace known skill dirs only | 13 `SKILL.md` files exist; OpenClaw-compatible frontmatter | target_cli contains openclaw or generic or reasonix |
| repository `skills/story-setup/references/agent-references/` | Along with the previous line, the entire skill copy is landed, this line no-op | story-setup managed | Do not copy separately | every reference resolves | target_cli contains openclaw or generic or reasonix |

### opencode.json merge algorithm

When deploying `opencode.json.patch`, merge it according to the following rules:

1. Read the existing `opencode.json` (if it exists) and parse the JSON
2. Merge `plugin` array: add `./.opencode/plugins/story-hooks.ts` to the array and remove duplicates
3. Keep other configuration fields that the user already has (`permission`, `model`, `provider`, etc.) and do not overwrite them.
4. Write the merged `opencode.json`

### Step 2: Deploy CLAUDE.md

- Read `skills/story-setup/references/templates/CLAUDE.md.tmpl`
- Replace placeholders (see "Template placeholders" section below)
- Write `CLAUDE.md` to the project root directory (if it already exists, follow the "CLAUDE.md merge strategy")

### Step 3: Deploy Hooks

- **Recursively copy complete directory tree**: Copy `skills/story-setup/references/templates/hooks/` to user project `.claude/hooks/`
- The subdirectory `lib/` must be retained where:
- `lib/common.sh` provides `project_root`, `discover_active_book`, `discover_all_books`
- `lib/sentinel.sh` provides `.story-deployed` field reading
- Just set execution permission (`chmod +x`) on `.claude/hooks/*.sh`; `lib/*.sh` is hooked by `source` and does not require executable bit

### Step 4: Deploy Rules

- Read all `.md` files under `skills/story-setup/references/templates/rules/`
- Copied to the `.claude/rules/` directory of the user project

### Step 5: Deploy Agents

- Read all `.md` files under `skills/story-setup/references/templates/agents/`
- Copied to the `.claude/agents/` directory of the user project
- The Agent file belongs to the story-setup management file and can be safely overwritten; when upgrading the version, it can be redeployed according to the version detection result of `UPGRADING.md`
- When **`target_cli` contains opencode, perform Step 1 of "Configuring OpenCode Agent Model" below to cache the existing `model:`** before overwriting `.opencode/agents/`. That step is written later in this section, but it must be run first - wherever it is read and executed in order, it will be overwritten and then cached, and the model configured by the user will be gone.
- **A new session must be opened after deployment**: The agent is only registered when the session is started; for the reason and the copy of the report that must be output, see "Output Installation Report" in "Verify Installation".

#### Agent compatibility processing

- The Agent text uses Claude Code Markdown as the real source; OpenCode's `.opencode/agents/*.md` and Codex's `.codex/agents/*.toml` are directly copied from the pre-generated products under `references/opencode/agents/` and `references/codex/agents/`. Antigravity's `.agents/agents/agent-name/agent.md` (`agent-name` is the actual name) calls `scripts/generate-antigravity-agents.mjs` distributed with story-setup during deployment to deterministically convert Claude's tool name, model file, reference root and calling term into the Antigravity 2.0 contract; Claude frontmatter must not be used Copy it as it is.
- **ZCode 3.3.4 does not deploy project agents**: Its custom sub-agent only supports user-level `~/.zcode/agents/`, and `agents` in the plugin manifest is not currently executed. Do not create `.zcode/agents/` or modify user home; the related Skill must solo/direct and report fallback.
- **OpenClaw Phase 1 does not deploy agents**: OpenClaw only deploys skills. Agent collaboration-related skills must be downgraded to solo/direct according to the existing fallback rules. Do not copy Claude/OpenCode agent frontmatter directly into OpenClaw agent.
- After being deployed to the project, the reference materials referenced in the agent must go to the `story-setup/references/agent-references/*.md` copy path within the skill; do not cross-skill references from other skills. Each adapter only uses the current specification prefix: Claude Code is `.claude/skills/`, Antigravity is `.agents/skills/`, OpenCode / OpenClaw / Reasonix / generic is `skills/`, Codex is `.codex/skills/`, ZCode is `.zcode/skills/`; historical alternative paths are not traversed at runtime.

#### Deploy Agent References

- Copy all `.md` under `skills/story-setup/references/agent-references/` to `.claude/skills/story-setup/references/agent-references/` in the project
- Verification: Whenever `story-setup/references/agent-references/<file>.md` appears in agent or reference, `<file>.md` must exist in both the source package and the target package.

#### Deploy Codex Agents (when target_cli contains codex)

- Read all `.toml` files under `skills/story-setup/references/codex/agents/` and copy them to the user project `.codex/agents/`
- The Agent file belongs to the story-setup management file and can be safely overwritten; the TOML in `references/codex/agents/` is deterministically generated from the Claude agent template by the `scripts/generate-codex-agents.py` in the warehouse root and submitted to the library. The deployment is only copied.
- Verify that each TOML can be parsed and contains Codex required fields: `name`, `description`, `developer_instructions`
- Read-only duty agents (`chapter-extractor`, `consistency-checker`, `story-explorer`) must be retained `sandbox_mode = "read-only"`
- **You must trust + open a new Codex session after deployment** (see "Verification Codex Deployment" for report copy and fallback rules); if `unknown agent_type` is returned during runtime, the caller must downgrade solo/direct and report fallback.
- Synchronously copy `skills/story-setup/references/agent-references/` to `.codex/skills/story-setup/references/agent-references/` as the main reference path in the project of Codex agent

#### Deploy Antigravity Agents (when target_cli contains antigravity)

- First make sure `node` is in PATH; Antigravity agent generation and project hooks both depend on Node. If it is missing, it will stop the deployment of Antigravity, leaving no semi-finished product, and prompting you to install Node and rerun.
- Execute `node "{story-setup skill directory}/scripts/generate-antigravity-agents.mjs" --source "{story-setup skill directory}/references/templates/agents" --dest "{project}/.agents/agents"`. The generator first renders all 7 agents, then atomically replaces the 7 known `.agents/agents/agent-name/agent.md` definitions (`agent-name` is the actual name), and cleans up the old version of the flat `.md` with the same name; other user agents are retained, and any source frontmatter exception must not leave a semi-updated directory, nor must it be written out of the project along the managed agent symlink.
- Verify 7 `.md`: `name` is consistent with the file name; `mainAgent: false`, `subagent: true`; model only uses `flash` / `pro`; tools only come from Antigravity official name `view_file`, `find_by_name`, `grep_search`, `write_to_file`, `replace_file_content`, `multi_replace_file_content`, `run_command`; Claude's `Read/Glob/Grep/Write/Edit/Bash` tool name or `.claude/skills/` reference prefix must not remain.
- Read-only agents (`chapter-extractor`, `consistency-checker`, `story-explorer`) must not contain write files or command tools; other agents are mapped according to the capability boundaries of Claude's true source.
- Antigravity invokes these agents via the `TypeName` of `invoke_subagent`. After deployment, open a new Antigravity conversation, and then use `story-review` to verify full/lean; when a custom agent cannot be resolved at runtime, press the solo/direct fallback of the skill to execute.

#### Configure OpenCode Agent model

> Only executed when `target_cli` contains `opencode`. When the OpenCode sub-agent does not specify a model, it inherits the main model, causing the low-cost Agent to also consume the quota of the main model. This step automatically detects the user model and writes the `model:` field.

##### Step 1: Retain existing model configuration (must be executed before replace in `.opencode/agents/`)

OpenCode agents deployment is `replace`, which will overwrite the last written `model:`. Therefore, before executing the replace **, scan the existing `.opencode/agents/*.md` and cache the `model:` (agent name → model ID) of each agent. When subsequent detection fails/times out, or the user skips a certain level, the cached value is used to backfill to avoid erasing the low-cost model configured by the user last time as the main model. If replace has occurred first and the cache is empty, it will be processed as a new deployment, and "Failed to retain the last model configuration" will be prompted in the installation report.

##### Step 2: Get the model list

Priority is given to executing `opencode models --verbose`, which outputs metadata containing cost (input/output/cache unit price), context, and capabilities; when unavailable or parsing fails, it falls back to `opencode models` plain text (each line of `provider/model`). Both use a 60000ms (60 seconds) timeout because the models.dev cache needs to be loaded on the first run.

- Success → Enter "Model Grading"
- Timeout → retry (the cache may not be warmed up); if it still times out, press "Keep existing model configuration" to cache backfill the existing `model:`, skip automatic configuration, and output manual configuration guide in the installation report
- Failure (command does not exist, output is empty, etc.) → Same as above: backfill the "Keep existing model configuration" cache, skip automatic configuration, and output manual configuration guide

##### Step 3: Model grading

**Prioritize grading by cost (when `--verbose` is present)**: Sort by the actual cost of each model from low to high - the cheapest/free tier for the low-end, the mid-price tier for the mid-range, and the most expensive or the most contextual/capable tier for the high-end. Free models are classified as low-end based on the real cost=0, not based on the marketing words in the name** (for example, `nemotron-3-ultra-free` has `ultra` in its name but cost=0, so it should be classified as low-end). Models without cost data are also candidates and will not be discarded.

**Fall back to grading by keyword (without `--verbose` or without cost)**: The model name after the last `/` in the model ID is divided into segments by `-`, `.`, `_`, and keywords are accurately matched segment by segment (not case-sensitive). For example, `minimax-m3` is split into `[minimax, m3]`, which does not match `mini` nor `max`; `claude-haiku-4.5` is split into `[claude, haiku, 4, 5]`, which matches `haiku`. Keyword ranking is heuristic, and the installation report is marked with `Grading basis: keyword (heuristic)`.

- A model may match keywords of multiple levels, and the highest level will be selected.
- Models that do not match any keywords under keyword fallback are still included in the candidate additional suggestions (all included according to cost classification), and are listed in the installation report with the prompt "can be used through custom input"
- Within the same level, if there are multiple model suppliers, models from well-known suppliers (anthropic, openai, google, deepseek) will be listed first

##### Step 4: Level-by-level interactive selection

```
Question: "Select a model for a low-cost Agent (chapter-extractor, consistency-checker, story-explorer):"
Options:
  - provider/model-id
  - provider/model-id
- Custom input (manually enter the full model ID, ID misspellings will not be revealed until runtime)
- Skip, use master model (cost may be higher)
```

```
Question: "Select a model for key agents in writing quality (narrative-writer, character-designer, story-researcher):"
Options:
  - provider/model-id
  - provider/model-id
- Custom input (do not use low-end models, it will affect the quality of the text; ID spelling errors will not be exposed until runtime)
- Skip, use master model (master model quality is usually sufficient)
```

**High end option structure:**

```
Question: "Select a model for the Commander Agent (story-architect):"
Options:
  - provider/model-id
  - provider/model-id
- Custom input (manually enter the full model ID, ID misspellings will not be revealed until runtime)
- Skip, use master model (cost may be higher)
```

rule:
- A maximum of 5 candidates can be displayed. If more than 5 candidates are displayed, they will be truncated and a prompt will be given "Please use custom input for more models". **AskUserQuestion will pop up at each level regardless of whether the number of candidates is 0**. The options include at least: candidate model (if any), `Customized input`, `Keep existing model` ("Keep existing model configuration" is cached to the agent's model, if not, this item will not be displayed), `Skip, use the main model`. A pop-up window will still pop up when the candidate is 0, and a corresponding warning will be given in the problem description + Unrated/undocumented models will be listed for reference - no longer silently skipping interactions (otherwise the user cannot reach the custom input).
- `Customized input`: The user enters the complete ID of `provider/model-id`; before writing, it is verified to be a single line, no control characters, matching `^[A-Za-z0-9._-]+/[A-Za-z0-9._:+-]+$`, if not matched, it will prompt to re-enter or choose to skip.
- `Keep existing model`: Write back the agent model cached by "Keep existing model configuration" (keep the user's last configuration when redeploying), not counted as "skipping".
- `Skip, use main model`: clear explicitly - do not write the `model:` of the agent, the agent inherits the main model. If you want to keep the last configuration, please select `Keep existing model`.
- When the number of candidates at each level is 0, a hint will be given in the question description:
- Low end: "No low-cost model detected, these 3 agents will use the main model, the cost may be higher"
- Mid-range: "No matching mid-range model is detected. Narrative-writer, character-designer, story-researcher will use the main model. If the quality of the main model is sufficient, this configuration is reasonable; if you need to reduce costs, please use custom input to specify a mid-range model that is not lower than the quality of the main model, or choose from the unclassified models below."
- high-end: "No high-end model detected, story-architect will use main model"

##### Step 5: Write model field

Corresponding to the agent file selected by the user (`.opencode/agents/*.md`, deployed before this step by the OpenCode agents deployment step in the deployment manifest), insert `model:` as a top-level field with zero indentation at the end of frontmatter and before closing `---` (do not insert `permission:` inside the indented block of a multi-line map). Use quotes when the value contains YAML special characters to ensure that the frontmatter is not destroyed:

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

- If the agent file already has a `model:` field (redeployment scenario), replace the value of the top-level `model:` without adding a duplicate key
- `Keep existing model`: Write back the agent model cached by "Keep existing model configuration"
- `Skip, use main model`: do not write the `model:` field
- Detection failed/timed out, and did not reach the level of this step: use "Keep existing model configuration" to cache backfill `model:` to avoid replace erasing the user's last configuration

### Step 6: Merge Hooks and register them in settings.local.json

1. Detect Python according to existing cross-platform rules: `for PYBIN in python3 python py; do "$PYBIN" -c "" 2>/dev/null && break; done`; stop when no interpreter is available, no handwriting or simplified merging.
2. Call `"$PYBIN" "{story-setup skill directory}/scripts/merge-claude-settings.py" --existing "{project}/.claude/settings.local.json" --template "{story-setup skill directory}/references/templates/settings-hooks.json" --output "{project}/.claude/settings.local.json"`.
3. The helper will remove all historical registrations of known story-setup hooks, and then append the current template; therefore matcher/timeout/if can be upgraded with the version, while user hooks and unknown top-level fields mixed in the old block will remain intact. After writing, parse the JSON, verify that one copy of the template command and the user configuration are still there, and then run the helper again to compare the file bytes to confirm idempotence.

### Codex hooks.json merging algorithm (when target_cli contains codex)

Codex project hooks are deployed to `.codex/hooks.json`; running scripts are deployed to `.codex/hooks/story_codex_hook.py`, `run-story-hook.sh`, `run-story-hook.cmd`. JSON is only responsible for locating the project root and delivering events, and interpreter detection is handled uniformly by the platform launcher.

### Antigravity deployment algorithm (when target_cli contains antigravity)

Antigravity 2.0 uses the project `.agents/` customization root. Deploy Skills, Always-On Rule, 7 custom subagents and workspace Hooks; do not modify `~/.gemini/` under user home.

| Level | Matching keywords | Corresponding Agent |
|------|-----------|-----------|
| Low-end | `haiku`, `flash`, `mini`, `nano`, `lite` | chapter-extractor, consistency-checker, story-explorer |
| Mid-range | `sonnet`, `plus` | story-researcher, narrative-writer, character-designer |
| 高端 | `opus`, `pro`, `ultra`, `max` | story-architect |

按 低端 → 中端 → 高端 顺序，每级用 AskUserQuestion 让用户选择。

**低端选项结构：**

**中端选项结构：**

1. Locate the current story-setup skill directory, read `references/codex/hooks/hooks.json` as the only current template, and read the project `.codex/hooks.json` (it will be treated as an empty object if it does not exist).
2. Detect available Python according to existing cross-platform rules: `for PYBIN in python3 python py; do "$PYBIN" -c "" 2>/dev/null && break; done`; stop when no interpreter is available, do not handwrite or simplify JSON merging.
3. Call `"$PYBIN" "{story-setup skill directory}/scripts/merge-codex-hooks.py" --existing "{project}/.codex/hooks.json" --template "{story-setup skill directory}/references/codex/hooks/hooks.json" --output "{project}/.codex/hooks.json"`. This helper will identify three types of management identities: the old direct call `story_codex_hook.py`, the current `run-story-hook.sh` and `run-story-hook.cmd`, first remove all known management registrations, and then append the current template.
4. 保留用户已有的非 story-setup hooks、matcher 块与未知顶层字段。重复执行必须幂等；禁止再按原始 `command` 字符串追加去重，否则 v17 直调命令会与 v18 launcher 双重注册。
5. 写入后解析 JSON 验证：旧直调 `story_codex_hook.py` 命令数为 0，当前模板 6 个注册各存在且仅存在一次，用户 hook 与未知顶层字段仍在。然后提示用户：项目 `.codex/` 层需要被 Codex trust，非 managed command hooks 还需要在 `/hooks` 中 review/trust 后才会运行；Windows 下走 `commandWindows`，launcher 从当前目录向上定位项目 `.codex/hooks/`，与 POSIX 路径的嵌套目录行为一致。

1. Find the 13 known skill directories (`browser-cdp` and `story*`) of the current skill package, and call `deploy-antigravity-skills.py --source "{current skill package root}" --dest "{project}/.agents/skills"` for atomic materialization. The helper only replaces 13 known names, preserves the user's other skills, and is no-op when the source and target are on the same realpath. The target must be a **real directory**, do not create a new top-level `.agents/skills → ../skills` symlink: Antigravity 2.0 project deployments use real directories as supported paths.
   - 若已有 `.agents/skills` 是 symlink，helper 必须先停止且不沿链接写入。用 AskUserQuestion 说明：迁移会把链接当前可见的所有 skills 复制到新的项目内真实目录、只更新 13 个 oh-story 名称、保留链接目标原样，但会把 symlink 本身替换成目录；这可能形成较大的 git diff。只有用户明确同意后才加 `--migrate-symlink` 重跑，拒绝则停止 Antigravity 部署并报告未获得完整支持。这个确认不得被“多端部署”或已有 Codex symlink 跳过。
2. 按上方「部署 Antigravity Agents」运行生成器，原子更新 `.agents/agents/` 中 7 个已知 `.agents/agents/agent-name/agent.md` 定义（`agent-name` 为实际名称）并保留其他用户 agent；不从用户 home 搬运 agent。
3. Copy `references/antigravity/rules/oh-story.md` to `.agents/rules/oh-story.md`, verify `trigger: always_on` and the file is smaller than Antigravity’s 12,000 character limit. This rule is responsible for skill routing, writing hard constraints, and recovery after compaction; Antigravity IDE does not use the root `AGENTS.md` as a workspace rule, so do not use the AGENTS template instead.
4. Copy `references/antigravity/hooks/story_antigravity_hook.js` and `story_hook_core.js` in the same directory to `.agents/hooks/`, and verify `node --check`. The hook command uses `.agents/` (the directory where `hooks.json` is located) as the working directory. `hooks/story_antigravity_hook.js` must be used and cannot be written as `.agents/hooks/...`. The shared core must be consistent with the Claude/OpenCode/ZCode source bytes.
5. 合并 `references/antigravity/hooks/hooks.json` 到 `.agents/hooks.json`：按跨平台规则探测 Python 3，调用 `merge-antigravity-hooks.py {项目}/.agents/hooks.json {skill目录}/references/antigravity/hooks/hooks.json`。helper 只替换顶层 `oh-story` named group，保留其他用户 hook groups；写后复跑并比较字节确认幂等。禁止把 Claude/Codex 的外层 `{ "hooks": ... }` schema 写入 Antigravity。
6. Verify event boundaries: only register `PreToolUse`, `PostToolUse`, `PreInvocation` and `Stop`. PreToolUse must output `decision` for each call; PostToolUse must only output `{}`, and the text findings are temporarily stored through the session `artifactDirectoryPath` and injected by the next PreInvocation; if the model is ready to end directly, Stop is forced to continue at most once to avoid infinite loops. Antigravity external hooks do not have SessionStart/PreCompact/PostCompact. The first context is injected by PreInvocation with `invocationNum=0`, and after compact, `Tracking/Context.md` is forced to be read by Always-On Rule.
7. `.story-deployed` 的 `target_cli` 写 `antigravity` 或多端组合，`references_dir` 写 `.agents/skills/story-setup/references/agent-references`。安装报告提示新开 conversation 使 Skills/Rules/Agents/Hooks 重新扫描；同时明确 Node 是 hook 运行时依赖。

Antigravity IDE and interactive `agy` share this set of workspace `.agents/` products, but they still need to separate the actual machine smoke test. Do not rely on which `~/.gemini/*` directory `npx skills add -g` currently writes global skills to; the support commitment of `story-setup` only covers the real directory deployment in the above project.

Plugin installation does not go through this algorithm: the warehouse root `.zcode-plugin/plugin.json` directly exposes the same set of Skills/Commands/Hooks. Plugin Skills has a lower priority than workspace `.zcode/skills`; when both exist at the same time, the project snapshot takes priority. To upgrade the project snapshot, you need to re-run `$story-setup`. **Hooks can only be registered once**: The plug-in manifest and workspace `.zcode/config.json` register the same batch of events. Once the plug-in is installed, do not merge the hooks of `config.json.patch` into `.zcode/config.json` (see the mutual exclusion of hooks in step 4 of the algorithm above), otherwise PreToolUse/PostToolUse will be double-triggered; when the plug-in is present, the plug-in manifest will be used as the hooks The only registration source.

### OpenClaw skills-only deployment algorithm (when target_cli contains openclaw)

OpenClaw Phase 1 only deploys skills and does not deploy OpenClaw agents/hooks/plugin.

Reasonix (DeepSeek-Reasonix CLI) currently only deploys skills and `AGENTS.md`, and does not deploy Reasonix hooks/custom agents (hook I/O contracts and sub-agent behaviors lack verifiable real CLI and are left to subsequent stages).

1. Read all story skill directories containing `SKILL.md` under the current `skills/` of the warehouse (13: `browser-cdp` and `story*`) to the target project `skills/{skill-name}/`; only replace these known skill directories managed by story-setup, and retain other user directories.
2. Create a relative symlink of `.agents/skills → ../skills` at the project root (the skill root shared with Codex), so that Reasonix can discover these skills when natively scanning `.agents/skills`; if it already points to the symlink of `skills/`, it will be retained. If it is occupied as a normal directory, it will not be overwritten and a prompt will be reported during the installation. If symlink is not enabled on Windows, skip this step and go to the `reasonix plugin install` of the root `reasonix-plugin.json` instead.
3. Copy `skills/story-setup/references/reasonix/AGENTS.md.tmpl` to the project `AGENTS.md`, and merge according to "AGENTS.md Merge Strategy".
4. The `target_cli` of `.story-deployed` is written to `reasonix` or multi-port combination; the `references_dir` is written to `skills/story-setup/references/agent-references` for Reasonix.
5. See Step 12 of Phase 3 for the installation report prompt items.

### General Web AI/Other Agent deployment algorithms (when target_cli contains generic)

The universal path is oriented to environments that can read project files such as NarraFork, Web AI, and custom Agents. It only deploys universal files and does not declare the platform's native hooks/agents capabilities.

1. Copy all story skill directories containing `SKILL.md` under the current `skills/` of the warehouse (13: `browser-cdp` and `story*`) to the target project `skills/{skill-name}/`; only replace these known skill directories managed by story-setup, and retain other user directories.
2. Copy `skills/story-setup/references/generic/AGENTS.md.tmpl` to the project `AGENTS.md`, and merge according to "AGENTS.md Merge Strategy".
3. The `target_cli` of `.story-deployed` is written to `generic` or multi-terminal combination; the `references_dir` is written to `skills/story-setup/references/agent-references` for generic.
4. See Step 11 of Phase 3 for the installation report prompt items.

### Step 7: Create deployment tags

## Phase 3: Verify installation

### ZCode 部署算法（target_cli 含 zcode 时）

ZCode 首版部署 Skills、Commands、AGENTS.md 和支持事件内的 Hooks；不部署 `.zcode/agents` 或 `.zcode/rules`。

1. 复制仓库当前 `skills/` 下 13 个包含 `SKILL.md` 的目录到 `.zcode/skills/{skill-name}/`；仅替换这些已知目录，保留用户其他 Skills。
2. Copy `references/zcode/commands/*.md` to `.zcode/commands/`; only replace 13 commands with the same name, and retain the user's other Commands.
3. Copy `references/zcode/hooks/story_zcode_hook.js` and `references/zcode/hooks/story_hook_core.js` to `.zcode/hooks/`.
4. 读取 `references/zcode/config.json.patch` 和现有 `.zcode/config.json`（如只有根 `zcode.json`，仍创建 `.zcode/config.json` 承载 oh-story 项目 Hooks，不改写根文件）：
   - 保留用户所有未知字段、MCP、plugins、skills/commands disable overrides；
   - **hooks 互斥（避免双触发）**：若本项目经已安装的 oh-story 插件运行（marketplace 安装，仓库根 `.zcode-plugin/plugin.json` 的 `hooks.json` 已全局注册 SessionStart/PreToolUse/PostToolUse），则**跳过**下面把 `config.json.patch` 的 `hooks` 块合并进 `.zcode/config.json`——插件 manifest 已注册这批 hooks，再合并会让同一事件跑两遍（PreToolUse 拦两次、PostToolUse 注入两次）。只有未装插件（直接克隆 / 手动导入 references）时才合并 hooks。不确定时以「ZCode 是否已通过本插件注册这套 hooks」为准；skills/commands/hook 文件/AGENTS 与 config 的非 hook 字段两条路径都照常部署。
   - 合并 hooks（仅未装插件时）：设置 `hooks.enabled: true`；用户已有更大的 `timeoutMs` 时保留，否则取模板值；对 `hooks.events` 的 SessionStart、PreToolUse、PostToolUse 按 `event + matcher + process command + args` 去重追加；不复制 ZCode 不支持的 PreCompact、PostCompact、SessionEnd、SubagentStop、Notification。
5. Write `references/zcode/AGENTS.md.tmpl` to the root `AGENTS.md` according to the "AGENTS.md merge strategy".
6. The `target_cli` of `.story-deployed` is written to `zcode` or multi-port combination, and the `references_dir` is written to `.zcode/skills/story-setup/references/agent-references`.
7. The installation report clearly states: ZCode 3.3.4’s project/plugin custom agents are not executed, and all professional roles use solo/direct; the system requires an available `node` command to run the project Hook.

1. Read all story skill directories containing `SKILL.md` under the current `skills/` of the warehouse (13: `browser-cdp` and `story*`).
2. Write to the target project `skills/{skill-name}/`, replacing only the known skill directories managed by these story-setup; retain the user's other directories under `skills/`.
3. 每个 `SKILL.md` 必须满足 OpenClaw frontmatter 约束：`name` / `description` 是单行键值，`metadata` 是单行 JSON 对象且含 `metadata.openclaw`。
4. Copy `skills/story-setup/references/openclaw/AGENTS.md.tmpl` to the project `AGENTS.md` and click "AGENTS.md Merge Strategy" to merge.
5. `.story-deployed` 的 `target_cli` 写入 `openclaw` 或多端组合；`references_dir` 对 OpenClaw 写 `skills/story-setup/references/agent-references`。
6. 安装报告提示项见 Phase 3 第 10 步。

### Reasonix skills-only 部署算法（target_cli 含 reasonix 时）

- Create `.story-deployed` file (sentinel file)
- Write the following fields (YAML `key: value` format, hook is read using `references/templates/hooks/lib/sentinel.sh`):
  ```
  deployed_at: <date -u +"%Y-%m-%dT%H:%M:%SZ">
  agents_version: 29
  setup_skill_version: 1.2.10
target_cli: claude-code (or opencode, codex, antigravity, zcode, openclaw, reasonix, generic, or any combination thereof)
  resolver_strategy: project-local-skill-reference
references_dir: .claude/skills/story-setup/references/agent-references (Codex writes .codex/skills/...; Antigravity writes .agents/skills/...; ZCode writes .zcode/skills/...; OpenClaw/Reasonix/generic writes skills/...; multiple ends are separated by commas)
  ```
- This file is used by session-start.sh and writing skills to detect deployment status and avoid repeated prompts
- target_cli 含 claude-code 时，同时创建一次性标记文件 `.claude/.agents-pending-restart`（空文件即可）。session-start.sh 在下一个会话启动时据此确认 agents 已随新会话注册，并自动删除该标记——用来向用户确认「重启已生效」。ZCode 不创建该标记，因为它不部署项目 agents。
- 如果 `.story-deployed` 已存在但 `agents_version` 缺失、非整数或小于 `29`，按本次流程更新 hooks/agents/rules/reference bundle（具体变更见 `UPGRADING.md`）；大于 `29` 时已在 Phase 1 停止，不得降级覆盖

1. 验证 hooks 注册：
   - 检查 `.claude/settings.local.json` 中的 hooks 字段是否正确
   - 检查 `.claude/hooks/` 下的脚本是否存在且有执行权限
   - 检查 `.claude/hooks/lib/common.sh` 与 `.claude/hooks/lib/sentinel.sh` 是否存在
2. 验证 rules 路径：
   - 检查 `.claude/rules/` 下的规则文件是否存在且包含 `paths` frontmatter
3. 验证 agents：
   - 检查 `.claude/agents/` 下的 7 个 agent 定义文件是否存在
4. 验证 agent reference bundle：
   - 检查 `.claude/skills/story-setup/references/agent-references/` 下 reference 文件完整
   - 检查所有 `story-setup/references/agent-references/<file>.md` 都能解析到 deployed bundle
5. 验证部署标记：
   - 检查 `.story-deployed` 是否存在且包含时间戳、`agents_version: 29`、`setup_skill_version: 1.2.10`、`target_cli`、`resolver_strategy`、`references_dir`
6. 输出安装报告：
   - 列出所有已部署的文件
   - 列出需要注意的事项（如已有配置已合并）
    - **⚠️ 重启提示（必须醒目输出）**：本次部署写入了 `.claude/agents/`，但这些 custom agent 只在「会话启动」时才会被 Claude Code 注册成 `subagent_type`。**请新开一个 Claude Code 会话再开始写作**，否则当前会话里 story-review / story-long-write 等想 spawn `story-architect`、`narrative-writer` 等时会拿到「subagent_type 不可用」并降级 solo（单视角，失去多 agent 协作）。判断是否生效：新会话里跑 `/story-review`，报告头若是 `Effective Mode: full/lean` 即注册成功；若是 `Fallback: ... -> solo` 说明还在旧会话或未注册。
    - 重启后即可使用 `/story-long-write` 或 `/story-short-write`
    - 如果执行了「配置 OpenCode Agent 模型」，输出 Agent 模型配置摘要：
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
    - 如果自动检测失败（`opencode models` 不可用），输出手动配置指南：
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
7. 验证 opencode 部署（仅当 target_cli 含 opencode 时）：
    - 检查 `.opencode/agents/` 下的 7 个 agent 定义文件是否存在，且 frontmatter 包含 `mode: subagent` 和 `permission` 字段
    - 检查 `.opencode/plugins/story-hooks.ts` 是否存在
    - 检查 `.opencode/plugins/lib/story_hook_core.js` 存在且 `node --check` 通过（story-hooks.ts import 之，与 `.zcode` 副本字节一致的共享写正文守卫核；置于 `lib/` 子目录以避开 OpenCode 单层 `.opencode/plugins/*.js` 插件自动发现）
     - 检查 `.opencode/commands/` 下的 13 个 command 文件是否存在
    - 检查 `skills/story-setup/references/agent-references/` 下 reference 文件完整且数量与源目录一致
    - 检查 `opencode.json` 的 `plugin` 数组是否包含 story-hooks 条目
    - 检查 `.git/hooks/pre-commit` 是否存在且有执行权限（Windows 上跳过执行权限检查）
    - 检查 `.opencode/agents/` 下 agent 文件 frontmatter 可被 YAML 解析、`model:`（如有配置）是合法顶层标量，而非仅 grep 到 `model:` 子串
8. 验证 Codex 部署（仅当 target_cli 含 codex 时）：
    - 检查 `AGENTS.md` 含 Codex story skill routing sections
    - 检查 `.codex/agents/` 下 7 个 `.toml` agent 定义文件存在并可解析
- Check that `.codex/hooks.json` exists and the JSON is valid, Unix `command` is only started through `run-story-hook.sh`, Windows `commandWindows` is only started through `run-story-hook.cmd`; there is no registration to directly call `story_codex_hook.py`
   - 检查 `.codex/hooks/story_codex_hook.py`、`run-story-hook.sh`、`run-story-hook.cmd` 存在，Python 语法有效，POSIX/Windows launcher 能从嵌套 cwd 定位项目根
    - 检查 `.codex/skills/story-setup/references/agent-references/` 下 reference 文件完整且数量与源目录一致
- The installation report must prompt: Codex requires the trust project `.codex/` configuration layer, and review/trust non-managed hooks in `/hooks`; open a new Codex session after deployment to make custom agents effective; if the current runtime still returns `unknown agent_type`, downgrade to solo/direct according to the fallback rules of each skill
9. 验证 Antigravity 部署（仅当 target_cli 含 antigravity 时）：
    - 检查 `.agents/skills/` 下 13 个 story skills 为真实目录且 `SKILL.md` 可读；`.agents/skills/story-setup/references/agent-references/` 完整
    - 检查 `.agents/agents/` 下 7 个 Markdown agent 可解析，名称、模型档、官方工具白名单、只读边界与 `.agents/skills/` reference 前缀正确
- Check that `.agents/rules/oh-story.md` is `trigger: always_on` and does not exceed 12,000 characters
    - 检查 `.agents/hooks.json` 有效、顶层 `oh-story` group 恰有 PreToolUse/PostToolUse/PreInvocation/Stop，用户 hook groups 保留；检查 `.agents/hooks/story_antigravity_hook.js` 与 `story_hook_core.js` 语法有效
    - 用 fixture 验证：PreToolUse 缺纲/追踪时 deny、普通写入 allow、commit advisory；PostToolUse stdout 恒为 `{}` 且把正文 findings 写进 session artifact；下一次 PreInvocation 注入 findings；Stop 对未处理 findings 最多 continue 一次；干净正文清除 pending state
    - 安装报告必须提示：新开 Antigravity conversation 刷新 customization；Hooks 依赖 PATH 中的 `node`；外部 hook API 没有 PreCompact/PostCompact，compact 恢复由 Always-On Rule 读取 `追踪/上下文.md`；IDE 与交互式 `agy` 仍建议分别实机 smoke test；`agy 1.1.22 -p` 每次 headless 启动都可能在静默鉴权前扫描 workspace，鉴权后不重载 custom agents/hooks，因此当前不在支持面内，可能报 `subagent not found` 或回退写入 `~/.gemini/antigravity-cli/scratch/`；命令行写作从项目目录进入交互式 `agy`，确认 `/skills`、`/agents`、`/hooks` 已发现 oh-story 后再发任务，测试后检查 scratch 无意外小说产物
10. 验证 ZCode 部署（仅当 target_cli 含 zcode 时）：
    - 检查根 `AGENTS.md` 含 ZCode `$story-*` 路由、大纲守卫和 solo/direct fallback
    - 检查 `.zcode/skills/` 下 13 个 Skills 与 `.zcode/commands/` 下 13 个 Commands，验证 frontmatter 和命名
    - 检查 `.zcode/hooks/story_zcode_hook.js`、`.zcode/hooks/story_hook_core.js` 存在且 `node --check` 通过
    - 检查 `.zcode/config.json` JSON 有效，并按「ZCode 部署算法」第 4 步的 hooks 互斥分支校验：未装 oh-story 插件时，`hooks.enabled=true`、仅注册 ZCode 支持事件、所有 `process` args 指向项目 Hook；已装 oh-story 插件（`.zcode-plugin/plugin.json` 已全局注册这批 hooks）时，改为校验 `.zcode/config.json` 不含（或已移除）这批 oh-story hooks 注册——**不得**为了让校验通过而把 `config.json.patch` 的 hooks 块合并回去，否则同一事件双触发
    - 检查 `.zcode/skills/story-setup/references/agent-references/` 完整且所有 reference 路径可解析
    - 用 fixture 调用 SessionStart、PreToolUse deny/allow、PostToolUse，确认无发现时 stdout 为空、有输出时符合 ZCode 严格 JSON
    - 安装报告必须提示：ZCode 3.3.4 不执行项目/plugin custom agents，full/lean 多 Agent 请求会稳定降级 solo/direct；Hook 依赖 PATH 中的 `node`；部署后新开 ZCode session 刷新 Skills/Commands/AGENTS.md
11. 验证 OpenClaw 部署（仅当 target_cli 含 openclaw 时）：
    - 检查 `AGENTS.md` 含 OpenClaw story skill routing sections
    - 检查 `skills/` 下 13 个 story skill 目录存在，且每个 `SKILL.md` 包含单行 `name`、单行 `description`、单行 JSON `metadata.openclaw`
    - 检查 `skills/story-setup/references/agent-references/` 下 reference 文件完整且数量与源目录一致
    - 安装报告必须提示：OpenClaw Phase 1 是 skills-only；未部署 OpenClaw agents/hooks，运行时硬拦截不可用，写正文前大纲守卫、commit 提醒、session/compact 自动注入只作为 skill 内软约束；OpenClaw 在 session 启动时 snapshot eligible skills，部署后如命令/skills 未出现，需新开 OpenClaw session 或等待 skills watcher 刷新
12. 验证通用 Web AI / 其他 Agent 部署（仅当 target_cli 含 generic 时）：
- Check `AGENTS.md` for common story skill routing sections
    - 检查 `skills/` 下 13 个 story skill 目录存在，且每个 `SKILL.md` 可读
    - 检查 `skills/story-setup/references/agent-references/` 下 reference 文件完整且数量与源目录一致
- The installation report must indicate: generic does not deploy platform-specific hooks/custom agents; hard interceptions such as outline guards, commit reminders, session/compact injection, and multi-agent collaboration are all executed according to soft constraints within the skill or solo/direct fallback
13. Verify Reasonix deployment (only if target_cli contains reasonix):
    - 检查 `AGENTS.md` 含 Reasonix story skill routing sections 与 solo/direct fallback 说明
    - 检查 `skills/` 下 13 个 story skill 目录存在，且每个 `SKILL.md` 可读
- Check that the project `.agents/skills` is a symlink pointing to `skills/` (POSIX; enables Reasonix to scan natively to discover the skill); when Windows does not build a symlink, instead confirm that the root `reasonix-plugin.json` can be used for `reasonix plugin install`
    - 检查 `skills/story-setup/references/agent-references/` 下 reference 文件完整且数量与源目录一致
    - 安装报告必须提示：Reasonix 当前是 skills-only；未部署 Reasonix hooks/custom agents，写正文前大纲守卫、commit 提醒、session/compact 自动注入只作为 skill 内软约束，涉及专业 Agent 的 Skill 走 solo/direct fallback；可用 `reasonix doctor capabilities` 校验 skill 发现，部署后如未显示新 skills，新开 Reasonix session 或走根 `reasonix-plugin.json` 原生 plugin 安装

---

## Template placeholder

| Placeholders | Replacement rules | Examples |
|--------|----------|------|
| `{Project name}` | User project name or directory name | "Jianlai", "Dark Guard" |
| `{Book title}` | Book title directory name (consistent with the directory) | Same as `{Project name}`, or user-defined |
| `{Target platform}` | Target publishing platform | Qidian, Tomato, Jinjiang, Zhihu Yanyan |
| `{author name}` | User pen name or nickname | Use "author" if not specified |

Remove the curly braces when replacing. If the user does not specify a project name, the current directory name is used. Unspecified placeholders are left unchanged and not replaced.

## CLAUDE.md merge strategy

---

---

Calling syntax at each end: Claude `/name`, Codex/ZCode `$name`, Antigravity through `/skills` to browse or directly name the skill, OpenClaw `/skill name`, Reasonix / generic to directly name the skill.


When the user already has CLAUDE.md, merge according to marker/section:
1. Prioritize the identification of story-setup management block tags (if the old project already has tags, only replace the content in the tags)
2. When there is no mark, read the user's existing CLAUDE.md and divide it into a section map according to the `##` title.
3. 读取模板 CLAUDE.md.tmpl，同样切分
4. The standard sections in the template (Skill routing table, file structure, collaboration rules, recovery context after Compact) **overwrite** the user's section with the same name
5. User-unique sections (custom content) are **reserved** unchanged
6. 未知冲突用 AskUserQuestion 让用户选择保留哪个版本

## AGENTS.md 合并策略（OpenCode / Codex / ZCode / OpenClaw / Reasonix / generic）

用户已有 AGENTS.md 时，按 marker/section 合并：
1. Prioritize the identification of story-setup management block tags (if the old project already has tags, only replace the content in the tags)
2. When there is no mark, read the user's existing AGENTS.md and divide it into a section map according to the `##` title.
3. OpenCode 使用 `skills/story-setup/references/opencode/AGENTS.md.tmpl`；Codex 使用 `skills/story-setup/references/codex/AGENTS.md.tmpl`；ZCode 使用 `skills/story-setup/references/zcode/AGENTS.md.tmpl`；OpenClaw 使用 `skills/story-setup/references/openclaw/AGENTS.md.tmpl`；Reasonix 使用 `skills/story-setup/references/reasonix/AGENTS.md.tmpl`；通用 Web AI / 其他 Agent 使用 `skills/story-setup/references/generic/AGENTS.md.tmpl`
4. Standard sections in the template (Skill routing table, file structure, collaboration rules, recovery context after Compact) overwrite the section with the same name; user-unique sections are reserved
5. 多端同时部署时，Codex/OpenCode/ZCode/OpenClaw/Reasonix/generic 共同可用的通用段落只保留一份；工具特有说明以小节区分，避免互相覆盖

## 重新部署

- `.story-deployed` 不存在 → 全新安装，Phase 2 全部执行
- `.story-deployed` 存在且 `agents_version: 29` → 提示已部署，AskUserQuestion 确认是否重新部署；提示里写明重新部署只用当前本地 skill 包刷新项目文件，skill 本身的更新走 `npx skills add` 或 marketplace
- `.story-deployed` exists but `agents_version` is missing, non-integer or less than `29` → prompts that update is required, re-execute Phase 2 to overwrite agents/hooks/rules/reference bundle, CLAUDE.md / AGENTS.md / settings.local.json / .codex/hooks.json / `.agents/hooks.json` / .zcode/config.json adopt the merge strategy
- `.story-deployed` 存在且 `agents_version` 大于 `29` → 当前 skill 版本过旧，停止并提示先更新 oh-story-claudecode；不覆盖项目中的更新部署

## 参考资料

| Documentation | Purpose |
|------|------|
| references/templates/hooks/ | 8 hook script templates + `story_hook_core.js` (shared implementation of text network/outline guard/continuity/commit detection, the same as OpenCode/ZCode) + `story_hook_cli.js` (node bridge for bash hook tuning) + `lib/common.sh`/`lib/sentinel.sh` (text cover) `check-prose-after-write.sh` is limited to PostToolUse Write/Edit; `cat>`/`tee`, etc. Bash writes the text by Codex Stop at the end of the round git scans the pocket, Claude/OpenCode's Bash only pre-guard) |
| references/antigravity/ | Antigravity 2.0 Always-On Rule, named-group hooks template and I/O adapter; after the text is written, findings are bridged to PreInvocation/Stop via session artifact |
| references/zcode/ | ZCode AGENTS、13 Commands、workspace config patch 与严格 JSON Hook runner |

## 流程衔接

**流水线：** 部署
**Position:** Initialization (frontmost)

| Timing | Jump to | Command |
|---|---|---|
| 部署完成，开始写作 | story-long-write / story-short-write | `/story-long-write` 或 `/story-short-write` |
| 导入已有小说做拆解 | story-import | `/story-import` |
| 需要浏览器登录态（扫榜/拆文取原文） | browser-cdp | `/browser-cdp`；generic 需平台允许本地脚本/浏览器控制 |