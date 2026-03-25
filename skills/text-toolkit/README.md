# Text Toolkit

Swiss-army knife for text manipulation. Case conversion (upper, lower, title, camelCase, PascalCase, snake_case, kebab-case, CONSTANT_CASE), slugify, word/character counting, text stats, reverse, truncate, word wrap, extract emails/URLs, deduplicate lines, and sort lines. Use when transforming text, converting variable naming conventions, counting words, generating URL slugs, extracting data from text, or any string manipulation task. Accepts piped stdin or inline arguments.

## Installation

```bash
clawhub install text-toolkit
```

## Usage

```bash
# Case conversion
python3 scripts/textool.py upper "hello world"
python3 scripts/textool.py slug "My Blog Post Title!"
python3 scripts/textool.py camel "user first name"
```

## Requirements

- Python 3 (no external dependencies)

## License

MIT
