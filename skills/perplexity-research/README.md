# Perplexity Research

Deep web research via Perplexity Pro browser automation. Zero API cost — uses a Pro subscription through the OpenClaw managed browser.

## What It Does

This skill provides a zero-cost deep research pipeline by automating Perplexity Pro through browser automation:

- **Browser-based search** — Navigates to perplexity.ai, enters queries, reads responses via snapshots
- **Multi-source research** — Run multiple targeted queries for comprehensive coverage
- **Optional verification** — Spawn a free-model agent to cross-check findings
- **Organized output** — Key findings, numbered sources, confidence levels, coverage gaps

## When to Use

- Deep research requiring multiple web sources
- "Research X for me" or "Find out about..."
- Fact-checking or source verification
- Skill creation research
- Any task where `web_fetch` or `ollama_web_search` isn't deep enough

**Not for:** Simple factual lookups (use `ollama_web_search` instead — it's faster).

## Pipeline

```
1. Search on Perplexity (browser, free via Pro subscription)
2. Read response + extract sources
3. If verification needed → spawn agent on free model
4. Return organized findings with sources and confidence
```

## Installation

```bash
# From GitHub
cp -r openclaw-skills/skills/perplexity-research ~/.openclaw/workspace/skills/

# Or symlink (stays updated)
ln -s /path/to/openclaw-skills/skills/perplexity-research ~/.openclaw/workspace/skills/perplexity-research
```

Restart the gateway:
```bash
openclaw gateway restart
```

## Prerequisites

- Perplexity Pro subscription logged in via the OpenClaw managed browser
- OpenClaw browser automation capability

## Cost

| Component | Cost |
|-----------|------|
| Perplexity search | $0.00 (Pro sub) |
| Verification agent | $0.00 (free model) |
| **Total per task** | **$0.00** |

## License

MIT
