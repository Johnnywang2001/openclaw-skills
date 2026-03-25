# Dependency Audit

Audit project dependencies for outdated packages, known vulnerabilities, and license issues across Node.js (package.json), Python (requirements.txt, pyproject.toml), and Ruby (Gemfile) projects. Use when checking for outdated dependencies, scanning for vulnerable packages, reviewing dependency health, or preparing for upgrades.

## Installation

```bash
clawhub install dep-audit
```

## Usage

```bash
# Auto-detect and audit current directory
python3 scripts/dep_audit.py .
# Audit a specific file
python3 scripts/dep_audit.py package.json
```

## Requirements

- Python 3.7+

## License

MIT
