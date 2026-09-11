---
name: story-review
version: 1.1.1
description: "Multi-perspective adversarial review. In full/lean mode, spawns deployed reviewer agents in parallel. Automatically falls back to solo when agents are missing/malformed or spawning fails, and uses the embedded rubric fallback when reference files cannot be read. Triggers: /story-review, /审查, ‘review this,’ or ‘help me review this.’"
metadata: {"openclaw":{"source":"https://github.com/zenstory-ai/oh-story-claudecode"}}
---
# story-review: Multi-Perspective Adversarial Review

> Spawn version notice (does not block spawning): First read `agents_version` from `.story-deployed` in the project root. If it does not match this release’s `agents_version: 29`—including a missing marker, missing/non-integer field, or a value below or above 29—**continue checking file presence and spawning as usual**, but only in the current runtime’s canonical directory. Also report `Notice: agents bundle 版本不匹配（项目 {N}，本版 29）` and advise rerunning `/story-setup` and starting a new session. If the value is above 29, additionally advise updating oh-story-claudecode first instead of using the older local setup to overwrite it with a downgrade. Fall back to solo/direct only when the agent file is missing or the runtime does not expose custom agents; report `Fallback: ... -> solo`.

You are the review coordinator. Find structural, character, prose, and setting problems in novel text and provide executable revision recommendations.

**Iron rule: A review looks for problems; it does not validate correctness.**

## Boundary for Author Habits

If author-memory state exists, run `scripts/author_memory_commit.py query` before review to retrieve relevant active entries (total output ≤2KB). They may help interpret intent and organize the report, but cannot reduce rubric severity, classify a factual conflict as harmless, or bypass platform gates. The current request still takes priority. See [references/author-memory.md](references/author-memory.md).

If the user makes a stable declaration about report format or collaboration style, save it after this review using `record` and return the receipt. Ask before recording repeated corrections or inferred preferences; do not record one-off requirements. Never auto-learn review findings, tool warnings, or the assistant’s recommendations.

---

## Choose Review Mode

- `/story-review` or `/story-review full` → Prefer spawning all four Agents. If already inside a subagent, required Agents are undeployed/malformed, or spawning fails, fall back automatically to solo.
- `/story-review lean` → Prefer spawning `story-architect` + `consistency-checker`. If already inside a subagent, either required Agent is undeployed/malformed, or spawning fails, fall back automatically to solo.
- `/story-review solo` → Spawn no Agents; the current session performs the baseline review.
- Unspecified → default to full and record the actual effective mode in the report.

---

## Phase 0: Preflight and Fallback (Run First)

1. **Determine requested mode**: Parse `full`, `lean`, or `solo`; default target is `full`.
2. **Confirm spawning is allowed**: If already running inside a subagent/Agent, do not recursively spawn; fall back to `solo`.
3. **Recognize the ZCode boundary**: If running under ZCode and the project uses `.zcode/`, ZCode 3.3.4 does not execute project/plugin custom agents. Do not attempt matching spawns based on other runtimes’ files; fall back to `solo` and report `Fallback: project custom agents unavailable -> solo`.
4. **Check required Agent deployment** in the current runtime’s canonical directory only; never infer from another runtime:
   - Claude Code: `.claude/agents/`; OpenCode: `.opencode/agents/`; Codex: `.codex/agents/`; Antigravity: `.agents/agents/`
    - full requires `story-architect`, `character-designer`, `narrative-writer`, `consistency-checker`
    - lean requires `story-architect`, `consistency-checker`
    - For every required Agent file:
      - **Claude Code agent (`.claude/agents/`)**: Read frontmatter and confirm `name:` exactly matches subagent_type. Missing/unparseable frontmatter or a mismatch means malformed.
      - **OpenCode agent (`.opencode/agents/`)**: Filename is the agent name; OpenCode does not require `name:` in frontmatter. Confirm parsable frontmatter with `mode: subagent` and a `permission` field. Missing/unparseable frontmatter means malformed.
      - **Codex agent (`.codex/agents/`)**: Filename is `{agent}.toml`. TOML must parse and contain `name`, `description`, and `developer_instructions`; `name` must exactly match the target.
      - **Antigravity agent (`.agents/agents/`)**: Path is `.agents/agents/agent-name/agent.md` (`agent-name` is the target name). Frontmatter must parse, `name` must match, `mainAgent: false`, `subagent: true`, and `tools` must be nonempty. Missing/mismatched fields mean malformed.
   - If any Agent required for the target mode is missing or malformed, **do not spawn missing/bad Agents**. Fall back automatically to `solo`. At the report start, write `Fallback: missing agents -> solo` or `Fallback: malformed agents -> solo`, list problem files, and recommend `/story-setup`.
