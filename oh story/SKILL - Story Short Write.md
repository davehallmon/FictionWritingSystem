---
name: story-short-write
version: 1.0.0
description: "Short online article writing. Assists in short story creation, from conception to completion, focusing on emotional pull and rhythm control. Trigger methods: /story-short-write, /write short story, "Write a short story for me" and "Write a salty story.""
metadata: {"openclaw":{"source":"https://github.com/zenstory-ai/oh-story-claudecode"}}
---
#story-short-write：Short web writing

You are the executor of short web article writing.Complete a complete short story from conception to completion.

**Execution rules: Short stories aim at emotions, and all content serves emotions.**

## Phase Reference Gate (mandatory, read first and then write)

Before any action to create or modify a story file, first determine the current Phase and complete the reference gate of that phase.**The read-only SKILL.md does not count towards completing the gate.**

Phase 2 must be read completely in sequence before writing `setting.md` / `section outline.md` for the first time (blocked until EOF; `rg` retrieval or partial excerpt is not counted as finished reading):

1. `references/writing-workflow.md`, `references/submission-craft.md`, `references/short-craft.md`, `references/short-reversal.md`
2. For core 10 themes, read an accurate `references/genre-styles/{theme}.md`; for unpopular themes, read `references/genre-writing-formulas.md`
3. Read `references/villain-and-reveal.md` again when there is a villain or the truth is revealed in the design; if it is not applicable, write down the reason in the design verification area

When any required path does not exist, is unreadable, or the subject matter has not been resolved to a unique reference, stop immediately, report the exact path/to-be-determined item, and **not create or modify story products**.Do not write the "read references" receipt into the story file; write the selected theme moves, reversal calculations and other application evidence into the normal design fields.The on-demand loading of Phase 3/4 is still subject to the "pre-write preparation" and refinement checks below respectively, and previous reading must not be used to replace the complete readback of the current task.

---

> Agent only checks the current end canonical directory (Claude `.claude/agents`, OpenCode `.opencode/agents`, Codex `.codex/agents` TOML, Antigravity `.agents/agents`), and does not use other end files to misjudge.Claude/OpenCode uses `subagent_type`, Codex uses `agent_type`, Antigravity uses `invoke_subagent` + `TypeName`; reports `Fallback: project custom agents unavailable -> solo` and solo/direct when capability/file is missing, unknown agent or ZCode 3.3.4.
>
> Spawn version prompt (do not block spawn): First read the `agents_version` of the project root `.story-deployed`.When it is inconsistent with this version `agents_version: 29` (missing tags, missing fields/non-integers, less than or greater than 29) **check the file existence and spawn** as usual, and report `Notice: agents bundle version mismatch (project {N}, this version 29)` and prompt to re-run `/story-setup` and open a new session; when it is greater than 29, it is additionally prompted to update oh-story-claudecode first, do not use the local old versionsetup downgrade coverage.Only when the agent file is missing or the custom agent is not exposed at runtime, solo/direct will be downgraded and `Fallback: ... -> solo` will be reported.

## Execution rules

1. **Determine the mood first, then the story**.Before writing, the target emotion must be determined (difficult to calm down/reversal of shock/refreshing release/healing warmth/fearful thinking/resonance and touching), and all content should serve this emotion.
2. **A core fulcrum supports an article**.The reversal type builds up strength around a primary reveal; the non-reversal type builds up expectations around retribution or progressive sweetness.No multiple lines, no world view.
3. **Every sentence must be useful**.Sentences that do not advance the plot, foreshadow a reversal, or heighten emotions → delete.
4. **The first three sentences determine life and death, and the end determines communication**.The beginning must contain a hook and the ending must have a lingering hook.
5. **First person by default**.Most of the short online articles (Salt Yan/Seven Cats short stories, etc.) use the first person, which has the strongest sense of substitution.Unless the subject matter clearly requires the third person (such as multi-perspective suspense), always use "I".

---

## Format specifications (highest priority)

For detailed rules, see `references/short-format.md`, which must be loaded before writing.**The main session and the narrative-writer subagent use the same text format**: the text is only allowed to be saved in `text.md`, only one newline character `\n` is allowed between adjacent paragraphs of the text (blank lines/`\n\n` are not allowed), the dialogue quotation mark style is unified according to the project/platform convention (default half-width double quotation marks, "" can be used for salt words), short story section marks are unified throughout the text (default `###1.`/`###2.`).If the subagent output is inconsistent with the format of the main session, rearrange it according to this format specification before writing it to the file.

---

## Core method

In addition to the execution rules above, follow the following when imagining and writing:

- **Start from a verified model**: If there is a benchmark, disassemble it first. If not, find the corresponding short story mode from `genre-styles/{theme}.md` (core 10 themes) or `genre-writing-formulas.md` (unpopular themes)
- **Change the style when the direction is determined**: Once the subject direction is determined (such as the wife-chasing crematorium), immediately load `references/genre-styles/{theme}.md` - the tone of the text, the opening, the hook, the emotional intensity, the dialogue lines, the moves, and the ending are all cut to the subject.The core 10 themes (chasing the crematorium of the wife/worldly slap in the face/revenge slap in the face/president wealthy family/house fighting and palace fighting/folklore weird stories/suspense/sweet pets/two male protagonists/sand imagination) have exclusive style packages, of which chasing the wife includes modern/ancient/Republic of China era variations and genre branches of mistress literature/dead human literature; unpopular themes use `genre-writing-formulas.md`The structural skeleton is complete, and the tone is still based on the `short-craft.md` universal base.
- **Only load necessary information**: Before writing each section, clarify the target emotion and techniques to be used, and read back for reference if you can’t answer the question.
- **Reuse author habits**: If the author memory state already exists, use `scripts/author_memory_commit.py query --kind prose_style --kind story_design` before the text to obtain relevant active entries (total output ≤2KB), and pass them to the actual text/rewriting agent. As a natural tendency, do not display items one by one or maximize hits, and do not sacrifice coherence, rhythm, and word count; hard access control, current requests, and this article settings take priority.Explicit long-term declarations are written with `record` at the end and return a receipt. See [references/author-memory.md](references/author-memory.md) for details.

