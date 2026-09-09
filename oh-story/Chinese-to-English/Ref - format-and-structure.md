# Prose Formatting and Section Structure

> Required reading before writing. The formats below are the repository's default prose-delivery conventions. Explicit user or target-platform requirements override them.
>
> **Scope**: Paragraph formatting—prioritizing dramatic units/shots, using short paragraphs as the base, and reserving long paragraphs for complete reasoning, atmosphere, and emotional chains—and dialogue formatting apply to every form. Section or beat structure applies only to short-form work; there is no universal minimum length per section. Long-form chapters use `visible_chars_v1` to measure the detailed outline's `字数目标` on the same basis: ±12% internally and ±15% for user delivery.

---

## Chapter Markers

Default formats, ordered by flexibility:

| Format | Platform use | Example |
|------|----------|------|
| `###1.` | Short-form default | `###1.` `###2.` `###3.` |
| `###第一章` | Some platforms | `###第一章` `###第二章` |
| `1.` (plain number) | Zhihu | `1.` `2.` `3.` with no `###` prefix |

**Rule**: Use one format consistently throughout. For short-form fiction, prefer `###1.` or plain numbers for simplicity and efficiency.

---

## Paragraph Formatting

### Core Rule: Prioritize Dramatic Units

The default layout breaks paragraphs naturally by **dramatic unit or shot and keeps them tightly spaced**. Never use a fixed character count as a mandatory cutting point. First determine whether one event, reasoning chain, or emotional change is complete.

- Each paragraph carries one dramatic unit: an action chain, clue discovery, viewpoint shift, psychological judgment, or continuous atmospheric/reasoning/emotional chain.
- Start a new paragraph when a scene, event, action, object, information item, or line of dialogue begins. Weave occurrence, perception, and reaction from the same instant together rather than splitting them into separate action/perception/reaction layers.
- Adjacent prose paragraphs allow **exactly one newline `\n`**. Do not insert blank lines or consecutive newlines `\n\n`; keep them tightly packed.
- Do not indent. The platform renderer handles indentation; do not add `　　` or spaces.
- Use length only for diagnosis. Split when a paragraph feels crowded, combines several beats, or becomes difficult to follow on a phone. Preserve a somewhat longer paragraph when a complete chain of reasoning, atmosphere, or emotional development is not finished.

### Paragraph Rhythm: Vary Length and Density

Short paragraphs provide the fast-reading base for mobile web fiction. Long paragraphs carry complete reasoning, atmosphere, and emotional accumulation. **Avoid uniform length throughout**, and do not cut every paragraph at one character threshold:

- **Vary length**: compress climaxes, face-slapping, and reversals into the shortest paragraphs, sometimes a single sentence. Preserve longer paragraphs for reasoning chains, environmental pressure, emotional accumulation, and chapter resolution so readers complete one full change.
- **Vary density and detail**: write payoffs and turning beats densely, with perception, action, and detail. Handle transitional beats lightly in one or two sentences. Giving every beat the same length and detail creates an AI-generated feel.
- **Avoid excessive fragmentation**: if several very short paragraphs belong to one shot or event, merge them into a natural paragraph rather than presenting an outline or poem.

### Rhythm of Subjects and Character Names

Do not omit character names constantly, but do not repeat them in every sentence. Use names for **subject reset**:

- Establish viewpoint with a protagonist or character name at a paragraph opening, scene change, multi-character scene, or moment of possible ambiguity.
- Inside one paragraph or action chain, mix pronouns, connected actions, and reasonable omission instead of beginning every sentence with the same name.
- Repeat the name at a decisive turn, emotional peak, identity contrast, or point where readers need to refocus on the protagonist.
- Review whether subject rhythm causes stumbling rather than applying a fixed whole-chapter count. Name density is excessive only when consecutive sentences or paragraphs repeat a name despite no need to reset the subject.

---

## Dialogue Formatting

### Dialogue Marks

Follow target-platform or user requirements. When unspecified, use the default:

| Priority | Format | Platform |
|--------|------|----------|
| Preferred | `"说话内容"` | Short-form default, Fanqie |
| Platform/project specified | `「说话内容」` | Zhihu Yanyan short fiction, some historical romance, Japanese style, or user request |

Use `""` by default. Switch to `「」` when the user or platform specifies Yanyan style, and never treat `「」` as an error.

### Dialogue Rules

1. Put dialogue **on its own line**, not inside a narrative paragraph.
2. Use dialogue tags only when needed. Replace frequent or formulaic `他说`, `她道`, and `他笑了笑说` with action or context. An occasional ordinary “said” is allowed, consistent with the rule against mechanical tagging among the eight absolute prohibitions.
3. During continuous two-person dialogue, omit tags and distinguish speakers through content.

**Correct example**:

```
她把杯子放下。
"你走吧。"
他没有动。
"我说，你走吧。"
```

**Also valid: infrequent ordinary “said”**:

```
她把杯子放下。
"你走吧。"她说。
他没有动。
"我说，你走吧。"
```

**Incorrect example**:

```
她把杯子放下，说道："你走吧。"他没有动，她又说："我说，你走吧。"
```

---

## Tone and Punctuation Spectrum

Punctuation serves tone, character voice, and emotional rhythm. Do not flatten the entire text into periods or randomly pile up marks for “variety.” Identify the sentence's function before choosing punctuation:

| Tone/function | Strategy | Guardrail |
|---|---|---|
| Pressure/calm/restraint | Short sentences, commas, periods, and when needed a colon that lands the judgment | Do not add artificial exclamation points; restraint does not mean every sentence becomes a flat period |
| Questioning/testing/rhetorical challenge | Question mark + brief follow-up fragments with action pauses | Avoid ending every sentence with `？` |
| Surprise/eruption/face-slapping | One exclamation point at a genuine peak; no more than one or two across a continuous eruption | No `!!!` or entire paragraphs of shouted exclamations |
| Hesitation/swallowing words/unfinished speech | Commas, periods, short breaks, and action beats | Do not use `……` for pauses; prefer action and sentence-length changes |
| Interruption/drawn-out sound | Do not use `——`; interrupt with action, a line break, a short sentence, or an unfinished action | `——` / `—` / `--` are prohibited in narration and dialogue |
| Information reveal/judgment landing | Colon, semicolon, or a single-sentence paragraph | Keep it mobile-friendly; avoid academic chains of semicolons |

Operating rules:

- In dialogue, first assess relationship and power. A dominant character often closes with short statements; a testing character uses more questions and fragments; a character in collapse may use a small number of exclamations or omissions.
- In narration, create rhythm through sentence length, comma pauses, and single-sentence paragraphs. Never use dashes as a pacing tool, including in dialogue.
- During revision, check for two problems: **periods throughout**, which flatten every voice, and **random punctuation piles**, where questions or exclamations have no emotional function or ellipses/dashes manufacture pauses.
- Follow project/platform quotation style. Zhihu Yanyan's `「」` is valid; never change it when `quote-mode keep` applies.

---

## Section or Beat Structure

### Basic Rules

- Divide sections with numbers `1` `2` `3`; each section is a complete narrative beat.
- Length follows narrative responsibility, with no universal minimum. Control the whole work to the locked delivery range; for long-form chapters use the detailed outline's `字数目标`.
- Let plot stage and transition needs determine section count. Do not split a complete action chain merely to equalize word counts or force beats with different responsibilities together.
- Advance one clear plot point per section.

### Internal Structure

Every section must complete Item 1; use the others only when the beat requires them:

1. **One primary event** + **one or more genuine advances**: change at least one of risk, information, relationship, resources, decision, action, or reader understanding. One action chain or exchange may fulfill related points simultaneously; never add obstacles, dialogue, or conflict just to increase the count.
2. **Emotional or pressure landing**: when a change genuinely occurs, clarify how reader experience changes. Do not force an emotional turn onto a task, reasoning, craft, or waiting chain.
3. **Change in reader model or next step**: new information, revised meaning of old information, decision, action, or consequence all qualify; do not force a new fact.
4. **Functional dialogue**: when needed, it changes information, strategy, power, relationship, or next action. Solitary discovery, evidence verification, waiting, and craft scenes may contain no dialogue.
5. **Weave information dimensions into progression as needed**: occurrence is the spine; include perception and reaction in the same shot only when they provide new information. See the scene-writing guidance in writing-craft.md.

### Connections Between Sections

- End each section with a hook: suspense, unresolved emotion, or a new question.
- Continue quickly at the next opening without repeating setup.
- Escalate emotion across sections: each section's intensity ≥ the previous. Exception: after a peak, such as a reversal section, intensity may hold steady for one section but may not collapse abruptly.

---

## Platform Dialogue Overrides

| Platform | Chapter marker | Dialogue format | Special requirement |
|------|----------|----------|----------|
| Zhihu Yanyan | `1.` | `「」` | Mark the introduction separately |
| Fanqie | `###第一章` | `""` | Opening paragraph must attract attention |
| Hongguo | `###1.` | `""` | None |

**General rule**: When the user does not name a platform, default to the general short-form format `###1.` + `""`. When Yanyan style is specified, `「」` is allowed.

---

## Eight Absolute Prohibitions

Apply throughout writing regardless of genre or style:

1. **No mechanical character-count paragraphing**: never split solely because a paragraph exceeds a threshold. Decide whether it remains one dramatic unit. Split only when it combines multiple actions, information items, or viewpoint shifts. Preserve somewhat longer paragraphs for complete reasoning, atmosphere, or emotional chains.
2. **No blank lines between prose paragraphs**: adjacent paragraphs use exactly one newline `\n`, never blank lines or consecutive `\n\n`.
3. **Avoid mechanical dialogue tags**: replace frequent or formulaic `他说`, `她道`, and `他笑了笑说` with action or context; ordinary “said” may remain.
4. **No indentation**: do not use `　　` or half-width spaces for indentation.
5. **No Markdown rendering in prose paragraphs**: outside the standardized section/chapter marker such as `###1.`, do not use bold `**`, italics `*`, headings `#`, dividers `---`, or other Markdown syntax in prose.
6. **No dashes in prose**: narration, dialogue, and interiority must not use `——`/`—` or `--`. Replace them with periods, commas, line breaks, action beats, or short sentences. There is no dialogue exception.
7. **No periods throughout or random punctuation piles**: punctuation must match tone, voice, and emotional function. Use questions for interrogation and limited exclamation for real eruptions. Express hesitation, swallowed words, and unfinished speech through action or sentence-length changes, not `……` or `——`. Do not scatter `？` or `！` without function.
8. **No chapter metadata inside prose**: chapter numbers may appear only in titles, section markers, filenames, or tracking records. Narration, dialogue, and interiority must not contain engineering terms matched by `第[一二三四五六七八九十百千万两0-9]+章|上一章|上章|前一章|本章|这一章|前文|后文|伏笔|细纲|读者`. Replace them with events the character can perceive or relative time. For example, replace “比第一章那三秒开火更疼” with “比那三秒开火更疼.” Exception: preserve the terms when a character genuinely reads or discusses a “Chapter X” text inside the story world or truly is an author/reader discussing reader identity.
