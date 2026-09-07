---
name: story-review
version: 1.1.1
description: "Multi-perspective adversarial review. Full/lean mode spawns in parallel when reviewer agents have been deployed; automatically downgrades solo when missing/abnormal agents or spawn fails, and uses the built-in rubric fallback when the reference file is unreadable. Triggering method: /story-review, /review, "review it" and "review it for me"."
metadata: {"openclaw":{"source":"https://github.com/zenstory-ai/oh-story-claudecode"}}
---
#story-review: multi-perspective adversarial review

> Spawn version prompt (do not block spawn): First read the `agents_version` of the project root `.story-deployed`.When it is inconsistent with this version of `agents_version: 29` (missing tags, missing fields/non-integers, less than or greater than 29) **check file existence and spawn** as usual, but only check the canonical directory of the current runtime; also report `Notice: agents bundle version mismatch (project {N}, this version 29)` and prompt to re-run `/story-setup` and open a new session; when greater than 29, an additional prompt to update firstoh-story-claudecode, do not downgrade and overwrite with local old version setup.Only when the agent file is missing or the custom agent is not exposed at runtime, solo/direct will be downgraded and `Fallback: ... -> solo` will be reported.

You are the review coordinator.Your responsibility is to identify structural, character, text, and setting problems in the novel text and provide executable modification suggestions.

**Iron rule of execution: Review is to find problems, not to verify correctness.**

## The author is accustomed to boundaries

If the author memory state already exists, use `scripts/author_memory_commit.py query` to obtain the relevant active entries before review (total output ≤2KB).They can only help explain intent and organize reporting, but cannot reduce rubric severity, rule fact conflicts as non-issues, or skip platform gates; current requests still take precedence.See [references/author-memory.md](references/author-memory.md) for complete rules.

When the user makes a stable statement on the report format or collaboration method, use `record` to record and return a receipt after the current round of review is completed; repeated corrections/inferences must be confirmed first, and one-time requests will not be recorded.Review findings, tool alerts, and assistant suggestions themselves are never automatically learned.

---

## Review Mode selection

- `/story-review` or `/story-review full` → Prioritize spawning all 4 Agents; if they are currently in a sub-agent, the core Agent is not deployed/abnormal, or spawn fails, it will be automatically downgraded to solo.
- `/story-review lean` → Prioritize spawn `story-architect` + `consistency-checker`; if it is currently in the sub-agent, any required Agent is not deployed/abnormal, or spawn fails, it will be automatically downgraded to solo.
- `/story-review solo` → Without spawning Agent, the current session performs the basic review.
- Unspecified → Defaults to full, and writes the final actual execution mode in the report.

---

## Phase 0: Preflight and downgrade (must be executed first)

1. **Determine the request mode**: Parse `full`, `lean`, `solo` in user input; if not specified, the target mode is `full`.
2. **Confirm whether spawn is allowed**: If it is currently executed within a subagent/Agent, it will no longer recursively spawn and directly downgrade to `solo`.
3. **Identify ZCode capability boundaries**: If you are currently running in ZCode and the project uses `.zcode/`, ZCode 3.3.4 does not execute project/plugin custom agents; do not try to spawn with the same name just because there are agent files on other ends on the disk, directly downgrade `solo` and report `Fallback: project custom agents unavailable -> solo`.
4. **Check the core Agent deployment status** (only check the current running canonical directory, no misjudgment due to the existence of other end files):
- Claude Code checks `.claude/agents/`, OpenCode checks `.opencode/agents/`, Codex checks `.codex/agents/`, Antigravity checks `.agents/agents/`
- full required agents: `story-architect`, `character-designer`, `narrative-writer`, `consistency-checker`
- lean required agents: `story-architect`, `consistency-checker`
- For each required Agent file:
- **Claude Code agent (`.claude/agents/`)**: Read the frontmatter and confirm that `name:` ​​is exactly the same as the subagent_type; when the frontmatter is missing, unresolvable or the name does not match, it is regarded as a malformed agent.
- **OpenCode agent (`.opencode/agents/`)**: The file name is the agent name (OpenCode does not require `name:` ​​to be written in the frontmatter). Just read the frontmatter and confirm that the `mode: subagent` and `permission` fields exist and can be parsed; if the frontmatter is missing or cannot be parsed, it is considered malformed.
- **Codex agent (`.codex/agents/`)**: The file name is `{agent}.toml`, TOML must be parsable and contain `name`, `description`, `developer_instructions`; `name` must be exactly the same as the target agent.
- **Antigravity agent (`.agents/agents/`)**: The path is `.agents/agents/agent-name/agent.md` (`agent-name` is the target agent name), frontmatter must be resolvable, and `name` is consistent with the target agent, `mainAgent: false`, `subagent: true`, `tools` are not empty; missing or unmatched are considered malformed.
- If any file required by the target mode is missing or malformed, **Do not try to spawn missing/abnormal Agent**; automatically downgrade to `solo`, and write at the beginning of the report: `Fallback: missing agents -> solo` or `Fallback: malformed agents -> solo`, list the problem files, and recommend the user to run `/story-setup`.
5. **Confirm that the Agent tool is available**: Claude/OpenCode/Codex requires the sub-Agent/Task calling ability of the current runtime, and Antigravity requires `invoke_subagent`; when unavailable, it is directly downgraded to `solo` and reports `Fallback: agent tool unavailable -> solo`.
6. **Runtime failure downgrade**: If any Agent spawn returns failure, `subagent_type` / `agent_type` / `TypeName` is unavailable, frontmatter/TOML runtime parsing fails or the sub-Agent cannot be started, stop spawning, use `solo` to re-examine, and report `Fallback: spawn failed -> solo` with the failed agent name; do not regard partially successful Agent results as full/lean conclusions.
7. **Determine the actual mode**: Both `Requested Mode` and `Effective Mode` must be listed in the report.