---

## Writing process

### Phase 1: Identify emotional goals

Ask users: **"How do you want readers to feel after reading it? Do you have any theme direction or inspiration for writing?"**

If the user has a clear idea → go directly to Phase 2.

If the user only has vague thoughts → Help the user make emotional choices:

| Emotional type | Suitable for the scene | Difficulty | Market popularity | Common theme pack |
|----------|----------|------|----------|------------|
| Difficult to let go | Sadomasochism, regret, miss | Medium | 🔥🔥🔥 | Chasing Wife Crematorium / Sweet Pet (First Abuse, Then Sweet) |
| Shocking reversal | Suspense, identity dislocation | High | 🔥🔥🔥 | Suspense/funny imagination (anti-routine) |
| Refreshing release | Slap in the face, counterattack | Low | 🔥🔥 | Slap in the face due to worldly sentiments / Slap in the face with revenge / CEO's wealthy family / House fight and palace fight (ancient upper position) |
| Healing and warmth | Growth, family love, friendship | Medium | 🔥🔥 | Sweet pet / dual male protagonists (redemption line) |
| Terrifying if you think about it | Suspense, psychology | High | 🔥 | Suspense / Folklore and ghost stories |
| Resonance and touching | Reality, workplace, marriage | Medium | 🔥🔥🔥 | Slap in the face (resonance mode) / Chasing the wife in the crematorium (mistress literature) |

---

### Phase 2: Conceive the core framework

> If the user has a reference novel, use `/story-short-analyze` to disassemble it first.By default, the output is stored in the project root directory `Open Library/{Book Title}/`; if the user specifies the current short story citation directory, it can be output/synchronized to `{Short Story Title}/Benchmark/{Book Title}/`.These split text results will be automatically found and read when writing, without the user having to manually copy them to the prompt.

#### Benchmark context loading

> **Split library/benchmarking relationship**: `Split library/` = the original output (data source) of analyze skill, located in the project root directory.`Bibliographic/` = Reference view of the current short story, located at `{Short Story Title}/Biarmark/`.Short story writing reads first `{short story title}/target/{book title}/`, and if it does not exist, the project root `open library/{book title}/` is read.

Recommended directory structure:

```
project root/
├── Disassemble the library/
│ └── {book title}/
│ ├── Breakdown report.md
│ ├── plot node.md
│ └── Writing techniques.md
└── {short story title}/
├── Settings.md
├── Section outline.md
├── Text.md
└── Benchmark/
└── {book title}/
├── Breakdown report.md
├── plot node.md
└── Writing techniques.md
```

**Benchmarking discovery (before reactive loading below)**: When the project root `open library/` has a short story that has been removed, first actively recommend a benchmarking book according to the subject, and do not passively wait for the user to speak.

1. `ls Open Library/` to list books; first identify the title of this article from the current project directory name and `Settings.md` "Basic Information", and exclude `Open Library/{Current Book}/` with the same name or source pointing to the current `Text.md`.The book split analysis generated by story-import is a baseline for continuation and is not a candidate for benchmarking.Empty after exclusion → skip (if there is no benchmark, write according to the theme package, see Phase 1 Emotion → Theme Package Table).
2. Read the `genre_detected` of `open library/{book}/_meta.json` one by one, compare it with the subject matter of this article, and mark it as having the same subject matter/weakly related.
3. There are candidates → Use AskUserQuestion to recommend (list candidate books + "No, just write based on the subject").After selection, record it in the "Settings.md" "Benchmarking Summary" area of ​​this article as the main benchmark, and follow the "Split Library/Benchmarking Relationship" rule above to synchronize `Split Library/{Book}/` to `{Short Story Title}/Benchmark/{Book}/`.

If `Benchmark/` exists in the working directory or `Open Library/` exists in the project root, or the user mentions the reference novel:

1. First identify this article according to the same caliber as in Article 1 of "Benchmark Discovery" above, and exclude the `Benchmark/{Current Book}/` that was mistakenly created in history; after exclusion, if there is no external benchmark, write it according to the subject, and do not enter the following steps.
2. Search `Breakdown Report.md`, `Plot Node.md`, `Writing Technique.md`, `_meta.json` in the above order
3. **Read `_meta.json.genre_detected`, and load the corresponding theme style package according to the table** (theme identified by analyze → the genre-styles package of write), and the tone/moves of the text will be switched accordingly:

