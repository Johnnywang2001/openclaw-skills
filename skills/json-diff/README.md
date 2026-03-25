# JSON Diff

Compare two JSON files and show differences. Use when asked to diff JSON, compare API responses, find config changes, detect schema drift, or compare two JSON objects. Shows added, removed, and changed keys with clear color-coded output.

## Installation

```bash
clawhub install json-diff
```

## Usage

```bash
# Compare two JSON files
python3 scripts/json_diff.py old.json new.json
# Output as JSON patch (RFC 6902)
python3 scripts/json_diff.py old.json new.json --format patch
```

## Requirements

- Python 3.7+

## License

MIT
