---
name: story-cover
version: 1.0.0
description: "Novel cover generation. Automatically analyzes genre and style from the book title and author name, then uses GPT-Image-2 to generate a professional web-fiction cover containing the title and byline; Codex CLI prioritizes built-in ImageGen and requires no separate API key. Triggers: /story-cover, /封面, “help me make a cover,” “generate a cover image,” “make a novel cover,” or “cover design.”"
metadata: {"openclaw":{"requires":{"env":["GPT_IMAGE_API_KEY"],"bins":["curl","jq","base64"]},"primaryEnv":"GPT_IMAGE_API_KEY","source":"https://github.com/zenstory-ai/oh-story-claudecode"}}
---
# story-cover: Novel Cover Generation

You are a novel cover designer. Based on the title and genre, use GPT-Image-2 to generate a complete cover containing the book title and author name in a single pass.

**Core principle: A cover is the reader’s first impression. It should communicate the genre and mood at a glance.**

---

## Generation Paths

- **Built into Codex (preferred)**: When `$imagegen` / `image_gen` is available in the current Codex CLI session, generate the image directly and save it to disk. This counts against general Codex usage, requires neither `OPENAI_API_KEY` nor `GPT_IMAGE_API_KEY`, and does not run `curl`. `story-cover` calls the tool itself; do not ask the user to run a separate command.
- **API fallback**: Use only when the session has no built-in tool or the user explicitly requests the API. Requires `GPT_IMAGE_API_KEY`. A missing tool does not mean the user’s Codex subscription lacks image generation; if a built-in call fails, report the error first rather than silently switching to a potentially billable API.

## Output Parameters and API Fallback Environment Variables

| Variable | Required | Default | Description |
|:-----|:----:|:-----|:-----|
| `GPT_IMAGE_API_KEY` | Required for API fallback | — | OpenAI or compatible proxy API key; not used by the built-in Codex path |
| `GPT_IMAGE_BASE_URL` | | `https://api.openai.com/v1` | Change this when using a compatible proxy |
| `GPT_IMAGE_MODEL` | | `gpt-image-2` | Override only when testing a new model |
| `GPT_IMAGE_SIZE` | | `1024x1536` | Target aspect-ratio hint for the API fallback (Tomato 3:4 → `768x1024`; default 2:3 → `1024x1536`). Official gpt-image-2 accepts any dimensions divisible by 16 (ratio ≤ 3:1), but **many proxy services ignore size and return a preset ratio of about 2:3** (verified in testing). Do not rely on this for platform dimensions; the “Export Platform Upload Dimensions” step provides the fallback guarantee. |
| `UPLOAD_SIZE` | | — | Platform’s fixed upload dimensions (Tomato: `600x800`). When set, the “Export Platform Upload Dimensions” step center-crops and resizes an upload-ready copy without distortion or dependence on the generated image dimensions. |
| `BOOK_DIR` | ✅ | — | Output directory; recommended: `./covers/<书名>` |
| `REF_IMAGE` | | — | Local path or URL for a reference image. When set, switch to image-to-image generation: load the image into the session for the built-in path, or use `images/edits` for the API fallback. |

---

## Generation Workflow

### Step 1: Gather Information

Required: book title, author name (pen name), target platform, and output directory `BOOK_DIR` (recommended: `./covers/<书名>`; use an environment variable for the API fallback and the current task value directly for the built-in path)
Optional: reference image `REF_IMAGE` (local path or URL; when set, switch to image-to-image generation), style preferences, and dimensions

> **The book title and pen name are required cover information**: If either is missing, use AskUserQuestion to ask the user for it before proceeding. Never invent or omit either value.

**Choose cover dimensions based on the target platform**: Tomato’s 600×800 upload size has a **3:4** ratio, not 2:3. If the generated ratio is wrong, the platform’s secondary crop may cut off the title or pen name.

| Platform | Upload Dimensions | Ratio | Generated `GPT_IMAGE_SIZE` (when possible) |
|:-----|:--------|:-----|:-------------------|
| Tomato Novel | 600×800 | 3:4 | `768x1024` |
| Other platforms (default portrait) | Follow platform specifications | 2:3 | `1024x1536` |

For the built-in path, include the target ratio in the prompt. For the API fallback, also `export GPT_IMAGE_SIZE` (many proxies ignore it and return about 2:3). When a platform has fixed upload dimensions, set `UPLOAD_SIZE` (Tomato: `600x800`). **The final platform dimensions are guaranteed by the center-crop-and-resize operation in “Export Platform Upload Dimensions,” regardless of the image’s actual generated dimensions.** See [references/cover-styles.md](references/cover-styles.md) for platform and genre styles.

