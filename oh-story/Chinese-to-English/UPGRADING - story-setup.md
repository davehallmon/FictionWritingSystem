# Upgrade Guide

## Current Version

- `setup_skill_version: 1.2.10`
- `agents_version: 29`

If `.story-deployed` lacks either field, or if `agents_version` is missing, not an integer, or below `29`, treat the deployment as requiring an update. Rerun `/story-setup` directly (use `$story-setup` in Codex; use `/skills` or name the skill in natural language in Antigravity). Do not maintain incremental runtime compatibility with historical templates. If the project’s `agents_version` is greater than `29`, the local story-setup is older than the project: update oh-story-claudecode first and do not overwrite it by downgrading to v29. See `CHANGELOG.md` at the repository root for historical version changes.

## Upgrade Strategy

| Strategy | Use case | Behavior |
|------|----------|------|
| Overwrite deployment | New project | Write the current agents/hooks/rules/reference bundle |
| Merge deployment | Existing project | Replace story-setup-managed files and merge user-maintained files |
| Manual update | Update only specific files | Recommended only for maintainers familiar with the deployment contract |

Always rerunning story-setup is recommended so the deployer can process files by owner class.

### Self-Nesting Residue

In the deployment manifest, Source is relative to the skill package and Target is relative to the project root. On skills-only clients, these two base directories may coincide; when loaded through a symlink such as `.agents/skills → ../skills`, textually different paths may still point to the same directory. Before copying, the deployer rejects the same object and recursive copies where “the target is inside the source directory” using realpath / samefile semantics, then removes existing `agent-references/agent-references/` (possibly nested multiple times) or `skills/story-setup/skills/` residue.

The OpenClaw / Reasonix / generic skill copies live inside the project’s `skills/`; reruns execute that project-local copy, which cannot clean itself. First delete the directories above manually. To update the text of the project-local skills themselves, also update oh-story-claudecode and then overwrite these 13 directories under the project’s `skills/` with the new package.

## File Ownership

### Managed by story-setup; Replaceable

These files are managed by story-setup and contain no user customization:
- `.claude/hooks/` — all hook scripts and `lib/` helper library
- `.claude/agents/` — all agent definitions
- `.claude/rules/` — all path-scoped rules
- `.claude/skills/story-setup/references/agent-references/` — copies of Agent references
- `.agents/skills/{13 known skills}/`, `.agents/agents/agent-name/agent.md` (7 known `agent-name` values), `.agents/rules/oh-story.md`, and `.agents/hooks/{story_antigravity_hook.js,story_hook_core.js}` — actual in-project Antigravity Skills, generated Agents, Always-On Rule, and Hook runtime; preserve other user Skills/Agents in the same directories
- `skills/{13 known skills}/` — project-local skill copies for OpenClaw / Reasonix / generic; overwrite only known oh-story names
- `.zcode/skills/{13 known skills}/` and `.zcode/commands/{13 known commands}.md` — overwrite only known oh-story names
- `.zcode/hooks/story_zcode_hook.js` — ZCode-specific Hook runner

### Jointly Maintained by the User and story-setup; Merge Managed Blocks Only

These files may contain user customization:
- `CLAUDE.md` — merge by marker/section; preserve user-only sections
- `.claude/settings.local.json` — identify story hooks by command; migrate existing managed commands to the current template’s event/matcher/timeout/if (for example, v25’s Bash manuscript pre-guard), while preserving other user hooks and configuration
- `AGENTS.md` — merge ZCode/OpenCode/Codex/OpenClaw/generic by marker/section
- `.zcode/config.json` — deduplicate and merge oh-story Hooks only by event, matcher, and process args; preserve other fields
- `.agents/hooks.json` — replace only the top-level `oh-story` named group; preserve other user hook groups

### User State; Never Overwrite

- `{书名}/正文/`, `正文.md`
- `{书名}/设定/`, `大纲/`, `追踪/`
- `.active-book`

## Current v29 Contract

