# Complete Guide to Removing AI-Like Writing

<!-- Keep five same-named copies byte-for-byte identical; after changes, run scripts/check-shared-files.sh -->

> Identifies AI-writing fingerprints, provides a systematic three-pass cleanup method, defines prohibited-word constraints, and supplies rewriting examples. Consult after drafting prose when reviewing and revising AI-like writing.

---

## Decision Router

| What You Are Doing | Module to Consult |
|-----------|-------------|
| Running a post-draft AI-style review | Core Rules → AI-Writing Pattern Detection → Quality-Dimension Review |
| Rewriting a passage with a strong AI feel | Rewrite Examples + Conflict-Dialogue Examples |
| Checking for prohibited words | Prohibited Words and Sentence Patterns → High-Frequency AI Terms (Pattern 1) |
| Systematically cleaning an entire chapter | Systematic Three-Pass AI Cleanup |
| Checking whether a chapter ends with summary or thematic elevation | AI-Writing Fingerprints → Summary-Style Chapter Endings |
| Determining whether emotion is told rather than shown | Show, Don’t Tell + Additional AI-Cleanup Techniques |
| Scanning overall chapter quality quickly | Quick Self-Check Mnemonic + Quality-Dimension Review |

## Directive Tone

This file relies primarily on diagnostic questions and high-risk lists. Check Tier 1 high-risk terms first. Judge Tier 2 and context-sensitive terms by frequency, context, and whether they substitute for real writing. When rules conflict, preserve creative intent and plot function before making mechanical replacements.

---

## AI-Writing Fingerprints (Must Be Avoided)

### High-Frequency AI Terms

> See [banned-words.md](banned-words.md) for the complete prohibited-word list.

**Additional categories** not covered by `banned-words.md`:

| Category | Replacement Principle |
|------|---------|
| Abstract elevation terms such as fate, destiny, and inevitability | Replace abstractions with concrete events |
| Generic similes such as “like a tide,” “like lightning,” or “like a spring breeze” | Prefer no simile; when one is necessary, retain only a few grounded comparisons that fit the character |

### Quotation Marks Are for Real Quotations, Not Emphasis on Ordinary Nouns

Do not put double quotation marks around ordinary nouns, familiar actions, or concepts the author has just coined merely to “emphasize” them. This artificially turns ordinary words into terminology. Repetition makes the prose especially likely to resemble a model highlighting ideas for the reader. The `quote-emphasis-tic` rule in `check-ai-patterns.js` only raises a prompt; context determines the final judgment.

- **Revise**: so-called “opportunity,” complete this “transformation,” or find the real “answer.” If the words have only their ordinary meanings, remove the quotation marks and let the events establish their importance.
- **Retain**: Character dialogue, exact quotations, book or story titles, codenames with genuine setting-specific meaning, and original text displayed through in-scene media such as messages, notices, or system announcements.
- **Boundary**: Quotation marks may define a term on first use, but do not repeat them afterward. They may also mark sarcasm, irony, or a character’s deliberate vocal emphasis when the context makes clear who is emphasizing the word and why.

### Summary-Style Chapter Endings

Do **not** end chapters with:

- A summarizing realization: “He finally understood...”
- A thematically elevated exclamation: “This night was destined to leave no one asleep.”
- A philosophical conclusion: “That is how life is...”
- A foreshadowing announcement: “What he did not know was that an even greater storm was approaching.”

**Correct approach**: End with an action, dialogue, or suspense. Let the plot create its own resonance.

### Stacked Description: Writing the Same Action Three Times

**Detection pattern**: An action occurs, then receives sensory detail, then receives a physical reaction, with all three presented in separate paragraphs. Readers see the same action broken apart and written three times.

**Typical characteristics**:

- A general action appears first, the same action is elaborated, and then a bodily reaction is added. All three paragraphs describe the same event.
- “Occurrence layer → sensory layer → reaction layer” appears in consecutive paragraphs.
- Each dimension occupies a separate paragraph rather than being integrated into continuous prose.

**Incorrect example**:

> Father Lin lowered his head, held the document down with his left hand, and brought his pen to the page with his right.
>
> His arm shook from elbow to wrist.
>
> The nib paused on the paper, made one horizontal stroke, then stopped again. The left-falling stroke in the character “Lin” came out crooked.

The same action—his hand shaking while writing—is divided across three paragraphs, each describing a different dimension of the same instant.

**Correct approach**: Integrate occurrence, sensation, and reaction into one continuous paragraph so readers experience a complete moment:

> Father Lin held the document down with his left hand and brought the pen to the page with his right. The nib veered as soon as it touched the paper; his arm would not stop shaking from elbow to wrist, and the horizontal stroke trailed away at an angle.

Occurrence, sensation, and reaction appear together in one paragraph.

**Treatment principle**: Preserve emotional details that perform a function, but combine repeated descriptions of the same instant into one continuous image. If the result becomes noticeably thin, restore functional information from the original or express existing information more naturally through action or dialogue. Do not invent plot events, setting rules, relationships, or timeline details.

---

## Core Rules

> **Rule 3 governs sentence length**: If Rules 1–4 or any other instruction about “short sentences,” “breaking sentences up,” or “deleting whatever can be deleted” conflicts with Rule 3, follow Rule 3.

### Rule 1: Diagnose Paragraph Density

