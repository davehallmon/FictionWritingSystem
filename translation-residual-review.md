# Translation Residual Review — Issue #5

**Acceptance:** FAIL

```json
{
  "pairs": 162,
  "files_with_residuals": 66,
  "residual_occurrences": 1411,
  "residual_han_characters": 4681,
  "classification_counts": {
    "intentional_bilingual_example": 214,
    "operational_chinese_output": 308,
    "proper_name_title": 43,
    "protected_literal": 745,
    "unexplained_prose": 46,
    "unresolved_anchor": 1
  },
  "deprecated_terminology": 0,
  "missing_outputs": 0,
  "ledger_status": "review_required",
  "accepted": false
}
```

## Terminology normalization

Files changed by deprecated-term normalization in this run: 4
- `drama/Chinese-to-English/README - DRAMA SKILLS`
- `drama/Chinese-to-English/README - Drama Skills - English.md`
- `oh-story/Chinese-to-English/Ref - topic-decision.md`
- `oh-story/Chinese-to-English/SKILL - story-long-scan.md`

## Classification totals

- `protected_literal`: 745 ledger entries
- `operational_chinese_output`: 308 ledger entries
- `proper_name_title`: 43 ledger entries
- `intentional_bilingual_example`: 214 ledger entries
- `unresolved_anchor`: 1 ledger entries
- `unexplained_prose`: 46 ledger entries

## Unaccepted findings

