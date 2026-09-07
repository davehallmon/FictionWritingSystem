## Current version

- `setup_skill_version: 1.2.10`
- `agents_version: 29`

If any field of `.story-deployed` is missing, or if `agents_version` is missing/non-integer/less than `29`, it will be considered as a deployment to be updated. Rerun `/story-setup` directly (use `$story-setup` for Codex, use `/skills` or natural language roll call for Antigravity); do not support historical templates at runtime. If the project `agents_version` is greater than `29`, it means that the local story-setup is older than the project: update oh-story-claudecode first and do not overwrite it with v29 downgrade. For historical version changes, please see the warehouse root directory `CHANGELOG.md`.

## Upgrade strategy

| Strategy | Applicable Scenarios | Behavior |
|------|----------|------|
| Override deployment | Brand new project | Write current agents/hooks/rules/reference bundle |
| Merge deployment | Existing projects | Replace story-setup management files and merge user maintenance files |
| Manual update | Only update specific files | Only recommended for maintainers familiar with deployment contracts |

It is recommended to always re-run story-setup to let the deployer process files by owner class.

### Self-nested residuals

The skill copies of the three paths of OpenClaw / Reasonix / generic are in the project `skills/`. When re-running, the copy in the project will be executed. Automatic cleaning cannot reach it: manually delete the above directory first. To update the skill text itself in the project, you need to update oh-story-claudecode and overwrite these 13 directories under the project `skills/` with the new package.

## File ownership

### story-setup management, replaceable

### User status, not covered

- `{Book title}/Text/`, `Text.md`
- `{book title}/setting/`, `outline/`, `tracking/`
- `.active-book`

## v29 Current contract

- The narrative-writer template removes paragraph-by-paragraph quotas: "Expand sub-events" are changed to "expand promotion units", and "the total number of detailed sub-events is ≥100-150 words" is deleted; String Theory no longer requires "at least once per section", and tasks, reasoning, crafts or waiting chains can be continuously expanded. Three-terminal (Claude / OpenCode / Codex) product synchronization.
- The short reference bundle changes to judge the length and rhythm according to the scene function: `short-genre-formulas.md` removes the fixed pitch of hook density, "cool article section 500-800 words/section" and "slap density once every 3-5 sections"; `short-emotional-methods.md` removes the fixed pitch of emotional turns and face-beating beats; `short-suspense.md` There is no longer a minimum suspense level for each type of section; `short-reversal.md` The sweet pet line no longer requires one dessert per section.
- The section structure of `format-and-structure.md` no longer has a uniform minimum word count and calculation of "8-15 sections / total word count ÷ 1000"; the length and number of sections are subject to narrative responsibilities, and the entire article is constrained by the user's delivery scope.

After redeployment, you need to open a new session before the custom agent and hooks can be re-registered.

## v28 Historical Contract

- `agent-reference-profiles.md` becomes the only profile inventory of story-architect; Agent template no longer copies the second inventory. Deployment guards verify Common / Long / Short ownership, file existence, and off-table reads.
- Suspense, reversal and quality standards are changed to profile exclusive: long uses `long-suspense.md`, `long-reversal.md`, `long-quality.md`, short uses the corresponding `short-*` files; `agent-quality.md` only retains the cross-genre five-dimensional core.
- The long-form genre data is changed to `long-genre-catalog.md` + `long-genre-mechanics.md`, and the three-act structure of short stories is no longer put into Common; short stories continue to use `short-genre-formulas.md`.
- `format-and-structure.md` only serves short files/import/setup; long files use independent `long-format.md` instead of "reading only part of the same file".
- Cross-Skill approximate copies are registered by `derived_groups` in `shared-references.json` and the reason for differentiation; the directory image list must cover all files in the source tree.

After redeployment, you need to open a new session before the custom agent and hooks can be re-registered.

## v27 Historical Contract

- story-architect maintains a single Agent name, but first selects `long` / `short` reference profile for each task, and only loads common + current-length assets; explicitly returns unresolved when it cannot be determined, and does not mix the two sets of calibers.
- `plot-core-methods.md` is conditionally consumed by story-architect in Kawen, plot cycle, five-step climax, transition, long-term expectation and daily progress scenarios; deployment guards will reject references without Agent consumption chain.
- The long profile uses `genre-prose-cards.md` and `long-emotional-methods.md`, the short profile uses `short-genre-formulas.md`, `short-paragraph-hooks.md` and `short-emotional-methods.md`. The long profile no longer inherits short profile default values ​​such as 500–800 words per section.
- The profile file and semantic alias of the setup reference bundle belong to the story-setup management assets; redeployment will replace the old bundle, and a new session must be opened after deployment.

