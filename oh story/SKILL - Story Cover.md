---
name: story-cover
version: 1.0.0
description: "Novel cover generation. Automatically analyzes genre/style from title and author name, calls GPT-Image-2 to produce a professional web-novel cover with title and byline; Codex CLI uses built-in ImageGen first, no separate API key needed. Triggers: /story-cover, /封面, \"help me make a cover\", \"generate cover image\", \"make a novel cover\", \"cover design\"."
metadata: {"openclaw":{"requires":{"env":["GPT_IMAGE_API_KEY"],"bins":["curl","jq","base64"]},"primaryEnv":"GPT_IMAGE_API_KEY","source":"https://github.com/zenstory-ai/oh-story-claudecode"}}
---
# story-cover: Novel Cover Generation

You are a novel cover designer. Given a title and genre, call GPT-Image-2 once to generate a complete cover containing the title and author name.

**Core principle: the cover is the reader's first impression — it must convey genre and atmosphere at a glance.**

---

## Generation Paths

- **Codex built-in (preferred)**: When the current Codex CLI session can call `$imagegen` / `image_gen`, generate and save directly; counts against Codex general usage, no `OPENAI_API_KEY` or `GPT_IMAGE_API_KEY` required, and `curl` is not run. `story-cover` calls the tool itself — the user does not run a separate command.
- **API fallback**: Used only when the session lacks a built-in tool or the user explicitly specifies the API; requires `GPT_IMAGE_API_KEY`. Missing tool ≠ Codex subscription doesn't support image gen; if the built-in call fails, report the error first, don't silently switch to a potentially billable API.

## Output Parameters & API Fallback Environment Variables

| Variable | Required | Default | Description |
|:-------|:------:|:------|:----------|
| `GPT_IMAGE_API_KEY` | API fallback only | — | OpenAI or compatible proxy API Key; not used for Codex built-in path |
| `GPT_IMAGE_BASE_URL` | | `https://api.openai.com/v1` | Change for compatible proxy |
| `GPT_IMAGE_MODEL` | | `gpt-image-2` | Override only when testing a new model |
| `GPT_IMAGE_SIZE` | | `1024x1536` | Target aspect hint for API fallback (Fanqie 3:4→`768x1024`, default 2:3→`1024x1536`). Official gpt-image-2 accepts any 16-multiple dimensions (ratio ≤3:1), but **many proxies ignore size and return ~2:3 preset** (verified) — platform size isn't guaranteed by this; the "Export Platform Upload Size" step handles it |
| `UPLOAD_SIZE` | | — | Fixed platform upload pixels (Fanqie `600x800`); when set, the "Export Platform Upload Size" step center-crops+scales to upload version (no distortion, independent of generated size) |
| `BOOK_DIR` | ✅ | — | Output directory, suggest `./covers/<title>` |
| `REF_IMAGE` | | — | Reference image local path or URL; built-in path loads image into session first, API fallback uses `images/edits` for img2img |

---

## Generation Flow

### Step 1: Gather Information

Required: title, author name (pen name), target platform, output directory `BOOK_DIR` (suggest `./covers/<title>`; API fallback uses env var, built-in uses current task value)
Optional: reference image `REF_IMAGE` (local path or URL; when set, switches to img2img), style preference, size

> **Title and pen name are required on the cover**: if either is missing, you MUST use AskUserQuestion to ask the user to provide it — do not invent or leave blank.

**Determine cover size by target platform**: Fanqie upload 600×800 is **3:4** (not 2:3); wrong aspect ratio → platform re-crops and cuts off title/byline.

| Platform | Upload Size | Ratio | Generated `GPT_IMAGE_SIZE` (best effort) |
|:------|:-----------|:-----|:-------------------------------|
| Fanqie Novel | 600×800 | 3:4 | `768x1024` |
| Other platforms (default portrait) | Per platform spec | 2:3 | `1024x1536` |

Built-in path writes target ratio into the prompt; API fallback also `export GPT_IMAGE_SIZE` (many proxies ignore and return ~2:3). When platform has fixed upload pixels, set `UPLOAD_SIZE` (Fanqie `600x800`). **Platform size is ultimately guaranteed by the "Export Platform Upload Size" step — center-crop+scale — independent of actual generated size.** Platform and genre styles see [references/cover-styles.md](references/cover-styles.md).

### Step 2: Genre Determination

Scan title (and synopsis if needed) for keywords, match against the "Genre Inference Rules" table in [references/cover-styles.md](references/cover-styles.md) to select genre.

- Single genre hit → adopt directly
- Multiple hits → take one by priority: Xianxia > Western Fantasy > Ancient Romance > Modern Romance > Urban > Mystery > Sci-Fi > Historical > Supernatural > Light Novel
- Zero hits → default `Urban`

