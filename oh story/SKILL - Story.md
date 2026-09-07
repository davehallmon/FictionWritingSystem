---
name: story
description: "The main entrance of the online novel toolbox. Automatically routes to the corresponding skill according to user needs, and can manage author habits and start the local Dashboard. Trigger methods: /story, $story, /story dashboard, /网文, "I want to write a novel", "Remember my writing habits", "Open the workbench", "Check for updates". "
metadata: {"openclaw":{"source":"https://github.com/zenstory-ai/oh-story-claudecode"}}
---
# story: Web toolbox routing

You are the routing entry of the web writing toolbox. When the user's request is vague, you distribute it to a specific skill.

## Routing table

> Codex CLI preferentially uses `$story-*` or `/skills` to trigger; Claude Code / OpenCode continues to use `/story-*`; Antigravity can be selected in `/skills` or named in natural language; OpenClaw can use `/skill story-*` or named skill in natural language. The following table shows the slash command. Codex can replace `/story-long-write` with `$story-long-write`, and OpenClaw can replace it with `/skill story-long-write`.

| User Intent | Keyword Examples | Route To |
|---|---|---|
| Write a long story | Open a book, write an outline, long story, serialization | `/story-long-write` |
| Write short stories | Short stories, salty words, ten thousand words | `/story-short-write` |
| Long story breakup | Breakdown the story, analysis of this book, three golden chapters | `/story-long-analyze` |
| Break down short stories | Break down short stories and analyze the story | `/story-short-analyze` |
| Long story scan list | Long story ranking, What's Hot, Starting Point/Tomato/Jinjiang | `/story-long-scan` |
| Topic selection decision-making | What to write about that will be popular, help me choose a topic, and choose a topic direction | `/story-long-scan` |
| Short story scan list | Short story ranking, Zhihu Yanyan ranking | `/story-short-scan` |
| Remove the AI flavor | Remove the AI flavor, too AI, remove the flavor | `/story-deslop` |
| Review the manuscript | Review, review, review for me, consistency check, see if there are any problems | `/story-review` |
| Cover | Cover, cover image | `/story-cover` |
| Environment deployment | Prepare to write a book, set up the environment, and initialize | `/story-setup` |
| Browser control | Browser, crawling, login status | `/browser-cdp` |
| Import novels | Import, reverse analysis, import novels, import my books | `/story-import` |
| Workbench | dashboard, workbench, review library, browse project files, open project panel | See "Dashboard Workbench" below |
| Check/update version | Check for updates, is there a new version, upgrade, update toolbox | See "Version Update Check" below |
| Switch/list books | Cut books, change books, list my books, which books I am writing, and switch items | See "Multiple book switching" below |
| Manage author habits | Remember my writing habits, author portrait, preferences to be confirmed, forget this preference | See "Author Memory" below |
| Check story information | Check characters, check foreshadowing, check progress, check settings, what status, where written | spawn `story-explorer` agent (structured prompt: `Project directory: {dir}\nQuery type: {Select based on intent}\nQuery parameters: {User query}`); when the agent is unavailable, see "Query downgrade" below |
| Check information | Check information, help me check information, research, search, search | spawn `story-researcher` agent; when the agent is unavailable, see "Query downgrade" below |

### Import continuation sequence

When the user asked "Which should I import and continue writing first, setup or import?", the direct answer was: **It is recommended to do `/story-setup` first, then `/story-import` after opening/refreshing the session, and finally `/story-long-write` or `/story-long-write` to write Chapter N**. If the user has directly triggered `/story-import`, press story-import to continue with the built-in environment detection: when it is not setup, let the user choose to setup first or continue the serial import.

## Author's memory

When the user asks to remember, view, confirm, replace or forget author habits, load [references/author-memory.md](references/author-memory.md) and only use this skill's `scripts/author_memory_commit.py` to manage the workspace level `.story/author memory/`. Commonly used change order events `record`; the tool cannot claim to have remembered it before it returns `ok: true` and `Author Memory Receipt`. Displaying images or items to be confirmed is a read-only operation; if they do not exist, it means that they have not been created yet.

New habits must retain the user's original words and applicable scope. One-time requests are only executed and not recorded; novel facts are written into the book settings/tracking; inferences and repeated corrections are entered first to be confirmed; explicit replace is used when conflicting with already effective habits, and history is not rewritten in place. When the user does not specify a workspace, the nearest ancestor or current creative workspace in the memory of the existing author is located according to the protocol, and writing to the user's home directory by default is prohibited.

## Dashboard workbench

The user executes `/story dashboard` (Codex is `$story dashboard`), or explicitly says "Open workbench / view project
file", directly start the local Dashboard distributed with this skill and no longer forward it to other skills:

1. Use the **current working directory** as the default workspace; use this directory instead when the user explicitly provides it. The directory must exist.
2. Locate `scripts/dashboard-server.mjs` from the currently loaded `story` skill directory. Do not hardcode the warehouse path.
   Global skill path or user home directory.
3. After checking that `node` is available, execute it as a long-running process:

   ```bash
   node "<story-skill-dir>/scripts/dashboard-server.mjs" --root "<workspace>" --open
   ```

4. Wait for the "local address" to appear in the output and return the complete URL to the user. Keep services running when tools support background processes/PTY;
   Failure to automatically launch the browser is not considered a failure and a clickable URL will still be returned.
5. Dashboard only listens to `127.0.0.1` by default. Do not actively add `--allow-network` and do not expose the workspace to
   LAN or public network.

The workbench will recognize the standard `open library/{book title}/` and be compatible with the stock `open library-{book title}/`. Writing project recognition also supports:

