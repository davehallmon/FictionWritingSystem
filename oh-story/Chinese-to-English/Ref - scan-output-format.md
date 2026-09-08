# Ranking-Scan Data Collection Format Specification
Defines collection fields, output templates, and cleaning rules for Qidian, Tomato Novel, Qimao, and Jinjiang.

---

## Qidian

### Qidian Collection Instructions

For the ranking list and URLs, see the “Qidian Collection Targets” table in SKILL.md.

Prefer `scripts/qidian-rank-scraper.js` with its default `--mode auto`. The script first reads the mobile SSR pageContext JSON from `https://m.qidian.com`, avoiding the PC site's risk-control page; it falls back to the CDP/PC page only when the mobile site is unavailable. The output header identifies the method as `抓取方式：mobile-ssr` or `cdp-pc`.


### Fields

Rank | Book title | Author | Genre | Status | Contract status | Payment model | Length (10,000 Chinese characters) | Total recommendations | Tags (detail page) | Latest update (detail page) | Work-page link | Synopsis (detail page, truncated to 100 Chinese characters)

### Output Template

```markdown
# qidian · {榜单名称}
- 来源：{榜单URL}
- 抓取时间：{ISO 8601}
- 条目数：{N}

---

## #{排名} {书名}
*{作者} · {题材} · {状态} · {签约} · {免费/VIP} · {字数}万字 · {推荐数}总推荐*
**标签：** {标签}
**最新更新：** {YYYY-MM-DD HH:MM:SS} · {章节标题}

[作品页]({URL})

**简介**
{简介原文}
```

**English guide (non-executable):** Qidian ranking name; source URL; collection time; item count; then rank, title, author, genre, publication status, contract status, free or VIP status, length in ten-thousands of Chinese characters, total recommendations, tags, latest update, work URL, and original synopsis.

### Collection Essentials

The ranking page contains rank/title/author/genre/length/recommendations/contract/free-or-VIP status. The detail page must supply tags/latest update/synopsis. Group Sanjiang results by week.

---

## Tomato Novel

For ranking URL formats and parameter descriptions, see the “Tomato Collection Targets” table in SKILL.md.

### Genre cat_id

19 male-audience genres: Western fantasy (1141) / Eastern xianxia (1140) / science-fiction apocalypse (8) / urban daily life (261) / urban cultivation (124) / urban high martial arts (1014) / ancient history (273) / god-of-war live-in son-in-law (27) / urban farming (263) / traditional fantasy (258) / alternate-history premise (272) / suspense premise (539) / urban premise (262) / fantasy premise (257) / supernatural suspense (751) / Resistance War espionage (504) / gaming and sports (746) / anime derivatives (718) / male-audience derivatives (1016)

18 female-audience genres: ancient-style social fiction (1139) / science-fiction apocalypse (8) / gaming and sports (746) / female-audience derivatives (1015) / fantasy romance (248) / farming (23) / period fiction (79) / contemporary-romance premise (267) / palace and household intrigue (246) / suspense premise (539) / ancient-romance premise (253) / quick transmigration (24) / youthful sweet romance (749) / entertainment stardom (745) / female-audience suspense (747) / workplace marriage and romance (750) / wealthy-family CEO romance (748) / Republican-era romance (1017)

### Fields

Rank | Book title (must be decoded from detail page) | Author (must be decoded from detail page) | Genre (detail-page categoryV2) | Status | Current readers (core metric) | Length | Tags (【】 in synopsis) | Latest update | bookId | Work-page link | Synopsis (truncated to 100 Chinese characters)

> Tomato's SSR detail page **does not provide a numeric rating**, so do not output a rating. Take the genre from detail-page `categoryV2` (the first `Name` in escaped JSON, such as “西方奇幻”); take tags from the leading `【tag+tag+...】` in the synopsis (such as “种田、慢热、西幻”). These provide genuine subgenre signals.

### Output Template

```markdown
# 番茄 · {频道}{榜单名} · 全 {N} 题材
- 频道参数：channel={0女频/1男频}，type={1新书榜/2阅读榜}
- 抓取时间：{ISO 8601}
- 标题解析：成功 {X} / 共 {Y}
- 数据质量：[OK / 标题解析异常 / 无数据]
- 每题材上限 ≈ {N}（cap≈20）

---

## {题材名称} — {N} 本

### #{排名} {书名}
*{作者} · {题材} · {状态} · {在读数} 在读 · {字数}字*
**标签：** {标签1、标签2}
**最新更新：** {章节}
**bookId：** {bookId}

[作品页]({URL})

**简介**
{简介原文}
```

**English guide (non-executable):** Fanqie channel and ranking name; channel parameters (female or male channel, new-book or reading ranking); collection time; title-parse success count; data quality; per-genre cap; then genre, rank, title, author, status, active-reader count, character count, tags, latest chapter, book ID, work URL, and original synopsis.

> Title/author/genre/tags/synopsis are all optional fields: output them only when obtained from the detail page. If title decoding fails, display `（标题待解析）` as the title, but always retain bookId and the work-page link for manual verification.

### Collection Essentials

Custom-font anti-scraping: because the list page's innerText is obfuscated by a custom font, `scripts/fanqie-rank-scraper.js` instead uses multiple strategies to decode plaintext from the detail-page HTML (embedded JSON `bookName`/`author`/`abstract`/`categoryV2` + `<title>` + og:meta), bypassing font-based protection. Flow: visit the category page → extract category links → obtain the `__INITIAL_STATE__` list for each category → request detail pages in batches of five books to decode them. The per-page limit is about 20 books and requires scrolling to load more; `--top N` adjusts the per-genre limit.

