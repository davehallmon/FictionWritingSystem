# Genre Style Modules

> Core principles, key techniques, and writing guidelines for each genre. After choosing a genre direction, consult the corresponding module.

---

## Decision Guide

| What You Are Doing | Module to Consult |
|-----------|-------------|
| Writing humor/comedy/absurd comedy | Humor / Comedy Fiction / Absurdist Style |
| Writing suspense/mystery/horror | Suspense / Mystery / Horror |
| Writing romance/redemption | Romance / Conflict Design for Redemption Fiction |
| Writing fantasy/xuanhuan/cultivation | Fantasy/Xuanhuan + Progression/Power Fantasy |
| Writing realism/social observation/new media | Realism/Social Observation |
| Writing light novels/anime-inspired fiction | Light-Novel/Anime-Inspired Style |
| Writing cyberpunk | Cyberpunk Style |
| Writing listicle/information-gap/simulation/livestream fiction | Listicle/Information-Gap Fiction / Simulation Fiction / Livestream Fiction |
| Choosing a genre/market lane | Market Positioning and Subject-Selection Strategy -> Audience Reach and Market Lanes -> Following Trends and Innovating |
| Designing an opening | Creative Approach and Opening Design -> Smooth Openings for Low-Status Protagonists -> Five Essentials of an Opening |
| Evaluating genre boundaries | Genre Boundaries and Atmosphere -> Differences Among Platform Styles |
| Generating genre-specific prose cards | `genre-prose-cards.md` index + individual `genre-prose-cards/{题材}.md` card |
| Designing combat/fights | Go to style-combat-face.md |

## Directive Tone

This file is written as a “genre operations manual.” Each module provides the genre's **core rules and operating points**, which are **mandatory constraints** when writing that genre. When combining genres: primary-genre rules > secondary-genre rules > general advice.

## Prose-Card Composition Model

Manuscript writing uses a three-part set: “general prose requirements + genre prose card + this book's style.” It no longer duplicates an entire prose prompt for every genre.

- **General prose requirements** are handled by Phase 4 of `story-long-write`: consume the detailed outline strictly, write to plot-beat obligations, progress slowly, do not write later plot early, and complete deterministic length/hook/prohibited-word/degradation validation.
- **The genre prose card** controls only stable genre-level fundamentals: world or everyday logic, reader expectations, central satisfaction/emotion, pacing density, scene granularity, and prohibited drift. The project first matches through the `genre-prose-cards.md` index, then reads the individual `genre-prose-cards/{题材}.md` card. This file provides only general genre supplements.
- **This book's style** comes from `设定/文风.md` or the comparable `文风.md`: it controls only sentence length, punctuation, subtext, anchor passages, and tone, without overriding the genre core or chapter intent.
- When they conflict: chapter outline and continuity > genre prose card > this book's style > general craft advice.

### Genre Prose Card Template

The project may generate `设定/题材正文提示卡.md` in Phase 2. If that file is absent, before Phase 4 writing, match `设定/题材定位.md` against the `genre-prose-cards.md` index and read the individual `genre-prose-cards/{题材}.md` card. If there is still no match, extract a lightweight card from this file on demand. Keep the card short, pass a summary to `narrative-writer`, and do not copy whole reference passages into the prompt.

```markdown
## 题材正文提示卡

- 主题材 / 平台：{如 番茄男频·都市高武}
- 题材边界：{这本书读起来必须是什么味，不能串到什么味}
- 核心逻辑：{世界观/社会关系/生活压力/能力规则如何驱动冲突}
- 读者期待：{读者进来等什么：打脸、升级、情感债、信息差、悬疑逼近等}
- 核心爽点 / 情绪：{本题材最稳定的 1-3 个释放方式}
- 节奏密度：{铺垫、爆发、冷却的比例；低压章允许的功能}
- 场景颗粒：{该题材需要哪些具体载体：账单/门店/宗门规矩/弹幕/案件线索等}
- 对话与人物声线：{该题材下台词承担什么功能，哪些角色不能说成同一种腔}
- 禁止漂移：{不能变成说明文、纯设定、纯科普、纯撒糖、纯战报等}
- 本章取舍：{仅本章使用的 2-4 条；从上面抽取，不全量执行}
```