### Step 3: Build Prompt

Prompt = **Text Layer** + **Style Layer** + **Scene Layer**, all written in English.

#### Text Layer: Title + Author Name Typography

Include Chinese title and author name directly in the prompt — GPT-Image-2 can render them natively. **Focus on describing font style:**

```
Title text '书名' at top center in [title font style].
Author name '作者名' at bottom center in [author name font style].
```

#### Title Font Style

| Genre | Description Keywords |
|:------|:---------------------|
| Xianxia / Fantasy | `bold golden brush calligraphy with metallic glow and sharp strokes` |
| Urban | `modern bold sans-serif with metallic silver finish` |
| Ancient Romance / Palace Intrigue | `elegant golden traditional Kai script with ornate decoration` |
| Modern Romance / Sweet | `soft rounded handwritten style in white with pink glow` |
| Mystery / Thriller | `distorted bold cracked letters in blood red` |
| Sci-Fi / Post-Apocalyptic | `neon glowing futuristic font in electric blue` |
| Western Fantasy | `metallic embossed fantasy lettering with glow effect` |
| Historical / Military | `heavy stone-carved seal script in deep red` |
| Supernatural / Horror | `eerie dripping handwritten font in sickly green` |
| Light Novel | `colorful cartoon outlined bubbly font` |

#### Author Name Font Style (key: author name must be carefully designed, not just "small text")

Author name is small but critical to professional cover feel. Must specify: **font + color + decorative elements**, so it echoes the title style without stealing focus.

| Genre | Author Name Style Prompt |
|:------|:------------------------|
| Xianxia / Fantasy | `small refined white serif text with faint golden glow, flanked by delicate cloud-scroll ornaments on both sides, resting on a thin horizontal gold line` |
| Urban | `small clean white modern text with subtle drop shadow, positioned above a thin silver horizontal divider line` |
| Ancient Romance / Palace Intrigue | `small elegant dark red traditional text inside a thin golden rectangular border frame with corner decorations` |
| Modern Romance / Sweet | `small soft pink-white handwritten text with a tiny heart motif on the left side, light sparkle effect` |
| Mystery / Thriller | `small pale grey text with slight blur effect, almost hidden in the shadows, a thin cracked line underneath` |
| Sci-Fi / Post-Apocalyptic | `small crisp white monospace text with subtle cyan scanline overlay, flanked by small geometric brackets` |
| Western Fantasy | `small bronze medieval script text with aged parchment texture, enclosed in a small decorative shield or banner shape` |
| Historical / Military | `small dignified white Song typeface text above a double horizontal line in dark red` |
| Supernatural / Horror | `small faded grey-green text slightly tilted, with a thin dripping ink line above` |
| Light Novel | `small playful rounded white text with pastel color outline, tiny star decorations on both sides` |