Paragraph length has no fixed virtue. The key question is whether reading aloud or on a phone feels obstructed:

- A paragraph generally carries one action, one information change, or one tightly connected group of reactions.
- If a long comma chain crowds several complete actions into one paragraph and forces the reader to pause for breath, divide it at an action or information change.
- If consecutive short paragraphs resemble an outline, combine adjacent sentences from the same shot so the image remains continuous.

```
过密：他看着窗外的雨，心中涌起一股说不清的感觉，这些年走过的路和很多已经忘记的事都在这一刻涌上心头。

更自然：他盯着窗外的雨，雨从下午下到天黑。
"你还在想她？"老刘问。
他没说话。
```

<!-- translation-companion: non-executable -->
```text
Too dense: He watched the rain outside the window, overwhelmed by a feeling he could not name, as the roads he had traveled over the years and many things he had already forgotten all returned to him at that moment.

More natural: He watched the rain outside the window. It had been falling since afternoon and was still falling after dark.
“Are you still thinking about her?” Old Liu asked.
He said nothing.
```

### Rule 2: Action + Dialogue + Emotional Reaction

Cycle among the three elements to advance the scene. Do not write more than two paragraphs of uninterrupted internal thought:

```
动作 -> 对话 -> 情绪反应 -> 动作 -> 对话 -> ……
```

<!-- translation-companion: non-executable -->
```text
Action → dialogue → emotional reaction → action → dialogue → ...
```

Do not write “he felt” or “he thought” to convey emotion. Use physical reactions and behavior:

- Do not write “He was nervous.” Write: “His palms were slick, and he nearly dropped his chopsticks.”
- Do not write “She was furious.” Write: “She smashed the cup. A shard struck the top of her foot, but she did not bend to pick it up.”
- Do not write “He was heartbroken.” Write: “He sat in the car for twenty minutes before starting the engine.”

These substitutions apply to major emotional beats. A low-intensity transitional emotion may be stated briefly—“He was a little annoyed”—without externalizing every feeling.

### Rule 3: Appropriate Sentence Length—Short Sentences Are a Tool, Not the Default

Narration should default to **long sentences linked by commas**: connect two to four actions or pieces of information in one sentence, with roughly 8–12 Chinese characters between commas and 20–30 Chinese characters in the complete sentence. Use an isolated short sentence occasionally for emphasis; do not make it the narrative default.

| Scene | Sentence Length | Example from Long-Form Source Material |
|------|------|------|
| Daily life, progression, and description—most narration | 8–12 Chinese characters between commas; 20–30 per sentence | A cold, damp smell rushed over him. A thin layer of straw lay beneath him, wet enough to cling to his skin. |
| Dialogue | Conversational; length follows the character | “Are you crazy?” “Maybe.” |

**Unacceptable—equivalent to an AI-style failure**:

- Chains of fragments containing five or fewer Chinese characters between commas, equivalent to “He raised his hand, opened the door, entered, sat down.”
- Three-to-eight-character sentences throughout, with periods so frequent that the prose resembles an outline or telegram.
- Mechanical alternation between one long sentence and one short sentence.

> **Calibration from successful fiction**: A study of narration from the first eight chapters of 125 highly successful long-form works across contemporary romance, urban fiction, historical romance, fantasy, and history on Qimao found an average of 8.8–9.6 Chinese characters between commas and 22–24 per sentence. Comma-linked long sentences represented 74–80% of narrative sentences. Fragments of five or fewer characters represented about one fifth and were mainly isolated time phrases, transitions, or emphatic actions. Short-form Yanyan-style stories use shorter paragraphs—single-sentence paragraphs of 15 characters or fewer can approach half, compared with roughly one quarter to one third in long fiction—but their internal sentence rhythm matches long-form fiction: **paragraphs become shorter by form; sentences do not become fragmented internally**.

### Rule 4: Conversational Expression

- Slang and profanity are permitted when they fit the character.
- Dialogue must not sound formal: replace “I believe this matter is inappropriate” with “I don’t think this is a good idea.”
- Narration must not posture: replace “His gaze burned like a torch” with “He stared without moving his eyes.”
- Prefer phrases over idioms: replace “utterly helpless” with “there was nothing he could do.” This applies only to dialogue and narration close to a character’s voice. Ordinary narrative idioms such as “without showing emotion” or “absentminded” may remain.

---

## Show, Don’t Tell

| Tell | Show |
|-------------|-------------|
| He was a coward | He turned the test report over three times but still could not open it |
| The bar was loud | The bartender had to shout in his ear twice before he heard |
| She was wealthy | She tossed a credit card onto the table; the number printed on its face was worth ten times the meal |
| Their relationship was terrible | He stubbed out his cigarette in the tea she had just made; expressionless, she pushed the cup aside |
| He was intelligent | Three seconds. He looked at the document for three seconds, then closed it. “Page three, second line.” |

**Core Methods**:

1. Replace adjectives with behavior.
2. Replace summaries with details.
3. Replace narrative explanation with dialogue.
4. Replace emotion words with reactions.

---

## Quality-Dimension Review

### 1. Core Consistency—Highest Weight

- Is the plot consistent with the outline and preceding text?
- Does character behavior fit established characterization?
- Do setting details contradict one another?

### 2. Surface Revision—Prevent AI Fingerprints

