# Rules and Routing Index

This file does only two things: routes each decision type to the **responsible skill**, and defines rule levels and conflict priority.
It does not duplicate rule text. Each skill's preflight checks, ownership boundaries, form inputs, and complete rule table live in that skill's
own `references/stage-contract.md`. The core does not decide which reference a child skill should read.

## Table of Contents

- [Topic-Authority Routing](#主题权威路由)
- [Rule Levels](#规则分级)
- [Conflict Priority](#冲突优先级)

## Topic-Authority Routing

After routing, the skill loads its own references. “Out-of-scope boundary” identifies what that skill **must not** cross.

| Topic | Responsible skill | When to read | Out-of-scope boundary |
|---|---|---|---|
| Long-form source slicing and chapter-by-chapter function extraction | `$short-drama-novel-analyze` | Importing a novel, serial, or scattered multi-episode draft that needs a traceable analysis layer | Does not write an adaptation contract or episode map; does not create assets |
| Sampled triage of whether a book is worth analyzing | `$short-drama-novel-analyze` | Before full analysis, judge adaptation density and risk from a sample | Conclusions are limited to the sample; does not create candidate-episode entries |
| Adaptation value and episode candidates | `$short-drama-novel-analyze` | Determine which units work onscreen and divide candidates by dramatic outcome | Candidates are not decisions; the creator and develop determine episode count |
| Story promise and conflict engine | `$short-drama-develop` | Build sustainable pressure and payoff from an idea | Does not generate plot directly from genre terms |
| Episode contract and ending handoff | `$short-drama-develop` | Plan entry state, local outcome, and outgoing pressure | Does not replace screenplay scene execution |
| Repeated mechanism and exhaustion within a unit | `$short-drama-develop` | A story unit repeatedly pays off through the same mechanism, or the middle begins repeating and thinning | Does not prescribe run count or replacement point; does not decide how an episode is written |
| Episode-capacity feasibility | `$short-drama-develop` | Estimate the magnitude of shots and duration per episode before scene realization | Uses project-specific proportions, not cross-project thresholds; does not block delivery |
| Serialized characters and recovery memory | `$short-drama-develop` | Character strategy, information permissions, and setup debt are substantial across episodes | A single-scene task need not create complete memory |
| Long-material adaptation | `$short-drama-develop` | Compress, merge, or convert exposition into an onscreen carrier | Does not copy source sentences or style into the new screenplay |
| Genre conditions and hooks | `$short-drama-develop` | Compare genre approaches by pressure mechanism | Does not treat example beats, numbers, or labels as formulas |
| Single-genre execution details | `$short-drama-develop` | Genre is established and must be realized at scene-level granularity | Read one card at a time; cards do not create blocking constraints |
| Premise devices (foreknowledge or external authorization) | `$short-drama-develop` | The protagonist begins with a known outcome or receives abilities from an external rule system | The device layers over genre; it does not replace the genre card or create a new genre |
| Single-form execution details | `$short-drama` | Production form is established and one form card must be located from the table | Read one card at a time; form does not rewrite identity or geography |
| Look Development and style frames | `$short-drama` | Convert visual direction into observable rules for characters, locations, and a representative high-pressure frame | `$short-drama-image-prompts` only projects prompts; style does not take ownership of identity, geography, or plot |
| Scenes and performable action | `$short-drama-write` | Realize episode beats as scenes | Does not determine storyboard shot sizes or camera movement |
| Dialogue action and character voice | `$short-drama-write` | Write, revise, or diagnose dialogue | Does not judge power from line length or catchphrase count |
| Legibility in multi-character scenes and protagonist-absent scenes | `$short-drama-write` | A scene contains too many people to tell who is contending with whom, or a scene/episode omits the protagonist | Does not determine blocking, shot size, or cuts; those belong to storyboarding |
| Scene sound dramaturgy | `$short-drama-write` | Sound source, silence, or a sound bridge carries story information and pressure | Does not replace shot-by-shot implementation or mixing; does not let music replace performance |
| Screenplay production tags | `$short-drama-write` | Normalize dialogue, actions, VO/OS, text, and continuity | Does not use formatting to invent plot |
| Finite action units and exact deadlines | `$short-drama-write` | The task explicitly supplies verifiable counts, rounds, beats, or a literal deadline | Checks against completion states and the task's agreement; does not upgrade qualitative pressure into numbers or add count structures |
| Asset-appearance evidence | `$short-drama-assets` | Extract characters, locations, props, and states from a screenplay | Does not create assets directly from noun/name matching |
| Identity, variants, and reuse | `$short-drama-assets` | Decide reuse, new variant, new identity, or unresolved | Camera angle is normally not an asset variant |
| Real brands and entities inherited from a source | `$short-drama-assets` | The screenplay retains a source proper noun referring to a real brand, trademark, institution, or person | Does not judge compliance, issue prohibitions, or maintain a list; passes the choice to the creator and records it |
| Asset image prompts | `$short-drama-image-prompts` | Project accepted assets into visible single-frame specifications | Does not carry sequential plot action |
| Location-board lighting and consistency across Views | `$short-drama-image-prompts` | One location is divided into multiple viewing directions whose boards will be intercut | Backlighting/shadow differences caused by direction need not be flattened |
| Targeted image-prompt modification | `$short-drama-image-prompts` | Modify a local detail while freezing the preserve set | Does not disguise a full-image rewrite as a local edit |
| Shot purpose and coverage | `$short-drama-storyboard` | Build motivated shots from the screenplay | Does not force shot splits merely for shot-size variety |
| Scene visual plans and Coverage Audition | `$short-drama-storyboard` | A key scene needs comparison of audience position, information timing, space, camera, and sound movement first | Optional intermediate layer; does not own screenplay facts or shot boundaries and does not prescribe grid/shot count |
| Frozen keyframes | `$short-drama-storyboard` | Write a freezable instant at the shot's starting point | Does not write an action chain or shot endpoint |
| Motion-comic keyframe visual lexicon | `$short-drama-storyboard` | Visual direction is accepted as motion-comic/2D-comic form and shared style plus current readability constraints must be projected consistently into keyframes | Every item is a `taste_option`; no quality threshold, and no replacement of identity, geography, or boundary facts |
| Multi-character blocking and delivery-surface occlusion | `$short-drama-storyboard` | Multi-person, crowd, evidence-reveal, or moving-object scenes, or a vertical delivery surface adds occlusion | Does not reuse one layout across all genres; occlusion zones come from the declared delivery profile, not a universal safe frame |
| Video motion specifications | `$short-drama-video-prompts` | Express accepted shot boundaries as changes over time | Does not change shot, asset, or screenplay authority |
| Delivery containers and segment arithmetic | `$short-drama-video-prompts` | The project declares segmented delivery or packaging multiple shots | Packaging does not rewrite shot boundaries or reviewability |
| Delivery routing and execution trigger phrases | `$short-drama-video-prompts` | The project declares routing beyond per-shot delivery, or a route requires fixed wording | Trigger phrases and routing come from creator profiles; the suite does not invent language, and continuation does not create a second starting-point authority |
| Performance action and duration | `$short-drama-video-prompts` | Action, dialogue, and landing point may be overloaded | Does not impose a universal actions-per-second threshold |
| Camera, sound, and adjacent boundaries | `$short-drama-video-prompts` | Write camera movement, environmental motion, lip sync, or sound direction | Does not add unsourced music/events |
| Target-executor capability profile | `$short-drama-video-prompts` | Executor duration, reference method, same-track audio, or length limit changes prompt wording | Capabilities are creator-declared, not inferred; does not embed model lists or rewrite accepted boundaries for convergence |
| Cross-scene and cross-shot continuity | `$short-drama-assets` | State changes pass to the next scene/shot/episode | Does not copy the entire specification set into every shot |
| Locking visible facts across shots | `$short-drama-assets` | Clothing or prop color/material drifts across shots beyond reference-image control | Locks invariant facts, not state, pose, or shot transients; the lock phrase does not choose colors for the creator |
| Production-form translation | `$short-drama` | Project live action, 2D, 3D, ink-wash, or another direction into each stage | A style name or model code is not a production decision |
| Independent evidence review | `$short-drama-review` | After freezing the target, write findings and a verdict | Reviewer does not edit owner sources |
| Project production observation and calibration | `$short-drama-review` | Authorized textual observations exist and must be located to an exact prompt/spec/reference/configuration | Valid only for the current project and versions; unobserved results remain unknown |
| Result-disposition judgment | `$short-drama-review` | A diagnosis exists and a decision is needed among keeping, post-production, local edit, resubmission, or rewrite | Disposition precedes revision; resubmitting identical text or appending adjectives is not a fix |
| Templated-writing diagnosis | `$short-drama-review` | Isomorphic mechanisms or expressive loss appears in at least two locations | Does not convict based on banned words or a one-time genre convention |

## Rule Levels

| Level | Meaning | Who decides |
|---|---|---|
| `structural_invariant` | Locally provable reference, ID, arithmetic, or explicit-state contradiction | Validator may block |
| `reviewed_invariant` | Semantic obligation requiring cited evidence and judgment | Reviewer |
| `craft_default` | Practice that usually helps | Creator may override with an explanation |
| `taste_option` | Creator's expressive choice | Must not block delivery by itself |

## Conflict Priority

```text
创作者已接受的事实、结局承诺与改编边界
→ 已接受的单集契约、进入/出去状态与铺垫兑现义务
→ 各技能 stage-contract 中的规则表
→ 题材卡、形态卡与通用叙事手感
```

**English guide (non-executable):** Creator-accepted facts, ending promises, and adaptation boundaries → the accepted episode contract, entry and exit states, and setup/payoff obligations → each skill's `stage-contract` rule table → genre cards, format cards, and transferable narrative feel.

Rule IDs use stable prefixes: `STY` development, `SCR` screenplay, `AST` assets, `IMG` image prompts,
`SHT` storyboard/keyframes, `VID` video prompts, `CON` continuity, and `REV` review. IDs are unique across the suite.
The skill owning a prefix maintains its rule text; the core no longer duplicates it. `CON` is shared by assets, storyboards, and video prompts,
and all three stage contracts list the same entries.
