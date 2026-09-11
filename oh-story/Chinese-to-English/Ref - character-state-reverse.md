# Reverse-Inference Rules for Current Core-Character Snapshots (Long-Form Import)

> Used only when `story-import` imports long-form fiction. The output is not an append-only character history; it is the initialization transaction's `character_snapshots`. For every core character, `tracking_commit.py init` generates `追踪/角色状态/{角色名}.md`.

## I. Input Sources

Infer state only from story-decomposition artifacts already written to disk; do not reread `原文/`:

| Input | Purpose |
|---|---|
| `拆文库/{书名}/角色/{角色名}.md` | Identity, abilities, objectives, growth arc, and appearance records |
| `拆文库/{书名}/角色/角色关系.md` | Important relationships through the final complete chapter |
| `拆文库/{书名}/章节/第N章_摘要.md` | Final location, latest state, known information, and unresolved matters |
| `拆文库/{书名}/剧情/*.md` | Faction and identity turns, phase objectives, and long-term conflicts |
| Foreshadowing and timeline candidates in the initialization transaction | Verify unresolved character matters and the boundaries of character knowledge |

## II. Tracked Characters

Create independent snapshots only for the protagonist, antagonist, and central supporting characters. Do not create files for temporary bystanders or characters serving a single function. When the boundary is unclear, prefer not to create one; a later chapter transaction may create the snapshot once the character enters a reusable state.

## III. Reverse-Inference Method

For each core character, use the final complete imported chapter N as the cutoff and determine:

1. `identity`: The identity or occupation actually established through Chapter N, excluding planned future promotions.
2. `location`: The character's last location or a location established before the next chapter begins.
3. `goal`: The specific objective the character is currently pursuing.
4. `state`: Current physical, emotional, reputational, or positional state that affects continuation; include only necessary information.
5. `abilities_resources`: Abilities, objects, permissions, works, or relationships currently and demonstrably possessed, with at most eight entries.
6. `relationships`: Current relationships with characters who will recur, with at most eight entries.
7. `knowledge`: Information the character personally knows and that will affect behavior, with at most eight entries. Do not misclassify author-only truth as character knowledge.
8. `open_threads`: Character-related unresolved matters, with at most eight entries. Each requires evidence in the written manuscript; purely future designs remain in the outline.

When a field changes more than once, retain only its current value through Chapter N instead of placing the change history in the snapshot. Later `逐章记录/第NNN章.md` files carry historical changes; do not fabricate these records for imported earlier chapters.

## IV. Initialization JSON Shape

The example below comes from Chapter 10 of the demo *You Manage the Account—and Your High-Energy Mashup Explodes Across the Internet*:

```json
{
  "江晨": {
    "identity": "火箭军文工团宣传兵；军宣爆款创作者",
    "location": "火箭军文工团高层看片会",
    "goal": "完成五天百万粉任务，继续做出真正能打的军宣内容",
    "state": "专业团队重拍版反向坐实手机原版的价值，军内认可继续抬升",
    "abilities_resources": [
      "前世 MCN 爆款运营经验",
      "《中国军魂》伴奏",
      "大师级导演能力"
    ],
    "relationships": [
      "钟嘉嘉持续提供军报资源",
      "周薄森和张耀祖已明确认可其创作能力"
    ],
    "knowledge": [
      "《军报》采访稿已经过审",
      "高层决定继续采用《诸君，且听龙吟》手机原版"
    ],
    "open_threads": [
      "五天百万粉任务尚未结算",
      "钟嘉嘉所谓只猜对一半仍未解释"
    ]
  }
}
```

**English guide (non-executable):**

```json
{
  "Jiang Chen": {
    "identity": "Military art-troupe publicity soldier and creator of viral military-publicity work",
    "location": "Senior screening meeting at the military art troupe",
    "goal": "Complete the five-day, one-million-followers task and continue producing effective military-publicity content",
    "state": "The professional remake has confirmed the phone-shot original's value, and military recognition continues to rise",
    "abilities_resources": [
      "Prior-life MCN viral-content operations experience",
      "Accompaniment track for Chinese Military Spirit",
      "Master-level directing ability"
    ],
    "relationships": [
      "Zhong Jiajia continues providing military-newspaper resources",
      "Zhou Bosen and Zhang Yaozu have explicitly recognized his creative ability"
    ],
    "knowledge": [
      "The military-newspaper interview draft has been approved",
      "Leadership will continue using the phone-shot original of Gentlemen, Hear the Dragon's Roar"
    ],
    "open_threads": [
      "The five-day, one-million-followers task is not settled",
      "Zhong Jiajia's statement that he guessed only half correctly remains unexplained"
    ]
  }
}
```

The translated object explains the sample values only. The canonical JSON retains the protected Chinese character name and text.

The generated file always contains: through chapter, identity, location, current objective, physical and emotional state, abilities and resources, key relationships, known information, and unresolved matters. The model must not create a second Markdown template.

## V. Incomplete Drafts and Batch Imports

- If the final chapter is incomplete, every snapshot stops at the preceding complete chapter. Actions, acquired objects, and relationship changes in the incomplete draft must not take effect early.
- For batch imports, a snapshot represents current state only within the imported range. When expanding that range, perform a new complete import rather than appending historical passages to the old snapshot.

## VI. Quality Checks

- [ ] Each file represents one core character; no accumulation of function-only characters.
- [ ] Every field contains the current value through the final complete chapter.
- [ ] Character-known information does not include author-only truth.
- [ ] Every unresolved matter has manuscript evidence; future designs remain in the outline.
- [ ] A single-character snapshot targets no more than 4,096 bytes. It may exceed that target when genuinely necessary but must remain below the hard limit of 8,192 bytes.
- [ ] `tracking_commit.py check` passes.