- Does the prose contain high-frequency AI terms listed above?
- Does the chapter end with a summary or thematic elevation?
- Does it contain a long block of pure internal thought?
- Do paragraph breaks follow dramatic units and shots naturally, avoiding mechanical one-sentence paragraphs or outline-like fragmentation created merely to shorten them?

### 3. Formatting Consistency

- Keep dialogue formatting consistent with project or platform conventions. Zhihu Yanyan-style short fiction may use 「」.
- Match punctuation rhythm to tone. Do not flatten everything into periods. Preserve functional question marks and a small number of exclamation points. Express hesitation and interruption through action or short sentences rather than forcing pauses with ellipses or em dashes.
- Mark scene changes clearly.
- Keep the timeline clear and traceable.

### 4. Readability

- Do several long sentences suppress the reading rhythm without actions, dialogue, or short sentences that provide breathing room?
- Is the dialogue conversational?
- Are unusual words or setting terms unexplained?
- Does the pace vary rather than remaining uniform?

### 5. Logical Coherence

- Are character motivations plausible?
- Is the event’s causal chain clear?
- Does the timeline align?
- Does each character know only what they could reasonably know, without an omniscient perspective?

---

## Quick Self-Check Mnemonic

```
一事一段，镜头自然断。
对话要像人说话。
心情不写心里话。
结尾不搞大升华。
打斗不写流水账。
日常要埋伏笔桩。
```

<!-- translation-companion: non-executable -->
```text
One event per paragraph; break naturally with the shot.
Dialogue should sound human.
Do not explain every feeling.
Do not elevate the ending.
Do not turn combat into a chronological list.
Plant future developments in daily scenes.
```

> Web-fiction paragraph rule: Break naturally when a dramatic unit, shot, or event ends. Short paragraphs read quickly; long paragraphs carry complete reasoning, atmosphere, or an emotional chain. Avoid mechanical single-sentence paragraphs and uniform paragraph lengths.

---

> **Calibration from highly rated Tomato Novel samples**: Tomato Novel prose is closer to “short mobile paragraphs + natural function words + in-scene action/dialogue” than to mechanical metric compliance. A 305-chapter sample window found a median paragraph length of roughly 23.5 Chinese characters; lines 50–60 characters wide averaged only 5.1%. Average dialogue share was about 20.6%; only 3 of 305 chapters reached 50% dialogue, and only 59 of 305 opened with dialogue. Every sample used `地/得`; 275 used `很`; 267 used `像/好像/仿佛/如同`; 176 used enumeration commas; and 281 used ellipses. Conclusion: Review these features in context. Do not impose zero-tolerance prohibitions.
>
> **Anti-gaming boundary**: Do not force a line break after every sentence, replace `……` with `........`, replace every `地/得` with `的`, prohibit every enumeration comma, “very,” or “like,” force dialogue into the opening, or rearrange chapters into a fixed “three turns and four pieces of evidence” pattern merely to evade detection. Removing AI-like writing is line editing, not structural rewriting. Unless the user explicitly requests a rewrite, do not change chapter order, foreshadowing distribution, dialogue share, or the timing of character information.

---

## Quick Reference: Prohibited Words and Sentence Patterns

> See [banned-words.md](banned-words.md) for the complete list and sentence templates.

### Correct Replacement Examples

- “He felt a trace of nervousness” → “His hand was shaking.”
- “She was very sad” → “She turned away and crushed the cuff in her fist.”
- “‘Okay,’ he said” → “‘Okay.’ He slipped the key card back into his pocket.”
- “He took a deep breath” → “He swallowed the words.”

---

## Ten AI-Writing Patterns

### Pattern 1: High-Frequency AI Terms

| Prohibited | Replace With |
|------|--------|
| Cannot help but | Delete |
| As if / just like | Delete or use concrete description |
| Came into view | Delete |
| Thought secretly | Show the thought through action |
| Said gravely / said lightly | Use an action tag |
| His expression changed | Use a specific expression or action |
| The corner of his mouth rose slightly | He smiled / one corner of his mouth lifted |
| Involuntarily | Delete |
| Behold / at this very moment | Delete |
| His gaze burned like a torch | Delete or make concrete |

### Pattern 2: Excessive Weakening Adverbs

Threshold: More than three per 1,000 Chinese characters is an AI signature. Closely monitor equivalents of “slightly,” “faintly,” “slowly,” and “gently.”

### Pattern 3: Inflated Significance

- “Far-reaching significance” → state the concrete consequence.
- “Unprecedented” → provide a comparison.
- “It may be said” → delete.

### Pattern 4: Generic Conclusions

- “The future is promising” → end with unresolved tension.
- “Boundless prospects” → delete.
- “Full of hope” → write the specific next action.

### Pattern 5: Academic Paragraph Structure

These openings in fiction indicate AI intrusion:

- “It is not difficult to see”
- “This shows that”
- “In fact”
- “In conclusion”

### Pattern 6: Excessive Formal Conjunctions

If narrative prose repeatedly uses equivalents of “thereupon,” “meanwhile,” “thereby,” “consequently,” or “admittedly,” replace them conversationally or delete them.

### Pattern 7: Compulsive Sets of Three

AI tends to force ideas into sets of three to appear “complete.” Reduce the set to its strongest item.

