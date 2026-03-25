# HTTP Security Audit

Audit HTTP security headers for any website. Use when a user asks to check security headers, harden a web server, audit HSTS/CSP/X-Frame-Options compliance, find information leaks (Server, X-Powered-By), or assess a website's security posture. Checks 10 security headers and grades A–F. Supports multiple URLs and JSON output.

## Installation

```bash
clawhub install http-sec-audit
```

## Usage

```bash
python3 scripts/sec_headers.py https://example.com
```

## Requirements

- Python 3.7+

## License

MIT
