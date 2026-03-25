# SQL Formatter

Format, minify, and lint SQL queries from the command line. Formats SQL with proper indentation and keyword casing, minifies by removing whitespace and comments, and lints for common anti-patterns (SELECT *, inconsistent casing, missing semicolons, trailing whitespace). No external dependencies — pure Python. Use when formatting SQL queries, cleaning up SQL files, minifying SQL for production, or checking SQL quality.

## Installation

```bash
clawhub install sql-formatter
```

## Usage

```bash
python3 scripts/sql_format.py format --sql "SELECT id, name FROM users WHERE active = true"
python3 scripts/sql_format.py format --input query.sql
python3 scripts/sql_format.py format --input query.sql --output formatted.sql
python3 scripts/sql_format.py format --input query.sql --indent 4 --lowercase
```

```bash
python3 scripts/sql_format.py minify --sql "SELECT  id,  name  FROM  users  -- comment"
python3 scripts/sql_format.py minify --input query.sql
```

```bash
python3 scripts/sql_format.py lint --input query.sql
python3 scripts/sql_format.py lint --sql "SELECT * FROM users WHERE 1=1" --json
```

## Requirements

- Python 3 (no external dependencies)

## License

MIT
