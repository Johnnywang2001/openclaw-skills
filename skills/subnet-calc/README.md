# Subnet Calc

CIDR and subnet calculator for network engineers. Calculate network address, broadcast, host range, subnet mask, wildcard mask, and more from CIDR notation. Supports IPv4 and IPv6, containment checks, and subnet splitting. Use when working with IP addresses, subnets, network planning, CIDR calculations, or checking if an IP is within a range.

## Installation

```bash
clawhub install subnet-calc
```

## Usage

```bash
# Basic subnet calculation
python3 scripts/subnet_calc.py 192.168.1.0/24
# JSON output
python3 scripts/subnet_calc.py 10.0.0.0/8 -f json
```

## Requirements

- Python 3.7+

## License

MIT