### Step 2: Determine the Genre

Scan the book title (and synopsis when needed) for keywords, then select a genre using the “Genre Inference Rules” table in [references/cover-styles.md](references/cover-styles.md).

- One genre match → use it directly
- Multiple genre matches → choose the highest-priority match: xianxia > Western fantasy > historical romance > contemporary romance > urban > mystery > science fiction > historical > supernatural > light novel
- No matches → default to `都市`

### Step 3: Build the Prompt

Prompt = **text layer** + **style layer** + **visual layer**, written entirely in English.

#### Text Layer: Typography for the Book Title and Author Name

Include the Chinese book title and author name directly in the prompt; GPT-Image-2 can render them. **Describe the typography in detail**:

```
Title text '书名' at top center in [书名字体风格].
Author name '作者名' at bottom center in [作者名字体风格].
```

#### Book Title Typography

| Genre | Descriptive Keywords |
|:-----|:-----------|
| Fantasy/xianxia | `bold golden brush calligraphy with metallic glow and sharp strokes` |
| Urban | `modern bold sans-serif with metallic silver finish` |
| Historical romance/palace intrigue | `elegant golden traditional Kai script with ornate decoration` |
| Contemporary romance/sweet romance | `soft rounded handwritten style in white with pink glow` |
| Mystery/detective | `distorted bold cracked letters in blood red` |
| Science fiction/post-apocalyptic | `neon glowing futuristic font in electric blue` |
| Western fantasy | `metallic embossed fantasy lettering with glow effect` |
| Historical/military | `heavy stone-carved seal script in deep red` |
| Supernatural/horror | `eerie dripping handwritten font in sickly green` |
| Light novel | `colorful cartoon outlined bubbly font` |

#### Author Name Typography (Important: The Author Name Must Be Carefully Designed, Not Merely “Small Text”)

Although smaller, the author name is essential to a professional-looking cover. Always specify the **font + color + decorative element**, complementing the title style without competing for attention.

| Genre | Author Name Style Prompt |
|:-----|:----------------|
| Fantasy/xianxia | `small refined white serif text with faint golden glow, flanked by delicate cloud-scroll ornaments on both sides, resting on a thin horizontal gold line` |
| Urban | `small clean white modern text with subtle drop shadow, positioned above a thin silver horizontal divider line` |
| Historical romance/palace intrigue | `small elegant dark red traditional text inside a thin golden rectangular border frame with corner decorations` |
| Contemporary romance/sweet romance | `small soft pink-white handwritten text with a tiny heart motif on the left side, light sparkle effect` |
| Mystery/detective | `small pale grey text with slight blur effect, almost hidden in the shadows, a thin cracked line underneath` |
| Science fiction/post-apocalyptic | `small crisp white monospace text with subtle cyan scanline overlay, flanked by small geometric brackets` |
| Western fantasy | `small bronze medieval script text with aged parchment texture, enclosed in a small decorative shield or banner shape` |
| Historical/military | `small dignified white Song typeface text above a double horizontal line in dark red` |
| Supernatural/horror | `small faded grey-green text slightly tilted, with a thin dripping ink line above` |
| Light novel | `small playful rounded white text with pastel color outline, tiny star decorations on both sides` |

**Universal author-name rules**:
- Size: `small` (not so large that it competes with the title, but not too small to read)
- Position: `at bottom center`, with appropriate spacing from the bottom edge
- Must include at least one decorative element: line, border, small icon, or glow
- Color must contrast with the background without looking harsh

#### Style Layer: Platform Style

Platform-style keywords come exclusively from the “Platform Styles” section of [references/cover-styles.md](references/cover-styles.md). Use the keyword string for the target platform directly; do not maintain a duplicate here that could drift from the reference file.

#### Visual Layer: Genre + Composition

Read the genre-specific style tags, palette, character, and background descriptions from [references/cover-styles.md](references/cover-styles.md).

Composition variants (provide 2–3 concepts initially):

| Concept | Composition | Best For |
|:-----|:-----|:---------|
| A | Character close-up + setting | All genres |
| B | Full-body portrait + dynamic pose | Fantasy, urban, Western fantasy |
| C | Environment/atmospheric image only | Mystery, science fiction, historical |

#### Complete Prompt Template

```
Chinese web novel cover design, [平台风格].
Title text '{书名}' at top center in [书名字体风格].
Author name '{作者名}' at bottom center in [作者名字体风格 — 从上表选择].
[题材风格标签]. [人物描述]. [背景描述].
[色彩指令]. [光效指令].
Professional book cover, high detail digital painting, portrait [平台比例：番茄=3:4，默认=2:3] ratio, keep title and author name inside the central safe area away from edges (inner ~85%), no watermark
```

