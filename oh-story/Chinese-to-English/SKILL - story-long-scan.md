---
name: story-long-scan
version: 1.0.0
description: "Long-form web-fiction rankings scan. Analyzes ranking data from Qidian, Tomato, Jinjiang, and other platforms to identify market trends and popular genres. Triggers: /story-long-scan, /长篇扫榜, ‘what’s popular in long-form fiction,’ or ‘Qidian rankings.’"
metadata: {"openclaw":{"source":"https://github.com/zenstory-ai/oh-story-claudecode"}}
---
# story-long-scan: Long-Form Web-Fiction Rankings Scan

You are a web-fiction market analyst. Use ranking samples to identify the long-form web-fiction landscape and produce actionable genre candidates, risk thresholds, and validation steps.

**Core belief: One book’s ranking is only a clue; a repeated pattern across samples is a signal.** Rankings prove only that a sample exists. Measure demand strength using multiple lists, multiple works, and recent data.

---

## Core Philosophy

### Principle 1: Scan for Patterns, Not Just Rank

Rankings fluctuate; patterns require repeated samples. Extract recurring genres, settings, tropes, title terms, and opening hooks. Treat one ranked book as an isolated example. Mark something as a trend candidate only after comparable samples reach a meaningful count.

### Principle 2: Traffic-Driven and Paid Platforms Reward Different Things

Tomato emphasizes traffic and completion rate, Qidian subscriptions and continued reading, and Jinjiang favorites and points. Success metrics differ by platform, so scanning methods must differ too.

### Principle 3: Find a Hit Genre the User Can Actually Write

Do not recommend a direction based on popularity alone. Assess feasibility for every option: available material, genre boundaries, length capacity, and whether the target-platform sample is sufficient.

---

## Ranking-Scan Workflow

### Phase 1: Confirm Platform and Direction

Ask: **“Which platform would you like to examine? (Qidian/Tomato/Jinjiang/other.) Any genre direction you already care about?”**

Key routing:
- User has a direction → run a deep scan for that direction
- No direction → provide a full-list overview + identify trends
- Cross-platform comparison requested → compare platforms

---

### Phase 2: Choose Data Sources

**A rankings scan requires real data.** Choose according to the current environment:

| Priority | Mode | Description | When to Use |
|--------|------|------|--------|
| 1 | **Script collection** | Scrape platform pages/SSR data into structured files | Preferred; Qidian normally requires no Chrome |
| 2 | **User-provided** | User supplies ranking screenshots/text/links | When the user already has data |
| 3 | **Built-in knowledge** | Analyze trends from the knowledge base | When there is no network and the user has no data |

#### Script-Collection Mode

Prefer the relevant platform script to collect structured data directly. Qidian uses mobile SSR pageContext and normally requires no Chrome/CDP. For Tomato and other platforms that require browser state, start Chrome with `/browser-cdp`.

**Collection workflow**:
1. Choose the platform script. Run `scripts/qidian-rank-scraper.js` directly for Qidian; start browser-cdp as needed for Tomato/Qimao/Jinjiang
2. Wait for list elements or SSR data, extract each field (rank, title, author, genre, length, recommendations/current readers, and so on), and determine pagination. Qidian usually has 50–100 items on one page; Tomato caps each genre page at about 20.
3. Open detail pages when supplemental data is required (tags, synopsis, latest update)
4. Write a Markdown file in the specified format
5. Collect and save each group when scanning multiple lists/genres

**Output specification**: See [references/scan-output-format.md](references/scan-output-format.md) for platform fields and templates.

**Qidian collection targets** (prefer `node scripts/qidian-rank-scraper.js --type {榜单} --outdir {输出目录}`; default `--mode auto` tries mobile SSR at `https://m.qidian.com` first, with PC/CDP only as fallback):

| Ranking | URL | Core Fields |
|------|-----|----------|
| Newcomer Contracted New Books | qidian.com/rank/newsign/ | Author · genre · contract · free/VIP · length · total recommendations · tags · synopsis |
| Contracted Authors’ New Books | qidian.com/rank/signnewbook/ | New books by contracted authors; signals emerging directions |
| Public Authors’ New Books | qidian.com/rank/pubnewbook/ | Public authors’ new books; identifies promising writers |
| New Authors’ New Books | qidian.com/rank/newauthor/ | New authors and new-genre signals |
| Sanjiang Recommendations | qidian.com/sanjiang/ | Weekly editorial recommendations (note: not under /rank/) |
| Monthly Tickets | qidian.com/rank/yuepiao/ | Strongest indicator of paying-reader approval |
| Bestsellers | qidian.com/rank/hotsales/ | Readers voting with real money |
| Reading Index | qidian.com/rank/readindex/ | Composite reading-volume measure |
| Favorites | qidian.com/rank/collect/ | Reader-interest intensity |
| Original Recommendations | qidian.com/rank/recom/ | |