- Long directory structure: The directory contains any ordinary subdirectory of `text/`, `outline/`, `settings/` or `tracking/`.
- Short story single file structure: The directory contains the ordinary file `text.md`, and also contains `section outline.md` or `settings.md`.

Symbolic links are not used as project tags, nor are plain source directories with a single `text.md`. Browser editable
`.md`, `.txt`, `.json`, `.yaml`, `.yml`, `.toml`, use the modification time before saving or confirming deletion.
Misoperation of external update.

When stopping the service, just terminate the corresponding Node long-running process. If the user only asks for usage, don't start it for him; give
`/story dashboard` / `$story dashboard` are the corresponding entrances for the two platforms.

## Routing process

1. Analyze user requests and extract intended keywords
2. Match the above table and find the corresponding skill
3. If there is a clear match, call the corresponding skill directly (Claude/OpenCode can use `Skill("skill-name")` or slash command; Codex can use `$skill-name` / `/skills`; Antigravity can use `/skills` or natural language naming; OpenClaw can use `/skill skill-name` or natural language naming)
4. If no match is found, ask the user what they want to do (select from the table above)
5. If the user says "I want to write a novel" but does not specify a long/short story, ask about the length type before routing.

## Query downgrade

> Spawn version prompt (do not block spawn): First read the `agents_version` of the project root `.story-deployed`. When it is inconsistent with this version of `agents_version: 29` (missing tags, missing fields/non-integers, less than or greater than 29) **check file existence and spawn** as usual, but only check the canonical directory of the current runtime; also report `Notice: agents bundle version mismatch (project {N}, this version 29)` and prompt to re-run `/story-setup` and open a new session; when greater than 29, an additional prompt to update first oh-story-claudecode, do not downgrade and overwrite with local old version setup. Only when the agent file is missing or the custom agent is not exposed at runtime, solo/direct will be downgraded and `Fallback: ... -> solo` will be reported.

"Check story information" "Check information" Before going to the agent, do a light availability check (routing only does this layer and does not bear the global deployment strategy): the Agent/Task or `invoke_subagent` tool that is not currently in the subagent context, current runtime, is available, and the corresponding deployment file exists (Claude `.claude/agents/*.md`, OpenCode `.opencode/agents/*.md`, Codex `.codex/agents/*.toml`, Antigravity `.agents/agents/agent-name/agent.md`, where `agent-name` is the target agent name) → You can try spawn. Antigravity uses `invoke_subagent` + the same name as `TypeName`, and it must not be misjudged due to the existence of other end files. If any of them are not satisfied, or unknown agent/custom-agent registry is not exposed when running, then downgrade without hard failure:

- `story-explorer` is not available → The main thread directly uses Read/Grep to retrieve from the project file (character status/foreshadowing/progress/settings), mark `Fallback: agent unavailable -> direct lookup` before answering; when the project has not been deployed, it prompts `/story-setup` (use `$story-setup` in Codex).
- `story-researcher` is not available → The main thread uses the existing search/answer capabilities to complete, or prompts the user to use `/browser-cdp` collection instead, also marked `Fallback: agent unavailable -> direct lookup`.

## Project status awareness

Check the current project status before routing:

- **No project directory** (no title directory containing `track/` or `settings/`):
  - If the user wants to write, the next step is to run `/story-setup` to initialize the environment (use `$story-setup` in Codex)
  - If the user wants to scan the list/remove articles, route directly
- **Existing project**: Check the `.story-deployed` mark, if not deployed, run `/story-setup` first (use `$story-setup` in Codex)

## Switch between multiple books

When the user wants to switch or view the book he is writing (one project can have multiple books at the same time):

1. 在项目根查找所有书目录：包含 `追踪/` 或 `设定/` 子目录的目录（含 `长篇/`、`短篇/` 下的子目录）。
2. 列出书名，并标出当前 `.active-book` 指向的那本。
3. 让用户选择，把所选书的相对路径写入项目根 `.active-book`（覆盖原内容）。
4. 只发现一本时直接确认为活跃书，无需询问。

## Version update check

Executed when the user asks "Is there a new version?" "Check for updates" and "Upgrade". **Only notifications, no updates determined by the user, no automatic installation. **

1. **当前版本**：读本 skill 同目录的 `VERSION` 文件；缺失则视为未知。
2. **最新版本**：优先 `gh release view --json tagName,name,url -R zenstory-ai/oh-story-claudecode` 取 `tagName`；无 gh 用 `curl -fsS --max-time 5 https://api.github.com/repos/zenstory-ai/oh-story-claudecode/releases/latest` 取 `.tag_name`（jq 或 grep）。查不到 → 告知"暂时拉不到最新版本，可手动看 [Releases](https://github.com/zenstory-ai/oh-story-claudecode/releases)"，不报错。
3. **比较**：去掉 `v` 前缀按语义版本比（major.minor.patch）。`gh release` 默认取 latest 稳定版，不含 pre-release。
4. **告知**：
   - 已最新 → 「已是最新版 vX.Y.Z」。
   - 有新版 → 列出 当前 vA → 最新 vB + [Releases](https://github.com/zenstory-ai/oh-story-claudecode/releases)/[CHANGELOG](https://github.com/zenstory-ai/oh-story-claudecode/blob/main/CHANGELOG.md)（能拿到 release notes 就附本次要点），再用 AskUserQuestion 问「现在更新吗？」：
     - 选更新 → 跑 `npx skills add zenstory-ai/oh-story-claudecode -y -g`（`-g` 全局，去掉则只更当前目录）；完成后提示：已部署过的项目在项目根重跑 `/story-setup`（Codex 中用 `$story-setup`）同步 hooks/agents/references，并**新开一个会话**让 agents 重新注册。
     - 选先不 → 不动，告知随时可再来。
