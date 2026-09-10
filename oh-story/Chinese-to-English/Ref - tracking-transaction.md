# Tracking-State Protocol

`追踪/` uses “one authoritative structured state + multiple deterministic derived views.” The model submits only one semantic JSON document rather than separately using `Write/Edit/echo >>` on multiple tracking files.

## Authoritative and Derived Layers

| Layer | File | Semantics |
|---|---|---|
| Sole authority | `_tracking-state.json` | Schema, last committed chapter, import cutoff chapter, state revision, context structure, characters/foreshadowing/timeline, and concise word-count records for committed chapters |
| Chapter record | `逐章记录/第NNN章.md` | Compact changes useful to future continuity; target ≤1,536 bytes, hard limit 3,072 bytes; revisions within the imported range are written as replacement records |
| Derived views | `上下文.md`, `角色状态/{角色名}.md`, `伏笔.md`, `时间线/作者真相.md`, `时间线/读者已知.md` | Generated entirely from `_tracking-state.json`; manual editing is prohibited, and programs do not use them as input |

Markdown exists only for authors and agents to read; tools no longer parse Markdown back into state. `check` rerenders directly from `_tracking-state.json` and compares every file byte for byte. Future plans for “which chapter reveals this” belong in volume/detailed outlines, not in the timeline as accomplished facts.
Chapter records are compact change logs for human readability; they do not promise lossless reconstruction of the entire current state on their own. `_tracking-state.json` is authoritative for complete current semantics.

## Runtime Tools

First detect a Python 3 interpreter for the runtime (try `python3`, `python`, then `py -3`). The tracking-transaction script uses the current skill root; word count and chapter closure consistently use the `story-long-write` skill root:

```text
{PYTHON} {当前 skill 根}/scripts/tracking_commit.py init   --project {书项目根} --input {初始化事务.json}
{PYTHON} {当前 skill 根}/scripts/tracking_commit.py check  --project {书项目根}
{PYTHON} {story-long-write skill 根}/scripts/storyctl.py wordcount checkpoint --file {前半段临时文件} --target {目标} --chapter {N}
{PYTHON} {story-long-write skill 根}/scripts/storyctl.py chapter check   --project {书项目根} --chapter {N}
{PYTHON} {story-long-write skill 根}/scripts/storyctl.py chapter commit  --project {书项目根} --chapter {N} --input {逐章事务.json}
{PYTHON} {story-long-write skill 根}/scripts/storyctl.py chapter accept-current-length --project {书项目根} --chapter {N} --input {逐章事务.json}
```

- `init`: Run only when `_tracking-state.json` does not exist; never overwrite an initialized project.
- `wordcount checkpoint`: Measurement only; returns the current actual length, user band, and remaining user range. It does not write manuscript text or tracking data and makes no semantic judgment. Invoke at most once per chapter.
- `chapter check`: Rereads the current manuscript and detailed-outline target, then returns deterministic length status, current blocking quality results, `state_revision`, and currently permitted actions without saving approval. `under` offers no automatic expansion; `over` additionally returns one net-deletion `compress-once` action and the machine-calculated deletion ranges required to enter the inner or user band.
- `chapter commit`: Rereads the current files, recounts, and reruns blocking quality; accepts only chapters inside the user band and atomically commits the concise word-count record with the chapter transaction.
- `chapter accept-current-length`: Accepts only out-of-band chapters that pass quality; when acceptance occurs, it rereads, recounts, and commits atomically at once rather than preserving a stale historical decision.
- `check`: Strictly validates the state schema, chapter-record continuity/canonical names/size, the fixed seven sections, character-snapshot hard limits, the derived-file set, and byte-for-byte consistency between every derived view and state.

Each book serializes write transactions through `追踪/.tracking-commit.lock`; `expected_state_revision` also rejects stale transactions constructed from an old state. When two different transactions run concurrently, at most one revision succeeds. Under the same lock, word-count records are revalidated against the current manuscript and target, so changes to either cause a preconstructed record to fail immediately.

Transaction JSON is temporary input, not a project artifact: retain it until success, then delete it immediately after the commit and the following `check` pass. Never leave inputs such as `init_transaction.json` or `chapter_*_transaction.json` in the book-project root. If file writing fails, `_tracking-state.json` has not advanced; fix the environment and rerun the **same** `commit`. A repeated append accepts an existing chapter record only when its content is identical; there is no `dirty/pending/repair` state machine.

