# Seamless Model Switching in OpenClaw

## The Problem Everyone Has

Switching models in OpenClaw breaks things. You're chatting with Opus, switch to Codex or Sonnet, and suddenly the agent forgets what you were talking about, crashes with context overflow errors, or starts behaving erratically.

This isn't a user error — it's a known architectural gap. Here's what actually happens under the hood and how to fix it.

## Why Model Switching Breaks Things

There are four distinct failure modes, each with a different cause:

### 1. Context Window Mismatch

The most common crash. You've been chatting on a model with a 1M token context window (like GPT-5.4 Codex). Your session accumulates 300K tokens of history. You switch to a model with a 200K window (like Sonnet). OpenClaw tries to send 300K tokens to a model that only accepts 200K.

**Result:** `Context overflow: prompt too large for the model` or a hard gateway crash.

**GitHub Issue #44303** documents this — switching from GPT-5.4 (1.05M context) to Qwen 3.5 (128K context) mid-session caused the gateway to lock up entirely, requiring a manual restart.

### 2. Cache Invalidation

OpenClaw uses prompt caching to save money and speed up responses. Your current model might have a 99% cache hit rate. When you switch to a different model (or even a different provider for the same model), the entire cache becomes useless — different tokenizer, different cache keys.

**Result:** Suddenly every prompt is processed from scratch. If the session is large, this triggers compaction, which summarizes and discards conversation detail.

### 3. Context Window Not Updating

**GitHub Issue #8240** found that when a model switch occurs (manual or failover), the session's reported context window doesn't update to reflect the new model's actual limit. The system still thinks it has 400K tokens available when the new model only supports 200K.

**Result:** Compaction fires too late or not at all. The agent keeps accumulating context until it hits the real limit, then crashes.

### 4. Workspace Injection Mismatch

**GitHub Issue #13557** identified that OpenClaw injects the same workspace files (MEMORY.md, daily notes, SOUL.md, etc.) regardless of which model is active. A 128K context model gets the same file payload as a 1M context model.

**Result:** On smaller models, workspace files can consume a disproportionate share of the context window, leaving little room for actual conversation.

## The Fixes

### Fix 1: Standardize Context Windows Across Models

The simplest prevention. Set all your models to the same context window so switching never triggers overflow.

In `openclaw.json` under `models.providers`, set explicit `contextWindow` values:

```json
{
  "models": {
    "providers": {
      "anthropic": {
        "models": [
          {
            "id": "claude-opus-4-6",
            "contextWindow": 200000,
            "maxTokens": 32768
          },
          {
            "id": "claude-sonnet-4-6",
            "contextWindow": 200000,
            "maxTokens": 32768
          }
        ]
      },
      "openai-codex": {
        "models": [
          {
            "id": "gpt-5.4-codex",
            "contextWindow": 200000,
            "maxTokens": 32768
          }
        ]
      }
    }
  }
}
```

By capping all models at 200K (the lowest common denominator among your models), context will never exceed any model's limit when you switch. You sacrifice the full context window of larger models, but you gain seamless switching.

**Tradeoff:** If you need the full 1M context of Codex for specific tasks, don't cap it — use Fix 2 instead.

### Fix 2: Manual Compact Before Switching

Before switching models, always run `/compact` or tell the agent to flush its memory:

```
Compact this conversation and write everything important to today's memory file. I'm about to switch models.
```

This triggers the memoryFlush (if configured from the Memory Upgrade), saves important context to files, and reduces the session size before the switch.

**Make this a habit:** If you're going to switch, compact first. The 10 seconds it takes saves you from a crash and context loss.

### Fix 3: Use Fallback Chains Instead of Manual Switching

