---
name: dep-audit
description: Audit project dependencies for outdated packages, known vulnerabilities, and license issues across Node.js (package.json), Python (requirements.txt, pyproject.toml), and Ruby (Gemfile) projects. Use when checking for outdated dependencies, scanning for vulnerable packages, reviewing dependency health, or preparing for upgrades. Triggers on "audit dependencies", "check for outdated packages", "vulnerability scan", "dependency health", "are my packages up to date", "npm audit", "pip audit", "outdated deps".
---

# Dependency Audit

Scan project dependency files for outdated packages, known vulnerabilities, and health issues.

## Quick Start

```bash
# Auto-detect and audit current directory
python3 scripts/dep_audit.py .

# Audit a specific file
python3 scripts/dep_audit.py package.json
python3 scripts/dep_audit.py requirements.txt
python3 scripts/dep_audit.py Gemfile

# JSON output
python3 scripts/dep_audit.py . --format json

# Only show outdated packages
python3 scripts/dep_audit.py . --outdated-only
```

## Supported Ecosystems

| File | Ecosystem | Checks |
|------|-----------|--------|
| package.json | Node.js/npm | Latest versions via npm registry |
| requirements.txt | Python/pip | Latest versions via PyPI |
| pyproject.toml | Python/Poetry | Latest versions via PyPI |
| Gemfile | Ruby/Bundler | Latest versions via RubyGems |

## What It Reports

- **Current version** vs **latest available**
- **Update type**: major, minor, patch
- **Packages behind**: count of outdated dependencies
- **Pinning issues**: unpinned or loosely pinned versions
- **Age**: how far behind the latest release

## Output

Text output shows a table per dependency file. JSON output provides structured data for pipeline integration.