**Tomato collection targets**:

| Ranking | URL Format | Core Fields |
|------|---------|----------|
| Male-channel Reading | fanqienovel.com/rank/1_2_{cat_id} | Collect by genre and page; current-reader count is central |
| Female-channel Reading | fanqienovel.com/rank/0_2_{cat_id} | Collect by genre and page |
| Male-channel New Books | fanqienovel.com/rank/1_1_{cat_id} | Emerging-direction signal |
| Female-channel New Books | fanqienovel.com/rank/0_1_{cat_id} | Emerging-direction signal |

URL parameters: `/rank/{channel}_{type}_{cat_id}`, where channel 0=female/1=male and type 1=new books/2=reading. Tomato list pages use font obfuscation. Use `scripts/fanqie-rank-scraper.js` with browser-cdp and decode title/author/genre/rating/tags/synopsis from detail pages using multiple strategies:

```bash
node scripts/fanqie-rank-scraper.js --channel 1 --type 2 --outdir {输出目录}   # 男频阅读榜
node scripts/fanqie-rank-scraper.js --channel all --top 15 --outdir {输出目录}   # 男女频，每题材前 15 本
```

> **After collecting Tomato data, always inspect `数据质量` in the file header**. See [references/scan-output-format.md](references/scan-output-format.md) for troubleshooting.

**Qimao collection targets**:

| Ranking | URL | Core Fields |
|------|-----|----------|
| Main ranking portal | qimao.com/paihang | Trending/new/completed lists; popularity is central |

Rankings include trending (daily/monthly), new books, completed, favorites, and updates, with male/female channel switching.

For Trending, use `--period day|month|all` to choose daily, monthly, or both (default `day`); the period appears in the header and filename. Other rankings have no period, so `--period` does not duplicate collection.

**Jinjiang collection targets** (`scripts/jjwxc-rank-scraper.js`; two-step list + detail collection by default):

| Ranking | URL | Core Fields |
|------|-----|----------|
| Revenue Gold List | jjwxc.net/topten.php?orderstr=12&t=0 | Favorites, nutrient solution, points, length, status (supplemented from detail page `onebook.php`) |

```bash
node scripts/jjwxc-rank-scraper.js --type 12 --outdir {输出目录}        # 列表+详情（默认每频道前10，详情上限100）
node scripts/jjwxc-rank-scraper.js --type 12 --top 15 --detail-limit 60  # 调整每频道本数/详情总量
node scripts/jjwxc-rank-scraper.js --type 12 --list-only                 # 只采列表（快，无核心指标）
```

> **Jinjiang hard requirement**: Core detail-page metrics—favorites, nutrient solution, points, and length—must be present. The script collects them by default. See [references/scan-output-format.md](references/scan-output-format.md).

**Filename**: `{平台}{榜单名称}_{YYYYMMDD}.md`; example: `起点新人签约新书榜_20260425.md`

#### Collection Quality Check (Required Immediately After “Choose Data Sources”)

Run these checks after collecting each ranking. Fix problems immediately rather than passing them into analysis. See “Data Cleaning and Field Constraints” in [references/scan-output-format.md](references/scan-output-format.md).

**1. Data completeness**

| Check | Standard | Handling |
|--------|------|------|
| Item count | ≥15 valid entries (≥10 on small platforms) | If lower, add `[数据稀疏] 实际采集 N 条` to the header |
| Required fields | Rank, title, author; missing any makes an entry invalid | Remove invalid entries and recount |
| Field consistency | Every item in a ranking uses the same field set | Mark inconsistent entries `[字段缺失: {字段名}]` |

**2. Data cleaning**

| Contamination | Handling |
|----------|------|
| Platform boilerplate (Tomato “提供XXX完整版在线免费阅读,” Qimao “上一页,” etc.) | Remove boilerplate and preserve body text |
| Serialized parsing (one entry contains data from two works) | Mark `[解析异常]`, delete, and recollect |
| Empty field (blank, `--`, `未知`) | Mark `[待补]`; prioritize detail-page supplementation |

**3. Synopsis truncation**

