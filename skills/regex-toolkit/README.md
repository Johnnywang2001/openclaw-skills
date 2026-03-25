# Regex Toolkit

Test, match, extract, replace, explain, and validate regular expressions from the command line. Includes a library of 25+ common patterns (email, URL, IP, phone, date, UUID, etc.) that can be used by name. Use when the user needs to build, debug, or test regex patterns, extract data with regex, do search-and-replace with backreferences, or understand what a regex does. Zero external dependencies.

## Installation

```bash
clawhub install regex-toolkit
```

## Usage

```bash
# Test a pattern
python3 scripts/regex_toolkit.py test '\d+' --text 'abc 123 def'
# Use a named pattern (email, url, ipv4, phone-us, uuid, etc.)
python3 scripts/regex_toolkit.py findall email --text 'Contact hello@example.com or support@test.org'
```

## Requirements

- Python 3 (no external dependencies)

## License

MIT