### Tomato Novel–First Calibration

When Tomato Novel is the primary platform for long-form prose, emphasize “a clear entry hook, rapid emotional payoff, reuse of functional roles, and few transitions.” Do not turn false metrics into hard gates:

- Do not require every line to contain 50–60 Chinese characters; paragraph length in strong samples changes with the scene, and fixed line length looks artificial.
- Do not require dialogue to occupy 50%–60%; increase dialogue only when conflict, relationships, or information reveals require it.
- Do not globally replace “地/得/很/像/顿号”; first determine whether the prose is genuinely greasy, hollow, or formulaic.
- Do not randomly invert sentences; when breaking smoothness is necessary, change the viewpoint entry, object entry, sound entry, or result-of-action entry first.
- Do not add “procedural tasks” merely for naturalism; a task obstacle must change information, relationships, cost, choice, or foreshadowing.

### Generation / Reading Rules

1. First read the primary genre, target platform, primary comparable title, and central premise from `设定/题材定位.md`.
2. First match the classification exactly in `genre-prose-cards.md`, then read the individual `genre-prose-cards/{题材}.md` card (such as Urban High-Concept / Wealthy CEO / Period / Boys' Love). Mark a low-confidence card accordingly and calibrate it against a same-genre comparable title.
3. If no classification matches, find the nearest general genre module in this file. For cross-genre work, take only 3–5 rules from the primary genre and 1–2 from the secondary genre.
4. Write the extracted result as `genre_prose_card`; each chapter carries only items relevant to that chapter's emotion/events.
5. A genre card must not alter plot order, replace characterization, or override authoritative retrieval from `剧情/情绪模块.md` / `剧情/节奏.md`.

---

## Humor

### Core Principle
Humor is a pressure-release valve, not joke delivery. The best humor comes from a character trying to preserve dignity/authority/composure while reality refuses to cooperate.

### Sources of Humor
- Character embarrassment (trying to look cool and failing)
- Deadpan contrast (a serious person meets an absurd situation)
- Relational teasing (barbs exchanged among people who know one another)
- Dark humor (one cutting line in desperate circumstances)
- Observational humor (precise commentary on everyday situations)

### Operating Rules
- Humor arises from a character's desire/bias/stubbornness/misreading, not a gag detached from the plot
- The punchline changes status, exposes a relationship, or creates a future cost
- Keep setup short and payoff clear; the aftermath matters more than the punchline itself
- A callback must escalate (more embarrassing/more public/more serious)

### Blending Rules
- Humor + romance: Expose attraction/stubbornness
- Humor + suspense: Arise from false confidence
- Humor + literary fiction: Serve dignity and social texture

---

## Suspense

### Core Principle
Suspense depends on making readers feel a question/danger/cost approaching while the answer remains just out of reach; do not rely only on withholding information.

### Core Rules
- One major unresolved question per chapter
- A delayed reveal needs an in-story reason (timing, viewpoint limits, cost, possibility of error)
- Suspense works because “the question becomes more expensive,” not because “information becomes scarcer”
- Scenes must remain clear (obscurity is not suspense)

### Chapter Operations
1. Define the unknown
2. Define the cost of being wrong
3. Arrange information asymmetry among reader/character/opponent
4. Narrow the choices or raise the stakes in the second half
5. Grow the hook from existing clues; do not insert a sudden scare

### Blending Rules
- Suspense + mystery: What do we do next vs. what actually happened
- Suspense + horror: Approach vs. distortion
- Suspense + romance: Use exposure of the relationship, missed timing, and emotional cost as sources of suspense

---

## Romance

### Core Principle
Romance runs on constant friction among desire, fear, pride, care, misreading, and emotional debt—not on “they finally got together.”

### Core Rules
- Chemistry comes from concrete differences between characters, not empty praise
- The best tension = desire for closeness + fear of loss/exposure/indebtedness
- Every major relationship scene changes the depth of trust/hope/possessiveness/vulnerability/boundaries/misunderstanding
- Delay is acceptable, but it must create new pressure/debt/understanding/cost
- The most moving intimacy hides in small acts, care, misreadings, and what remains unsaid

### Chapter Operations
1. Define what each lead wants and fears
2. Decide whether this chapter draws them closer, pushes them apart, or entangles them more dangerously
3. Let one practical action carry emotional meaning
4. If there is a misunderstanding, root it in cognition/circumstance/wounds rather than a childish failure to “just explain”
5. End with a new emotional debt/risk/expectation

---

## Mystery

### Core Principle
The heart of mystery is making readers believe “I could solve this too,” so clues must be presented fairly.

### Key Techniques
- Blend clues into natural narration (never stop solely to list them)
- Place one or two misleading clues beside every true clue
- Reveal order matters more than the truth itself (guess the motive before the culprit)
- Give every suspect one major secret, with only one connected to the case

---

## Horror

### Core Principle
Horror works through a “limited viewpoint”—what a character does not know is more frightening than a displayed monster.

### Key Techniques
- Escalate fear (do not maintain one intensity throughout)
- Restrict information sources (power failure, lost signal, isolation)
- Use physiological reactions instead of directly describing fear
- A brief return of safety makes the next wave of horror stronger

---

## Fantasy/Xuanhuan

### Core Principle
A world's power comes from rules and costs, not from the ability to “do anything.”

### Key Techniques
- The power system must have clear boundaries and costs
- Tie world expansion to plot progression (no expository essays)
- Everyday details make the world feel more “alive” than grand premises (market currency, inn prices)
- Deliver new world-level information at least once every five chapters

### Special-Advantage Design
- The special advantage determines the payoff ceiling: the stronger it is, the larger the conflicts it can solve
- Avoid dependence on one-use secret treasures—the story becomes less stable over time
- Fragment the special advantage: Divide complex abilities and integrate the pieces into the plot
- The incomplete collection creates long-term anticipation; acquiring each fragment must solve at least one conflict
- Worldbuilding serves plot and must not restrain it in reverse; the protagonist must be a special variable within the rules

---

## Realism/Social Observation

### Core Principle
Realistic fiction derives power from “readers recognize these people.” Resonance comes from precise observation of everyday life.

### Key Techniques
- Dialogue must be conversational (never written in a formal register)
- Make settings specific down to store names, brands, and neighborhoods (more specificity feels more real)
- Conflict arises from genuine social pressures (money, reputation, relationships, class)
- Use all five senses for detail (cooking-oil fumes, mahjong tiles, the hum of an e-bike charging)

### Values and Commercial Principles
- Web fiction is commercial writing; judge prose by target-reader response and writing objectives
- Express plain values: a killer pays with life, debts are repaid, grudges and kindnesses are returned, good and evil receive their due
- Sophisticated argument = tell a story and let readers reach the conclusion themselves
- Hold a clear, sharp position: People who do evil must be punished
- Do not disgust readers merely to display “human complexity”

---

## Progression/Power Fantasy

### Core Principle
The essence of power fantasy is “an unknown process leading to an outcome readers already know.” Central expectations are becoming stronger, becoming richer, and earning recognition.

### Key Techniques
- The advancement–gain–power-display cycle is the universal core loop
- Advancement creates gains (contrast); gains create power displays (shock); power displays drive new advancement
- Release gains in layers; extra, uncertain rewards produce more surprise than fixed ones
- The central payoff comes down to four Chinese characters: the protagonist is formidable—the method used to solve a problem determines the satisfaction
- One serene finger-strike that annihilates the enemy >> a hysterical, grueling victory
- Failing to deliver full satisfaction when it is due feels worse than a toxic plot point

### Distilling the Central Premise
- Understand the central premise to determine the market lane and audience; blind imitation fails
- The central premise determines how the special advantage obtains resources (endless killing vs. cultivating a relationship network + farming)
- The central premise shapes the entire book's tone (relaxed everyday life vs. serious passion)

### Characterization Consistency
- The source of power determines behavioral logic:

| Power Type | Source | Behavioral Trait |
|----------|------|----------|
| Individual strength | Cultivation model; strength is authority | Skills and treasures belong to the individual |
| Compliance-based | Lordship model; power comes from subordinates' obedience | When interests diverge, followers cannot be commanded |

- Never break a brilliant character: An intelligent person follows the principle of economy (maximum gain at minimum cost)
- When an antagonist gathers an army for direct confrontation, consider whether the army will obey and whether its interests align
- Broken characterization = a character acts against their power structure/personality merely to move the plot

### Power-Scale Principles
- The maximum scale depends on genre boundaries and controllability; keep it stable enough to write coherently
- Anything below single-universe scale is generally sufficient; multiverse tricks are unnecessary
- Avoid rule-based abilities when possible; they become uncontrollable too easily
- Scale must fit the genre's boundaries

---

## Comedy Fiction

- Comedy does not mean insanity; logic is the foundation—comic events must remain logically inferable (a solution within the rules but outside expectations)
- An irrational, deranged protagonist may amuse readers early, but later becomes cringe-inducing when readers cannot follow the character's thinking
- Meme rule: Forcing a meme is worse than omitting it—memes have life cycles, and after popularity passes only embarrassment remains
- Correct approach: Extract the internal comic logic of a meme and adapt it to the novel's situation

---

## Light-Novel/Anime-Inspired Style

- Core definition: Fiction whose primary appeal is dramatic characterization, especially varied attractive heroine archetypes
- Characterization is the selling point: Every character has a vivid “tagged” trait readers recognize immediately
- Everyday texture matters more than plot progression: Character interactions and fragments of daily life are the main content
- Dense commentary/interiority: The protagonist acts as the “straight man,” and their response to absurdity becomes a payoff
- Exaggerate differences among archetypes: tsundere/yandere/kuudere/airhead—the clearer the tag, the better
- Selling characterization > selling plot: Plot exists to showcase character appeal
- Dialogue volume > descriptive volume: Advance interaction through dialogue and reduce long interior monologues

---

## Absurdist Style

- Absurdist style = creating humor through absurd, convention-breaking narration
- Character behavior is unexpected but logically coherent (intelligent absurdity, not chaos)
- Absurd behavior dissolves a serious scene, and the contrast creates humor
- Sect daily life > combat progression: Advancement is only a minor element in absurdist sect fiction
- Strong ensemble feel: A group plays off one another rather than relying on one person for every laugh
- Absurd does not mean stupid: A character follows their own logic, even when that logic is outrageous
- Core risk: Pure absurdity lacks emotional depth and is forgotten after the laugh; it needs a foundation of genuine feeling

---

## Cyberpunk Style

- High technology, low quality of life: neon, cybernetics, data streams, rigid class divisions
- High information density: Integrate abundant world details naturally rather than writing exposition
- Hard, cold tone: Alienation, oppression, and technological estrangement run throughout
- World texture > plot complexity: Cyberpunk readers come for the world's atmosphere
- Establish sufficient atmosphere in the opening chapters: rainy nights, neon, body modification, virtual networks
- Avoid xuanhuan wearing cyberpunk skin: The power system must obey technological logic

---

## Listicle/Information-Gap Fiction

- Core mechanism: The protagonist presents exclusive information to uninformed observers, producing shock and a power-display effect
- Knowledge-based information gaps are the central payoff: Readers and protagonist “overwhelm” an uninformed world together
- Unit structure: one listed subject = one power-display unit, repeated in a cycle
- Resonance first: Choose listed subjects that create national/cultural/professional resonance for readers
- Every unit needs: establish the setting's ignorance -> protagonist demonstrates -> observers react -> information gap closes
- Can blend with other genres: listicle + game fiction, listicle + transmigration, listicle + entertainment industry
- Boundary rule: Information gaps drive listicle pacing; it must not become pure popular education

---

## Simulation Fiction

- Core structure: Gain rewards and information gaps through “simulation,” then advance the main plot and fulfill expectations in reality
- Unit structure: Simulation creates an emotional deficit -> simulation provides a reward (creating an information gap) -> reality fulfills the expectation
- Volume structure: Simulation reveals a major crisis/expectation -> repeat small [simulation + reward + real-world progression] units -> finally achieve/resolve the central expectation
- Information from simulation = leverage for real-world power displays
- Simulation can show the consequences “if no intervention occurs,” increasing urgency
- Layer rewards: Minor simulations give minor rewards (advancement resources); major simulations give critical information (plot turn)
- Simulation is not omniscience: Preserve unknown variables; the protagonist cannot learn everything through it

---

## Livestream Fiction

- Core mechanism: Use livestreaming as a frame that combines money-making, power displays, confrontation, and stunts into varied payoffs

| Source of Satisfaction | Concrete Expression |
|----------|----------|
| Making money | Receive tips/gifts directly; monetary totals visibly rise |
| Confrontation | PK battles, ranking campaigns, competition with peers |
| Hidden identity | Hidden major figures among the audience; chat-based information gaps create surprises |
| Stunts | Absurd/comedic livestream content attracts spectators |
| Talent demonstration | A showcase for the protagonist's unique ability |

- Clear objectives: Every stream has a concrete target (earn X money/gain X followers), giving readers a defined expectation
- Livestream chat = instant feedback system: a built-in audience for power displays that needs no separate design
- Can blend with social observation: one guest/one resolved issue per stream = one social-observation story unit
- Pacing requirement: Do not livestream continuously; interweave a real-world plot thread

---

## Conflict Design for Redemption Fiction

| Conflict Type | Method | Example |
|----------|------|------|
| Redemption-objective conflict | One person's desired redemption requires the other's sacrifice | Qiao Feng and A'Zhu |
| Redemption-action conflict | Redemption is built on lies/harm/a zero-sum contest | Taking another person's identity |
| Triangle | One person's act of redemption causes a third party to need redemption | Chain reaction |
| Redemption countdown | Redemption must occur before an event or the character falls completely | Time pressure |
| Increasing redemption cost | One person's cost to redeem the other keeps rising | Escalating emotional/resource/physical and psychological costs |
| Scarce redemption resources | Both need redemption, but resources can save only one | Zero-sum contest |
| Opposing positions | They disagree in principle but need each other's help | Conflict between redemption and position |
| Personality contrast | Optimism vs. pessimism; coldness vs. compassion | Obstructs understanding and communication |

---

## Genre Boundaries and Atmosphere

### Essence of Genre Boundaries
Genre boundaries = the set of genre-specific information points. Use them to shape atmosphere so readers feel, “This has exactly that flavor.”

### Three Levels of Boundaries

| Level | Content | Failure Mode |
|------|------|----------|
| Genre boundary | Genre-specific worldbuilding, pacing, and emotional tone | Urban fiction tastes like cultivation; farming fiction tastes like empire-building |
| Style boundary | The genre's linguistic texture and narrative pacing | A light novel sounds like serious literature; social-observation fiction sounds like xuanhuan |
| Audience boundary | Target readers' expectations and dealbreakers | Using male-oriented pacing for female-oriented fiction; applying Qidian standards to Tomato Novel |

### Tonal Consistency
- The tone must remain consistent throughout; changing it midway destroys the central appeal
- Tone = readers' shared understanding of “what this book feels like it is about”
- Test: After every chapter ask, “Does this chapter match the opening's tone?”

### Evaluating Boundaries When Combining Genres
- Before combining genres, define each one's central premise
- Does the resulting appeal move beyond those central premises? Beyond = outside the boundaries = dangerous
- Correct method: Keep one genre as the primary tone while the other supplies the special advantage or surface setting
- Incorrect method: Alternate two pacing systems until readers no longer know what they are reading

### Genre Boundaries in Comparable-Title Selection
- A comparable must match platform + genre + type; all three are mandatory
- Audiences differ across platforms, so methods cannot be copied directly

---

## Differences Among Platform Styles

| Platform | Core Strength | Reader Preference | Strategy |
|------|-----------|----------|------|
| Qidian Main Site | Progression/professional threads | Long-term anticipation, stable pacing, deep worldbuilding | Prioritize genres with clear boundaries and mature audiences |
| Tomato Novel | Fast and punchy, strong emotion, dense payoffs | Fast pacing, no dragging, a hook in Chapter 1 | Analyze early structures in same-platform, same-genre samples; reuse functional roles rather than plot events |
| Ciweimao | Stunts > pacing; characterization > plot | Anime-fan-fiction + gacha-game readers who value “fun” over stable pacing | Fit fan fiction, light novels, high-concept premises, and stunt-driven work |
| Lower-tier markets | Gag-driven fiction | Wild, eccentric, uninhibited work | Write freely, but get the flavor right |

---

## Market Positioning and Subject-Selection Strategy

- Prioritize categories with broad audiences, many samples, and clear boundaries; validate current popularity through the latest scan/analyze results or user samples.
- A popular category only indicates a larger potential reader pool, not that any specific premise is currently effective.
- To reduce competitive pressure, retain genre boundaries while changing the entry angle, relationships, or emotional trigger.
- Do not use “traditional fiction is just like this” to excuse slow pacing, weak conflict, or an unclear selling point.

---

## The Essence of Genre = Combining Elements

- The essence of genre: Every genre is a combination and arrangement of elements
- Element = something readers find interesting + something previously popular in web fiction
- An element is neither a special advantage nor a channel category
- Check-in fiction combines: [lying low + high-intensity gains + strong anticipation]
- A genre with two disconnected elements (cultivation + technology) is extremely difficult; first make it coherent + make the collision interesting
- Market-lane rule: Prefer emerging lanes with distributed competition and recently validated samples; avoid mature lanes dominated by strong brands where functional roles are hard to reuse.
- Study mid-tier samples rather than only market leaders—their structures are more reusable.
- Commercialization = respect the target reader; private expression cannot override the central selling point and reading experience.

---

## Audience Reach and Market Lanes

- Audience reach = a genre's upper limit/ceiling; sometimes the genre is weak rather than the writing
- Market lane = a genre track; different lanes have different reader pools and expectations.
- Three dimensions of lane selection: audience reach (ceiling) + competition (number of competitors) + fit with material/capabilities.
- Examine the ceiling before choosing a lane; lower length and commercial expectations for lanes with very small reader pools.

---

## Following Trends and Innovating

- The core of web-fiction writing = the ability to tell a story, not elegant prose/originality for its own sake/broad knowledge
- Following trends = reusing validated functional roles, one method of reducing risk
- Homogeneity arises when an imitator does not deeply process the objective and only copies
- Trend-following is not the problem; copying actions and tone is—the broken-engagement trope can support many combinations
- An unconventional premise is not inherently innovative—mainstream ideas are mainstream because most people accept them
- Core of innovation: Extract the internal comic logic of a trope and adapt it to a new situation

---

## Combining Genre Elements and Thinking in Modes

- Extract the elements of one mode + extract the elements of another -> synthesize a new book
- An idea is usable only when “material, characters, conflict, and length” all support it.
- Anti-trope = overturning an established pattern to create freshness.
- Common problem: The manuscript does not make critical information explicit, so readers cannot understand the selling point.
- Target readers must recognize the novel's central selling point or its commercial value cannot be realized.

---

## Market Awareness and Creative Guidelines

- Opening-pacing rule: Focus early on rapidly developing the central selling point/special advantage; avoid overinvesting in setting and foreshadowing until the manuscript slows
- Once perfection becomes the goal -> obsession with setting, plot, and foreshadowing -> slow manuscript pacing
- Information-gap risk: The preparation promises exciting later development, but the manuscript shows only a dithering male lead and a heroine who undermines the team
- A new-media entry depends on a striking premise and immediate appeal; the opening must fulfill its entry promise immediately
- Do not move randomly from one concern to another; every plot passage must directly advance the central conflict

---

## Creative Approach and Opening Design

- Three-step creative approach: Determine the protagonist's identity -> match a special-advantage type -> establish the opening environment -> establish an image (tag)
- Image = attach a tag to character and plot to add depth
- An opening does not require conflict and may begin with setting; the key is smooth delivery of all information
- Do not introduce background through narration; mix information into dialogue
- Protagonist's identity -> crisis faced -> attempts a solution -> lacks the ability -> special advantage arrives
- Do not pour in too much information at once
- Pacing misconception: If the book does not interest readers, making the protagonist a god-emperor in Chapter 1 will not help

---

## Smooth Openings for Low-Status Protagonists

- The core of a low-status opening = smoothness; it does not require reversals or push-pull
- Deliver all information smoothly—the reader's thoughts follow the content downward without resistance
- Do not pour every pressure onto the protagonist at once; introduce pressure gradually
- Convey information through dialogue and minimize narrated background
- After granting the special advantage, create an immediate change—let readers see the transformation occur
- The special advantage should arrive only after the protagonist actively confronts the crisis but lacks sufficient ability—then the protagonist is not incompetent
- Act according to status: A stable boy cannot afford moral purity; taking too large a step = structural damage
- Before writing a major plot event, ask whether the protagonist's current level, identity, and resources qualify them for it

---

## Five Essentials of an Opening

- **Keep it simple**: Clearly establish five elements (who/where/what/why/intended action) in Chapter 1
- **Stay aligned**: The opening plot must fit the main plot; drifting = a zero-score opening
- **Move fast**: Enter the plot quickly; lingering over background = verbosity
- **Deliver satisfaction**: The first minor plot event needs a payoff; no shock within five chapters = failure, and there can be no toxic trigger/land mine/reason to quit
- **Avoid flatness**: Prose, like mountains, is valued for variation; no conflict or contradiction and nothing but calm = failure

**Common opening problems**:
- Opening prologue -> reclusive experts A, B, C, and D speak -> cryptic riddles -> readers are bewildered
- Obscure and incomprehensible -> readers leave immediately
- Long-winded “setup” -> actually all wasted words -> pacing is too slow

---

## Quality Checklist

After writing a chapter/volume in a genre, check each item:

- [ ] **Genre boundaries**: The chapter tastes like the target genre with no contamination
- [ ] **Consistent tone**: It matches the opening's tone without changing midway
- [ ] **Execute core genre techniques**: Follow every “core rule” in the relevant module
- [ ] **Characterization fits tags**: Character behavior follows its tags with no collapse
- [ ] **Conversational dialogue**: No formal register (mandatory for realism/social observation/progression)
- [ ] **Five-senses detail**: Scenes contain concrete sensory detail rather than abstraction
- [ ] **Five opening essentials** (when checking an opening): simple/aligned/fast/satisfying/not flat
- [ ] **Cross-genre boundaries** (when combining genres): primary genre supplies the tone; secondary genre supplies the surface layer
- [ ] **Comparable-title consistency**: Comparable title matches platform + genre + type
- [ ] **Market fit**: The target lane's reader pool is large enough, and the genre fits the strengths of existing material/capabilities