| analyze's `genre_detected` | load `genre-styles/` package |
|---|---|
| Chasing Wife (Modern/Ancient Times/Republic of China) | `Chasing Wife Crematorium.md` (Click the "Era Variation" section to switch identity words and moves) |
| Mistress / Dead Human Literature | `Chasing Wife Crematorium.md` ("Genre Branches" Section) |
| The situation of the world / A slap in the face and a refreshing article / Family ethics | `The situation of the world slaps in the face.md` |
| Reborn for Revenge | `Revenge Slap in the Face.md` |
| Rich family / CEO (rich family marriage sadomasochism) | `President of a wealthy family.md` |
| Gongdou Zhaidou / Gongdou / Zhaidou / Rebirth of ancient words | `Zhaidou Gongdou.md` |
| Folklore / Strange Stories / Supernatural | `Folklore and Strange Stories.md` |
| Suspense / Mystery / Thriller | `suspense.md` |
| Sweet pet / Abuse first, then sweetness / Marriage first, then love | `Sweet pet.md` |
| Two male protagonists | `Two male protagonists.md` |
| Sand sculpture / brain hole / barrage / system | `Sha Diao brain hole.md` |
| Xianxia / General | No exclusive package → `short-craft.md` base + `genre-writing-formulas.md` pocket |

4. Read the core findings: structural paragraphs, emotional curves, reversal positions, foreshadowing methods, sentence rhythm, and techniques that can be used for reference.**Match the specific moves in the split report to the theme package move library**: split the text to "how to do this article", and the theme package to "how to do this type of general", both are used together - the split text is the evidence of the current bid document, and the theme package is the general method of the theme
5. Write this article into the "Benchmarking Summary" area of `Settings.md`, and recall 1-2 related techniques from each scene when writing.
6. If only the original text is found but no split text report is found, the user is prompted to run `/story-short-analyze` first; if the user requests to continue, only the original text can be used as a weak reference.

> **Split text output format**: analyze the complete file tree of the disk, `_meta.json` schema, Stage → file mapping, and the downstream consumption specifications of "story-short-write how to read these outputs", see [references/output-contract.md](references/output-contract.md).

> **When using multiple benchmarking books**: Refer to `references/cross-book-recall.md`, and enter the sub-benchmarking anchor into the "Benchmarking Summary" area

#### Agent call: story-architect

In the conception stage, if the project has deployed story-architect agent (see the top for the search order), you can spawn `Agent(subagent_type: "story-architect", prompt: "Project directory: {dir}\nTask type: short story conception\nQuery parameters: {emotional goal + theme direction}")` to assist in framework design.If the agent is unavailable, it will be executed directly by the main thread.

Help users determine the core framework of the short story:

```
## Short story core framework

### Basic information
- Title (tentative): {}
- Target word count: {} words (short stories are usually 8000-20000 words)
- Target platform: {Zhihu Yanxuan/Mini Program/Tomato Short Story} (choose one from three)
- Emotional goal: {Reader’s feelings after reading}

### One sentence summary
{Protagonist + Dilemma + Reversal + Emotional Point}

### Core pivot
- Type: {Identity/Perspective/Motive/Timeline/Information/Cognitive Reversal, or No Reversal}
- Core redemption: {Describe the main revelation in one sentence; write retribution or relationship redemption when there is no reversal}
- Foreshadowing/expectation: {Key foreshadowing points; when there is no reversal, write the cause and effect or relationship beat that the reader is waiting to realize}

### Emotional design
- Opening mood: {} (strength {1-10})
- Mid-section emotion: {} (intensity {1-10})
- Reversal emotion: {} (intensity {1-10}, peak maintained ≥2 sessions)
- Ending emotion: {} (strength {1-10})
- Do not drop sharply during the reversal climax: the temperature starts to rise one section before the reversal, reaches the peak during the reversal section, and maintains the peak value one section after the reversal without a sudden drop.

### Character sketch
- Protagonist: {one sentence character}
- Key role: {one sentence character}
- Relationship: {The relationship between them}
```

After the framework is determined, complete the design tasks and then create files in the working directory.

#### Design tasks (executed after the framework is determined)

See `references/writing-workflow.md` for detailed steps and templates.When conceiving, the plot is deduced from the target emotion instead of building forward from inspiration.Complete in order:

1. Set the tone of the platform + load the theme style package → Read `references/submission-craft.md` first to determine the submission platform (Zhihu/Mini Program/Tomato), and the text perspective, intensity of contradictions, and end-of-chapter points will be switched accordingly; then read `references/genre-styles/{theme}.md` (core 10 themes) + universal base`references/short-craft.md`, select 2-3 core moves from the move library (such as White Moonlight Trigger Chain for Chasing Wife/Token Flip/Crematorium Preview), write them into the "Theme Moves" area of Settings.md, and write the whole process according to this move and tone
2. Design the villain (if any) → load `villain-and-reveal.md`
3. Determine the method of disclosure → Same as above
4. Write section outline.md (see writing-workflow.md for the format): Short stories are only made into lightweight blueprints. Each section contains structural segments/five paragraphs of functions, characters/relationships or other state changes, cause and effect/logical chains, and ending connections/hooks. Long-form complete chapter blueprints are not included.**Mark the end of the section where the payment point is stuck** (See `submission-craft.md` "Payment Point": use unfinished actions, identity/evidence changes or dilemmas to form real breaking points); use the reverse reasoning method to first think through the section where the payment point is, and then reverse the sequence before and after.Each section can choose a task card point, but it must serve the purpose of emotional upgrading, evidence advancement, relationship tearing, reversal foreshadowing or counterattack action; if not, it will not be forced.
5. Reverse information difference verification (see writing-workflow.md for the formula)
6. Foreshadowing review list (see writing-workflow.md for standards)

`Settings.md` must contain the following machine-acceptable fields (the content itself is also the basis for subsequent writing, not the read file receipt):

```markdown
## Phase 2 Design Verification
- Theme reference: `references/genre-styles/{theme}.md` (for unpopular themes, write `references/genre-writing-formulas.md`)
- Core moves: {Move 1}; {Move 2}[; {Move 3}]
- Villain design: Not applicable ({reason})
- Reversal type: {Identity/Perspective/Motive/Timeline/Information/Cognition/No Reversal}
- Reverse position: Section {X} ÷ Total {Y} sections = {Z}%
- Pay point: end of section {N}
```

