# Visual Style Library for Novel Covers

Visual-style definitions for web-fiction covers across genres, used to build English prompts for GPT-Image-2.

---

## Platform Styles

### Fanqie Novel

Visuals: highly saturated, high contrast / character occupies 60% or more with a clearly visible face / large, bold title with gold, red, or white lighting effects / close-up portrait composition with an ornate background  
Keywords: `vibrant saturated colors, eye-catching bold design, character portrait dominating frame, mass-market novel cover style, high contrast`

### Qidian

Visuals: polished, detailed, semi-realistic illustration / layered, carefully composed image / title often in traditional regular-script brush calligraphy / restrained colors / cinematic balance between character and setting  
Keywords: `polished refined illustration, detailed cinematic composition, epic atmospheric, mature sophisticated style, premium quality`

### Jinjiang

Visuals: soft pink, purple, pale blue, and warm-white tones / romantic art with large eyes and refined features / petals, bokeh, silk, and jewelry accents / clean, centered, symmetrical composition / elegant running-script or thin rounded title  
Keywords: `dreamy ethereal aesthetic, soft pastel tones, elegant romantic, delicate beauty, flower petals and bokeh`

### Zhihu Yanyan

Visuals: abundant negative space and minimalism / cool gray, blue, white, and dark tones / atmosphere over character detail, often using settings, objects, or abstract imagery / modern minimalist sans-serif title / independent-film poster quality  
Keywords: `minimalist literary style, clean composition with negative space, subtle moody atmosphere, independent film poster aesthetic`

### Qimao

Visuals: extreme saturation and intense impact / elaborate character costumes and equipment / fire, lightning, and spiritual-energy effects / oversized glowing title occupying substantial space / information-dense poster aesthetic  
Keywords: `striking high-impact design, vivid dramatic colors, spectacular visual effects, attention-grabbing poster style`

### Ciweimao

Visuals: Japanese-style anime illustration / bright colors and crisp linework / chibi elements / cartoonish hand-drawn title / lighthearted and lively  
Keywords: `anime illustration style, vibrant colorful, detailed character art, Japanese light novel aesthetic`

---

## Genre-Inference Rules

| Title keywords | Genre | Style tag |
|:-------|:-----|:---------|
| `仙/道/剑/灵/修/宗/天/帝/尊/神` | Fantasy/xianxia | xianxia fantasy |
| `都市/总裁/校园/重生/系统/学霸/医生/兵王` | Urban fiction | urban modern |
| `妃/皇/侯/宫/嫡/庶/后/朝/凤/鸾` | Historical romance | ancient romance |
| `总裁/契约/替嫁/甜宠/娇妻/萌宝/闪婚` | Contemporary romance | modern romance |
| `诡/案/侦探/悬疑/推理/密室/连环` | Mystery | mystery thriller |
| `星际/末世/机甲/赛博/废土/进化` | Science fiction | sci-fi |
| `龙/骑/魔法/异世界/精灵/领主` | Western fantasy | western fantasy |
| `三国/大明/大唐/战场/将军/谋士` | Historical | historical epic |
| `鬼/僵尸/阴阳/风水/盗墓/咒` | Supernatural | supernatural horror |
| `萌/喵/团宠/娇/转生` | Light novel | light novel |

---

## Prompt-Construction Formula

```
[平台风格] + [文字层：书名+作者名+字体设计] + [题材风格标签] + [人物描述]
+ [背景元素] + [色彩指令] + [光效指令] + [通用修饰]
```

Universal modifiers: `professional book cover design, high detail digital painting, portrait orientation 2:3 ratio, no watermark`

The text layer must specify the title content + position (`top center`) + font style + color, and the author name + position (`bottom center`) + font style + color.

---

## Prompt Techniques

### Text Rendering

GPT-Image-2 can render Chinese directly. Format:

```
Title text '书名' at top center in {字体风格}
Author name '作者名' at bottom center in {字体风格}
```

### Make Character Descriptions Specific

Do not use only “a man.” Use:

```
a young man in flowing white silk robes with gold embroidery,
long black hair tied in a topknot with a jade crown,
piercing dark eyes, confident expression,
holding a glowing blue spirit sword
```

### Three Background Layers

Foreground (character/prop) → midground (setting: peak/building/forest) → background (atmosphere: sea of clouds/starfield/flames)

### Lighting

| Lighting | Keywords | Impression |
|------|--------|------|
| Divine | `dramatic golden light from above` | Sacred |
| Mysterious | `cold moonlight from the left casting long shadows` | Mysterious |
| Warm | `warm sunset glow backlighting the figure` | Warm |
| Science-fiction | `neon blue and purple lights from below` | Futuristic |

### Avoid a Live-Action Photograph Look

Add `digital painting style`; web-fiction covers should feel illustrated.

### Composition Variants

| Type | Keywords | Best for |
|:-----|:-------|:-----|
| Character close-up | `close-up portrait, face filling upper half` | Emphasizing the character |
| Full body | `full body shot, dynamic pose` | Showing clothing and action |
| Setting only | `no human figure, landscape composition` | Mystery/science fiction |
| Two characters | `two figures facing each other` | Romance |

---

## Style Library

### Fantasy / Xianxia