Across paragraphs, the pattern “Not A. / Nor B. / Only C.” is advisory under `formulaic-parallelism`. It may be artificial symmetry, but it may also convey a defense, eliminate suspense possibilities, or escalate emotion. Compress it only when it repeats an outline and slows the scene. Treat this warning—and patterns such as “As for whether X, how could X” or repeated “not verb A, not verb B”—as a semantic review. Check dialogue too, but preserve it when it has a clear character voice or task function. If it comes from several detailed-outline fields repeating one requirement, the manuscript may use the requirement only once rather than restating every field.

### Pattern 8: Explanatory Voice, Omniscience, and Visible Plot Arrangement

This is the hardest and most recognizably AI-like category. The narrator steps outside the character’s present experience to explain, foreshadow, summarize, classify, or elevate. Readers can sense the author’s presence and the feeling that the plot has been arranged. This produces preachiness, omniscience, mechanical prose, and contrivance.

| Expression | Example and Revision |
|---|---|
| Explaining causality | Delete constructions such as “The reason... was because,” “It turned out,” “This meant,” and “Precisely because.” Let readers assemble causality from action, dialogue, and reaction |
| Omniscient foreshadowing | Delete “What she didn’t know,” “Little did he know,” “Many years later,” “By some mysterious design,” and “As if foreshadowing.” Write only what the character currently knows and let readers experience the suspense |
| Drawing conclusions for readers | Delete judgments such as “What a performance,” “She had seen this play before,” or “He was that heartless.” Present the facial expressions, actions, and dialogue; let readers judge |
| Summarizing psychology for the character | Replace “She understood that all of this was fate” with one biased passing thought or a bodily reaction |
| Explaining all meaning through summaries, motives, and evaluations | Delete conclusions such as “He finally understood,” “This was the best choice,” and “Everyone would remember this moment.” Replace them with the concrete unresolved problem, unfinished action, or local feedback the character must handle now. Do not retain the evaluation and tack on an object or action |
| Visible arrangement and forced setup | Do not insert background or a long flashback merely to support later events. Introduce background in fragments through a passing thought, half a line, or an object when the character genuinely needs it |
| Elevated ending | Replace balanced moral statements and thematic final lines with one action or an unfinished line, pressing the meaning into the image |
| Abstract fate/opening conclusions | Replace “Destiny finally bared its fangs,” “a game arranged long ago,” “at this moment he finally understood,” or “his counterattack had only begun” with a document, action, dialogue, or physical consequence the character can perceive. Prioritize this when `check-ai-patterns.js` reports `abstract-summary-tic` |
| High cliché density | When phrases equivalent to “as if,” “a trace,” “a hint,” “took a deep breath,” “calm and still,” or “knuckles whitened” recur together under `cliche-density-tic`, do not rotate synonyms. Return the entire passage to evidence in the character’s immediate experience: documents, actions, dialogue, and physical consequences |
| Stock reaction details | When tapping fingertips, fists clenched in sleeves, whitened knuckles, averted gazes, or “a voice as calm as if reading...” accumulate under `stock-reaction-tic`, test deleting each one. Remove details that only label emotion and do not change a choice, relationship, object, or action outcome. Do not substitute a different body part or synonym. Keep bodily details that affect an injury, cause an action to fail, or have a plot consequence |
| Excessive metaphor density | When markers equivalent to “like,” “as if,” or “just as” recur under `metaphor-density-tic`, preserve the one or two comparisons that best convey information or emotion. Convert the rest to concrete actions, objects, sounds, or consequences; do not invent replacement metaphors |
| Excessive bureaucratic system notices | Keep bracketed rules, panels, and announcements as screens, notices, or other media visible to a character. If `system-notice-formality-tic` fires, simplify some rigid terms inside the medium or show the concrete consequence the character understands immediately. Do not turn the notice into narrator explanation |

**A subtler layer, difficult to self-review because it has no marker words**, produces the same sense of arrangement and omniscience:

- Evaluative adverbs and complements: “her concern was exactly measured,” “her smile was perfectly proportioned,” or “no more and no less” stamp the author’s judgment that a performance is false. Write only the action—“She covered her mouth with a handkerchief, but her eyes did not move”—and let readers decide.
- Foreshadowing that states subtext: “She saw through that smile” or “everyone could tell he was lying” exposes what should remain hidden. Leave it unstated.
- Defining similes and final judgments: “like pronouncing a predetermined verdict” or “like looking at a dead object” decide the character’s meaning. Delete them unless they express the viewpoint character’s intense immediate subjectivity; even then, they must be a biased instant impression rather than an objective declaration.

Self-check every sentence: Is the **character experiencing**, or is the **author explaining or arranging**? Delete any moment when the author steps forward, or recast it within the character’s viewpoint. The fundamental remedy is a locked deep-limited viewpoint; see “Viewpoint Stance: Deep Limited” in writing-craft.md. When the camera is anchored inside the character’s body, the author has nowhere to step in.

Revision priority: Delete or replace the contaminated sentence in place. Do not append a “human” detail to the end of the paragraph. When information must remain, replace the summary, motive, or judgment with a concrete pressure the character can encounter now: a problem, procedure, reply, payment, or sound outside the door. Preserve information already carried by an in-scene phone, screen, notice, sign, form, or similar medium rather than converting it into narrator explanation. The carrier must follow the plot, not a fixed checklist.