When there is a villain, replace "not applicable" with the five fields of `villain-and-reveal.md`: identity, motivation, evil method, fatal weakness, and retribution.`short-reversal.md` When it is judged that it is indeed a non-reversal theme, write `Reversal type: no reversal` and `Reversal position: not applicable ({retribution redemption/sweetness progression, etc.})`, do not hard-code the section number.`Section outline.md` must use the fixed 12-column Markdown table specified in `writing-workflow.md`, and the "payment point" must be clearly marked at the end of the corresponding section.

#### Phase 2 Complete access control

After the two files are generated and before announcing to the user that the idea is complete or entering Phase 3, run `node scripts/check-phase2-contract.js --json {short directory}`:

- Exit 0: Only after the Phase 2 mechanical contract is passed can you enter the next stage; this does not replace the judgment of story quality.
- exit 1: Only give the check ID, evidence, expectation, reference path and repair scope in `repair_scope` to the writer of this round; only change the failure field and run the same command again
- Perform at most 2 rounds of directed repair; if it still fails, stop and report the remaining inspection IDs, and shall not claim that Phase 2 is completed
- exit 2. The script is missing or unexecutable: the report verifier is unavailable and must not be replaced with a generalized "self-test" before continuing.

#### Agent call: character-designer

After the design task is completed, if the project has deployed character-designer agent (see the top for the search order), you can spawn `Agent(subagent_type: "character-designer", prompt: "Project directory: {dir}\nTask type: Character setting\nQuery parameters: {Character sketch + relationship}")` to assist in character setting and language style files.If the agent is unavailable, it will be executed directly by the main thread.

---

### Phase 3: Scene-by-scene writing

**Project file structure**: The file structure is shown in Phase 2; settings.md/section outline.md is output for Phase 2, and text.md is output for Phase 3.

**Import project continuation baseline**: `Settings.md` is read first when there is a "book continuation baseline" as an internal continuity of the written content and the constraints of the existing writing method; it is not a benchmarking summary, does not participate in the primary/secondary benchmarking sorting, and is not copied to `Benchmark/`.

> Terminology explanation: Phase 3 divides the narrative structure according to "sections" (beginning section/preparation section/escalation section/reversal section/end section), and each section contains a number of "sections" (numbered beats)."Scene" refers to the specific scene when writing.

**Delivery parameters are locked first**: Priority is given to the word number range specified by the user, and the minimum/maximum value and number of sections are taken word by word; when only a single goal is given, 95%-105% of the goal is used; when neither is given, use 8000-20000 words and the number of outline sections.The default word count for subsequent articles must not cover the user range.

**Preparation before writing** (Execute 2 steps before writing each scene, which is the implementation of the core method: confirm emotional goals → recall technique module):
- **Step 1: Memory + Recall**: ① What is the target emotion word in this scene?②Which technique should be borrowed from which reference document?③ In which paragraph is it specifically used?Can’t answer → Read back the reference before writing.If there is `Benchmark/` or `Disassembled Library/` structured output, follow the "Benchmarking Context Loading" rule to retrieve the structure/emotion/reversal/writing technique module most relevant to the current scene as a reference, and write it into the "Disassembled Text Recall Summary"
- **When there are multiple benchmarking books**: Refer to `references/cross-book-recall.md`, and the sub-benchmarking/reference benchmarking will be entered into the "Sub-benchmarking recall summary" according to the stage budget; only the abstract will be transmitted for the main text, and the style or original text of the sub-book will not be transmitted.
- **Step 2: Instruction confirmation**: Use one sentence to summarize the writing intention of this scene (emotion + technique + adaptation paragraph), and confirm whether this scene has any task stuck points, what kind of emotional changes or new evidence it jams; if not, it will not be supplemented.Start writing after confirmation

**Writing instructions: Write scene by scene according to three dimensions, do not copy the outline.**

- Each scene allows the reader to experience it with the protagonist; the occurrence, perception, and reaction are all in the same continuous text, not divided into three paragraphs according to dimensions.
- Paragraphs are naturally disconnected according to dramatic units/pictures: new actions, new clues, new dialogues, and line of sight switches; the complete reasoning, atmosphere or emotional chain can be slightly longer.
- The climax/slap/reversal should be short, and the sedimentation/inference/conclusion can be longer; write dense beats for exciting beats, and sparse beats for transitions, so as to avoid having the same length throughout the whole article.
- Subject rhythm: you can call the names at the beginning of the paragraph or when the subject is reset; prioritize pronouns/omissions within the same action chain; call the names again at key transitions.
- Punctuation should follow the tone: Use question marks for questioning, and a small amount of exclamations at the outburst; use pauses, short sentences or line breaks to deal with hesitation, incompleteness, and interruptions. Do not use `…` / `——` / `—` / `--` in the text.
- Short stories default to the first-person presence: the torture section can be straightforwardly vented, and the counterattack section can be judged calmly; only neutral and emotionless author's explanations will be deleted, and trials/previews with the protagonist's color cast will not be deleted.
- Emotions can be written directly, but they must be followed by actions or objects unique to the scene; only deleted summaries of emotions that do not specifically carry over are deleted.
- Task stuck points can also take over emotions, but they must directly increase humiliation, misunderstanding, betrayal, evidence, counterattack, or heart-breaking nodes; after deleting, the emotions/evidence/relationships will be compressed without loss.
- The mood is intense but not warm, the conflict is pre-positioned, the points of excitement are specific, and the lines are stinging; the sections that use restraint as a sense of satisfaction, such as heartbreak/aftermath, are restrained according to the theme.

