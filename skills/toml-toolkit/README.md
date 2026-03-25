# TOML Toolkit

Validate, query, convert, merge, and inspect TOML files. Use when working with TOML configuration files (pyproject.toml, Cargo.toml, config.toml), converting between TOML and JSON, querying specific keys, validating syntax, listing all keys, or merging multiple TOML files.

## Installation

```bash
clawhub install toml-toolkit
```

## Usage

```bash
python3 scripts/toml_toolkit.py validate config.toml
```

```bash
python3 scripts/toml_toolkit.py query pyproject.toml tool.poetry.name
python3 scripts/toml_toolkit.py query Cargo.toml package.version
```

```bash
python3 scripts/toml_toolkit.py to-json config.toml
python3 scripts/toml_toolkit.py to-json config.toml -o config.json --compact
```

## Requirements

- Python 3.11+

## License

MIT
