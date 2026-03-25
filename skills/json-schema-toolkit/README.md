# JSON Schema Toolkit

Validate JSON data against JSON Schema, generate schemas from sample JSON, and convert schemas to TypeScript interfaces, Python dataclasses, or Markdown docs. Use when working with JSON validation, API contract testing, schema generation from examples, or converting JSON Schema to typed code. No external dependencies — pure Python.

## Installation

```bash
clawhub install json-schema-toolkit
```

## Usage

```bash
python3 scripts/json_schema.py generate --input sample.json
python3 scripts/json_schema.py generate --input sample.json --output schema.json
echo '{"name":"Jo","age":25}' | python3 scripts/json_schema.py generate --input -
```

```bash
python3 scripts/json_schema.py validate --schema schema.json --data data.json
```

```bash
python3 scripts/json_schema.py convert --input schema.json --format typescript
python3 scripts/json_schema.py convert --input schema.json --format python-dataclass
python3 scripts/json_schema.py convert --input schema.json --format markdown --name User
```

## Requirements

- Python 3 (no external dependencies)

## License

MIT
