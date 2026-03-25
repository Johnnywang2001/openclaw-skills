# OpenClaw Context Upgrade

Optimize your agent's context window by delegating heavy tasks to sub-agents while keeping the main session lightweight for conversation.

## What It Does

Restructures your OpenClaw agent into an orchestrator pattern — the main session handles conversation while sub-agents handle research, coding, file operations, and other context-heavy work. Each sub-agent gets its own fresh context window.

## Installation

```bash
# From this repo
cp -r skills/openclaw-context-upgrade ~/.openclaw/workspace/skills/

# Or from ClawHub
clawhub install openclaw-context-upgrade
```

## Automatic Implementation

Paste this single prompt into your OpenClaw agent to implement everything:

```
Implement the OpenClaw Context Upgrade on this system. Read the guide at:
~/.openclaw/workspace/skills/openclaw-context-upgrade/SKILL.md

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

## What's Included

- **Upgrade 1:** Orchestrator delegation pattern (AGENTS.md rules)
- **Upgrade 2:** Sub-agent concurrency configuration
- **Upgrade 3:** Enhanced compaction safeguards
- **Upgrade 4:** Context pruning with TTL
- **Upgrade 5:** Pipeline pattern for complex multi-step tasks

## Expected Results

- Main session context usage drops 50-70%
- Compaction fires less frequently
- Conversation history preserved longer
- Complex tasks complete faster via parallel sub-agents

## License

MIT
