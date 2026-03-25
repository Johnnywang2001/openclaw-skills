# Reasoning Upgrade

Inject frontier-level reasoning patterns into any OpenClaw agent, regardless of which model powers it.

## What It Does

This skill teaches your agent to think more systematically by providing explicit reasoning scaffolding that top-tier models (like Claude Opus 4.6) do naturally. It covers:

- **Reasoning patterns** — decompose problems, consider alternatives, state assumptions, verify work
- **Decision frameworks** — evaluate tradeoffs, quantify, rank options, commit with reasoning
- **Tool use discipline** — search before guessing, verify after acting, don't chain blindly
- **Context management** — delegate heavy work, summarize don't paste, protect context window
- **Communication discipline** — lead with answers, be direct, cite sources, admit uncertainty
- **Error handling** — read errors, diagnose before fixing, don't retry blindly
- **Research discipline** — search broadly, cross-reference, check dates, distinguish facts from opinions
- **Self-monitoring** — continuously check if you're answering the right question the right way

## Why It Matters

When switching from a frontier model (Opus) to a more cost-effective model (Sonnet, Haiku, Codex, MiniMax), the quality drop often isn't in knowledge — it's in reasoning discipline. Smaller models skip steps, make assumptions, chain actions without verifying, and give verbose answers that dodge the actual question.

This skill closes that gap by making the reasoning process explicit rather than implicit.

## Installation

```bash
# From GitHub
cp -r openclaw-skills/skills/reasoning-upgrade ~/.openclaw/workspace/skills/

# Or symlink (stays updated)
ln -s /path/to/openclaw-skills/skills/reasoning-upgrade ~/.openclaw/workspace/skills/reasoning-upgrade
```

Restart the gateway:
```bash
openclaw gateway restart
```

## Expected Impact

- Smaller models produce more structured, reliable responses
- Fewer hallucinated or unverified claims
- Better tool use (verify before claiming success)
- More concise communication (less filler, more substance)
- Better error recovery (diagnose before retrying)

This won't make a small model as intelligent as Opus — that's in the weights. But it will make it behave more like Opus in practice, which is what matters for agent reliability.

## License

MIT
