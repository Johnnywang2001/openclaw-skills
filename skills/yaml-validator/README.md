# YAML Validator

Validate and lint YAML files for syntax errors, duplicate keys, tab indentation, and structural issues. Use when checking YAML configs (Kubernetes manifests, CI/CD pipelines, docker-compose, Ansible playbooks, etc.) for correctness. Supports strict mode, JSON output, directory scanning, and multi-document YAML.

## Installation

```bash
clawhub install yaml-validator
```

## Usage

```bash
# Validate a single file
python3 scripts/yaml_validate.py config.yaml
# Validate multiple files
python3 scripts/yaml_validate.py *.yaml
```

## Requirements

- Python 3.7+

## License

MIT
