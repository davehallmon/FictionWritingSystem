# Novel Cover Visual Style Library

Visual style definitions for web-novel covers by genre, used to build GPT-Image-2 English prompts.

---

## Platform Styles

### Fanqie Novel

Visual: high saturation & contrast / character 60%+ face clear / title large bold with glow (gold/red/white) / headshot composition + ornate background  
Keywords: `vibrant saturated colors, eye-catching bold design, character portrait dominating frame, mass-market novel cover style, high contrast`

### Qidian (Qidian Chinese Network)

Visual: refined semi-realistic illustration / composition with rich layers / title in traditional brush calligraphy / muted colors / character & scene balanced, cinematic feel  
Keywords: `polished refined illustration, detailed cinematic composition, epic atmospheric, mature sophisticated style, premium quality`

### Jinjiang

Visual: soft tones (pink/purple/light blue/warm white) / ethereal pretty art, large eyes delicate features / petal bokeh silk jewelry decoration / centered symmetric composition clean / title elegant cursive/rounded  
Keywords: `dreamy ethereal aesthetic, soft pastel tones, elegant romantic, delicate beauty, flower petals and bokeh`

### Zhihu Yanyan

Visual: heavy negative space minimalist / cool tones (gray/blue/white/dark) / atmosphere > character detail, often scene/object/abstract imagery / title modern clean sans-serif / indie film poster texture  
Keywords: `minimalist literary style, clean composition with negative space, subtle moody atmosphere, independent film poster aesthetic`

### Qimao (7cat)

Visual: extreme saturation high impact / character lavish costumes gear / fire lightning spirit effects / title huge glowing dominates frame / poster feel high info density  
Keywords: `striking high-impact design, vivid dramatic colors, spectacular visual effects, attention-grabbing poster style`

### Ciweimao

Visual: anime illustration 2D / bright colors clean linework / chibi elements / title cartoon hand-drawn / lighthearted lively  
Keywords: `anime illustration style, vibrant colorful, detailed character art, Japanese light novel aesthetic`

---

## Genre Inference Rules

| Keywords | Genre | Style Tags |
|:---------|:------|:-----------|
| 仙/道/剑/灵/修/宗/天/帝/尊/神 | Xianxia / Fantasy | xianxia fantasy |
| 都市/总裁/校园/重生/系统/学霸/医生/兵王 | Urban | urban modern |
| 妃/皇/侯/宫/嫡/庶/后/朝/凤/鸾 | Ancient Romance | ancient romance |
| 总裁/契约/替嫁/甜宠/娇妻/萌宝/闪婚 | Modern Romance | modern romance |
| 诡/案/侦探/悬疑/推理/密室/连环 | Mystery | mystery thriller |
| 星际/末世/机甲/赛博/废土/进化 | Sci-Fi | sci-fi |
| 龙/骑/魔法/异世界/精灵/领主 | Western Fantasy | western fantasy |
| 三国/大明/大唐/战场/将军/谋士 | Historical | historical epic |
| 鬼/僵尸/阴阳/风水/盗墓/咒 | Supernatural | supernatural horror |
| 萌/喵/团宠/娇/转生 | Light Novel | light novel |

---

## Prompt Construction Formula

```
[Platform Style] + [Text Layer: Title+Author+Font Design] + [Genre Style Tags] + [Character Description]
+ [Background Elements] + [Color Directive] + [Lighting Directive] + [Universal Modifiers]
```

Universal modifiers: `professional book cover design, high detail digital painting, portrait orientation 2:3 ratio, no watermark`

Text layer MUST specify: title content + position (top center) + font style + color; author name content + position (bottom center) + font style + color

---

## Prompt Tips

### Text Rendering

GPT-Image-2 can render Chinese directly. Format:
```
Title text '书名' at top center in {font style}
Author name '作者名' at bottom center in {font style}
```

### Character Description — Be Specific

Not "a man", but:
```
a young man in flowing white silk robes with gold embroidery,
long black hair tied in a topknot with a jade crown,
piercing dark eyes, confident expression,
holding a glowing blue spirit sword
```

### Background Three Layers

Foreground (character/props) → Midground (scene: peaks/buildings/forest) → Far ground (atmosphere: cloud sea/stars/fire)

### Lighting

| Lighting | Keywords | Feel |
|:--------|:---------|:-----|
| Divine | `dramatic golden light from above` | Sacred |
| Mysterious | `cold moonlight from the left casting long shadows` | Mysterious |
| Warm | `warm sunset glow backlighting the figure` | Warm |
| Sci-Fi | `neon blue and purple lights from below` | Sci-Fi |

### Avoid Photographic Look