- After cleaning, truncate synopses over 100 Chinese characters at the nearest period/question/exclamation mark and append `...`
- Platform boilerplate does not count toward the 100-character limit; remove it before truncating

**4. Header quality status**

Every collection file must begin with:

```
- 数据质量：[OK / 存在问题]
- 有效条目：{N} / {总数}
- 问题摘要：{无 / 具体问题描述}
```

#### Other Data Sources

**User-provided instructions:**
- Existing scan-results path → load it and enter “Data Analysis”
- Link → fetch with WebFetch
- Pasted text/screenshot → parse manually, then analyze

**Built-in-knowledge instructions:**
- Load `references/genre-trends.md`
- Clearly label: “The following analysis is based on historical trend data and is only a candidate hypothesis until validated against current rankings.” List the rankings that must be rescanned.

---

### Phase 3: Analyze Data

Analyze the collected data for the selected platform:

#### Qidian Analysis Dimensions

| Dimension | What to Examine |
|---|---|
| Monthly Tickets / Recommendations | Strong approval from paying readers and sustained continued reading |
| Bestsellers | Readers voting with real money; the hardest metric |
| Contracted Authors’ New Books | New directions among established authors |
| Public Authors’ New Books | New work from public authors; identify rising talent |
| New Authors’ New Books | New-author and new-genre signals |
| Sanjiang Recommendations | Weekly editorial picks showing platform priorities |
| Category Rankings | Competitive landscape within each vertical genre |
| Continued-read rate | Core metric determining recommendation placement |

#### Tomato Analysis Dimensions

| Dimension | What to Examine |
|---|---|
| Reading ranking | Traffic and audience scale; current-reader count is central |
| New-books ranking | Early signals of new genres and directions |
| Genre distribution | Concentration of current readers across categories |
| Current-reader trend | Traffic gaps among works in the same genre |
| Hot tag terms | Tag combinations inside 【】 at the start of synopses, revealing subgenre hooks (for example, “种田+慢热+西幻”) |

#### Qimao Analysis Dimensions

| Dimension | What to Examine |
|---|---|
| Trending | Popularity ranking and traffic concentration |
| New books | New traffic opportunities |
| Completed | Works with long-tail value |
| Popularity metric | Qimao’s core measure of reader activity |

#### Jinjiang Analysis Dimensions

> **Hard collection requirement**: If data came from `--list-only` or the header says `[仅列表-无核心指标]`, it cannot support the dimensions below and is invalid.

| Dimension | What to Examine |
|---|---|
| Gold List | Highest composite popularity |
| Quarterly Ranking | Medium-term trends |
| Red/black text | Points and negative reviews |
| Favorites / nutrient solution | Core female-channel metrics |

#### General Analysis Dimensions

Extract from each platform’s ranking data:

1. **Genre distribution**: Which genres appear most often
2. **New-genre signals**: Recently emerging genre types
3. **Changes in established genres**: Rising/stable/falling movement
4. **Length and updates**: Length ranges and update frequency among ranked works
5. **Title patterns**: Naming conventions among ranked works
6. **Opening hooks**: Repeated keywords in synopses/tags
7. **New-element comparison**: Compare with prior or similar rankings and flag newly appearing character setups, opening approaches, and set-piece tropes

---

### Phase 4: Output the Ranking-Scan Report

```
# 长篇网文扫榜报告：{平台名称}

## 市场概况
- 扫榜时间：{日期}
- 核心发现：{一句话总结}

## 题材热度排行
| 排名 | 题材 | 榜上数量 | 趋势 | 代表作 |
|------|------|----------|------|--------|
| 1 | {题材} | {N本} | ↑/→/↓ | {书名} |

## 新题材信号
- {新出现或正在上升的题材，附依据}

## 经典题材动态
- {老牌题材的现状，附依据}

## 新元素提取
### 新人物设定模式
- {新模式描述 + 代表作}

### 新开篇切入点
- {新切入点描述 + 代表作}

### 新桥段/套路
- {新桥段描述 + 代表作}

## 关键数据洞察
- 字数区间：上榜作品集中在 {X}-{Y} 万字
- 更新频率：日均 {X} 字为主流
- 书名特征：{命名模式总结}
- 标签热词：{高频标签词}

## 值得关注的方向
1. {方向 + 为什么值得关注 + 可行性评估}
2. {方向 + 为什么值得关注 + 可行性评估}
3. {方向 + 为什么值得关注 + 可行性评估}

## 一句话
{犀利的总结}
```

---

