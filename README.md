# OpenClaw Skills Collection

27 curated, high-quality skills for [OpenClaw](https://openclaw.ai) — the open-source AI agent operating system. Plus 4 setup guides that fundamentally improve how your agent thinks, remembers, and operates.

Every skill here genuinely extends what an agent can do. No filler, no utilities an LLM already knows how to do natively.

Built and maintained by [@Johnnywang2001](https://github.com/Johnnywang2001).

---

## 🚀 Start Here: Upgrade Your Agent

Before installing any skills, apply these foundational upgrades. They're not skills — they're setup guides that change how your agent operates at a fundamental level.

### 🧪 Reasoning Upgrade — Make Any Model Think Like Opus

**[→ Reasoning Upgrade Skill](skills/reasoning-upgrade/SKILL.md)**

Based on published research (Think² metacognitive framework, Chain-of-Thought, ReAct, Tree of Thoughts, Stanford's LLM Reasoning Failures survey), this skill injects frontier-level reasoning patterns into any model. ~2,450 tokens per session.

- **Think² three-phase cycle:** Plan before acting, Monitor during execution, Evaluate before delivering (3x self-correction improvement in research)
- **Goal coherence (anti-drift):** Maintain objective across multi-step chains — the #1 failure mode in smaller models on agentic tasks
- **Robustness guards:** Anti-hallucination, anti-anchoring, anti-pattern-matching, precision preservation
- **First-attempt completion:** Front-load preparation to match Opus's first-try success rate
- **Self-consistency checks:** Solve hard problems two ways, compare results
- **Tree of Thoughts:** Generate multiple approaches, evaluate, pursue the best
- **Adaptive effort allocation:** Fast path for simple questions, deep reasoning for complex ones
- **Tool use discipline:** ReAct pattern — Reason → Act → Observe → Reason again

---

### 🧠 Memory Upgrade — Make Your Agent Remember

**[→ OpenClaw Memory Upgrade Guide](guides/memory-upgrade/SKILL.md)**

Transforms your agent from forgetting everything between sessions to having persistent, searchable memory across 6 upgrades:

1. **Enhanced memoryFlush** — automatically saves 8 categories of important info before context is lost
2. **Session indexing** — makes past conversations searchable
3. **Manual memory management** — two-tier file system (daily logs + curated long-term memory)
4. **QMD hybrid search** — keyword + semantic search with diversity ranking and recency bias
5. **Mem0 plugin** — auto-capture and auto-recall of memories
6. **Cognee** (optional) — graph-based memory (requires Docker)

### 🧹 Context Upgrade — Make Your Agent Think Efficiently

**[→ OpenClaw Context Upgrade Guide](guides/context-upgrade/SKILL.md)**

Restructures your agent into an orchestrator pattern — the main session stays lean for conversation while sub-agents handle all the heavy lifting:

1. **Orchestrator delegation** — agent delegates research, coding, and file operations to sub-agents
2. **Sub-agent concurrency** — up to 8 parallel sub-agents for complex tasks
3. **Compaction safeguards** — higher thresholds to preserve conversation detail
4. **Context pruning** — automatically drops old context with TTL
5. **Pipeline pattern** — reusable PM → Workers → QA pattern for multi-step tasks

### 🔄 Seamless Model Switching — Stop Crashes When Changing Models

**[→ Seamless Model Switching Guide](guides/seamless-model-switching/article.md)**

If you use multiple LLM models, switching between them mid-session can cause crashes and context loss. This guide explains the four root causes and six config-level fixes.

### ⚡ One-Prompt Setup (All Upgrades)

Paste this into your OpenClaw agent to implement the Memory and Context upgrades automatically:

```
Implement both the OpenClaw Memory Upgrade and Context Upgrade on this system. Read the guides at:
- ~/.openclaw/workspace/guides/memory-upgrade/SKILL.md
- ~/.openclaw/workspace/guides/context-upgrade/SKILL.md

For the Memory Upgrade: implement all 5 upgrades (skip Cognee/upgrade 6).
For the Context Upgrade: implement all 5 upgrades.

Merge all config changes into openclaw.json without overwriting existing settings.
Add all AGENTS.md instructions.
Install the Mem0 plugin.
Restart the gateway.
Report what you changed when done. Do not ask for permission at each step — execute the full upgrade.
```

---

## Installation

### From this GitHub repo

Clone the collection:
```bash
git clone https://github.com/Johnnywang2001/openclaw-skills.git
```

Copy any skill into your workspace:
```bash
cp -r openclaw-skills/skills/<skill-name> ~/.openclaw/workspace/skills/
```

Or symlink (stays updated when you `git pull`):
```bash
ln -s /path/to/openclaw-skills/skills/<skill-name> ~/.openclaw/workspace/skills/<skill-name>
```

Install ALL skills at once:
```bash
for skill in openclaw-skills/skills/*/; do
  name=$(basename "$skill")
  ln -s "$(pwd)/$skill" ~/.openclaw/workspace/skills/$name
done
```

After adding skills, restart the gateway:
```bash
openclaw gateway restart
```

---

## Skills Directory

### 🤖 Agent Self-Improvement
| Skill | Description |
|-------|-------------|
| [reasoning-upgrade](skills/reasoning-upgrade) | **Inject Opus-level reasoning into any model** — Think², goal coherence, robustness guards, first-attempt completion |
| [self-improving-agent](skills/self-improving-agent) | Capture learnings, errors, and corrections for continuous improvement |
| [find-skills](skills/find-skills) | Discover and install skills on the fly |
| [auto-updater](skills/auto-updater) | Auto-update OpenClaw and skills daily |
| [memory-setup](skills/memory-setup) | Configure memory search for persistent context |
| [memory-tiering](skills/memory-tiering) | Multi-tiered memory management (HOT/WARM/COLD) |

### 🔒 Security
| Skill | Description |
|-------|-------------|
| [dep-vuln-scanner](skills/dep-vuln-scanner) | Scan dependencies for known CVEs via OSV.dev API |
| [docker-audit](skills/docker-audit) | Audit Dockerfiles and docker-compose for security issues |
| [http-sec-audit](skills/http-sec-audit) | Audit HTTP security headers on live URLs |
| [jrv-env-doctor](skills/jrv-env-doctor) | Catch leaked secrets in .env files (AWS, GitHub, Stripe, etc.) |
| [port-scanner](skills/port-scanner) | TCP port scanning for network recon and security auditing |

### 📊 DevOps & Monitoring
| Skill | Description |
|-------|-------------|
| [jrv-log-analyzer](skills/jrv-log-analyzer) | Analyze log files — error fingerprinting, severity breakdown, anomaly detection |
| [jrv-ssl-monitor](skills/jrv-ssl-monitor) | Monitor SSL certificate expiry across multiple domains |
| [network-speed-test](skills/network-speed-test) | Measure download/upload speed and latency |
| [jrv-yaml-toolkit](skills/jrv-yaml-toolkit) | Validate, format, convert, merge, and query YAML files |

### 🌐 SEO & Web
| Skill | Description |
|-------|-------------|
| [dead-link-scanner](skills/dead-link-scanner) | Crawl websites and find broken links |
| [seo-audit-report](skills/seo-audit-report) | Run comprehensive SEO audits with actionable reports |
| [sitemap-generator](skills/sitemap-generator) | Generate XML sitemaps by crawling a website |

### 💼 Business & Productivity
| Skill | Description |
|-------|-------------|
| [api-cost-tracker](skills/api-cost-tracker) | Track and optimize LLM API spending across providers |
| [app-store-optimization](skills/app-store-optimization) | App Store keyword research and metadata optimization |
| [competitor-monitor](skills/competitor-monitor) | Monitor competitor websites, pricing, and product changes |
| [invoice-generator](skills/invoice-generator) | Generate professional PDF invoices |
| [price-tracker](skills/price-tracker) | Track product prices and alert on changes |

### 📝 Obsidian & Notes
| Skill | Description |
|-------|-------------|
| [save-to-obsidian](skills/save-to-obsidian) | Save content to Obsidian vault via SSH |
| [obsidian-organizer](skills/obsidian-organizer) | Organize and standardize Obsidian vaults |
| [obsidian-daily-mai](skills/obsidian-daily-mai) | Obsidian daily note management |
| [obsidian-openclaw-sync](skills/obsidian-openclaw-sync) | Sync OpenClaw config across iCloud devices |

---

## Guides

| Guide | Description |
|-------|-------------|
| [Memory Upgrade](guides/memory-upgrade) | 6-step guide to persistent, searchable agent memory |
| [Context Upgrade](guides/context-upgrade) | Orchestrator pattern for efficient context window usage |
| [Seamless Model Switching](guides/seamless-model-switching) | Fix crashes and context loss when changing models |
| [How to Create an Effective AI Agent](guides/how-to-create-an-effective-ai-agent) | Practical guide for building AI agents |

---

## License

MIT

## Contributing

Pull requests welcome. Quality bar: every skill must genuinely extend what an OpenClaw agent can do. If an LLM can already do it natively without a skill, it doesn't belong here.
