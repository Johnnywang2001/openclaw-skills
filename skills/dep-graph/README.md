# Dependency Graph

Analyze and visualize project dependency trees from manifest files. Supports Node.js (package.json), Python (requirements.txt, pyproject.toml), Go (go.mod), Rust (Cargo.toml), Ruby (Gemfile), and PHP (composer.json). Use when asked to list dependencies, show a dependency tree, check what packages a project uses, compare prod vs dev deps, or audit dependency counts.

## Installation

```bash
clawhub install dep-graph
```

## Usage

```bash
# Analyze current project
python3 scripts/dep_graph.py
# Analyze specific directory
python3 scripts/dep_graph.py /path/to/project
```

## Requirements

- Python 3.7+

## License

MIT
