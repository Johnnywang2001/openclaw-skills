# OpenClaw Memory Upgrade

A setup guide that transforms your OpenClaw agent from forgetting everything between sessions to having persistent, searchable memory.

## This Is Not a Skill

This is a manual configuration guide. It walks you through changes to your `openclaw.json` config file and `AGENTS.md` workspace file. Your agent does not install this — you (or your agent via the one-prompt setup) apply these changes directly.

## Setup

### Option 1: Automatic (one prompt)

Paste this into your OpenClaw agent:

```
Implement the OpenClaw Memory Upgrade on this system. Read the guide at:
~/.openclaw/workspace/guides/memory-upgrade/SKILL.md

Implement all 5 upgrades (skip Cognee/upgrade 6).
Merge all config changes into openclaw.json without overwriting existing settings.
Add all AGENTS.md instructions.
Install the Mem0 plugin.
Restart the gateway.
Report what you changed when done.
```

### Option 2: Manual

Read [SKILL.md](SKILL.md) and follow each upgrade step by step. Copy the JSON config blocks into your `openclaw.json` and add the memory management instructions to your `AGENTS.md`.

### Option 3: From GitHub

```bash
git clone https://github.com/Johnnywang2001/openclaw-skills.git
# Read the guide
cat openclaw-skills/guides/memory-upgrade/SKILL.md
```

## What's Included

1. **Enhanced memoryFlush** — auto-saves 8 categories of important info before context is lost
2. **Session indexing** — makes past conversations searchable
3. **Manual memory management** — two-tier file system (daily logs + curated long-term memory)
4. **QMD hybrid search** — keyword + semantic search with diversity and recency ranking
5. **Mem0 plugin** — auto-capture and auto-recall of memories
6. **Cognee** (optional, skip recommended) — graph-based memory requiring Docker

## License

MIT
