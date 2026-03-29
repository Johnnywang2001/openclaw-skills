---
name: jrv-yaml-toolkit
description: Full-featured YAML toolkit for validating, formatting, converting, merging, and querying YAML files. Supports YAML-to-JSON, JSON-to-YAML, schema validation, path queries, and multi-document YAML.
---

# jrv-yaml-toolkit

Everything you need to work with YAML files: validate syntax, format/prettify, convert to/from JSON, query with dot-path expressions, merge multiple files, and check against a schema.

## Quick Start

```bash
# Validate YAML syntax
python3 scripts/yaml_toolkit.py validate config.yaml

# Format/prettify YAML
python3 scripts/yaml_toolkit.py format messy.yaml

# Convert YAML to JSON
python3 scripts/yaml_toolkit.py to-json config.yaml

# Convert JSON to YAML
python3 scripts/yaml_toolkit.py from-json data.json

# Query a value by dot-path
python3 scripts/yaml_toolkit.py get config.yaml "server.host"

# Set a value
python3 scripts/yaml_toolkit.py set config.yaml "server.port" 8080

# Merge multiple YAML files (later files override earlier)
python3 scripts/yaml_toolkit.py merge base.yaml override.yaml

# Lint a file for duplicate keys, tabs, syntax errors
python3 scripts/yaml_toolkit.py lint config.yaml

# Lint an entire directory recursively
python3 scripts/yaml_toolkit.py lint ./configs/

# Lint with strict checks (trailing whitespace, long lines)
python3 scripts/yaml_toolkit.py lint config.yaml --strict

# Lint with JSON output
python3 scripts/yaml_toolkit.py lint config.yaml --json

# Lint against a schema file
python3 scripts/yaml_toolkit.py lint config.yaml --schema schema.yaml

# List all keys (flattened dot-path)
python3 scripts/yaml_toolkit.py keys config.yaml

# Minify YAML (single-line flow style)
python3 scripts/yaml_toolkit.py minify config.yaml
```

## Commands

| Command | Description |
|---------|-------------|
| `validate <file>` | Check YAML syntax, report errors with line numbers |
| `format <file>` | Pretty-print YAML with consistent indentation |
| `to-json <file>` | Convert YAML to JSON |
| `from-json <file>` | Convert JSON to YAML |
| `get <file> <path>` | Get value at dot-path (e.g. `server.host`) |
| `set <file> <path> <val>` | Set value at dot-path, output updated YAML |
| `merge <file1> <file2> ...` | Deep-merge YAML files (right overrides left) |
| `lint <file>` | Lint YAML for duplicate keys, tabs, syntax errors |
| `lint <dir>` | Recursively lint all .yaml/.yml files in a directory |
| `lint <file> --schema <s>` | Validate keys against a schema YAML |
| `keys <file>` | List all keys as flattened dot-paths |
| `minify <file>` | Output compact single-line YAML |

## Options

| Flag | Description |
|------|-------------|
| `--output <file>` | Write output to file instead of stdout |
| `--indent N` | Indentation spaces (default: 2) |
| `--allow-unicode` | Allow unicode in output (default: true) |
| `--strict` | Lint: also check trailing whitespace, long lines (>256 chars) |
| `--quiet` | Lint: only show errors, suppress info/warnings |
| `--json` | Lint: output results as JSON |

## Use Cases

- **DevOps**: Validate Kubernetes and Docker Compose configs before applying
- **CI/CD**: Merge environment-specific YAML overrides
- **Config management**: Query and patch config values programmatically
- **Data pipelines**: Convert between JSON and YAML for different tools
- **Documentation**: List all config keys for auto-generated docs

## Exit Codes

- `0` — Success
- `1` — Validation error or key not found
- `2` — File not found or parse error
