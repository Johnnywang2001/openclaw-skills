---
name: openclaw-context-upgrade
description: Optimize OpenClaw's context window usage by delegating heavy tasks to sub-agents, keeping the main session lightweight for conversation. Includes automatic implementation via a single prompt.
---

# OpenClaw Context Upgrade

Your agent's context window is its most valuable resource. Every tool call, every file read, every long response eats into it. Once it fills up, compaction kicks in and context gets summarized — losing detail in the process.

This upgrade restructures how your agent works so the main session stays lean and conversational while sub-agents handle all the heavy lifting.

## The Problem

In a default OpenClaw setup:
```
You → Agent (does EVERYTHING in one session)
        - Reads files (tokens consumed)
        - Runs commands (output fills context)
        - Does research (web fetches fill context)
        - Writes code (large outputs)
        - Manages memory (more tokens)
        - Responds to you (finally)
```

Result: your context fills up fast, compaction fires frequently, and the agent loses track of earlier conversation details.

## The Solution

Split the workload:
```
You → Orchestrator (lightweight, conversational)
        - Understands your request
        - Delegates to the right sub-agent
        - Summarizes results back to you
        - Context stays clean

      Sub-agents (disposable, heavy lifting)
        - Research agent: web searches, URL fetching, deep dives
        - Code agent: file reads, writes, edits, exec commands
        - Memory agent: searches memory, reads files, updates notes
        - Each agent gets its own fresh context window
        - Results summarized back to orchestrator
```

The orchestrator's context only contains your conversation and summaries — never raw tool output, file contents, or command results.

## Prerequisites

- OpenClaw 2026.3.0 or later
- Recommended: Complete the [Memory Upgrade](../memory-upgrade/SKILL.md) first
- A model that supports sub-agent spawning (Claude Opus/Sonnet, GPT-5.x, etc.)

---

## Upgrade 1: Orchestrator Delegation Pattern

**What it does:** Instructs the main agent to delegate all heavy tasks to sub-agents instead of doing them directly.

**Add to your `AGENTS.md` (workspace root):**

```markdown
## Context Management — Delegation Rules

You are the ORCHESTRATOR. Your job is to talk to the user and coordinate work. You do NOT do heavy processing yourself.

### What you do directly (in this session):
- Read and respond to user messages
- Make decisions about what needs to happen
- Summarize sub-agent results for the user
- Read MEMORY.md and daily notes at session start
- Quick, small tool calls (checking time, simple status)

### What you DELEGATE to sub-agents:
- Any web research (spawn a research agent)
- Reading large files or codebases (spawn a code agent)
- Running shell commands with potentially large output
- Writing or editing multiple files
- Deep analysis of documents or URLs
- Any task that would consume more than ~2,000 tokens of context

### How to delegate:
1. Identify the task type
2. Spawn a sub-agent with a clear, specific task description
3. Include all context the sub-agent needs in the task prompt
4. Wait for the sub-agent to complete
5. Summarize the result concisely for the user (don't paste raw output)

### Sub-agent models:
- Research tasks: use the default model
- Code tasks: use the default model with high thinking
- Simple tasks: use a cheaper/faster model if available
- Always set a reasonable timeout (300-600 seconds for most tasks)

### Context budget:
- Keep your context under 50% of the window at all times
- If a user asks for something that would require reading 5+ files, delegate it
- If a command might output more than 50 lines, delegate it
- Prefer spawning 2-3 focused sub-agents over one mega-agent
```

---

## Upgrade 2: Sub-Agent Configuration

**What it does:** Configures OpenClaw to support efficient sub-agent spawning with appropriate concurrency and model settings.

**Add to `openclaw.json` under `agents.defaults`:**

```json
{
  "agents": {
    "defaults": {
      "maxConcurrent": 4,
      "subagents": {
        "maxConcurrent": 8
      }
    }
  }
}
```

**Config explained:**
- `maxConcurrent: 4` — up to 4 agent sessions can run simultaneously
- `subagents.maxConcurrent: 8` — up to 8 sub-agents can run in parallel (for research fanning out across multiple sources)

---

## Upgrade 3: Compaction Safeguards

**What it does:** Configures compaction to be more aggressive about preserving context quality, working alongside the delegation pattern to keep the main session lean.

**Add to `openclaw.json` under `agents.defaults.compaction`:**