**A task obstacle is neither a fixed formula nor a universal way to add procedure.** It merely returns an existing explanation to the unresolved issue the character currently faces. First ask whether the original contains something that must be done and something blocking it. Only then may the explanation become a task obstacle. Otherwise, delete the explanation or replace it with action/dialogue without inventing an event chain. After revision, perform a deletion test: If removing the sentence does not affect information, emotion, relationships, cost, or foreshadowing, compress or delete it.

**Removing explanatory prose does not mean confusing the reader.** When a new term, setting element, or object first appears, give readers one anchor through a character’s action, a natural half-line in dialogue, or a physical consequence in the scene. Show its present function or weight without explaining its entire history or mechanics, but do not throw readers a meaningless term. Handle memory, emotional pauses, and causal continuity the same way. If an apparently explanatory sentence actually provides local continuity—why a character blushes, pauses, or cannot control their voice—do not delete it mechanically. Compress it into the character’s immediate language, action, object, or half-formed thought.

Example: When `蓝晶` first appears, do not write “This is a device that stores memories.” Instead, show her pressing the `蓝晶` to her temple as someone else’s memories burst into view. Readers see its function while the complete explanation remains unresolved. Distinguish an anchor—a consequence, memory, or emotional connection the character perceives now, which should remain or be compressed—from explanation, where the author describes history, mechanics, or conclusions and should be removed.

### Pattern 9: Overcompression—Telegraphic Prose

This is the reverse fingerprint created by deleting too aggressively. Every sentence has been reduced to its shortest possible form, structural particles have disappeared, and each action receives a tiny “slightly” or “a little” reaction. Individual sentences look clean, but the sequence resembles an outline and feels choppy. The objective is to remove waste—explanation, padding, and quota-filling—not the natural redundancy of language.

| Symptom | Correction |
|---|---|
| Even non-peak narrative sentences are reduced to the shortest possible form | Keep emphatic action, emotional, and suspense sentences short. Write setup, transitions, and ordinary actions in natural language, preserving necessary structural words |
| High-density micro-actions such as slight tugs, brief pauses, repeated pats, or half-turns, reported by `micro-action-tic` | Combine actions and use specific details. Not every action needs a reaction appended |
| Emphatic adverbs equivalent to “even,” “only then,” “again,” “only,” “all,” and “instead” have been stripped away | Test meaning before deletion. Retain words that convey characterization, contrast, or irony. Removing “only” from “only twenty-three days” reverses the emphasis |
| Dialogue particles disappear entirely | Retain a natural, low-frequency set appropriate to the character. Do not add them excessively; human presence comes from natural structure, not chatty style |
| Formal or archaic narrative residue | Replace rigid equivalents of “must not,” “must,” “not yet,” “already,” and “currently” with ordinary language. System notices, rules, and panels may retain functional rigidity. If `system-notice-formality-tic` fires, simplify only part of the language within the original medium rather than converting it into narrator explanation |
| Clusters of short narrative paragraphs in a long text, reported by `overcompressed-prose-tic` | Do not lengthen every short paragraph. Read manually: preserve emphatic short lines and dense shots when context flows. Only repair outline-like transitions by recombining them into the same shot so readers can follow action, space, and causality |
| Low connective density in narration outside quotation marks, combined with few medium or long sentences, reported by `low-connective-density-tic` | Do not globally add function words or alter naturally terse dialogue, comments, or system messages. Find breaks where narration resembles an outline and restore necessary connections, references, and longer linking sentences. Preserve low-function-word prose when it already contains coherent longer sentence chains |

Self-check: Read the result continuously. If it resembles an outline or a stream of commands, too much was deleted. Restore non-peak sentences to natural language instead of continuing to cut.

This pattern controls the degree of deletion; it does not weaken the cleanup. Continue to apply Patterns 1–8 and Gates A–G fully. Restore only structural words and connections, never prohibited or formulaic language.

### Pattern 10: False Naturalness After Revision—Awkward Inversion, Surveillance-Camera Action Lists, and Metric-Driven Dialogue

Some “anti-detection prompts” push prose into another template: arbitrary inversion to increase surprise, mechanical mistakes and profanity to seem human, forced line breaks for mobile reading, or converting thought and narration into speech to increase dialogue share. These are signs of a second-pass revision, not natural web fiction.

| Symptom | Correction |
|---|---|
| Awkward inversion | Do not front-load accompanying actions in constructions equivalent to “A knife in his hand, he charged.” When the same subject continues, vary sentence openings naturally through an in-scene object, sound, body part, or environmental response. Do not overuse personification of inanimate objects |
| Surveillance-camera action lists | Consecutive actions such as reaching, picking up, taking, lifting, setting down, and turning resemble instructions. Combine trivial movements and retain only actions with emotional, plot, or spatial function. When necessary, use hesitation, error, another character’s response, or environmental feedback as a transition |
| Excessive dehydration in high-pressure scenes | Conflict, pursuit, and combat may remove explanation and connective logic. Daily life, romantic ambiguity, and setup cannot be stripped throughout. Remove waste, not natural connective words |
| Missing words | If cleanup leaves a verb without an object, an unclear target, or uncertainty about who acted on whom, restore the necessary object, carrier, or physical feedback. Chinese permits omission, but not until prose resembles an outline |
| Metric-driven dialogue | Do not expand dialogue merely to achieve a 50–60% share. Add speech only when the character would genuinely speak and must speak now. Break long dialogue with action; compress expository dialogue into conflict, avoidance, or partial information |
| Formatting tricks | Do not force a line break after every sentence, enforce 50–60 characters per line, replace ellipses with English periods, or deliberately misuse `地/得`. Follow the project’s and platform’s existing format |