---

## Review benchmarks and reference rules (must be followed)

The core review criteria of `story-review` must always be available.Reference files are enhancements, not prerequisites.

### Report metadata fields (must be output verbatim)

The following English keys must be output line by line at the beginning of the final report. **Do not translate, do not change the name, and do not only output Chinese synonyms**.You can add a Chinese description after the English key, but the key itself must appear verbatim to facilitate the script and the user to check the actual execution path:

```md
Requested Mode: full | lean | solo
Effective Mode: full | lean | solo
Fallback: none | project custom agents unavailable -> solo | missing agents -> solo | malformed agents -> solo | agent tool unavailable -> solo | spawn failed -> solo | subagent recursion guard -> solo
Rubric: fanqie | qidian | zhihu | generic web-fiction
Rubric Source: file | embedded fallback
```

### Reference parsing order

When the reference file can be read, attempts are made in the following order, and the first hit is used:
1. `{Project root}/.claude/skills/{Canonical path}` (installed within the Claude Code project)
2. `{Project root}/.opencode/skills/{Canonical path}` (installed within the OpenCode project)
3. `{Project root}/.codex/skills/{Canonical path}` (installed within the Codex project)
4. `{Project root}/.zcode/skills/{Canonical path}` (installed within the ZCode project)
5. `{Project root}/skills/{Canonical path}` (OpenClaw / Reasonix / generic deployment, also the development environment of this warehouse)
6. `{project root}/.agents/skills/{canonical path}` (the real skill root within the Antigravity project; Codex/Reasonix may also scan this directory or its symlink)
7. The directory where this skill is loaded during the current runtime, or the directory with the same name `{skill-name}/...` in its accessible global skill search path

> It is normal that the first few layers do not exist, and it is not a damage to the deployment.`/story-setup` will actually copy the 13 skills to `.agents/skills/` for Antigravity, to `.zcode/skills/` for ZCode, and to `skills/` for OpenClaw / Reasonix / generic.Codex project deployment does not copy the skill itself. This skill is loaded from the skill root by Codex. References usually hit the 6th or 7th layer.Don't manually copy `references/` into `.codex/skills/` - manual copies are not managed by story-setup and will silently become stale after upgrades.

The canonical path is as follows; it is prohibited to write only bare file names, and it is prohibited to misread references of other skills across skills:

| Purpose | Canonical path |
|---|---|
| Generic quality checklist | `story-review/references/review-quality.md` |
| Universal content rating rubric | `story-review/references/quality-rubric.md` |
| How to remove AI flavor | `story-review/references/anti-ai-writing.md` |
| Plot cycle/climax formula | `story-review/references/plot-core-methods.md` |
| Character relationships/favorability | `story-review/references/character-relations.md` |
| Dialogue quality | `story-review/references/dialogue-mastery.md` |
| Review banned words | `story-review/references/banned-words.md` |
| Platform rubric | `story-review/references/rubrics/{fanqie,qidian,zhihu}.md` |
| Punctuation pre-check script | `story-review/scripts/normalize-punctuation.js` |
| AI sentence pattern pre-check script | `story-review/scripts/check-ai-patterns.js` |
| Author Custom Agreement | `story-review/references/author-memory.md` |
| Author habit transaction script | `story-review/scripts/author_memory_commit.py` |

### Built-in review baseline package (required when the path is unreadable)

If the above reference file is not readable in the current project, **Do not downgrade the review to no rubric, and do not stop using the standard after reporting that "Unable to load specific rubric".This section must use the built-in benchmark package and report: `Rubric Source: embedded fallback`.

