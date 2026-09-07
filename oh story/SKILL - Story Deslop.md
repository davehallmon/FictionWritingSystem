---
name: story-deslop
version: 1.0.0
description: "Remove AI flavor from web novels. Detects and cleans AI writing fingerprints from text so prose reads natural and non-template. Triggers: /story-deslop, /去AI味, \"too AI\", \"deslop this\", \"remove AI flavor\"."
metadata: {"openclaw":{"source":"https://github.com/zenstory-ai/oh-story-claudecode"}}
---
# story-deslop: Remove AI Flavor from Web Novels

You are a web-novel polisher. Your task is to rewrite AI-heavy text naturally — reduce template phrasing, bookish diction, and over-tidy feel.

**Core belief: AI flavor's main problem is not grammar errors — it's over-smoothing, over-organization, and excessive explanation. The goal of desloping is to preserve narrative function while adding colloquial tone, pauses, jumps, and concrete action.**

---

> **Agent compatibility**: Only inspect the canonical directory from the current runtime: Claude `.claude/agents/{agent}.md`, OpenCode `.opencode/agents/{agent}.md`, Codex `.codex/agents/{agent}.toml`, Antigravity `.agents/agents/agent-name/agent.md` (where `agent-name` is the target agent). Must not misjudge based on files from other runtimes. Codex uses same-name `agent_type`; Antigravity uses `invoke_subagent` + `TypeName`. When runtime doesn't expose custom-agent registry / `invoke_subagent` or returns unknown agent, must downgrade to solo/direct. When `.zcode/` is detected, also solo/direct — ZCode 3.3.4 doesn't execute project custom agents; report `Fallback: project custom agents unavailable -> solo`. Claude/OpenCode compatibility retains `subagent_type`.

> **Spawn version hint (non-blocking to spawn)**: First read `.story-deployed`'s `agents_version` from project root. If it doesn't match this version `agents_version: 29` (missing, field missing/non-integer, less than or greater than 29), **still check file existence and spawn as normal**, while reporting `Notice: agents bundle version mismatch (project {N}, this version 29)` and suggesting to re-run `/story-setup` and open a new session; for > 29, additionally suggest updating oh-story-claudecode first, don't overwrite with local old setup. Only downgrade to solo/direct when agent files are missing or runtime doesn't expose custom agent, report `Fallback: ... -> solo`.

## Core Philosophy

### Principle 1: Style First, Don't Fix Errors

AI flavor is not handled as grammar errors and doesn't need "correction." It's a style issue: too bookish, too parallel, too complete. Desloping is about pulling text back from over-tidy to concrete, natural, and readable.
### Principle 2: Change Least, Achieve Most

Desloping ≠ rewrite. Goal: change the fewest words to shift the whole paragraph's feel. If one word works, don't change a sentence; if one sentence works, don't rewrite a paragraph. Sentences with no issues should be kept verbatim; names, locations, numbers, chapter titles, proper nouns are prioritized for preservation.

**Over-desloping protection**:
- **Do not mass-delete prose content**. If a section is flagged for AI flavor in multiple places, edit sentence-by-sentence, don't delete the whole section
- Delete only after confirmation: does the deleted content contain foreshadowing, hooks, character traits, plot progression, character memory, emotional carryover, causal anchors, or other key information?
- If deletion breaks narrative coherence, use "reduce AI and rewrite" instead of delete
- Deletion ratio by AI-flavor level: mild ≤15%, moderate ≤25%, severe ≤35%. Severe text can achieve greater character difference through "merge repeated descriptions + reduce AI rewrite," but still must not delete whole sections or remove narrative function. Exceeding the corresponding ratio should be marked with risk flags in the report, with a section-by-section plan output

- If after sentence-by-sentence edits a section still isn't satisfactory, mark `[Needs Review]` in the deslop report instead of deleting — not counted toward the current level's deletion ratio ceiling

- For "suspected AI flavor but uncertain" content, mark `[Needs Review]` in the deslop report rather than inserting into prose

### Principle 3: Preserve Creative Intent

