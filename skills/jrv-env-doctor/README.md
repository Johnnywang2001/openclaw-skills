# Env Doctor

Validate .env files for common issues — detect leaked secrets (AWS keys, GitHub tokens, Stripe keys, JWTs), find duplicate variables, flag empty values, compare against .env.example templates, and catch syntax errors. Use when asked to check .env files, audit environment variables, scan for leaked secrets, validate env configuration, or compare .env against .env.example. No external dependencies.

## Installation

```bash
clawhub install jrv-env-doctor
```

## Usage

```bash
python3 scripts/env_doctor.py .env
python3 scripts/env_doctor.py .env --example .env.example
python3 scripts/env_doctor.py .env --strict --json
```

## Requirements

- Python 3 (no external dependencies)

## License

MIT
