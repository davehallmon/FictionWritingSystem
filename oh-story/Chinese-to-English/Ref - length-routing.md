# Length-Routing Decision Rules

Use these rules during Phase 1, “Confirm Basic Information,” to determine whether an imported book is long-form or short-form. The result selects the subsequent migration path.

---

## Decision Priority

Evaluate in the following order. Stop at the first match and do not continue downward.

| Priority | Signal source | Decision rule |
|--------|---------|---------|
| 1 | Explicit user declaration | The user says “this is long-form / short-form” → follow the user and lock the type immediately |
| 2 | Structural signal + word-count validation | If explicit chapter separators are detected and chapter count ≥ 5 → long-form. If the complete text has no chapter separators and is one work in one file → apply the three word-count bands in the detailed table below (using the suggested thresholds from Priority 3) |
| 3 | Word-count fallback | Enable only when neither 1 nor 2 is conclusive; see “Word-Count Fallback Rules” below |
| — | Conflict handling | When signals conflict, do not decide automatically. Return to Phase 1, restate the evidence to the user, and ask the user to decide |

---

## Priority 1: Explicit User Declaration

During Phase 1 information confirmation, ask the user: **“Is this long-form or short-form?”**

- If the user answers explicitly → lock the type and skip subsequent detection.
- If the user does not answer or says “uncertain” → proceed to Priority 2 structural-signal detection.

---

## Priority 2: Structural Signal + Word-Count Validation

### Recognizing Chapter Separators

Reuse the separator-recognition table from `structure-mapping-long.md`:

| Separator pattern | Example |
|-----------|------|
| `第X章` / `第X章 ` / `第X章：` / `第X章 XXX` | Chapter 1: Entering the Martial World |
| `Chapter X` | Chapter 1 |
| Plain numeric index + title | 1. Awakening |

### Decision Rules

| Detection result | Decision |
|---------|------|
| Explicit chapter separators and ≥ 5 recognized chapters | Strong long-form signal → classify as **long-form** |
| No chapter separators anywhere, one work in one file, and total word count < 20000 | Strong short-form signal → classify as **short-form** |
| No chapter separators anywhere, one work in one file, and 20000 ≤ total word count < 30000 | Classify as **short-form**, but during the Phase 1 restatement tell the user that it exceeds the short-form breakdown pipeline's suggested 20000-word upper bound and ask the user to confirm short-form import |
| No chapter separators anywhere, one work in one file, but total word count ≥ 30000 | Structure and word-count signals conflict → do not classify automatically; ask the user to decide under “Conflict Handling” below |
| Chapter separators exist, but chapter count < 5 | Structural signal is inconclusive → proceed to Priority 3 word-count fallback |
| Separator pattern is ambiguous (for example, only one title line) | Structural signal is inconclusive → proceed to Priority 3 word-count fallback |

---

## Priority 3: Word-Count Fallback

**Use only when neither Priority 1 nor Priority 2 produces a clear decision.** The current import contract treats 8000–20000 words as the usual short-form range, uses 30000 words as a suggested upper bound, and preserves room for genre differences.

| Condition | Decision | Note |
|------|------|------|
| Total word count < 30000 and no chapter structure | **Short-form** | — |
| Total word count ≥ 30000 | **Long-form** | — |
| Chapter count ≥ 5 (at any word count) | **Long-form** | — |
| Total word count < 30000 but chapter count ≥ 5 | Initially classify as **long-form**, but prompt the user | See “Serialized Chaptered Short Fiction” below |

> **About the suggested value**: The 30000-word threshold is an estimate; short-form upper limits differ by platform and genre. During execution, add it to open-questions and recommend that the user verify whether it applies to the current imported book.

### Serialized Chaptered Short Fiction

When total word count is < 30000 but chapter count ≥ 5, tell the user during confirmation:

> “A chaptered structure ({N} chapters total) was detected, but the total word count is approximately {X}, below 30000. This may be serialized, chaptered short fiction. Should it be imported as long-form or handled as short-form?”

Lock the type after the user decides.

---

## Conflict Handling

When signals point in different directions, **do not decide automatically**. Return to Phase 1 and restate the detection results to the user:

| Typical conflict | Handling |
|------------|---------|
| The user says “short-form,” but 20 chapters are detected | Restate: “A 20-chapter structure was detected, which usually indicates long-form work. Confirm import as short-form?” Let the user decide |
| The user says “long-form,” but the complete text has no chapter separators and word count < 30000 | Restate: “The complete text has no chapter separators and is approximately {X} words, which usually indicates short-form work. Confirm import as long-form?” Let the user decide |
| The user has not declared a type; the complete text has no chapter separators, is one work in one file, but word count ≥ 30000 | Restate: “The complete text has no chapter separators, but its total word count is approximately {X}, above the common short-form upper bound. Build a long-form import project, or still handle it as short-form?” Let the user decide |
| Structural and word-count signals point in opposite directions | Show both signals and ask the user to decide |

Record the user's decision in the Phase 1 context. Subsequent steps follow it without classifying again.

---

## Decision Result and Subsequent Path

After classification, route migration as follows:

| Decision result | Migration path | Mapping-rule reference file |
|---------|---------|----------------|
| **Long-form** | Long-form migration path (Phase 3-L) | `structure-mapping-long.md` |
| **Short-form** | Short-form migration path (Phase 3-S) | `structure-mapping-short.md` |

> Note: `structure-mapping-long.md` contains long-form migration mapping rules; `structure-mapping-short.md` contains short-form migration mapping rules.

---

## Quick Decision Flowchart

```
Phase 1 问用户：「长篇还是短篇？」
         │
         ├─ 用户明确回答 ──────────────────────────► 锁定类型
         │
         └─ 未回答 / 不确定
                  │
                  ▼
         检测章节分隔符
                  │
                  ├─ 有分隔符且章节数 ≥ 5 ──────────► 长篇
                  │
                  ├─ 无分隔符，单文件单篇，< 20000 ─► 短篇
                  │
                  ├─ 无分隔符，单篇，20000 ≤ 字数 < 30000 ─► 短篇（复述时告知超出建议上界）
                  │
                  ├─ 无分隔符，单文件单篇，≥ 30000 ─► 提示用户裁定
                  │
                  └─ 信号不明确
                            │
                            ▼
                   字数兜底判定（30000 字阈值）
                            │
                            ├─ < 30000 且无章节结构 ─► 短篇
                            ├─ ≥ 30000 ─────────────► 长篇
                            ├─ 章节数 ≥ 5 ──────────► 长篇
                            └─ < 30000 但章节数 ≥ 5 ─► 提示用户裁定
```

**English guide (non-executable):**

1. In Phase 1, ask whether the work is long-form or short-form. If the user answers clearly, lock that type.
2. Otherwise inspect chapter separators:
   - Separators with at least five chapters → long-form.
   - No separators, one self-contained file, and fewer than 20,000 Chinese characters → short-form.
   - One self-contained work of 20,000–29,999 characters → short-form, but report that it exceeds the recommended upper bound.
   - One self-contained file of at least 30,000 characters → ask the user to decide.
3. If signals remain unclear, use the 30,000-character fallback:
   - Fewer than 30,000 characters with no chapter structure → short-form.
   - At least 30,000 characters → long-form.
   - At least five chapters → long-form.
   - Fewer than 30,000 characters but at least five chapters → ask the user to decide.
