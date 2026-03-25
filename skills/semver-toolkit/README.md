# SemVer Toolkit

Semantic Versioning (SemVer 2.0.0) toolkit for parsing, validating, comparing, bumping, and sorting version strings. Use when working with software versions, release management, version bumps, or checking if version strings conform to semver spec.

## Installation

```bash
clawhub install semver-toolkit
```

## Usage

```bash
# Parse a version into components
python3 scripts/semver_toolkit.py parse 1.2.3-beta.1+build.42
# Validate versions
python3 scripts/semver_toolkit.py validate 1.0.0 v2.1 not-a-version
```

## Requirements

- Python 3.7+

## License

MIT
