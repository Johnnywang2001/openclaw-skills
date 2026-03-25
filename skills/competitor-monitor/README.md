# Competitor Monitor

Monitor competitors' websites, social media, pricing, and product changes automatically. Use when the user wants to track competitor activity, detect website changes, monitor pricing updates, track new features or blog posts, get alerts on competitor moves, or conduct ongoing competitive intelligence. Supports scheduled checks with configurable alert channels.

## Installation

```bash
clawhub install competitor-monitor
```

## Usage

```bash
python3 scripts/monitor.py add --name "Acme Corp" --url https://acme.com --track pricing,blog,changelog
```

```bash
python3 scripts/monitor.py check --all
```

## Requirements

- Python 3.7+

## License

MIT
