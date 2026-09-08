# Genre Prose-Prompt Card Index

> This document defines only **indexing and recall rules**. Each genre's prose-prompt card is stored separately under `genre-prose-cards/` in the same directory.

---

## Usage Principles

Manuscript writing uses three components: **general manuscript requirements + one genre prose-prompt card + this book's prose style**.

- Maintain only one set of general manuscript requirements: strictly consume the detailed outline, write to plot-point obligations, advance slowly, never write later plot prematurely, and finish with deterministic word-count, hook, banned-word, and degradation checks.
- A genre card governs only stable genre-level essentials: world/life logic, reader expectations, core gratification/emotion, common scenes, common hooks, and prohibited drift.
- This book's prose style governs only sentence length, punctuation, subtext, anchor passages, and tone. It does not override the genre card or `剧情/情绪模块.md` / `剧情/节奏.md`.
- When the three conflict: chapter detailed outline and continuity > authoritative emotion/rhythm recall > genre card > this book's prose style > general techniques.

## Recall Rules

1. Read `设定/题材定位.md` first and confirm the primary genre, target platform, audience channel, primary benchmark book, and core premise.
2. Match the genre in this index, then read only the single card `genre-prose-cards/{题材}.md` from the same directory. Do not load the entire card set into the prompt.
3. For cross-genre work, read one complete primary-genre card; read one secondary-genre card but extract only 1–2 “common scene/prohibited drift” entries. Do not stack two complete pacing systems in parallel.
4. A high-confidence card may feed Phase 2 `设定/题材正文提示卡.md` directly. Compare a medium-confidence card with this book's benchmark/detailed outline. A low-confidence card is fallback only; label it low-confidence and prioritize adding a same-genre benchmark.
5. The `genre_prose_card` passed to narrative-writer for each chapter retains only chapter-relevant entries, preferably 120–300 Chinese characters: genre constraints, core logic, reader expectations, core gratification/emotion, prose realization, early/middle/late strategy, scene granularity, prohibited drift, chapter-specific choices, and card confidence.
6. **Genre cards calibrate genre flavor internally for the writer and must never appear in the manuscript**. The manuscript must not mention card names, genre labels, confidence, entry numbers, or “evidence summary” data. It must not include compliance self-assessments or process commentary such as “followed the genre card / met the word count / zero violations.” Output only the story.

## Principles for Writing Genre Cards

Every genre card must answer nine questions: genre core, main-line goal, conflict engine, gratification position, common emotional transformation, scene granularity, prose realization, early/middle/late strategy, and prohibited drift. The “urban slice-of-life” model may be used as a reference: establish a clear life goal; explain how low-intensity conflict creates real consequences; ground the opening, conflict, and ending in specific objects and scenes; and finally state which gratification beats are small but visible changes. Do not force one general methodology onto every genre.

## Do Not Turn These into Hard Rules

The local long-form sample does not support mechanical templates such as a fixed 50–60-character line width, a fixed 50%–60% dialogue share, global replacement of “地/得/很/像/顿号,” random inversion, three amines/eight emotions, or three reversals/four shocks. A genre card states only the scenes and emotional destinations more common to that genre; individual paragraphs still follow the detailed outline, prose style, and current scene.

---

## High-Confidence Genre Cards