```json
{
  "compaction": {
    "mode": "safeguard",
    "reserveTokensFloor": 30000,
    "memoryFlush": {
      "enabled": true,
      "softThresholdTokens": 6000,
      "systemPrompt": "Session nearing compaction. Analyze the conversation and extract durable memories NOW before context is lost.",
      "prompt": "Scan the current conversation and write any of the following to memory/YYYY-MM-DD.md (use today's date):\n\n1. DECISIONS made (with reasoning and context)\n2. USER PREFERENCES or corrections expressed\n3. TECHNICAL DETAILS (commands, configs, API keys, endpoints, file paths)\n4. PROJECT STATUS changes or milestones\n5. PEOPLE mentioned (names, roles, contact info, relationships)\n6. WORKFLOWS or processes described\n7. ERRORS encountered and their solutions\n8. OPINIONS or feedback the user gave\n\nFor each item, include timestamps and enough context that future-you can understand it without the conversation. If nothing meaningful happened, reply with NO_REPLY."
    }
  }
}
```

**Differences from the Memory Upgrade defaults:**
- `reserveTokensFloor: 30000` (up from 20000) — more breathing room since the orchestrator should stay lean
- `softThresholdTokens: 6000` (up from 4000) — triggers memory flush earlier, giving more time to save context

---

## Upgrade 4: Context Pruning

**What it does:** Automatically prunes old context that's no longer relevant, keeping the session window fresh.

**Add to `openclaw.json` under `agents.defaults`:**

```json
{
  "contextPruning": {
    "mode": "cache-ttl",
    "ttl": "45m"
  }
}
```

**Config explained:**
- `mode: "cache-ttl"` — prunes context entries older than the TTL
- `ttl: "45m"` — context older than 45 minutes gets pruned (sub-agent results are already summarized, so raw data can be dropped)

---

## Upgrade 5: Pipeline Pattern for Complex Tasks

**What it does:** Establishes a reusable pattern for multi-step tasks that would normally consume enormous context.

**Add to your `AGENTS.md`:**

```markdown
## Pipeline Pattern

For complex, multi-step tasks, use the pipeline pattern:

### Structure:
- Orchestrator (you) → PM sub-agent → Worker sub-agents → QA sub-agent → back to you

### When to use:
- Tasks with 3+ steps that each require different tools
- Research + analysis + output generation workflows
- Anything that would take more than 10 minutes of agent work

### How it works:
1. Orchestrator receives the request and spawns a PM agent
2. PM breaks the task into steps and spawns worker agents
3. Workers execute in parallel where possible
4. PM compiles results and optionally spawns a QA agent
5. Final result comes back to Orchestrator as a summary
6. Orchestrator presents the summary to the user

### Benefits:
- Each agent gets a fresh context window
- Parallel execution for independent tasks
- QA catches errors before results reach the user
- Orchestrator context stays clean throughout
```

---

## Automatic Implementation

To implement all Context Upgrade changes automatically, paste this single prompt into your OpenClaw agent:

```
Implement the OpenClaw Context Upgrade on this system. Read the guide at:
guides/context-upgrade/SKILL.md (or ~/.openclaw/workspace/guides/context-upgrade/SKILL.md)

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

If you also need the Memory Upgrade, use this combined prompt:

```
Implement both the OpenClaw Memory Upgrade and Context Upgrade on this system. Read the guides at:
- guides/memory-upgrade/SKILL.md
- guides/context-upgrade/SKILL.md

For the Memory Upgrade: implement all 5 upgrades (skip Cognee/upgrade 6).
For the Context Upgrade: implement all 5 upgrades.

Merge all config changes into openclaw.json without overwriting existing settings.
Add all AGENTS.md instructions.
Install the Mem0 plugin.
Restart the gateway.
Report what you changed when done.
```

---

## How It All Fits Together

```
BEFORE (everything in one session):
You → Agent [context: 100%+ → compaction → loses detail]

AFTER (orchestrator + sub-agents):
You → Orchestrator [context: ~20-30%, stays lean]
        ├── Research Agent [fresh context, disposable]
        ├── Code Agent [fresh context, disposable]
        ├── Memory Agent [fresh context, disposable]
        └── Pipeline PM → Workers → QA [each fresh context]
```

**Expected improvements:**
- Main session context usage drops 50-70%
- Compaction fires less frequently
- Conversation history preserved longer
- Parallel sub-agents complete complex tasks faster
- Each sub-agent gets full context window for its specific task

## Estimated Token Overhead

Sub-agent spawning adds a small overhead per delegation:
- Task prompt to sub-agent: ~500-1,000 tokens
- Summary returned: ~200-500 tokens
- Net savings: typically 5,000-50,000+ tokens per task (the raw tool output that would have filled your main context)

The delegation overhead pays for itself on the first task that would have consumed more than 2,000 tokens of context.
