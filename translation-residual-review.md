# Translation Residual Review — Issue #5

**Acceptance:** FAIL

```json
{
  "pairs": 160,
  "files_with_residuals": 65,
  "residual_occurrences": 1410,
  "residual_han_characters": 4677,
  "classification_counts": {
    "intentional_bilingual_example": 189,
    "operational_chinese_output": 78,
    "proper_name_title": 43,
    "protected_literal": 744,
    "unexplained_prose": 301,
    "unresolved_anchor": 1
  },
  "deprecated_terminology": 2,
  "missing_outputs": 0,
  "ledger_status": "review_required",
  "accepted": false
}
```

## Terminology normalization

Files changed by deprecated-term normalization in this run: 1
- `drama/Chinese-to-English/README - DRAMA SKILLS`

## Classification totals

- `protected_literal`: 744 ledger entries
- `operational_chinese_output`: 78 ledger entries
- `proper_name_title`: 43 ledger entries
- `intentional_bilingual_example`: 189 ledger entries
- `unresolved_anchor`: 1 ledger entries
- `unexplained_prose`: 301 ledger entries

## Unaccepted findings

- `drama/Chinese-to-English/Ref - asset-review-checklist.md:69` — `unexplained_prose` — `未决` — Write creator-confirmed results directly into `视觉设定.md`. Keep unconfirmed choices marked “未决” and explain their impact. Creator confirmation does not mean that structural checks passed, review passed, or production may b
- `drama/Chinese-to-English/Ref - creator-documents.md:218` — `unexplained_prose` — `创作者已明确选择文生视频` — need restate only local starting-point and anti-drift facts required for motion. Use text-to-video only when the field is 输入参考图：无（创作者已明确选择文生视频）; its prose must independently
- `drama/Chinese-to-English/Ref - creator-documents.md:218` — `unexplained_prose` — `无` — need restate only local starting-point and anti-drift facts required for motion. Use text-to-video only when the field is 输入参考图：无（创作者已明确选择文生视频）; its prose must independently
- `drama/Chinese-to-English/Ref - creator-documents.md:218` — `unexplained_prose` — `输入参考图` — need restate only local starting-point and anti-drift facts required for motion. Use text-to-video only when the field is 输入参考图：无（创作者已明确选择文生视频）; its prose must independently
- `drama/Chinese-to-English/Ref - occurrence-extraction.md:49` — `unexplained_prose` — `未决` — When no decision has been reached, mark the corresponding entry “未决” and list candidates, missing evidence, and impact. For a continuity change that will occur only in the future, write only a “需要同步” note; do not create 
- `drama/Chinese-to-English/Ref - occurrence-extraction.md:49` — `unexplained_prose` — `需要同步` — When no decision has been reached, mark the corresponding entry “未决” and list candidates, missing evidence, and impact. For a continuity change that will occur only in the future, write only a “需要同步” note; do not create 
- `drama/Chinese-to-English/Ref - stage-contract.md:34` — `unexplained_prose` — `设定集` — | CON-03 | craft_default | Track downstream-relevant deltas, not the whole 设定集 in every shot. |
- `oh-story/Chinese-to-English/Ref - material-decomposition.md:367` — `unexplained_prose` — `沈暮月心碎地听到了真相` — - Prohibited: “沈暮月心碎地听到了真相.”
- `oh-story/Chinese-to-English/Ref - material-decomposition.md:368` — `unexplained_prose` — `手停在半空` — - Correct: “沈暮月听到‘私生子而已’，手停在半空.”
- `oh-story/Chinese-to-English/Ref - material-decomposition.md:368` — `unexplained_prose` — `沈暮月听到` — - Correct: “沈暮月听到‘私生子而已’，手停在半空.”
- `oh-story/Chinese-to-English/Ref - material-decomposition.md:368` — `unexplained_prose` — `私生子而已` — - Correct: “沈暮月听到‘私生子而已’，手停在半空.”
- `oh-story/Chinese-to-English/Ref - material-decomposition.md:377` — `unexplained_prose` — `通过这段对话展现了她的坚强` — - Prohibited: “通过这段对话展现了她的坚强.”
- `oh-story/Chinese-to-English/Ref - material-decomposition.md:378` — `unexplained_prose` — `她直视霍庭煜说` — - Correct: “她直视霍庭煜说‘我没有义务配合你’.”
- `oh-story/Chinese-to-English/Ref - material-decomposition.md:378` — `unexplained_prose` — `我没有义务配合你` — - Correct: “她直视霍庭煜说‘我没有义务配合你’.”
- `oh-story/Chinese-to-English/Ref - material-decomposition.md:379` — `unexplained_prose` — `气氛变得紧张` — - Prohibited: “气氛变得紧张.”
- `oh-story/Chinese-to-English/Ref - material-decomposition.md:380` — `unexplained_prose` — `周身散发出威压` — - Correct: “霍庭煜眼神骤冷，周身散发出威压.”
- `oh-story/Chinese-to-English/Ref - material-decomposition.md:380` — `unexplained_prose` — `霍庭煜眼神骤冷` — - Correct: “霍庭煜眼神骤冷，周身散发出威压.”
- `oh-story/Chinese-to-English/Ref - output-contract.md:143` — `unexplained_prose` — `共鸣分析` — 2. Read the “核心手法,” “共鸣分析,” and “可复用结构” sections of `拆文报告.md` to decide what to retain or adjust.
- `oh-story/Chinese-to-English/Ref - output-contract.md:143` — `unexplained_prose` — `可复用结构` — 2. Read the “核心手法,” “共鸣分析,” and “可复用结构” sections of `拆文报告.md` to decide what to retain or adjust.
- `oh-story/Chinese-to-English/Ref - output-contract.md:143` — `unexplained_prose` — `核心手法` — 2. Read the “核心手法,” “共鸣分析,” and “可复用结构” sections of `拆文报告.md` to decide what to retain or adjust.
- `oh-story/Chinese-to-English/Ref - output-templates.md:43` — `unexplained_prose` — `平台` — Length {X} Chinese characters | Sections {N} | Platform {平台} | Type {题材/情绪类型} | Ending {HE/BE/开放式} | POV {第一/第三人称}
- `oh-story/Chinese-to-English/Ref - output-templates.md:54` — `unexplained_prose` — `字概括全文` — {200-500字概括全文}
- `oh-story/Chinese-to-English/Ref - output-templates.md:60` — `unexplained_prose` — `功能` — | Opening | {X}-{Y} | {Z%} | {功能} | {节号} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:60` — `unexplained_prose` — `节号` — | Opening | {X}-{Y} | {Z%} | {功能} | {节号} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:61` — `unexplained_prose` — `功能` — | Development | {X}-{Y} | {Z%} | {功能} | {节号} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:61` — `unexplained_prose` — `节号` — | Development | {X}-{Y} | {Z%} | {功能} | {节号} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:62` — `unexplained_prose` — `功能` — | {转折/过渡（可选）} | {X}-{Y} | {Z%} | {功能} | {节号} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:62` — `unexplained_prose` — `节号` — | {转折/过渡（可选）} | {X}-{Y} | {Z%} | {功能} | {节号} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:63` — `unexplained_prose` — `功能` — | Climax | {X}-{Y} | {Z%} | {功能} | {节号} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:63` — `unexplained_prose` — `节号` — | Climax | {X}-{Y} | {Z%} | {功能} | {节号} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:64` — `unexplained_prose` — `功能` — | Ending | {X}-{Y} | {Z%} | {功能} | {节号} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:64` — `unexplained_prose` — `节号` — | Ending | {X}-{Y} | {Z%} | {功能} | {节号} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:71` — `unexplained_prose` — `故事内时间跨度` — | Time span | {故事内时间跨度} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:129` — `unexplained_prose` — `事件` — | Opening | {X} | N{N} | {好奇/心酸/震惊} | {虐-9~爽+9} | {事件} | {悬念/冲突/反差/代入/信息差/无} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:129` — `unexplained_prose` — `爽` — | Opening | {X} | N{N} | {好奇/心酸/震惊} | {虐-9~爽+9} | {事件} | {悬念/冲突/反差/代入/信息差/无} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:129` — `unexplained_prose` — `虐` — | Opening | {X} | N{N} | {好奇/心酸/震惊} | {虐-9~爽+9} | {事件} | {悬念/冲突/反差/代入/信息差/无} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:130` — `unexplained_prose` — `事件` — | Low point | {X} | N{N} | {心疼/绝望/愤怒} | {虐-9~爽+9} | {事件} | {钩子类型} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:130` — `unexplained_prose` — `爽` — | Low point | {X} | N{N} | {心疼/绝望/愤怒} | {虐-9~爽+9} | {事件} | {钩子类型} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:130` — `unexplained_prose` — `虐` — | Low point | {X} | N{N} | {心疼/绝望/愤怒} | {虐-9~爽+9} | {事件} | {钩子类型} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:130` — `unexplained_prose` — `钩子类型` — | Low point | {X} | N{N} | {心疼/绝望/愤怒} | {虐-9~爽+9} | {事件} | {钩子类型} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:131` — `unexplained_prose` — `事件` — | Reversal point | {X} | N{N} | {震惊/心疼} | {虐-9~爽+9} | {事件} | {钩子类型} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:131` — `unexplained_prose` — `爽` — | Reversal point | {X} | N{N} | {震惊/心疼} | {虐-9~爽+9} | {事件} | {钩子类型} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:131` — `unexplained_prose` — `虐` — | Reversal point | {X} | N{N} | {震惊/心疼} | {虐-9~爽+9} | {事件} | {钩子类型} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:131` — `unexplained_prose` — `钩子类型` — | Reversal point | {X} | N{N} | {震惊/心疼} | {虐-9~爽+9} | {事件} | {钩子类型} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:132` — `unexplained_prose` — `事件` — | Climax | {X} | N{N} | {情绪} | {虐-9~爽+9} | {事件} | {钩子类型} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:132` — `unexplained_prose` — `情绪` — | Climax | {X} | N{N} | {情绪} | {虐-9~爽+9} | {事件} | {钩子类型} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:132` — `unexplained_prose` — `爽` — | Climax | {X} | N{N} | {情绪} | {虐-9~爽+9} | {事件} | {钩子类型} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:132` — `unexplained_prose` — `虐` — | Climax | {X} | N{N} | {情绪} | {虐-9~爽+9} | {事件} | {钩子类型} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:132` — `unexplained_prose` — `钩子类型` — | Climax | {X} | N{N} | {情绪} | {虐-9~爽+9} | {事件} | {钩子类型} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:133` — `unexplained_prose` — `事件` — | Ending | {X} | N{N} | {满足/意难平/治愈} | {虐-9~爽+9} | {事件} | {钩子类型} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:133` — `unexplained_prose` — `爽` — | Ending | {X} | N{N} | {满足/意难平/治愈} | {虐-9~爽+9} | {事件} | {钩子类型} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:133` — `unexplained_prose` — `虐` — | Ending | {X} | N{N} | {满足/意难平/治愈} | {虐-9~爽+9} | {事件} | {钩子类型} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:133` — `unexplained_prose` — `钩子类型` — | Ending | {X} | N{N} | {满足/意难平/治愈} | {虐-9~爽+9} | {事件} | {钩子类型} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:137` — `unexplained_prose` — `从` — Curve characteristics: Start {...} | Direction {上行/下行/波浪/V形/倒V/阶梯/断崖/压缩弹簧} | Extremes {最高%X 最低%Y} | Directional difference {从X到Y} | Number of reversals {N}
- `oh-story/Chinese-to-English/Ref - output-templates.md:137` — `unexplained_prose` — `到` — Curve characteristics: Start {...} | Direction {上行/下行/波浪/V形/倒V/阶梯/断崖/压缩弹簧} | Extremes {最高%X 最低%Y} | Directional difference {从X到Y} | Number of reversals {N}
- `oh-story/Chinese-to-English/Ref - output-templates.md:137` — `unexplained_prose` — `最低` — Curve characteristics: Start {...} | Direction {上行/下行/波浪/V形/倒V/阶梯/断崖/压缩弹簧} | Extremes {最高%X 最低%Y} | Directional difference {从X到Y} | Number of reversals {N}
- `oh-story/Chinese-to-English/Ref - output-templates.md:137` — `unexplained_prose` — `最高` — Curve characteristics: Start {...} | Direction {上行/下行/波浪/V形/倒V/阶梯/断崖/压缩弹簧} | Extremes {最高%X 最低%Y} | Directional difference {从X到Y} | Number of reversals {N}
- `oh-story/Chinese-to-English/Ref - output-templates.md:143` — `unexplained_prose` — `什么让读者开始在意` — | Setup | {什么让读者开始在意}，前{X}字完成 |
- `oh-story/Chinese-to-English/Ref - output-templates.md:143` — `unexplained_prose` — `前` — | Setup | {什么让读者开始在意}，前{X}字完成 |
- `oh-story/Chinese-to-English/Ref - output-templates.md:143` — `unexplained_prose` — `字完成` — | Setup | {什么让读者开始在意}，前{X}字完成 |
- `oh-story/Chinese-to-English/Ref - output-templates.md:144` — `unexplained_prose` — `什么在积累情绪势能` — | Accumulation | {什么在积累情绪势能}，积累{X}字 |
- `oh-story/Chinese-to-English/Ref - output-templates.md:144` — `unexplained_prose` — `字` — | Accumulation | {什么在积累情绪势能}，积累{X}字 |
- `oh-story/Chinese-to-English/Ref - output-templates.md:144` — `unexplained_prose` — `积累` — | Accumulation | {什么在积累情绪势能}，积累{X}字 |
- `oh-story/Chinese-to-English/Ref - output-templates.md:146` — `unexplained_prose` — `哪个瞬间释放全部情绪` — | Eruption | {哪个瞬间释放全部情绪}，精确到句子："{引用}" |
- `oh-story/Chinese-to-English/Ref - output-templates.md:146` — `unexplained_prose` — `引用` — | Eruption | {哪个瞬间释放全部情绪}，精确到句子："{引用}" |
- `oh-story/Chinese-to-English/Ref - output-templates.md:146` — `unexplained_prose` — `精确到句子` — | Eruption | {哪个瞬间释放全部情绪}，精确到句子："{引用}" |
- `oh-story/Chinese-to-English/Ref - output-templates.md:147` — `unexplained_prose` — `角色反应` — | Aftermath | {释放后的余震：角色反应} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:147` — `unexplained_prose` — `释放后的余震` — | Aftermath | {释放后的余震：角色反应} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:148` — `unexplained_prose` — `情绪释放后留下什么` — | Impression | {情绪释放后留下什么，读者记住什么} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:148` — `unexplained_prose` — `读者记住什么` — | Impression | {情绪释放后留下什么，读者记住什么} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:160` — `unexplained_prose` — `制造` — | 1 | {期待A} | {制造} | {A} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:160` — `unexplained_prose` — `期待` — | 1 | {期待A} | {制造} | {A} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:161` — `unexplained_prose` — `升级` — | 2 | {期待B} | {升级A} | {A+, B} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:161` — `unexplained_prose` — `期待` — | 2 | {期待B} | {升级A} | {A+, B} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:180` — `unexplained_prose` — `三年前的` — | {如：三年前的"灌醉"事件实为做局} | {霍庭煜} | {第9章} | {沈暮月当面驳斥} | {铺垫：证明判断基于错误前提} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:180` — `unexplained_prose` — `事件实为做局` — | {如：三年前的"灌醉"事件实为做局} | {霍庭煜} | {第9章} | {沈暮月当面驳斥} | {铺垫：证明判断基于错误前提} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:180` — `unexplained_prose` — `如` — | {如：三年前的"灌醉"事件实为做局} | {霍庭煜} | {第9章} | {沈暮月当面驳斥} | {铺垫：证明判断基于错误前提} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:180` — `unexplained_prose` — `沈暮月当面驳斥` — | {如：三年前的"灌醉"事件实为做局} | {霍庭煜} | {第9章} | {沈暮月当面驳斥} | {铺垫：证明判断基于错误前提} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:180` — `unexplained_prose` — `灌醉` — | {如：三年前的"灌醉"事件实为做局} | {霍庭煜} | {第9章} | {沈暮月当面驳斥} | {铺垫：证明判断基于错误前提} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:180` — `unexplained_prose` — `章` — | {如：三年前的"灌醉"事件实为做局} | {霍庭煜} | {第9章} | {沈暮月当面驳斥} | {铺垫：证明判断基于错误前提} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:180` — `unexplained_prose` — `第` — | {如：三年前的"灌醉"事件实为做局} | {霍庭煜} | {第9章} | {沈暮月当面驳斥} | {铺垫：证明判断基于错误前提} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:180` — `unexplained_prose` — `证明判断基于错误前提` — | {如：三年前的"灌醉"事件实为做局} | {霍庭煜} | {第9章} | {沈暮月当面驳斥} | {铺垫：证明判断基于错误前提} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:180` — `unexplained_prose` — `铺垫` — | {如：三年前的"灌醉"事件实为做局} | {霍庭煜} | {第9章} | {沈暮月当面驳斥} | {铺垫：证明判断基于错误前提} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:180` — `unexplained_prose` — `霍庭煜` — | {如：三年前的"灌醉"事件实为做局} | {霍庭煜} | {第9章} | {沈暮月当面驳斥} | {铺垫：证明判断基于错误前提} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:182` — `unexplained_prose` — `无` — If none exists, write “无.”
- `oh-story/Chinese-to-English/Ref - output-templates.md:190` — `unexplained_prose` — `具体行为` — | {如：虐待妻女} | {具体行为} | {对应惩罚} | {以彼之道还施彼身/自食恶果} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:190` — `unexplained_prose` — `如` — | {如：虐待妻女} | {具体行为} | {对应惩罚} | {以彼之道还施彼身/自食恶果} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:190` — `unexplained_prose` — `对应惩罚` — | {如：虐待妻女} | {具体行为} | {对应惩罚} | {以彼之道还施彼身/自食恶果} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:190` — `unexplained_prose` — `虐待妻女` — | {如：虐待妻女} | {具体行为} | {对应惩罚} | {以彼之道还施彼身/自食恶果} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:200` — `unexplained_prose` — `事件` — | 1 | {类型} | {事件} | {从A认知变为B认知} | — |
- `oh-story/Chinese-to-English/Ref - output-templates.md:200` — `unexplained_prose` — `从` — | 1 | {类型} | {事件} | {从A认知变为B认知} | — |
- `oh-story/Chinese-to-English/Ref - output-templates.md:200` — `unexplained_prose` — `类型` — | 1 | {类型} | {事件} | {从A认知变为B认知} | — |
- `oh-story/Chinese-to-English/Ref - output-templates.md:200` — `unexplained_prose` — `认知` — | 1 | {类型} | {事件} | {从A认知变为B认知} | — |
- `oh-story/Chinese-to-English/Ref - output-templates.md:200` — `unexplained_prose` — `认知变为` — | 1 | {类型} | {事件} | {从A认知变为B认知} | — |
- `oh-story/Chinese-to-English/Ref - output-templates.md:201` — `unexplained_prose` — `事件` — | 2 | {类型} | {事件} | {从B认知变为C认知} | {反转1如何解释/加深反转2} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:201` — `unexplained_prose` — `从` — | 2 | {类型} | {事件} | {从B认知变为C认知} | {反转1如何解释/加深反转2} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:201` — `unexplained_prose` — `类型` — | 2 | {类型} | {事件} | {从B认知变为C认知} | {反转1如何解释/加深反转2} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:201` — `unexplained_prose` — `认知` — | 2 | {类型} | {事件} | {从B认知变为C认知} | {反转1如何解释/加深反转2} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:201` — `unexplained_prose` — `认知变为` — | 2 | {类型} | {事件} | {从B认知变为C认知} | {反转1如何解释/加深反转2} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:220` — `unexplained_prose` — `含位置` — - Setup clues: {文本埋了哪些线索，含位置}
- `oh-story/Chinese-to-English/Ref - output-templates.md:220` — `unexplained_prose` — `文本埋了哪些线索` — - Setup clues: {文本埋了哪些线索，含位置}
- `oh-story/Chinese-to-English/Ref - output-templates.md:221` — `unexplained_prose` — `文本把读者往哪个方向引` — - Misdirection: {文本把读者往哪个方向引}
- `oh-story/Chinese-to-English/Ref - output-templates.md:222` — `unexplained_prose` — `反转怎么揭开的` — - Truth revealed: {反转怎么揭开的}
- `oh-story/Chinese-to-English/Ref - output-templates.md:223` — `unexplained_prose` — `反转是否经得起回看` — - Plausibility: {反转是否经得起回看}
- `oh-story/Chinese-to-English/Ref - output-templates.md:257` — `unexplained_prose` — `具体效果` — | {时间跳跃/场景压缩/倒叙/闪回/实时展开} | {节N} | {具体效果} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:257` — `unexplained_prose` — `节` — | {时间跳跃/场景压缩/倒叙/闪回/实时展开} | {节N} | {具体效果} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:271` — `unexplained_prose` — `具体效果` — | {感官锚定/句式节奏/对比设计/意象物件/留白/首尾呼应} | {节N} | {具体效果} | {高/中/低} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:277` — `unexplained_prose` — `从` — | {物件名} | {节1, 节5, 节9} | {含义变化} | {从A到B} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:277` — `unexplained_prose` — `到` — | {物件名} | {节1, 节5, 节9} | {含义变化} | {从A到B} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:277` — `unexplained_prose` — `含义变化` — | {物件名} | {节1, 节5, 节9} | {含义变化} | {从A到B} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:277` — `unexplained_prose` — `物件名` — | {物件名} | {节1, 节5, 节9} | {含义变化} | {从A到B} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:277` — `unexplained_prose` — `节` — | {物件名} | {节1, 节5, 节9} | {含义变化} | {从A到B} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:279` — `unexplained_prose` — `无明显意象重复` — If no object or image repeats, write “无明显意象重复.”
- `oh-story/Chinese-to-English/Ref - output-templates.md:299` — `unexplained_prose` — `主角名` — | {主角名} | {主人公/重要配角} | {主动型/被动型/转变型} | {情绪承载者/...} | {核心心理冲突} | {始→转→终} | "{最具代表性的台词}" |
- `oh-story/Chinese-to-English/Ref - output-templates.md:299` — `unexplained_prose` — `始` — | {主角名} | {主人公/重要配角} | {主动型/被动型/转变型} | {情绪承载者/...} | {核心心理冲突} | {始→转→终} | "{最具代表性的台词}" |
- `oh-story/Chinese-to-English/Ref - output-templates.md:299` — `unexplained_prose` — `核心心理冲突` — | {主角名} | {主人公/重要配角} | {主动型/被动型/转变型} | {情绪承载者/...} | {核心心理冲突} | {始→转→终} | "{最具代表性的台词}" |
- `oh-story/Chinese-to-English/Ref - output-templates.md:299` — `unexplained_prose` — `终` — | {主角名} | {主人公/重要配角} | {主动型/被动型/转变型} | {情绪承载者/...} | {核心心理冲突} | {始→转→终} | "{最具代表性的台词}" |
- `oh-story/Chinese-to-English/Ref - output-templates.md:300` — `unexplained_prose` — `台词` — | {配角名} | {重要配角/功能人物} | {主动型/被动型} | {压迫源/...} | {矛盾} | {弧线/扁平} | "{台词}" |
- `oh-story/Chinese-to-English/Ref - output-templates.md:300` — `unexplained_prose` — `矛盾` — | {配角名} | {重要配角/功能人物} | {主动型/被动型} | {压迫源/...} | {矛盾} | {弧线/扁平} | "{台词}" |
- `oh-story/Chinese-to-English/Ref - output-templates.md:300` — `unexplained_prose` — `配角名` — | {配角名} | {重要配角/功能人物} | {主动型/被动型} | {压迫源/...} | {矛盾} | {弧线/扁平} | "{台词}" |
- `oh-story/Chinese-to-English/Ref - output-templates.md:308` — `unexplained_prose` — `名` — | {名} | {高/中/低} | {承担N项功能} | {不可删/可删} | {每句都推动/部分推动} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:308` — `unexplained_prose` — `承担` — | {名} | {高/中/低} | {承担N项功能} | {不可删/可删} | {每句都推动/部分推动} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:308` — `unexplained_prose` — `项功能` — | {名} | {高/中/低} | {承担N项功能} | {不可删/可删} | {每句都推动/部分推动} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:314` — `unexplained_prose` — `制造了什么情绪` — | A ↔ B | {如：单向依附→对等拒绝} | {节N:状态A → 节M:状态B} | {制造了什么情绪} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:314` — `unexplained_prose` — `单向依附` — | A ↔ B | {如：单向依附→对等拒绝} | {节N:状态A → 节M:状态B} | {制造了什么情绪} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:314` — `unexplained_prose` — `如` — | A ↔ B | {如：单向依附→对等拒绝} | {节N:状态A → 节M:状态B} | {制造了什么情绪} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:314` — `unexplained_prose` — `对等拒绝` — | A ↔ B | {如：单向依附→对等拒绝} | {节N:状态A → 节M:状态B} | {制造了什么情绪} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:314` — `unexplained_prose` — `状态` — | A ↔ B | {如：单向依附→对等拒绝} | {节N:状态A → 节M:状态B} | {制造了什么情绪} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:314` — `unexplained_prose` — `节` — | A ↔ B | {如：单向依附→对等拒绝} | {节N:状态A → 节M:状态B} | {制造了什么情绪} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:328` — `unexplained_prose` — `绝对强度量表` — | Opening emotional intensity | {1-10，绝对强度量表，非情感曲线的-9~+9} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:328` — `unexplained_prose` — `非情感曲线的` — | Opening emotional intensity | {1-10，绝对强度量表，非情感曲线的-9~+9} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:337` — `unexplained_prose` — `读者离开时在想什么` — | Emotional landing | {读者离开时在想什么} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:339` — `unexplained_prose` — `为什么` — | Sharing impulse | {读者是否会推荐，为什么} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:339` — `unexplained_prose` — `读者是否会推荐` — | Sharing impulse | {读者是否会推荐，为什么} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:340` — `unexplained_prose` — `所有钩子是否回收` — | Completeness of resolution | {所有钩子是否回收，未回收的列出} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:340` — `unexplained_prose` — `未回收的列出` — | Completeness of resolution | {所有钩子是否回收，未回收的列出} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:348` — `unexplained_prose` — `元素` — | {元素} | {如：第1节"私生子而已"} | {如：结尾终身未娶} | {对比/反转/升级} | {形成闭环/制造遗憾} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:348` — `unexplained_prose` — `如` — | {元素} | {如：第1节"私生子而已"} | {如：结尾终身未娶} | {对比/反转/升级} | {形成闭环/制造遗憾} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:348` — `unexplained_prose` — `私生子而已` — | {元素} | {如：第1节"私生子而已"} | {如：结尾终身未娶} | {对比/反转/升级} | {形成闭环/制造遗憾} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:348` — `unexplained_prose` — `第` — | {元素} | {如：第1节"私生子而已"} | {如：结尾终身未娶} | {对比/反转/升级} | {形成闭环/制造遗憾} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:348` — `unexplained_prose` — `结尾终身未娶` — | {元素} | {如：第1节"私生子而已"} | {如：结尾终身未娶} | {对比/反转/升级} | {形成闭环/制造遗憾} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:348` — `unexplained_prose` — `节` — | {元素} | {如：第1节"私生子而已"} | {如：结尾终身未娶} | {对比/反转/升级} | {形成闭环/制造遗憾} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:356` — `unexplained_prose` — `如何回收` — | {描述} | {节N} | {悬念/冲突/信息差} | {节M} | {如何回收} | {已回收/留白/遗漏} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:356` — `unexplained_prose` — `描述` — | {描述} | {节N} | {悬念/冲突/信息差} | {节M} | {如何回收} | {已回收/留白/遗漏} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:356` — `unexplained_prose` — `节` — | {描述} | {节N} | {悬念/冲突/信息差} | {节M} | {如何回收} | {已回收/留白/遗漏} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:370` — `unexplained_prose` — `具体说明` — | Opening appeal | 1-5 | {具体说明：钩子类型+效果+改进空间} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:370` — `unexplained_prose` — `改进空间` — | Opening appeal | 1-5 | {具体说明：钩子类型+效果+改进空间} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:370` — `unexplained_prose` — `效果` — | Opening appeal | 1-5 | {具体说明：钩子类型+效果+改进空间} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:370` — `unexplained_prose` — `钩子类型` — | Opening appeal | 1-5 | {具体说明：钩子类型+效果+改进空间} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:371` — `unexplained_prose` — `具体说明` — | Emotional push and pull | 1-5 | {具体说明：曲线形态+极值+翻转} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:371` — `unexplained_prose` — `曲线形态` — | Emotional push and pull | 1-5 | {具体说明：曲线形态+极值+翻转} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:371` — `unexplained_prose` — `极值` — | Emotional push and pull | 1-5 | {具体说明：曲线形态+极值+翻转} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:371` — `unexplained_prose` — `翻转` — | Emotional push and pull | 1-5 | {具体说明：曲线形态+极值+翻转} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:372` — `unexplained_prose` — `具体说明` — | Reversal design | 1-5 | {具体说明：反转类型+铺垫质量+合理性} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:372` — `unexplained_prose` — `反转类型` — | Reversal design | 1-5 | {具体说明：反转类型+铺垫质量+合理性} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:372` — `unexplained_prose` — `合理性` — | Reversal design | 1-5 | {具体说明：反转类型+铺垫质量+合理性} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:372` — `unexplained_prose` — `铺垫质量` — | Reversal design | 1-5 | {具体说明：反转类型+铺垫质量+合理性} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:373` — `unexplained_prose` — `具体说明` — | Pacing control | 1-5 | {具体说明：密度分布+异常检测+节奏匹配} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:373` — `unexplained_prose` — `密度分布` — | Pacing control | 1-5 | {具体说明：密度分布+异常检测+节奏匹配} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:373` — `unexplained_prose` — `异常检测` — | Pacing control | 1-5 | {具体说明：密度分布+异常检测+节奏匹配} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:373` — `unexplained_prose` — `节奏匹配` — | Pacing control | 1-5 | {具体说明：密度分布+异常检测+节奏匹配} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:374` — `unexplained_prose` — `传播欲` — | Ending aftertaste | 1-5 | {具体说明：结尾类型+落点+传播欲} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:374` — `unexplained_prose` — `具体说明` — | Ending aftertaste | 1-5 | {具体说明：结尾类型+落点+传播欲} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:374` — `unexplained_prose` — `结尾类型` — | Ending aftertaste | 1-5 | {具体说明：结尾类型+落点+传播欲} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:374` — `unexplained_prose` — `落点` — | Ending aftertaste | 1-5 | {具体说明：结尾类型+落点+传播欲} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:378` — `unexplained_prose` — `传播性如何` — {核心爆点是什么？铺垫是否充分？释放是否到位？传播性如何？}
- `oh-story/Chinese-to-English/Ref - output-templates.md:378` — `unexplained_prose` — `核心爆点是什么` — {核心爆点是什么？铺垫是否充分？释放是否到位？传播性如何？}
- `oh-story/Chinese-to-English/Ref - output-templates.md:378` — `unexplained_prose` — `释放是否到位` — {核心爆点是什么？铺垫是否充分？释放是否到位？传播性如何？}
- `oh-story/Chinese-to-English/Ref - output-templates.md:378` — `unexplained_prose` — `铺垫是否充分` — {核心爆点是什么？铺垫是否充分？释放是否到位？传播性如何？}
- `oh-story/Chinese-to-English/Ref - output-templates.md:382` — `unexplained_prose` — `争议点` — {读者会讨论什么？争议点？代入式自省？"如果是我会怎样"的讨论空间？}
- `oh-story/Chinese-to-English/Ref - output-templates.md:382` — `unexplained_prose` — `代入式自省` — {读者会讨论什么？争议点？代入式自省？"如果是我会怎样"的讨论空间？}
- `oh-story/Chinese-to-English/Ref - output-templates.md:382` — `unexplained_prose` — `如果是我会怎样` — {读者会讨论什么？争议点？代入式自省？"如果是我会怎样"的讨论空间？}
- `oh-story/Chinese-to-English/Ref - output-templates.md:382` — `unexplained_prose` — `的讨论空间` — {读者会讨论什么？争议点？代入式自省？"如果是我会怎样"的讨论空间？}
- `oh-story/Chinese-to-English/Ref - output-templates.md:382` — `unexplained_prose` — `读者会讨论什么` — {读者会讨论什么？争议点？代入式自省？"如果是我会怎样"的讨论空间？}
- `oh-story/Chinese-to-English/Ref - output-templates.md:388` — `unexplained_prose` — `具体触发点` — | Emotional resonance | {强/中/弱/无} | {具体触发点} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:390` — `unexplained_prose` — `具体触发点` — | Experiential resonance | {强/中/弱/无} | {具体触发点} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:391` — `unexplained_prose` — `具体触发点` — | Social-phenomenon resonance | {强/中/弱/无} | {具体触发点} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:392` — `unexplained_prose` — `具体触发点` — | Cultural resonance | {强/中/弱/无} | {具体触发点} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:394` — `unexplained_prose` — `具体触发点` — | Philosophical resonance | {强/中/弱/无} | {具体触发点} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:395` — `unexplained_prose` — `具体触发点` — | Deep emotional resonance | {强/中/弱/无} | {具体触发点} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:396` — `unexplained_prose` — `具体触发点` — | Deep character resonance | {强/中/弱/无} | {具体触发点} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:416` — `unexplained_prose` — `文本分布与真实状态变化` — | Event density | {X个/千字} | {文本分布与真实状态变化} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:418` — `unexplained_prose` — `直接冲突与其他压力来源的关系` — | Conflict density | {Z%} | {直接冲突与其他压力来源的关系} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:445` — `unexplained_prose` — `压缩弹簧` — | Emotional-curve shape | {如：压缩弹簧} | {如：V形} | {如：波浪} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:445` — `unexplained_prose` — `如` — | Emotional-curve shape | {如：压缩弹簧} | {如：V形} | {如：波浪} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:445` — `unexplained_prose` — `形` — | Emotional-curve shape | {如：压缩弹簧} | {如：V形} | {如：波浪} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:445` — `unexplained_prose` — `波浪` — | Emotional-curve shape | {如：压缩弹簧} | {如：V形} | {如：波浪} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:446` — `unexplained_prose` — `信息差` — | Core technique | {如：假死+信息差} | {如：时间线反转} | {如：套娃反转} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:446` — `unexplained_prose` — `假死` — | Core technique | {如：假死+信息差} | {如：时间线反转} | {如：套娃反转} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:446` — `unexplained_prose` — `套娃反转` — | Core technique | {如：假死+信息差} | {如：时间线反转} | {如：套娃反转} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:446` — `unexplained_prose` — `如` — | Core technique | {如：假死+信息差} | {如：时间线反转} | {如：套娃反转} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:446` — `unexplained_prose` — `时间线反转` — | Core technique | {如：假死+信息差} | {如：时间线反转} | {如：套娃反转} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:461` — `unexplained_prose` — `原因` — | Zhihu Salt Selection | {高/中/低} | {原因} | {如有} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:461` — `unexplained_prose` — `如有` — | Zhihu Salt Selection | {高/中/低} | {原因} | {如有} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:462` — `unexplained_prose` — `原因` — | Fanqie Short Stories | {高/中/低} | {原因} | {如有} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:462` — `unexplained_prose` — `如有` — | Fanqie Short Stories | {高/中/低} | {原因} | {如有} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:463` — `unexplained_prose` — `原因` — | Qimao Short Stories | {高/中/低} | {原因} | {如有} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:463` — `unexplained_prose` — `如有` — | Qimao Short Stories | {高/中/低} | {原因} | {如有} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:477` — `unexplained_prose` — `文本分布与真实状态变化` — | Event density | {N}个/千字 | {文本分布与真实状态变化} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:480` — `unexplained_prose` — `读者模型变化与消化效果` — | Information density | {X%} | {读者模型变化与消化效果} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:492` — `unexplained_prose` — `具体说明` — | {节奏塌陷/压力过载/信息洪峰/对白失效/对白挤压场景/反转过载} | {节N} | {具体说明} |
- `oh-story/Chinese-to-English/Ref - output-templates.md:494` — `unexplained_prose` — `节奏无明显异常` — If none exist, write “节奏无明显异常.”
- `oh-story/Chinese-to-English/Ref - output-templates.md:524` — `unexplained_prose` — `无` — - [ ] Every node has a hook type, including “无” `[WARN]`
- `oh-story/Chinese-to-English/Ref - plot-special-topics.md:19` — `unresolved_anchor` — `#ranking-scans-and-book-deconstruction` — | Need market research / competitor deconstruction | [Rankings Scans and Book Deconstruction](#ranking-scans-and-book-deconstruction) |
- `oh-story/Chinese-to-English/Ref - structure-mapping-long.md:59` — `unexplained_prose` — `觉醒` — | Number only + title | 1. 觉醒 |
- `oh-story/Chinese-to-English/Ref - structure-mapping-long.md:316` — `unexplained_prose` — `天元三年春` — | Explicit date | "天元三年春" | Record directly |
- `oh-story/Chinese-to-English/Ref - structure-mapping-long.md:317` — `unexplained_prose` — `三日后` — | Relative time | "三日后", "半月后" | Calculate absolute time |
- `oh-story/Chinese-to-English/Ref - structure-mapping-long.md:317` — `unexplained_prose` — `半月后` — | Relative time | "三日后", "半月后" | Calculate absolute time |
- `oh-story/Chinese-to-English/Ref - structure-mapping-long.md:318` — `unexplained_prose` — `次日` — | Interval between events | "翌日", "次日" | Mark as consecutive |
- `oh-story/Chinese-to-English/Ref - structure-mapping-long.md:318` — `unexplained_prose` — `翌日` — | Interval between events | "翌日", "次日" | Mark as consecutive |
- `oh-story/Chinese-to-English/Ref - structure-mapping-long.md:319` — `unexplained_prose` — `入冬` — | Seasonal marker | "入冬", "春暖花开" | Infer the season |
- `oh-story/Chinese-to-English/Ref - structure-mapping-long.md:319` — `unexplained_prose` — `春暖花开` — | Seasonal marker | "入冬", "春暖花开" | Infer the season |
- `oh-story/Chinese-to-English/Ref - style-craft.md:93` — `unexplained_prose` — `了` — | Overuse of the Chinese aspect particle “了” | Control unnecessary use of “了” |
- `oh-story/Chinese-to-English/Ref - style-profile-protocol.md:82` — `unexplained_prose` — `字原文` — {300-500 字原文}
- `oh-story/Chinese-to-English/Ref - style-profile-protocol.md:90` — `unexplained_prose` — `字原文` — {300-500 字原文}
- `oh-story/Chinese-to-English/Ref - style-profile-protocol.md:98` — `unexplained_prose` — `字原文` — {300-500 字原文}
- `oh-story/Chinese-to-English/Ref - style-profile-protocol.md:106` — `unexplained_prose` — `字原文` — {300-500 字原文}
- `oh-story/Chinese-to-English/SKILL - story-deslop.md:67` — `unexplained_prose` — `嘤` — | Interjections | “嘤,” “嘶,” “靠,” “行吧” | Almost none |
- `oh-story/Chinese-to-English/SKILL - story-deslop.md:67` — `unexplained_prose` — `嘶` — | Interjections | “嘤,” “嘶,” “靠,” “行吧” | Almost none |
- `oh-story/Chinese-to-English/SKILL - story-deslop.md:67` — `unexplained_prose` — `行吧` — | Interjections | “嘤,” “嘶,” “靠,” “行吧” | Almost none |
- `oh-story/Chinese-to-English/SKILL - story-deslop.md:67` — `unexplained_prose` — `靠` — | Interjections | “嘤,” “嘶,” “靠,” “行吧” | Almost none |
- `oh-story/Chinese-to-English/SKILL - story-deslop.md:278` — `unexplained_prose` — `他拿起笔` — - ❌ “他拿起笔。手在抖。笔尖又停住。”
- `oh-story/Chinese-to-English/SKILL - story-deslop.md:278` — `unexplained_prose` — `手在抖` — - ❌ “他拿起笔。手在抖。笔尖又停住。”
- `oh-story/Chinese-to-English/SKILL - story-deslop.md:278` — `unexplained_prose` — `笔尖又停住` — - ❌ “他拿起笔。手在抖。笔尖又停住。”
- `oh-story/Chinese-to-English/SKILL - story-deslop.md:279` — `unexplained_prose` — `他拿起笔` — - ✅ “他拿起笔，笔尖刚碰到纸就偏了，手腕压了两次都没压稳。”
- `oh-story/Chinese-to-English/SKILL - story-deslop.md:279` — `unexplained_prose` — `手腕压了两次都没压稳` — - ✅ “他拿起笔，笔尖刚碰到纸就偏了，手腕压了两次都没压稳。”
- `oh-story/Chinese-to-English/SKILL - story-deslop.md:279` — `unexplained_prose` — `笔尖刚碰到纸就偏了` — - ✅ “他拿起笔，笔尖刚碰到纸就偏了，手腕压了两次都没压稳。”
- `oh-story/Chinese-to-English/SKILL - story-deslop.md:285` — `unexplained_prose` — `兴高采烈地笑着跑过来` — | Repeated adjective | “兴高采烈地笑着跑过来” | “笑着跑过来” |
- `oh-story/Chinese-to-English/SKILL - story-deslop.md:285` — `unexplained_prose` — `笑着跑过来` — | Repeated adjective | “兴高采烈地笑着跑过来” | “笑着跑过来” |
- `oh-story/Chinese-to-English/SKILL - story-deslop.md:286` — `unexplained_prose` — `关键问题` — | Synonym repetition | “非常重要的关键问题” | “关键问题” |
- `oh-story/Chinese-to-English/SKILL - story-deslop.md:286` — `unexplained_prose` — `非常重要的关键问题` — | Synonym repetition | “非常重要的关键问题” | “关键问题” |
- `oh-story/Chinese-to-English/SKILL - story-deslop.md:287` — `unexplained_prose` — `我好饿` — | Repeated meaning | “我好饿，肚子咕咕叫” | “我好饿” |
- `oh-story/Chinese-to-English/SKILL - story-deslop.md:287` — `unexplained_prose` — `肚子咕咕叫` — | Repeated meaning | “我好饿，肚子咕咕叫” | “我好饿” |
- `oh-story/Chinese-to-English/SKILL - story-deslop.md:330` — `unexplained_prose` — `他知道` — - If an ending contains “他知道...” or “这一刻...,” it can usually be deleted
- `oh-story/Chinese-to-English/SKILL - story-deslop.md:330` — `unexplained_prose` — `这一刻` — - If an ending contains “他知道...” or “这一刻...,” it can usually be deleted
- `oh-story/Chinese-to-English/SKILL - story-long-analyze.md:169` — `unexplained_prose` — `生成记录` — If source text is missing or chapter separators cannot be identified, write `文风可用：否：{原因}` under “生成记录” in `文风.md`. A Stage 6 failure does not block the pipeline.
- `oh-story/Chinese-to-English/SKILL - story-setup.md:266` — `unexplained_prose` — `个` — - Low: “未检测到低成本模型，这 3 个 agent 将使用主模型，成本可能较高”
- `oh-story/Chinese-to-English/SKILL - story-setup.md:266` — `unexplained_prose` — `将使用主模型` — - Low: “未检测到低成本模型，这 3 个 agent 将使用主模型，成本可能较高”
- `oh-story/Chinese-to-English/SKILL - story-setup.md:266` — `unexplained_prose` — `成本可能较高` — - Low: “未检测到低成本模型，这 3 个 agent 将使用主模型，成本可能较高”
- `oh-story/Chinese-to-English/SKILL - story-setup.md:266` — `unexplained_prose` — `未检测到低成本模型` — - Low: “未检测到低成本模型，这 3 个 agent 将使用主模型，成本可能较高”
- `oh-story/Chinese-to-English/SKILL - story-setup.md:266` — `unexplained_prose` — `这` — - Low: “未检测到低成本模型，这 3 个 agent 将使用主模型，成本可能较高”
- `oh-story/Chinese-to-English/SKILL - story-setup.md:268` — `unexplained_prose` — `将使用主模型` — - High: “未检测到高端模型，story-architect 将使用主模型”
- `oh-story/Chinese-to-English/SKILL - story-setup.md:268` — `unexplained_prose` — `未检测到高端模型` — - High: “未检测到高端模型，story-architect 将使用主模型”
- `oh-story/Chinese-to-English/SKILL - story-setup.md:486` — `unexplained_prose` — `作者` — | `{作者名}` | Pen name or nickname | Use “作者” when unspecified |
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:90` — `unexplained_prose` — `信息差` — >      "technique": "铺垫后置|反应层放大|信息差|对比锚点|延迟揭示|身体反应|小目标嵌套|其他",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:90` — `unexplained_prose` — `其他` — >      "technique": "铺垫后置|反应层放大|信息差|对比锚点|延迟揭示|身体反应|小目标嵌套|其他",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:90` — `unexplained_prose` — `反应层放大` — >      "technique": "铺垫后置|反应层放大|信息差|对比锚点|延迟揭示|身体反应|小目标嵌套|其他",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:90` — `unexplained_prose` — `对比锚点` — >      "technique": "铺垫后置|反应层放大|信息差|对比锚点|延迟揭示|身体反应|小目标嵌套|其他",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:90` — `unexplained_prose` — `小目标嵌套` — >      "technique": "铺垫后置|反应层放大|信息差|对比锚点|延迟揭示|身体反应|小目标嵌套|其他",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:90` — `unexplained_prose` — `延迟揭示` — >      "technique": "铺垫后置|反应层放大|信息差|对比锚点|延迟揭示|身体反应|小目标嵌套|其他",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:90` — `unexplained_prose` — `身体反应` — >      "technique": "铺垫后置|反应层放大|信息差|对比锚点|延迟揭示|身体反应|小目标嵌套|其他",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:90` — `unexplained_prose` — `铺垫后置` — >      "technique": "铺垫后置|反应层放大|信息差|对比锚点|延迟揭示|身体反应|小目标嵌套|其他",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:91` — `unexplained_prose` — `其他` — >      "reader_effect": "好奇|期待|压抑|爽|心疼|紧张|甜|热血|其他",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:91` — `unexplained_prose` — `压抑` — >      "reader_effect": "好奇|期待|压抑|爽|心疼|紧张|甜|热血|其他",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:91` — `unexplained_prose` — `好奇` — >      "reader_effect": "好奇|期待|压抑|爽|心疼|紧张|甜|热血|其他",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:91` — `unexplained_prose` — `心疼` — >      "reader_effect": "好奇|期待|压抑|爽|心疼|紧张|甜|热血|其他",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:91` — `unexplained_prose` — `期待` — >      "reader_effect": "好奇|期待|压抑|爽|心疼|紧张|甜|热血|其他",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:91` — `unexplained_prose` — `热血` — >      "reader_effect": "好奇|期待|压抑|爽|心疼|紧张|甜|热血|其他",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:91` — `unexplained_prose` — `爽` — >      "reader_effect": "好奇|期待|压抑|爽|心疼|紧张|甜|热血|其他",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:91` — `unexplained_prose` — `甜` — >      "reader_effect": "好奇|期待|压抑|爽|心疼|紧张|甜|热血|其他",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:91` — `unexplained_prose` — `紧张` — >      "reader_effect": "好奇|期待|压抑|爽|心疼|紧张|甜|热血|其他",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:95` — `unexplained_prose` — `合` — >     "emotion_flow": {"start": "<起>", "build": "<承>", "turn": "<转>", "close": "<合>"},
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:95` — `unexplained_prose` — `承` — >     "emotion_flow": {"start": "<起>", "build": "<承>", "turn": "<转>", "close": "<合>"},
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:95` — `unexplained_prose` — `起` — >     "emotion_flow": {"start": "<起>", "build": "<承>", "turn": "<转>", "close": "<合>"},
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:95` — `unexplained_prose` — `转` — >     "emotion_flow": {"start": "<起>", "build": "<承>", "turn": "<转>", "close": "<合>"},
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:97` — `unexplained_prose` — `动作` — >     "structure_formula": ["<节点1动作（目的）>", "<节点2动作（目的）>"],
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:97` — `unexplained_prose` — `目的` — >     "structure_formula": ["<节点1动作（目的）>", "<节点2动作（目的）>"],
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:97` — `unexplained_prose` — `节点` — >     "structure_formula": ["<节点1动作（目的）>", "<节点2动作（目的）>"],
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:98` — `unexplained_prose` — `一句话结构手法` — >     "core_technique": "<一句话结构手法>",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:106` — `unexplained_prose` — `不与` — >     {"id": "P<integer>", "title": "<string, ≤15 字短标签，不与 event 同句>",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:106` — `unexplained_prose` — `同句` — >     {"id": "P<integer>", "title": "<string, ≤15 字短标签，不与 event 同句>",
- `oh-story/Chinese-to-English/Templates - chapter-extractor.md:106` — `unexplained_prose` — `字短标签` — >     {"id": "P<integer>", "title": "<string, ≤15 字短标签，不与 event 同句>",
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
- `oh-story/Chinese-to-English/Ref - topic-decision.md:94` — deprecated `Ranking scans` → `rankings scan`
- `oh-story/Chinese-to-English/SKILL - story-long-scan.md:311` — deprecated `Ranking scan` → `rankings scan`

## Review contract

- Protected literals are retained because changing them would alter source-compatible paths, fields, assets, anchors, schemas, or identifiers.
- Operational Chinese outputs are retained only where the surrounding structured instruction establishes that the literal value is consumed or emitted by the workflow.
- Proper names/titles are retained for identity and provenance.
- Intentional bilingual examples are retained only in explicitly quoted/demo/trigger/example contexts.
- Any occurrence not matched by those narrow rules remains `unexplained_prose` and blocks acceptance.