- `oh-story/Chinese-to-English/Ref - output-templates.md:143` — `unexplained_prose` — `字完成` — | Setup | {什么让读者开始在意}，前{X}字完成 |
- `oh-story/Chinese-to-English/Ref - output-templates.md:144` — `unexplained_prose` — `字` — | Accumulation | {什么在积累情绪势能}，积累{X}字 |
- `oh-story/Chinese-to-English/Ref - plot-special-topics.md:19` — `unresolved_anchor` — `#ranking-scans-and-book-deconstruction` — | Need market research / competitor deconstruction | [Rankings Scans and Book Deconstruction](#ranking-scans-and-book-deconstruction) |
- `oh-story/Chinese-to-English/SKILL - story-deslop.md:278` — `unexplained_prose` — `他拿起笔` — - ❌ “他拿起笔。手在抖。笔尖又停住。”
- `oh-story/Chinese-to-English/SKILL - story-deslop.md:278` — `unexplained_prose` — `手在抖` — - ❌ “他拿起笔。手在抖。笔尖又停住。”
- `oh-story/Chinese-to-English/SKILL - story-deslop.md:278` — `unexplained_prose` — `笔尖又停住` — - ❌ “他拿起笔。手在抖。笔尖又停住。”
- `oh-story/Chinese-to-English/SKILL - story-deslop.md:279` — `unexplained_prose` — `他拿起笔` — - ✅ “他拿起笔，笔尖刚碰到纸就偏了，手腕压了两次都没压稳。”
- `oh-story/Chinese-to-English/SKILL - story-deslop.md:279` — `unexplained_prose` — `手腕压了两次都没压稳` — - ✅ “他拿起笔，笔尖刚碰到纸就偏了，手腕压了两次都没压稳。”
- `oh-story/Chinese-to-English/SKILL - story-deslop.md:279` — `unexplained_prose` — `笔尖刚碰到纸就偏了` — - ✅ “他拿起笔，笔尖刚碰到纸就偏了，手腕压了两次都没压稳。”
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:90` — `unexplained_prose` — `信息差` — >      "technique": "铺垫后置|反应层放大|信息差|对比锚点|延迟揭示|身体反应|小目标嵌套|其他",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:90` — `unexplained_prose` — `其他` — >      "technique": "铺垫后置|反应层放大|信息差|对比锚点|延迟揭示|身体反应|小目标嵌套|其他",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:90` — `unexplained_prose` — `反应层放大` — >      "technique": "铺垫后置|反应层放大|信息差|对比锚点|延迟揭示|身体反应|小目标嵌套|其他",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:90` — `unexplained_prose` — `对比锚点` — >      "technique": "铺垫后置|反应层放大|信息差|对比锚点|延迟揭示|身体反应|小目标嵌套|其他",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:90` — `unexplained_prose` — `小目标嵌套` — >      "technique": "铺垫后置|反应层放大|信息差|对比锚点|延迟揭示|身体反应|小目标嵌套|其他",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:90` — `unexplained_prose` — `延迟揭示` — >      "technique": "铺垫后置|反应层放大|信息差|对比锚点|延迟揭示|身体反应|小目标嵌套|其他",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:90` — `unexplained_prose` — `身体反应` — >      "technique": "铺垫后置|反应层放大|信息差|对比锚点|延迟揭示|身体反应|小目标嵌套|其他",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:90` — `unexplained_prose` — `铺垫后置` — >      "technique": "铺垫后置|反应层放大|信息差|对比锚点|延迟揭示|身体反应|小目标嵌套|其他",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:108` — `unexplained_prose` — `信息揭示` — >      "type": "转折点|信息揭示|冲突|解决|铺垫|行动|对话|状态变化",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:108` — `unexplained_prose` — `冲突` — >      "type": "转折点|信息揭示|冲突|解决|铺垫|行动|对话|状态变化",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:108` — `unexplained_prose` — `对话` — >      "type": "转折点|信息揭示|冲突|解决|铺垫|行动|对话|状态变化",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:108` — `unexplained_prose` — `状态变化` — >      "type": "转折点|信息揭示|冲突|解决|铺垫|行动|对话|状态变化",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:108` — `unexplained_prose` — `行动` — >      "type": "转折点|信息揭示|冲突|解决|铺垫|行动|对话|状态变化",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:108` — `unexplained_prose` — `解决` — >      "type": "转折点|信息揭示|冲突|解决|铺垫|行动|对话|状态变化",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:108` — `unexplained_prose` — `转折点` — >      "type": "转折点|信息揭示|冲突|解决|铺垫|行动|对话|状态变化",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:108` — `unexplained_prose` — `铺垫` — >      "type": "转折点|信息揭示|冲突|解决|铺垫|行动|对话|状态变化",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:113` — `unexplained_prose` — `亲情` — >      "themes": ["爱情|亲情|友情|权力|金钱|成长|复仇|悬念|搞笑|热血|日常|其他"],
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:113` — `unexplained_prose` — `其他` — >      "themes": ["爱情|亲情|友情|权力|金钱|成长|复仇|悬念|搞笑|热血|日常|其他"],
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:113` — `unexplained_prose` — `友情` — >      "themes": ["爱情|亲情|友情|权力|金钱|成长|复仇|悬念|搞笑|热血|日常|其他"],
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:113` — `unexplained_prose` — `复仇` — >      "themes": ["爱情|亲情|友情|权力|金钱|成长|复仇|悬念|搞笑|热血|日常|其他"],
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:113` — `unexplained_prose` — `悬念` — >      "themes": ["爱情|亲情|友情|权力|金钱|成长|复仇|悬念|搞笑|热血|日常|其他"],
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:113` — `unexplained_prose` — `成长` — >      "themes": ["爱情|亲情|友情|权力|金钱|成长|复仇|悬念|搞笑|热血|日常|其他"],
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:113` — `unexplained_prose` — `搞笑` — >      "themes": ["爱情|亲情|友情|权力|金钱|成长|复仇|悬念|搞笑|热血|日常|其他"],
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:113` — `unexplained_prose` — `日常` — >      "themes": ["爱情|亲情|友情|权力|金钱|成长|复仇|悬念|搞笑|热血|日常|其他"],
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:113` — `unexplained_prose` — `权力` — >      "themes": ["爱情|亲情|友情|权力|金钱|成长|复仇|悬念|搞笑|热血|日常|其他"],
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:113` — `unexplained_prose` — `热血` — >      "themes": ["爱情|亲情|友情|权力|金钱|成长|复仇|悬念|搞笑|热血|日常|其他"],
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:113` — `unexplained_prose` — `爱情` — >      "themes": ["爱情|亲情|友情|权力|金钱|成长|复仇|悬念|搞笑|热血|日常|其他"],
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:113` — `unexplained_prose` — `金钱` — >      "themes": ["爱情|亲情|友情|权力|金钱|成长|复仇|悬念|搞笑|热血|日常|其他"],
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:114` — `unexplained_prose` — `其他` — >      "tone": "紧张|轻松|悲伤|热血|爽|甜|温馨|恐怖|压抑|其他"}
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:114` — `unexplained_prose` — `压抑` — >      "tone": "紧张|轻松|悲伤|热血|爽|甜|温馨|恐怖|压抑|其他"}
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:114` — `unexplained_prose` — `恐怖` — >      "tone": "紧张|轻松|悲伤|热血|爽|甜|温馨|恐怖|压抑|其他"}
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:114` — `unexplained_prose` — `悲伤` — >      "tone": "紧张|轻松|悲伤|热血|爽|甜|温馨|恐怖|压抑|其他"}
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:114` — `unexplained_prose` — `温馨` — >      "tone": "紧张|轻松|悲伤|热血|爽|甜|温馨|恐怖|压抑|其他"}
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:114` — `unexplained_prose` — `热血` — >      "tone": "紧张|轻松|悲伤|热血|爽|甜|温馨|恐怖|压抑|其他"}
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:114` — `unexplained_prose` — `爽` — >      "tone": "紧张|轻松|悲伤|热血|爽|甜|温馨|恐怖|压抑|其他"}
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:114` — `unexplained_prose` — `甜` — >      "tone": "紧张|轻松|悲伤|热血|爽|甜|温馨|恐怖|压抑|其他"}
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:114` — `unexplained_prose` — `紧张` — >      "tone": "紧张|轻松|悲伤|热血|爽|甜|温馨|恐怖|压抑|其他"}
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:114` — `unexplained_prose` — `轻松` — >      "tone": "紧张|轻松|悲伤|热血|爽|甜|温馨|恐怖|压抑|其他"}

## Review contract

- Protected literals are retained because changing them would alter source-compatible paths, fields, assets, anchors, schemas, or identifiers.
- Operational Chinese outputs are retained only where the surrounding structured instruction establishes that the literal value is consumed or emitted by the workflow.
- Proper names/titles are retained for identity and provenance.
- Intentional bilingual examples are retained only in explicitly quoted/demo/trigger/example contexts.
- Any occurrence not matched by those narrow rules remains `unexplained_prose` and blocks acceptance.
