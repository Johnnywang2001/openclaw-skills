# JWT Toolkit

Decode, inspect, and validate JWT (JSON Web Token) tokens from the command line. Shows header, payload, algorithm, expiry status, and known claim labels. Use when debugging auth tokens, checking if a JWT is expired, inspecting JWT claims, decoding Bearer tokens, or analyzing token structure.

## Installation

```bash
clawhub install jwt-toolkit
```

## Usage

```bash
# Decode a JWT token
python3 scripts/jwt_decode.py eyJhbGciOiJIUzI1NiIs...
# Read token from file
python3 scripts/jwt_decode.py --file token.txt
```

## Requirements

- Python 3 (no external dependencies)

## License

MIT
