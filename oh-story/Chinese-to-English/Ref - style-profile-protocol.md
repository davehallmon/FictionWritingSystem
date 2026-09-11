# Prose-Style Protocol

> **When to load**: Before story-long-analyze Stage 6 executes. Downstream writing skills read `文风.md` directly and do not load this protocol.

## Artifact Definition

`拆文库/{书名}/文风.md` is a whole-book view of writing techniques that aggregates:

- Sentence-length / punctuation / paragraph rhythm (statistics sampled from the source text)
- Dialogue-subtext patterns + differentiation among character voices
- Within-chapter + cross-chapter emotional alternation cycles (how each chapter's tone changes)
- Existing “writing techniques” and “reusable patterns” from `拆文报告.md`
- Tiered imitation guidance (foundation / advanced / adaptation, emphasizing learning techniques without copying plot devices)
- 4–6 source-text anchor passages of 300–500 Chinese characters (for use as example passages)

## File Paths

- **Write**: `拆文库/{书名}/文风.md` (exclusive to analyze)
- **Read**: When this book is explicitly selected as an external benchmark for another project, story-import or story-long-write synchronizes it on first reference to `{项目}/对标/{书名}/文风.md`; story-long-write reads the project's benchmark view, falling back to the breakdown library. The current book being rebuilt by story-import does not use this synchronization path.

## Length Budget

- **Hard upper limit: approximately 4,000 Chinese characters**
- Descriptive content (overall feel + dialogue techniques + emotional-alternation patterns + reusable techniques + tiered imitation guidance) ≤ 1,800 Chinese characters
- 4–6 source-text anchor passages × 300–500 Chinese characters ≈ 1,600–2,400 Chinese characters
- Prohibited imitation + generation record ≤ 100 Chinese characters

## Template

```markdown
# {书名} 文风

## 生成记录
- 参考资料：拆文报告.md、黄金三章深度拆解、章节摘要
- 抽样章节：第 {K1}/{K10}/{K20} 章（每章约 1000 字）
- 生成时间：{date}
- 适用对标书路径：拆文库/{书名}/
- 文风可用：是  # 若原文缺失或锚点不足，写“否：原因”

## 整体语感
- 句长分布：{由 `style-profile-generator.md` Step 4 的跨平台 Python 1-liner 在 3 章拼接样本上确定性测量——短句(<15字)占比 X%、中句(15-30)Y%、长句(>30)Z%、平均句长 N 字、标点密度 M%。一句概括语感。`confidence: high`（数据由脚本算出，不是抽样估计）。}
  - confidence: high | med | low
- 标点习惯：{破折号/省略号/句号/感叹号/分号 的高频用法。附 2-3 个原文短片段示例。}
  - confidence: high | med | low
- 段落节奏：{平均段长、单段单动作 vs 多动作堆叠、断行习惯。}
  - confidence: high | med | low

## 对话技法
- 潜台词模式：{2-3 种典型潜台词手法（问非所答 / 语气反差 / 信息隐瞒等），每种附 1 段原文示例。}
  - confidence: high | med | low
- 对话标签习惯：{说话动词多样性、动作替代说话标签的频率、对话与动作的穿插比例。}
- 角色语气区分：{主角和 1-2 个核心配角的口头禅/句式差异，引用原文样本句。}

## 情绪交替模式
- 章内基调切换：{统计章节内情节点基调序列——典型章节是否在 紧张↔轻松 或 热血↔温馨 之间切换、切换频率（每章 N 次）。}
  - confidence: high | med | low
- 跨章基调周期：{前 20 章「章基调」序列，识别“虐 3 章爽 1 章”之类周期。}
- 喜剧↔重击的转场手法：{对标书在 轻松→悲伤 锐角转场时用了什么手法，举 1-2 个原文锚点。}

## 可借鉴技巧（从 拆文报告.md 直接引用）
- 写法技巧 Top 5：
  1. {技巧名}：{一句话用法说明}
  2. ...
- 可借鉴套路 Top 3：
  1. {套路名}：{适用场景}
  2. ...

## 分层模仿建议
- 基础层（必学）：{词汇偏好、句式节奏、对话标签、描写重心中最容易迁移的 3-5 条；只学表达习惯，不复制原句}
- 进阶层（结构）：{节奏推进、伏笔埋回、视角切换、场景衔接中最值得复用的 3-5 条；替换人物/场景/道具后再使用}
- 适配层（本书化）：{哪些技法适合当前项目，哪些会导致人设/题材错位；明确不要搬运专名、标志性台词、独特桥段和事件顺序}

## 原文锚点片段

> 每片段 300-500 字，**用于 narrative-writer 写作时的范例片段**。从 `原文/原文.txt` 按章节分隔符切片。模仿手法、不抄字句。

### 片段 A — 基调：紧张
**出处**：第 {K} 章 第 {段号} 段（行 {L1}-{L2}）
**示范点**：{句长节奏（该处长短如何分布） / 标点位置 / 一笔两用 等}

```
{300-500 字原文}
```

### 片段 B — 基调：悲伤/压抑
**出处**：第 {K} 章 第 {段号} 段（行 {L1}-{L2}）
**示范点**：{对话潜台词手法}

```
{300-500 字原文}
```

### 片段 C — 基调：轻松/搞笑
**出处**：第 {K} 章 第 {段号} 段（行 {L1}-{L2}）
**示范点**：{句子节奏 / 角色语气区分}

```
{300-500 字原文}
```

### 片段 D — 基调：热血/爽点
**出处**：第 {K} 章 第 {段号} 段（行 {L1}-{L2}）
**示范点**：{爽点铺放比 / 动作描写句长}

```
{300-500 字原文}
```

> 优先覆盖项目可能用到、且对标书中样本充足的基调：紧张、悲伤/压抑、轻松/温馨、热血。按拆文里实际分布挑 4-6 段；缺哪个基调就写“本书该基调样本不足，跳过”，不要编造。

## 不可模仿
- {对标书的明显缺陷或不适合当前项目的技法。可选段落，可空。}
```

### English guide (non-executable)

The protected template above uses these operational headings and fields:

| Chinese literal | English meaning |
|---|---|
| `{书名} 文风` | `{Book Title} Style Profile` |
| `生成记录` | Generation record |
| `参考资料` / `抽样章节` / `生成时间` | Reference materials / sampled chapters / generation time |
| `适用对标书路径` / `文风可用` | Applicable benchmark path / style profile usable |
| `整体语感` | Overall prose feel |
| `句长分布` / `标点习惯` / `段落节奏` | Sentence-length distribution / punctuation habits / paragraph rhythm |
| `对话技法` | Dialogue techniques |
| `潜台词模式` / `对话标签习惯` / `角色语气区分` | Subtext patterns / dialogue-tag habits / character-voice differentiation |
| `情绪交替模式` | Emotional-alternation patterns |
| `章内基调切换` / `跨章基调周期` | Within-chapter tone shifts / cross-chapter tone cycles |
| `喜剧↔重击的转场手法` | Transition technique from comedy to emotional impact |
| `可借鉴技巧` | Reusable techniques |
| `写法技巧 Top 5` / `可借鉴套路 Top 3` | Top five writing techniques / top three reusable patterns |
| `分层模仿建议` | Tiered imitation guidance |
| `基础层` / `进阶层` / `适配层` | Foundation / structural / project-adaptation tiers |
| `原文锚点片段` | Source-text anchor passages |
| `出处` / `示范点` | Source location / technique demonstrated |
| `紧张` / `悲伤或压抑` / `轻松或温馨` / `热血或爽点` | Tension / sadness or oppression / lightness or warmth / high-energy payoff |
| `不可模仿` | Elements that must not be imitated |

Each anchor passage contains 300–500 Chinese characters from the source manuscript. Select four to six passages representing tones that both matter to the current project and have adequate evidence in the benchmark. If the benchmark lacks a tone, record that the sample is insufficient and skip it; never fabricate an example.

## Semantics of the confidence Field

| Value | Trigger condition | Downstream handling |
|---|---|---|
| `high` | Data is directly readable (for example, the tone sequence is obtained by grep from summaries) | narrative-writer adopts it preferentially, overriding the default Gate |
| `med` | Inferred from an adequate sample (for example, chapter-tone trends or organized dialogue subtext) | narrative-writer treats it as a reference and reconciles it with the default Gate |
| `low` | Sample is insufficient / source text is absent | narrative-writer yields to the default Gate (not mandatory) |

## Availability Semantics

- `文风可用：是` → The prose style may be used for writing; narrative-writer applies it by confidence tier.
- `文风可用：否：{原因}` → Prose-style quality is inadequate (for example, the source is absent or every anchor is a placeholder). When story-explorer reads it, return `gaps.profile_degenerate: true`; narrative-writer skips the prose style and writes under the default Gates to avoid being misled.

## Override and Prohibited-Imitation Principles

- **Override**: Prose style ranks above Gate D (rhythm adjustment), Gate B (removing formulaic sentence patterns), and default punctuation habits. These Gates are **defaults** for removing AI-like qualities; when the prose-style profile gives more specific instructions, it wins.
- **Cannot be overridden (hard constraints)**: banned-words / Gate F prohibition on end-of-chapter moralizing / prohibition on universal or stacked metaphors / prohibition on chapter-end previews / minimum word count. These hard constraints always win, even when the style example does the opposite.

For the exact resolution table, see the “invocation protocol” section of `.claude/agents/narrative-writer.md`.
