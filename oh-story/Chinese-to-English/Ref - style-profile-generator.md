# Style-Profile Generation SOP

> **When to load**: During Stage 6 of story-long-analyze. `拆文报告.md` is a blocking prerequisite; `章节/*_摘要.md`, `章节/第1-3章_深度拆解.md`, and `原文/原文.txt` (or `.md`) are quality inputs. When any are missing, handle them item by item according to “Failure Modes and Degradation” below.
>
> **Output**: `拆文库/{书名}/文风.md` (see the template in [style-profile-protocol.md](style-profile-protocol.md)).

## Six-Step Process

### Step 1: Read Core Fields from the Deconstruction Report

Read `拆文库/{书名}/拆文报告.md` and extract:

- **“Writing Techniques” section** → populate “Top 5 Writing Techniques” under “Reusable Techniques” in the style profile
- **“Reusable Formulas” section** → populate “Top 3 Reusable Formulas” under “Reusable Techniques” in the style profile
- **“Book-Wide Emotional Pacing Overview / Foreshadowing and Conflict Network” sections** → populate the advanced and adaptation layers under “Layered Imitation Guidance”; abstract only pacing and technique, never copy specific plot events
- **Basic information** (title, genre, total chapter count) → populate the style-profile title and “Generation Record”
- In “Generation Record,” write only information useful to the author: which materials were consulted, which chapters were sampled, generation time, and whether the style profile is usable. Do not write implementation terminology such as file timestamps or internal degradation markers.

### Step 2: Read the In-Depth Deconstruction of the Golden Three Chapters

Read `章节/第1章_深度拆解.md`, `第2章_深度拆解.md`, and `第3章_深度拆解.md`, then extract:

- **Opening-hook type + technique**
- **Reaction-layer deconstruction table** (samples of dialogue subtext)
- **Setup-to-payoff ratio** (samples of emotional alternation)
- **Reusable elements** (merge with Step 1, deduplicate, and feed into “Top 5 Writing Techniques”)

### Step 3: Extract the Chapter Tone/Theme-Tag Sequence

Use Grep to read every `章节/*_摘要.md`:

```bash
grep -hE '基调：(紧张|轻松|悲伤|热血|爽|甜|温馨|恐怖|压抑|其他)' 章节/*_摘要.md
```

**Critical formatting note**: The actual format of `章节/*_摘要.md` is `主题标签X | 基调：Y` on its own line after each plot beat (10–40 lines per chapter). `基调` uses a **full-width colon**, `主题标签` has **no colon** after it, and neither appears **at the start of the line**. The grep pattern must not use an anchor such as `^基调:`.

**Chapter-tone aggregation rules** (one chapter tone per chapter, written into “Emotional Alternation Pattern” in the style profile):

- Calculate the mode of every plot beat's “tone” field in that chapter
- When tied (such as five tense vs. five passionate), select the tone that appears **earliest** in the chapter (by line number in `_摘要.md`)
- Output format: `第N章: {章基调}`, linked into a book-wide sequence

**Within-chapter plot-beat tone sequence** (used to analyze “within-chapter tone shifts”):

- Do not aggregate; preserve plot-beat order from `_摘要.md`
- Use it to calculate switching frequency: number of adjacent beats with different tones / total plot beats

### Step 4: Sample the Source Text

Under `原文/`, there is **only one complete-book file**, `原文.txt` (or `.md`), **not separate chapter files**. Stage 0 has written the validated start and end lines of every chapter into `拆文库/{书名}/_progress.md`; this table is the sole slicing authority shared by Stages 1/2/6.

**Stage 6 reads only the “chapter boundaries” table in `_progress.md`. It must not search for chapter headings again, infer boundaries independently, or correct the rules itself.** If the table is absent, the target chapter lacks a boundary, boundaries are discontinuous, or a boundary points outside the source range, stop Stage 6 immediately and instruct the user to rerun Stage 0 to rebuild the progress file. Never continue generating the style profile with temporary slices.

**Sample slices**:

- Select Chapters 1, 10, and 20 from the chapter-boundaries table in `_progress.md` (when total chapters <20, select at the one-third, two-thirds, and ending positions)
- For each chapter, use `Read offset={该章起始行} limit=50` to extract approximately 1,000 Chinese characters
- Combine the three passages in `拆文库/{书名}/_style-sample.txt` (use this exact filename): **write the first passage with `>` to overwrite, then append only the latter two with `>>`**. Using `>>` throughout would accumulate the previous run's sample when Stage 6 is rerun, making the measured sentence-length distribution a mixture of two runs

**Deterministic sentence-length/punctuation statistics** (replaces subjective visual estimation):

Stage 6 is executed by the **main thread**, where Bash tools are available. Feed the `_style-sample.txt` created above into the script below (the heredoc supplies the Python source while the sample path is passed through argv, avoiding conflicting redirection from both an stdin heredoc and `< file`). Probe for an available interpreter first—**do not invoke `python3` directly** because on Windows it may trigger the Microsoft Store placeholder and fail with exit 49.

The sample path **must be relative to the project**, never `/tmp/...`: the detected interpreter may be native Windows Python (through the `py` launcher), which resolves `/tmp/x.txt` as `C:\tmp\x.txt`, a different file from the one written by Git Bash, causing an immediate FileNotFoundError.

```bash
SAMPLE="拆文库/{书名}/_style-sample.txt"   # {书名} 换成实际书名，别照抄占位符
for PYBIN in python3 python py; do "$PYBIN" -c "" 2>/dev/null && break; done
"$PYBIN" - "$SAMPLE" <<'PYEOF'
import re
import sys
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    text = f.read()
sents = [s for s in re.split(r'[。！？]+', text) if s.strip()]
total = max(len(sents), 1)
short = sum(1 for s in sents if len(s) < 15)
mid   = sum(1 for s in sents if 15 <= len(s) <= 30)
lng   = sum(1 for s in sents if len(s) > 30)
chars = max(sum(1 for c in text if not c.isspace()), 1)
puncts = sum(1 for c in text if c in '，。！？；：、…—""\'\'')
avg = sum(len(s) for s in sents) // total
print(f'sentences={total}; short_lt15={100*short//total}%; mid_15to30={100*mid//total}%; long_gt30={100*lng//total}%; avg_len={avg}; punct_density={100*puncts//chars}%')
PYEOF
```

A real output looks like `sentences=6; short_lt15=66%; mid_15to30=33%; long_gt30=0%; avg_len=12; punct_density=15%`.

Copy the output values for `short_lt15 / mid_15to30 / long_gt30 / avg_len / punct_density` directly into the `{...X% / Y% / Z%}` placeholders on line 40 of the style-profile-protocol.md template—`confidence: high`, because these are deterministic measurements rather than sample-based estimates.

**Degradation when Bash is unavailable** (only in extreme cases such as a subagent context; never triggered in the main thread):

- Skip this step; in the sentence-length section write “Bash tools unavailable; deterministic statistics skipped”
- Set `confidence: low`; narrative-writer yields to default Gate D (calibrated by sentence-length standards)

### Step 5: Select Source Anchor Passages (4–6 Passages)

From the chapter tones output in Step 3, choose 4–6 categories with the highest coverage that the project may need (prioritize tense / sad or oppressive / relaxed or warm / passionate). If the comparable title contains fewer than three chapters in a category, do not fabricate one; state in the style file that it was skipped. Select one anchor chapter per category.

**Selection rules when multiple chapters share the same tone**:

1. **L1 strongest match for payoff type**: Use the chapter's “key events” + tone sequence in `_摘要.md` to select the chapter with the strongest payoff
2. **L2 source chapter length closest to the daily target**: If Step 4 produced chapter boundaries, estimate the length from the source slice; if the source cannot be sliced, use only the number of plot beats in `_摘要.md` to approximate complexity—never treat the summary file's length as the source chapter's length
3. **L3 lowest chapter number**: The earliest chapter = the author's most canonical voice (before serialization drift)

Anchor slices:

- Use the chapter start and end lines read from `_progress.md` in Step 4
- Select one 300–500-character passage from that chapter (prefer interwoven dialogue + action; do not select pure monologue/exposition)
- Extract it with `Read offset limit`, preserving original punctuation and paragraph breaks
- **Every anchor must be a verbatim contiguous slice; rewriting/shortening/skipping paragraphs/combining is prohibited**: narrative-writer uses anchors directly as few-shot examples, and the cited lines must trace back to the source. Before saving, sample one or two sentences from each passage and run `grep -F` against `原文/原文.txt`. If grep finds nothing, the passage was rewritten or combined—reslice it faithfully. If an intermediate transition must be omitted, label the real line ranges separately (for example, “lines 264–267 + lines 269–270”) and explicitly mark the break inside the quotation as “（……中略……）”; never disguise it as one continuous range

### Step 6: Save to Disk

Fill the `拆文库/{书名}/文风.md` template from [style-profile-protocol.md](style-profile-protocol.md):

- **The style file must remain in the deconstruction library** (`拆文库/{书名}/文风.md`) and is **never written directly by analyze** into `对标/` or a writing-project directory—the deconstruction library is the data source. Only when the book is explicitly selected as an external comparable for another project may story-import or story-long-write synchronize it on first reference into `对标/{书名}/`
- Mark every section `confidence: high/med/low` (used internally by the writing agent to judge strength; ordinary users may ignore it):
  - `high`: Data comes directly from a deconstruction artifact (for example, “Writing Techniques” quoted directly from the deconstruction report)
  - `med`: Inferred from adequate samples (for example, a tone sequence calculated from ≥10 chapter summaries)
  - `low`: Samples are insufficient or sampling failed (for example, missing anchors or Bash unavailable, causing Step 4 sentence-length statistics to be skipped)
- “Layered Imitation Guidance” must be divided into foundation / advanced / adaptation layers. The foundation layer covers only vocabulary, sentences, description, and dialogue habits; the advanced layer covers pacing, foreshadowing, viewpoint, and scene transitions; the adaptation layer identifies what can be used and what may misalign this project. Explicitly prohibit copying proper nouns, signature dialogue, distinctive plot events, and event order
- Length budget: hard limit ~4,000 Chinese characters. **Descriptive sections ≤1,800 Chinese characters + 4–6 anchor passages × 300–500 Chinese characters**
- If Step 4 fails (chapter separators cannot be identified) → write `文风可用：否：无法识别章节分隔符` in “Generation Record”; fill every source-anchor passage with the placeholder “原文缺失，需手动补充,” and set all confidence values to low

## Failure Modes and Degradation

| Scenario | Degradation Strategy |
|---|---|
| `原文/原文.txt` does not exist | Skip Steps 4–5; the style file contains descriptive sections only; write `文风可用：否：原文缺失` in “Generation Record” |
| Fewer than three `章节/*_摘要.md` files | Skip the Step 3 tone sequence; mark the emotional-alternation section confidence: low |
| `章节/第1-3章_深度拆解.md` is absent | Skip Step 2; fall back to the deconstruction report for dialogue subtext; confidence: low |
| `拆文报告.md` does not exist | **Stop Stage 6**; tell the user deconstruction is incomplete and Stage 5 must finish first |

## Relationship to chapter-extractor

**Do not modify chapter-extractor**. Generate the style profile directly from existing fields (tone/theme tags/reusable elements).

Sentence length / punctuation density is calculated directly in the Stage 6 main thread using the cross-platform Python one-liner from Step 4 and does not depend on chapter-extractor.

## Relationship to the Writing Side

- Analyze Stage 6 writes `拆文库/{书名}/文风.md`
- When story-import explicitly binds an external comparable or story-long-write first references `拆文库/{书名}/`, synchronize it into the project's `{项目}/对标/{书名}/` **including** the style profile (treat it the same as the deconstruction report); never make the book currently being imported its own external comparable
- The daily loop on the writing side (story-long-write) reads `{项目}/对标/{书名}/文风.md` (following comparable-title path-resolution rules, falling back to `拆文库/{书名}/`)

## Rebuilding a Style Profile Independently

If the current deconstruction output lacks only `文风.md`, run the six steps in this SOP directly (Stage 6 only) without rerunning Stages 0–5, provided `_progress.md` satisfies the current chapter-boundary contract. Trigger: the user directly says “为对标书 X 生成文风” or “重生 文风.”