- The narrative-writer template removes per-paragraph quotas: “expand subevents” becomes “develop progression units,” and “expanded subevents total ≥100-150 characters” is removed. Emotional-string theory no longer requires “pluck at least once in every section”; task, reasoning, craft, or waiting chains may unfold continuously. Outputs for all three clients (Claude / OpenCode / Codex) are synchronized.
- The short-form reference bundle now determines length and pacing by scene function: `short-genre-formulas.md` removes fixed hook intervals, “500-800 characters per cathartic-fiction section,” and “one public humiliation every 3-5 sections”; `short-emotional-methods.md` removes fixed-interval emotional turns and humiliation beats; `short-suspense.md` no longer assigns a minimum suspense level to each section type; and `short-reversal.md` no longer requires one sweet moment per section in sweet-romance arcs.
- The section structure in `format-and-structure.md` no longer sets a universal minimum length or estimates “8-15 sections / total word count ÷ 1000.” Section length and count follow narrative responsibility, while the whole work is constrained by the user’s delivery range.

After redeployment, **start a new session** so custom agents and hooks are registered again.

## Historical v28 Contract

- `agent-reference-profiles.md` becomes story-architect’s sole source list; Agent templates no longer duplicate a second inventory. Deployment guards validate Common / Long / Short ownership, file existence, and out-of-table reads.
- Suspense, twist, and quality standards become profile-specific: long uses `long-suspense.md`, `long-reversal.md`, and `long-quality.md`; short uses the corresponding `short-*` files. `agent-quality.md` retains only the five cross-genre core dimensions.
- Long-form genre material changes to `long-genre-catalog.md` + `long-genre-mechanics.md`, and no longer places the short-form three-act structure in Common; short continues to use `short-genre-formulas.md`.
- `format-and-structure.md` serves only short/import/setup; long form moves to separate `long-format.md` rather than “reading only part of the same file.”
- Near-duplicate cross-Skill files register their source and reason for divergence in `derived_groups` within `shared-references.json`; the directory mirror manifest must cover every source-tree file.

After redeployment, **start a new session** so custom agents and hooks are registered again.

## Historical v27 Contract

- story-architect retains one Agent name but selects a `long` / `short` reference profile before every task, loading only common + assets for the current length. If it cannot decide, it explicitly returns unresolved rather than mixing both standards.
- story-architect conditionally consumes `plot-core-methods.md` for blocked plotting, plot loops, five-step climaxes, transitions, long-range anticipation, and daily-outline progression. The deployment guard rejects a reference without an Agent consumption chain.
- The long profile uses `genre-prose-cards.md` and `long-emotional-methods.md`; the short profile uses `short-genre-formulas.md`, `short-paragraph-hooks.md`, and `short-emotional-methods.md`. Long form no longer inherits short-form defaults such as 500-800 characters per section.
- The setup reference bundle’s profile files and semantic aliases are story-setup-managed assets. Redeployment replaces the old bundle, and a new session is required afterward.

After redeployment, **start a new session** so custom agents and hooks are registered again.

## Historical v26 Contract

- Adds Google Antigravity 2.0 project deployment: copies 13 real skills into `.agents/skills/`, deterministically converts 7 Claude agent sources to `.agents/agents/agent-name/agent.md` (`agent-name` is the actual name), and installs the `.agents/rules/oh-story.md` Always-On Rule.
- Antigravity Workspace Hooks use only official `PreToolUse`, `PostToolUse`, `PreInvocation`, and `Stop` events. The pre-write gate returns allow/deny directly; PostToolUse returns only `{}` per protocol; post-write manuscript findings pass through a session artifact to the next PreInvocation; Stop retries at most once.
- `.agents/hooks.json` atomically merges the top-level `oh-story` managed group without overwriting other user hook groups. Deployment does not write `~/.gemini/` or depend on global skill/symlink discovery. An existing `.agents/skills` symlink requires explicit confirmation before migration to a real directory; helpers never follow the symlink to write its target.
- Antigravity custom agents are called with `invoke_subagent` + matching `TypeName`; if the runtime lacks that capability, degrade according to existing solo/direct rules. The external Hook API has no PreCompact/PostCompact, so context recovery after compaction is enforced by the Always-On Rule reading `追踪/上下文.md`.

After redeployment, **start a new Antigravity conversation** so Skills, Rules, Agents, and Hooks are rescanned; smoke-test the IDE and interactive `agy` separately.