#### Prompt Techniques (Validated in Testing)

- Make character descriptions as specific as possible: define clothing, pose, hairstyle, expression, and props
- Layer the background: foreground (character) → middle ground (setting) → background (atmosphere)
- Specify lighting with a direction and color (for example, `dramatic golden light from above`)
- Use `digital painting style` rather than `photo` to avoid a live-action photographic look

### Step 4: Generate and Save

#### Built-in Codex ImageGen (Preferred)

1. Call `image_gen` with the complete prompt from Step 3. Put the ratio and safe area in the prompt; do not pass API parameters such as `GPT_IMAGE_MODEL`, `GPT_IMAGE_SIZE`, or `response_format`.
2. When `REF_IMAGE` is set, load a local file into the session with the image-viewing tool. Download a URL first, then load it. State whether it is the edit target or a style reference, and list the content that must be preserved.
3. Make a separate call for each composition concept. Create `BOOK_DIR/封面/` first, then copy each returned image to `封面_vN.png`, incrementing `N` without overwriting earlier versions. Preserve the original file under `$CODEX_HOME/generated_images/`, save a matching `.prompt.txt`, and, when a reference image is present, save `.ref.txt` as well. Confirm that the image is readable and pass its absolute path to Step 5.

#### API Fallback

`gpt-image-2` always returns base64. Do not include `response_format` in the request body (it is a legacy DALL-E parameter unsupported by the gpt-image family). `$PROMPT` is the complete prompt assembled in the “Build the Prompt” step.

Choose one of two call methods: when `REF_IMAGE` is unset, use “Text-to-Image”; when it is set, use “Image-to-Image.”

#### Text-to-Image (Default)

```bash
set -euo pipefail
: "${GPT_IMAGE_API_KEY:?请设置 export GPT_IMAGE_API_KEY=你的key}"
: "${PROMPT:?请先 export PROMPT=构建提示词步骤拼好的完整提示词}"
BASE_URL="${GPT_IMAGE_BASE_URL:-https://api.openai.com/v1}"
MODEL="${GPT_IMAGE_MODEL:-gpt-image-2}"
SIZE="${GPT_IMAGE_SIZE:-1024x1536}"
BOOK_DIR="${BOOK_DIR:?请先 export BOOK_DIR=./covers/<书名>}"

mkdir -p "$BOOK_DIR/封面"

# 自增版本号，避免覆盖之前生成的封面
i=1
while [ -f "$BOOK_DIR/封面/封面_v${i}.png" ]; do i=$((i+1)); done
OUT="$BOOK_DIR/封面/封面_v${i}.png"
RESP=$(mktemp)
trap 'rm -f "$RESP"' EXIT

# 用 jq 拼 JSON 体，避免 PROMPT 里的引号/换行/中文把 shell 字符串撑破
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

# API 出错时早退，避免把 error JSON 当成 base64 写成损坏 PNG
if jq -e '.error' "$RESP" >/dev/null 2>&1; then
  echo "API error:" >&2
  jq '.error' "$RESP" >&2
  exit 1
fi

# `// empty` 让缺失字段输出空串而非 "null"，配合下面的 -s 检查避免写出 3 字节假 PNG
jq -er '.data[0].b64_json // empty' "$RESP" | base64 --decode > "$OUT"
[ -s "$OUT" ] || { echo "empty or malformed output: $OUT" >&2; head -c 300 "$RESP" >&2; exit 1; }

# 落地提示词副本，方便迭代时基于上一次微调
printf '%s\n' "$PROMPT" > "${OUT%.png}.prompt.txt"

file "$OUT"
ls -lt "$BOOK_DIR/封面/"
```

#### Image-to-Image (When a Reference Image Is Provided)

`/v1/images/edits` uses `multipart/form-data` and **cannot** use `Content-Type: application/json`. Use `--form-string` for text fields (to prevent `@` from being mistaken for a file reference), and `-F image=@path` for the image field.

```bash
set -euo pipefail
: "${GPT_IMAGE_API_KEY:?请设置 export GPT_IMAGE_API_KEY=你的key}"
: "${PROMPT:?请先 export PROMPT=构建提示词步骤拼好的完整提示词}"
BASE_URL="${GPT_IMAGE_BASE_URL:-https://api.openai.com/v1}"
MODEL="${GPT_IMAGE_MODEL:-gpt-image-2}"
SIZE="${GPT_IMAGE_SIZE:-1024x1536}"
BOOK_DIR="${BOOK_DIR:?请先 export BOOK_DIR=./covers/<书名>}"
REF_IMAGE="${REF_IMAGE:?请先 export REF_IMAGE=本地路径或 URL}"

