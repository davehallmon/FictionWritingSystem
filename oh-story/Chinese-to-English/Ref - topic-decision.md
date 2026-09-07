# Topic Selection: From Ranking-Scan Data to “What Can Become a Hit?”

Turn ranking-scan results into directly usable topic recommendations: **what to write, why it might become a hit, whether it is viable, and how to validate it**.
Phase 5 uses this method to produce `选题决策.md`, an initial market-oriented topic proposal. Treat “why it can become a hit” as a hypothesis until story decomposition with story-long-analyze validates it; story-long-write can use the result directly when starting a book.

---

## Decision Routing

| What are you doing? | Read this section |
|-----------|--------|
| Turn ranking-scan results into topic recommendations | Four Topic-Selection Steps |
| Determine whether a direction is viable | Viability Assessment |
| Work without internet or ranking data | Built-In Knowledge Mode |
| Save and deliver the result | 选题决策.md Template + Delivery |

---

## Four Topic-Selection Steps

Every recommended topic must complete all four steps:

1. **Why it can become a hit (initially a hypothesis):** Use **recurring samples** in the rankings—not one-book outliers—plus newly extracted elements to hypothesize: “This direction can become a hit because structure/trope/characterization X serves this audience.” A single ranked book is only an outlier; ranking-scan principle 1 requires recurrence across several books. Mark the hypothesis `待拆文验证`; story decomposition must later validate it.
2. **Market validation:** Record the number of ranked books in the same direction, the trend (↑/→/↓), and counterexamples such as failures or abandoned endings in that direction. More samples and a steadier trend increase confidence.
3. **Differentiated positioning:** Author advantage × market gap = “How does your version differ from existing ranked works?” Without differentiation, the work cannot enter a homogeneous market.
4. **Viability, risk, and validation action:** Assign high, medium, or low viability under the rules below; identify the most likely failure; and define a low-cost pre-drafting validation action, usually “write the opening three chapters, test continued-reading behavior, and change direction if it fails.”

---

## Viability Assessment

Use three levels. Never assign “high” from insufficient samples; a few data points must not create false confidence.

| Viability | Meaning | Conditions |
|--------|------|------|
| High | Safe to draft | Enough ranked samples in the direction (≥15; ≥10 on small platforms) + upward or stable trend + sufficient author material + room for differentiation |
| Medium | Viable, but validate first | Enough samples but a downward trend, unclear differentiation, or only partial support from the author's material |
| Low | Not recommended | Saturated direction with many failed counterexamples, insufficient author material, or mismatch with platform tone |

**Hard rule:** If the supporting ranking is marked `[数据稀疏]`—fewer than 15 valid entries, or fewer than 10 on a small platform, using the ranking-scan collection threshold—the direction **must not receive “high.”** Downgrade it to “medium” and state: “Insufficient samples; collect enough samples or run a low-cost test before deciding.”

**Built-In Knowledge Mode:** Without rankings and relying only on knowledge-base trends, assign **“medium” to every direction**. State: “Based on general knowledge without ranking validation; scan rankings or run a low-cost test before drafting.” Never assign “high.”

---

## 选题决策.md Template

```
# 选题决策：{平台/方向}
- 扫榜日期：{YYYYMMDD}     # 数据新鲜度；写作读取时若过期会提示复扫
- 数据来源：{榜单文件名 / 内置知识}

## 推荐选题

### 选题 1：{一句话方向}
- 题材组合：{主类型 + 副类型/梗}
- 目标读者：{画像}
- 核心卖点：{读者为什么追}
- 能爆的原因：{X 结构/梗为什么吃这波}（假设，`待拆文验证`）
- 差异化定位：{和榜上现有的不同在哪}
- 可行性：高/中/低 — {理由，写清同方向几本 + 趋势}
- 失败风险：{最可能崩在哪}
- 验证动作：{开写前怎么低成本验证}
- 篇幅/平台：{建议字数区间 + 目标平台}

### 选题 2 ...
### 选题 3 ...
```

Recommend two or three topics, ordered by viability with the highest first.

---

## Delivery

1. Write the result to the output directory of the current ranking scan, beside the ranking file: `{outdir}/选题决策.md`. Ranking scans often run before a novel project exists, so save the artifact here rather than directly in a project.
2. Tell the user the path and explain the next step: “If the novel project is created in this directory or beside it under the same parent, `/story-long-write` will find this file automatically and ask for confirmation. If it is farther away, copy `选题决策.md` to the novel-project root or provide its path when starting the book. To validate ‘why it can become a hit,’ first run `/story-long-analyze` on benchmark books; decomposition will fill in the validation.”
3. Describe, but do not execute, the later handoff: after producing the aggregate report, story decomposition fills in validation for the corresponding topic's “why it can become a hit”; writing Phase 1 reads `选题决策.md` as the starting point for a new book.
