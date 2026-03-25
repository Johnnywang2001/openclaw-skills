# Whois Toolkit

Domain WHOIS lookup toolkit for querying registrar, creation/expiry dates, nameservers, status, and registrant info. Use when looking up domain ownership, checking domain expiry dates, monitoring domain renewals, or investigating domain registration details. Supports all major TLDs. No external dependencies or API keys required.

## Installation

```bash
clawhub install whois-toolkit
```

## Usage

```bash
# Basic WHOIS lookup
python3 scripts/whois_lookup.py example.com
# Multiple domains at once
python3 scripts/whois_lookup.py example.com example.org example.io
```

## Requirements

- Python 3 (no external dependencies)

## License

MIT
