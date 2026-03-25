# IP Geolocation Toolkit

Look up IP geolocation, find your public IP, perform reverse DNS, and run bulk IP lookups. Uses free APIs (ip-api.com, ipify) with no API key required. No external dependencies — pure Python. Use when looking up IP address location, finding your public IP, checking ISP/ASN info, doing reverse DNS, or processing lists of IPs for geolocation data.

## Installation

```bash
clawhub install ip-geo-toolkit
```

## Usage

```bash
python3 scripts/ip_geo.py lookup 8.8.8.8
python3 scripts/ip_geo.py lookup 8.8.8.8 1.1.1.1 9.9.9.9
python3 scripts/ip_geo.py lookup 8.8.8.8 --json
```

```bash
python3 scripts/ip_geo.py myip
python3 scripts/ip_geo.py myip --json
```

```bash
python3 scripts/ip_geo.py bulk --input ips.txt
python3 scripts/ip_geo.py bulk --input ips.txt --json --output results.json
cat ips.txt | python3 scripts/ip_geo.py bulk --input -
```

## Requirements

- Python 3 (no external dependencies)

## License

MIT
