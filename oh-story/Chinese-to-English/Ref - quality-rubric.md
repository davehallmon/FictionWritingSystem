# General Web-Fiction Content Review Rubric

> Purpose: Use this as the default fiction-content scoring standard for `/story-review` when the user has not specified a target platform such as Tomato Novel, Qidian, or Zhihu Yanxuan. It evaluates **story-text quality**, not skill/plugin implementation quality.

## Scoring Method

Mark each item PASS / WARN / FAIL, then convert every FAIL/WARN into the unified Findings Schema:
- Affects the main plot, character motivation, world rules, or reader trust → S1
- Clearly affects retention, pacing, chapter impact, or character credibility → S2
- Local quality, formatting, wording, or minor pacing issue → S3
- Style suggestion or optional enhancement → S4

## Core Dimensions

| Dimension | PASS | WARN | FAIL |
|---|---|---|---|
| Core selling point | The chapter advances around a clear selling point, and readers know why they should continue | The selling point exists but is weakly expressed or diluted by subplots | It is unclear which selling point or main plot this chapter serves |
| Conflict progression | The chapter contains a clear conflict, obstacle, choice, or cost | Conflict is light and the sense of progress is insufficient | The chapter consists mainly of explanation, small talk, or summary, with no substantive progress |
| Task obstruction | A character's attempt to accomplish something is blocked, and the blockage changes information, relationships, costs, choices, or foreshadowing | An obstruction exists, but the resulting change is weak and could be compressed | The obstruction is merely procedural detail; removing it would not affect the story |
| Emotional curve | The chapter builds, intensifies, releases, or reverses emotion | Emotion changes, but the turning points are unclear | Emotion is flat or changes direction abruptly |
| Hooks and anticipation | At least one point at the beginning or end creates anticipation | The hook is weak, but a question remains for what follows | There is no suspense, goal, or unresolved expectation |
| Opening freshness (opening/first 3 chapters only) | The opening uses a specific character or situation as its entry point rather than the genre's default routine | A hook exists, but the opening's shape collides with comparable works in the genre | The opening is the genre's default template and could be transplanted wholesale into any similar book (homogenized) |
| Character motivation | Behavior fits goals, personality, circumstances, and relationship pressure | Some behavior lacks setup | A character becomes implausible merely to advance the plot |
| Dialogue quality | Dialogue contains subtext, information control, and distinct character voices | Some dialogue dumps information or voices sound somewhat alike | Dialogue reads like a manual and everyone speaks in the same voice |
| Setting consistency | The text does not violate established rules, timeline, or character attributes | A minor ambiguity needs supporting evidence | The text conflicts with established setting or prior facts |
| Naturalness of prose | Prose is concrete and perceptible, with action carrying information | Occasional stock phrases or abstract summaries appear | AI-like phrasing, clichés, or summary-style prose is conspicuous |
| Sentence-length rhythm | Narration defaults to long comma-linked sentences; short sentences appear only as occasional isolated emphatic beats, after which the prose returns to long comma-linked sentences | Local fragments or telegraphic prose, or occasional mechanical alternation between long and short sentences | Clauses of ≤5 Chinese characters are chained between commas, ultra-short sentences make the whole text read like an outline, or revision fractures long comma-linked sentences |
| Punctuation rhythm | Punctuation matches tone, character voice, and emotional function | Punctuation is locally monotonous or slightly overused | The entire text is forced into periods, question/exclamation marks are piled up randomly, or `……`/`——` are used to manufacture pauses |
| Exact character-count expression | Claims such as “these five characters” or “just four short characters” have been verified as accurate and narratively necessary | The count is accurate, but wording such as “those few characters” would sound more natural | The stated count is wrong, or the counting convention cannot be confirmed |
| Formatting readability | Paragraphs break naturally by dramatic unit or shot, dialogue stands alone, blank lines are not excessive, and subject cadence feels natural | Some paragraphs are too long or too fragmented, or subjects repeat slightly too often | Dense blocks, mechanical paragraphing, hard-to-read dialogue/narration, or excessive subjects impair readability |
| Plot loop | The goal → obstacle → action → cost/feedback → new expectation loop is clear | A loop exists but one link is missing or feedback is weak | There is no goal, obstacle, or feedback, so readers cannot tell how the situation changes |
| Climax construction | Accumulation → false victory → collapse → reversal/payoff unfolds in layers | A high-impact moment exists, but buildup or payoff is insufficient | The climax is flat and direct, carries no cost, offers no payoff, or leaves emotion unresolved |
| Relationship progression | Interaction intensity matches the relationship stage, and boundary crossings are prepared | Some progression is slightly fast but can be supported with evidence | Intimacy, trust, or hostility appears suddenly, causing the relationship to jump states |
| Foreshadowing state | Setup, state, and payoff path are traceable | Foreshadowing is somewhat too dense or sparse but remains understandable | Foreshadowing conflicts with the setting, breaks off, or confuses understanding of the main plot |

## Three Golden Questions

1. **Why does the reader turn the page?** If this cannot be answered, assign at least S2.
2. **What changed in this chapter?** At least one of plot, relationship, information, or emotion must change; otherwise assign at least S2.
3. **What evidence supports your judgment?** Do not output a finding without source-text evidence; write “insufficient evidence” instead.

## Publication Recommendation Thresholds

| Overall condition | Verdict |
|---|---|
| No S1/S2 issues; S3 issues can be handled quickly | APPROVE |
| S2 issues exist, or numerous S3 issues impair reading | CONCERNS |
| An S1 issue exists, or the core selling point, motivation, or rules have collapsed | REJECT |

## Output Requirements

- Every issue must include severity, category, location, evidence, issue, and fix.
- List S1/S2 issues before S3/S4 issues.
- Do not provide only vague evaluation; every finding must guide the next revision.
- For a `consistency` / `factual` finding, the fix should state only how to unify the facts, not offer literary-writing advice.
