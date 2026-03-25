# SSL Certificate Monitor

Check SSL/TLS certificate expiry, issuer, protocol, and SANs for one or more domains. Use when asked to check SSL certificates, monitor cert expiry, verify HTTPS is working, audit domain security, or check if a certificate is about to expire. Supports custom ports and warning thresholds. No external dependencies — uses Python stdlib ssl module.

## Installation

```bash
clawhub install jrv-ssl-monitor
```

## Usage

```bash
python3 scripts/check_ssl.py example.com
python3 scripts/check_ssl.py example.com google.com github.com --warn-days 30
python3 scripts/check_ssl.py internal.host --port 8443 --json
```

## Requirements

- Python 3 (no external dependencies)

## License

MIT
