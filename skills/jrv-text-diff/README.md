# Text Diff

Compare two text files or strings side-by-side or unified. Highlights additions, deletions, and changes with color. Supports word-level diff, ignore-whitespace, and JSON/YAML structural diff modes.

## Installation

```bash
clawhub install jrv-text-diff
```

## Usage

```bash
# Compare two files
python3 scripts/text_diff.py file1.txt file2.txt
# Compare inline strings
python3 scripts/text_diff.py --text "hello world" --text2 "hello there"
```

## Requirements

- Python 3.7+

## License

MIT