Handle validation failures differently from write failures: For validation failures (invalid fields, retired structures, excess capacity), correct the transaction itself; rerunning the same result will not change anything. If a manually or externally modified derived view makes `check` report `derived view differs from _tracking-state.json`, resubmit **that chapter's** `mode=revision` transaction so the tool rebuilds everything. Take `expected_state_revision` from the `state_revision` field in `追踪/_tracking-state.json`—when `check` fails, it writes only ERROR to stderr and emits no JSON. Never edit derived files manually or delete `_tracking-state.json` to start over. A manually written chapter record causes same-chapter `append` to fail permanently with `chapter delta N already exists with different content`; delete that handwritten file and rerun the original transaction.

The tool does not parse legacy `_tracking-meta.json`, `时间线/事件库.json`, or earlier tracking structures and provides no semantic compatibility layer. When `init` encounters such legacy files, first move them unchanged as a complete set into `追踪/_旧追踪存档/`, then create the current protocol in place. The old content remains available for author review but is not parsed; current state derives entirely from the init input. A failed `init` validation moves no files. `commit` and `check` still reject legacy structures directly—they run only on projects using the established protocol.

## Initialization Transaction

A new book initializes at Chapter 0. When `story-import` imports an existing novel, write its final complete chapter to `last_chapter=N`; do not fabricate daily-writing records for Chapters 1..N, and begin ordinary continuation at Chapter N+1.

```json
{
  "schema_version": 1,
  "book_title": "让你管账号，你高燃混剪炸全网",
  "last_chapter": 0,
  "context": {
    "position": {
      "volume": "第一卷·军宣整顿",
      "volume_start_chapter": 1,
      "story_time": "江晨到火箭军文工团报到前",
      "scene": "火箭军文工团"
    },
    "long_term_constraints": ["军宣爽点要用作品效果和围观反应链兑现，不能只靠系统播报"],
    "active_character_names": [],
    "continuity_risks": [],
    "recent_chapters": [],
    "next_chapter_commitments": ["让江晨报到，并落下五天百万粉的新手任务"]
  },
  "character_snapshots": {},
  "foreshadow": [],
  "timeline_events": []
}
```

For import initialization, pass the current central-character snapshots, current foreshadowing rows, timeline events, and fixed seven-section state input directly. Review a stage/volume by querying manuscript text when needed; it is not a strongly consistent per-chapter tracking artifact.

The caller's chapter JSON does not include `wordcount`; the formal `chapter commit` or `chapter accept-current-length` entry point generates and injects it at commit time. Final state retains only `metric / target / actual / status / resolution / body_sha256` for committed chapters; it does not preserve MEASURE/RESOLVE events, ID chains, a policy fingerprint, or independent chapter state.

## Chapter Transaction

```json
{
  "schema_version": 1,
  "mode": "append",
  "chapter": 10,
  "chapter_title": "专业团队拍得还不如他拍的好？",
  "expected_state_revision": 9,
  "delta": {
    "result": "专业团队重拍的高清版在高层看片会上被判定缺了灵魂，张耀祖拍板继续采用江晨的手机原版。",
    "character_changes": [
      {"name": "江晨", "change": "作品价值获军内高层确认，从爆款新人升为不可替代的军宣创作者"}
    ],
    "foreshadow_changes": [
      {
        "action": "upsert",
        "id": "F027",
        "summary": "专业团队仍拍不出江晨原版的灵魂，继续验证其创作能力不可复制",
        "planted_chapter": 10,
        "planned_resolution_chapter": null,
        "status": "已埋",
        "importance": "中"
      }
    ],
    "timeline_events": [
      {
        "action": "upsert",
        "id": "E010",
        "story_time": "实弹训练两天后",
        "objective_fact": "文工团高层否决专业重拍版，决定沿用江晨手机拍摄的原版视频",
        "reader_knowledge": "读者已看到周薄森指出专业版缺了灵魂，张耀祖当场拍板用回原版",
        "reveal_status": "已揭示",
        "reveal_chapter": 10,
        "characters": ["江晨", "周薄森", "张耀祖"]
      }
    ],
    "constraints": ["后续继续用作品落地效果和围观反应放大江晨的高光，不能只写系统奖励数字"],
    "next_chapter_commitments": ["结算五天百万粉任务，并承接老兵主题的新任务"]
  },
  "context": {
    "position": {
      "volume": "第一卷·军宣整顿",
      "volume_start_chapter": 1,
      "story_time": "实弹训练两天后",
      "scene": "火箭军文工团高层看片会"
    },
    "long_term_constraints": ["军宣爽点要用作品效果和围观反应链兑现，不能只靠系统播报"],
    "active_character_names": ["江晨"],
    "continuity_risks": ["钟嘉嘉说江晨只猜对一半，未公开的培养安排不能被当成读者已知事实"]
  },
  "character_snapshots": {
    "江晨": {
      "identity": "火箭军文工团宣传兵；军宣爆款创作者",
      "location": "火箭军文工团高层看片会",
      "goal": "完成五天百万粉任务，持续做出真正能打的军宣内容",
      "state": "专业团队反向验证原版价值，军内认可继续抬升",
      "abilities_resources": ["前世MCN爆款运营经验", "《中国军魂》伴奏", "大师级导演能力"],
      "relationships": ["钟嘉嘉持续提供军报资源", "周薄森和张耀祖已明确认可其创作能力"],
      "knowledge": ["《军报》采访稿已经过审", "原版视频将继续作为正式军宣内容"],
      "open_threads": ["五天百万粉任务尚未结算", "钟嘉嘉所谓只猜对一半仍未解释"]
    }
  }
}
```