**Author Name General Rules:**
- Size: `small` (not so large it steals title focus, not so small it's unreadable)
- Position: `at bottom center`, maintain appropriate spacing from bottom edge
- Must have decorative element: at least one of line / border / small icon / glow
- Color contrasts with background but not harsh

#### Style Layer: Platform Style

Platform style description keywords come exclusively from [references/cover-styles.md](references/cover-styles.md) "Platform Styles" section — use the corresponding keyword string directly for the target platform; no duplicate maintenance here to avoid drift from the reference file.

#### Scene Layer: Genre + Composition

Read genre's style tags, colors, character, background descriptions from [references/cover-styles.md](references/cover-styles.md).

Composition variants (first output 2-3 options):

| Option | Composition | Suitable Genres |
|:------|:-----------|:----------------|
| A | Character close-up + scene | All genres |
| B | Full body + dynamic pose | Xianxia, Urban, Western Fantasy |
| C | Pure scene / atmosphere | Mystery, Sci-Fi, Historical |

#### Complete Prompt Template

```
Chinese web novel cover design, [platform style].
Title text '{title}' at top center in [title font style].
Author name '{author}' at bottom center in [author name font style — from table above].
[genre style tags]. [character description]. [background description].
[color directive]. [lighting directive].
Professional book cover, high detail digital painting, portrait [platform ratio: Fanqie=3:4, default=2:3] ratio, keep title and author name inside the central safe area away from edges (inner ~85%), no watermark
```

#### Prompt Tips (Verified)

- More specific character description = better: specify clothing, pose, hairstyle, expression, props
- Layered background: foreground (character/props) → midground (scene: peaks/buildings/forest) → far ground (atmosphere: cloud sea/stars/fire)
- Lighting = specify light source direction + color (e.g., `dramatic golden light from above`)
- Use `digital painting style` not `photo` — avoids photographic realism

### Step 4: Generate & Save

#### Codex Built-in ImageGen (Preferred)

1. Call `image_gen` with the complete prompt from Step 3. Ratio and safe area go in the prompt; do not pass `GPT_IMAGE_MODEL`, `GPT_IMAGE_SIZE`, `response_format`, etc.
2. If `REF_IMAGE` is set, load local file via image viewer tool into session first; for URL, download then load. Specify whether it's an edit target or style reference, and list what must be preserved.
3. Each composition option = one call. Create `BOOK_DIR/封面/` first, then copy tool's returned image as `封面_vN.png` (N auto-increments, no overwrite); keep `$CODEX_HOME/generated_images/` original, also save same-name `.prompt.txt`; if reference image, also save `.ref.txt`. Confirm image readable, pass original absolute path to Step 5.

#### API Fallback

`gpt-image-2` always returns base64; request body must NOT include `response_format` (legacy DALL-E param, unsupported by gpt-image series). `$PROMPT` = complete prompt assembled in Step 3.

Two modes — pick one: no `REF_IMAGE` → text-to-image; `REF_IMAGE` set → image-to-image.

#### Text-to-Image (Default)

```bash
set -euo pipefail
: "${GPT_IMAGE_API_KEY:?Please set export GPT_IMAGE_API_KEY=your_key}"
: "${PROMPT:?Please first export PROMPT=complete prompt from build-prompt step}"
BASE_URL="${GPT_IMAGE_BASE_URL:-https://api.openai.com/v1}"
MODEL="${GPT_IMAGE_MODEL:-gpt-image-2}"
SIZE="${GPT_IMAGE_SIZE:-1024x1536}"
BOOK_DIR="${BOOK_DIR:?Please first export BOOK_DIR=./covers/<title>}"

mkdir -p "$BOOK_DIR/封面"

# Auto-increment version to avoid overwriting previous covers
i=1
while [ -f "$BOOK_DIR/封面/封面_v${i}.png" ]; do i=$((i+1)); done
OUT="$BOOK_DIR/封面/封面_v${i}.png"
RESP=$(mktemp)
trap 'rm -f "$RESP"' EXIT

# Use jq to build JSON body — avoids shell quoting issues with quotes/newlines/CJK in PROMPT
BODY=$(jq -n \
  --arg m "$MODEL" \
  --arg p "$PROMPT" \
  --arg s "$SIZE" \
  '{model:$m, prompt:$p, size:$s}')

curl -fsS --max-time 180 --retry 2 --retry-delay 5 \
  "$BASE_URL/images/generations" \
  -H "Authorization: Bearer $GPT_IMAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$BODY" > "$RESP"

# Fail fast on API error — don't write error JSON as base64 → corrupted PNG
if jq -e '.error' "$RESP" >/dev/null 2>&1; then
  echo "API error:" >&2
  jq '.error' "$RESP" >&2
  exit 1
fi

# `// empty` makes missing fields output empty string not "null"; combined with -s check avoids writing 3-byte fake PNG
jq -er '.data[0].b64_json // empty' "$RESP" | base64 --decode > "$OUT"
[ -s "$OUT" ] || { echo "empty or malformed output: $OUT" >&2; head -c 300 "$RESP" >&2; exit 1; }

# Save prompt copy for iteration/tweaking later
printf '%s\n' "$PROMPT" > "${OUT%.png}.prompt.txt"

file "$OUT"
ls -lt "$BOOK_DIR/封面/"
```

#### Image-to-Image (When Reference Image Provided)

`/v1/images/edits` uses `multipart/form-data` — **CANNOT** use `Content-Type: application/json`. Text fields use `--form-string` (avoids `@` misinterpreted as file reference), image field uses `-F image=@path`.

```bash
set -euo pipefail
: "${GPT_IMAGE_API_KEY:?Please set export GPT_IMAGE_API_KEY=your_key}"
: "${PROMPT:?Please first export PROMPT=complete prompt from build-prompt step}"
BASE_URL="${GPT_IMAGE_BASE_URL:-https://api.openai.com/v1}"
MODEL="${GPT_IMAGE_MODEL:-gpt-image-2}"
SIZE="${GPT_IMAGE_SIZE:-1024x1536}"
BOOK_DIR="${BOOK_DIR:?Please first export BOOK_DIR=./covers/<title>}"
REF_IMAGE="${REF_IMAGE:?Please first export REF_IMAGE=local path or URL}"

mkdir -p "$BOOK_DIR/封面"

# Auto-increment version
i=1
while [ -f "$BOOK_DIR/封面/封面_v${i}.png" ]; do i=$((i+1)); done
OUT="$BOOK_DIR/封面/封面_v${i}.png"
RESP=$(mktemp)
REF_TMP=""
trap '[ -n "$REF_TMP" ] && rm -f "$REF_TMP"; rm -f "$RESP"' EXIT

# URL → download to temp file; local path → use directly. Bare mktemp for macOS/Linux consistency.
case "$REF_IMAGE" in
  http://*|https://*)
    REF_TMP=$(mktemp)
    curl -fsSL --max-time 60 -o "$REF_TMP" "$REF_IMAGE"
    REF_LOCAL="$REF_TMP"
    ;;
  *)
    [ -f "$REF_IMAGE" ] || { echo "Reference image not found: $REF_IMAGE" >&2; exit 1; }
    REF_LOCAL="$REF_IMAGE"
    ;;
