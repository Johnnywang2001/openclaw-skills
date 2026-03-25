---
name: disk-usage-analyzer
description: Analyze disk usage, find large files, detect potential duplicates, and get cleanup recommendations for any directory. Use when a user asks about disk space, storage usage, large files, cleanup suggestions, finding duplicates, or freeing up space on their filesystem. Triggers on "disk usage", "disk space", "large files", "storage", "free up space", "what's taking space", "find big files", "duplicate files".
---

# Disk Usage Analyzer

Scan directories to understand storage consumption with breakdowns by directory, file type, and individual files.

## Commands

All commands use `scripts/disk_usage.py` (Python 3, no external dependencies).

### Scan a directory

```bash
python3 scripts/disk_usage.py scan /path/to/dir
python3 scripts/disk_usage.py scan /path/to/dir --depth 2 --limit 20
python3 scripts/disk_usage.py scan /path/to/dir --json
```

Shows: total size, top directories by size with visual bar chart, largest files, and extension breakdown.

Options:
- `--depth N` — directory grouping depth (default: 1)
- `--limit N` — number of top items to show (default: 15)
- `--json` — output raw JSON for further processing

### Find large files

```bash
python3 scripts/disk_usage.py find-large /path/to/dir --threshold 100MB
python3 scripts/disk_usage.py find-large ~ --threshold 1GB --json
```

Lists all files above the given size threshold.

### Detect potential duplicates

```bash
python3 scripts/disk_usage.py duplicates /path/to/dir
python3 scripts/disk_usage.py duplicates /path/to/dir --min-size 10MB
```

Groups files by identical size (quick heuristic for spotting duplicates without hashing).

## Tips

- Start with `scan .` to get a high-level overview, then drill into specific directories
- Use `--json` flag to pipe output into other tools or for programmatic analysis
- For cleanup: combine `find-large` results with `duplicates` to identify quick wins
- The scan handles permission errors gracefully and reports them at the end
