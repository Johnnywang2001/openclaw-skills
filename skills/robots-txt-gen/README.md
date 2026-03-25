# robots.txt Generator

Generate, validate, and analyze robots.txt files for websites. Use when creating robots.txt from scratch, validating existing robots.txt syntax, checking if a URL is allowed/blocked by robots.txt rules, or generating robots.txt for common platforms (WordPress, Next.js, Django, Rails). Also use when auditing crawl directives or debugging search engine indexing issues.

## Installation

```bash
clawhub install robots-txt-gen
```

## Usage

```bash
# Generate a robots.txt for a platform
python3 scripts/robots_txt_gen.py generate --preset nextjs --sitemap https://example.com/sitemap.xml
# Validate an existing robots.txt
python3 scripts/robots_txt_gen.py validate --file robots.txt
```

## Requirements

- Python 3.7+

## License

MIT