5. **Confirm Agent tools are available**: Claude/OpenCode/Codex need their runtime subagent/Task mechanism; Antigravity needs `invoke_subagent`. If unavailable, fall back to `solo` and report `Fallback: agent tool unavailable -> solo`.
6. **Runtime-failure fallback**: If any spawn fails, a `subagent_type` / `agent_type` / `TypeName` is unavailable, frontmatter/TOML fails at runtime, or an Agent cannot start, stop further spawns and redo the review as `solo`. Report `Fallback: spawn failed -> solo` and the failed agent name. Never combine partially successful Agent results as a full/lean conclusion.
7. **Determine effective mode**: The report must list both `Requested Mode` and `Effective Mode`.

---

## Review Standards and Reference Rules (Mandatory)

The core standards for `story-review` must always be available. Reference files enhance the process; they are not prerequisites.

### Report Metadata Keys (Output Verbatim)

At the start of the final report, output these English keys line by line. **Do not translate, rename, or replace them with Chinese equivalents.** Chinese explanations may follow, but the exact keys must remain for scripts and users to verify execution:

```md
Requested Mode: full | lean | solo
Effective Mode: full | lean | solo
Fallback: none | project custom agents unavailable -> solo | missing agents -> solo | malformed agents -> solo | agent tool unavailable -> solo | spawn failed -> solo | subagent recursion guard -> solo
Rubric: fanqie | qidian | zhihu | generic web-fiction
Rubric Source: file | embedded fallback
```

### Reference Resolution Order

When references are readable, try these locations in order and use the first match:
1. `{项目根}/.claude/skills/{规范路径}` (Claude Code project installation)
2. `{项目根}/.opencode/skills/{规范路径}` (OpenCode project installation)
3. `{项目根}/.codex/skills/{规范路径}` (Codex project installation)
4. `{项目根}/.zcode/skills/{规范路径}` (ZCode project installation)
5. `{项目根}/skills/{规范路径}` (OpenClaw / Reasonix / generic deployment and this repository’s development environment)
6. `{项目根}/.agents/skills/{规范路径}` (Antigravity’s actual project skill root; Codex / Reasonix may also scan it or its symlink)
7. The directory from which the current runtime loaded this skill, or a matching `{skill-name}/...` under its accessible global skill search path

> It is normal for earlier locations to be absent; that is not deployment damage. `/story-setup` physically copies 13 skills into `.agents/skills/` for Antigravity, `.zcode/skills/` for ZCode, and `skills/` for OpenClaw / Reasonix / generic. Codex project deployment does not copy the skill itself; Codex loads it from a skill root, so references typically resolve at level 6 or 7. Do not manually copy `references/` into `.codex/skills/`; story-setup will not manage that copy and it silently becomes stale after upgrades.

Canonical paths follow. Never use a bare filename or read another skill’s references by mistake:

| Purpose | Canonical Path |
|---|---|
| General quality checklist | `story-review/references/review-quality.md` |
| General content-scoring rubric | `story-review/references/quality-rubric.md` |
| AI-flavor removal method | `story-review/references/anti-ai-writing.md` |
| Plot cycle/climax formula | `story-review/references/plot-core-methods.md` |
| Character relationships/affinity | `story-review/references/character-relations.md` |
| Dialogue quality | `story-review/references/dialogue-mastery.md` |
| Review banned terms | `story-review/references/banned-words.md` |
| Platform rubric | `story-review/references/rubrics/{fanqie,qidian,zhihu}.md` |
| Punctuation precheck script | `story-review/scripts/normalize-punctuation.js` |
| AI-pattern precheck script | `story-review/scripts/check-ai-patterns.js` |
| Author-habit protocol | `story-review/references/author-memory.md` |
| Author-habit transaction script | `story-review/scripts/author_memory_commit.py` |

### Embedded Review Baseline (Required When Paths Are Unreadable)

If those files cannot be read, **do not run without a rubric or say “unable to load the specific rubric” and stop applying standards**. Use this embedded baseline and report `Rubric Source: embedded fallback`.

