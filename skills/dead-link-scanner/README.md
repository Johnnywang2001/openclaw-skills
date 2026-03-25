# Dead Link Scanner

Scan websites, markdown files, and HTML files for broken links (dead links). Use when checking a website for 404s, validating links in documentation or README files, auditing link health before a deploy, or finding broken internal/external links. Supports recursive crawling with depth limits, markdown file scanning, and output in text or JSON format.

## Installation

```bash
clawhub install dead-link-scanner
```

## Usage

```bash
# Scan a website for broken links
python3 scripts/dead_link_scanner.py scan https://example.com
# Scan with depth limit (default: 1)
python3 scripts/dead_link_scanner.py scan https://example.com --depth 3
```

## Requirements

- Python 3.7+

## License

MIT