- Long-form word count is measured only through the `visible_chars_v1` runtime entry in `storyctl.py`. During writing, add only one pure `checkpoint`; final `chapter check` returns length and current blocking quality. Chapters inside the user’s band may be committed. For `under`, automatic additions are prohibited and the user chooses whether to accept natural length, change the target/outline, or abandon it. For `over`, perform at most one net-deletion compression without adding meaning, recheck, and defer to the user if still outside the band. Proceed to the next chapter only after tracking is committed.
- Manuscript Hooks for Claude, OpenCode, Codex, and ZCode no longer parse detailed outlines, count characters, or issue the old 90% deficit warning independently. Adapters retain only the manuscript-content gate, avoiding a second word-count standard alongside `storyctl`.
- narrative-writer and story-architect use an explicit word-count standard, no longer assign numeric quotas to individual plot beats, and never default to 3,000 characters when no target exists. The second half completes only approved unwritten beats and stops when they are complete rather than inventing independent plot to reach a count.
- During `story-import`, record the current-standard length of written chapters through `storyctl wordcount measure`. Stop explicitly if Python 3/CLI cannot run; do not replace measurement with model estimates.
- The workspace adds `.story/作者记忆/`: only stable preferences supported by verbatim evidence and confirmed by the author enter the author profile. Candidates, conflicting alternatives, and withdrawals retain audit records. It is isolated from per-book tracking; current instructions, book settings, and hard gates take precedence.
- If story-explorer encounters a registered benchmark whose primary artifacts are missing, it fails closed instead of silently switching to another book. Reference tables for narrative-writer, story-architect, and character-designer read conditionally by task to avoid listing without triggering.
- New detailed outlines use a five-column plot-beat table recording content, function, characters, constraints, and placement; per-beat word quotas no longer serve as manuscript-arrangement instructions. Existing outlines may continue daily writing; only new, completed, or revised outlines adopt the new format.
- Before copying, the deployer uses realpath / samefile to block source and target from being the same object or the target from being nested under the source, and removes known nested residue. Old project-local OpenClaw / Reasonix / generic copies must first be handled manually as described under “Self-Nesting Residue” on this page.

After redeployment, **start a new session** so custom agents and hooks are registered again.

## Historical v25 Contract

- Claude Code’s manuscript pre-guard is also registered for Bash: common redirection, `tee`, `touch`, `cp`, `mv`, and `install` writes to manuscript files reuse the shared JS core to identify targets and enforce outline/tracking gates. Quoted examples in read-only commands and mentions inside heredoc bodies do not block, and relative paths resolve from the hook `cwd`. This surface provides **static best-effort detection, not a shell sandbox**: paths indirected through environment variables, runtime-generated commands, and arbitrary unlisted file-writing programs cannot be identified reliably through static analysis; use Write/Edit for those writes. The Bash command surface depends on Node and fails open with an explicit warning if Node/shared-core errors occur; the pure-Bash fallback for Write/Edit/MultiEdit is unaffected.
- Codex Python and shared JS book-directory discovery now share a four-level limit under the project and prune hidden directories and `node_modules`, preventing unbounded SessionStart/Stop scans and cross-client discovery drift.
- narrative-writer and deployment references add the Gate B rule that ordinary nouns do not need quotation-mark emphasis; retain legitimate dialogue, direct quotation, book titles/code names, and in-world system-carrier text.
- narrative-writer’s tool allowlist adds `Bash`: word counts, sentence-length distribution, and rescans through `check-ai-patterns.js` and `check-outline-copy.js` all require deterministic values, and those rules become ineffective without the tool. Word count and sentence length must be measured; if Python / Node cannot be found, state “未完成机器验证” truthfully rather than claiming statistics or script execution.
- narrative-writer divides detailed-outline consumption into two parallel rules: content layer (implement each item independently; omit none and do not merge two into one sentence) and shape layer (choose placement/order/paragraphing; may scatter and reorder; do not march one item per paragraph). The shape half is synchronized into `story-long-write`’s spawn checklist.
- Detailed-outline “plot elaboration” adds the **refrain anchor sentence** field: list exact source wording line by line and state its placement. Write “无” if absent. Existing outlines without the field are treated as having no anchor and need not be retrofitted.

After redeployment, **start a new session** so custom agents and hooks are registered again.

## Current v24 Contract