Constraints:

- Run `check` before constructing a transaction and copy the current `state_revision` unchanged into `expected_state_revision`; if state has changed, reread it and reconstruct the transaction.
- The fields permitted under `context` differ by subcommand: `init` accepts `position`, `long_term_constraints`, `active_character_names`, `continuity_risks`, `recent_chapters`, and `next_chapter_commitments`; `commit` accepts only the first four. During commit, the tool derives `recent_chapters` and `next_chapter_commitments` from the current view and this chapter's `delta`; supplying them manually is rejected before any write (`context contains unsupported fields: ...`, exit 2). Copying the init example into a commit transaction is the easiest mistake to make.
- Characters appearing in `character_snapshots` are treated as central reusable characters and must also appear in `character_changes`; when an established central snapshot changes again, submit a new snapshot.
- The four lists in a character snapshot have no item-count limit, only per-item length and final-file byte limits: target ≤4,096 bytes; warning above that; hard limit 8,192 bytes, with rejection before any write.
- A changed character without a snapshot is treated as temporary and receives no state file; `context.active_character_names` allows at most six people, each with an existing current snapshot.
- `context.long_term_constraints` and `context.continuity_risks` are the complete current values. Every item present in the prior version but absent now must be listed individually in `delta.retired_context_items`, or the tool rejects the transaction before any write—omission is not treated as deletion. The tool writes genuinely retired items to `## 本章退役登记` in this chapter's record, where they remain reviewable.
- Put central characters no longer in reuse into `delta.retired_characters`: The tool deletes their current snapshot and `角色状态/{角色名}.md` while retaining a record in the chapter log. A transaction cannot both retire a character and submit their snapshot, nor can it retire someone still listed in `context.active_character_names`. In the chapter where a character dies/exits, still record the change in `character_changes`; a character retired in that chapter need not receive a new snapshot that would be deleted immediately, and the chapter record still labels them as central. Retirement only means leaving hot context; manuscript text and chapter records remain unaffected.
- Both retirement types are permitted only in `mode=append`. Retirement means “leaves current state from this moment forward,” while a revision transaction's chapter record belongs to a rewritten earlier chapter and would falsely report the retirement there. A `mode=revision` transaction must resubmit every current context item unchanged; place any retirement in the next append.
- `伏笔.md` shows only the current state of foreshadowing that has actually been planted. Future plans remain in the outline.
- `timeline_events.action` may be `upsert/delete`. For `未揭示`, `reveal_chapter` must be `null`; partial/full reveals may contain only an actual chapter that has occurred.
- Under `mode=revision`, recalculate the chapter record as the complete continuity record that remains true for that revised chapter; submit the current values, through the latest written chapter, for affected characters, foreshadowing, timeline, and context.
- Revising manuscript text inside the import cutoff adds or replaces that chapter's record; `imported_through_chapter` remains unchanged.

## Fixed Format for the Continuation Status Card

`上下文.md` is ≤12,288 bytes, generated as a whole from state, and contains only these seven top-level sections:

1. `## 当前位置`
2. `## 长期约束`
3. `## 核心角色状态`
4. `## 活跃伏笔`
5. `## 近三章速记`
6. `## 下一章承诺`
7. `## 连贯性风险`

At most six active characters, eight deterministically selected active foreshadowing items, and three recent chapters appear here. These limits apply to hot context for the next chapter, not to the total capacity of complete character state.