The `action-list-tic` rule in `check-ai-patterns.js` only identifies possible surveillance-camera action lists and is not blocking. Functional combat, pursuit, or ritual procedures may remain when the action chain itself conveys information, or may be marked `[需复核]`. The highly rated Tomato Novel sample had no matches of this kind, so the warning is useful as a prompt to reread rather than an automatic failure.

#### Handling Tool Prompts

`check-ai-patterns.js` is a local writing linter. Only deterministic sentence-pattern and punctuation problems are blocking; advisories do not prevent completion. When users paste reports from other tools, convert only issues grounded in the manuscript’s sentences, paragraphs, or vocabulary into specific changes. Do not claim “0% AI,” “100% human,” or a fixed formula, and do not repeatedly optimize around a score.

Tool prompts do not outrank reading quality. If a reference contains high-risk equivalents of “as if,” “very,” or “felt,” or tells psychology directly, clean it under Patterns 1–8. Do not mechanically add words, introduce deliberate errors, or apply one genre’s shell.

**Additional AI-cleanup judgments**:

- Prioritize authorial explanation, summary, significance tails, and sentences that translate events into “he realized,” “this meant,” “what really mattered,” or “this growth.” Delete them first or return them to in-scene actions, dialogue, object state, task state, and immediate consequences.
- Prefer in-scene media. Preserve phones, screens, announcements, signs, forms, bills, evidence, or rule lines as text or objects the character sees, misreads, or handles. Do not restate the same information through narrator explanation.
- Use plain language without padding. Do not repeatedly replace plot progression with polished reaction phrases such as scalp tightening, eyelids twitching, heart sinking, or stomach churning. Use ordinary actions and sensations when possible while preserving natural connective words.
- Prioritize genre-specific style. Style matching can help, but it must come from the target genre or the current book’s style fingerprint. Do not treat the voice of *Coiling Dragon*, older web fiction, or first-person narration as a universal solution.
- Do not treat adding headings, objects, action tails, longer or shorter sentences, queues, access controls, or record-like prose as universal corrections. None replaces diagnosis of the actual plot, viewpoint, and language problem.

#### Turning Outline-Like Sentences into Continuous Paragraphs

When no blocking issue or obvious advisory remains but the prose still resembles an outline, repair only the breaks:

1. Mark paragraphs that read like logical reports—chains such as “he knew,” “he understood,” “this meant,” “the real problem,” “must,” or “needed”—without immediate action, objects, or dialogue feedback.
2. Ground narrator conclusions. Replace “he realized” or “this meant” with a consequence the character can touch, hear, or must address. Do not apply a fixed object checklist or universal scene shell.
3. Restore natural connections and structural words only at the breaks. Do not set a numerical target or add connections mechanically.
4. System notices, rules, and panels may remain cold and terse. When `system-notice-formality-tic` fires, simplify some rigid language only within the original medium or let the character see an immediate consequence; do not turn it into narrator explanation.

Specific corrections for `overcompressed-prose-tic` and `low-connective-density-tic`:

1. Circle consecutive short narrative paragraphs and label their functions. Explosive moments, reversals, emphatic fear, and dense shots may remain short. Setup, space, causality, and action transitions should return to the same shot. If manual reading flows, do not lengthen solely because of the advisory.
2. When combining, restore action order, spatial position, and causal transitions rather than inserting a structural word into every sentence.
3. After combining, remove clichés and told psychology again. Restoring flow must not restore AI-like writing or add clusters of “as if,” “felt,” “very,” or “seemed.”

If the reading still feels unstable after clearing `overcompressed-prose-tic` and `low-connective-density-tic`, stop making local adjustments and switch to paragraph-level rewriting or comparison with a human-edited reference.

Example:

```
过度压缩：
林遥抬头。
雨棚外的街灯灭了。
风也停了。
柜台上的纸杯晃了两下。

读顺后：
林遥抬头时，雨棚外的街灯正一盏盏熄下去。风忽然停了，柜台上的纸杯还在原地轻轻打转。
```

<!-- translation-companion: non-executable -->
```text
Overcompressed:
Lin Yao looked up.
The streetlight beyond the awning went out.
The wind stopped too.
The paper cup on the counter wobbled twice.

Restored:
When Lin Yao looked up, the streetlights beyond the awning were going out one by one. The wind suddenly stopped, but the paper cup on the counter continued to turn slowly in place.
```

---

## Systematic Three-Pass AI Cleanup

### Pass 1: Strip Generic Language

- Abstract emotional summaries → delete or replace with concrete action
- False profundity → delete
- Inflated significance → reduce to a specific effect
- Empty conclusions → delete
- Perfectly balanced contrasts → break and rewrite
- Decorative adjective piles → use plain description
- Excessive equivalents of “then,” “however,” and “at this moment” → delete half
- Every character speaks with the same polished voice → differentiate their speech

**Principle**: Delete when possible; otherwise replace with concrete details. This pass removes 80% of the AI feel.

### Pass 2: Cut Professional Diction