After redeployment, you need to open a new session before the custom agent and hooks can be re-registered.

## v26 Historical Contract

- Added Google Antigravity 2.0 project deployment: 13 skills are truly copied to `.agents/skills/`, 7 Claude agent true sources are deterministically converted to `.agents/agents/agent-name/agent.md` (`agent-name` is the actual name), and `.agents/rules/oh-story.md` Always-On Rule is installed.
- Antigravity Workspace Hooks only use the official `PreToolUse`, `PostToolUse`, `PreInvocation`, and `Stop` events; pre-write access directly returns allow/deny, PostToolUse only returns `{}` according to the protocol, post-write body findings are handed over to the next PreInvocation through session artifacts, and Stop can continue running at most once.
- `.agents/hooks.json` is atomically merged according to the top-level `oh-story` management group and does not cover other user hook groups; deployment does not write `~/.gemini/` and does not rely on global skill or symlink discovery. Existing `.agents/skills` symlinks must be explicitly acknowledged before being migrated to a real directory, and the helper never writes along the symlink to its target.
- Antigravity custom agent is called through `invoke_subagent` + the same name `TypeName`; if it does not have this capability at runtime, it will be downgraded according to the existing solo/direct rules. The external Hook API does not have PreCompact/PostCompact, and post-compression context recovery is forced by the Always-On Rule to read `tracing/context.md`.

After redeployment, you need to open a new Antigravity conversation to re-scan Skills, Rules, Agents and Hooks; it is recommended to smoke test separately for IDE and interactive `agy`.

## v25 Historical Contract

# 升级指南

部署清单的 Source 相对 skill 包、Target 相对项目根，两个基准目录在 skills-only 端会重合；经 `.agents/skills → ../skills` 等 symlink 加载时，路径文字不同也可能指向同一目录。部署器会先按 realpath / samefile 语义拒绝同对象与「目标位于源目录内」的递归复制，再删掉已有的 `agent-references/agent-references/`（可能多层）或 `skills/story-setup/skills/` 残留。

These files are managed by story-setup and do not contain user-defined content:
- `.claude/hooks/` — all hook scripts and `lib/` helper libraries
- `.claude/agents/` — all agent definitions
- `.claude/rules/` — all path-scoped rules
- `.claude/skills/story-setup/references/agent-references/` — copy of Agent reference materials
- `.agents/skills/{13 known skills}/`, `.agents/agents/agent-name/agent.md` (7 known `agent-name`), `.agents/rules/oh-story.md`, `.agents/hooks/{story_antigravity_hook.js,story_hook_core.js}` — Real Skills, generation within the Antigravity project Agents, Always-On Rule and Hook runtime; Skills/Agents of other users in the same directory are reserved
- `skills/{13 known skills}/` — OpenClaw / Reasonix / generic 的项目 skill 副本，仅覆盖 oh-story 已知名称
- `.zcode/skills/{13 known skills}/`、`.zcode/commands/{13 known commands}.md` — 仅覆盖 oh-story 已知名称
- `.zcode/hooks/story_zcode_hook.js` — ZCode dedicated Hook runner

### 用户与 story-setup 共同维护，只合并管理块

