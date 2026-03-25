---
name: yaml-validator
description: Validate and lint YAML files for syntax errors, duplicate keys, tab indentation, and structural issues. Use when checking YAML configs (Kubernetes manifests, CI/CD pipelines, docker-compose, Ansible playbooks, etc.) for correctness. Supports strict mode, JSON output, directory scanning, and multi-document YAML.
---

# YAML Validator

Validate YAML files for common issues including syntax errors, duplicate keys, tab characters, and structural problems.

## Quick Start

```bash
# Validate a single file
python3 scripts/yaml_validate.py config.yaml

# Validate multiple files
python3 scripts/yaml_validate.py *.yaml

# Scan an entire directory recursively
python3 scripts/yaml_validate.py ./k8s/

# Strict mode (checks trailing whitespace, long lines)
python3 scripts/yaml_validate.py --strict deployment.yaml

# JSON output for programmatic use
python3 scripts/yaml_validate.py --json config.yaml

# Quiet mode (errors only)
python3 scripts/yaml_validate.py --quiet *.yml
```

## What It Checks

- **Syntax errors** — invalid YAML with line/column numbers
- **Duplicate keys** — keys repeated in the same mapping
- **Tab characters** — YAML requires spaces, not tabs
- **Empty files** — warns on zero-content files
- **Multi-document** — detects and reports `---` separated documents
- **Strict mode** — trailing whitespace, lines over 256 chars

## Exit Codes

- `0` — all files valid
- `1` — one or more files have errors

## Requirements

- Python 3.7+
- PyYAML (`pip3 install pyyaml`) — pre-installed on most systems
