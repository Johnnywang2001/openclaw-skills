# Subdomain Enum

Enumerate subdomains for any domain using DNS brute-force and certificate transparency logs (crt.sh). Use when a user needs to discover subdomains, perform reconnaissance, audit attack surface, find forgotten or exposed services, or map the infrastructure of a domain. No API keys required. Supports custom wordlists, concurrent threads, and JSON output.

## Installation

```bash
clawhub install subdomain-enum
```

## Usage

```bash
python3 scripts/subenum.py example.com
```

## Requirements

- Python 3.7+

## License

MIT