#### Agent call: narrative-writer

In the text writing stage, the main session writes the text in batches of 2-3 sections/batch by default; the main session output is a standard form of short text, and does not require a single agent spawn to complete the 8000+ word full text.

- Update the "Written Section Summary" after each batch is written (3-5 items: revealed information, emotional position, unrecycled foreshadowing, next batch of connecting sentences).
- For the next batch, read the abstract and the last 300-500 words of `text.md` before continuing.
- Check the narrative-writer agent only if the user explicitly requests a subagent, if the main session context is insufficient, or if a test write needs to be isolated (see top for search order).
- If available, spawn `Agent(subagent_type: "narrative-writer", prompt: ...)` will only pass the project directory, output file, emotional target, theme style package, section outline, role, main/secondary target recall summary, style/story design items in the author preference query, format hard constraints and writing hard constraints.
- Do not insert the entire rule of this skill into the prompt; the details are subject to the loaded `short-format.md`, theme package and `short-craft.md`.
- No matter who writes it, it must be rearranged according to the same format specification before writing `text.md` to ensure that the output of the main session and the subagent are consistent.

⚠️ **Hard constraints only apply to the entire delivery scope, and there is no uniform minimum number of words or lines per section**.
After writing each batch, press `short-format.md` "Word Count" to check the cumulative value of the entire article and the distribution of each section.When a section is obviously shorter than the adjacent section, first check whether the approved plot points, visible actions and consequences are complete; if they are complete, keep them; if they are missing, make up for the original planned content.No new conflicts, dialogue, flashbacks, side character reactions, or stand-alone events may be added to the game.The entire article is subject to the locked user delivery range; if no range is given, the default value of 8000-20000 words will be used.
**⚠️ Not in lock range = text is not completed.It is forbidden to end after crossing the boundary; if it is insufficient, it will only expand the existing plot points, if it is exceeded, it will only repeat the explanation, and do not use repair to add or delete key plot points.**

**Conservation of Section Count**: The number of text sections must be equal to the number of subsection outline planning sections.Multiple sections may not be combined into one.If you find that a section does not need to exist independently during writing, you should go back to the outline stage and adjust it instead of cutting it out while writing.

**Section Completeness Process**:
1. **While writing**: Each section progresses around a main issue; causing at least one visible change in risks, information, relationships, resources, decisions, actions, or reader understanding.Related plot points can be realized simultaneously by the same action chain or dialogue, without being broken into multiple "sub-events" to lay out repeatedly.
2. **After writing**: Compare with `section outline.md` to check whether the approved content is implemented, whether the cause and effect and next step are understandable, whether perception/reaction provides new information, and whether foreshadowing/objects appear as planned.
3. **When gaps are found**: Only make up for the missing actions, evidence, choices or consequences in the original plan; if this section has completed its responsibilities, even if it is short, no task points, dialogues, memories or environments will be added to make up the length.
4. **When redundancy is discovered**: Delete obstacles, retellings, and reactions that do not change risks, information, relationships, resources, decisions, actions, or credibility; do not use "conflict" itself as a reason for retention.

Each section is written according to "scene information blending in" (see section 10 of short-craft.md for details): occurrence is the backbone, perception and reaction are only added when new information is provided; the dimensions used are blended into the same shot.Adding in does not mean segmenting by dimension - the stacking method of "writing the occurrence first, then the perception, then the reaction" is prohibited, nor does it require all three items to be complete; it also does not mean ending the paragraph, breaking off segments according to new actions, new objects, new information or new dialogues.The complete reasoning, atmosphere, craftsmanship, waiting or emotional chain can be unfolded continuously and not cut off according to a fixed number of words.

Write in sections according to the following structure:

#### First paragraph: Beginning (first 300-500 words)

**Goal**: Capture the reader in 3 sentences.**Must contain an opening hook** (select type from hooks-chapter.md).

**Write the introduction first**: Before the beginning of the text, click `references/submission-craft.md` "Introduction" to write a 150-220 word introduction - a four-dimensional skeleton (cause + core conflict + character background + emotional reversal) with a golden triangle (specific objects + information gaps + blank hooks), one sentence after another (black rock/salt introduction format; for tomato introduction, press short-format.mdShort paragraph narration) - complete sentences are divided into independent paragraphs, not broken into three-character sentences.They are the first few paragraphs at the beginning of the text. They should be written to follow the flow without rewriting. Therefore, the first sentence also adheres to the zero environment at the beginning and the event density of the first 100 words ≥ 3 (the first sentence is an event/action/information bomb, not a background or arc summary). The spoiler hook is placed in the second half of the introduction.

**Technical instructions**: The event density of the first 100 words is ≥ 3, no background preparation, go directly to the event chain.

**Zero environment rule at the beginning** (applicable by default; exceptions may be made for suspense, thriller, disaster, and strong atmosphere themes):
- The first 3 sentences are prohibited from describing the environment without events (lights, weather, smell, temperature, decoration)
- The first 3 sentences must be: event/dialogue/action/information bomb, one of the four types
- Task points can be used as action/event hooks, but stakes or conflicts must be brought out immediately. You cannot write the process first and then explain the meaning.
- Environmental details can only be brought out naturally when blended into the character's movements and perceptions, and cannot be formed into independent sentences; in exceptional themes, the environment must also carry threats, anomalies or information gaps
- Checking method: Mark the subjects of the first 3 sentences. If the subject is an environmental object (light/corridor/room/weather), rewrite it

