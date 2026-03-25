# Process Top

Monitor, search, and analyze running processes on macOS and Linux. Use when a user asks about running processes, CPU usage, memory hogs, what's consuming resources, finding a process by name, process summary, or system load.

## Installation

```bash
clawhub install process-top
```

## Usage

```bash
python3 scripts/process_top.py list
python3 scripts/process_top.py list --sort mem --limit 10
python3 scripts/process_top.py list --sort rss --json
```

```bash
python3 scripts/process_top.py search python
python3 scripts/process_top.py search "node|deno"
python3 scripts/process_top.py search nginx --json
```

```bash
python3 scripts/process_top.py summary
python3 scripts/process_top.py summary --json
```

## Requirements

- Python 3.7+
- macOS

## License

MIT