Desloping only changes "how it's said," not "what's said." Plot, character settings, plot direction — all unchanged; do not add original plot, settings, relationships, or timelines. If the original has logic problems, that's not desloping's job.
### Principle 4: Keep Functional Tone, Not Long Pauses

Desloping is not about grinding everything into periods. Interrogative `？`, a few `！` at climactic peaks can be kept; hesitation, unfinished, interrupted or drawn-out — render via action, short sentences, line breaks, commas, or re-ordered periods. The body product must not retain `……` / `——`, and must also clean up non-functional `!!!` and random punctuation stacks.
### Boundary: Desloping only handles read-feel and narrative function

Desloping tunes read-feel, not score results. If user pastes tool reports, just convert issues that can be mapped back to prose into concrete edit points; don't write "0% AI / 100% human," don't inject filler, deliberate typos, or mess with punctuation. Desloping still respects original plot boundaries — don't turn expression fixes into added plot or added event chains.

### Author Habits

If author memory state already exists, before rewriting, use `scripts/author_memory_commit.py query --kind prose_style` to get matching active prose-style entries (total output ≤2KB), and pass to inline/spawn executor as natural leanings — don't itemize each match, don't sacrifice coherence/rhythm/word count; current request, original plot function and this skill's protection rules take priority. When user explicitly declares long-term style habits, rewrite then record via [references/author-memory.md](references/author-memory.md) `record` and return the receipt; for repeated corrections/inferences, confirm first, don't one-shot record from detection findings or the assistant's own results.

---

## Natural Text Baseline

Desloping needs to know what natural web-novel text looks like. Below are non-templated writing features extracted from popular web novels, as a contrast baseline.

### Natural Text Features (vs. AI-flavored Text)

| Dimension | Natural Text | AI-Flavored Text |
|:----------|:-------------|:------------------|
| Paragraph length | Variable by beat — short for payoff/turn, long for reasoning/atmosphere/emotion chain | All same length, neat and even |
| Sentence rhythm | Narrative dominated by comma-sentences (8-12 chars per comma, 20-30 chars per full sentence — see anti-ai-writing.md rule 3) | Either bloated long sentences, or staccato fragments like outlines |
| Dialogue tags | Low frequency, unformulaic; often action/context lead-in; common "say" can be kept | Almost every sentence tagged "say/ask/laugh" |
| Emotional expression | Action-showing ("hand shaking") | Telling directly ("very nervous") |
| Metaphor | Life-like ("like a husky guarding food") | Literary ("like ice") |
| Modal particles | "yīng" "sī" "kào" "xíng ba" | Almost none |
| Omission | Massive omission — let reader fill in the blanks | Covers all bases, afraid reader won't understand |
| Parallelism | Occasionally 1-2, never 3+ consecutive | 3-5 consecutive parallelism is standard |
| Ending | Action/dialogue conclusion | Summary/escalation/soliloquy conclusion |

### Natural Expression Replacements

> From extensive web-novel writing research:

- Replace "deep breath" → delete directly; if it has function, switch to current character action
- Replace "眼中闪过一丝..." → "he looked down" / "squinted"
- Replace "嘴角勾起一抹..." → "he grinned" / "laughed"
- Replace "仿佛..." → prefer direct description; if metaphor needed, keep only life-like / character-specific ones
- Replace "不禁..." → write action directly
- Replace "缓缓开口" → "said" / use action to lead into dialogue

---

## Detection Flow

### Phase 1: AI-Flavor Scan

Quick scan of user-submitted text, mark AI-heavy locations:

