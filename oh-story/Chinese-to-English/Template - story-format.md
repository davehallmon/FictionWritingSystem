---
paths:
  - "**/正文/**"
---

# Story Format Rules

Formatting rules for manuscript files. Load automatically when the user edits a manuscript file directly.

## Absolute Prohibitions

1. **Do not divide text mechanically or use oversized paragraphs throughout:** Start a new paragraph naturally when a dramatic unit, shot, or event ends. Do not force breaks at fixed character counts or pack multiple actions, clues, and shifts in attention into one paragraph. Complete reasoning, sustained atmospheric pressure, and chains of emotional change may use somewhat longer paragraphs.
2. **Do not place blank lines between paragraphs:** Adjacent manuscript paragraphs may contain only one newline character, `\n`; never use blank lines or consecutive newlines, `\n\n`.
3. **Avoid mechanical dialogue tags:** Replace frequent or formulaic tags such as “he said,” “she said,” or “he said with a smile” with actions or contextual cues. Occasional neutral uses of “said” may remain.
4. **Do not pile up long passages of description:** Interweave description with actions or dialogue. Never write more than three consecutive paragraphs of pure description.
5. **Do not leave the established viewpoint:** After selecting first person or limited third person, do not shift into another character's interiority.
6. **Do not overuse explicit subjects:** Within one chain of action, do not repeat the protagonist's name unnecessarily in consecutive sentences or paragraphs. Name the character at the start of a paragraph or when the subject resets; continue with pronouns, actions, or natural omission, and name the character again at a critical turn.

## Formatting Standards

- Put dialogue on its own line and introduce it with a colon or action.
- Divide paragraphs by dramatic unit, shot, emotion, or action.
- Format chapter titles as `## 第X章 章名`, followed by one Markdown blank line.
- Adjacent manuscript paragraphs may contain only one newline character, `\n`; do not use blank lines or `\n\n`.
- Do not place `---`, horizontal rules, or additional blank lines between chapters.

## Examples

### Correct — Natural Breaks by Dramatic Unit
```
沈栀抬手，灵力从指尖涌出。
面前的结界出现一道裂缝，碎纹像蛛网般蔓延开。
她咬紧牙关加大输出，整条手臂开始发颤。
```
Each paragraph carries one action or informational change. Paragraphs advance naturally by dramatic unit, with only one `\n` between them.

### Wrong — Multiple Beats Compressed Into One Paragraph
```
沈栀抬手灵力从指尖涌出面前的结界出现一道裂缝碎纹像蛛网般蔓延开她咬紧牙关加大输出整条手臂开始发颤最后结界轰然碎裂碎片向四周飞溅。
```
This paragraph combines multiple actions, clues, and outcomes, preventing the reader from pausing at critical changes.

### Correct — Action Introduces Dialogue Without “He Said”
```
沈栀将茶杯往桌上一顿。
"你到底想说什么？"
陆衍没接话，只是看着窗外。
```
Action and context introduce the dialogue without frequent formulaic tags.

### Wrong — Dialogue Tags
```
沈栀将茶杯往桌上一顿。
她说道："你到底想说什么？"
陆衍没接话，他轻轻叹道只是看着窗外。
```
Using the formulaic tags “said” and “sighed” together in one paragraph creates clutter; replace them with actions.

### Correct — No Extra Blank Line After a Chapter Title
```
## 第二章 暗流

陆衍推开门时，屋内已经坐了三个人。
沈栀坐在最里面的角落，手里捏着一张纸条。
```
There is only one blank line between the chapter-title `##` and manuscript text, as required for Markdown rendering. There are no blank lines between manuscript paragraphs.

### Wrong — Extra Blank Lines Between Paragraphs
```
## 第二章 暗流


陆衍推开门时，屋内已经坐了三个人。


沈栀坐在最里面的角落，手里捏着一张纸条。
```
Extra blank lines between paragraphs—consecutive newlines, `\n\n`—break the compact rhythm.
