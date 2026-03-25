# Auto Updater

Automatically update OpenClaw and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed.

## Installation

```bash
clawhub install auto-updater
```

## Usage

```bash
Set up daily auto-updates for yourself and all your skills.
```

```bash
openclaw cron add \
  --name "Daily Auto-Update" \
  --cron "0 4 * * *" \
  --tz "America/Los_Angeles" \
```

## License

MIT
