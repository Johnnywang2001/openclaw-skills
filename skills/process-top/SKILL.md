---
name: process-top
description: Monitor, search, and analyze running processes on macOS and Linux. Use when a user asks about running processes, CPU usage, memory hogs, what's consuming resources, finding a process by name, process summary, or system load. Triggers on "top processes", "what's running", "high CPU", "memory usage", "find process", "process list", "kill process", "system resources", "ps aux".
---

# Process Top

Monitor and analyze running processes using `scripts/process_top.py` (Python 3, no external dependencies). Works on macOS and Linux.

## Commands

### List top processes

```bash
python3 scripts/process_top.py list
python3 scripts/process_top.py list --sort mem --limit 10
python3 scripts/process_top.py list --sort rss --json
```

Sort options: `cpu`, `mem`, `rss`, `pid`.

### Search for processes

```bash
python3 scripts/process_top.py search python
python3 scripts/process_top.py search "node|deno"
python3 scripts/process_top.py search nginx --json
```

Uses regex matching against command and user fields.

### System summary

```bash
python3 scripts/process_top.py summary
python3 scripts/process_top.py summary --json
```

Shows total process count, CPU/memory totals, process state breakdown, and top consumers.

### Group by command

```bash
python3 scripts/process_top.py group
python3 scripts/process_top.py group --sort cpu --limit 10
```

Aggregates processes by command name showing total count, CPU, and memory per group.
