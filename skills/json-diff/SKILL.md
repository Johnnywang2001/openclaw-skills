---
name: json-diff
description: Compare two JSON files and show differences. Use when asked to diff JSON, compare API responses, find config changes, detect schema drift, or compare two JSON objects. Shows added, removed, and changed keys with clear color-coded output. Also triggers on "compare json", "json changes", "what changed in config", or "diff two files".
---

# json-diff

Compare two JSON files or objects and display a clear, structured diff.

## Quick Start

```bash
# Compare two JSON files
python3 scripts/json_diff.py old.json new.json

# Output as JSON patch (RFC 6902)
python3 scripts/json_diff.py old.json new.json --format patch

# Output as flat key paths
python3 scripts/json_diff.py old.json new.json --format flat

# Ignore specific keys
python3 scripts/json_diff.py old.json new.json --ignore-keys timestamp updated_at

# Compare from stdin (pipe one file, pass the other)
cat old.json | python3 scripts/json_diff.py - new.json

# Show only specific change types
python3 scripts/json_diff.py old.json new.json --only added removed

# Summary only (count of changes)
python3 scripts/json_diff.py old.json new.json --summary
```

## Output Formats

| Format | Flag | Description |
|--------|------|-------------|
| Tree (default) | `--format tree` | Indented tree showing changes with +/−/~ markers |
| Flat | `--format flat` | Dot-notation key paths with change type |
| Patch | `--format patch` | JSON Patch (RFC 6902) operations array |

## Options

| Flag | Description |
|------|-------------|
| `--format FORMAT` | Output format: tree, flat, or patch |
| `--ignore-keys KEY ...` | Keys to ignore during comparison |
| `--only TYPE ...` | Show only: added, removed, changed |
| `--summary` | Show change count summary only |
| `--no-color` | Disable colored output |
| `--exit-code` | Exit 1 if differences found (for CI) |
