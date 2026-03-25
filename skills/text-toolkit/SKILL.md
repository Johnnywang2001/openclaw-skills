---
name: text-toolkit
description: Swiss-army knife for text manipulation. Case conversion (upper, lower, title, camelCase, PascalCase, snake_case, kebab-case, CONSTANT_CASE), slugify, word/character counting, text stats, reverse, truncate, word wrap, extract emails/URLs, deduplicate lines, and sort lines. Use when transforming text, converting variable naming conventions, counting words, generating URL slugs, extracting data from text, or any string manipulation task. Accepts piped stdin or inline arguments.
---

# Text Toolkit

All-in-one text manipulation from the command line. No dependencies.

## Quick Start

```bash
# Case conversion
python3 scripts/textool.py upper "hello world"
python3 scripts/textool.py slug "My Blog Post Title!"
python3 scripts/textool.py camel "user first name"
python3 scripts/textool.py snake "getUserName"
python3 scripts/textool.py kebab "MyComponentName"
python3 scripts/textool.py constant "api base url"

# Word/char counting
python3 scripts/textool.py count "The quick brown fox jumps"
echo "some text" | python3 scripts/textool.py count --json

# Slugify for URLs
python3 scripts/textool.py slug "Héllo Wörld! Spëcial Chars"

# Extract emails and URLs
python3 scripts/textool.py extract emails "Contact us at foo@bar.com or baz@qux.io"
python3 scripts/textool.py extract urls "Visit https://example.com or https://foo.bar/page"

# Reverse
python3 scripts/textool.py reverse "hello"
python3 scripts/textool.py reverse --words "one two three"

# Truncate
python3 scripts/textool.py truncate 20 "This is a rather long sentence that needs trimming"

# Word wrap
python3 scripts/textool.py wrap --width 40 "A very long paragraph..."

# Deduplicate and sort lines (pipe-friendly)
cat file.txt | python3 scripts/textool.py dedup
cat file.txt | python3 scripts/textool.py sort -r
```

## Commands

| Command | Description |
|---------|-------------|
| `upper` | UPPERCASE |
| `lower` | lowercase |
| `title` | Smart Title Case |
| `slug` | url-friendly-slug |
| `camel` | camelCase |
| `pascal` | PascalCase |
| `snake` | snake_case |
| `kebab` | kebab-case |
| `constant` | CONSTANT_CASE |
| `count` | Character, word, line, sentence, paragraph stats |
| `reverse` | Reverse text (or `--words` for word order) |
| `truncate` | Truncate to N chars with suffix |
| `wrap` | Word wrap to width |
| `extract` | Extract `emails` or `urls` from text |
| `dedup` | Remove duplicate lines |
| `sort` | Sort lines (`-r` for reverse) |

## Input

All commands accept text as arguments or piped via stdin:
```bash
echo "hello world" | python3 scripts/textool.py upper
python3 scripts/textool.py upper "hello world"
```

## Requirements

- Python 3.7+ (no external dependencies)
