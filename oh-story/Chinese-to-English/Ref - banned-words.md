# Banned AI-Sounding Words and Sentence Patterns

<!-- Six same-named copies must remain byte-for-byte identical; after changes, run scripts/check-shared-files.sh -->

## Most Toxic Banned Patterns (Fix Every Occurrence; Highest Priority)

These are the most damaging AI-sounding patterns in web fiction. Once an author develops the habit, they tend to recur. Gate A's first scan must catch them:

| Severity | Pattern | Bad example | Fix |
|------|------|--------|------|
| ★★★★★ | `不是A，（而）是B` / `不是A，不是B，（而）是C` (“not A, but B” / “not A, not B, but C”; `而` may be omitted and still counts) | `他不是冷漠，而是绝望` (“He wasn't indifferent; he was desperate.”) | State B directly or use a more natural construction |
| ★★★☆☆ | Cross-paragraph `不是A。/也不是B。/只是C。` (“Not A. / Nor B. / Only C.”) | `不是嚎啕大哭。/也不是扯着嗓子喊不舍。/只是一个人走远了……` | Review the meaning. If it repeats the outline or slows the scene, compress it to C. Keep it when the exclusions serve a genuine defense or suspense function |
| ★★★★ | Universal adverbial `，带着……` (“with…”) | `他笑了一下，带着一丝不易察觉的嘲讽` | Remove the modifier and keep the main clause, or replace it with a concrete action |
| ★★★★ | Emotionless-voice formulas: `声音不大，却带着……` / `语气毫无波澜` / `平静无波` / `声音平直/平平/听不出情绪` | `她声音不大，却带着不容置疑的力量` | Write the spoken words, an audible quality, or an action directly |
| ★★★★ | `他/她知道……` (“he/she knew…”) | `他知道这一切都来不及了` | Show the realization through behavior |
| ★★★ | `仿佛/犹如/宛若……一般` (“as if / like…”) | `仿佛能穿透一切一般` | Delete it or describe the fact plainly |
| ★★★ | `眼中闪过一丝……` / `嘴角勾起一抹……` | `眼中闪过一丝悲伤` | Delete it; write what the character says or decides in that moment |
| ★★★ | `心中涌起一股……` / `心头一震` | `心中涌起一股暖流` | Show what it changes: a choice, line, object, or consequence |
| ★★★ | Abstract fate/opening wrap-ups: `命运……棋局/獠牙` / `这一刻终于明白` / `反击才刚刚开始` | `命运终于露出獠牙；属于他的反击才刚刚开始` | Return to a document, action, line of dialogue, or physical consequence visible to the character now |
| ★★ | End-of-chapter preview `他不知道的是……` (“What he didn't know was…”) | `他不知道的是，更大的风暴即将来临` | End on a concrete hook object or event, not a vague preview |

> One ★★★★★ match is strong evidence of severe AI flavor; two or more ★★★★ matches trigger a moderate-level rescan.

The `formulaic-parallelism` check in `check-ai-patterns.js` also flags `至于X不X，怎么X` and same-verb `不V A，不V B`. These can be functional colloquial speech, so they are advisory only. Gate B must read the surrounding dialogue and review the context. If the line merely restates the detailed outline or earlier prose, compress it into one judgment; do not skip it just because dialogue is exempt from the hook.

**Punctuation**: In prose, including narration and dialogue, do not use em dashes `——`/`—`, double hyphens `--`, or ellipses as pauses. Replace them with periods, commas, short sentences, or action beats. There is no dialogue exception for em dashes. Yanyan-style `「」` quotation marks are unaffected.

---

## Tier 1 Banned Words (Replace Every Occurrence)

> Tier 1 contains only expressions that are nearly absent from real-person corpora and strongly characteristic of AI. Natural adverbs and function words that people use frequently belong under Tier 2 density control instead.

### Modality
`仿佛、犹如、宛若、如同、一丝、一抹、些许、几分、隐约、毫无征兆、几不可闻、微不可察`

Approximate functions: “as if,” “like,” “a trace,” “a hint,” “somewhat,” “faintly,” “without warning,” “barely audible,” and “imperceptible.”

### Actions
`深吸一口气、不禁` — “take a deep breath,” “couldn't help but”

### Expressions
`眼中闪过、嘴角勾起、眉头微皱、眉眼低垂、瞳孔微缩、瞳孔收缩、瞳孔一缩、指节泛白、眼神锐利、目光锐利`

These are stock flashes in the eyes, curling lips, slight frowns, lowered gazes, contracting pupils, whitening knuckles, and “sharp gaze” descriptions.

### Interior State
`心中一动、心头一震、心下了然、心中暗道、心底泛起、不由得、心中一凛`

These are stock internal-reaction formulas such as “his heart stirred,” “her heart jolted,” “he understood inwardly,” and “she thought to herself.”

### Judgment
`不容置疑、不容置喙、不易察觉、显而易见、毫无疑问、不可否认、前所未有`

Approximate meanings: “unquestionable,” “allowing no argument,” “imperceptible,” “obvious,” “without doubt,” “undeniable,” and “unprecedented.”

### Description
`坚定、闪烁着光芒、狡黠、深邃、凛冽、冰冷`

Approximate meanings: “resolute,” “glittering with light,” “sly,” “profound,” “biting,” and “icy.”

### Transitions
`不由自主、情不自禁、自然而然、话锋一转`

Approximate functions: “involuntarily,” “unable to help oneself,” “naturally,” and “changing the subject.”

## Tier 2 Banned Words (Replace When Overused)

### Context-Sensitive Words (Address Only When Frequent or Used as a Crutch)

`突然、陡然、骤然、猛然、好像、似乎、瞬间、猛地、死死地` — variants of “suddenly,” “as if,” “seemingly,” “instantly,” “violently,” and “tightly.” They may remain in character speech, genuine sudden events, time compression, or uncertain point of view. Rotating synonyms to disguise repetition is not an exemption; count them as the same density pattern.

### Weakening Adverbs (Density Control)

`缓缓、微微、轻轻、淡淡` — “slowly,” “slightly,” “gently,” and “faintly.” Combined total: ≤3 per 1,000 Chinese characters. All four also count toward `cliche-density-tic`. Isolated natural uses may remain; replace them when they cluster or cushion every action.

### Formal Register → Colloquial

| Formal wording | Colloquial replacement |
|--------|-----------|
| `瓦解` (“disintegrate”) | `消失 / 散了 / 没了` (“disappear / fall apart / be gone”) |
| `无名火` (“nameless anger”) | `烦躁` (“irritation”) |
| `往我心上捅刀子` (“stab a knife into my heart”) | `心烦意乱` (“upset”) |

### Summary Patterns

- `他/她终于明白...` — “He/she finally understood…”
- `他/她这才意识到...` — “Only then did he/she realize…”
- `这一刻，他/她终于明白/意识到...` — “At that moment, he/she finally understood/realized…”
- `从这一刻开始...` — “From that moment on…”
- `属于X的反击/复仇/故事，才刚刚开始` — “X's counterattack/revenge/story had only just begun.”
- `命运/宿命 + 齿轮/棋局/獠牙/改写/安排` — fate/destiny paired with gears, chessboards, fangs, rewriting, or arrangements
- `此刻，他/她...` — “At this moment, he/she…”
- `一切...都...` — “Everything…”
- `原来...` — “So it turned out…”

### Parallel Patterns

- Three or more consecutive sentences with the same structure
- `有的...有的...有的...` — repeated “some… some… some…”
- `一边...一边...一边...` — repeated simultaneous-action clauses

### Elevated Wrap-Up Patterns

- `这一刻...` — “At this moment…”
- `他知道...` — “He knew…”
- `她明白...` — “She understood…”
- `这就是...` — “This was…”

## Banned Sentence Templates

| Pattern | Example | Problem |
|------|------|------|
| `不是A，而是B` | `他不是冷漠，而是绝望` | Most toxic; state B directly |
| `...，带着...` | `他说，带着一丝无奈` | Universal adverbial |
| `声音不大，却带着……` | `她声音不大，却带着不容置疑的力量` | AI-favored voice description |
| `仿佛能...一般` | `仿佛能穿透一切一般` | Pseudo-classical register |
| Excessive dialogue tags / formulaic tags | `好的，他说道` | Ordinary “said” may remain; address it when frequent or formulaic |
| `他/她感到...` | `她感到一丝失落` | Telling instead of showing |
| `他/她意识到...` | `他意识到事情不对` | States the realization directly |
| `眼中闪过一丝XX` | `眼中闪过一丝悲伤` | Formulaic |
| `嘴角勾起一抹XX` | `嘴角勾起一抹冷笑` | Formulaic |
| `心中涌起一股XX` | `心中涌起一股暖流` | Formulaic |
| `取而代之的是` | `笑容消失，取而代之的是冰冷` | AI transition template; state the new condition directly |
| `淬了/淬着X` | `眼里淬了毒` | AI synesthesia cliché; use action or dialogue |
| `显得（有些）X` | `他显得有些兴奋` | Telling instead of showing |
| `心底/心里某个地方+软` | `心里某个地方软得一塌糊涂` | Romance cliché; write an action |
| `（浑身）散发着一股X气息/气场` | `浑身散发着一股生人勿近的气息` | Generic aura description; show other people's reactions |
| `命运/宿命 + 齿轮/棋局/獠牙/改写/安排` | `命运终于露出獠牙` / `早已布好的棋局` | Abstract authorial summary; replace it with a document, action, dialogue, or physical consequence the character encounters now |
| `这一刻终于明白/从这一刻开始/才刚刚开始` | `这一刻，他终于明白` / `反击才刚刚开始` | AI wrap-up register; remove the summary and end on an action or unresolved problem |

## Simile Categories (Review by Default; Do Not Delete All by Default)

Similes containing `像/如/仿佛/犹如/宛若` are not automatically AI-generated. The real risks are dense clusters, generic literary comparisons, ornate similes that substitute for plot movement, and paragraph-ending comparisons that interpret meaning for the reader. Use this table to identify similes that need review:

| Simile category | Example | Handling |
|---------|----|------|
| Everyday / character-specific | `像一头被抛弃的野狗` (“like an abandoned stray dog”) | Keep it if it fits the viewpoint and conveys information or emotion |
| Object / phenomenon | `像一把刀` (“like a knife”); `脸色惨白得像这漫天的雪` (“a face as pale as the snow filling the sky”) | Ordinary functional comparisons may remain; rewrite formulaic or repeated ones as plain description |
| State cliché | `梨花带雨`; `如沐春风` | Prefer deletion or a concrete action/expression |
| Abstract | `像命运的齿轮`; `像上辈子的尘埃` | High risk; return to actions, objects, sounds, or consequences |
| Hypothetical | `力道大得像是要把骨头捏碎` (“with enough force to crush the bone”) | Keep it when it reflects bodily perception; replace stacked exaggeration with the factual consequence |

Principle: assess function first, then density. Keep the one or two comparisons that best convey information or emotion. Rewrite the rest using direct description, verbs, nouns, effects, results, or facts. Do not replace deleted similes with a fresh batch of similes. For example, if `脸色惨白得像这漫天的雪` is only a stock phrase, reduce it to `脸色惨白` (“her face was pale”). If the snow is actively pressing on the character's perception, keep it or replace it with a concrete image the character sees.

> `metaphor-density-tic` is advisory: it calls for a full read-through, not an automatic block. Everyday, character-specific, and individually functional similes may remain.

## Quick Replacement Guide

| Source type | Replacement method | Example |
|----------|----------|------|
| Abstract emotion word | First determine whether context already establishes it; then use a choice, dialogue, object, consequence, or one direct statement | If `紧张` (“nervous”) does not affect the next step, state it plainly or delete it. If it invalidates a signature, write the invalidated result |
| `感到XX` (“felt XX”) | Remove `感到`, then decide whether the scene still needs an emotion sentence | `他感到愤怒` can become `他火了`, or simply show him withdrawing the offer; do not default to a clenched fist |
| Stacked adjectives | Plain description | `美丽动人的笑容` → `她笑了` |
| Formal expression | Colloquial wording | `不容置疑` → `就是` |
| Explanatory description | Leave room for inference | `他因为害怕而...` → `他退后一步` |
| Consecutive parallelism | Keep the strongest line | Reduce three parallel sentences to one |
| Summarizing or elevating line | Delete it | `这一刻，她终于明白了...` → delete |
| `不是A，而是B` | State B directly or use a more natural construction | `他不是冷漠，而是绝望` → state B directly |
| Extra modifiers (adjectives, attributives, measure words, demonstratives) | Delete them | `白色的药片` → `药片`; `手里那截链子` → `链子`; `飞驰的汽车` → `车` |

**Do not reuse replacements**: The right column gives directions, not standard answers. When the same banned expression appears multiple times in a chapter, make each revision concrete in a different way. If the same replacement recurs—every instance becomes `垂下眼`, or every action gains `了一下`—the replacement itself becomes a new template fingerprint.

**Prioritize cliché density**: When `check-ai-patterns.js` reports `cliche-density-tic`, the banned words are not isolated mistakes; they have accumulated into a formulaic voice. Do not begin by swapping synonyms. First delete abstract summaries, then anchor emotions and judgments in actions, objects, dialogue, and concrete consequences visible to the character now.

**Test every stock reaction for deletion**: A `stock-reaction-tic` warning does not ban physical description. For each occurrence, ask whether deleting it would damage information, choice, relationship, an object, or the result of an action. If not, delete it; do not replace `指尖轻叩` with `目光微沉`. Keep the reaction when it clearly expresses an injury, failed action, character habit, or plot consequence.
