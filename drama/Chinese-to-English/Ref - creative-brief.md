# Creative Brief

Source: `输入/长篇-让你管账号，你高燃混剪炸全网.txt` (20 chapters),
fully analyzed in `项目开发/source-analysis/` (437 plot events / 14 story units / 24 candidate sets).

## I. Creator Contract

### Immutable Source Facts

After each item, identify **the image from which the audience can learn it within this pass's scope (EP001–EP003)**,
or explicitly defer it to a named episode. Do not include an item in this table when neither answer is available (STY-23).

| ID | Fact | Delivery in this pass |
|---|---|---|
| F-W2 | **New media throughout this world is underdeveloped:** not only in the military; across the entire industry, very few creators have more than ten thousand followers | **Delivered in EP001.** Visible carrier: the protagonist scrolls to the platform's industry-ranking page, where the leading creator has a four-digit follower count. Compared with the scale of his former life, the number lets the audience reach the conclusion independently |
| F-W3 | The Rocket Force has almost no new-media presence; across more than a dozen accounts, the combined follower count is lower than the number of accounts | **Delivered in EP001.** Visible carrier: a backend account list with a single-digit number at the end of each row |
| F-C5 | The protagonist does not understand music. In his former life he hired music consultants and cannot even reproduce well-known compositions | **Delivered in EP001.** Visible carrier: after writing the two Chinese characters for “score,” his pen stops and he throws it aside |
| F-DEV | The entire world attributes the device-granted ability to his personal talent | **Delivered in EP003.** Visible carrier: a veteran says in the group chat that the song is original and better than every military song he has heard. The protagonist is absent and cannot correct him |
| F-W4 | The Rocket Force handles highly classified work, so this kind of material is rarely displayed | **Delivered in EP002.** Visible carrier: the veteran pauses when he sees the official blue verification badge and speaks one line to himself |
| F-W6 | The publicity unit has ranked last for years; the midyear evaluation is approaching and affects both unit honors and individual promotion | **Delivered in EP002.** Visible carrier: cold tea on the deputy commander's desk beside the ranking notice |
| F-L1 | Veteran Li Lin defends him because of his own military service and a fallen comrade | **Partially delivered in EP003; fully delivered in EP004.** Visible carrier in EP003: an old group photograph precisely aligned on his cabinet. The name Guoqiang and the story of taking a bullet are **explicitly deferred to EP004** |
| F-W7 | Senior military leadership hopes to use the opportunity to demonstrate hard power | **Explicitly deferred to EP008.** No obligation in this pass |
| F-SYS-COST | The device has a cost | **Explicitly deferred to EP007**, when the cost first becomes visible. EP001 plants only a contractual clause and does not disclose the cost |

### Exploratory Gaps

- The device's failure conditions and cost are absent from the entire source novel (see `world.md`). This project completes them in the story engine's device-contract table.
- The source does not provide an ending for antagonist Wu Wei; this pass does not address it.
- The source disconnects Li Lin from the later ensemble of veterans. By creator decision, this project combines them into one line.

### Formal Constraints

- Vertical 9:16, 24 episodes × 90 seconds, delivery rate of 5.0 Chinese characters per second, and 2.5 seconds per action segment (`short-drama.json#/format`).
- Production form: a generative model creates the visuals in a semi-realistic style (`creator_authority/production_profile`).
- Delivery scope for this pass: episode records for EP001–EP003; script, assets, image prompts, storyboard, and video prompts for EP001.

## II. Dramatic Promise

A person carrying all the experience of a former life falls into a world where nobody yet knows how to use it.
He must prove not how powerful he is, but whether **what others mistake for talent is worthy of the trust they place in him**.

## III. Recurring Audience Rewards

| Reward | Form |
|---|---|
| Gratification from overwhelming advantage | Using a tool everyone owns—a phone—he creates something nobody else can |
| Repression followed by vindication | Before each work appears, a group of people first declares that it will fail |
| Being seen | Through his work, an overlooked person or group receives serious attention from a large audience for the first time |

## IV. Target Audience and Emotional Landing Point

The overlapping audience for military fiction, mainstream-values stories, and system fiction. The emotional landing point is not “he won,” but “someone was finally seen.”

## V. Production Boundaries

- Generate all large-scale military scenes. Use smoke and dust to obscure long shots, and do not show extended shots of individual projectiles.
- Use fictional unit designations and non-realistic insignia; do not show identifiable markings of real units.
- Convey age in elderly characters through hands, old objects, and medals, avoiding full-body continuity failures.