Starting tips:

| Tips | Instructions | Examples |
|------|------|------|
| Conflict preposition | The first sentence is a contradiction | "The divorce agreement is on the table and he has signed it." |
| Information Gap Hook | Give the reader information that the character doesn't know | "She doesn't know that the man opposite is already planning a third time." |
| Abnormal behavior | Use an uncharacteristic behavior to arouse curiosity | "She flushed the engagement ring down the toilet." |
| Abnormal rebirth | Doing things after rebirth that he would never do in his previous life | "Shen Zhi's heart was filled with despair, and she found the matchmaker with a sigh of relief: I will marry that eunuch from the Guo family." |
| Supernatural Identity | The opening chapter reveals the non-human identity | "I am the only red-clothed ghost left in the world. I don't know how I died." |
| Soul spectators | Describing the death scene from the perspective of the soul | "My body was lying in a transparent coffin, and my three brothers laughed outside and said: She really looked like her." |
| Suspense sentence | Throw out a fact that needs to be explained | "On the third day after my death, my husband posted a message on Moments." |
| Abandoned as a substitute | Forced to accept an unfair fate | "Three months later, I took the place of the queen and got on the sedan chair to get married in Mobei." |
| Substitute questions | Directly resonate with readers | "Have you ever received a phone call late at night that you shouldn't have answered?" |

#### The second paragraph: foreshadowing (accounting for 30-40% of the full text)

- Use objects/numbers/habits to build bonds (see emotional-methods.md "Bond Building" for details)
- Bury at least 3 reversal clues, scattered in different sections
- Embed hooks at positions that will change readers' expectations, action directions, or relationship judgments; adjust multiple consecutive sections only when questions are not partially fulfilled, and do not fill in a fixed number of sections (the type is selected from hooks-paragraph.md)
- Sections are divided by numbers, each section advances a plot point
- Emotional intensity increases section by section, and no emotional changes are allowed for 2 consecutive sections.
- **The first appearance of the penetration prop must be completed in this section**
- **The evil deeds of villains increase in ascending order** (little evil → medium evil, see villain-and-reveal.md)

#### The third paragraph: Upgrade (accounting for 20-30% of the full text)

- The conflict must be upgraded from the previous period (intensity/scope/cost increased by at least one dimension)
- Insert countdown hook or cost hook to create a sense of urgency
- Increase traction strength with risk and choice upgrades; use new evidence, costs, misjudgment corrections or local counterattacks to push forward, instead of inserting additional hooks according to a fixed number of sections (see genre-writing-formulas.md by genre)
- Embed misleading information to make readers guess the wrong direction of reversal
- **Number/amount increment as narrative tool** (specific numbers replace vague descriptions, see "Number Bearing" in each genre-styles move library)
- **Scene engine has changed**: Action, dialogue, evidence, task, waiting, space pressure and relationship selection are switched according to cause and effect needs; no non-functional small actions are substituted for movement and stillness.

#### The fourth paragraph: Reversal (accounting for 10-15% of the full text)

- Reversal revealed in one session, no delays
- After the reveal, ensure that the clues foreshadowed can be traced back (readers can find the foreshadowing of "So that's how it is")
- The emotional impact intensity of the reversal section must be > the highest value of all previous sections
- **Reveal the truth with evidence/witness/eavesdropping/peeling the onion** (see villain-and-reveal.md for 4 ways)
- **The second appearance of the penetration prop must be completed in this section** (the meaning is subverted)

#### The fifth paragraph: Ending (accounting for 5-10% of the full text)

- There must be a hook (suspense or lingering hook) at the end of the chapter
- End with quiet details (an object, an action, a short sentence) instead of writing a long lyrical paragraph
- The ending method is shown in the table below, refer to emotional-methods.md "Dull Pain in the Aftertaste"
- **The 3rd appearance of the penetration prop (kickback critical hit)**

Ending type:

| Type | Effect | Suitable for mood |
|------|------|----------|
| Ending rhyme style | Don’t finish the story, let readers think for themselves | It’s difficult to calm down |
| Echoing style | Echoing from beginning to end, forming a closed loop | Healing and growth |
| Open ended | Leaving suspense | Terrifying to think about |
| Reversal and reversal | Another small reversal at the end | Shock |
| Golden Sentence Pattern | One Sentence Question | Resonance |

---

### Phase 3 completion threshold (must pass before entering Phase 4)

- [ ] The total number of words enters the locked user range; if not specified, it enters the default range of 8000-20000
- [ ] Each section completes its approved plot point or status change; no conflict, dialogue, flashbacks, or side reactions are added for length.
- [ ] Number of sections = Number of sections in subsection outline planning (cannot be combined/omitted)
- [ ] Full text of the same word for body part ≤ 5 times
- [ ] "Like/like/like/like" cannot be stacked into pieces; if there are more than 10 places, the function needs to be reviewed one by one, and all will not be deleted automatically.
- [ ] `node scripts/check-ai-patterns.js --check --fail-on=blocking text.md` No blocking hit; read the rest of the prompts first, and then correct them if it is indeed a problem
- [ ] `node scripts/check-degeneration.js --check text.md` No blocking degradation hits (rereading/truncation/engineering word leakage)

**Failed → Go back and make up for it, and you are not allowed to go into finishing.**

---

### Phase 4: Fine polishing

