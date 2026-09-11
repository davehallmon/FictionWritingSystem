# Evaluation Standard for Hooks in Short-Form Source Text

> Observe how the source changes reader expectations at paragraph breaks, section boundaries, and paywall breaks. Report only hooks, promises, and later responses that actually appear. Do not supply chapter-opening or chapter-ending templates, impose serialization loops, or use fixed character counts.

## Conditions for a Valid Hook

A boundary counts as a hook only when it changes “what the reader is waiting for next.” A sentence break, heightened emotion, a shocked character, or authorial preview does not automatically constitute a hook.

Record each candidate point:

```markdown
位置：{段落/小节/付费断点}
边界前已知：{事实与判断}
边界新增：{动作、证据、关系、风险或选择}
读者新问题：{具体问题}
后续回应：{位置与交付}
```

**English guide (non-executable):** Location (paragraph, section, or paywall break); what was known before the boundary; what the boundary adds through action, evidence, relationships, risk, or choice; the reader's new question; and where and how the story later answers it.

## Functional Types

| Type | Observable change | Common false positive |
|---|---|---|
| Unfinished action | A character begins a risky action whose result has not appeared | The text merely says “he decided,” and no action follows in the next section |
| Ownership of evidence | New evidence appears, or its holder, authenticity, or interpretive authority changes | One item of background information is added |
| Fracture in identity or motive | Behavior creates a traceable contradiction with an apparent identity or motive | The ending directly declares “he has a secret” |
| Relationship turn | Trust, alliance, control, or responsibility changes | An emotional argument occurs without changing the relationship's position |
| Dilemma | Two genuine costs exist simultaneously and the character has not chosen | A false choice in which one option is obviously impossible |
| Risk becomes concrete | An abstract threat becomes a specific deadline, loss, or accountability | Adjectives intensify without changing the conditions for action |
| Provisional answer | A local question receives a credible answer while exposing an explanatory gap | The story immediately reverses the answer again without causality |
| Consequence strikes back | A completed action produces an unexpected but traceable consequence | A new crisis arrives by coincidence and is unrelated to the earlier action |
| Emotional debt | A relational or ethical choice remains unsettled | Authorial summary replaces consequences for the characters |

## Assessing Strength

Do not use subjective rankings or adjectives such as “must-click.” Compare three reproducible dimensions:

1. **Prediction change:** Does the boundary cause the reader to revise a prediction about suspicion, relationships, results, or cost?
2. **Pull toward action:** Must the next paragraph or section respond to this change rather than opening an unrelated topic?
3. **Payoff quality:** Does the response deliver evidence, a choice, or a consequence rather than merely repeating the question?

When all three dimensions hold, report a key hook. When only one holds, report weak pull or a transitional boundary.

## Hook Chains

A hook chain is not an accumulation of hooks. The response to one question becomes the cause of the next question. Track the chain in this table:

| Starting location | Question | Response location | What the response delivers | How it generates the next question |
|---|---|---|---|---|

If a later question has no causal relationship to the preceding answer, report a “new mystery.” If several consecutive questions receive no local answer, report “escalation without delivery.”

## Paywall Breaks

A paywall break is a commercial position; a hook is a narrative function. Neither proves the other. Evaluate them separately:

- Does the break occur on an unfinished action, changed ownership of evidence, a relationship turn, or a genuine dilemma?
- Does the text respond to the break's promise soon after payment?
- Does that response advance the central question rather than delay it through a side branch?
- If platform information is unavailable, report only a “candidate strong break”; do not infer the actual paid position.

## Report Format

```markdown
关键钩子：{位置、类型、边界前后变化}
读者新问题：{具体问题}
后续回应：{位置、交付}
钩子链：{因果接力或断裂}
付费断点：{已知/候选/证据不足}
弱边界或假钩子：{位置与原因}
```

**English guide (non-executable):** Key hook and boundary change; reader's new question; later response and delivery; causal continuity or break in the hook chain; known, candidate, or unsupported paywall break; and weak boundaries or false hooks with their locations and reasons.

## Boundaries

- You may count actual hooks, but never use a fixed count as a quality threshold for the source.
- You may compare differences in pull between adjacent sections, but do not require a strong hook in every section.
- Do not evaluate chapter openings or endings by fixed character counts; boundary length follows information and action.
- Do not automatically classify shocked bystanders, system rewards, or a new map as hooks. Demonstrate that the element changes the reader's question.