**Tags**: `xianxia Chinese fantasy art style, ethereal atmosphere`  
**Colors**: cyan-blue + gold + deep black; primarily cool tones accented by gold or warm light sources  
**Characters**: man—long hair tied under a crown or loose, carrying a sword or ritual artifact, flowing garments | woman—flowing immortal robes, accompanied by a spirit beast, lotus ornamentation  
**Background**: sea of clouds, immortal mountains, ancient pavilions, spiritual-energy effects  
**Lighting**: `divine golden light rays, mystical mist, spiritual energy glow`  
**Example**:

```
Chinese web novel cover, xianxia fantasy style.
Title text '剑道独尊' at top center in bold golden brush calligraphy with metallic glow and sharp strokes.
Author name '青椒炒肉' at bottom center in small refined white serif text with faint golden glow, flanked by delicate cloud-scroll ornaments, resting on a thin horizontal gold line.
A young swordsman in flowing white robes standing on a mountain peak,
holding a glowing blue spirit sword, long black hair flowing in the wind.
Ethereal clouds swirling below, dramatic golden divine light from above,
spiritual energy particles. Dark misty mountain peaks in background.
Color palette: deep blue, gold, white, black.
Professional book cover, high detail digital painting, portrait 2:3 ratio, no watermark
```

### Urban

**Tags**: `modern urban contemporary style, clean cinematic composition`  
**Colors**: deep blue + gray + gold, with neon accents for night scenes or warm orange at dusk  
**Characters**: man—suit or smart casual wear, polished and sharply defined | woman—fashionable clothing and a confident expression  
**Background**: city skyline, executive office, campus, neon street  
**Lighting**: `sharp city lights, sunset glow reflecting on glass buildings, neon rim light`

### Historical Romance / Palace Intrigue

**Tags**: `ancient Chinese romance palace drama, elegant classical beauty`  
**Colors**: imperial red + gold + ink black; opulent and weighty  
**Characters**: woman—ornate formal robes, phoenix crown and swaying hair ornaments, refined makeup | man—an emperor or general, commanding or gentle  
**Background**: palace, courtyard, red walls, beaded curtains, folding screens, lanterns  
**Lighting**: `warm lantern light, golden candle glow, silk fabric shimmering`

### Contemporary Romance / Sweet Romance

**Tags**: `modern romance cover art, soft dreamy warm atmosphere`  
**Colors**: pink + warm white + pale gold; warm and gentle  
**Characters**: primarily a two-person composition with affectionate interaction, such as embracing, meeting eyes, or holding hands  
**Background**: café, garden, cozy interior, sunset beach  
**Lighting**: `soft warm backlighting, dreamy bokeh, gentle sunset glow`

### Mystery / Detective

**Tags**: `dark mystery thriller, noir atmosphere, high contrast shadows`  
**Colors**: black + dark gray + deep blue, accented with blood red or cold white  
**Characters**: silhouette, partially concealed face, or back view; calm or tense  
**Background**: rainy night street, aging building, locked room, dark alley  
**Lighting**: `dramatic chiaroscuro, single spotlight, rain-slicked reflections`

### Science Fiction / Post-Apocalyptic

**Tags**: `sci-fi cyberpunk, futuristic technology, post-apocalyptic`  
**Colors**: deep blue + black + silver, accented with neon blue, electric purple, or energy green  
**Characters**: powered armor, tactical gear, or lab clothing; futuristic weapons or holographic interfaces  
**Background**: space, ruined city, laboratory, space station  
**Lighting**: `holographic blue glow, neon rim lighting, energy arcs`

### Western Fantasy

**Tags**: `western high fantasy, epic medieval atmosphere`  
**Colors**: deep blue + antique gold + silver-white, accented by flame red or magical purple  
**Characters**: knight armor, mage robes, or ranger leathers, accompanied by a dragon or griffin  
**Background**: castle, dragon's lair, magic circle, broad plains  
**Lighting**: `magic spell glow, dramatic stormy sky, firelight from torches`

### Historical / Military

**Tags**: `historical Chinese war epic, grand battlefield panorama`  
**Colors**: iron gray + dark red + ocher, accented by gleaming gold armor or beacon-fire orange  
**Characters**: armored general or robed strategist, carrying a weapon  
**Background**: battlefield, city wall, military camp, beacon fires  
**Lighting**: `dramatic battlefield firelight, smoke-filled sky, sunset over war`

### Supernatural / Horror

**Tags**: `Chinese supernatural horror, eerie ghostly atmosphere`  
**Colors**: ink black + spectral green + dark red, accented by paper white or candle yellow  
**Characters**: a Daoist priest or ordinary person caught in the uncanny; ghostly shadows, paper effigies, or jiangshi  
**Background**: cemetery, ancient temple, dark alley, coffin  
**Lighting**: `eerie green glow, flickering candlelight, cold ghostly luminescence`

### Light Novel / Anime

**Tags**: `anime light novel cover, vibrant colorful moe style`  
**Colors**: bright multicolor palette with starlight or petal accents  
**Characters**: chibi or moe characters with cute traits such as cat ears or wings  
**Background**: fantasy world, school campus, otherworld, starry sky  
**Lighting**: `sparkly star effects, magical particle effects, soft luminous glow`
