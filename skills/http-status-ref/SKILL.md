---
name: http-status-ref
description: HTTP status code reference, lookup, search, and URL header analyzer with security audit. Use when looking up HTTP status codes, checking what a status code means, searching for codes by keyword, inspecting response headers from a URL, or auditing security headers. Triggers on "HTTP status", "status code", "what does 403 mean", "response headers", "security headers", "HSTS", "CSP", "check headers".
---

# HTTP Status Reference

Complete HTTP status code database with URL header checking using `scripts/http_status.py` (Python 3, no external dependencies).

## Commands

### Look up a status code

```bash
python3 scripts/http_status.py lookup 404
python3 scripts/http_status.py lookup 301 --json
python3 scripts/http_status.py lookup 0   # List all codes
```

### Search by keyword

```bash
python3 scripts/http_status.py search redirect
python3 scripts/http_status.py search cache
python3 scripts/http_status.py search auth
```

Searches code names and descriptions.

### Check URL headers

```bash
python3 scripts/http_status.py check example.com
python3 scripts/http_status.py check https://api.github.com --security
python3 scripts/http_status.py check example.com --json
```

The `--security` flag audits 10 security headers (HSTS, CSP, X-Frame-Options, etc.) and gives a score.

## Coverage

Includes all standard HTTP status codes: 1xx informational, 2xx success, 3xx redirection, 4xx client errors, 5xx server errors, plus WebDAV and non-standard codes (418 teapot, 451 legal).
