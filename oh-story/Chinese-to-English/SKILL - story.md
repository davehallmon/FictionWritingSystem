---
name: story
description: "Main entry point for the web-fiction toolkit. Automatically routes user requests to the appropriate skill, manages author preferences, and launches the local Dashboard. Triggers: /story, $story, /story dashboard, /网文, 'I want to write a novel,' 'remember my writing preferences,' 'open the workspace,' and 'check for updates.'"
metadata: {"openclaw":{"source":"https://github.com/zenstory-ai/oh-story-claudecode"}}
---
# story: Web-Fiction Toolkit Router

You are the routing entry point for the web-fiction toolkit. When a user's request is ambiguous, route it to the appropriate skill.

## Routing Table

> In Codex CLI, prefer `$story-*` or `/skills`; Claude Code and OpenCode continue to use `/story-*`; in Antigravity, select the skill through `/skills` or name it in natural language; in OpenClaw, use `/skill story-*` or name the skill in natural language. The table uses slash commands. Codex may treat `/story-long-write` as `$story-long-write`, and OpenClaw may treat it as `/skill story-long-write`.

| User intent | Example keywords | Route to |
|---|---|---|
| Write long-form fiction | start a book, write an outline, long-form, serialize | `/story-long-write` |
| Write short-form fiction | short story, Salt-Selection story, ten thousand words | `/story-short-write` |
| Analyze long-form fiction | decompose a story, analyze this book, opening three chapters | `/story-long-analyze` |
| Analyze short-form fiction | decompose a short story, analyze this story | `/story-short-analyze` |
| Scan long-form rankings | long-form rankings, what is popular, Qidian/Fanqie/Jinjiang | `/story-long-scan` |
| Choose a marketable topic | what should I write, help me choose a topic, topic direction | `/story-long-scan` |
| Scan short-form rankings | short-form rankings, Zhihu Salt-Selection rankings | `/story-short-scan` |
| Remove AI writing traces | remove AI traces, sounds too AI-generated, de-slop | `/story-deslop` |
| Review a manuscript | review, edit, review this for me, consistency check, find problems | `/story-review` |
| Create a cover | cover, cover image | `/story-cover` |
| Deploy the environment | prepare to write a book, configure environment, initialize | `/story-setup` |
| Control a browser | browser, scrape, authenticated session | `/browser-cdp` |
| Import a novel | import, reverse-parse, import a novel, bring my book into the project | `/story-import` |
| Open the workspace | dashboard, workspace, view decomposition library, browse project files, open project panel | See Dashboard Workspace below |
| Check or update the version | check for updates, is there a new version, upgrade, update the toolkit | See Version Update Check below |
| Switch or list books | switch books, change books, list my books, which books am I writing, switch project | See Switching Between Multiple Books below |
| Manage author preferences | remember my writing preferences, author profile, unconfirmed preferences, forget this preference | See Author Memory below |
| Query story information | find a character, find foreshadowing, check progress, inspect settings, current status, where did I stop | Spawn the `story-explorer` agent with the structured prompt `项目目录：{dir}\n查询类型：{根据意图选择}\n查询参数：{用户查询}`; if the agent is unavailable, see Query Fallback below |
| Research a topic | research, help me research, investigate, search this, look this up | Spawn the `story-researcher` agent; if the agent is unavailable, see Query Fallback below |

### Import and Continuation Order

When a user asks whether setup or import comes first for an imported continuation, answer directly: **Recommended order: run `/story-setup` first, start or refresh the conversation, run `/story-import`, and then run `/story-long-write 日更` or `/story-long-write 写第N章`.** If the user has already invoked `/story-import`, continue with story-import's built-in environment check. If setup has not run, let the user choose between running setup first and continuing with a sequential import.

## Author Memory

When the user asks to remember, view, confirm, replace, or forget an author preference, load [references/author-memory.md](references/author-memory.md), and use this skill's `scripts/author_memory_commit.py` exclusively to manage the workspace-level `.story/作者记忆/` directory. Use a single-event `record` operation for ordinary changes. Do not claim that a preference has been remembered until the tool returns `ok: true` and an `Author Memory Receipt`. Viewing the profile or unconfirmed items is read-only; if no profile exists, say so directly.

New preferences must retain the user's exact words and scope. Execute one-time requirements without recording them. Store novel facts in that book's specification or tracking files. Put inferred preferences and repeated corrections into the confirmation queue first. When a new preference conflicts with an active one, perform an explicit replacement instead of rewriting history in place. If the user does not specify a workspace, locate the nearest ancestor containing existing author memory or use the current writing workspace. Never default to the user's home directory.

## Dashboard Workspace

When the user runs `/story dashboard` (`$story dashboard` in Codex), or explicitly asks to open the workspace or view project files, launch the local Dashboard distributed with the currently loaded `story` skill. Do not route the request to another skill:

1. Use the **current working directory** as the default workspace. If the user provides a directory, use it instead. The directory must exist.
2. Locate `scripts/dashboard-server.mjs` relative to the currently loaded story skill directory. Do not hard-code a repository path, global skill path, or user home directory.
3. Confirm that `node` is available, then start this long-running process:

   ```bash
   node "<story-skill-dir>/scripts/dashboard-server.mjs" --root "<workspace>" --open
   ```

4. Wait for output containing “本机地址,” then return the complete URL to the user. Keep the service running when the tool supports background processes or a PTY. Failure to launch a browser automatically is not a service failure; still return the clickable URL.
5. The Dashboard listens only on `127.0.0.1` by default. Do not add `--allow-network` proactively, and do not expose the workspace to a local network or the public internet.

The workspace recognizes the standard `拆文库/{书名}/` structure and remains compatible with the legacy `拆文库-{书名}/` structure. Writing-project detection supports both forms below:

- Long-form directory structure: the directory contains any ordinary subdirectory named `正文/`, `大纲/`, `设定/`, or `追踪/`.
- Short-form single-file structure: the directory contains the ordinary file `正文.md` together with either `小节大纲.md` or `设定.md`.

Symbolic links do not count as project markers. An ordinary reference directory containing only `正文.md` must not be misidentified as a project. The browser can edit `.md`, `.txt`, `.json`, `.yaml`, `.yml`, and `.toml` files. Before saving changes or confirming deletion, use the modification time to detect external updates.

Stop the service by terminating the corresponding long-running Node process. If the user asks only how to use it, do not start it; provide the platform-specific `/story dashboard` and `$story dashboard` entry points.

## Routing Process

1. Analyze the user's request and extract intent keywords.
2. Match those keywords against the table and identify the appropriate skill.
3. If the match is clear, invoke the skill directly. Claude and OpenCode may use `Skill("skill-name")` or a slash command; Codex uses `$skill-name` or `/skills`; Antigravity uses `/skills` or a natural-language skill name; OpenClaw uses `/skill skill-name` or a natural-language skill name.
4. If no route matches, ask the user what they want to do and offer choices from the table.
5. If the user says “I want to write a novel” without choosing long-form or short-form, ask for the intended length before routing.

## Query Fallback

> Spawn-version notice (does not block spawning): first read the project root's `.story-deployed` file and retrieve `agents_version`. If it does not match this release's `agents_version: 29`—because the marker is missing, the field is missing or not an integer, or the value is lower or higher than 29—continue checking file availability and spawning, but check only the canonical directory for the current runtime. Also report `Notice: agents bundle 版本不匹配（项目 {N}，本版 29）` and advise the user to rerun `/story-setup` and start a new conversation. If the project value is higher than 29, additionally advise the user to update oh-story-claudecode before setup so an older local setup does not overwrite it. Fall back to solo/direct execution only when the agent file is missing or the runtime does not expose custom agents; report `Fallback: ... -> solo`.

Before using an agent for “query story information” or “research a topic,” perform this lightweight availability check. The router handles only this layer and does not own the global deployment policy: confirm that the current process is not already inside a subagent, the runtime exposes Agent/Task or `invoke_subagent`, and the corresponding deployment file exists—Claude `.claude/agents/*.md`, OpenCode `.opencode/agents/*.md`, Codex `.codex/agents/*.toml`, or Antigravity `.agents/agents/agent-name/agent.md`, where `agent-name` is the target agent's name. Antigravity must use `invoke_subagent` with the matching `TypeName`; do not infer availability from files belonging to another runtime. If any check fails, or the runtime reports an unknown agent or has no custom-agent registry, fall back without hard failure:

- If `story-explorer` is unavailable, use Read/Grep in the main thread to search project files for character status, foreshadowing, progress, or specifications. Begin the response with `Fallback: agent unavailable -> direct lookup`. If the project has not been deployed, advise the user to run `/story-setup` (`$story-setup` in Codex).
- If `story-researcher` is unavailable, complete the work with the main thread's available research capabilities or suggest collecting the material through `/browser-cdp`. Again begin with `Fallback: agent unavailable -> direct lookup`.

## Project-State Awareness

Before routing, inspect the current project state:

- **No project directory** (no book directory containing `追踪/` or `设定/`):
  - If the user wants to write, run `/story-setup` first to initialize the environment (`$story-setup` in Codex).
  - If the user wants to scan rankings or decompose a story, route the request directly.
- **Existing project:** check the `.story-deployed` marker. If it is missing, run `/story-setup` first (`$story-setup` in Codex).

## Switching Between Multiple Books

When the user wants to switch books or see which books are in progress—a project can contain more than one book:

1. Search the project root for book directories containing a `追踪/` or `设定/` subdirectory, including book directories below `长篇/` and `短篇/`.
2. List the book names and identify the book referenced by `.active-book` as active.
3. Ask the user to choose a book, then overwrite the project root's `.active-book` with that book's relative path.
4. If only one book is found, confirm it as active without asking.

## Version Update Check

Run this procedure when the user asks whether a new version is available or requests an update or upgrade. **Only report availability. The user decides whether to update; never install automatically.**

1. **Current version:** read the `VERSION` file in the same directory as this skill. Treat a missing file as an unknown version.
2. **Latest version:** prefer `gh release view --json tagName,name,url -R zenstory-ai/oh-story-claudecode` and read `tagName`. If gh is unavailable, run `curl -fsS --max-time 5 https://api.github.com/repos/zenstory-ai/oh-story-claudecode/releases/latest` and read `.tag_name` using jq or grep. If retrieval fails, say that the latest version is temporarily unavailable and provide the [Releases](https://github.com/zenstory-ai/oh-story-claudecode/releases) page. Do not treat this as an error.
3. **Compare:** remove the `v` prefix and compare semantic versions as major.minor.patch. By default, `gh release` returns the latest stable release and excludes prereleases.
4. **Report:**
   - Already current: say “You are already using the latest version, vX.Y.Z.”
   - Update available: show current vA → latest vB and link to [Releases](https://github.com/zenstory-ai/oh-story-claudecode/releases) and [CHANGELOG](https://github.com/zenstory-ai/oh-story-claudecode/blob/main/CHANGELOG.md). Include key release notes if available. Then use AskUserQuestion to ask whether to update now:
     - If yes, run `npx skills add zenstory-ai/oh-story-claudecode -y -g`. The `-g` flag installs globally; omit it for the current project only. After completion, advise the user to rerun `/story-setup` (`$story-setup` in Codex) from the root of every previously deployed project to synchronize hooks, agents, and references, then **start a new conversation** so the agents register again.
     - If not now, make no changes and tell the user they can return to the update at any time.