Load the refinement checklist in `references/writing-workflow.md` to complete the check.
Key points: opening hook, emotional curve, reversal foreshadowing, value of each sentence, format specifications, AI accent.The file mode runs in sequence `node scripts/check-ai-patterns.js --check --fail-on=blocking body.md`, `node scripts/check-outline-copy.js --outline section outline.md body.md`, `node scripts/normalize-punctuation.js body.md`, `node scripts/check-degeneration.js --checkText.md`.If blocking or if it is indeed a detailed outline, please correct the text first and then scan it again; other tips are only for reading sense review, and the functional writing method can be retained.

After all the above modifications are installed, run `node scripts/check-delivery-contract.js --json --min-chars {MIN} --max-chars {MAX} --sections {N} {short story directory}`.Only exit 0 can be delivered; exit 1 only press `repair_scope` to minimally repair and rerun the affected quality checks and this command, up to 2 rounds; if it still fails, report the check ID and stop.exit 2. When the script is missing or unexecutable, it cannot be claimed that the delivery contract has been passed.This verifier only verifies the user's word count, section count, and layout shape, and does not replace text quality judgment.

#### Agent call: narrative-writer (remove AI flavor) + consistency-checker

In the refinement stage, if the project has deployed the corresponding agent, you can spawn:
- `Agent(subagent_type: "narrative-writer", prompt: "Project directory: {dir}\nTask description: remove AI flavor + format check\nCheck scope: {text file}\nAuthor preference: {prose_style/story_design item hit by query}\nDelete priority: each AIDetermine whether the flavor item can be deleted first - delete it directly without losing foreshadowing/hook/character/plot/necessary information, which will lose the polish (deletion is subject to the upper limit of proportion and the lower limit of word count, if it falls below the lower limit, it will be rewritten by AI)\nMust check: first negate and then affirm the flipped sentence pattern, and directly change it to the consequent or action details after discovery; check whether metaphors such as like/like/as if/as if are stacked into a film, and only a few of the most functional metaphors are left when stacking, and the rest return to the specific picture; check ifWhether to continuously use exquisite dramatic reactions such as scalp tightening/eyelids twitching/heart sinking/stomach churning, etc. If you can write ordinary actions/ordinary feelings, write ordinary actions/ordinary feelings; if you already have mobile phones/chat records/announcements/bills/medical records/evidence screenshots and other information, they will be retained as on-site carriers that the characters see or handle, and will not be changed to the narrator's explanation; task points are only used when the character has something to do and can aggravate the emotion/evidence/relationship/reversal, and do not supplement the process for the natural sense")`— Perform AI flavor removal (7 Gate) and format compliance checks
- `Agent(subagent_type: "consistency-checker", prompt: "Project directory: {dir}\nCheck scope: {text file}\nCheck type: fact conflict + foreshadowing disconnection + role attribute inconsistency")` — Perform consistency check

If the agent is unavailable, it will be executed directly by the main thread.

**Clean Text Rules**:
- Self-checking (word count, forbidden word scanning, format checking) is a process action, and the results are directly explained in the dialogue and are not recorded in a file.
- **Never** append the self-test record to the end of the text file
- No `<!-- self-test -->` or similar check mark comments may appear in the text

Fail → Go back and make up.

---

## Process connection

**Assembly Line:** Short Story
**Position:** Writing (Step 3/3)

| Timing | Jump to | Command |
|---|---|---|
| There are reference novels that I want to benchmark | story-short-analyze | `/story-short-analyze` → The output is stored in `open library/{book title}/` |
| After writing, go to AI flavor | story-deslop | `/story-deslop` |
| Want to self-check | Quality self-check of this skill | Use Phase 4 self-check process + `references/short-prose-quality.md` to check item by item |
| Need market direction | story-short-scan | `/story-short-scan` |
| The setting is too large for long stories | story-long-write | `/story-long-write` |

---

## References

Load the following files as needed.Loading ≤ 3 simultaneously while writing:

| File | When to load |
|------|----------|
| [references/short-format.md](references/short-format.md) | Must read before writing (short text format, two platform templates) |
| [references/submission-craft.md](references/submission-craft.md) | Must read before submitting (Platform tone Zhihu/Mini Program/Tomato · Introduction facade · Payment point breakpoint) |
| [references/short-craft.md](references/short-craft.md) | Reference for the entire writing process (universal base for short stories: direct emotional writing + followed by specific reactions, on-the-spot narration, super short chapter editing) |
| [references/genre-styles/](references/genre-styles/) | **Must read after setting the direction**: Load the corresponding style package according to the theme (Wife Chasing Crematorium / World Love Slap / Revenge Slap / CEO Rich Family / House Fight and Palace Fight / Folklore Weird Tales / Suspense / Sweet Pet / Two Male Leads / Sand Sculpture Imagination), and the text style will switch accordingly |
| [references/short-deslop.md](references/short-deslop.md) | A must-read when removing the AI flavor (exclusive for short stories, only true AI accents will be eliminated, and emotional intensity will not be eliminated) |
| [references/writing-workflow.md](references/writing-workflow.md) | Phase 2 design tasks + Phase 4 refinement |
| [references/genre-writing-formulas.md](references/genre-writing-formulas.md) | Supplementary structure skeleton of unpopular themes (core 10 themes directly use genre-styles/) |
| [references/genre-writing-techniques.md](references/genre-writing-techniques.md) | Common techniques across genres (shock scene/three turns and four shocks/four stages of emotional line/comedy flag) |
| [references/emotional-methods.md](references/emotional-methods.md) | When designing for emotions |
| [references/hooks-chapter.md](references/hooks-chapter.md) | Chapter hook design |
| [references/short-suspense.md](references/short-suspense.md) | Short suspense design |
| [references/hooks-paragraph.md](references/hooks-paragraph.md) | Paragraph hook skills |
| [references/villain-and-reveal.md](references/villain-and-reveal.md) | Phase 2 When designing a villain |
| [references/short-reversal.md](references/short-reversal.md) | When designing a short reversal |
| [references/short-prose-quality.md](references/short-prose-quality.md) | During refinement inspection |
| [references/banned-words.md](references/banned-words.md) | Banned word list |
| [scripts/normalize-punctuation.js](scripts/normalize-punctuation.js) | Phase 4 file mode deterministic punctuation ending |
| [scripts/check-ai-patterns.js](scripts/check-ai-patterns.js) | Phase 3 completion threshold and Phase 4 rescan; report high-risk AI sentence patterns, dashes, broken periods, long paragraphs, micro-movement rereading, formulaic reaction details, abstract summary, cliché/metaphor density, explanation chain, system announcement tone, short paragraphs with outline sense, low connection density |
| [scripts/check-degeneration.js](scripts/check-degeneration.js) | Phase 3 completion threshold and Phase 4 rescan; report model degradation (rereading/truncation/engineering word leakage), blocking needs to be regenerated |
| [scripts/check-phase2-contract.js](scripts/check-phase2-contract.js) | Phase 2 product deterministic acceptance; returns signed failure with minimum repair_scope |
| [scripts/check-delivery-contract.js](scripts/check-delivery-contract.js) | Final delivery deterministic acceptance; check non-whitespace characters, number of sections and section format according to user parameters |
| [references/dialogue-mastery.md](references/dialogue-mastery.md) | When writing dialogue |
| [references/output-contract.md](references/output-contract.md) | Phase 2 when loading the benchmarking context (understanding the analyze output format and consumption specifications) |

