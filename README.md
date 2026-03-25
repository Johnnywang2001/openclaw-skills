# OpenClaw Skills Collection

A curated collection of 72+ skills for [OpenClaw](https://openclaw.ai) — the open-source AI agent operating system.

Built and maintained by [@Johnnywang2001](https://github.com/Johnnywang2001).

---

## 🚀 First: Upgrade Your Agent

Before installing any skills, apply these two foundational upgrades. These are not skills — they're setup guides that fundamentally improve how your agent thinks and remembers.

You can implement both automatically with a single prompt (see below), or follow each guide manually.

### 🧠 Memory Upgrade — Make Your Agent Remember

**[→ OpenClaw Memory Upgrade Guide](skills/openclaw-memory-upgrade/SKILL.md)**

Transforms your agent from forgetting everything between sessions to having persistent, searchable memory across 6 upgrades:

1. **Enhanced memoryFlush** — automatically saves 8 categories of important info before context is lost
2. **Session indexing** — makes past conversations searchable
3. **Manual memory management** — two-tier file system (daily logs + curated long-term memory)
4. **QMD hybrid search** — keyword + semantic search with diversity ranking and recency bias
5. **Mem0 plugin** — auto-capture and auto-recall of memories
6. **Cognee** (optional) — graph-based memory (requires Docker)

### 🧹 Context Upgrade — Make Your Agent Think Efficiently

**[→ OpenClaw Context Upgrade Guide](skills/openclaw-context-upgrade/SKILL.md)**

Restructures your agent into an orchestrator pattern — the main session stays lean for conversation while sub-agents handle all the heavy lifting:

1. **Orchestrator delegation** — agent delegates research, coding, and file operations to sub-agents
2. **Sub-agent concurrency** — up to 8 parallel sub-agents for complex tasks
3. **Compaction safeguards** — higher thresholds to preserve conversation detail
4. **Context pruning** — automatically drops old context with TTL
5. **Pipeline pattern** — reusable PM → Workers → QA pattern for multi-step tasks

### ⚡ One-Prompt Setup (Both Upgrades)

Paste this into your OpenClaw agent to implement everything automatically:

```
Implement both the OpenClaw Memory Upgrade and Context Upgrade on this system. Read the guides at:
- ~/.openclaw/workspace/skills/openclaw-memory-upgrade/SKILL.md
- ~/.openclaw/workspace/skills/openclaw-context-upgrade/SKILL.md

For the Memory Upgrade: implement all 5 upgrades (skip Cognee/upgrade 6).
For the Context Upgrade: implement all 5 upgrades.

Merge all config changes into openclaw.json without overwriting existing settings.
Add all AGENTS.md instructions.
Install the Mem0 plugin.
Restart the gateway.
Report what you changed when done. Do not ask for permission at each step — execute the full upgrade.
```

**These are manual setup guides.** You'll need to copy the JSON config blocks from each guide into your `openclaw.json` file, or use the one-prompt setup above to have your agent do it for you.

---

## Installation

### Option 1: Install from ClawHub (if published)
```bash
clawhub install <skill-name>
```

### Option 2: Install directly from this GitHub repo

Clone the entire collection:
```bash
git clone https://github.com/Johnnywang2001/openclaw-skills.git
```

Then copy any skill folder into your OpenClaw workspace:
```bash
cp -r openclaw-skills/skills/<skill-name> ~/.openclaw/workspace/skills/
```

Or symlink it (stays updated when you `git pull`):
```bash
ln -s /path/to/openclaw-skills/skills/<skill-name> ~/.openclaw/workspace/skills/<skill-name>
```

To install ALL skills at once:
```bash
# Copy all
cp -r openclaw-skills/skills/* ~/.openclaw/workspace/skills/

# Or symlink all
for skill in openclaw-skills/skills/*/; do
  name=$(basename "$skill")
  ln -s "$(pwd)/$skill" ~/.openclaw/workspace/skills/$name
done
```

After adding skills, restart your OpenClaw gateway:
```bash
openclaw gateway restart
```

---

## What Are Skills?

Skills are modular packages that extend your OpenClaw agent's capabilities. Each skill provides specialized knowledge, workflows, scripts, or tool integrations that turn a general-purpose AI agent into a domain expert.

Each skill contains:
- `SKILL.md` — the core instructions the agent reads
- `scripts/` (optional) — executable scripts the agent can run
- `references/` (optional) — documentation or data files
- `README.md` — human-readable description and usage guide

---

## Skills Directory

### 🔒 Security & Networking
| Skill | Description |
|-------|-------------|
| [cors-tester](skills/cors-tester) | Test CORS configurations across endpoints |
| [dep-vuln-scanner](skills/dep-vuln-scanner) | Scan dependencies for known vulnerabilities |
| [file-hasher](skills/file-hasher) | Generate and verify file hashes (MD5, SHA256, etc.) |
| [http-sec-audit](skills/http-sec-audit) | Audit HTTP security headers |
| [ip-geo-toolkit](skills/ip-geo-toolkit) | IP geolocation lookups |
| [jwt-toolkit](skills/jwt-toolkit) | Decode, verify, and debug JWT tokens |
| [password-gen](skills/password-gen) | Generate secure passwords |
| [port-scanner](skills/port-scanner) | Scan ports on target hosts |
| [subdomain-enum](skills/subdomain-enum) | Enumerate subdomains for a domain |
| [subnet-calc](skills/subnet-calc) | Calculate subnets, CIDR ranges, and IP math |
| [whois-toolkit](skills/whois-toolkit) | WHOIS lookups for domains |
| [wifi-scanner](skills/wifi-scanner) | Scan and analyze WiFi networks |

### 🛠 Dev Tools
| Skill | Description |
|-------|-------------|
| [code-metrics](skills/code-metrics) | Analyze code complexity and metrics |
| [crontab-wizard](skills/crontab-wizard) | Generate and explain cron expressions |
| [dep-audit](skills/dep-audit) | Audit project dependencies |
| [dep-graph](skills/dep-graph) | Visualize dependency graphs |
| [encoding-toolkit](skills/encoding-toolkit) | Base64, URL, HTML encoding/decoding |
| [env-file-toolkit](skills/env-file-toolkit) | Validate and manage .env files |
| [git-hooks-toolkit](skills/git-hooks-toolkit) | Create and manage Git hooks |
| [git-stats](skills/git-stats) | Analyze Git repository statistics |
| [gitignore-gen](skills/gitignore-gen) | Generate .gitignore files by language/framework |
| [jrv-changelog-gen](skills/jrv-changelog-gen) | Generate changelogs from Git history |
| [jrv-env-doctor](skills/jrv-env-doctor) | Validate .env files, catch leaked secrets |
| [jrv-http-client](skills/jrv-http-client) | HTTP client for API testing |
| [jrv-mock-data](skills/jrv-mock-data) | Generate mock/fake data for testing |
| [jrv-text-diff](skills/jrv-text-diff) | Compare text files and show diffs |
| [jrv-yaml-toolkit](skills/jrv-yaml-toolkit) | Validate and manipulate YAML files |
| [json-diff](skills/json-diff) | Compare JSON files |
| [json-schema-toolkit](skills/json-schema-toolkit) | Validate and generate JSON schemas |
| [lorem-gen](skills/lorem-gen) | Generate lorem ipsum placeholder text |
| [regex-toolkit](skills/regex-toolkit) | Build, test, and explain regular expressions |
| [semver-toolkit](skills/semver-toolkit) | Parse and compare semantic versions |
| [sql-formatter](skills/sql-formatter) | Format and beautify SQL queries |
| [text-stats](skills/text-stats) | Word count, reading time, text analysis |
| [timezone-toolkit](skills/timezone-toolkit) | Convert between timezones |
| [uuid-toolkit](skills/uuid-toolkit) | Generate and validate UUIDs |

### 📊 DevOps & Monitoring
| Skill | Description |
|-------|-------------|
| [docker-audit](skills/docker-audit) | Audit Docker configurations |
| [disk-usage-analyzer](skills/disk-usage-analyzer) | Analyze disk usage |
| [jrv-log-analyzer](skills/jrv-log-analyzer) | Analyze log files with error fingerprinting |
| [jrv-ssl-monitor](skills/jrv-ssl-monitor) | Monitor SSL certificate expiry |
| [network-speed-test](skills/network-speed-test) | Test network speed |
| [process-top](skills/process-top) | Monitor running processes |
| [uptime-checker](skills/uptime-checker) | Check website uptime |

### 🌐 SEO & Web
| Skill | Description |
|-------|-------------|
| [dead-link-scanner](skills/dead-link-scanner) | Find broken links on websites |
| [htaccess-gen](skills/htaccess-gen) | Generate Apache .htaccess files |
| [robots-txt-gen](skills/robots-txt-gen) | Generate robots.txt files |
| [seo-audit-report](skills/seo-audit-report) | Run SEO audits on websites |
| [sitemap-generator](skills/sitemap-generator) | Generate XML sitemaps |

### 🤖 Agent Self-Improvement
| Skill | Description |
|-------|-------------|
| [self-improving-agent](skills/self-improving-agent) | Capture learnings and errors for continuous improvement |
| [find-skills](skills/find-skills) | Discover and install skills on the fly |
| [auto-updater](skills/auto-updater) | Auto-update OpenClaw and skills daily |
| [memory-setup](skills/memory-setup) | Configure memory search for persistent context |
| [memory-tiering](skills/memory-tiering) | Multi-tiered memory management (HOT/WARM/COLD) |

### 📝 Obsidian & Notes
| Skill | Description |
|-------|-------------|
| [save-to-obsidian](skills/save-to-obsidian) | Save content to Obsidian vault via SSH |
| [obsidian-organizer](skills/obsidian-organizer) | Organize and standardize Obsidian vaults |
| [obsidian-daily-mai](skills/obsidian-daily-mai) | Obsidian daily note management |
| [obsidian-openclaw-sync](skills/obsidian-openclaw-sync) | Sync OpenClaw config across iCloud devices |

### 💼 Business & Productivity
| Skill | Description |
|-------|-------------|
| [api-cost-tracker](skills/api-cost-tracker) | Track API usage costs |
| [app-store-optimization](skills/app-store-optimization) | App Store keyword research and optimization |
| [competitor-monitor](skills/competitor-monitor) | Monitor competitor activity |
| [email-validator](skills/email-validator) | Validate email addresses |
| [invoice-generator](skills/invoice-generator) | Generate invoices |
| [price-tracker](skills/price-tracker) | Track product prices |

### 📚 Reference & Utilities
| Skill | Description |
|-------|-------------|
| [color-toolkit](skills/color-toolkit) | Color conversion and palette tools |
| [csv-toolkit](skills/csv-toolkit) | Parse and manipulate CSV files |
| [exif-toolkit](skills/exif-toolkit) | Read and edit image EXIF data |
| [http-status-ref](skills/http-status-ref) | HTTP status code reference |
| [text-toolkit](skills/text-toolkit) | Text manipulation utilities |
| [toml-toolkit](skills/toml-toolkit) | Parse and validate TOML files |
| [yaml-validator](skills/yaml-validator) | Validate YAML syntax |
| [net-speed-test](skills/net-speed-test) | Network speed testing |

---

## License

MIT

## Contributing

Pull requests welcome. Each skill should have a `SKILL.md` at its root following the [OpenClaw skill format](https://docs.openclaw.ai).
