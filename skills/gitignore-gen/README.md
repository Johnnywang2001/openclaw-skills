# Gitignore Gen

Generate .gitignore files for any project type using GitHub's 200+ official templates. Use when creating new projects, setting up repositories, needing to combine multiple gitignore templates (e.g., Python + Node + JetBrains), auto-detecting project types, or adding custom ignore rules. Supports listing, filtering, combining templates, auto-detection, appending to existing files, and custom patterns.

## Installation

```bash
clawhub install gitignore-gen
```

## Usage

```bash
# List all available templates
python3 scripts/gitignore_gen.py list
# Generate for a Python project
python3 scripts/gitignore_gen.py generate Python --force
```

## Requirements

- Python 3.7+
- Docker

## License

MIT