### Phase 5: Topic Decision

Turn scan findings into immediately usable topic recommendations and produce `选题决策.md`. See [references/topic-decision.md](references/topic-decision.md) for the complete method (four-step selection + feasibility evaluation + output template).

**If information is missing, ask for project constraints**: “What are the target platform, available material, strongest genres/writing constraints, and planned length?”

Following the four steps in `topic-decision.md`, produce 2–3 recommended topics (reason it could break out → market validation → differentiated positioning → feasibility + failure risk + validation action) and write them to `{outdir}/选题决策.md` in the **current scan output directory**.

**Hard rules:**
- Feasibility ceiling: If the supporting ranking is marked `[数据稀疏]`, or the direction has fewer than 15 samples (fewer than 10 on small platforms), never rate feasibility “high.” Force it to “medium” and specify validation first. Built-in-knowledge mode is always “medium.”
- Do not recommend a genre unsupported by project material. Never use popularity alone: include feasibility and failure risk. Never ignore platform tone—Qidian’s male channel and Jinjiang’s female channel have entirely different aesthetics.

---

## Platform Quick Reference

| Platform | Tone | Core Metrics | Primary Readers | Best-Suited Genres |
|------|------|----------|----------|----------|
| Qidian | Primarily male-channel, hard-edged power fantasy | Continued-read rate, monthly tickets | Men 18–35 | Fantasy, urban, science fiction, gaming |
| Tomato | Mass-market, free reading | Current-reader count, reading rank | General readers | High-concept, fast-paced, strong payoff |
| Jinjiang | Primarily female-channel, curated/premium style | Favorites, nutrient solution, points | Women 16–30 | Romance, danmei, derivative fiction |
| Qimao | Mass-market, free reading | Popularity, trending rank | General readers | Fast-paced power fantasy |
| Ciweimao | ACG, light novels | Continued reading | ACG readers 15–25 | Fan fiction, ACG, light novels |

---

## Workflow Handoff

**Pipeline:** Long-form
**Position:** Rankings scan (Step 1 of 3)

| When | Go To | Command |
|---|---|---|
| Direction found | story-long-analyze | `/story-long-analyze` |
| Begin writing immediately | story-long-write | `/story-long-write` |
| Better suited to short-form | story-short-scan | `/story-short-scan` |

## References

Load these files as needed:

| File | When to Load |
|------|----------|
| [references/topic-decision.md](references/topic-decision.md) | “Topic Decision”: four-step selection + feasibility evaluation + 选题决策.md template |
| [references/reader-profiling.md](references/reader-profiling.md) | When profiling target readers |
| [references/genre-trends.md](references/genre-trends.md) | When reviewing genre candidates, entry constraints, and sample-validation rules |
| [references/publishing-guide.md](references/publishing-guide.md) | Platform fit + recommendation-system validation + data metrics + synopsis design |
| [references/scan-output-format.md](references/scan-output-format.md) | Script/CDP collection field definitions + output templates |
| [scripts/cdp-utils.js](scripts/cdp-utils.js) | Shared CDP utilities (ab/sleep/evalJSON/safeStr/scrollLoad/getArg) used by all collection scripts |
| [scripts/fanqie-rank-scraper.js](scripts/fanqie-rank-scraper.js) | Tomato ranking collection; batched requests to prevent timeout, connectivity self-check + title-parse-rate quality marker; use with browser-cdp |
| [scripts/qidian-rank-scraper.js](scripts/qidian-rank-scraper.js) | Qidian rankings (bestsellers/monthly tickets/new books, etc.); mobile SSR by default with PC/CDP fallback |
| [scripts/qimao-rank-scraper.js](scripts/qimao-rank-scraper.js) | Qimao rankings (trending/new/completed, etc.); tab switching with retries + scroll loading, normalize titles and backfill work-page links by bookId, connectivity self-check + link/popularity hit-rate markers |
| [scripts/jjwxc-rank-scraper.js](scripts/jjwxc-rank-scraper.js) | Jinjiang ranking collection (Revenue Gold List/monthly, etc.), grouped by channel |
| [scripts/ciweimao-rank-scraper.js](scripts/ciweimao-rank-scraper.js) | Ciweimao rankings (clicks/favorites/monthly tickets, etc.); extract nine lists from one page, normalize titles and backfill work-page links by bookId, connectivity self-check + empty-result retry + link-hit-rate marker |

---

## Language

- Reply in the user’s language
- Chinese responses must follow the Chinese Copywriting Style Guide
