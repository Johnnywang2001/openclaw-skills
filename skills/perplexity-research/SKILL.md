---
name: perplexity-research
description: "Deep web research via Perplexity Pro browser automation. Zero API cost -- uses John's Pro subscription through the OpenClaw managed browser. Use when asked to research a topic, find current information, verify claims, or gather sources. Preferred over web_fetch or ollama_web_search for deep research tasks."
---

# Perplexity Research

Deep research pipeline using Perplexity Pro via browser automation. All research is free (Pro subscription), verification uses free models.

## When to Use

- "Research X for me"
- "Find out about..."
- "What's the latest on..."
- Deep research for skill creation
- Fact-checking or source verification
- Any task requiring multiple web sources

## Pipeline

```
1. Search on Perplexity (browser, free)
2. Read response + sources
3. If verification needed: spawn agent on nemotron-3-super-free
4. Return organized findings
```

## Step 1: Search Perplexity

Always use the OpenClaw managed browser (not profile="user"):

```
browser navigate → https://www.perplexity.ai/
browser act → click textbox, type query, press Enter
browser act → wait 10000ms (let response fully render)
browser snapshot → read the response
```

**Model selection:** Leave on **Sonar** (default). It's optimized for search. Only switch models if the user explicitly asks.

**For deep research:** Use Perplexity's "Deep Research" follow-up buttons when available, or ask multi-part follow-up questions in the same thread.

## Step 2: Extract Response

From the snapshot, extract:
- The full answer text
- Source count and key citations
- Follow-up suggestions (useful for deeper dives)

**Multi-query research:** For comprehensive topics, run 2-3 targeted queries instead of one broad one. Each query is free.

## Step 3: Verify (Optional)

Only verify when:
- Claims seem surprising or extraordinary
- Specific numbers/statistics are cited
- The research will be used for published content or critical decisions

Spawn a verification agent:

```
model: opencode-zen/nemotron-3-super-free (free)
task: "Verify these findings. Check that source URLs are real and claims are consistent. Flag anything suspicious."
```

Skip verification for:
- General knowledge queries
- Opinion/recommendation requests
- Exploratory research where precision isn't critical

## Step 4: Organize Output

Return findings as:
- Key findings (bullet points)
- Sources (numbered, with URLs)
- Confidence level (high/medium/low based on source agreement)
- Gaps (what wasn't well-covered)

## Cost Breakdown

| Component | Model | Cost |
|-----------|-------|------|
| Perplexity search | Sonar (Pro sub) | $0.00 |
| Verification agent | nemotron-3-super-free | $0.00 |
| Follow-up searches | Sonar (Pro sub) | $0.00 |
| **Total per research task** | | **$0.00** |

## Important Notes

- John is logged into Perplexity Pro in the OpenClaw managed browser
- Session persists across restarts -- no need to re-login
- Perplexity Pro = unlimited searches
- Do NOT use Perplexity API (costs credits). Always use the browser.
- For simple factual lookups, ollama_web_search is faster. Use Perplexity for deep/multi-source research.

## Example Usage

**User:** "Research the current state of SwiftUI adoption in production apps"

**Agent workflow:**
1. Navigate to perplexity.ai
2. Search: "SwiftUI adoption in production iOS apps 2026 statistics"
3. Wait for response, read snapshot
4. Follow up: "What are the main pain points developers report with SwiftUI in production?"
5. Read second response
6. Compile findings with sources
7. Return organized summary

**User:** "Deep research into App Store optimization strategies"

**Agent workflow:**
1. Search: "App Store Optimization best practices 2026"
2. Search: "ASO keyword research strategies that work"
3. Search: "App Store screenshot optimization conversion rates"
4. Compile all three responses
5. Spawn nemotron verification agent if publishing the research
6. Return comprehensive report with all sources