| Genre card | Common aliases/match terms | Confidence |
|---|---|---|
| [Urban High-Concept](genre-prose-cards/都市脑洞.md) | Urban system / advice-following fiction / rule rewards / slice-of-life high concept | High |
| [Wealthy CEO Romance](genre-prose-cards/豪门总裁.md) | Dominant CEO / Beijing elite circle / marriage before love / contract marriage | High |
| [Dual Male Leads](genre-prose-cards/双男主.md) | Pure love / BL / danmei | High |
| [Urban Slice of Life](genre-prose-cards/都市日常.md) | Slice of life / urban life / warm daily life | High |
| [Urban High Martial Arts](genre-prose-cards/都市高武.md) | High martial arts / spiritual-energy revival / sequences / urban abilities | High |
| [Period Fiction](genre-prose-cards/年代.md) | Period fiction / 1970s / 1980s / military-family relocation / period rebirth | High |
| [Fantasy High-Concept](genre-prose-cards/玄幻脑洞.md) | Fantasy system / anti-trope fantasy / many children, much fortune / attribute fantasy | High |
| [War-God Son-in-Law](genre-prose-cards/战神赘婿.md) | Live-in son-in-law / war god returns / hidden identity | High |
| [Traditional Fantasy](genre-prose-cards/传统玄幻.md) | Fantasy / Eastern fantasy / general xianxia-fantasy | High |
| [Historical Social Realism](genre-prose-cards/古风世情.md) | Historical social realism / historical household / historical marriage realism | High |
| [Women's Farming Fiction](genre-prose-cards/女频种田.md) | Historical farming / farming commerce / farming with children | High |
| [Workplace Marriage and Romance](genre-prose-cards/职场婚恋.md) | Workplace romance / urban marriage / mature romance | High |
| [Science-Fiction Apocalypse](genre-prose-cards/科幻末世.md) | Apocalypse / catastrophe / wasteland / apocalypse stockpiling | High |
| [Urban Cultivation](genre-prose-cards/都市修真.md) | Urban immortality / urban immortal sovereign / modern cultivation | High |
| [Historical/Ancient](genre-prose-cards/历史古代.md) | Alternate history / historical political intrigue / imperial court | High |
| [Historical-Romance High-Concept](genre-prose-cards/古言脑洞.md) | Historical-romance high concept / book-transmigration historical romance / system historical romance | High |
| [Women's Suspense](genre-prose-cards/女频悬疑.md) | Female-led suspense / suspense romance / heroine detective | High |
| [Palace and Household Intrigue](genre-prose-cards/宫斗宅斗.md) | Palace intrigue / household intrigue / inner household / political historical romance | High |
| [Supernatural Suspense](genre-prose-cards/悬疑灵异.md) | Supernatural / thriller / strange tales / folklore suspense | High |
| [War of Resistance/Espionage](genre-prose-cards/抗战谍战.md) | Espionage / Republican-era espionage / agents | High |
| [Entertainment Stardom](genre-prose-cards/星光璀璨.md) | Entertainment industry / popular entertainment / best actress / variety shows | High |
| [Fantasy Romance](genre-prose-cards/玄幻言情.md) | Women's fantasy / xianxia romance / goddess | High |
| [Urban Farming](genre-prose-cards/都市种田.md) | Business slice of life / rebirth business / rural-urban | High |

## Medium-Confidence Genre Cards

| Genre card | Common aliases/match terms | Confidence |
|---|---|---|
| [Historical High-Concept](genre-prose-cards/历史脑洞.md) | Historical sky-screen / historical system / ancient livestream / industrial history | Medium |
| [Quick Transmigration](genre-prose-cards/快穿.md) | Quick-transmigration system / cannon-fodder comeback / universally adored quick transmigration | Medium |
| [Gaming and Sports](genre-prose-cards/游戏体育.md) | Online games / esports / competitive sports / gaming fiction | Medium |
| [Youth Sweet Romance](genre-prose-cards/青春甜宠.md) | Campus sweet romance / campus romance / school youth | Medium |
| [Contemporary-Romance High-Concept](genre-prose-cards/现言脑洞.md) | Contemporary-romance high concept / women's system fiction / elite-academy high concept | Medium |
| [Eastern Xianxia](genre-prose-cards/东方仙侠.md) | Xianxia / cultivation / classical xianxia | Medium |
| [Suspense High-Concept](genre-prose-cards/悬疑脑洞.md) | Rules suspense / system suspense / strange-tale high concept | Medium |
| [Western Fantasy](genre-prose-cards/西方奇幻.md) | Western fantasy / magic / monsters / Western-fantasy simulator | Medium |
| [Republican-Era Romance](genre-prose-cards/民国言情.md) | Republican-era tragic romance / Republican-era marriage / warlord romance | Medium |

## Low-Confidence Genre Cards

There are currently no individual low-confidence cards. A newly added low-confidence card may serve only as a draft direction. Before writing, prioritize the same-genre benchmark book, user definitions, and latest ranking scan.

---

## Guidance for Using Low-Confidence Genres

A low-confidence card cannot determine the manuscript alone. Before writing, add three things:

1. `剧情/情绪模块.md` and `剧情/节奏.md` from a same-genre benchmark book.
2. `设定/文风.md` or benchmark `文风.md`, confirming sentence length, voice, and paragraph rhythm.
3. Target emotion, order of appearance, information gap, and closing hook from this chapter's detailed outline.

If two or more are missing, generate only a temporary `genre_prose_card`, label it “low confidence,” and do not let the genre card override the detailed outline.
