# Port Scanner

Fast TCP port scanner for network reconnaissance and security auditing. Scan hosts for open ports, detect common services, and identify potential attack surface. Use when checking what ports are open on a server, scanning a network range, auditing firewall rules, or performing pre-deployment security checks.

## Installation

```bash
clawhub install port-scanner
```

## Usage

```bash
# Scan common ports on a host
python3 scripts/port_scan.py example.com
# Scan specific port range
python3 scripts/port_scan.py 192.168.1.1 --ports 1-1024
```

## Requirements

- Python 3 (no external dependencies)

## License

MIT
