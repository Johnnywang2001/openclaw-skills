---
name: toml-toolkit
description: Validate, query, convert, merge, and inspect TOML files. Use when working with TOML configuration files (pyproject.toml, Cargo.toml, config.toml), converting between TOML and JSON, querying specific keys, validating syntax, listing all keys, or merging multiple TOML files. Triggers on "toml", "pyproject.toml", "Cargo.toml", "toml to json", "json to toml", "validate toml", "merge config".
---

# TOML Toolkit

Work with TOML files using `scripts/toml_toolkit.py` (Python 3.11+, no external dependencies).

## Commands

### Validate syntax

```bash
python3 scripts/toml_toolkit.py validate config.toml
```

Reports validity, key count, and table count. Exits non-zero on invalid TOML.

### Query a key

```bash
python3 scripts/toml_toolkit.py query pyproject.toml tool.poetry.name
python3 scripts/toml_toolkit.py query Cargo.toml package.version
```

Supports dotted key paths. Returns the value (or JSON for nested objects/arrays).

### Convert TOML → JSON

```bash
python3 scripts/toml_toolkit.py to-json config.toml
python3 scripts/toml_toolkit.py to-json config.toml -o config.json --compact
```

### Convert JSON → TOML

```bash
python3 scripts/toml_toolkit.py to-toml data.json
python3 scripts/toml_toolkit.py to-toml data.json -o output.toml
```

### List all keys

```bash
python3 scripts/toml_toolkit.py keys pyproject.toml
```

Shows every key path including nested tables — useful for exploring unfamiliar config files.

### Merge TOML files

```bash
python3 scripts/toml_toolkit.py merge base.toml overrides.toml -o merged.toml
```

Deep-merges multiple files. Later files override earlier ones. Useful for environment-specific configs.
