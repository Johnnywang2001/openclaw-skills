# Skill Evolution

AutoSkill-powered self-evolving skill system. Automatically extracts reusable skills from conversations, merges duplicates, versions updates, and mirrors to OpenClaw's native skills directory.

## What It Does

Based on the AutoSkill framework (Yang et al., 2026 — [arxiv:2603.01145](https://arxiv.org/abs/2603.01145)), this skill enables your agent to learn from every conversation:

- **Automatic extraction** — After each session, analyzes conversations for durable patterns worth keeping
- **Smart filtering** — Extracts preferences, corrections, recurring workflows, and domain conventions; skips one-off requests and generic knowledge
- **Merge over duplicate** — Updates existing skills instead of creating duplicates, with semantic versioning
- **Vector-indexed retrieval** — Relevant skills are automatically found and injected into future sessions
- **Auto-pruning** — Skills retrieved 40+ times but never used are pruned automatically
- **OpenClaw mirror** — Skills sync to `~/.openclaw/workspace/skills/` for native availability

## When to Use

This skill runs automatically in the background. It's most valuable when:

- Your agent handles recurring workflows that should improve over time
- You frequently correct your agent and want those corrections to persist
- You want domain-specific conventions encoded as reusable skills
- You want your agent to get better the more you use it

## Architecture

```
Conversation → Session Archive → Skill Extraction → Maintenance (add/merge/discard)
                                                   → SkillBank (versioned SKILL.md + vector index)
                                                   → Mirror to ~/.openclaw/workspace/skills/

Future Query → Embedding Search → Skill Retrieval → Context Injection → Better Response
```

## Installation

```bash
# From GitHub
cp -r openclaw-skills/skills/skill-evolution ~/.openclaw/workspace/skills/

# Or symlink (stays updated)
ln -s /path/to/openclaw-skills/skills/skill-evolution ~/.openclaw/workspace/skills/skill-evolution
```

Restart the gateway:
```bash
openclaw gateway restart
```

## Prerequisites

- AutoSkill4OpenClaw installed and configured in embedded mode
- See SKILL.md for full configuration details

## Key Concepts

- **SkillBank** — Versioned storage at `~/.openclaw/autoskill/SkillBank/`
- **Embedded mode** — Runs as an OpenClaw adapter plugin, no separate process needed
- **Session archives** — Raw conversation data at `~/.openclaw/autoskill/embedded_sessions/`
- **Top-K retrieval** — Configurable number of skills injected per session (default: 3, min score: 0.4)

## License

MIT
