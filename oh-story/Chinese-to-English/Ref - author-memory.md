# Author Memory Protocol

Author memory stores creative preferences that can be reused across sessions; it does not store facts from a novel's world. It follows a memory pipeline of “raw evidence → candidates → confirmed profile → change log,” while leaving final decisions to the author.

## Boundaries and Priority

Load information in this order, from highest to lowest priority:

1. Hard gates such as safety, platform, word-count, and file protocols;
2. Explicit requirements in the user's current request;
3. The current book's `设定/文风.md`, genre positioning, detailed outline, and other project settings;
4. Book-specific preferences in author memory;
5. Genre, workflow, and global preferences in author memory;
6. Comparable materials, general methods, and defaults.

Author memory must not store book facts in `.story/作者记忆/`, override the current request, lower the review rubric, or allow de-AI editing to alter plot intent. Novel facts remain managed in each book's `追踪/` and `设定/` directories.

## Files and Ownership

Workspace-level directory:

```text
{工作区}/.story/作者记忆/
├── _author-memory-state.json  # 唯一结构化权威
├── 作者画像.md               # 仅 active，供作者查看与管理
├── 待确认.md                 # pending / conflict，不参与约束
└── 变更记录.md               # 最近 100 次、最新在前的事务记录
```

All three Markdown files are generated deterministically from the state file and must not be edited manually. The state retains the complete history, while the change log displays only the 100 most recent transactions. `作者画像.md` is the human management view. Ordinary writing agents do not inject the entire file; they call `query` to retrieve compact context relevant to the current task. If author memory does not exist, ordinary writing, review, and de-AI tasks continue without automatically creating an empty directory. The first `record` transaction creates it.

The workspace must be passed to the script explicitly. Prefer the nearest ancestor that already contains `.story/作者记忆/`. During first-time initialization, use the root of the creative workspace that contains multiple books, `.active-book`, `长篇/`, `短篇/`, or `拆文库/`. Do not use the user's home directory as the default workspace.

## When to Read It

Before beginning long-form fiction, short-form fiction, or de-AI editing, if the state exists, use `query` to filter active entries by book, genre, workflow, and kind. Query output is capped at 2,048 bytes. Do not query everything and make the agent filter it afterward; select kinds directly for the task:

| Task | query kinds | Injection point |
|---|---|---|
| Drafting / continuation | `prose_style` + `story_design` | Main session and the agent writing the actual prose |
| De-AI editing / rewriting | `prose_style` | Main session and the agent performing the rewrite |
| Settings / outline | `story_design` + `workflow` + `interaction` | Main session only; do not pass to the prose agent |
| Review | `delivery` + `interaction` + necessary `prose_style` | Main session only; do not lower the rubric |

Matches during review are used only for delivery format, collaboration style, and explanations of “expressive choices intentionally made by the author.” Issue severity and PASS/FAIL remain determined by the rubric.

Pending items do not become prompt constraints and should not interrupt the current task for confirmation. Present them together only when the user asks to view the author profile, candidates have accumulated to a suitable review point, or a new preference conflicts with an active entry.

## Reliability and Load Boundaries

- Explicit requests to “remember / confirm / replace / forget” go through a single-event `record`; the agent does not need to read the revision manually or assemble a multi-operation transaction. A successful response returns `Author Memory Receipt: rN · APxxx`. Without a receipt, do not claim that the preference has been remembered.
- Ordinary creative work performs only one local `query`. If no state exists, it returns an empty result and creates no files. When memory exists, it returns only relevant active entries, with a hard limit of 2,048 bytes. The full profile, evidence, candidates, and journal do not enter the prose prompt.
- Query results are low-priority tendencies, not a checklist. Absorb them naturally. Do not recite the profile, deliberately maximize literal term matches, or sacrifice coherence, pacing, word count, or the book's established voice to satisfy a preference.
- Do not install a prompt hook that records every user message. The agent must still decide whether natural-language input represents a lasting habit. This cannot promise 100% capture of implicit preferences, but it avoids silently writing one-time requests, private conversations, and novel facts into long-term memory. When reliable storage is needed, the user can explicitly say “记住：……,” then verify the receipt.

## Capture Decisions

| Input evidence | Handling |
|---|---|
| Direct, stable, clearly scoped statements such as “以后都这样” or “我一直习惯……” | `active`, `source=explicit_user` |
| The user explicitly accepts a long-term practice proposed by the assistant | `active`, `source=accepted_suggestion` |
| Similar corrections recur, but the user has not said they are a lasting rule | `pending`, `source=repeated_correction` |
| A pattern inferred from completed work or operating history | `pending`, `source=inferred_pattern` |
| One-time requests such as “这一章别……” or “这次给我……” | Execute only; do not record |
| Characters, timelines, foreshadowing, worldbuilding, and the current plot direction | Write to project settings/tracking, not author memory |
| Assistant-generated text, default templates, tool warnings, and rubric conclusions | Do not self-learn |

Preserve the user's negations, qualifications, and scope. Put the exact original wording in `quote`; `assertion` may only be a compact summary that does not change the meaning. Scope rules:

- “本书 / 这个角色 / 这次连载” → `book`;
- “都市文 / 这类题材” → `genre`;
- Operating habits involving delivery, checking, or confirmation cadence → `workflow`;
- “以后 / 一贯 / 我习惯” without a narrower qualification → `global`;
- Potentially stable but ambiguous scope → use the narrowest reasonable current scope and set it to `pending`.

Available kinds: `prose_style`, `story_design`, `workflow`, `delivery`, and `interaction`. Confidence and importance each use `low | medium | high`.

## Conflicts, Retractions, and Reinforcement

- When the same kind, scope, and summarized text appears again, the script reinforces the original entry by adding evidence and confirmation counts instead of creating a duplicate.
- When a new preference contradicts an active entry, record it first as a `conflict` candidate and list the conflicting IDs in `conflicts_with`. The current task still follows the explicit request in the present turn.
- When the author selects the new rule, use `replace` to activate the new entry and mark the old one `superseded` in a single operation.
- A pending item can use `decide=activate|reject`; a conflict candidate cannot bypass the old rule and activate directly.
- When the author says “忘掉 / 这不再是我的习惯,” use `forget`. Retain the historical evidence, but no longer load the entry.
- The meaning of an active entry must never be silently edited in place. Semantic changes require `replace` so the history remains auditable.

## Running the Tool

Try `python3`, `python`, and `py -3` in that order to find Python 3, then run the local copy from the current skill root:

```text
{PYTHON} {当前 skill 根}/scripts/author_memory_commit.py init   --workspace {工作区}
{PYTHON} {当前 skill 根}/scripts/author_memory_commit.py record --workspace {工作区} --input {单事件.json}
{PYTHON} {当前 skill 根}/scripts/author_memory_commit.py query  --workspace {工作区} [--kind prose_style] [--book {书名}] [--genre {题材}] [--workflow {流程}]
{PYTHON} {当前 skill 根}/scripts/author_memory_commit.py commit --workspace {工作区} --input {事务.json}
{PYTHON} {当前 skill 根}/scripts/author_memory_commit.py check  --workspace {工作区}
```

- `record`: The standard single-event entry point. It reads the current revision automatically and initializes storage on first use. If an identical `event_id` and payload recur, it idempotently returns the original receipt; if the content differs, it fails.
- `query`: Reads only relevant active entries. `--kind` can be repeated. If no state exists, it returns an empty result with zero writes. If the result reports `omitted > 0`, narrow kind / book / genre / workflow and query again; do not evade the budget by reading the full profile.
- `commit`: The advanced batch entry point. It validates the schema, references, capacity, and every view in memory before atomically replacing the state. The transaction file must remain in place until success. A stale revision fails before any write.
- `check`: Rebuilds every derived view from the state and verifies it byte for byte.

## Transaction Format

Standard single-event creation or reinforcement:

```json
{
  "schema_version": 1,
  "event_id": "conversation-2026-08-25-message-42",
  "operation": {
    "action": "remember",
    "preference": {
      "kind": "prose_style",
      "scope": {"level": "global", "value": null},
      "assertion": "对话尽量短，用动作承接情绪，不用大段解释",
        "quote": "以后对话都短一点，情绪放动作里，别让角色长篇解释。",
        "source_ref": "conversation:2026-08-25",
        "source": "explicit_user",
        "confidence": "high",
        "importance": "high",
      "status": "active",
      "reason": "用户以“以后”明确声明长期偏好",
      "conflicts_with": []
    }
  }
}
```

Pass the file to `record`. For an item awaiting confirmation, use `pending` as its `status`; for a conflict candidate, use `conflict` and supply the active ID. To confirm or reject a candidate, pass the following object as the new event's `operation`:

```json
{"action":"decide","item_id":"AP002","decision":"activate","quote":"对，这就是我的长期习惯。","reason":"作者明确确认"}
```

When replacing one or more old entries with a new rule, `replace.preference` uses the same fields as the earlier example, but omit `status` and `conflicts_with`; the new entry becomes active immediately. The following object is likewise passed as `operation`:

```json
{
  "action": "replace",
  "old_ids": ["AP001", "AP002"],
  "preference": {
    "kind": "prose_style",
    "scope": {"level": "book", "value": "雾港来信"},
    "assertion": "本书对话允许更长的试探，但避免解释设定",
    "quote": "这本书可以让对话慢一点，多试探，但还是别拿台词讲设定。",
    "source_ref": "conversation:2026-08-25",
    "source": "explicit_user",
    "confidence": "high",
    "importance": "high",
    "reason": "作者明确用本书新规则替代旧候选"
  }
}
```

To retract an entry, use this `operation`:

```json
{"action":"forget","item_id":"AP003","quote":"忘掉这个偏好。","reason":"作者明确撤回"}
```

Use the advanced `commit` only when multiple actions must be bound into one atomic commit. At the top level, pass `schema_version`, a unique `transaction_id`, the current `expected_state_revision`, and `operations` containing 1–32 items. Operations are applied in array order; if any step fails, the entire transaction performs zero writes. Delete the temporary input file after success. For an explicit memory request, also relay the receipt returned by the tool verbatim to the user.