- Analytical terms such as “mechanism,” “structure,” “logic,” and “system” in fiction → use everyday language
- Excessive abstract nouns → state what happens directly
- Bureaucratic equivalents of “further,” “deepen,” “advance,” and “implement” → delete
- Stacks of technical terms → retain only what is necessary and explain it plainly

**Exceptions**: Scenes that intentionally require professional language, such as formal historical diction, deliberately dense literary fiction, or exaggerated comic rhetoric.

### Pass 3: Restore Natural Presence

- Add concrete sensory detail: smell, temperature, and texture.
- Distinguish how characters speak.
- Vary sentence openings when three or more consecutive sentences begin with the same subject or part of speech. Use an action, scene element, or dialogue entrance.
- Vary rhythm through long and short sentences according to emotional beats, action progression, and dramatic units. Do not create strings of equal-length paragraphs or fragment prose merely to make it short. Length variation is not random: reflection may slow; conflict and reversals may become abruptly brief; complete reasoning and emotional chains remain coherent.
- Give dialogue a sense of social position: a superior and subordinate should not speak alike.
- Add a memorable detail specific to the scene.
- Preserve project-specific language habits, including character catchphrases.

**Principle**: Less is more. One or two concrete details per paragraph are enough.

### Escalation Strategy

| Degree of AI Feel | Strategy |
|----------|------|
| Mild | Pass 1 only |
| Moderate | Pass 1 + Pass 2 |
| Severe | All three passes + paragraph-level rewriting of key sections |

### Self-Check

- Does dialogue use conversational language and avoid formal diction?
- Would deleting a sentence affect understanding? If not, it may be unnecessary.
- Can characters be distinguished through dialogue alone?
- Does the scene contain at least one detail unique to it?

---

## Additional AI-Cleanup Techniques

### Show vs. Tell

| Type of Telling | AI Approach | Natural Approach |
|----------|--------|----------|
| Telling anticipation | “He was excited” | Show the chain of expectation → emotion → satisfaction |
| Telling a character’s goal | “She wanted a divorce” | Show the goal through action |
| Telling a character’s attitude | “She was calm” | Reveal it through dialogue and response |
| Telling the plot direction | “Something major was about to happen” | Show setup → reversal → continuation |

### Integrating Internal Thought Naturally

- Parenthetical labels for internal activity break immersion.
- Long internal monologues explaining motivation are an AI signature.
- Direct statements such as “she felt” or “she realized” tell emotion.

**Natural approach**: Integrate thought into narration, imply it through behavior, and express it through silence, action, or behavior that violates expectations.

### Immersion Check

- Can readers understand, relate to, and accept the protagonist’s behavior?
- Is the antagonist strong enough? A weak antagonist makes victory meaningless.
- Does behavior follow characterization, with actions, language, and thought organized around personality?
- Is known information being controlled effectively so information gaps create emotional movement?

---

## Rewrite Examples

### Externalizing Emotion

**Nervousness**

- “He felt a wave of nervousness, and his heart involuntarily began to race.”
- He tightened his grip on the paper cup, spilling some water.

**Anger**

- “Anger burned inside him, and he could not help clenching his fists.”
- He slapped his chopsticks onto the table, splashing soup from the bowl.

**Sadness**

- “A trace of sadness rose inside her, and tears flashed in her eyes.”
- She looked down and stirred her coffee for a long time.

**Fear**

- “Fear enveloped him instantly, and he felt himself tremble.”
- He pressed his back against the wall and did not move.

**Disappointment**

- “She felt a trace of disappointment, as though something had squeezed her heart.”
- “Oh.” She locked her phone.

**Surprise**

- “His pupils contracted slightly. He clearly had not expected to hear that.”
- He opened his mouth but could not speak.

### Scene-Description Examples

**AI-style scene**

- “Sunlight filtered through a gap in the curtains and cast dappled shadows across the floor. A faint floral scent filled the air, as though the whole world were immersed in peace and tranquility.”
- Three in the afternoon. Only the clock moved in the living room.

**AI-style weather**

- “The sky was dark and covered with heavy clouds, as though torrential rain might begin at any moment. A bitter wind roared past, carrying a trace of bone-piercing cold.”
- Rain was coming. The wind tossed the clothes hanging outside.

**AI-style combat**

- “His fists struck like a violent storm, each blow containing unquestionable power. His opponent’s pupils contracted slightly, clearly unprepared for such a fierce attack.”
- He drove a fist forward. The other man failed to dodge, and the corner of his mouth split.

### Ending-Rewrite Examples

**Elevated ending** → “He stood by the window, looking toward the distant skyline, and finally understood the truth of life: Sometimes letting go is the best choice.” → He put out his cigarette and went inside to sleep.

**Summary ending** → “At that moment, everything changed. She knew her life would open a new page from then on.” → She closed the door. She did not look back.

**Reflective ending** → “The years passed quietly like flowing water...” → Delete the paragraph.

### Rhythm-Adjustment Examples

> These examples remove bloated modification, stacked comparisons, and abstract summaries. They do not mean “split every long sentence.” Revised narration should still favor comma-linked long sentences under Rule 3. Do not break normal long sentences into fragment chains.

**Parallel structure**

- “He looked into her eyes, looked at her lips, looked at her slightly trembling eyelashes, and felt an indescribable emotion rise inside him.”
- He looked at her. She said nothing.

**Removing decoration from a bloated sentence**