esac

curl -fsS --max-time 240 --retry 2 --retry-delay 5 \
  "$BASE_URL/images/edits" \
  -H "Authorization: Bearer $GPT_IMAGE_API_KEY" \
  --form-string "model=$MODEL" \
  --form-string "size=$SIZE" \
  --form-string "prompt=$PROMPT" \
  -F "image=@$REF_LOCAL" > "$RESP"

if jq -e '.error' "$RESP" >/dev/null 2>&1; then
  echo "API error:" >&2
  jq '.error' "$RESP" >&2
  exit 1
fi

# `// empty` makes missing fields output empty string not "null"; with -s check avoids writing 3-byte fake PNG
jq -er '.data[0].b64_json // empty' "$RESP" | base64 --decode > "$OUT"
[ -s "$OUT" ] || { echo "empty or malformed output: $OUT" >&2; head -c 300 "$RESP" >&2; exit 1; }

printf '%s\n' "$PROMPT"    > "${OUT%.png}.prompt.txt"
printf '%s\n' "$REF_IMAGE" > "${OUT%.png}.ref.txt"

file "$OUT"
ls -lt "$BOOK_DIR/封面/"
```

### Step 5: Export Platform Upload Size (When Platform Has Fixed Pixels)

When platform has fixed upload pixels (Fanqie 600×800), center-crop+scale the original to upload size — whether generated at 2:3 or 3:4, crop to exact platform pixels, no distortion, avoids platform re-cropping off title/byline. Original retained, save `_上传` version; `SRC` and `TARGET` use prior step task values directly, no cross-shell temp vars:

```bash
SRC='<Step 4 generated original image absolute path>'
TARGET='<Step 1 determined platform upload size; empty if none>'
[ -f "$SRC" ] || { echo "Cover original not found: $SRC" >&2; exit 1; }
if [ -n "$TARGET" ] && [ -f "$SRC" ]; then
  UP="${SRC%.png}_上传.png"; W="${TARGET%x*}"; H="${TARGET#*x}"
  if command -v magick >/dev/null 2>&1; then M=magick
  elif command -v convert >/dev/null 2>&1; then M=convert; else M=""; fi
  if [ -n "$M" ]; then
    "$M" "$SRC" -resize "${W}x${H}^" -gravity center -extent "${W}x${H}" "$UP"  # scale to fill then center crop
  elif command -v sips >/dev/null 2>&1; then
    cp "$SRC" "$UP"
    sw=$(sips -g pixelWidth "$UP" | awk '/pixelWidth/{print $NF}')
    sh=$(sips -g pixelHeight "$UP" | awk '/pixelHeight/{print $NF}')
    if [ $((sw*H)) -ge $((sh*W)) ]; then sips --resampleHeight "$H" "$UP" >/dev/null
    else sips --resampleWidth "$W" "$UP" >/dev/null; fi
    sips -c "$H" "$W" "$UP" >/dev/null   # sips -c is height width, center crop
  else
    echo "No magick/convert/sips, skipping; manually center-crop+scale $SRC to $TARGET then upload" >&2
  fi
  [ -f "$UP" ] && file "$UP"
fi
```

> Title/byline already placed in center safe area in prompt — center crop won't cut them.

### Step 6: Quality Check + Iterate

| Check Item | Standard |
|:----------|:--------|
| Text rendering | Title clearly legible, font style matches genre |
| Genre match | Visual style consistent with title genre |
| Composition | Subject prominent, text doesn't obscure key art |
| Platform fit | Matches target platform's cover tone |
| Platform size | Ratio matches platform; scaled to upload size title/byline fully visible, not cropped |

When unsatisfied: swap composition, adjust palette, change font style, change platform style.

---

## References

| File | When to Load |
|:-----|:------------|
| [references/cover-styles.md](references/cover-styles.md) | Genre→visual style mapping, platform style details, prompt templates |

---

## Language

- Reply in the user's language — whatever language the user uses, reply in that language
- Chinese replies follow the "Chinese Copywriting Layout Guide"