- `.claude/rules/story-narrative.md` removes the red-line block “禁止 AI 腔.” That block loaded only under the three paths `拆文库/`, `对标/`, and `设定/`, never matched the manuscript directory, and its five rules were already covered by narrative-writer’s 7 Gates / prohibitions and the blocking rules in `check-ai-patterns.js`.
- `.claude/rules/story-format.md` changes the dialogue-tag rule from “禁止「他说」「她道」” to “避免对话标签机械化”: replace frequent or formulaic tags with action/context, while retaining occasional ordinary “said.” Previously this file was the only place in the repository that treated ordinary “said” as a violation; it conflicted with 11 other standards including `format-and-structure.md`, and it was the file that loaded for the `正文/` path.
- `.claude/agents/narrative-writer.md` is reduced by about 19%: removes review checklists duplicated by the 7 Gates / prohibitions (story-review injects the full rubric when spawning), specific word-count expression checks during manuscript drafting (moved to review), and repeated statements about `……`/`——`, blank lines between paragraphs, and chapter-metadata regexes. The writing rules are not relaxed; Gates A-G and prohibitions remain unchanged.
- `.claude/hooks/guard-outline-before-prose.sh` adds a tracking-checkpoint gate in the same order as OpenCode / ZCode / Codex: writing manuscript is blocked if tracking state is missing, schema is not 4, the continuation state-card revision differs from state, or the previous chapter transaction is uncommitted when creating a new chapter. Outline/detailed-outline gates run only on initial creation; the tracking gate runs for initial and continued writing. The shared core implements the decision through the `tracking-checkpoint` subcommand of `.claude/hooks/story_hook_cli.js`. Because it must parse JSON, this gate allows execution when Node is unavailable (the pure-Bash outline/detailed-outline gates still block without Node).
  - **Impact on deployed projects**: Legacy tracked projects that should have migrated starting in v0.7.3 could previously continue writing in Claude Code; they are now blocked. Use the “Legacy Tracking Project Migration” path in `/story-import` to rebuild `追踪/`. A full-book reanalysis is unnecessary.

After redeployment, **start a new session** so custom agents are registered again.

## Current v23 Contract

- `story-import` rebuilds only the author’s existing novel as a writing project: `拆文库/{导入书名}/` migrates into manuscript/settings/outline/tracking and is no longer automatically registered as a primary/secondary benchmark or copied into project `对标/`. Only an external work explicitly selected by the user and sourced from independent `拆文库/{对标书名}/` is synchronized to `对标/{对标书名}/`.
- Without an external benchmark, skip only benchmark modules, pacing, and style recall; the project genre card is still generated from the current book’s genre information and is no longer disabled by the benchmark branch. Missing primary benchmark artifacts continue to fail fast; only a missing individual optional module card is skipped locally.
- Every Skill that may spawn a project agent first reads `.story-deployed.agents_version`. If it differs from v23, **spawn normally** and add only a report notice about the mismatch and recommendation to rerun `/story-setup` and start a new session. A version mismatch does not block parallel execution—bumps often result from other deployment changes while the agent template is unchanged. The true signal for solo/direct fallback is a missing agent file or a runtime that does not expose custom agents.
- Writing and import accept only current analysis artifacts: if `剧情/情绪模块.md` or `剧情/节奏.md` is missing, fail fast and provide a repair action to rerun Stage 3+ / re-import.
- New, completed, or revised detailed outlines accept only the full chapter blueprint. If stage position, structural formula, prohibited early reveals, content summary, plot arrangement, character relationships, plot elaboration, or ending setup is missing, complete it before writing. Legacy detailed outlines missing these fields do not block daily writing; fall back to legacy fields (core event, plot-beat sequence, target emotion, opening/ending hooks, word-count target).
- Detailed-outline fields specify “what happens” in the chapter, not manuscript shape. Every field must be honored in prose, but plot beats may be merged, interwoven, and reordered rather than advanced one item per paragraph. “Ending / ending setup” records the exact final action, image, or line—not a state judgment.
- Each agent adapter reads only the canonical reference path for its target: Claude `.claude/skills/`, OpenCode `skills/`, Codex `.codex/skills/`.
- `_progress.md` resume accepts only `schema_version: 2` with a chapter-boundary table and no longer performs implicit legacy migration.
- Codex hook upgrades use a stable managed identity to replace registrations: remove old direct Python commands and existing launcher commands before writing the current six registrations, preventing duplicate execution.
- If a custom hook called the removed `discover_book_dir()`, change it to `discover_active_book()`. The compatibility alias no longer exists.
- The “incomplete analysis” reminder for `拆文库/` filters by “final status” in `_progress.md`: `completed` / `completed_with_errors` do not count; all other values, missing fields, empty files, and unreadable files count as incomplete. The decision lives in `discover_incomplete_analyses()` within `lib/common.sh`.
- Passive version-update reminders throttle the notice itself for 24 hours; failure to reach GitHub writes a negative cache and does not repeat the request in the same window.

