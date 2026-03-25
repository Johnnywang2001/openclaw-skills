# Disk Usage Analyzer

Analyze disk usage, find large files, detect potential duplicates, and get cleanup recommendations for any directory. Use when a user asks about disk space, storage usage, large files, cleanup suggestions, finding duplicates, or freeing up space on their filesystem.

## Installation

```bash
clawhub install disk-usage-analyzer
```

## Usage

```bash
python3 scripts/disk_usage.py scan /path/to/dir
python3 scripts/disk_usage.py scan /path/to/dir --depth 2 --limit 20
python3 scripts/disk_usage.py scan /path/to/dir --json
```

```bash
python3 scripts/disk_usage.py find-large /path/to/dir --threshold 100MB
python3 scripts/disk_usage.py find-large ~ --threshold 1GB --json
```

```bash
python3 scripts/disk_usage.py duplicates /path/to/dir
python3 scripts/disk_usage.py duplicates /path/to/dir --min-size 10MB
```

## Requirements

- Python 3.7+

## License

MIT