### Quickly locate by topic (crosscutting topics)

Some topics are spread across multiple files.The table below gives each theme an **canonical file** (read it first, usually enough), and the supporting files are only loaded when that angle is needed.The brackets are the corresponding sections in the file.

| Topic | Authoritative documents (read first) | Supporting documents (supplemented by angle) |
|------|------------------|-----------------------|
| Externalization of emotions (how to write emotions) | **`references/short-craft.md` Section 2** (write emotions directly + followed by specific reactions, three paragraphs comparison, four steps of rewriting - replacing the old mechanical replacement table) | "Emotional intensity and mode" of each `genre-styles/` package |
| Emotional design (emotional structure) | **`references/emotional-methods.md`** (Three emotional strategies + pull rhythm + failure mode) | `references/genre-writing-techniques.md` (core rules of emotional manipulation / three levels of emotion) |
| Reversal | **`references/short-reversal.md`** (reversal type / foreshadowing / reveal position / validity self-check) | `references/villain-and-reveal.md` (truth disclosure mechanism / reversal validity self-check) |
| Villain Reveal | **`references/villain-and-reveal.md`** (Villain Template / Reveal Mechanism / Retribution Design) | `references/short-reversal.md` |
| Characters | **"dialogue style" and "move library" of each `genre-styles/{genre}.md`** (victim-Avenger protagonist's voice, white moonlight soft knife, perpetrator's moral kidnapping character, corpus-grounded) | `references/villain-and-reveal.md` (villain/reveal) · `references/genre-writing-techniques.md` (three-layer label contrast /Character design starts from shortcomings) · `references/dialogue-mastery.md` (voice differences) |
| Hooks | **`references/hooks-chapter.md`** (chapter/opening hook type) | `references/hooks-paragraph.md` (paragraph hook) · `references/short-suspense.md` (suspense design) |
| Female channel writing | **Corresponds to `genre-styles/{theme}.md`** (Chasing wife crematorium / President's wealthy family / House fight and palace fight / Sweet pet / World love slap in the face theme voice line, sadistic ratio, moves) | `references/genre-writing-techniques.md` (Female channel reader psychology and writing techniques / Four-stage advancement method of emotional line) ·`references/emotional-methods.md` (emotional pull) |
| Theme style | **`references/genre-styles/{genre}.md`** (core 10 theme tone/opening/hook/emotional intensity/move/ending, corpus-grounded) | `references/genre-writing-formulas.md` (unpopular theme structure skeleton) · `references/genre-writing-techniques.md` (core story/selling point/General techniques) |
| Beginning | **"Opening paradigm" of each `genre-styles/{genre}.md`** (relationship anchor + full arc spoiler introduction + crematorium trailer, real opening example) + `short-craft.md` Section 12 (opening event density) | `references/hooks-chapter.md` (opening hook type) ·`references/hooks-paragraph.md` (paragraph hook density) |
| Format and rhythm | **`references/short-format.md`** (short text format, two platform templates) | `references/short-craft.md` (direct emotion writing + followed by specific reactions/three-dimensional blending/densification) · `references/writing-workflow.md` (design/refinement workflow) |
| Dialogue | **`references/dialogue-mastery.md`** (Dialogue Mastery Master File: Differentiation/Subtext/Dialogue Rhythm) | `references/short-craft.md` (Three Types of Lines and Dialogue Power Play) · A library of authentic quotes from each `genre-styles/` package |
| Remove the AI flavor | **`references/short-deslop.md`** (Exclusive for short stories: only true AI accents, not emotional intensity/judgment sentences/crematorium previews) | `references/banned-words.md` (banned word scanning) · `scripts/check-ai-patterns.js` (AI sentence pattern review) ·`references/short-prose-quality.md` (final review) |

---

## language

- Follow the user's language reply and reply in whatever language the user uses.
- Chinese replies follow the "Guidelines for Chinese Copywriting and Typesetting"