Add `digital painting style` — web-novel covers need illustration feel.

### Composition Variants

| Type | Keywords | Use Case |
|:-----|:---------|:---------|
| Character close-up | `close-up portrait, face filling upper half` | Emphasize character |
| Full body | `full body shot, dynamic pose` | Show costume/action |
| Pure scene | `no human figure, landscape composition` | Mystery/Sci-Fi |
| Two characters | `two figures facing each other` | Romance |

---

## Style Library

### Xianxia / Fantasy

**Tags**: `xianxia Chinese fantasy art style, ethereal atmosphere`  
**Colors**: cyan-blue + gold + dark-blue, cool tones dominant, gold/warm light accents  
**Characters**: male — long hair crown/loose, holding sword/artifact, robes flowing | female — immortal dress flowing, spirit beast companion, lotus decoration  
**Background**: cloud sea, immortal mountains, ancient pavilions, spirit energy effects  
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
**Colors**: deep blue + gray + gold, neon accents (night) / warm orange (sunset)  
**Characters**: male — suit/casual sharp confident silhouette | female — fashionable confident expression  
**Background**: city skyline, high-end office, campus, neon streets  
**Lighting**: `sharp city lights, sunset glow reflecting on glass buildings, neon rim light`

### Ancient Romance / Palace Intrigue

**Tags**: `ancient Chinese romance palace drama, elegant classical beauty`  
**Colors**: true red + gold + ink black, magnificent heavy  
**Characters**: female — elaborate court dress phoenix crown hairpins exquisite makeup | male — emperor/general majestic or gentle  
**Background**: palace halls, courtyards, red walls, bead curtains, screens, lanterns  
**Lighting**: `warm lantern light, golden candle glow, silk fabric shimmering`

### Modern Romance / Sweet

**Tags**: `modern romance cover art, soft dreamy warm atmosphere`  
**Colors**: pink + warm white + light gold, warm gentle  
**Characters**: two-character composition dominant, sweet interaction (embrace/eye contact/hand-hold)  
**Background**: cafe, garden, cozy interior, sunset beach  
**Lighting**: `soft warm backlighting, dreamy bokeh, gentle sunset glow`

### Mystery / Thriller

**Tags**: `dark mystery thriller, noir atmosphere, high contrast shadows`  
**Colors**: black + dark gray + dark blue, blood red / cool white accents  
**Characters**: silhouette / half-masked / back view, calm or tense  
**Background**: rainy night streets, old buildings, locked room, dark alleys  
**Lighting**: `dramatic chiaroscuro, single spotlight, rain-slicked reflections`

### Sci-Fi / Post-Apocalyptic

**Tags**: `sci-fi cyberpunk, futuristic technology, post-apocalyptic`  
**Colors**: deep blue + black + silver, neon blue / electric purple / energy green accents  
**Characters**: mecha armor / tactical suit / lab coat, sci-fi weapons / holo interfaces  
**Background**: space, ruined cities, laboratory, space station  
**Lighting**: `holographic blue glow, neon rim lighting, energy arcs`

### Western Fantasy

**Tags**: `western high fantasy, epic medieval atmosphere`  
**Colors**: deep blue + dark gold + silver-white, flame red / magic purple accents  
**Characters**: knight armor / mage robes / ranger leather, with dragon / griffin  
**Background**: castle, dragon nest, magic circle, vast plains  
**Lighting**: `magic spell glow, dramatic stormy sky, firelight from torches`

### Historical / Military

**Tags**: `historical Chinese war epic, grand battlefield panorama`  
**Colors**: iron gray + dark red + earth yellow, gold armor sheen / beacon fire orange accents  
**Characters**: general armor / strategist robes, holding weapons  
**Background**: battlefield, city walls, military camp, beacon fires  
**Lighting**: `dramatic battlefield firelight, smoke-filled sky, sunset over war`

### Supernatural / Horror

**Tags**: `Chinese supernatural horror, eerie ghostly atmosphere`  
**Colors**: ink black + ghostly green + dark red, paper white / candle yellow accents  
**Characters**: daoist robes / ordinary person in uncanny, ghost shadows / paper effigies / jiangshi  
**Background**: cemetery, ancient temple, dark alley, coffin  
**Lighting**: `eerie green glow, flickering candlelight, cold ghostly luminescence`

### Light Novel / 2D

**Tags**: `anime light novel cover, vibrant colorful moe style`  
**Colors**: bright multi-color, starlight / petal accents  
**Characters**: chibi/moe characters, cat ears / wings etc. moe attributes  
**Background**: fantasy world, campus, isekai, starry sky  
**Lighting**: `sparkly star effects, magical particle effects, soft luminous glow`