## Upgrade Steps

1. Rerun story-setup at the project root.
2. Confirm that `.story-deployed` contains `agents_version: 29` and `setup_skill_version: 1.2.10`.
3. Confirm that the target CLI’s agents, hooks/rules, and reference bundle pass installation validation.
4. Start a new session so custom agents and hooks register under the current files.
5. **Required for active long-form projects**: Check whether each book has `追踪/_tracking-state.json`. Its absence means the project uses the legacy tracking structure; writing the next chapter will be blocked until you rebuild it through “Tracking-Model Migration” below.
6. If an existing analysis library or detailed outline does not satisfy the current contract, reanalyze/re-import it or complete the outline before continuing.

## Cleaning Self-Benchmarks from Imported Projects (v23)

Older `story-import` versions may have mistakenly created `对标/{当前书名}/` from the author’s own imported book or registered the current book as a “primary benchmark.” Upgrades never delete user files automatically; review them manually using these boundaries:

1. Preserve `拆文库/{导入书名}/`; it is the data source for current-book import analysis and project reconstruction, not an erroneous directory.
2. Treat project-root `设定/` as the current book’s official settings. If `对标/{当前书名}/` is confirmed to be copied only from this book’s `设定/` or `拆文库/{导入书名}/` with no manual additions, delete the mistakenly created directory.
3. Remove fields in `设定/题材定位.md` that register the current book as a primary/secondary benchmark; leave genuine external benchmarks unchanged.
4. If a `对标/{外部书名}/` directory appears external but its contents actually come from the current book, delete the erroneous view and resynchronize from the genuine `拆文库/{对标书名}/`; do not rename it as a pretend repair.
5. Rerun `/story-setup` (use `$story-setup` in Codex) and start a new session so v23 agent templates take effect. Until then, spawning still works and adds only one version-mismatch notice.

## Tracking-Model Migration (Required for Long-Form Projects on v0.7.2 or Earlier)

Long-form tracking changes from “the model freely writes multiple Markdown files” to **one structured authority at `追踪/_tracking-state.json` + transactional writes through `scripts/tracking_commit.py`**. Every Markdown file (continuation state card, per-chapter records, character snapshots, foreshadowing table, dual timeline views) is a complete derived view generated by the tool and is no longer handwritten.

Conditions and consequences:

| Condition | Result |
|------|------|
| `追踪/_tracking-state.json` exists and `check` passes | Normal; no action required |
| `_tracking-state.json` missing but manuscript exists | Daily writing stops; hooks directly block manuscript writes on OpenCode / ZCode / Codex |
| Exists but a derived view was edited manually | `check` reports `derived view differs from _tracking-state.json` |

Migration **does not require a full-book reanalysis**. Manuscript, `设定/`, `大纲/`, and `拆文库/` are unaffected; only `追踪/` is rebuilt. Run the “Legacy Tracking Project Migration” path in `/story-import`: count the last complete chapter `N`, reconstruct current state from legacy tracking files and the latest chapters, construct an initialization transaction with `last_chapter=N`, and run `tracking_commit.py init`. The legacy tracking structure is moved intact to `追踪/_旧追踪存档/`; it is not deleted or parsed.

Retired structures: `_tracking-meta.json`, `时间线/事件库.json`, and older tracking files are no longer parsed; `commit` and `check` reject them directly.

Two hard rules for daily writing: every tracking write goes through `tracking_commit.py`; after a derived view is modified, rebuild it completely through that chapter’s `mode=revision` transaction rather than editing it manually.
