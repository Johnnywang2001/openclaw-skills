# HTTP Status Reference

HTTP status code reference, lookup, search, and URL header analyzer with security audit. Use when looking up HTTP status codes, checking what a status code means, searching for codes by keyword, inspecting response headers from a URL, or auditing security headers.

## Installation

```bash
clawhub install http-status-ref
```

## Usage

```bash
python3 scripts/http_status.py lookup 404
python3 scripts/http_status.py lookup 301 --json
python3 scripts/http_status.py lookup 0   # List all codes
```

```bash
python3 scripts/http_status.py search redirect
python3 scripts/http_status.py search cache
python3 scripts/http_status.py search auth
```

```bash
python3 scripts/http_status.py check example.com
python3 scripts/http_status.py check https://api.github.com --security
python3 scripts/http_status.py check example.com --json
```

## Requirements

- Python 3.7+

## License

MIT
