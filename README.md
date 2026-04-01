# OpenClaw Skills Collection

74 skills for [OpenClaw](https://openclaw.ai) — the open-source AI agent operating system. Plus 7 setup guides that fundamentally improve how your agent thinks, remembers, and operates.

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

### 🧬 Skill Evolution — An Agent That Writes Its Own Skills

**[→ Skill Evolution](skills/skill-evolution/SKILL.md)**

Based on the [AutoSkill framework](https://arxiv.org/abs/2603.01145) (Yang et al., 2026), this skill turns your agent into a self-improving system. After each session, the agent analyzes the conversation, extracts durable patterns, and writes them as versioned skills that get injected into future sessions automatically.

```
Conversation → Skill Extraction → SkillBank (versioned + indexed) → Auto-retrieval in future sessions
```

- **Automatic extraction:** Identifies stable preferences, corrections, recurring workflows, and domain conventions from real conversations
- **Smart filtering:** Skips one-off requests, generic knowledge, and temporary instructions — only durable patterns become skills
- **Version management:** New patterns create skills; similar patterns merge into existing ones with version bumps
- **Vector retrieval:** Future queries automatically pull the most relevant skills into context via embedding search
- **Self-pruning:** Skills that get retrieved but never used are automatically pruned
- **Human-editable:** Every skill is a plain SKILL.md file you can review and revise

The result: your agent gets better at your specific workflows the more you use it — without you manually writing any instructions.

---

### ⚡ One-Prompt Setup (All 4 Upgrades)

First, clone the repo into your workspace:
```bash
git clone https://github.com/Johnnywang2001/openclaw-skills.git ~/.openclaw/workspace/openclaw-skills
```

Then paste this into your OpenClaw agent:

```
Implement all four OpenClaw upgrades on this system. The guides are at ~/.openclaw/workspace/openclaw-skills. Read and follow each guide:

1. REASONING UPGRADE — Copy the skill into the workspace:
   cp -r ~/.openclaw/workspace/openclaw-skills/skills/reasoning-upgrade ~/.openclaw/workspace/skills/

2. MEMORY UPGRADE — Read ~/.openclaw/workspace/openclaw-skills/guides/memory-upgrade/SKILL.md
   Implement all 5 upgrades (skip Cognee/upgrade 6).
   Install the Mem0 plugin: openclaw plugin install @mem0/openclaw-mem0

3. CONTEXT UPGRADE — Read ~/.openclaw/workspace/openclaw-skills/guides/context-upgrade/SKILL.md
   Implement all 5 upgrades. Add delegation rules and pipeline pattern to AGENTS.md.

4. SEAMLESS MODEL SWITCHING — Read ~/.openclaw/workspace/openclaw-skills/guides/seamless-model-switching/article.md
   Apply Fix 1 (standardize context windows), Fix 3 (fallback chains), Fix 5 (compaction thresholds), and Fix 6 (context pruning).

For all upgrades:
- Merge config changes into openclaw.json without overwriting existing settings.
- Add all AGENTS.md instructions.
- Restart the gateway: openclaw gateway restart
- Verify: openclaw status

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
| [reasoning-upgrade](skills/reasoning-upgrade) | Inject Opus-level reasoning into any model — Think², goal coherence, robustness guards, first-attempt completion |
| [self-improving-agent](skills/self-improving-agent) | Capture learnings, errors, and corrections for continuous improvement |
| [skill-evolution](skills/skill-evolution) | AutoSkill-powered self-evolving skills — automatic extraction from conversations, versioned merging, vector retrieval |
| [find-skills](skills/find-skills) | Discover and install skills on the fly |
| [auto-updater](skills/auto-updater) | Auto-update OpenClaw and skills daily |
| [memory-tiering](skills/memory-tiering) | Multi-tiered memory management (HOT/WARM/COLD) |
| [openclaw-memory-upgrade](skills/openclaw-memory-upgrade) | Complete 6-step guide to persistent, searchable agent memory |

### 🔒 Security
| Skill | Description |
|-------|-------------|
| [docker-audit](skills/docker-audit) | Audit Dockerfiles and docker-compose for security issues |
| [http-sec-audit](skills/http-sec-audit) | Audit HTTP security headers on live URLs |
| [jrv-env-doctor](skills/jrv-env-doctor) | Catch leaked secrets in .env files (AWS, GitHub, Stripe, etc.) |
| [port-scanner](skills/port-scanner) | TCP port scanning for network recon and security auditing |
| [subdomain-enum](skills/subdomain-enum) | Enumerate subdomains via DNS brute-force and certificate transparency logs |
| [password-gen](skills/password-gen) | Generate secure passwords, passphrases, and PINs with entropy analysis |
| [jwt-toolkit](skills/jwt-toolkit) | Decode, inspect, and validate JWT tokens |
| [email-validator](skills/email-validator) | Validate email addresses with MX checks and disposable email detection |

### 📊 DevOps & Monitoring
| Skill | Description |
|-------|-------------|
| [jrv-log-analyzer](skills/jrv-log-analyzer) | Analyze log files — error fingerprinting, severity breakdown, anomaly detection |
| [jrv-ssl-monitor](skills/jrv-ssl-monitor) | Monitor SSL certificate expiry across multiple domains |
| [uptime-checker](skills/uptime-checker) | Check URL uptime, response times, and SSL status |
| [network-speed-test](skills/network-speed-test) | Measure download/upload speed and latency |
| [process-top](skills/process-top) | Monitor running processes, CPU, and memory usage |
| [disk-usage-analyzer](skills/disk-usage-analyzer) | Analyze disk usage, find large files, detect duplicates |
| [wifi-scanner](skills/wifi-scanner) | Scan and analyze nearby WiFi networks and signal strength |

### 🔧 Git & GitHub
| Skill | Description |
|-------|-------------|
| [github-repo-manager](skills/github-repo-manager) | Production GitHub repo management — branching, PRs, versioning, releases, branch protection, CI/CD hygiene |
| [git-stats](skills/git-stats) | Analyze git repo statistics — contributors, commit frequency, lines of code |
| [git-hooks-toolkit](skills/git-hooks-toolkit) | Generate and manage Git hooks with pre-built templates |
| [gitignore-gen](skills/gitignore-gen) | Generate .gitignore files from 200+ GitHub templates |
| [jrv-changelog-gen](skills/jrv-changelog-gen) | Generate changelogs from git history with conventional commit parsing |
| [semver-toolkit](skills/semver-toolkit) | Parse, validate, compare, bump, and sort semantic versions |

### 📱 iOS Development
| Skill | Description |
|-------|-------------|
| [ios-app-publisher](skills/ios-app-publisher) | Complete iOS app publishing lifecycle — Xcode setup, code signing, App Store Connect, TestFlight, submission, post-launch |
| [ios-ui-design](skills/ios-ui-design) | iOS UI/UX design with SwiftUI/UIKit — HIG compliance, design systems, accessibility, App Store visual optimization |
| [app-store-optimization](skills/app-store-optimization) | App Store keyword research and metadata optimization |

### 🌐 SEO & Web
| Skill | Description |
|-------|-------------|
| [seo-audit-report](skills/seo-audit-report) | Run comprehensive SEO audits with actionable reports |
| [dead-link-scanner](skills/dead-link-scanner) | Crawl websites and find broken links |
| [sitemap-generator](skills/sitemap-generator) | Generate XML sitemaps by crawling a website |
| [robots-txt-gen](skills/robots-txt-gen) | Generate, validate, and analyze robots.txt files |
| [htaccess-gen](skills/htaccess-gen) | Generate .htaccess files for Apache (redirects, rewrites, security headers) |
| [cors-tester](skills/cors-tester) | Test and debug CORS configurations on live URLs |
| [http-status-ref](skills/http-status-ref) | HTTP status code reference, lookup, and header analyzer |

### 💼 Business & Productivity
| Skill | Description |
|-------|-------------|
| [api-cost-tracker](skills/api-cost-tracker) | Track and optimize LLM API spending across providers |
| [competitor-monitor](skills/competitor-monitor) | Monitor competitor websites, pricing, and product changes |
| [invoice-generator](skills/invoice-generator) | Generate professional PDF invoices |
| [price-tracker](skills/price-tracker) | Track product prices and alert on changes |

### 🔬 Research
| Skill | Description |
|-------|-------------|
| [perplexity-research](skills/perplexity-research) | Zero-cost deep research via Perplexity Pro browser automation with optional free-model verification |

### 📝 Obsidian & Notes
| Skill | Description |
|-------|-------------|
| [save-to-obsidian](skills/save-to-obsidian) | Save content to Obsidian vault via SSH |
| [obsidian-organizer](skills/obsidian-organizer) | Organize and standardize Obsidian vaults |
| [obsidian-daily-mai](skills/obsidian-daily-mai) | Obsidian daily note management |
| [obsidian-openclaw-sync](skills/obsidian-openclaw-sync) | Sync OpenClaw config across iCloud devices |

### 🛠️ Code Quality & Analysis
| Skill | Description |
|-------|-------------|
| [code-metrics](skills/code-metrics) | Analyze code quality — lines of code, complexity, function counts, comment ratios |
| [dep-audit](skills/dep-audit) | Audit dependencies for outdated packages, vulnerabilities, and license issues |
| [dep-graph](skills/dep-graph) | Analyze and visualize project dependency trees |
| [sql-formatter](skills/sql-formatter) | Format, minify, and lint SQL queries |
| [regex-toolkit](skills/regex-toolkit) | Test, match, extract, replace, and explain regular expressions |

### 📄 Data & File Formats
| Skill | Description |
|-------|-------------|
| [json-diff](skills/json-diff) | Compare two JSON files and show differences |
| [json-schema-toolkit](skills/json-schema-toolkit) | Validate JSON against schemas, generate schemas from samples, convert to TypeScript/Python |
| [jrv-yaml-toolkit](skills/jrv-yaml-toolkit) | Validate, format, convert, merge, and query YAML files |
| [toml-toolkit](skills/toml-toolkit) | Validate, query, convert, and merge TOML files |
| [csv-toolkit](skills/csv-toolkit) | View, filter, sort, convert, and analyze CSV files |
| [env-file-toolkit](skills/env-file-toolkit) | Manage .env files — validate, diff, template, merge, and check for missing keys |

### 🔤 Text & Encoding
| Skill | Description |
|-------|-------------|
| [text-toolkit](skills/text-toolkit) | Swiss-army knife for text manipulation — case conversion, slugify, extract emails/URLs, deduplicate |
| [text-stats](skills/text-stats) | Word count, readability scores, reading time, vocabulary statistics |
| [jrv-text-diff](skills/jrv-text-diff) | Compare text files side-by-side or unified with word-level diff |
| [encoding-toolkit](skills/encoding-toolkit) | Encode/decode Base64, Hex, URL, HTML entities, ROT13, Binary, plus hash functions |
| [lorem-gen](skills/lorem-gen) | Generate placeholder text — Lorem Ipsum, hipster, tech jargon |
| [color-toolkit](skills/color-toolkit) | Convert, analyze, and generate colors — HEX, RGB, HSL, WCAG contrast, palette generation |

### 🌍 Networking & IP
| Skill | Description |
|-------|-------------|
| [ip-geo-toolkit](skills/ip-geo-toolkit) | IP geolocation, public IP lookup, reverse DNS, bulk processing |
| [subnet-calc](skills/subnet-calc) | CIDR and subnet calculator — network address, broadcast, host range, IPv4/IPv6 |
| [whois-toolkit](skills/whois-toolkit) | Domain WHOIS lookup — registrar, expiry dates, nameservers, registrant info |

### 🧰 Utilities
| Skill | Description |
|-------|-------------|
| [uuid-toolkit](skills/uuid-toolkit) | Generate, parse, validate UUIDs (v1/v3/v4/v5), ULIDs, and NanoIDs |
| [file-hasher](skills/file-hasher) | Compute, verify, and compare file hashes (MD5, SHA-256, SHA-512) |
| [timezone-toolkit](skills/timezone-toolkit) | Convert times between timezones, world clocks, meeting overlap finder |
| [exif-toolkit](skills/exif-toolkit) | Read, write, and strip EXIF/image metadata from photos |
| [crontab-wizard](skills/crontab-wizard) | Explain, generate, validate, and preview crontab expressions |
| [jrv-mock-data](skills/jrv-mock-data) | Generate realistic fake data — names, emails, addresses, UUIDs, dates |
| [jrv-http-client](skills/jrv-http-client) | Make HTTP requests with auth, headers, JSON body — agent-friendly curl replacement |

---

## Guides

| Guide | Description |
|-------|-------------|
| [Memory Upgrade](guides/memory-upgrade) | 6-step guide to persistent, searchable agent memory |
| [Context Upgrade](guides/context-upgrade) | Orchestrator pattern for efficient context window usage |
| [Seamless Model Switching](guides/seamless-model-switching) | Fix crashes and context loss when changing models |
| [How to Create an Effective AI Agent](guides/how-to-create-an-effective-ai-agent) | Practical guide for building AI agents |
| [AI Agents for Data Analysis](guides/ai-agents-for-data-analysis) | How to create AI agents that transform your data analysis workflow |
| [Streamline Workflows with AI Agents](guides/streamline-workflows-with-ai-agents) | Practical playbook for identifying, mapping, and automating your highest-value workflows |
| [Implement Agentic Workflows](guides/implement-agentic-workflows) | End-to-end guide to implementing agentic workflows — architecture patterns, platform selection, and a 30-day deployment plan |

---

## Related Projects

| Project | Description |
|---------|-------------|
| [claw-mini](https://github.com/Johnnywang2001/claw-mini) | Zero-dependency Python CLI coding agent — full tool-calling agent in pure stdlib Python. No pip install needed, just `python -m claw`. |
| [claw-code](https://github.com/Johnnywang2001/claw-code) | Clean-room rewrite of Claw Code's agent harness in Python and Rust. |

---

## License

MIT

## Contributing

Pull requests welcome. Quality bar: every skill must genuinely extend what an OpenClaw agent can do. If an LLM can already do it natively without a skill, it doesn't belong here.
