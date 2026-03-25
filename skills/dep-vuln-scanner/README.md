# Dependency Vulnerability Scanner

Scan project dependencies for known security vulnerabilities using the OSV.dev API. Supports npm (package.json), Python/pip (requirements.txt), and Go (go.mod). Use when checking a project for vulnerable packages, auditing dependencies before deployment, or investigating CVEs in third-party libraries. No API key required.

## Installation

```bash
clawhub install dep-vuln-scanner
```

## Usage

```bash
# Scan current directory (auto-detects project type)
python3 scripts/dep_vuln_scan.py .
# Scan a specific project
python3 scripts/dep_vuln_scan.py /path/to/project
```

## Requirements

- Python 3.7+

## License

MIT
