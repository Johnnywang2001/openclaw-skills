---
name: skill-evolution
description: "Self-evolving skill system powered by AutoSkill. Automatically extracts reusable skills from conversations, merges duplicates, versions updates, and mirrors to OpenClaw's native skills directory. Based on the AutoSkill framework (arxiv:2603.01145)."
---

# Skill Evolution

This agent uses AutoSkill4OpenClaw for automatic skill self-evolution. Skills are extracted from real conversations, versioned, and made available for future sessions.

## How It Works

AutoSkill runs in **embedded mode** as an OpenClaw adapter plugin:

1. **After each session ends** (`extractOnAgentEnd: true`), AutoSkill analyzes the conversation
2. It identifies **durable user preferences, corrections, and recurring patterns** -- not generic requests
3. Candidate skills are either **created** (new SKILL.md) or **merged** into existing skills (version bump)
4. Skills are stored in the **SkillBank** and **mirrored** to OpenClaw's native `skills/` directory
5. On future sessions, relevant skills are **retrieved** and injected into context automatically

## What Gets Extracted (and What Doesn't)

**Extracts:**
- Stable user preferences ("always use conventional commits")
- Corrections ("no, use squash merge not regular merge")
- Recurring workflows (multi-step procedures done repeatedly)
- Tool-specific patterns ("xcrun altool needs app-specific password")
- Domain conventions ("follow HIG spacing guidelines")

**Skips:**
- One-off requests ("write me a report")
- Generic knowledge any LLM already has
- Temporary/situational instructions

## Architecture

```
Conversation → Session Archive → Skill Extraction → Maintenance (add/merge/discard)
                                                   → SkillBank (versioned SKILL.md + vector index)
                                                   → Mirror to ~/.openclaw/workspace/skills/

Future Query → Embedding Search → Skill Retrieval → Context Injection → Better Response
```

## Key Paths

- SkillBank: `~/.openclaw/autoskill/SkillBank/`
- Session archives: `~/.openclaw/autoskill/embedded_sessions/`
- OpenClaw mirror: `~/.openclaw/workspace/skills/` (auto-synced)
- AutoSkill repo: `~/Projects/AutoSkill/`
- Plugin config: `~/.openclaw/plugins/autoskill-openclaw-plugin/`
- Adapter: `~/.openclaw/extensions/autoskill-openclaw-adapter/`

## Config (in openclaw.json)

```json
{
  "runtimeMode": "embedded",
  "openclawSkillInstallMode": "openclaw_mirror",
  "skillScope": "all",
  "topK": 3,
  "minScore": 0.4,
  "extractOnAgentEnd": true,
  "successOnly": true,
  "embedded": {
    "sessionMaxTurns": 20
  }
}
```

## Manual Operations

Force extraction from current session:
- Say "extract skills from this conversation" or "/extract_now"

Check what skills exist:
```bash
ls ~/.openclaw/autoskill/SkillBank/
```

## Skill Quality Rules

From AutoSkill paper (Yang et al., 2026):
- Skills are **versioned artifacts** (v0.1.0 → v0.1.1 on merge)
- **Merge over duplicate**: if a similar skill exists, update it instead of creating a new one
- **Discard noise**: generic patterns that encode no user-specific knowledge get discarded
- **Human-editable**: any SKILL.md can be manually reviewed and revised
- **Auto-prune**: skills retrieved 40+ times but never used get pruned automatically