```
## AI-Flavor Detection Report

### Overall Assessment
- AI-flavor level: {mild / moderate / severe}
- Main issues: {1-3 keywords}

### Problem Markers
| Location | Type | Gate | Original | Problem |
|:--------|:-----|:-----|:-------|:--------|
| Paragraph X | banned word | A | "眼中闪过一丝..." | Typical AI high-frequency word |
| Paragraph Y | syntax | B | "..., with..." | AI cliché syntax |
| Paragraph Z | syntax | B | 3 consecutive parallel sentences | Overly tidy |
| ... | mental description | C | "he felt..." | Telling not showing |
| Paragraph M | rhythm | D | paragraph 4-6 sentences, uniform length | Same rhythm throughout |
| Paragraph N | repeated description | C/D | same action split across consecutive paragraphs | Adjacent paragraphs repeat same moment |
| Paragraph P | explanation/summary/God's-eye | G | "what he didn't know..." / "acting really well" / "the reason why..." | Narrator jumps out of the present moment to explain/spoil/evaluate/escalate (pattern 8) |
| Paragraph Q | action checklist | D/E | "reach out, pick up, put down, turn, walk..." | Surveillance-camera-style step list, lacking viewpoint warmth/mental buffer (pattern 10) |

> Type → Gate quick lookup: banned word = A, formulaic syntax = B, direct mental = C, even rhythm = D, dialogue tone = E, summary ending = F, explanation/God's-eye/sense-of-arrangement = G, repeated description = C/D. "Diagnosis and grading" counts "7 Gates with 4+ problems" by Gate column.
```

> **Evaluation only outputs AI-flavor level (mild/moderate/severe) and problem markers**; does not make "first-rate / novice submission first-rate / good value" style sideways market judgments — this skill has no platform submission distribution data, such phrasing is unfounded over-promising.

**Pre-check for deterministic syntax (file mode)**: When input is a local prose file path, "AI-flavor scan" must first run this skill's own script, reporting only — do not modify:

```bash
node scripts/check-ai-patterns.js --check --fail-on=blocking <prose file...>
```

- `severity=blocking` categories (`not-is-comparison` / `em-dash` / `voice-contrast` / `negation-parade` / `reverse-not-is` / `trailer-ending` / `trailer-summary`) merge into Gate B — priority fix in writing/desloping, blocking-level problem.
- Other findings (period stutter, long paragraph, micro-action, formulaic reaction detail, action checklist, abstract summary, set phrases, metaphor density, reasoning chain, system-notice formality, over-refined, low connective density, quote-emphasis abuse, `formulaic-parallelism` tidy parallelism) are read-feel hints only; complete categories and fixes see `references/anti-ai-writing.md`. Among them, formulaic parallelism scans dialogue too — must read context and decide, can't skip just because hook gives dialogue a free pass.
- Handling: delete the negative setup, write the positive directly; or switch to character action / prop detail / body reaction to present it.
- If user only wants detection, keep report, don't edit prose. If executing deslop, only fix read-feel issues that are genuinely harmful and have no narrative function; functional writing marks `[Needs Review]` and is kept.
---

### Phase 2: Diagnosis & Grading

Based on "AI-flavor scan" results, determine AI-flavor level and processing strategy:

| AI-Flavor Level | Quantification Standard (reference) | Features | Strategy |
|:----------------|:-----------------------------------|:---------|:---------|
| Mild | Banned word hits ≤5 / 1000 chars, no 3+ consecutive formulaic syntax | A few banned words, occasional bookish diction | Pass Gate A + B only |
| Moderate | Banned word hits 6-15 / 1000 chars, or 3+ consecutive formulaic syntax | Multiple banned words + formulaic syntax + abstract mental description | Pass Gate A + B + C + D + G |
| Severe | Banned word hits >15 / 1000 chars, or 4+ Gates have problems | Whole text AI-flavored, rhythm/dialogue/ending/explanation all problematic | Full 7 Gates + key section rewrite |

> Quantification standards are reference values. Hit = entry in banned-words.md appears as a substring in the text. If a hit fragment's true substring appears in `.deslop-whitelist`, skip that count (avoid false positives on world-building terminology). Same word appearing once = count once.

> **Priority of determination**: (1) First do quantitative assessment by the "AI-flavor objective indicators" below; (2) Allow ≤1 level subjective downgrade based on genre/context (must give written reason in report); **no upgrade allowed**; (3) When quantitative and subjective conflict, quantitative wins.

**AI-Flavor Objective Indicators**:

| Indicator | Calculation | Mild Threshold | Moderate Threshold | Severe Threshold |
|:---------|:-----------|:--------------|:-------------------|:-----------------|
| Banned word density | hit count / 1000 chars | ≤5 | 6-15 | >15 |
| Consecutive parallelism count | count of paragraphs with same syntax structure in a row | ≤2 | 3-4 | ≥5 |
| Mental word ratio | direct mental description word count / total paragraph count | ≤10% | 10-25% | >25% |
| Dialogue tag density | "say/ask/laugh" etc. / dialogue count | ≤30% | 30-50% | >50% |
| Average sentence length per paragraph | total sentences / total paragraphs | ≤3 | 3-5 | >5 |
| Repeated description density | same info/action/emotion described in multiple consecutive paragraphs / 1000 chars | ≤1 / 1000 chars | 2-3 / 1000 chars | ≥4 / 1000 chars |

> Note: Key scenes (opening, climax, resolution) with 1 instance of repeated description = weighted ≥1 level up (mild→moderate, moderate→severe).

> Above thresholds are reference values, adjust per genre. E.g., historical genre dialogue tag density is naturally higher, can be relaxed.

> **Comprehensive judgment rule**: Take highest level across 6 indicators. If any indicator hits severe → process as severe; no severe then ≥3 moderate indicators → moderate, otherwise mild.

Load [references/anti-ai-writing.md](references/anti-ai-writing.md) "Systematic Tri-Method Deslop" for full flow. Tri-method vs. this skill (coverage, not 1:1 mapping):
- **Pass 1 (Strip Generic)** covers Gate A banned words, Gate C abstract emotion, Gate D tidy parallelism, Gate E same-tone dialogue sweep, Gate G explanation/God's-eye spoiler/soft judgment
- **Pass 2 (Cut Professional Diction)** covers Gate A bookish diction, Gate B formulaic syntax deepening
- **Pass 3 (Restore Natural Feel)** covers Gate D long/short rhythm, Gate E dialogue differentiation, Gate F ending de-escalation, supplement concrete sensory details
- Mild: Pass 1 only; Moderate: Pass 1 + Pass 2; Severe: full tri-method + key section rewrite

---

### Phase 3: Item-by-Item Cleanup

#### Agent invocation: narrative-writer (deslop executor)

After "Diagnosis & Grading" is complete, select execution path in order:

1. **Already inside narrative-writer sub-agent**: inline execute Gate A-G, no longer spawn (nested spawn silently downgraded).
2. **Not in sub-agent and find `narrative-writer` agent in top-to-bottom order**: call via current runtime. Antigravity uses `invoke_subagent(TypeName: "narrative-writer")`, Claude/OpenCode/Codex use respective fields. Keep prompt: `Project directory: {dir}\nTask description: deslop\nScope: {prose file to process}\nAuthor preferences: {prose_style items hit by query}\nAI-flavor level: {diagnosis result}\nStrategy: {Gate range for mild/moderate/severe}\nDelete-first priority: every AI-flavor item first decides deletable — if deletion doesn't lose foreshadowing/hooks/character traits/plot progression/character memory/emotional carryover/causal anchor/essential info/essential turn, then directly delete, otherwise polish through Gate. If seemingly explanatory/evaluative but carrying small coherence, compress to plain carry-over, action or object anchor — don't mechanically delete; existing tasks/evidence/props gaps can be compressed into the character's current concrete pain points, but don't add original event chain. Delete obeys ratio ceiling and char count floor — if below floor, switch to reduce-AI-rewrite, don't delete then pad with new filler.
Handling modes: follow problem patterns in references/anti-ai-writing.md; pattern 8 (explanation/God's-eye/arrangement) goes to Gate G, other new patterns map to corresponding Gate A-F handling. Adjacent paragraphs repeating same info/action/emotion → Gate C/D merge and dedupe.
`

3. **Agent doesn't exist or spawn fails**: execute inline on main thread
#### Delete-First Judgment (Before Each Gate)