**Troubleshooting (every title is `bookId:xxx` / `（标题待解析）`)**:
- Check `数据质量` in the file header: `[标题解析异常]` indicates a high detail-page decoding failure rate.
- This usually means the detail-page structure changed or a login/verification page blocked access. In a signed-in Chrome session, manually open any `https://fanqienovel.com/page/{bookId}` and confirm that it is the normal page rather than a verification page.
- If the console reports `CDP 无响应`, Chrome/CDP is not running or the port is wrong. Restart it according to the browser-cdp skill. After confirming normal operation, collect the data again.

---

## Qimao

### Rankings

Entry point: qimao.com/paihang; switch between the male-audience and female-audience tabs. Types: Popular Ranking (daily/monthly) / New Book Ranking / Completed Ranking / Favorites Ranking / Update Ranking.

### Fields

Rank | Book title | Author | Genre | Classification tags | Status | Length (10,000 Chinese characters) | Popularity (core metric) | Latest update | Work-page link | Synopsis (truncated to 100 Chinese characters)

### Output Template

```markdown
# 七猫 · {男/女}频 · {榜单名称}
- 来源：qimao.com/paihang
- 抓取时间：{ISO 8601}
- 条目数：{N}

---

### #{排名} {书名}
*{作者} · {题材} · {分类标签} · {状态} · {字数}万字 · {热度}万热度*
**最新更新：** {时间} · {章节}

[作品页]({URL})

**简介**
{简介原文}
```

**English guide (non-executable):** Qimao male or female channel and ranking name; source, collection time, and item count; then rank, title, author, genre, category tags, status, length, popularity, latest update, work URL, and original synopsis.

### Collection Essentials

No obvious anti-scraping; scrolling is required to load more. Switch between male-audience and female-audience ranking tabs; the Popular Ranking has daily/monthly switches.

---

## Jinjiang

### Ranking URL

`jjwxc.net/topten.php?orderstr={榜单ID}&t={频道ID}` (t=0 for the entire site; obtain other channel IDs from the page)

| Ranking | orderstr |
|------|----------|
| Revenue Gold Ranking | 12 |
| Monthly Ranking | 7 |
| Quarterly Ranking | 8 |
| Completed Works Gold Ranking | 14 |
| Newcomer Gold Ranking | 15 |
| Per-Thousand-Characters Gold Ranking | 17 |

### Fields

Channel | Rank | Book title | Author | novelid | Favorites (core metric) | Nutrient solution | Points | Length | Status | Work-page link

### Output Template

```markdown
# 晋江 · {榜单名}
- 来源：{topten URL}
- 抓取时间：{ISO 8601}
- 频道数：{N} / 总条目数：{M}
- 详情采集：{命中收藏数} / {计划数}（每频道前 {top}，上限 {limit}）
- 数据质量：[OK / 详情解析异常·登录态缺失 / 仅列表-无核心指标]

---

## {频道名} — {N} 本

### #{排名} {书名}
*{作者} · 收藏 {X} · 营养液 {Y} · 积分 {Z} · 字数 {W}字 · {状态}*
[作品页](https://www.jjwxc.net/onebook.php?novelid={id})
```

**English guide (non-executable):** Jinjiang ranking name; source URL; collection time; channel and total-item counts; detail-collection success and plan counts; data quality; then each channel's item count and, for every work, rank, title, author, favorites, nutrient-solution count, points, character count, status, and work URL.

### Collection Essentials

Two steps: ① obtain channel groups + titles/authors from list-page `topten.php`, taking `novelid` from each title anchor (exclude overlord-ticket records in the form “X向《书名》投了Y”); ② visit the `onebook.php?novelid=` detail page to collect the core metrics.
- **Encoding**: Jinjiang uses gb18030. The detail page must be decoded with `fetch+arrayBuffer+TextDecoder('gb18030')` (responseText from synchronous XHR is decoded as UTF-8 and becomes garbled).
- **Field sources**: detail-page `itemprop` microdata—`collectedCount` (favorites)/`nutritionCount` (nutrient solution)/`scoreCount` (points)/`wordCount` (length)/`updataStatus` (status). These are public metrics and **do not require login**.
- **Volume control**: retain the complete list, but fetch details only for the first `--top` books in each channel (subject to the overall `--detail-limit`), avoiding individual requests for hundreds of books across the whole site.

---

## Data Cleaning

General: remove platform boilerplate → truncate synopses longer than 100 Chinese characters at a period and append `...` → mark empty values `[待补]`.

| Platform | Additional required fields |
|------|----------|
| Qidian | Genre, length, total recommendations |
| Tomato | Current readers |
| Qimao | Popularity |
| Jinjiang | Favorites, nutrient solution (or points), length |

Minimum collection size: 15 entries for major platforms and 10 for smaller platforms. Mark anything below the threshold `[数据稀疏]`.

---

## Batch Collection

| Platform | Default combination |
|------|----------|
| Qidian | Top 20 on Newcomer Contracted New Books + top 20 on Contracted Authors' New Books + top 20 on Monthly Tickets + top 20 on Bestsellers |
| Tomato | Every genre on the male-audience Reading Ranking + every genre on the female-audience Reading Ranking |
| Qimao | Male-audience daily Popular Ranking + female-audience daily Popular Ranking |
| Jinjiang | Revenue Gold Ranking + Monthly Ranking |
| All platforms | Default Qidian + Tomato + Qimao combinations |
