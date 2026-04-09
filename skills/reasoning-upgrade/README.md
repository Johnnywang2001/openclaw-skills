# Reasoning Upgrade

Inject frontier-level reasoning patterns into any OpenClaw agent, regardless of which model powers it.

## What It Does

This skill upgrades how an agent works, not just how it sounds. It produces observable behavior change:

- **Better decisions** — clarifies goals, considers alternatives, verifies before claiming
- **Tighter writing** — no filler, direct answers, structure when it helps
- **Stronger verification** — checks facts, tests changes, surfaces uncertainty
- **Fewer unforced errors** — reads errors before retrying, stops when blocked

The skill covers:

- **Behavioral delta** — how to tell if it's working
- **Response defaults** — match effort to stakes, choose format for clarity
- **Decision rules** — when to act vs ask, when to delegate vs do directly
- **Reasoning loop** — clarify, constrain, consider alternatives, verify
- **Execution loop** — plan, gather context, execute, verify, report
- **Tool discipline** — search before guessing, read output, check exit codes
- **Communication style** — be direct, calm, useful; have opinions when they help
- **Error handling** — what failed, why, what next; diagnose before retrying
- **Anti-patterns** — signs the skill is failing

## Why It Matters

When switching from a frontier model (Opus, GPT-5) to a cost-effective model (Sonnet, GLM-5, MiniMax), the quality drop often isn't in knowledge — it's in reasoning discipline. Smaller models:

- Skip steps and make assumptions
- Chain actions without verifying
- Give verbose answers that dodge the actual question
- Use filler phrases and performative helpfulness
- Report success without checking

This skill closes that gap by making the reasoning process explicit rather than implicit.

## Key Principles

1. **Answer the request, don't paraphrase it.**
2. **Check before asserting.** Files, tools, state — verify specifics.
3. **Be as short as the task allows, and no shorter.**
4. **Match effort to stakes.** Low stakes = fast. High stakes = verify.
5. **No filler.** Skip "Great question", "Happy to help", etc.
6. **Verify important work before claiming completion.**
7. **Read errors before retrying.** Same action + same conditions = same failure.
8. **Admit uncertainty plainly.** "I don't know" beats a fluent hallucination.

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

- More structured, reliable responses from smaller models
- Fewer hallucinated or unverified claims
- Better tool use (verify before claiming success)
- More concise communication (less filler, more substance)
- Better error recovery (diagnose before retrying)
- Observable behavior change, not just tone adjustment

This won't make a small model as intelligent as a frontier model — that's in the weights. But it will make it behave more like one in practice, which is what matters for agent reliability.

## Version History

- **v2.0** (2026-04-08) — Complete rewrite: behavior-first approach, decision rules, execution loop, anti-patterns
- **v1.0** — Initial release: Think² framework, CoT, ReAct, ToT patterns

## License

MIT
