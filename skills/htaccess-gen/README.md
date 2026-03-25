# .htaccess Generator

Generate .htaccess files for Apache web servers. Use when creating redirect rules, URL rewrites, security headers, HTTPS enforcement, IP blocking, caching rules, custom error pages, or hotlink protection. Covers common Apache configurations including mod_rewrite, mod_headers, mod_deflate, and mod_expires. Also use when converting nginx config concepts to Apache .htaccess format.

## Installation

```bash
clawhub install htaccess-gen
```

## Usage

```bash
# Generate HTTPS redirect + security headers + caching
python3 scripts/htaccess_gen.py generate --https --security-headers --caching
# Generate redirect rules
python3 scripts/htaccess_gen.py redirect --from /old-page --to /new-page --type 301
```

## Requirements

- Python 3.7+

## License

MIT