mkdir -p "$BOOK_DIR/封面"

# 自增版本号
i=1
while [ -f "$BOOK_DIR/封面/封面_v${i}.png" ]; do i=$((i+1)); done
OUT="$BOOK_DIR/封面/封面_v${i}.png"
RESP=$(mktemp)
REF_TMP=""
trap '[ -n "$REF_TMP" ] && rm -f "$REF_TMP"; rm -f "$RESP"' EXIT

# URL 先下载到临时文件，本地路径直接用。用裸 mktemp 以保证 macOS/Linux 行为一致。
case "$REF_IMAGE" in
  http://*|https://*)
    REF_TMP=$(mktemp)
    curl -fsSL --max-time 60 -o "$REF_TMP" "$REF_IMAGE"
    REF_LOCAL="$REF_TMP"
    ;;
  *)
    [ -f "$REF_IMAGE" ] || { echo "参考图不存在: $REF_IMAGE" >&2; exit 1; }
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

# `// empty` 让缺失字段输出空串而非 "null"，配合 -s 检查避免写出 3 字节假 PNG
jq -er '.data[0].b64_json // empty' "$RESP" | base64 --decode > "$OUT"
[ -s "$OUT" ] || { echo "empty or malformed output: $OUT" >&2; head -c 300 "$RESP" >&2; exit 1; }

printf '%s\n' "$PROMPT"    > "${OUT%.png}.prompt.txt"
printf '%s\n' "$REF_IMAGE" > "${OUT%.png}.ref.txt"

file "$OUT"
ls -lt "$BOOK_DIR/封面/"
```

### Step 5: Export Platform Upload Dimensions (When the Platform Specifies Fixed Pixels)

When a platform requires fixed upload dimensions (Tomato: 600×800), **center-crop and resize** the original image to those dimensions. Whether the generated image is 2:3 or 3:4, this produces exact platform pixels without distortion and prevents the platform from cropping out the title or pen name. Preserve the original and save the upload copy with an `_上传` suffix. Use the task values from the preceding steps directly for `SRC` and `TARGET`; do not depend on temporary variables from another shell:

```bash
SRC='<Step 4 生成的原图绝对路径>'
TARGET='<Step 1 确定的平台上传尺寸；无则留空>'
[ -f "$SRC" ] || { echo "封面原图不存在: $SRC" >&2; exit 1; }
if [ -n "$TARGET" ] && [ -f "$SRC" ]; then
  UP="${SRC%.png}_上传.png"; W="${TARGET%x*}"; H="${TARGET#*x}"
  if command -v magick >/dev/null 2>&1; then M=magick
  elif command -v convert >/dev/null 2>&1; then M=convert; else M=""; fi
  if [ -n "$M" ]; then
    "$M" "$SRC" -resize "${W}x${H}^" -gravity center -extent "${W}x${H}" "$UP"  # 缩放填满后居中裁
  elif command -v sips >/dev/null 2>&1; then
    cp "$SRC" "$UP"
    sw=$(sips -g pixelWidth "$UP" | awk '/pixelWidth/{print $NF}')
    sh=$(sips -g pixelHeight "$UP" | awk '/pixelHeight/{print $NF}')
    if [ $((sw*H)) -ge $((sh*W)) ]; then sips --resampleHeight "$H" "$UP" >/dev/null
    else sips --resampleWidth "$W" "$UP" >/dev/null; fi
    sips -c "$H" "$W" "$UP" >/dev/null   # sips -c 是 高 宽，居中裁
  else
    echo "无 magick/convert/sips，跳过；手动把 $SRC 居中裁剪+缩放到 $TARGET 再上传" >&2
  fi
  [ -f "$UP" ] && file "$UP"
fi
```

> The prompt keeps the book title and pen name inside the central safe area, so center-cropping will not cut them off.

### Step 6: Quality Check + Iteration

| Check | Standard |
|:-------|:-----|
| Text rendering | Book title is clear and legible; typography suits the genre |
| Genre match | Visual style matches the title’s genre |
| Composition | Subject stands out; text does not cover essential artwork |
| Platform fit | Matches the target platform’s cover conventions and tone |
| Platform dimensions | Ratio matches the platform; after resizing to upload dimensions, the title and pen name remain fully visible and uncropped |

If the result is unsatisfactory, change the composition, adjust the palette, select a different typography style, or change the platform style.

---

## References

| File | When to Load |
|:-----|:---------|
| [references/cover-styles.md](references/cover-styles.md) | Genre-to-visual-style mappings, platform style details, and prompt templates |

---

## Language

- Reply in the user’s language
- Chinese responses must follow the Chinese Copywriting Style Guide
