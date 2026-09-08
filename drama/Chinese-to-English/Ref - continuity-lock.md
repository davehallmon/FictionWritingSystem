# Cross-Shot Continuity Locks

## Contents

- [Why Recognition Anchors Are Not Enough](#为什么识别锚点还不够)
- [What Deserves a Lock](#什么值得上一把锁)
- [How to Write the Lock Surface](#锁面怎么写)
- [Syntax](#语法)
- [Who Carries the Lock Surface Forward](#谁负责把锁面带走)
- [Counterexamples](#反例)
- [Validation](#校验)

## Why Recognition Anchors Are Not Enough

Recognition anchors are facts written for creators to read. The executor cannot read them; it sees only the body of each individual prompt. If the same sweater is blue in the first shot and red in the second, the asset is usually not defined incorrectly. Instead, **none of the prompts carried the color forward**: the visual definition included it, the keyframe included only part of it, and the motion prompt removed repeated description because it assumed the reference frame had already established it.

A reference image cannot fill this gap. A character board constrains only what it depicts. A sweater still being knitted and only half formed, a prop obscured by a hand, or clothing details recomposed in every shot all fall on the “must not control by default” side of an identity reference.

A continuity lock fills this gap: it fixes the few words that must remain unchanged across shots and requires them to appear verbatim in every affected prompt.

## What Deserves a Lock

All three conditions must hold:

1. The visible fact appears in more than one shot in the episode, or in one shot plus an asset board;
2. The audience can directly perceive an inconsistency;
3. It does not change with the plot—changing facts are state, and **state is not locked**.

Typical examples: the primary color and form of clothing; the primary color and material of a prop; hair length; wound location and shape; and the form/color scheme of a sign or interface. Atypical examples: emotion, pose, left/right hand, camera angle, time-of-day lighting, damage progression, and holder. These are state or shot transients and belong respectively to `本集状态` and the storyboard.

**`craft_default`**: An episode usually has a single-digit number of locks. Promoting every recognition anchor to a lock fills every prompt with the same string of noun phrases and crowds out the action that the current shot must actually perform.

## How to Write the Lock Surface

`锁面` is **the short span that must be carried verbatim into the prompt body**. It is not a description or a human-facing explanation:

- Write it in the project's prompt language (`short-drama.json#/format/prompt_language`; default `en` when unconfigured), because it belongs in the copyable body rather than creator-facing explanation.
- Retain only the smallest recognizable noun phrase, usually “color + material/form + object,” such as `pale blue chunky knit wool sweater`.
- Include no period, action, state, quantity, shot information, or plot.
- Do not include words that change across shots (`in her hands`, `half-finished`, `on the sofa`).
- Use one lock per entity. Two looks for the same entity require two locks, each with its own effective shots.

Comparison ignores letter case and treats line breaks as spaces because copyable text already renders as a paragraph and hard wraps do not affect matching. Compare every other character verbatim. A prompt may add grammar around the lock surface (`she keeps knitting the pale blue chunky knit wool
sweater`), but it cannot rewrite anything inside it: omitting one `stand-collar` or adding one comma counts as drift.

Two apparent matches are deliberately excluded because they do not actually put the fact into the image:

- **A match attached to another word does not count.** When the lock surface begins or ends with an alphanumeric character, an adjacent alphanumeric character or hyphen invalidates the match: `chipped white enamel mug` is not satisfied by `unchipped white enamel mug`, and `pale blue knit` is not satisfied by `pale blue knitwear-print fleece`. The lock surface must read as a complete phrase.
- **A match inside a negative prompt does not count.** A lock surface following `no`/`not`/`without`/`avoid` or `不要`/`不能`/`没有`/`避免` means “do not show this,” the opposite of the lock's purpose. `..., no pale blue chunky knit wool
  sweater` is not evidence that the lock surface is present. The lock surface must occur in the body that describes visible image content. “Attached to another word” applies only to ASCII words; Chinese has no word separators, so `织着浅蓝色粗棒针毛线` is a valid match.

## Syntax

Write the lock beneath the corresponding asset entry in `视觉设定.md`, alongside its recognition anchor:

```markdown
## 道具 · 织了一半的毛衣

- 识别锚点：浅蓝色粗棒针手织毛线，竹制棒针两根，衣身只织到胸口。
- 本集状态：SC002 起衣身加长约一掌；颜色与针法不变。
- 连续性锁：LOCK-KNIT《织了一半的毛衣》（镜头：全集；图片提示词项：IMG-PROP-KNIT）· 锁面：pale blue chunky knit wool sweater
```

**English guide (non-executable):** Prop: a half-knitted sweater. Identity anchors: pale-blue chunky hand-knit wool, two bamboo needles, and a body knitted only to chest length. From SC002 onward, the body grows by roughly one handspan while color and stitch pattern remain unchanged. Continuity lock `LOCK-KNIT` applies to the full episode and image-prompt item `IMG-PROP-KNIT`; the locked English surface is “pale blue chunky knit wool sweater.”

- Whether the list marker is `-`, `*`, or `+`, and the amount of indentation, does not affect recognition. A line that resembles a lock but is incomplete is reported as a syntax error rather than silently skipped—a lock cannot become inert.
- `LOCK-...`: the episode's unique stable ID, not interchangeable with `IMG-...`, `REF-...`, or `SHOT-...`.
- `《中文名》`: the creator-facing name, which must contain Chinese.
- `镜头：`: either `全集` or a `、`-separated list of `SHOT-...` entries; never mix the two.
- `图片提示词项：`: optional, followed by a `、`-separated list of `IMG-...` entries. Omitting the entire segment means the lock does not constrain image prompts.
- `锁面：`: the verbatim span carried forward, written at the end of the line.

## Who Carries the Lock Surface Forward

| Document | Obligation |
|---|---|
| `图片提示词.md` | Each named `IMG-...` copyable body contains the lock surface, ensuring the reference image itself is correct |
| `分镜.md` | The frozen-keyframe prompt for every effective shot contains the lock surface |
| `视频提示词.md` | The corresponding `MOTION-...` copyable body contains the lock surface |

**`structural_invariant` CON-07**: A lock surface must not be deleted within its effective scope on the grounds that “the reference frame already established it.” Removing repeated static description from image-to-video prompts is normal, but the lock surface is an explicit exception: it exists specifically to prevent cross-shot drift.

State changes do not enter the lock surface. Put the sweater's increasing length in `本集状态`; put its color and stitch pattern in the lock surface. When both exist, the prompt describes the length while the lock surface controls color and stitch pattern.

## Counterexamples

- `锁面：蓝色毛衣`—it will never match an English prompt body, and “blue” does not distinguish pale blue from navy.
- `锁面：a pale blue sweater that she has been knitting since the first scene`—it contains plot and tense and must be rewritten in the next shot, immediately defeating the lock.
- `锁面：high quality, detailed`—this is not a recognizable fact, so locking it proves no continuity.
- Limiting a lock's `镜头` scope to “the shots where the wording is already correct”—scope must reflect **every shot where the fact actually appears**. Defining it only around correct instances points the validator away from the risk.
- Applying `镜头：全集` to a prop that appears in only two shots forces irrelevant nouns into every other shot.

## Validation

```bash
python3 <core 技能目录>/scripts/creator_markdown_check.py 剧集/<EP> --project-root .
```

**English guide (non-executable):** Replace `<core 技能目录>` with the core skill directory and `剧集/<EP>` with the episode directory before running the check.

The validator checks only syntax, parseable scope, and whether the lock surface truly occurs in every named body. Whether a lock is warranted and whether its surface is accurate remain creative and review judgments.
