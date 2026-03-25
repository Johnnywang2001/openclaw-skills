# Crontab Wizard

Explain, generate, validate, and preview crontab expressions. Use when a user needs to understand what a cron expression means, create a new cron schedule, check if a cron expression is valid, or see when a cron job will run next. Supports standard 5-field cron syntax and shortcuts like @daily, @hourly, @weekly. No dependencies required.

## Installation

```bash
clawhub install crontab-wizard
```

## Usage

```bash
# Explain what a cron expression does
python3 scripts/cronwiz.py explain "*/5 * * * *"
# Generate an expression from options
python3 scripts/cronwiz.py generate --every 5m
```

## Requirements

- Python 3 (no external dependencies)

## License

MIT
