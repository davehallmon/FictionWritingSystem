# {Project Name} — Web-Fiction Writing Toolkit

## Skill Routing Table

| Command | Skill | Description |
|------|-------|------|
| `/story-long-write`, `/写长篇` | story-long-write | Write long-form web fiction chapter by chapter |
| `/story-short-write`, `/写短篇` | story-short-write | Write emotionally driven short-form web fiction |
| `/story-long-analyze`, `/长篇拆文` | story-long-analyze | Perform an in-depth decomposition of a long-form novel |
| `/story-short-analyze`, `/短篇拆文` | story-short-analyze | Analyze and decompose a short story |
| `/story-long-scan`, `/长篇扫描` | story-long-scan | Batch-scan long-form novels |
| `/story-short-scan`, `/短篇扫描` | story-short-scan | Batch-scan short-form fiction |
| `/story-deslop`, `/去AI味` | story-deslop | Remove recognizable AI-writing patterns |
| `/story-cover`, `/封面` | story-cover | Generate cover artwork |
| `/story-review`, `/审查` | story-review | Perform an adversarial, multi-perspective review |
| `/story-import`, `/导入` | story-import | Reverse-import an existing novel into the project structure |
| `/story`, `/网文` | story | Toolkit router that automatically dispatches ambiguous requests |
| `/story-setup`, `/准备写书` | story-setup | Deploy hooks, rules, and agents in one operation |
| `/browser-cdp` | browser-cdp | Browser CDP tools |

## File Structure

- `拆文库/` — Stores story-decomposition results.
- `{书名}/正文/` — Chapters of a long-form novel.
- `{书名}/设定/` — Character and worldbuilding specifications.
- `{书名}/大纲/` — Volume outlines and detailed chapter outlines.
- `{书名}/追踪/` — Contains `_tracking-state.json`, the sole structured authority; the fixed seven-section `上下文.md` continuation-state card; compact chapter records; independently derived snapshots for core characters; the current foreshadowing view; and separate author and reader timelines. All are generated through tracking tools.
- `{书名}/对标/` — Analysis of benchmark works.

## Collaboration Rules

Each agent definition describes its own responsibilities and coordination boundaries. No separate coordination-rules file is required.

## Restoring Context After Compaction

This section takes effect automatically after compaction. CLAUDE.md is reloaded after every compaction.
Critical context for work in progress:
1. Current writing-project name and progress
2. Recently discussed changes to character specifications
3. Unresolved foreshadowing items
4. The current chapter's emotional and pacing targets

If {书名}/追踪/上下文.md exists, read it first after compaction to restore context.