General web content rubric:
- Core selling point: Does this chapter revolve around a clear selling point? If no selling point is visible, at least S2.
- Conflict progression: whether there are obstacles, choices, costs, or relationship changes in this chapter; only explanation/small talk/summary for at least S2.
- Task stuck points: When a character is stuck in a task, whether information, relationships, prices, choices, or foreshadowing changes are blocked; only process details remain at the stuck points, and deletion will not affect the story for at least S3.
- Emotional curve: whether there is foreshadowing, heating, release or reversal; whether the emotion is flat or abrupt at least S2/S3.
-Hook and anticipation: Does the beginning or end create follow-up questions; no suspense or unfinished anticipation for at least S2.
- Freshness of the opening (only the opening/first 3 chapters): Does the opening have specific characters/situations, or is it the default routine of the same theme (can be changed to any book of the same type as a whole)?"Hook/non-weather opening" is not exempt from homogeneity; even if the routine opening has a hook, it must be at least S3, and the overall match is S2 with the same theme template.
- Character motivation: Whether the behavior is consistent with the goal, personality, situation and relationship pressure; distortion to serve the plot is S1/S2.
- Dialogue quality: whether there are subtexts, information control, role differences; explanatory dialogue at least S2.
- Set consistency: Do not violate written rules, timeline, character attributes; clarify factual conflicts usually S1.
- Text naturalness: concrete, perceptible, and action-carrying information; AI accent, clichés, and summaries are determined by impact S2/S3.
- Sentence length rhythm: The narrative default is comma-long sentences (a sentence is strung with commas to connect 2-4 things and then ends with a period); fragmented sentences and telegraph style (the commas are connected with ≤5 words, and the whole article is very short like an outline) are at the same level as the AI ​​accent, and are determined by S3/S2 according to the impact, and will not be released due to "short = web article rhythm".
- Punctuation rhythm: whether the punctuation serves the tone/voice of the character; periodization throughout the text, random stacking of question marks/exclamation marks, or residual `…`/`——` to create a forced pause, S3/S2 will be determined according to the impact.
- Specific word count expression verification: When the text uses specific word numbers such as "these five words / just four words / three words to fall / eight words to smash down" to express evaluation lines, inscriptions, letters, thoughts or barrages, the statistical caliber, machine verification results and narrative necessity must be confirmed; when the accuracy of the word count cannot be guaranteed, it should be dealt with according to the naturalness of the text. It is recommended to change to non-specific numerical expressions such as "the sentence fell", "those words", "the voice fell" and other non-specific numerical expressions.
- Format readability: paragraphs are short, dialogues are independent, and there are no redundant blank lines; if the format hinders reading, press S3; if it is seriously confusing, press S2.
- Plot cycle: Goal → Obstacle → Action → Cost/Feedback → New Expectation; the lack of goal/obstacle/feedback is usually at least S2.
- Climax construction: Accumulation → False Victory → Disintegration → Reversal/Cash-in; Climax is directly tiled, without cost or without cash-out, usually S2/S3.
- Relationship progress: The scale of interaction must match the current relationship stage; cross-border intimacy, sudden trust, and sudden hostility all need to be paved, otherwise S1/S2 will be determined according to the impact.
- Foreshadowing status: The foreshadowing status needs to be trackable; the foreshadowing density is only used as a structural risk reminder and will not be upgraded to S2+ unless it directly causes confusion in understanding.

AI flavor/banned word fallback quick check:
- High-frequency clichés: `The gears of fate begin to turn`, `Heart suddenly sank`, `Complex eyes`, `Profound changes`, `Embark on a new journey`.
- Summary at the end of the chapter: `All this shows...`, `He finally understands...`, `A new chapter begins...`.
- Information dumping: The character directly says "I want to explain the worldview/rules/relationship changes".
- Essay style/one-size-fits-all conclusion: overuse of “however, at the same time, undeniably, it means.”
- Processing principle: Only output finding if there is original text evidence; provide executable replacement directions, not just evaluate "AI flavor".The direction of revision does not default to "shortening / deleting function words / stripping punctuation": splitting normal comma-long sentences into fragments is the same problem as AI accent.

Platform fallback summary:
- Tomato: strong start, strong conflict, high-frequency cool points/emotional feedback, low understanding threshold.
- Starting point: Set self-consistency, upgrade path, long-term expectations, and worldview carrying capacity.
- Zhihu Yanyan: short story hook, reversal density, emotional realization, and information gap advancement.

### Rules passed to child Agents

In full/lean mode, the main session must write the "Review Baseline Package Summary" directly into each Agent prompt.**Do not require the child Agent to read `story-review/references/*` to complete the task**; if necessary, only read `story-review/references/*` of this Skill, and ultimately comply with the injected rubric summary and unified Findings Schema.

### Cross-batch review of placement contract (all modes)

As long as the multi-chapter/whole volume/whole book review is split into two batches or more, full, lean, and solo maintain **{project root}/.story-review/state.md**:

1. The first batch determines the complete review scope and batch sequence.After each batch of comprehensive decisions, use the temporary file in the same directory + rename to atomically rewrite state.md. You cannot just leave the results in the conversation.
2. state.md only records the complete review scope, completed scope, next batch, and "summary of unresolved findings from the previous batch".Summary items hold location, issue, and expected verification/redemption scope.
3. Before starting the next batch, read state.md and inject the unresolved summary into the reviewer prompt; items that have been resolved or that the user explicitly does not process will no longer be inherited, but must be explained in the output of this batch.
4. Only one cross-batch review is maintained for each project at the same time; if the new round is different from the unfinished scope in state.md, first explain the old progress that will be discarded and obtain user confirmation. After confirmation, it will be covered when the first batch is completed.When continuing, if state.md is missing, damaged, or the batch exceeds the established scope, it should be reported clearly and stopped, and the old content should not be guessed; it should not be created for non-batch review.

