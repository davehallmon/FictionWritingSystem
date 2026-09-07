# {Project Name} — Web-Fiction Writing Toolkit (General Agents / Web AI)

This project integrates oh-story skills as ordinary files. If the current platform does not support hooks or custom agents for Claude Code, OpenCode, Codex, Antigravity, ZCode, or OpenClaw, an agent can still execute the workflow by reading `skills/*/SKILL.md` and `skills/*/references/` directly. Runtime enforcement and automatic multi-agent collaboration will simply be unavailable.

## Skill Routing Table

Prefer naming the skill in natural language. If the platform supports custom commands, you may also map the following entries to commands.

| Intent | Skill | Description |
|------|-------|------|
| Write, start, or continue a long-form story | story-long-write | Long-form web-fiction writing, advanced chapter by chapter |
| Write a short story | story-short-write | Short-form web-fiction writing driven by emotional progression |
| Analyze a long-form story | story-long-analyze | In-depth decomposition of a long-form novel |
| Analyze a short story | story-short-analyze | Structural analysis of short-form fiction |
| Scan long-form rankings | story-long-scan | Long-form fiction rankings and market trends |
| Scan short-form rankings | story-short-scan | Short-form fiction rankings and emerging emotional trends |
| Remove AI writing traces | story-deslop | Remove recognizable AI-writing patterns |
| Create a cover | story-cover | Generate cover artwork |
| Review | story-review | Multi-perspective review; falls back to single-threaded review when custom agents are unavailable |
| Import | story-import | Reverse-import an existing novel into the project structure |
| Web-fiction toolkit | story | Automatically route ambiguous requests |
| Prepare or deploy a book project | story-setup | General project structure and skill entry point |
| Use an authenticated browser or scrape content | browser-cdp | Browser CDP tools; requires a platform that permits local scripts and browser control |

## File Structure

- `skills/` — Project-local skills. The agent should read the applicable `SKILL.md` first, then read from `references/` as needed.
- `拆文库/` — Stores story-decomposition results.
- `{书名}/正文/` — Chapters of a long-form novel.
- `{书名}/正文.md` — Main text of a short story.
- `{书名}/设定/` — Character and worldbuilding specifications.
- `{书名}/大纲/` — Volume outlines and detailed chapter outlines.
- `{书名}/追踪/` — Contains `_tracking-state.json`, the sole structured authority; the fixed seven-section `上下文.md` continuation-state card; compact chapter-by-chapter records; independent derived snapshots for core characters; the current foreshadowing view; and separate author and reader timelines. All are generated through tracking tools.
- `{书名}/对标/` — Analysis of benchmark works.

## General Usage Conventions

- Create an outline before drafting prose. Long-form work requires `大纲/细纲_第N章*.md`; short-form work requires `小节大纲.md`.
- Platforms without hooks cannot automatically block unauthorized prose generation. When running a writing skill, the agent must check the outline, context, and tracking files itself.
- Platforms without custom agents execute in solo/direct mode. When a skill calls for an agent such as story-architect or narrative-writer, the current agent must complete the work directly and disclose the fallback in the result.
- **Self-lock for removing AI writing traces** (the only safeguard on platforms without hooks): immediately after saving each chapter, run the writing skill's “Most Toxic Sentence Patterns Quick Reference + Banned-Term Scan” in the same turn and clear every finding. When Node is available, run `check-ai-patterns.js --check --fail-on=blocking`. Before writing the next chapter, verify again that the previous chapter has no unresolved findings. The only exception is an explicit user instruction saying “do not remove AI traces from this chapter.” Add `<!-- 去味:跳过 -->` immediately below the title of an exempt chapter.
- After compaction or in a new conversation, read `{书名}/追踪/上下文.md` first to restore the current writing state.

## Restoring Context After Compaction

Critical context for work in progress:

1. Current writing-project name and progress
2. Recently discussed changes to character specifications
3. Unresolved foreshadowing items
4. The current chapter's emotional and pacing targets

If `{书名}/追踪/上下文.md` exists, read it first after compaction to restore context.