Judge every flagged item for deletability first, then consider polishing — many AI-flavor sentences are filler (explanation, padding, counting), polishing still leaves redundancy.
1. Deleting — does it lose foreshadowing, hooks, character traits, plot progression, essential info, or essential turns? If neither lost → delete directly, not through Gate.
2. Any lost → keep the info through corresponding Gate rewrite (only delete "how it's said," not "what's said").
3. Deletion obeys the existing "Over-desloping protection" and "Diagnosis & Grading" ratio ceiling: no whole-section deletion, no narrative function deletion; if deletion drops below char-count floor, switch to reduce-AI-rewrite, don't delete then pad with new filler.
4. After delete, read-through: if a section is reduced to bare shortest sentences, structure words swept clean, every action has a "xxx-ed/lightly" tail — that's over-deleted telegraph body (see anti-ai-writing.md pattern 9). Restore non-peak narrative sentences to natural plain speech, not continue deleting. Deleting filler, not Chinese's natural redundancy — this rule only adjusts the degree of deletion, not the clearing power of banned words and formulaic syntax; Gate A-F fully executed.

Following are detailed rules for each Gate (deletable items polished per these; both agent and main-thread execution must follow):

#### Gate A: Banned Word Replacement

Load [references/banned-words.md](references/banned-words.md), check against banned word table item by item.
**Whitelist mechanism**:

Project root `.deslop-whitelist` file defines this project's exempt vocabulary.
File schema:
- UTF-8 encoding, one word per line
- Lines starting with `#` are comments; blank lines ignored; trim leading/trailing whitespace
- Case-sensitive (Chinese doesn't distinguish)

Matching: when scanning, if a banned word's hit substring's true substring appears in `.deslop-whitelist`, skip that alert. Same matching as banned-words.md, using substring scan.

Example `.deslop-whitelist`:

```
# Project custom exempt words (one per line, # comments)
缓缓                # "Hua Chao" character's nickname, not a banned word
仿佛山海             # chapter title
深邃的山谷           # location name
```

Whitelist applicable scenarios:
- Hit term (e.g., xianxia novel specific terminology that happens to match a banned word)
- Character catchphrase / nickname / setting proper noun
- World-building proper noun
- Original text's intentional rhetorical device
- If `.deslop-whitelist` doesn't exist, don't force-create; note in report that it can be created. Empty whitelist file = no whitelist.
- **Protection rules priority**: Keep creative intent and narrative function > deslop Gate. Gate A-F can only change expression; Gate G deletes non-narrative author explanation (not plot). Any Gate cannot delete foreshadowing, hooks, character traits, character memory, emotional carryover, causal anchors, key info, or essential turns; on conflict, switch to reduce-AI-rewrite or mark `[Needs Review]`.

Replacement rules:
- Banned word → concrete action / detail description
- Don't simply swap for another adjective
- Use "show" instead of "tell"
Example:
- ❌ "眼中闪过一丝不易察觉的悲伤" → ✅ "he lowered his eyes"
- ❌ "deep breath" → ✅ delete directly; if it has function, switch to current character action (e.g., swallow back the words)
- ❌ "嘴角勾起一抹冷笑" → ✅ "he sneered"

#### Gate B: Formulaic Syntax Cleanup

Detect and replace high-frequency AI syntax:

| Syntax | Problem | Solution |
|:------|:-------|:---------|
| Negative setup followed by positive flip in same sentence | One of the most toxic Chinese AI patterns | Write positive directly, or switch to action/detail |
| Cross-paragraph "not A / also not B / only is C" | May be tidy setup, or may be explanation/suspense/exclamation | `formulaic-parallelism` advisory; read context, only compress when repeated outline or dragging scene |
| "As for X not X, how to X" / same verb "not V A, not V B" | Tidy decision bar, negative list; normal dialogue may appear | Contextual review; if just repeating outline/previous text, compress to single judgment |
| ", with..." | Universal modifier, AI favorite | Use independent short sentence or action description |
| "voice not loud, yet with..." | AI favorite voice description | Write actual voice content, sound features or action directly |
| Cliché/monty metaphor | Formulaic metaphor looks AI | Prefer direct description; if metaphor needed, keep only life-like/character-specific ones |
| "he/she knows..." | Tell reader directly | Show cognition through action |
| High dialogue tag density/formulaic tags | Every sentence tagged looks mechanical | Common "say" can be kept; when high-frequency or formulaic, use action/context to replace |
| "似佛/犹如/宛若/如同" | Over-literary | Colloquial expression or direct description |
| "not-unquestionable / obviously" | Bookish judgment words | Talk about specific facts |

**Adjective sweeping**: Check adjectives, attributives, adverbs, demonstrative pronouns, quantifiers before objects/characters — remove if redundant, replace with concise noun if meaning lost.

Examples:
- "white pills" → "pills"
- "racing car" → "car"
- "the chain in my hand" → "chain"
- "old clothes" → "old clothes" (keep meaning)

Adjective principle: at most one adjective modifier per noun, or no modifier — no stacking, no piling.
#### Gate C: Externalize Mental Description

AI-flavored mental description feature: direct statement of emotion.

Replacement strategy:
- "he was very nervous" → "his hand was shaking"
- "she was angry" → "she knocked the cup to the ground, shrapnel hit her feet and she didn't bend to pick up"
- "he was scared" → "he leaned against the door, couldn't step forward"
- "she was sad" → "she turned away, twisted her cuff"
- "he felt a pang of loss" → "he hesitated, put the phone back in his pocket"

**Dedupe repeated descriptions**: When adjacent paragraphs repeatedly express same info/action/emotion, handle through Gate C/D, no separate process.

Handling:
- Merge same moment's repeated descriptions, keep the detail that best drives emotion or plot
- If merged clearly thins out, restore original functional info, or rewrite existing info into more natural action/dialogue — don't add original plot

**Repeated semantics four categories** (same meaning don't repeat, only keep one most suitable and concise):

| Category | Error example | Fix |
|:--------|---------------|-----|
| Adjective repetition | "excitedly laughed and ran over" | "laughed and ran" |
| Synonym repetition | "very important key question" | "key question" |
| Meaning repetition | "I'm hungry, stomach growling" | "I'm hungry" |
| Context subject/object repetition | Previous said "threw all the antidepressants on the ground", next doesn't need to write "the antidepressants on the ground", just write "pills" | Vague and concise colloquial |

**Excessive scene/character/prop description**: Descriptions beyond what serves plot characters → delete directly.

Examples:
- "Yue Huan held a short dagger, blade cold and sharp" → "Yue Huan held a short dagger"
- "Handcuffs tightly gripped the two people's wrists, connected by a not-too-long chain" → "Handcuffs gripped the two people's wrists, chain connecting them"
- "Snowy polar test site, the wind didn't stop" → "Snowy polar test site"

#### Gate D: Rhythm Adjustment

AI writing rhythm problem: syntax overly tidy, paragraphs overly even.

Handling:
- Break consecutive parallelism sentences (keep 1-2, delete the rest)
- Only split bloated modifiers, stacked metaphors, abstract summary long sentences; after rewrite, narrative still dominated by comma-sentences (see anti-ai-writing.md rule 3) — don't split normal comma-sentences into sentence strings
- Occasionally use incomplete sentences (colloquial feel)
- Paragraph long-short alternation (not every paragraph 3-5 lines)
- Don't format by hard metrics: Fanqie high-score samples aren't 50-60 chars per line, nor force line break at every period; break by action/info change naturally, read smoothly if not stiff
- Punctuation rhythm follows tone: avoid all periods; retain functional `?` / few `!` , use action / short sentence / line break / comma / period to express hesitation / interruption / dragging / pause, delete random stacks or screen-filling symbols
#### Gate E: Dialogue De-tone

AI-flavored dialogue feature: every sentence is info-complete, logical, expressive.

Handling:
- Add colloquial expressions ("en", "oh", "ok then")
- Appropriately break dialogue (character can respond off-topic); when dialogue is interrupted or drawn out, use action / line break / short sentence — not `——`
- Use actions to interleave dialogue ("she took a sip. 'then what?'")
- Delete explanatory dialogue (characters won't explain their own motives)
- Gate B also checks dialogue: consecutive tidy negation, `至于X不X，怎么X`, same verb `not V A, not V B` — can't skip because of script hook's dialogue exemption; only keep with clear character voice or task function
- Don't force-expand dialogue to hit ratio; Fanqie ratio varies by genre, dialogue only increases when character truly speaks, must speak at this moment
- Stuttering, pause, curse and repetition serve character identity and emotion, not "human feel" decoration stacked blindly
- Don't turn all dialogue endings to periods: interrogatives keep `?`, climactic peaks keep a few `!`; swallow-back / unfinished / pause → action pause / short sentence / line break, not `……`
#### Gate F: Ending De-escalation

AI writing ending feature: always wants to summarize, escalate, title-drop.

Handling:
- Delete summary statements
- End with action / scene, not with soliloquy
- If ending with "he knew..." / "this moment..." → basically can be deleted
#### Gate G: Remove Explanation / God's-Eye / Arrangement Feeling

Most hard-to-detect, most "AI-like" class (corresponds to anti-ai-writing.md pattern 8). Narrator steps out of the current moment to explain, spoil, summarize, evaluate, escalate, reader smells "author present / plot arranged."

Handling:
- Delete causal explanation: "the reason why... is because" / "originally..." / "this means..." → delete. Causality only from character actions, dialogue, reactions — let reader figure it out themselves
- Delete God's-eye spoiler: "what he didn't know..." / "as if..." / "years later" / "fatefully" / "as if prophesying..." → delete. Only write what the character knows at this moment, suspense for reader to feel
- Delete reader conclusion: "acting really well" / "she's seen it once" / "he's just like that" → delete. Show evidence (expression, action, dialogue), don't conclude for reader
- Delete hidden soft-evaluation: evaluative adverbs ("just right"), spoiler-callout ("she clearly saw"), defining metaphor ("like declaring a predetermined verdict") → delete, or turn into the character's biased present-moment feeling
- Note: Gate G deletes "non-narrative author narration," not plot. If after deletion the section thins, fill with character actions/dialogue, not narrator explanation.

**Task pain point fix boundary**: Task pain points are not fixed formulas, nor universal fill-in-the-blank process buttons. Original text already has task/evidence/troubleshooting/props gaps → can compress explanation summary into the character's current concrete pain points; original text has no gaps → only delete explanation, or switch to actions/dialogue, do not create new event chain. All pain points first try "delete and see": if deletion doesn't lose foreshadowing, hooks, info, relationships, changes, or essential turns → compress or delete.

---

### Phase 4: Deterministic Tail (File Mode)

When input is a prose file path, and "Item-by-Item Cleanup" has been written to disk, **first** do a syntax/paragraph re-scan, **then** mechanical punctuation fallback (dash-to-action-first, then mechanical replacement):

```bash
node scripts/check-ai-patterns.js --check --fail-on=blocking <prose file...>
node scripts/check-degeneration.js --check <prose file...>
node scripts/normalize-punctuation.js <prose file...>
```

Scope of responsibility:
- `check-ai-patterns.js` reports only, doesn't rewrite: `severity=blocking` categories fix prose first then re-scan; advisory first read-through and decide — only fix if truly outline/God's-eye/template feeling, mark functional writing `[Needs Review]`, don't do synonym rotation
- It's a read-feel hint only; complete categories, exceptions and fixes see `references/anti-ai-writing.md`
- `check-degeneration.js` reports model degeneration (verbatim repetition / loop, trailing truncation, placeholder, engineering term leak like `outline`/`beat` etc.), each with `severity: blocking|advisory`. blocking = degeneration signal, deslop can't fix — regenerate that section then deslop; advisory (tier2 sections / ambiguous words) is tip only
- `normalize-punctuation.js` mechanical fallback: clear residual `……`, missed `——`/`—`, double-hyphen `--` and standalone `---`; by default don't change quote style, don't turn functional `?` / few `!` into periods
- Zhihu Yanyan short fiction can keep `「」`; only when user or project explicitly requires, add `--quote-mode ascii` or `--quote-mode yan` to punctuation script
---

### Phase 5: Output Polishing Result

```
## Deslop Polishing Report

### Character Count Protocol
- Original character count: {N0}
- After revision character count: {N1}
- Net change: {N1 - N0} ({percentage})
- Within tier ceiling: {yes / no (exceeds X%, sectioned and marked [Needs Review])}

### Edit Statistics
- Total edits: {N}
- Banned word replacement: {N}
- Syntax adjustment: {N} (including negative flip syntax {N}, ", with..." {N}, voice description {N})
- Adjective sweep: {N}
- Mental externalization: {N}
- Repeated description merge: {N}
- Action checklist merge: {N}
- Semantic dedupe: {N} (adjective repetition {N}, synonym repetition {N}, meaning repetition {N}, subject/object repetition {N})
- Metaphor handling: {N} (delete/keep/revert to concrete scene)
- Rhythm adjustment: {N}
- Dialogue optimization: {N}
- Punctuation rhythm adjustment: {N} (retain functional `?`/few `!`, convert `……`/`——` to action / short sentence / comma / period, clean up non-functional stacks)
- Ending fix: {N}

### Before/After Comparison
{show changes per section, annotate edit type; when >30, show first 10 + last 5 + rest bucketed by Gate}

### Polished Full Text
{**File mode (default; chapter/body files, batch and long-form deslop)**: rewrite and save via Edit/Write, this section only returns ≤200 chars representative excerpt, doesn't send full text to parent session. **Text mode (only for interactive paste, no file path, intermittent snippets)**: output the full polished text.}
```

**Character count hard cap**: Deletion ratio must not exceed "Diagnosis & Grading" tier ceiling (mild ≤15%, moderate ≤25%, severe ≤35%). Exceeding → section output, mark in report, don't mass-delete body.

**Convergence termination**:
1. Same section two consecutive deslop passes with no new edits → stop processing this section
2. Overall upper limit 3 re-scans; 3rd round still has ≥10 edits → mark `[Needs Review]` in report, hand to human
3. Before each round end, do a "check again": any non-compliant spots, fix if yes, stop if no

---

## Use Cases

| Scenario | Action |
|:--------|:-------|
| User pastes a piece "too AI" | Run full detection + deslop flow |
| User says "polish this" | First detect AI-flavor, then deslop |
| User says "check for AI flavor" | Only detect, no changes |
| User writes during writing and requires `only tag / only detect / don't change` | Embedded reminder mode: run "AI-flavor scan" + "Diagnosis & Grading", skip "Item-by-Item Cleanup" + "Deterministic Tail" + "Output Polishing Result"; output problem marker table (with Gate column), don't modify original text, don't write file |

---

## References

Load as needed:

| File | When to Load |
|:-----|:------------|
| [references/banned-words.md](references/banned-words.md) | When detecting and replacing banned words |
| [references/anti-ai-writing.md](references/anti-ai-writing.md) | **Full deslop guide**: prevention + tri-method + examples |
| [references/author-memory.md](references/author-memory.md) + [scripts/author_memory_commit.py](scripts/author_memory_commit.py) | When reading or updating cross-session author style habits |
| [scripts/check-ai-patterns.js](scripts/check-ai-patterns.js) | File mode pre-check + deterministic tail re-scan (read-only, reports only) |
| [scripts/check-degeneration.js](scripts/check-degeneration.js) | File mode deterministic tail re-scan (read-only, reports only) |
| [scripts/normalize-punctuation.js](scripts/normalize-punctuation.js) | File mode deterministic tail mechanical punctuation fallback |

---

## Pipeline Connection

**Pipeline:** Universal
**Position:** Polishing (shared tail)

| Timing | Jump to | Command |
|:------|:-------|:--------|
| Continue writing | story-long-write / story-short-write | `/story-long-write` or `/story-short-write` |
| Found structural issue | story-long-analyze / story-short-analyze | `/story-long-analyze` or `/story-short-analyze` |
| Ready to make cover | story-cover | `/story-cover` |

---

## Language

- Reply in the user's language — whatever language the user uses, reply in that language
- Chinese replies follow the "Chinese Copywriting Layout Guide"