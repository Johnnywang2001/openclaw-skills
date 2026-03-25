# Env File Toolkit

Manage .env files with validate, diff, template generation, merge, and missing-key checks. Use when working with environment variable files, comparing .env.local vs .env.production, generating .env.example templates, validating .env syntax, merging env files, or checking for missing environment variables.

## Installation

```bash
clawhub install env-file-toolkit
```

## Usage

```bash
python3 scripts/env_toolkit.py validate .env
```

```bash
python3 scripts/env_toolkit.py diff .env.local .env.production
```

```bash
python3 scripts/env_toolkit.py template .env
python3 scripts/env_toolkit.py template .env -o .env.example
python3 scripts/env_toolkit.py template .env --keep-values  # keep actual values
```

## Requirements

- Python 3.7+

## License

MIT