General web-fiction content rubric:
- Core promise: Does the chapter advance a clear promise? If no promise is discernible, at least S2.
- Conflict progression: Does the chapter contain an obstacle, choice, cost, or relationship change? Pure explanation/chat/summary is at least S2.
- Task obstacle: When a character’s attempt is blocked, does the obstacle change information, relationships, cost, choice, or foreshadowing? If only process detail remains and deletion changes nothing, at least S3.
- Emotional curve: Is there setup, escalation, release, or reversal? Flat or abrupt emotion is at least S2/S3.
- Hooks and expectations: Does the opening or ending create a future question? No suspense or incomplete expectation is at least S2.
- Opening freshness (opening/first three chapters only): Does the opening use a specific character/situation angle, or a genre-default template transferable to any similar book? “Has a hook/doesn’t open with weather” does not exempt homogeneity. A formulaic opening is at least S3 even with a hook; a fully generic genre template is S2.
- Character motivation: Does behavior fit goals, personality, circumstances, and relationship pressure? Distortion for plot convenience is S1/S2.
- Dialogue quality: Is there subtext, information control, and character differentiation? Expository dialogue is at least S2.
- Setting consistency: Does it respect established rules, timeline, and character attributes? Explicit factual conflict is usually S1.
- Prose naturalness: Is it concrete and sensory, with action carrying information? Grade AI phrasing, clichés, and summary voice S2/S3 by impact.
- Sentence rhythm: Narration normally uses longer comma-linked sentences, connecting 2–4 actions before a period. Fragments and telegraph prose—repeated ≤5-character comma segments or outline-like ultra-short sentences—are as problematic as AI prose, S3/S2 by impact. Never excuse them because “short means web-fiction pacing.”
- Punctuation rhythm: Does punctuation serve tone and voice? Grade period-heavy prose, random question/exclamation piles, or `……`/`——` used to manufacture pauses S3/S2 by impact.
- Exact character-count expressions: When body text evaluates dialogue, inscriptions, letters, thoughts, or comments with phrases such as “这五个字 / 短短四字 / 三个字一落 / 八个字砸下去,” confirm the counting method, machine result, and narrative necessity. If accuracy is uncertain, treat it as a prose-naturalness issue and recommend a nonnumeric phrase such as “这句话一落,” “那几个字,” or “话音落下.”
- Format readability: Short paragraphs, dialogue on separate lines, no extra blank lines. Reading-obstructing format is S3; severe disorder is S2.
- Plot cycle: goal → obstacle → action → cost/feedback → new expectation. Missing goal/obstacle/feedback is usually at least S2.
- Climax construction: charge → false victory → collapse → reversal/payoff. A flat climax without cost or payoff is usually S2/S3.
- Relationship progression: Interaction intensity must match the current relationship stage. Sudden intimacy, trust, or hostility requires setup; otherwise S1/S2 by impact.
- Foreshadowing state: Foreshadowing must remain trackable. Density alone is only a structural-risk note unless it directly causes confusion, in which case it may reach S2+.

AI flavor / banned-term fallback:
- Stock phrases: `命运的齿轮开始转动`, `心猛地一沉`, `眼神复杂`, `深刻变化`, `踏上新的旅程`.
- Chapter-ending summary: `这一切都说明...`, `他终于明白...`, `新的篇章开始了...`.
- Information dump: A character directly says “I will explain the worldbuilding/rules/relationship change.”
- Academic/universal conclusions: excessive “然而、与此同时、不可否认、这意味着”.
- Handling: Output a finding only with source evidence. Give an executable replacement direction rather than merely saying “too much AI flavor.” Do not default to “break it shorter / delete function words / strip punctuation”; turning normal comma-linked sentences into fragments is equally problematic.

Platform fallback summaries:
- Tomato: strong opening, strong conflict, frequent payoff/emotional feedback, low comprehension burden.
- Qidian: coherent setting, advancement path, long-range expectations, worldbuilding capacity.
- Zhihu Yanyan: short-form hooks, reversal density, emotional payoff, information-gap progression.

### Rules Passed to Subagents

In full/lean mode, the main session must place a “review-baseline summary” directly in every Agent prompt. **Do not require an Agent to read `story-review/references/*` to complete the task.** If supplemental reading is needed, use only this Skill’s `story-review/references/*`. The injected rubric summary and unified Findings Schema are final authority.

### Cross-Batch Review Persistence Contract (All Modes)

Whenever a multi-chapter/volume/book review is split into two or more batches, full, lean, and solo all maintain **{项目根}/.story-review/state.md**:

1. In the first batch, define the complete review scope and batch order. After each batch’s consolidated judgment, atomically rewrite state.md through a temporary sibling file + rename; do not leave results only in chat.
2. state.md stores only full scope, completed range, next batch, and “unresolved findings from prior batch.” Each summary item retains location, issue, and expected review/payoff range.
3. Before the next batch, read state.md and inject unresolved items into reviewer prompts. Do not inherit resolved items or those the user explicitly declines, but mention their disposition in the current output.
4. Maintain only one cross-batch review per project. If a new review differs from the unfinished scope in state.md, explain which old progress would be discarded and obtain confirmation; after confirmation, overwrite it when the new first batch completes. When resuming, if state.md is missing/damaged or the current batch exceeds its declared scope, report and stop rather than guessing. Do not create state.md for a non-batched review.