Instead of manually switching models, configure fallback chains and let OpenClaw handle routing:

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-opus-4-6",
        "fallbacks": [
          "openai-codex/gpt-5.4-codex",
          "anthropic/claude-sonnet-4-6"
        ]
      }
    }
  }
}
```

When the primary model is rate-limited or unavailable, OpenClaw automatically falls to the next one. The session stays intact because the fallback logic is built into the same request cycle.

**Important:** Ensure your fallback models have context windows equal to or larger than your primary. If Opus (200K) falls back to Codex (1M), no problem. If it fell back to a 32K model, you'd hit Fix 1's issue.

### Fix 4: Start a New Session When Changing Models

The cleanest approach for deliberate model changes. Instead of switching mid-conversation:

1. Tell the agent to save everything important to memory files
2. Start a new session (the agent reads MEMORY.md and daily notes fresh)
3. Set the new model on the fresh session

The new session loads your workspace files, has full context from memory, and starts clean on the new model. No overflow, no cache invalidation, no mismatch.

### Fix 5: Configure Model-Aware Compaction Thresholds

Raise your compaction thresholds so the system has more buffer when a switch triggers emergency compaction:

```json
{
  "compaction": {
    "mode": "safeguard",
    "reserveTokensFloor": 30000,
    "memoryFlush": {
      "enabled": true,
      "softThresholdTokens": 6000
    }
  }
}
```

Higher `reserveTokensFloor` (30K instead of default 20K) means the agent always keeps more breathing room. Higher `softThresholdTokens` (6K) means memory flush triggers earlier, saving more context before compaction fires.

### Fix 6: Context Pruning with TTL

Enable automatic pruning of old context so your session stays lean enough to survive a switch:

```json
{
  "contextPruning": {
    "mode": "cache-ttl",
    "ttl": "45m"
  }
}
```

Context older than 45 minutes gets pruned automatically. This keeps your session size manageable, making any model switch safer because there's less accumulated context to worry about.

## The Ideal Setup

Combine all fixes for maximum resilience:

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-opus-4-6",
        "fallbacks": [
          "openai-codex/gpt-5.4-codex",
          "anthropic/claude-sonnet-4-6"
        ]
      },
      "compaction": {
        "mode": "safeguard",
        "reserveTokensFloor": 30000,
        "memoryFlush": {
          "enabled": true,
          "softThresholdTokens": 6000,
          "systemPrompt": "Session nearing compaction. Analyze the conversation and extract durable memories NOW before context is lost.",
          "prompt": "Scan the current conversation and write any of the following to memory/YYYY-MM-DD.md (use today's date):\n\n1. DECISIONS made (with reasoning and context)\n2. USER PREFERENCES or corrections expressed\n3. TECHNICAL DETAILS (commands, configs, API keys, endpoints, file paths)\n4. PROJECT STATUS changes or milestones\n5. PEOPLE mentioned (names, roles, contact info, relationships)\n6. WORKFLOWS or processes described\n7. ERRORS encountered and their solutions\n8. OPINIONS or feedback the user gave\n\nFor each item, include timestamps and enough context that future-you can understand it without the conversation. If nothing meaningful happened, reply with NO_REPLY."
        }
      },
      "contextPruning": {
        "mode": "cache-ttl",
        "ttl": "45m"
      }
    }
  },
  "models": {
    "providers": {
      "anthropic": {
        "models": [
          {
            "id": "claude-opus-4-6",
            "contextWindow": 200000,
            "maxTokens": 32768
          },
          {
            "id": "claude-sonnet-4-6",
            "contextWindow": 200000,
            "maxTokens": 32768
          }
        ]
      }
    }
  }
}
```

## What OpenClaw Should Fix (But Hasn't Yet)

Several feature requests and PRs exist but haven't been merged:

- **Pre-compaction on model switch** (Issue #6404) — Auto-compact before sending to a smaller model. Proposed but not shipped.
- **Context profiles per model** (Issue #13557) — Different workspace file injection based on which model is active. Proposed with detailed spec, not shipped.
- **Block risky model switches** (PR #44389) — Prevent switching to a model that can't handle current context. Open PR, not merged.
- **Graceful truncation** (Issue #44303) — Instead of crashing, truncate context to fit new model. Not implemented.

Until these ship, the fixes above are your best defense.

## Quick Reference

| Scenario | What To Do |
|----------|-----------|
| Switching to a model with a smaller context window | Compact first, or standardize context windows |
| Random crashes when switching | Check context window sizes match between models |
| Agent forgets everything after switch | Ensure memoryFlush is enabled, use file-based memory |
| Want automatic failover without thinking about it | Use fallback chains, keep fallback context windows >= primary |
| Long session, want to change models | Start a new session instead of switching mid-conversation |

## Sources

- [GitHub Issue #44303](https://github.com/openclaw/openclaw/issues/44303) — Hard crash on smaller-context model switch
- [GitHub Issue #8240](https://github.com/openclaw/openclaw/issues/8240) — Context window not updating on model switch
- [GitHub Issue #13557](https://github.com/openclaw/openclaw/issues/13557) — Context profiles per model proposal
- [GitHub Issue #6404](https://github.com/openclaw/openclaw/issues/6404) — Pre-compaction on model switch
- [GitHub PR #44389](https://github.com/openclaw/openclaw/pull/44389) — Block risky model switches
