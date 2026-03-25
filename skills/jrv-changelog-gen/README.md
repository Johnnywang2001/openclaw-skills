# Changelog Generator

Generate changelogs from git commit history with conventional commit parsing. Use when asked to generate a changelog, create release notes, summarize git history, list changes between tags or dates, or prepare release documentation. Supports conventional commits (feat, fix, docs, etc.), breaking change detection, grouped output, and markdown or JSON format. No external dependencies.

## Installation

```bash
clawhub install jrv-changelog-gen
```

## Usage

```bash
python3 scripts/changelog_gen.py
python3 scripts/changelog_gen.py --since v1.0.0 --group
python3 scripts/changelog_gen.py --since v1.0.0 --until v2.0.0 --format json
python3 scripts/changelog_gen.py --repo /path/to/project --since "2026-01-01" -o CHANGELOG.md
```

## Requirements

- Python 3 (no external dependencies)

## License

MIT
