# OpenClaw Context Upgrade

A setup guide that optimizes your agent's context window by delegating heavy tasks to sub-agents while keeping the main session lightweight for conversation.

## This Is Not a Skill

This is a manual configuration guide. It walks you through changes to your `openclaw.json` config file and `AGENTS.md` workspace file. Your agent does not install this — you (or your agent via the one-prompt setup) apply these changes directly.

## Setup

### Option 1: Automatic (one prompt)

Paste this into your OpenClaw agent:

```
Implement the OpenClaw Context Upgrade on this system. Read the guide at:
~/.openclaw/workspace/guides/context-upgrade/SKILL.md

Follow every step:
1. Add the Orchestrator Delegation Rules to AGENTS.md
2. Update openclaw.json with the sub-agent configuration (Upgrade 2)
3. Update compaction settings (Upgrade 3) — merge with existing, don't overwrite
4. Update context pruning settings (Upgrade 4) — merge with existing
5. Add the Pipeline Pattern to AGENTS.md
6. Restart the gateway with: openclaw gateway restart
7. Verify the changes with: openclaw status

Report what you changed when done. Do not ask for permission at each step — execute the full upgrade.
```

### Option 2: Manual

Read [SKILL.md](SKILL.md) and follow each upgrade step by step. Copy the JSON config blocks into your `openclaw.json` and add the delegation rules to your `AGENTS.md`.

### Option 3: From GitHub

```bash
git clone https://github.com/Johnnywang2001/openclaw-skills.git
# Read the guide
cat openclaw-skills/guides/context-upgrade/SKILL.md
```

## What's Included

1. **Orchestrator delegation** — agent delegates research, coding, and file operations to sub-agents
2. **Sub-agent concurrency** — up to 8 parallel sub-agents for complex tasks
3. **Compaction safeguards** — higher thresholds to preserve conversation detail
4. **Context pruning** — automatically drops old context with TTL
5. **Pipeline pattern** — reusable PM → Workers → QA pattern for multi-step tasks

## License

MIT