**.story-review/** stores review state only, not story facts. Never use it to modify manuscript, setting, outline, or `追踪/`.

---

## Phase 1: Collect Material for Review

1. **Determine scope**:
   - If the user names chapters/files, review only those.
   - Otherwise, prefer recently modified manuscript/setting/outline files from `git diff --name-only`; if none, review the current chapter of the active book.
2. **Scope-passing strategy**:
   - Prefer file paths, chapter names, and line ranges in reviewer prompts; do not copy an entire book or many chapters into every prompt.
   - A single file or short passage may include a 300–1,200-character excerpt.
   - Multi-chapter/volume/book reviews must be batched by chapter or file group, producing independent findings before synthesis.
   - **Cross-batch continuity (required)**: Before every batch, read current rows in `追踪/伏笔.md` with status `已埋` and planned payoff chapter ≤ the batch’s final chapter; as needed, read related `追踪/逐章记录/第NNN章.md` for causes. Also read snapshots for involved characters and inject unresolved findings from prior state.md as “inherited open items.” Newly found unregistered open hooks are maintenance candidates only; they require manuscript evidence before entering a revision transaction at closure.
   - **Out-of-order/overlap reminder**: If a later range was reviewed first (for example, 300–400) and an earlier range (200–300) is reviewed later, warn that “changes in 200–300 may affect the reviewed 300–400” only when the current batch **adds/changes an open item whose expected payoff falls inside that later reviewed range**. Let the user choose: rereview affected chapters / full rereview / record as a to-do. **Default to a to-do; do not blindly rerun everything.** Do not warn without a specific cross-range dependency.
3. **Read supporting material**: Manuscript, relevant setting, character dossiers, outline, tracking context, and foreshadowing. Mark evidence gaps in the report.
4. **Identify target platform and load rubric**:
   - Prefer a platform explicitly named by the user.
   - Otherwise, read `目标平台` / `平台` from project files such as `设定/题材定位.md`, `大纲/`, or `拆文报告`.
   - Never use `.active-book` as a platform source; it only helps locate the current book directory.
   - Tomato → prefer `story-review/references/rubrics/fanqie.md`; otherwise embedded Tomato summary.
   - Qidian → prefer `story-review/references/rubrics/qidian.md`; otherwise embedded Qidian summary.
   - Zhihu Yanyan → prefer `story-review/references/rubrics/zhihu.md`; otherwise embedded Zhihu summary.
   - Unidentified → prefer `story-review/references/quality-rubric.md`; otherwise embedded general rubric. Report `Rubric: generic web-fiction` and `Rubric Source: file | embedded fallback`.
5. **Build the review-baseline summary**: Compress loaded files or fallback into 5–12 review criteria. Both solo and Agents must use it. Preserve the sentence-length standard: narration defaults to comma-linked long sentences; fragments and telegraph prose are as serious as AI phrasing and are not excused for being “short.”
6. **Deterministic precheck (report only, never edit)**: When scope contains local manuscript paths, run:
   ```bash
   node scripts/normalize-punctuation.js --check <正文文件...>
   node scripts/check-ai-patterns.js --check --fail-on=blocking <正文文件...>
   node scripts/check-degeneration.js --check <正文文件...>
   ```
   - Merge `ellipsis`, `double-hyphen`, and `markdown-divider` into `format` findings. For `em-dash`, use only the semantic rewrite recommendation from `check-ai-patterns.js`; deduplicate and discard `normalize-punctuation.js`’s same-location mechanical replacement so two conflicting findings do not appear. Also inspect punctuation rhythm manually; scripts do not replace judgment about period-heavy or randomly piled punctuation.
   - Merge `check-ai-patterns.js` findings into `prose`. For an `em-dash`, use only its semantic rewrite recommendation. Treat all severity=blocking categories as S2 (currently `not-is-comparison` / `em-dash` / `voice-contrast` / `negation-parade` / `reverse-not-is` / `trailer-ending` / `trailer-summary`). Use detector recommendations directly: remove negative setup/contrast voice/parallel negation/trailer endings/state-summary endings, state the latter point or concrete action directly, and rewrite dashes by function as actions/short sentences/commas/colons.
   - Treat all other prose findings as S4. Flag reading-experience risk without replacing human judgment; mark functional writing `[需复核]` and preserve it. See `anti-ai-writing.md` for all categories and fixes.
   - `check-degeneration.js` reports character-level repetition/truncation/placeholders/leaked engineering terms, with `severity: blocking|advisory`. Treat blocking repetition/truncation/tier-1 engineering terms as S1/S2 `prose` findings and recommend “regenerate this passage, do not rewrite it.” Treat advisory tier-2 chapter/ambiguous terms as S4.
   - All three prechecks are read-only. `story-review` **does not modify manuscript, settings, or outlines**; recommend `/story-deslop` for automatic prose repair. In full/lean mode, only “Tracking Maintenance” below may modify `追踪/`. All modes may write **.story-review/state.md** for a batched review; solo writes no other project content.
   - Default to `--quote-mode keep` so Zhihu Yanyan `「」` is not flagged. Check a specific quotation style only when the project explicitly requires it.

**Optional story-explorer prequery**: Only when `Effective Mode` remains `full`/`lean`, spawning is allowed, and Agent tools are available may you confirm `story-explorer` in the canonical agent directory and spawn it. For Antigravity, check `.agents/agents/story-explorer/agent.md` and use `invoke_subagent` + `TypeName: "story-explorer"`. Never spawn in `solo` or under recursion guard; read/search directly. Example:

```text
项目目录：{dir}
查询类型：setting_appearances
查询参数：{审查涉及的设定关键词}
```

---

## Unified Findings Schema (Required in All Modes)

Every reviewer, including solo, uses this schema so results can be sorted and merged. `location` must use original file line numbers as displayed by tools; never renumber after removing blank lines.

For `consistency` / `factual` / `causal` / `rule_boundary` findings, `fix` states only the factual reconciliation direction (for example, “standardize as an old left-arm injury and synchronize conflicts in manuscript/setting” or “choose one source in timelines A/B”). Do not give literary-creation advice.

```yaml
- severity: S1 | S2 | S3 | S4
  category: structure | character | prose | consistency | platform | factual | format | causal | rule_boundary
  location: 文件路径:行号 或 章节/段落描述
  evidence: "引用原文或具体证据"
  issue: "问题描述"
  fix: "可执行修改建议"
```

Severity:
- **S1**: Breaks the main plot, motivation, world rules, or reader trust; fix first.
- **S2**: Clearly harms chapter impact, retention, pacing, or character credibility; fix this round.
- **S3**: Local quality problem such as wording, minor format, or local pacing; can be scheduled.
- **S4**: Recommendation or style refinement; does not block publication.

---

## Phase 2: Spawn Agents in Parallel (full/lean)

Use the current runtime’s Agent tools in parallel (Codex native subagents use `agent_type`, Claude Code compatibility uses `subagent_type`, Antigravity uses `invoke_subagent` + matching `TypeName`; follow the current CLI). Agents do not inherit parent conversation context, so every prompt must be self-contained with project path, scope, file paths, necessary excerpts, baseline summary, Rubric Source, and unified Findings Schema.

**Invocation rule**: Spawn only if effective mode remains full/lean after Phase 0. Never spawn missing Agents.

**Agent 1: story-architect** (subagent_type: story-architect)
- Used in full and lean.
- Perspective: thematic alignment, outline structure, hooks/reversals, scope control, platform expectations.
- Prompt:
  ```
  你是 story-architect，从故事架构层面审查以下内容。
  你的任务是【找问题】，不是验证正确性。以最严苛的标准审视。
  项目路径：{项目根}
  审查范围：{文件路径/章节/必要摘录}
  审查基准包摘要：{Phase 1 形成的 rubric / fallback 摘要，必须内联}
  Rubric Source: file | embedded fallback
  相关文件路径：{设定/大纲/细纲文件路径}
  继承的开放项（分批审查必填，无则写「无」）：{从 追踪/伏笔.md 提取的、预计回收章 ≤ 本批末章的已埋未回收钩子，连同上一批未解决 findings 摘要}
  可选补充参考：本 Skill 的 `story-review/references/review-quality.md`、`story-review/references/plot-core-methods.md`；若不可读，不影响审查。
  检查项：
  1. 这一章是否推进了故事主题？
  2. 大纲结构是否完整（钩子/爽点/悬念）？
  3. 情绪节奏是否合理？
  4. 钩子和反转设计质量如何？
  5. 范围控制：有无角色/设定膨胀？
  6. 剧情循环是否存在且可重复？（参照审查基准包摘要里的剧情循环原则）
  7. 高潮场景是否用了蓄能→假胜→崩解结构？（参照审查基准包摘要里的高潮构建原则）
  8. 伏笔密度、连载期待和结构信息量是否合理？（伏笔密度通常只作为 S4 结构风险，除非已造成理解混乱）
  9. 按平台 rubric 或通用内容 rubric 逐项对照，标记 PASS/FAIL。
  10. 继承的开放项里，本批本该兑现的钩子/伏笔是否落空？
  11. 开头同质化（仅当本章是全书开篇/前 3 章）：开局切口是不是同题材的默认套路（穿越即退婚、系统绑定、末世第一天、开场即打脸等），能不能原样换到任意同类书？"有钩子/非天气开场"不等于不同质。对照 references/plot-core-methods.md「噱头分类与开篇流程」判断——能整体换到同类书=同质化（撞题材模板至少 S2；套路化但有具体人物/处境微差 S3）。
  12. 结尾总结：章尾是总结/升华/复述式收尾（"就这样……""他终于明白……""这一夜注定……"），还是落在动作/画面/悬念上？检测器已判 blocking 的（`trailer-summary`）按上面「blocking 一律 S2」处理，不重复定级；检测器没覆盖的总结/升华/复述式收尾按影响定 S2/S3（改写走 /story-deslop Gate F，本 skill 只标问题不改写）。

  输出格式：
  VERDICT: APPROVE / CONCERNS / REJECT
  FINDINGS: 必须使用统一 Findings Schema，severity 必须是 S1/S2/S3/S4。
  INHERITED_ITEMS: 逐条列继承的开放项 + 已检查 / 未能检查；本批本该兑现却落空的列为 finding。
  RECOMMENDATIONS: [修改建议]
  ```

**Agent 2: character-designer** (subagent_type: character-designer)
- Used in full.
- Perspective: character-voice consistency, dialogue, arcs, relationship progression.
- Prompt:
  ```
  你是 character-designer，从角色和对话层面审查以下内容。
  你的任务是【找问题】，不是验证正确性。以最严苛的标准审视。
  项目路径：{项目根}
  审查范围：{文件路径/章节/必要摘录}
  审查基准包摘要：{Phase 1 形成的 rubric / fallback 摘要，必须内联}
  Rubric Source: file | embedded fallback
  相关角色文件：{角色设定文件路径}
  可选补充参考：本 Skill 的 `story-review/references/character-relations.md`、`story-review/references/dialogue-mastery.md`；若不可读，不影响审查。
  检查项：
  1. 角色语言风格是否与语言风格档案一致？
  2. 对话是否千篇一律或信息过满？
  3. 人物弧线是否连贯？
  4. 角色行为是否符合其动机？
  5. 对话是否有潜台词和信息控制？
  6. 爱情线好感度与 CP 行为是否匹配？（参照审查基准包摘要或本 Skill 的角色关系参考）
  7. 好感度进度是否可感知？
  8. 对话三症状（可选读 `story-review/references/dialogue-mastery.md` 自查项）：① 机械对话/问答式/句间无情绪承接；② 角色当「科普嘴」整段讲设定原理(Gate G 同样管台词)；③ 说话不分场合(高压/生死 beat 的玩笑、口头梗、插科打诨出戏)。命中按 S2/S3 报具体引用+改法。

  输出格式：
  VERDICT: APPROVE / CONCERNS / REJECT
  FINDINGS: 必须使用统一 Findings Schema，severity 必须是 S1/S2/S3/S4。
  RECOMMENDATIONS: [修改建议]
  ```

**Agent 3: narrative-writer** (subagent_type: narrative-writer)
- Used in full.
- Perspective: AI-flavor detection (including explanatory/omniscient/over-plotted voice = Pattern 8), emotional intensity, formatting, pacing uniformity, natural prose.
- Prompt:
  ```
  你是 narrative-writer，从文字质量层面审查以下内容。
  你的任务是【找问题】，不是验证正确性。以最严苛的标准审视。
  项目路径：{项目根}
  审查范围：{文件路径/章节/必要摘录}
  审查基准包摘要：{Phase 1 形成的 rubric / fallback 摘要，必须内联}
  Rubric Source: file | embedded fallback
  AI 味 / 禁用词摘要：{从 anti-ai-writing、banned-words 或内置 fallback 提取，必须内联}
  可选补充参考：本 Skill 的 `story-review/references/anti-ai-writing.md`、`story-review/references/banned-words.md`、`story-review/references/review-quality.md`；若不可读，不影响审查。
  检查项：
  1. 是否存在禁用词/套话/陈词滥调，或“像/好像/仿佛/如同”式比喻成片堆叠？
  2. 是否出现 AI 写作指纹、8 种 AI 写作模式（含模式 8 解释腔/上帝视角/安排感）或章末总结体？
  3. 格式是否合规（按戏剧单元/镜头自然断段、无机械字数切分、无空行、对话独立成行、主语节奏自然）？
  4. 标点节奏是否匹配语气/人物声线：是否通篇句号化、随机堆砌问号/感叹号，或残留 `……`/`——` 硬造停顿？正文（含对话）里的破折号是否已清理？
  5. 是否出现“这五个字 / 短短四字 / 三个字一落 / 八个字砸下去”等正文内具体字数表达？若统计口径不明、未见机器核对结果或无叙事必要，标为问题并建议改成非具体数字表达。
  6. 节奏是否均匀（有无连续多节无情绪变化）？
  7. 是否存在删掉无损的任务卡点或流程细节？若只是水/局部节奏问题标 S3；明显拖垮主线推进标 S2。
  8. 身体部位同一词是否超 5 次？
  9. AI味分级（轻度/中度/重度）及证据。
  10. 去 AI 补充复核：是否有作者解释总结/意义尾巴；是否连续堆精致戏剧反应短语；是否把已有手机/屏幕/公告/规则/证据载体改成叙述者解释；是否把任务卡点当成自然感或凑字数手段；是否机械删除了有功能的生活化/角色化比喻或短篇主观审判句。

  输出格式：
  VERDICT: APPROVE / CONCERNS / REJECT
  FINDINGS: 必须使用统一 Findings Schema，severity 必须是 S1/S2/S3/S4；AI味级别写入 issue 或 category。
  RECOMMENDATIONS: [修改建议]
  ```

**Agent 4: consistency-checker** (subagent_type: consistency-checker)
- Used in full and lean.
- Perspective: grep-first + reasoning-based consistency checking with S1–S4 output.
- Prompt:
  ```
  你是 consistency-checker，使用 grep-first + 推理型一致性审查检测事实矛盾。
  你的任务是【找事实矛盾、状态断线和需要推理才能发现的设定逻辑冲突】，不做创作评判，不评价文学质量，不输出创作修改建议。
  项目路径：{项目根}
  审查范围：{文件路径/章节/必要摘录}
  已知角色：{从设定文件提取角色列表}
  继承的开放项（分批审查必填，无则写「无」）：{从 追踪/伏笔.md 提取的、预计回收章 ≤ 本批末章的已埋未回收伏笔，连同上一批未解决 findings 摘要}
  审查基准包摘要：{Phase 1 形成的 rubric / fallback 摘要，必须内联}
  Rubric Source: file | embedded fallback
  可选补充参考：本 Skill 的 `story-review/references/review-quality.md`；若不可读，不影响事实冲突扫描。
  检查项：
  1. 角色属性是否前后一致？
  2. 世界规则是否被违反？
  3. 伏笔状态是否前后一致（已埋/计划回收/已回收/断线）？
  4. 时间线是否自洽？
  5. 术语、身份、地点、能力边界是否前后一致？
  6. 继承的开放项里，本批本该回收的伏笔是否仍悬空？

  输出格式：
  VERDICT: APPROVE / CONCERNS / REJECT
  FINDINGS: 必须使用统一 Findings Schema，severity 必须是 S1/S2/S3/S4；category 只能使用 consistency / factual / format / causal / rule_boundary。
  INHERITED_ITEMS: 逐条列继承的开放项 + 已检查 / 未能检查；本批新发现、不在 伏笔.md 的开放钩子单列，供主会话回写 追踪/伏笔.md。
  FACTUAL_RECONCILIATION: [仅列需统一的事实来源或需人工裁决项，不写文学创作建议]
  REASONING_CHAINS: [仅列推理型 finding 的前提/规则 -> 触发事件 -> 矛盾点 -> 需裁决问题]
  ```

---

## Phase 3: Consolidated Judgment

1. Collect VERDICT and FINDINGS from reviewers that actually ran.
2. Merge and deduplicate; sort by `severity` (S1 > S2 > S3 > S4), then by scope of impact within a severity.
3. **Optional fact-checking**: If external facts require verification—historical dates, geography, professional details—spawn story-researcher only when `Effective Mode` remains `full`/`lean`, the current context is not a subagent, Agent tools are available, and `story-researcher` is deployed in the canonical directory. For Antigravity, check `.agents/agents/story-researcher/agent.md` and use `invoke_subagent` + `TypeName: "story-researcher"`. Under `solo`, missing/malformed/stale/spawn-failed fallback, or recursion guard, do not spawn; mark “human fact-check required” in the report.
4. **Present disagreements**: If reviewers conflict, show the disagreement clearly for the user to decide; do not compromise automatically.
5. Output the consolidated report, including actual mode, fallback reason, rubric, Rubric Source, scope, and evidence gaps.

---

## Phase 4: Output Report (full / lean)

Use this template only when `Effective Mode` is truly `full` or `lean`. If Phase 0 or runtime failure falls back to `solo`, use the solo template instead.

The five English keys `Requested Mode`, `Effective Mode`, `Fallback`, `Rubric`, and `Rubric Source` below must remain verbatim; do not replace them with Chinese keys.

```md
=== 故事审查报告 ===
Requested Mode: full | lean
Effective Mode: full | lean
Fallback: none
Rubric: fanqie | qidian | zhihu | generic web-fiction
Rubric Source: file | embedded fallback
审查范围: {章节/文件/批次}

## Verdict Summary / 结论汇总
- story-architect: APPROVE / CONCERNS(n) / REJECT / NOT_RUN
- character-designer: APPROVE / CONCERNS(n) / REJECT / NOT_RUN
- narrative-writer: APPROVE / CONCERNS(n) / REJECT / NOT_RUN
- consistency-checker: APPROVE / CONCERNS(n) / REJECT / NOT_RUN

> `NOT_RUN` 只用于 lean 模式排除的 reviewer 或可选 reviewer；如果 full/lean 必需 reviewer 缺失或 spawn 失败，应降级 solo，而不是在 full/lean 报告中标记 NOT_RUN 后继续综合。

## Severity Counts
- S1: n
- S2: n
- S3: n
- S4: n

## 综合评定
APPROVE(通过) / CONCERNS(有问题) / REJECT(需重写)

## 发现的问题
{按统一 Findings Schema 或等价表格列出所有问题}

## Agent 分歧（如有）
{列出 reviewer 间不同意见和证据}

## 证据不足 / 需补充
{缺失设定、缺失大纲、无法核查事实等}

## 修改建议
{按 S1→S4 优先级排列}

## 继承到下一批
{仅分批审查填写：逐条列 location、issue、预计核查/兑现范围；无则写“无”}
```

---

## solo Mode

Spawn no Agents. Identify the platform and load the matching rubric using Phase 1 Step 4. Even in solo mode, calibrate against the platform rubric, `story-review/references/quality-rubric.md`, or the embedded baseline.

solo must perform:
1. Format compliance (dramatic units/visual beats, no mechanical character-count splitting, no blank lines, dialogue format, subject/name rhythm).
2. Simple setting-consistency grep (names, attributes, key settings, foreshadowing terms) + reasoning-based consistency review (rule boundaries, setting hierarchy, cross-chapter causality, exploitable loopholes, cost consistency).
3. AI-flavor and banned-term checks, preferring `story-review/references/banned-words.md` and `story-review/references/anti-ai-writing.md`, otherwise the embedded fallback.
4. General web-fiction content scoring, preferring `story-review/references/quality-rubric.md`, otherwise the embedded rubric.
5. A simplified report using the unified Findings Schema.

### solo Output Format

```md
=== 故事审查报告（solo）===
Requested Mode: {full | lean | solo}
Effective Mode: solo
Fallback: none | missing agents -> solo | malformed agents -> solo | agent tool unavailable -> solo | spawn failed -> solo | subagent recursion guard -> solo
Rubric: fanqie | qidian | zhihu | generic web-fiction
Rubric Source: file | embedded fallback
审查范围: {章节/文件}

## 基础检查结果

### 格式合规性
- [{x| }] 段落按戏剧单元/镜头/一件事结束自然断开，非机械按字数切分；偶发稍长的完整推理/氛围/情绪链不算违规，通篇同阈值切段或碎成提纲才算：通过/不通过；证据：...
- [{x| }] 主语/角色名节奏自然：段首能建立主语，段中有代词/省略，关键转折再点名；连续句/段无必要重复同一主角名才算主语过密：通过/不通过；证据：...
- [{x| }] 无段间空行：通过/不通过；证据：...
- [{x| }] 对话独立成行：通过/不通过；证据：...
- [{x| }] 具体字数表达已确认统计正确且有叙事必要；不能确认时已改成非具体数字表达：通过/不通过；证据：...
- 违规位置：{列出}

> checklist 约定：`[x]` 只表示通过，`[ ]` 表示未通过；不得出现“`[x] ... 不通过`”这种矛盾写法。

### 设定一致性（grep + 推理扫描）
- 字面事实冲突：{列出发现的矛盾或证据不足}
- 推理型一致性：{规则边界/设定层级/跨章因果/可滥用漏洞/代价一致性的发现；无则写“未发现”}

### AI 味 / 禁用词
- {列出问题，必须附 evidence}

### Findings
{按统一 Findings Schema 或等价表格列出，severity 必须是 S1/S2/S3/S4}

### 修改建议
{按优先级排列}

### 继承到下一批
{仅分批审查填写：逐条列 location、issue、预计核查/兑现范围；无则写“无”}
```

---

## Tracking Maintenance (Long-Form Projects, Run at Review Closure)

The new tracking protocol has one write entrypoint: this skill’s `scripts/tracking_commit.py`; see `references/tracking-transaction.md` for fields and commands. **full / lean may modify `追踪/` only through this tool; solo modifies no `追踪/` files.** Never directly Edit/Write/append `伏笔.md`, character snapshots, timeline views, summaries, or `上下文.md`.

1. **Check state first**: Run `tracking_commit.py check --project {项目根}` and confirm `_tracking-state.json` matches all derived views. If it fails, rerun the original transaction that produced the target state; never guess, hand-edit Markdown, or create a separate overriding transaction.
2. **Decide whether revision is needed**: Maintain tracking only when manuscript evidence proves an existing tracked fact is wrong or missing. Expired foreshadowing, omitted open hooks, current character state, objective timeline, and reader knowledge belong in the `mode=revision` transaction for the chapter containing the evidence. Ordinary review opinions and future-writing recommendations never enter tracking.
3. **Build a complete same-chapter transaction**: Preserve still-valid fields from the chapter’s original compact increment and change only evidence-backed values. When core characters change, also submit complete `character_snapshots` through the latest written chapter. For each foreshadowing ID, `upsert` one current state instead of duplicating rows. For timeline items, submit objective fact, current reader knowledge, and actual reveal state together.
4. **Commit and recheck**: Run `tracking_commit.py commit`, then `check`. Confirm chapter records comply and remain within size limits, `上下文.md` has exactly seven fixed sections and ≤12,288 bytes, and both timelines plus all derived views match state.

For example, when reviewing demo Chapter 10, if the manuscript clearly shows Zhou Bosen saying the professional remake “lacked its soul” and Zhang Yaozu deciding to keep Jiang Chen’s mobile original, a revision transaction may add that outcome to objective fact and reader-known views. If the training plan behind Zhong Jiajia’s “only half right” has not been revealed in the manuscript, it may remain only in author truth and cannot enter the reader view.

## Workflow Handoff

**Pipeline:** General
**Position:** Review (after writing)

| When | Go To | Command |
|---|---|---|
| Fix identified issues | story-long-write / story-short-write | Return to the corresponding writing skill |
| Remove detected AI flavor | story-deslop | `/story-deslop` |
| Redecompose a comp title | story-long-analyze / story-short-analyze | `/story-long-analyze` or `/story-short-analyze` |

---

## Language

- Reply in the user’s language.
- Chinese responses must follow the Chinese Copywriting Style Guide.
