# Password Gen

Generate secure passwords, passphrases, and PINs with entropy analysis. Use when the user needs a random password, passphrase, PIN, or wants to check how strong an existing password is. Supports custom length, character sets, exclusions, batch generation, and JSON output. Zero external dependencies.

## Installation

```bash
clawhub install password-gen
```

## Usage

```bash
# Generate a 16-character password
python3 scripts/password_gen.py
# Generate a 32-character password, 5 at a time
python3 scripts/password_gen.py -l 32 -n 5
```

## Requirements

- Python 3.7+

## License

MIT