- “When he finally pushed open the heavy wooden door, what came into view was a dark room. The air was filled with an aged smell, and dusty boxes were piled in the corner.”
- He pushed open the wooden door. The room was dim, and several dusty boxes stood in the corner.

**Breaking artificial symmetry**

- “She loved spring flowers, summer sunshine, autumn leaves, and winter snow. Every season had its own unique beauty.”
- She liked spring. The other seasons were fine.

---

## Conflict-Dialogue Rewrite Examples

### Mild AI-Style Dialogue

- “I don’t think what you’re doing is appropriate. Could you consider my feelings?” → “Do I matter to you at all?”

### Perfect AI-Style Explanation

- “I actually had a reason for doing this, because the situation at the time was extremely complicated...” → “What are you going to do about it?” She set the teacup down hard.

### Five Levels of Escalating Emotional Dialogue

The same conflict, from weak to strong:

1. **Objective statement**: “You threw away my things.”
2. **Statement + request**: “You threw away my things. Could you ask me first next time?”
3. **Subjective accusation**: “What gave you the right to touch my things?”
4. **Accusation + order**: “Who do you think you are, touching my things? Get out.”
5. **Accusation + manipulation**: “I wait on you hand and foot, and you can’t even put one thing away properly. This is all you’ll ever be. Without me, you’re nothing.”

### Layered-Shock Rewrite Example

**Instant AI-style shock**: Everyone was shocked and could not believe their ears.

**Natural layered shock**:

1. The man opposite her jolted, spilling water from his teacup.
2. The people beside him exchanged looks. Someone stepped back, and a person in the corner reached for a phone.
3. The arrogant woman’s smile froze. She opened her mouth but could not produce a word.

### Restoring Agency

**Passive protagonist**: She was terrified and did not know what to do. She could only wait for it to end.

**Active protagonist**: She locked the door, silenced her phone, and started recording.

---

## Quality Checklist

After writing each chapter, scan every item:

- [ ] **Paragraph control**: Paragraphs break at changes in action or information and read smoothly.
- [ ] **No em dashes in body text**: Narration and dialogue contain no `——`, `—`, or `--`. Use periods, commas, short sentences, or actions; dialogue receives no exception.
- [ ] **High-frequency AI-term scan**: No equivalents of “cannot help but,” “as if,” “came into view,” “thought secretly,” “said gravely,” “corner of his mouth rose slightly,” “involuntarily,” or “behold.”
- [ ] **Weakening-adverb count**: No more than three equivalents of “slightly,” “faintly,” “slowly,” and “gently” per 1,000 Chinese characters.
- [ ] **No compulsive sets of three**: No AI-style three-item rhetorical sets.
- [ ] **Balanced negative lists reviewed**: Review every cross-paragraph “not A / nor B / only C” pattern and every other `formulaic-parallelism` advisory, including dialogue. Preserve functional rhetoric.
- [ ] **No academic prose**: No equivalents of “it is not difficult to see,” “this shows that,” “in fact,” or “in conclusion.”
- [ ] **No excessive formal conjunctions**: No repeated equivalents of “thereupon,” “meanwhile,” “thereby,” “consequently,” or “admittedly.”
- [ ] **No summary or elevation at chapter end**: End through action, dialogue, or suspense rather than reflection, philosophy, or announcement.
- [ ] **No long blocks of internal thought**: Internal thought does not exceed two paragraphs and is not labeled in parentheses.
- [ ] **Show emotion through action**: At major emotional beats, do not state anger, sadness, or nervousness directly; use physical response. Transitional low-intensity emotions may be stated briefly.
- [ ] **Conversational dialogue**: No formal tone, and characters have distinguishable voices.
- [ ] **Punctuation retains shape**: Challenges, eruptions, and hesitation have not all been flattened into periods. Question and exclamation marks are functional rather than random, and ellipses or em dashes do not manufacture pauses.
- [ ] **Show, don’t tell**: Replace adjectives with behavior and summaries with detail.
- [ ] **Sentence length passes**: Narration defaults to comma-linked long sentences, with roughly 8–12 Chinese characters between commas and 20–30 per sentence under Rule 3. Short sentences appear only as occasional isolated emphasis before returning to long sentences. There are no chains of five-character-or-shorter fragments and no outline-like telegraphic prose throughout.
- [ ] **Review every detector advisory**: For `micro-action-tic`, `stock-reaction-tic`, `abstract-summary-tic`, `cliche-density-tic`, `metaphor-density-tic`, `reasoning-chain-tic`, `system-notice-formality-tic`, `overcompressed-prose-tic`, `low-connective-density-tic`, and `action-list-tic`, follow the script’s correction guidance. Read first to determine whether the pattern is mechanical; revise only confirmed problems. Preserve functional writing or mark it `[需复核]`. Do not rotate synonyms or add mechanical padding.
- [ ] **No metric gaming**: Do not force a line break after every sentence, enforce 50–60 characters per line or 50–60% dialogue, use English periods as ellipses, or deliberately replace `地/得` with `的`.
- [ ] **Task obstacles respect source boundaries**: Converting an abstract summary into a blocked task requires an existing task, evidence, procedure, or object gap. Do not invent event chains.
- [ ] **Three-pass AI cleanup completed**: Mild cases receive Pass 1, moderate cases Passes 1–2, and severe cases all three passes.
- [ ] **Dialogue naturalness test**: No traces of formal prose.