这些文件可能含用户自定义内容：
- `CLAUDE.md` — merge by marker/section, user-unique sections are reserved
- `.claude/settings.local.json` — Identify story hooks by command; existing managed commands will be migrated to the event/matcher/timeout/if of the current template (such as v25's Bash body pre-guard), and other user hooks and configurations will be retained
- `AGENTS.md` — ZCode/OpenCode/Codex/OpenClaw/generic 按 marker/section 合并
- `.zcode/config.json` — only merge oh-story Hooks by event, matcher and process args, other fields are retained
- `.agents/hooks.json` — only replaces the top-level `oh-story` named group, other user hook groups remain

- Long-form word count is only measured by the `visible_chars_v1` runtime entry in `storyctl.py`. Only one pure `checkpoint` is added during writing, and the final `chapter check` returns the length and existing blocking quality at the same time; the user can submit it in-band, `under` prohibits automatic rewriting and the user accepts the natural length or changes the target/details/gives up, `over` defaults to only one clean-delete compression without adding new semantics and rechecks, and it is left to the user to make decisions if it is still out-of-band. Tracking is submitted before entering the next chapter.
- Claude、OpenCode、Codex、ZCode 的正文 Hook 不再各自解析细纲、计算字符数或执行旧 90% 欠账提示；Adapter 只保留正文内容网，避免与 `storyctl` 形成第二套字数口径。
- narrative-writer 与 story-architect 使用显式字数口径，不再填写逐情节点数字配额，也不在缺少目标时回退 3000 字；后半段只能完成尚未写的批准情节点，完成即停，不为字数新增独立剧情。
- 使用 `story-import` 导入时按 `storyctl wordcount measure` 记录已写章节的当前口径长度；无法执行 Python 3/CLI 时明确停止，不用模型估算代替。
- 工作区新增 `.story/作者记忆/`：只有带原话证据、经过确认的稳定偏好才进入作者画像；候选、冲突替代和撤回保留审计记录。它与单本小说追踪隔离，当前指令、本书设定和硬门禁优先。
- story-explorer 遇到已登记但主产物缺失的对标时 fail-closed，不再静默换用另一本；narrative-writer、story-architect、character-designer 的 reference 表改为按任务条件读取，避免列出但不触发。
- 新建细纲的情节点使用五列表格记录内容、功能、人物、约束与落点；不再把逐点字数配额当正文编排指令。存量细纲仍可继续日更，只有新建、补建或改纲时采用新格式。
- 部署器在复制前按 realpath / samefile 拦截源目标同对象和目标嵌入源目录，并清理已知嵌套残留；OpenClaw / Reasonix / generic 的项目内旧副本需按本页“自嵌套残留”先手动处理。

重新部署后需**新开会话**，custom agent 与 hooks 才会重新注册。

- Claude Code 的正文前置守卫现在也注册到 Bash：常见的重定向、`tee`、`touch`、`cp`、`mv`、`install` 写入正文时复用共享 JS 核识别目标并执行大纲/追踪门；只读命令里的引号示例与 heredoc 正文提及不拦，并按 hook `cwd` 解析相对路径。该面是**静态 best-effort 识别，不是 shell 沙箱**：环境变量间接路径、运行时生成命令与未列出的任意写文件程序无法可靠静态判定；这类写入应改用 Write/Edit。Bash 命令面依赖 node，node/共享核异常时显式告警后 fail-open；Write/Edit/MultiEdit 的纯 bash 兜底不受影响。
- Codex Python 与共享 JS 的书目录发现统一限制为项目下 4 层，并剪枝隐藏目录、`node_modules`，避免 SessionStart/Stop 无界扫描和跨端发现范围漂移。
- narrative-writer 与部署 reference 增加“普通名词不用引号强调”的 Gate B；合法对话、直接引用、书名/代号和场内系统载体原文保留。
- narrative-writer 的工具白名单加入 `Bash`：字数统计、句长分布、`check-ai-patterns.js` 与 `check-outline-copy.js` 复扫都要确定性数值，缺工具时这几条规则整条空转。字数与句长必须报实测值，探测不到 Python / node 时如实声明“未完成机器验证”，不得声称已统计或已运行脚本。
- narrative-writer 的细纲消费规则拆成两条并列：内容层（每项独立落地、不许漏、不许两项并一句）与形状层（落地位置、顺序、断段自定，可打散重排，不要一项一段平推）。形状半边同步进 `story-long-write` 的 spawn 清单。
- 细纲「情节细化」新增**复沓锚句**字段：必须一字不差进正文的原话逐行列出并注明落点，没有写“无”。存量细纲缺该字段时按“无锚句”处理，行为与此前一致，不必回头补。

After redeployment, you need to open a new session before the custom agent and hooks can be re-registered.

- `.claude/rules/story-narrative.md` Delete the red line block "No AI cavity". This block is only loaded under the three paths of `open library/` `benchmark/` `setting/`. The text directory is not hit at all. The five rules have also been covered by narrative-writer's 7 Gate/prohibited matters and `check-ai-patterns.js`'s blocking rules.
- The dialogue tag rules in `.claude/rules/story-format.md` were changed from "Prohibit "he said" and "she said"" to "Avoid mechanization of dialogue tags": high-frequency or formulaic tags are replaced with actions/contexts, and ordinary "say" can be retained for low-frequency use. Previously, this file was the only place in the warehouse where ordinary "saying" was judged as a violation. It conflicted with `format-and-structure.md` and other 11 calibers, and it happened to be loaded on the `text/` path.
- `.claude/agents/narrative-writer.md` streamlined to 19%: delete the review list that is repeated with 7 Gate/prohibited matters (the complete rubric will be inlined when story-review spawns), the specific word count expression verification in the text writing stage (moved to the review side), and repeated statements of `…`/`——`, blank lines between paragraphs, and chapter meta-information regularity. The writing rules themselves have not been relaxed, and the scope of Gates A-G and prohibited matters remains the same.
- `.claude/hooks/guard-outline-before-prose.sh` adds the tracking checkpoint gate, in the same order as OpenCode / ZCode / Codex: the tracking status is missing, the schema is not 4, the renewal status card revision number is inconsistent with the state, and the previous chapter transaction is not submitted when the new chapter is first created, all of which prevent the text from being written. The detailed outline/outline gate is only judged when it is first built, and the tracking gate is judged for both the first build and the continuation. It is determined that the `tracking-checkpoint` subcommand of `.claude/hooks/story_hook_cli.js` is used to adjust the shared core, and the four ends are implemented separately; JSON needs to be parsed, so this door is allowed when the node is not present (the outline/details door is still pure bash, and it can be blocked without node).
  - **Impact on deployed projects**: Old tracking projects that should be migrated since v0.7.3 could continue to be written on Claude Code, but will now be blocked. Follow the prompts and go to "Old Tracking Project Migration" in `/story-import` to rebuild `tracking/`. There is no need to re-run the entire book to disassemble it.

## v24 当前契约

重新部署后需**新开会话**，custom agent 才会重新注册。

## v23 当前契约

- `story-import` 只把作者已有小说重建为写作工程：`拆文库/{导入书名}/` 迁移到正文/设定/大纲/追踪，不再自动登记成主/副对标，也不再复制到项目 `对标/`。只有用户明确选择、且来源为独立 `拆文库/{对标书名}/` 的外部作品才同步到 `对标/{对标书名}/`。
- 无外部对标时只跳过对标模块、节奏和文风召回；项目题材卡仍从本书题材信息生成，不再被对标分支误伤。对标主产物缺失继续 fail-fast，只有单个可选模块卡未命中时才局部跳过。
- 所有可能 spawn 项目 agent 的 Skill 都先读取 `.story-deployed.agents_version`：与 v23 不一致时**照常 spawn**，只在报告里提示版本不匹配、建议重跑 `/story-setup` 并新开会话。版本不匹配不阻断并行——bump 常常源于别的部署物变化而 agent 模板未动。真正降级 solo/direct 的信号是 agent 文件缺失或运行时不暴露 custom agent。
- 写作与导入只接受当前拆文产物：`剧情/情绪模块.md` 与 `剧情/节奏.md` 缺失时 fail-fast，并给出重跑 Stage 3+ / 重新导入的修复动作。
- 新建、补建、改纲的细纲只接受完整章节蓝图：缺少阶段位置、结构公式、禁止提前释放、内容概括、情节安排、人物关系、情节细化或结尾设定时，先补齐再写。旧版细纲缺这些字段不阻塞日更，回退消费旧字段（核心事件、情节点序列、目标情绪、章首/章尾钩子、字数目标）。
- 细纲字段是本章「要发生什么」的内容规格，不规定正文形状：各字段都要在正文里兑现，但正文可合并、穿插、重排情节点，不按条目顺序一条一段平推。细纲「结尾 / 结尾设定」写本章最后落在什么动作、画面或台词上，不写状态判词。
- 每个 agent adapter 只读取本目标的 canonical reference 路径：Claude `.claude/skills/`、OpenCode `skills/`、Codex `.codex/skills/`。
- `_progress.md` 恢复只接受 `schema_version: 2` 与章节边界表，不再执行隐式历史迁移。
- Codex hooks 升级使用稳定管理身份替换注册；会先移除旧直调 Python 命令与已有 launcher 命令，再写入当前 6 个注册，不会双重执行。
- 定制 hook 如果调用了已删除的 `discover_book_dir()`，请改为 `discover_active_book()`。当前版不再保留该兼容别名。
- `拆文库/` 的「未完成拆文」提醒按 `_progress.md` 的「最终状态」取值过滤：`completed` / `completed_with_errors` 不计入，其余取值与字段缺失、空文件、不可读一律按未完成上报。判定收在 `lib/common.sh` 的 `discover_incomplete_analyses()`。
- 被动版本更新提醒按 24h 节流提示本身；取不到 GitHub 时写入负缓存，同一窗口内不重复请求。

## 升级步骤

1. 在项目根目录重新运行 story-setup。
2. 确认 `.story-deployed` 写入 `agents_version: 29` 与 `setup_skill_version: 1.2.10`。
3. 确认目标 CLI 的 agents、hooks/rules 和 reference bundle 都通过安装验证。
4. 新开会话，使 custom agents 与 hooks 按当前文件重新注册。
5. **长篇在写项目必做**：检查每本书的 `追踪/_tracking-state.json` 是否存在。不存在就是旧追踪结构，按下方「追踪模型迁移」重建，否则写下一章会被拦。
6. 若已有拆文库或细纲不满足当前契约，先重新拆解/导入或补齐细纲，再继续写作。

## 导入项目的自对标清理（v23）

旧版 `story-import` 可能把作者自己的导入书误建成 `对标/{当前书名}/`，甚至把本书设定登记成“主对标”。升级不会自动删除用户文件，按以下边界人工核对：

1. 保留 `拆文库/{导入书名}/`；它是本书导入分析和重建工程的数据源，不是错误目录。
2. 以项目根 `设定/` 为本书正式设定。若 `对标/{当前书名}/` 的内容确认只是从本书 `设定/` 或 `拆文库/{导入书名}/` 复制而来，且没有人工补充，再删除这个误建目录。
3. 清理 `设定/题材定位.md` 中把当前书登记为主/副对标的字段；真实外部对标登记不动。
4. 若某个 `对标/{外部书名}/` 目录名看似外部作品，但内容实际来自当前书，删除这份错误视图，再从真正的 `拆文库/{对标书名}/` 重新同步；不要改名冒充修复。
5. 重新运行 `/story-setup`（Codex 用 `$story-setup`）并新开会话，使 v23 的 agent 模板生效；在此之前 spawn 照常工作，只会多一条版本不匹配提示。

## 追踪模型迁移（v0.7.2 及更早的长篇项目必读）

长篇追踪从「模型自由写多个 Markdown」改成 **`追踪/_tracking-state.json` 单一结构化权威 + `scripts/tracking_commit.py` 事务写入**。所有 Markdown（续写状态卡、逐章记录、角色快照、伏笔表、时间线双视图）都是由工具整份生成的派生视图，不再手写。

判断与后果：

| 情况 | 表现 |
|------|------|
| `追踪/_tracking-state.json` 存在且 `check` 通过 | 正常，无需处理 |
| 缺 `_tracking-state.json` 但已有正文 | 日更停止；OpenCode / ZCode / Codex 上写正文被 hook 直接拦截 |
| 存在但派生视图被手改 | `check` 报 `derived view differs from _tracking-state.json` |

迁移**不需要重跑全书拆解**：正文、`设定/`、`大纲/`、`拆文库/` 都不受影响，只重建 `追踪/`。执行 `/story-import` 的「旧追踪项目迁移」——数出最后完整章号 `N`，从旧追踪文件与最近几章正文重建当前状态，构造 `last_chapter=N` 的初始化事务跑 `tracking_commit.py init`。旧追踪结构会被按原样整体移入 `追踪/_旧追踪存档/`，不删除、不参与解析。

退役结构：`_tracking-meta.json`、`时间线/事件库.json` 及更早追踪文件不再被解析，`commit` 与 `check` 遇到会直接拒绝。

日常写作的两条硬约束：所有追踪写入都走 `tracking_commit.py`；派生视图被改动后用该章的 `mode=revision` 事务整份重建，不手改。
