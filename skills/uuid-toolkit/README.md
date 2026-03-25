# UUID Toolkit

Generate, parse, validate, and convert UUIDs (v1/v3/v4/v5), ULIDs, and NanoIDs. Use when creating unique identifiers, parsing existing UUIDs to extract version/timestamp/node info, validating identifier formats, converting between UUID representations (hex, base64, URN, integer), or generating bulk IDs. No external dependencies.

## Installation

```bash
clawhub install uuid-toolkit
```

## Usage

```bash
# Generate a UUIDv4
python3 scripts/uuid_toolkit.py generate uuid4
# Generate 10 ULIDs
python3 scripts/uuid_toolkit.py generate ulid --count 10
```

## Requirements

- Python 3 (no external dependencies)

## License

MIT
