# Git Hooks Toolkit

Generate, install, and manage Git hooks with pre-built templates. Includes hooks for linting staged files, enforcing conventional commits, blocking debug statements, preventing large file commits, auto-formatting code, requiring ticket references, protecting branches, running tests before push, and auto-installing dependencies after merge. Use when setting up git hooks, enforcing commit conventions, or automating pre-commit/pre-push checks.

## Installation

```bash
clawhub install git-hooks-toolkit
```

## Usage

```bash
# List all available templates
python3 scripts/git_hooks.py list
# Install a hook
python3 scripts/git_hooks.py install pre-commit lint-staged
```

## Requirements

- Python 3.7+

## License

MIT