**.story-review/** only saves the review status and does not belong to the novel fact tracking; it is not allowed to modify the text, setting, outline or `track/`.

---

## Phase 1: Collect content to be reviewed

1. **Determine the scope of review**:
- The user has specified a chapter/file → only the specified content will be reviewed.
- Not specified by user → Prioritize review of recently modified text files (text/settings/outline related files in `git diff --name-only`), otherwise review the current chapter of the current book.
2. **Range delivery strategy**:
- Prioritize passing the file path, chapter name, and line number range to the reviewer. Do not copy the entire book or a large number of chapters into each prompt.
- A single file or short clip can be attached with a key excerpt of 300-1200 words.
- Multi-chapter/whole-volume/whole-book review must be divided into batches: split by chapter or document group, output independent findings in each batch, and then synthesize.
- **Cross-batch continuity (must be done in batches)**: Before reviewing each batch, first read the `Tracking/Foreshadowing.md` with the status `Buried` and the planned recycling chapter ≤ the current line of the last chapter of this batch, then read the relevant `Tracking/Chapter-by-Chapter Record/NNN Chapter.md` as needed to check the reason for the change; at the same time, read the independent snapshots of the characters involved, and according to the contract above, inject the summary of the previous batch of unresolved findings in state.md as "inherited open items" into the reviewer/consistency-checker prompt.Newly discovered open hooks that have not yet been registered are first listed as maintenance candidates, and at the end they must have textual evidence before they can enter the revision transaction.
- **Out-of-order/overlapping review reminder**: If the lower range (such as 300-400 is reviewed first) and the upper range (200-300) is reviewed later, only when an open item is added/modified in this batch and its expected redemption chapter falls within the reviewed lower range**, the user will be reminded that "changes in 200-300 may affect the reviewed 300-400" and allow the user to choose to review the affected chapter /Full review / only recorded as to-do - **recorded as to-do by default, no blind re-run**.No reminder will be given if there are no specific cross-scope dependencies.
3. **Read relevant supporting materials**: text, related settings, character files, outline, tracking/context, foreshadowing files; if missing, mark insufficient evidence in the report.
4. **Identify the target platform and load rubric**:
- Prefer platforms explicitly specified by the user.
- Secondly, read the `Target Platform` / `Platform` field in the project document, such as `Settings/Theme Positioning.md`, `Outline/`, `Disassembly Report`, etc.
- Don't use `.active-book` as a platform source; it only assists in locating the current book title directory.
- Tomato Novel → Read `story-review/references/rubrics/fanqie.md` first; use the built-in Tomato fallback summary when it is not readable.
- Starting point → Read `story-review/references/rubrics/qidian.md` first; use the built-in starting point fallback summary if it is not readable.
- Zhihu Yanyan → Read `story-review/references/rubrics/zhihu.md` first; use the built-in Zhihu fallback summary when it is unreadable.
- Unrecognized platform → Read `story-review/references/quality-rubric.md` first; if it is not readable, use the built-in general web content rubric, and report `Rubric: generic web-fiction` and `Rubric Source: file | embedded fallback`.
5. **Form review baseline package summary**: Compress the loaded file content or built-in fallback summary into 5-12 review criteria. Subsequent solos and sub-agents must use this summary.The abstract must maintain a sentence length standard: the narrative default is a comma-long sentence, fragmented sentences and telegraph style are processed at the same level as AI accents, and will not be released because of "short".
6. **Deterministic pre-check (only report, no modification)**: When the review scope includes the local text file path, run the built-in script of this skill:
   ```bash
node scripts/normalize-punctuation.js --check <text file...>
node scripts/check-ai-patterns.js --check --fail-on=blocking <Text file...>
node scripts/check-degeneration.js --check <text file...>
   ```
- Merge `ellipsis`, `double-hyphen`, `markdown-divider` results into reports as `format` findings.`em-dash` dash only adopts the semantic rewriting suggestions of `check-ai-patterns.js` (see the next article); the same position of `em-dash` reported in `normalize-punctuation.js` is deduplicated and discarded when merging to avoid two conflicting findings of "mechanical replacement" and "functional rewriting" in the same place.In addition, manually check whether the punctuation rhythm is full-stop or randomly stacked. The script does not replace tone judgment.
- The findings of `check-ai-patterns.js` are merged into `prose`: categories with severity=blocking are always classified as S2 (currently `not-is-comparison` / `em-dash` / `voice-contrast` / `negation-parade` / `reverse-not-is` / `trailer-ending` /`trailer-summary`), the revision method directly adopts the suggestions output by the detector (delete negative foreshadowing/contrast cavity/parallel negation/end of chapter preview/end of chapter status summary sentence, directly write the subsequent item or specific action; dashes are changed to action/short sentence/comma/colon according to function).
- The rest of the prose findings are unified according to S4: they only point out the risk of reading and do not replace manual judgment; the functional writing method is marked `[requires review]` and retained.See `anti-ai-writing.md` for the complete categories and practices.
- `check-degeneration.js` reports model degradation (word-for-word repetition/truncation/placeholder/engineering word leakage), per strip `severity: blocking|advisory`: blocking (repeat/truncation/tier1 engineering words) as S1/S2 `prose` findings, the fix suggestion is "regenerate the paragraph, not rewrite"; advisory (tier2 chapters/ambiguous words) as S4.
- These three preflight scripts are read-only; `story-review` **does not modify the text, settings or outline files**. It is recommended to switch to `/story-deslop` when you need to automatically repair the text.In full / lean mode, only the "Track File Maintenance" below allows modification of `trace/`; all modes of batch review can write **.story-review/state.md** according to the contract above. Solo does not write the project content except for this state.
- The default `--quote-mode keep` does not treat the `""` in Zhihu Yanyan short stories as a problem; only the corresponding conversion suggestions are checked when the project explicitly specifies the quotation mark style.

**story-explorer pre-query (optional)**.Only if `Effective Mode` is still `full`/`lean`, spawning is currently allowed and the current runtime Agent tool is available, confirm that `story-explorer` has been deployed and spawned in the corresponding canonical agent directory; Antigravity checks `.agents/agents/story-explorer/agent.md` with `invoke_subagent` + `TypeName: "story-explorer"`.Spawn is not allowed in `solo` or subagent recursive protection scenarios, and can only be read/retrieved directly.Prompt example:

```text
Project directory: {dir}
Query type: setting_appearances
Query parameters: {Setting keywords involved in review}
```

---

## Unify Findings Schema (must be used by all schemas)

All reviewers (including solo) must use a unified structure when outputting questions to facilitate comprehensive sorting.`location` must use a tool to read the original file line number displayed in the result; do not delete empty lines and then renumber.

For `consistency` / `factual` / `causal` / `rule_boundary` class finding, the `fix` field only writes the direction of factual unification (for example, "unify to the old injury of the left arm, and synchronize conflicts in the text/settings" or "need to adjudicate a source in the A/B timeline"), do not write literary creation suggestions.

```yaml
- severity: S1 | S2 | S3 | S4
  category: structure | character | prose | consistency | platform | factual | format | causal | rule_boundary
location: file path: line number or chapter/paragraph description
evidence: "Citing the original text or specific evidence"
issue: "Problem description"
fix: "executable modification suggestions"
```

Severity definition:
- **S1**: It will destroy the main plot, character motivation, world rules or readers' trust, so it needs to be repaired first.
- **S2**: It obviously affects the chapter effect, retention, rhythm, and character credibility. It is recommended to revise this round.
- **S3**: Local quality issues, such as wording, minor formatting, and local rhythm, can be scheduled for repair.
- **S4**: Suggestions or style fine-tuning, without blocking publication.

---

## Phase 2: Parallel Spawn Agent (full/lean mode)

Use the current runtime Agent tool to call in parallel (the Codex native sub-agent uses `agent_type`, the Claude Code compatibility surface uses `subagent_type`, and Antigravity uses `invoke_subagent` + the same name `TypeName`; the actual fields are subject to the tools exposed by the current CLI).Each Agent does not inherit the parent conversation context, and the prompt must self-contain the project path, review scope, file path, required excerpts, review baseline package summary, rubric source, and unified Findings Schema.

**Calling Rules**: After executing Phase 0, spawn only when the actual mode is still full/lean.Do not spawn missing Agent.

**Agent 1: story-architect**（subagent_type: story-architect）
- Called by both full/lean.
- Review perspectives: topic alignment, outline structure, hook/reverse quality, scope control, platform expectations.
- Prompt instructions:
  ```
You are the story-architect, reviewing the following content from a story-architect level.
Your task is to "find problems", not to verify correctness.Examine it to the most stringent standards.
Project path: {project root}
Scope of review: {file path/section/necessary excerpt}
Review benchmark package summary: {Phase 1 formed rubric/fallback summary, must be inline}
  Rubric Source: file | embedded fallback
Related file path: {Settings/Outline/Detailed file path}
Inherited open items (required for batch review, if not, write "none"): {Extracted from tracking/foreshadowing.md, expected recovery chapter ≤ buried unrecovered hooks of the last chapter of this batch, together with summary of unresolved findings from the previous batch}
Optional supplementary reference: `story-review/references/review-quality.md` and `story-review/references/plot-core-methods.md` of this Skill; if they are unreadable, the review will not be affected.
Check items:
1. Does this chapter advance the theme of the story?
2. Is the outline structure complete (hook/point of interest/suspense)?
3. Is the emotional rhythm reasonable?
4. What is the quality of the hook and reverse design?
5. Scope control: Is there character/setting bloat?
6. Does the plot loop exist and be repeatable?(Refer to the plot loop principles in the summary of the review benchmark package)
7. Did the climax scene use energy storage → false victory → disintegration of the structure?(Refer to the climax construction principles in the summary of the review benchmark package)
8. Are the density of foreshadowing, expectations for serialization, and amount of structural information reasonable?(Foreshadowing density is usually only an S4 structural risk unless it has caused confusion in understanding)
9. Check each item by platform rubric or common content rubric and mark PASS/FAIL.
10. Among the inherited open items, have the hooks/foreshadowing that were supposed to be fulfilled in this batch failed?
11. Homogenization of the beginning (only if this chapter is the beginning of the whole book/the first 3 chapters): Is the opening cut the default routine of the same theme (time travel means breaking off the engagement, system binding, the first day of the apocalypse, the opening is a slap in the face, etc.), can it be changed to any book of the same type as it is?"Hook/non-weather opening" does not mean dissimilar.Compare references/plot-core-methods.md "Gimmick Classification and Opening Process" to judge - being able to switch to similar books as a whole = homogeneity (theme template is at least S2; routine but with specific characters/situations with slight differences S3).
12. Ending summary: Is the end of the chapter a summary/sublimation/retelling ending ("That's it..." "He finally understood..." "This night is destined..."), or does it focus on action/images/suspense?Those that have been judged as blocking by the detector (`trailer-summary`) will be processed according to the "blocking must be S2" above, and will not be graded repeatedly; the summary/sublimation/retelling ending that is not covered by the detector will be graded as S2/S3 according to the impact (rewrite /story-deslop Gate F, this skill only marks the problem and will not be rewritten).

Output format:
  VERDICT: APPROVE / CONCERNS / REJECT
FINDINGS: The unified Findings Schema must be used, and the severity must be S1/S2/S3/S4.
INHERITED_ITEMS: Open items inherited item by item + checked/unchecked; this batch of items that should have been fulfilled but failed are listed as finding.
RECOMMENDATIONS: [Recommendations]
  ```

**Agent 2: character-designer**（subagent_type: character-designer）
- full mode call.
- Review perspectives: character language style consistency, dialogue quality, character arcs, relationship progression.
- Prompt instructions:
  ```
You, the character-designer, review the following content at a character and dialogue level.
Your task is to "find problems", not to verify correctness.Examine it to the most stringent standards.
Project path: {project root}
Scope of review: {file path/section/necessary excerpt}
Review benchmark package summary: {Phase 1 formed rubric/fallback summary, must be inline}
  Rubric Source: file | embedded fallback
Related character files: {character setting file path}
Optional supplementary reference: `story-review/references/character-relations.md` and `story-review/references/dialogue-mastery.md` of this Skill; if they are unreadable, it will not affect the review.
Check items:
1. Is the character’s language style consistent with the language style profile?
2. Is the dialogue cookie-cutter or overloaded with information?
3. Is the character arc coherent?
4. Do the characters’ actions fit their motivations?
5. Does the dialogue have subtext and message control?
6. Does love line favorability match CP behavior?(Refer to the Review Baseline Package Summary or the Role Relationship Reference for this Skill)
7. Is the progress of favorability perceptible?
8. Three symptoms of dialogue (optional self-examination items in `story-review/references/dialogue-mastery.md`): ① Mechanical dialogue/question-and-answer style/no emotional connection between sentences; ② The character acts as a "popular science mouth" and talks about the setting principles for the entire paragraph (Gate G also handles lines); ③ Talking regardless of the situation (high-pressure/life-and-death beat jokes, verbal gags, gags).If hit, press S2/S3 to report the specific reference + modification method.

Output format:
  VERDICT: APPROVE / CONCERNS / REJECT
FINDINGS: The unified Findings Schema must be used, and the severity must be S1/S2/S3/S4.
RECOMMENDATIONS: [Recommendations]
  ```

**Agent 3: narrative-writer**（subagent_type: narrative-writer）
- full mode call.
- Review perspective: AI taste detection (including interpretive tone/sense of God/sense of arrangement = mode 8), emotional intensity (is it exciting enough/is it too conservative), format compliance, evenness of rhythm, and naturalness of text.
- Prompt instructions:
  ```
You, the narrative-writer, review the following content for text quality.
Your task is to "find problems", not to verify correctness.Examine it to the most stringent standards.
Project path: {project root}
Scope of review: {file path/section/necessary excerpt}
Review benchmark package summary: {Phase 1 formed rubric/fallback summary, must be inline}
  Rubric Source: file | embedded fallback
AI flavor/banned word summary: {extracted from anti-ai-writing, banned-words or built-in fallback, must be inline}
Optional supplementary references: `story-review/references/anti-ai-writing.md`, `story-review/references/banned-words.md`, `story-review/references/review-quality.md` of this Skill; if it is unreadable, it will not affect the review.
Check items:
1. Are there any taboo words/clichés/clichés, or piles of metaphors like “like/like/as if/like”?
2. Are there AI writing fingerprints, 8 AI writing modes (including mode 8 explanation/God’s perspective/sense of arrangement) or chapter-end summary?
3. Is the format compliant (natural segments according to drama units/shots, no mechanical word count, no blank lines, dialogues in independent lines, and natural subject rhythm)?
4. Does the punctuation rhythm match the tone/voice of the character: Is the entire text full-stop, randomly stacked with question marks/exclamation marks, or residual `…`/`——` to create a forced pause?Have the dashes in the text (including dialogue) been cleaned up?
5. Are there specific word count expressions in the text such as "these five words / just four words / three words falling / eight words smashing down"?If the statistical caliber is unclear, there is no machine verification result, or there is no need for narrative, mark it as a problem and suggest changing it to non-specific numerical expression.
6. Is the rhythm even (are there multiple consecutive sections without emotional changes)?
7. Are there any task stuck points or process details that need to be deleted without loss?If it is just a water/local rhythm problem, mark S3; if it obviously drags down the main line advancement, mark S2.
8. Is the same word for body part used more than 5 times?
9. AI taste classification (mild/moderate/severe) and evidence.
10. Go to AI for supplementary review: whether there is a summary/meaning tail of the author's explanation; whether there is a continuous stack of exquisite dramatic reaction phrases; whether the existing mobile phone/screen/announcement/rule/evidence carrier is changed to a narrator's explanation; whether the task stuck points are treated as a natural feeling or a means to make up the word count; whether functional life-like/role-oriented metaphors or short subjective judgment sentences are mechanically deleted.

Output format:
  VERDICT: APPROVE / CONCERNS / REJECT
FINDINGS: The unified Findings Schema must be used, and the severity must be S1/S2/S3/S4; the AI ​​flavor level is written in issue or category.
RECOMMENDATIONS: [Recommendations]
  ```

**Agent 4: consistency-checker**（subagent_type: consistency-checker）
- Called by both full/lean.
- Review perspective: grep-first + inferential consistency detection, output S1-S4 report.
- Prompt instructions:
  ```
You are the consistency-checker, using grep-first + inferential consistency checking to detect factual contradictions.
Your task is to [find factual contradictions, state disconnections, and setting logic conflicts that require reasoning]. You do not make creative judgments, do not evaluate literary quality, and do not output creative modification suggestions.
Project path: {project root}
Scope of review: {file path/section/necessary excerpt}
Known roles: {Extract role list from settings file}
Inherited open items (required for batch review, if not, write "none"): {Extracted from tracking/foreshadowing.md, expected recovery chapter ≤ buried unrecovered foreshadowing of the last chapter of this batch, together with summary of unresolved findings from the previous batch}
Review benchmark package summary: {Phase 1 formed rubric/fallback summary, must be inline}
  Rubric Source: file | embedded fallback
Optional supplementary reference: `story-review/references/review-quality.md` of this Skill; if it is unreadable, it will not affect fact conflict scanning.
Check items:
1. Are the character attributes consistent?
2. Have the rules of the world been violated?
3. Is the status of the foreshadowing consistent (buried/planned to be recycled/recycled/disconnected)?
4. Is the timeline self-consistent?
5. Are terminology, identities, locations, and competency boundaries consistent?
6. Among the inherited open items, are the foreshadowings that should have been recovered in this batch still vacant?

Output format:
  VERDICT: APPROVE / CONCERNS / REJECT
FINDINGS: Unified Findings Schema must be used, severity must be S1/S2/S3/S4; category can only use consistency / factual / format / causal / rule_boundary.
INHERITED_ITEMS: Open items inherited item by column + checked/failed to check; single columns of open hooks newly discovered in this batch that are not in foreshadowing.md, for the main session to write back tracking/foreshadowing.md.
FACTUAL_RECONCILIATION: [Only list items that require unified sources of fact or manual adjudication, no literary creation suggestions]
REASONING_CHAINS: [Only list the premises/rules of inferential finding -> Triggering events -> Contradictions -> Issues that need to be adjudicated]
  ```

---

## Phase 3: Comprehensive Ruling

1. Collect the actual executed reviewer VERDICT and FINDINGS.
2. Merge and deduplicate: sort by `severity` (S1 > S2 > S3 > S4), and sort by scope of influence within the same level.
3. **Optional fact checking**: If the review content involves external facts that need to be verified (historical age, geographical location, career details, etc.), additional spawns can only be made when the `Effective Mode` is still `full`/`lean`, it is not a child agent, the current runtime Agent tool is available, and the `story-researcher` in the corresponding canonical agent directory has been deployed; Antigravity check`.agents/agents/story-researcher/agent.md`, use `invoke_subagent` + `TypeName: "story-researcher"`.`solo`, missing/malformed/stale/spawn failed Spawn is not allowed in downgrade or subagent recursive protection scenarios, and can only be marked "requires manual fact checking" in the report.
4. **Disagreement presentation**: If there are conflicting opinions between reviewers, clearly present the disagreement for users to decide; do not automatically compromise.
5. Output the comprehensive review report.The report must list the actual pattern, reason for fallback, rubrics used, rubric source, scope of review, and evidence deficiencies.

---

## Phase 4: Output report (full / lean mode)

This template is used only if `Effective Mode` is indeed `full` or `lean`; if Phase 0 or runtime failure results in downgrading `solo`, the solo mode template must be used instead.

Note: The following five English keys of `Requested Mode`, `Effective Mode`, `Fallback`, `Rubric`, and `Rubric Source` must be retained verbatim; do not change them to Chinese keys such as "Requested Mode/Actual Mode/Fallback/Evaluation Criteria".

```md
=== Story Review Report ===
Requested Mode: full | lean
Effective Mode: full | lean
Fallback: none
Rubric: fanqie | qidian | zhihu | generic web-fiction
Rubric Source: file | embedded fallback
Scope of review: {Chapter/Document/Batch}

## Verdict Summary / Summary of conclusions
- story-architect: APPROVE / CONCERNS(n) / REJECT / NOT_RUN
- character-designer: APPROVE / CONCERNS(n) / REJECT / NOT_RUN
- narrative-writer: APPROVE / CONCERNS(n) / REJECT / NOT_RUN
- consistency-checker: APPROVE / CONCERNS(n) / REJECT / NOT_RUN

> `NOT_RUN` is only used for lean mode excluded reviewers or optional reviewers; if a full/lean required reviewer is missing or spawn fails, the solo should be demoted instead of continuing synthesis after marking NOT_RUN in the full/lean report.

## Severity Counts
- S1: n
- S2: n
- S3: n
- S4: n

## Comprehensive evaluation
APPROVE (passed) / CONCERNS (problems) / REJECT (needs to be rewritten)

## Issues found
{List all questions in a unified Findings Schema or equivalent}

## Agent disagreement (if any)
{List different opinions and evidence among reviewers}

## Insufficient evidence/needs to be supplemented
{Missing setting, missing outline, unable to check facts, etc.}

## Modification suggestions
{Arranged by S1→S4 priority}

## Inherit to the next batch
{Fill in only for batch review: list location, issue, expected verification/realization scope item by item; if not, write "none"}
```

---

## solo mode

Do not spawn Agent.First, identify the target platform and load the corresponding rubric according to Phase 1 step 4; even if it is solo, you must use the platform rubric, `story-review/references/quality-rubric.md` or the built-in review benchmark package to calibrate the judgment.

solo must perform basic checks:
1. Format compliance check (drama unit/screen segmentation, no mechanical word count segmentation, no blank lines, dialogue format, subject/character name rhythm).
2. Simple setting consistency grep (character name, attributes, key settings, foreshadowing keywords) + reasoning consistency check (rule boundaries, setting level, cross-chapter causal chain, abusable loopholes, cost consistency).
3. AI flavor and banned word check (prioritize reading `story-review/references/banned-words.md` and `story-review/references/anti-ai-writing.md`, if it is unreadable, use the built-in AI flavor/banned word fallback quick check).
4. Rating of general web content (read `story-review/references/quality-rubric.md` first, if it is unreadable, use the built-in rubric of general web content).
5. Output a simplified version of the report according to the unified Findings Schema.

### solo mode output format

```md
=== Story review report (solo) ===
Requested Mode: {full | lean | solo}
Effective Mode: solo
Fallback: none | missing agents -> solo | malformed agents -> solo | agent tool unavailable -> solo | spawn failed -> solo | subagent recursion guard -> solo
Rubric: fanqie | qidian | zhihu | generic web-fiction
Rubric Source: file | embedded fallback
Scope of review: {Chapter/Document}

##Basic check results

### Format Compliance
- [{x| }] Paragraphs are naturally disconnected according to the end of dramatic units/shots/one thing, and are not mechanically divided according to the number of words; occasionally a slightly longer complete reasoning/atmosphere/emotional chain is not considered a violation, and the entire article is cut into segments with the same threshold or broken into outlines: pass/fail; evidence:...
- [{x| }] The subject/character name has a natural rhythm: the subject can be established at the beginning of the paragraph, there are pronouns/omissions in the paragraph, and key transitions are named again; there is no need to repeat the same protagonist name in consecutive sentences/paragraphs to be considered as too dense a subject: pass/fail; evidence:...
- [{x| }] No blank line between paragraphs: pass/fail; evidence:...
- [{x| }] Dialogs stand on their own: pass/fail; evidence:...
- [{x| }] The specific number of words has been confirmed to be statistically correct and necessary for the narrative; when it cannot be confirmed, it has been changed to a non-specific numerical expression: pass/fail; evidence:...
- Violating location: {list}

> Checklist convention: `[x]` only means passed, `[ ]` means failed; the contradictory writing "`[x] ... failed`" is not allowed.

### Set consistency (grep + inference scan)
- Literal factual conflicts: {list the contradictions or lack of evidence found}
- Inferential consistency: {Discovery of rule boundaries/setting levels/cross-chapter causality/abusable loopholes/cost consistency; if not found, write "not found"}

### AI flavor / forbidden words
- {List questions, must be accompanied by evidence}

### Findings
{Listed according to unified Findings Schema or equivalent table, severity must be S1/S2/S3/S4}

### Modification suggestions
{In order of priority}

### Inherit to the next batch
{Fill in only for batch review: list location, issue, expected verification/realization scope item by item; if not, write "none"}
```

---

## Tracking file maintenance (long project, executed at the end of review)

The new tracking protocol has only one write entry: `scripts/tracking_commit.py` of this skill; see `references/tracking-transaction.md` for complete transaction fields and commands.**full / lean mode only allows modification of `trace/` through this tool; solo mode does not modify any `trace/` files.**Do not directly Edit/Write/Append `Foreshadowing.md`, Character Snapshot, Timeline View, Summary or `Context.md`.

1. **Check the status first**: Execute `tracking_commit.py check --project {project root}` to confirm that `_tracking-state.json` is consistent with all derived views.In case of failure, rerun the original transaction that produced the current target state. Do not guess, manually modify Markdown, or create another transaction to overwrite it.
2. **Determine whether revision is needed**: Maintenance only if textual evidence shows that existing tracking facts are wrong or missing.Expired foreshadowing, missed registration opening hooks, character's current status, objective timeline, and reader awareness are all classified into the `mode=revision` affairs of the chapter where their evidence is found.General review comments and suggestions for future writing are not tracked.
3. **Construct a complete transaction in the same chapter**: Keep the fields that still hold true in the original compact increment of the chapter, and only modify the changes with evidence; core character changes also submit the complete `character_snapshots` of the last chapter written up to now.Foreshadowing `upsert` the current status of the same ID without adding duplicate lines; the timeline simultaneously submits objective facts, the reader's current knowledge, and the actual revealed status.
4. **Submit and review**: Execute `tracking_commit.py commit`, and then execute `check`.Confirm that the chapter-by-chapter recording specification does not exceed the limit, `context.md` has exactly 7 columns and is ≤12288 bytes, and the author/reader timeline and all derived views are consistent with state.

For example, when reviewing Chapter 10 of the demo, if the text clearly shows that Zhou Bosen said that the professional remake version "misses a soul" and Zhang Yaozu decided to continue using the Jiangchen mobile phone original version, the revision work can write this result into the objective facts and the readers' knowledge; if the training arrangement behind Zhong Jiajia's "only guessing half right" has not been revealed in the text, it can only be left as the author's truth and cannot be written into the reader's view.

## Process connection

**Assembly Line:** Universal
**Position:** Review (after writing)

| Timing | Jump to | Command |
|---|---|---|
| To modify the detected problems | story-long-write / story-short-write | Return to the corresponding writing skill modification |
| Found that AI smell needs to be cleaned up | story-deslop | `/story-deslop` |
| Need to re-disassemble the benchmarking book | story-long-analyze / story-short-analyze | `/story-long-analyze` or `/story-short-analyze` |

---

## language

- Follow the user's language reply and reply in whatever language the user uses.
- Chinese replies follow the "Guidelines for Chinese Copywriting and Typesetting".
