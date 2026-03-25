#!/usr/bin/env python3
"""TOML toolkit — validate, query, convert, and merge TOML files.

Uses Python 3.11+ built-in tomllib for reading. For writing, uses a bundled
minimal TOML serializer (no external dependencies needed).
"""

import argparse
import json
import sys
from pathlib import Path

# Python 3.11+ has tomllib; older versions need tomli
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib  # type: ignore
    except ImportError:
        print("Error: Python 3.11+ required (has built-in tomllib), or install tomli: pip install tomli", file=sys.stderr)
        sys.exit(1)


def toml_dumps(obj, prefix=""):
    """Minimal TOML serializer for dicts (handles nested tables, arrays, basic types)."""
    lines = []
    tables = []

    for key, val in obj.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(val, dict):
            tables.append((full_key, val))
        elif isinstance(val, list) and val and isinstance(val[0], dict):
            # Array of tables
            for item in val:
                lines.append(f"\n[[{full_key}]]")
                lines.append(toml_dumps(item, ""))
        else:
            lines.append(f"{key} = {_toml_value(val)}")

    for full_key, val in tables:
        lines.append(f"\n[{full_key}]")
        lines.append(toml_dumps(val, full_key))

    return "\n".join(lines)


def _toml_value(val):
    """Serialize a single TOML value."""
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, int):
        return str(val)
    if isinstance(val, float):
        return str(val)
    if isinstance(val, str):
        escaped = val.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        return f'"{escaped}"'
    if isinstance(val, list):
        items = ", ".join(_toml_value(v) for v in val)
        return f"[{items}]"
    if isinstance(val, dict):
        items = ", ".join(f"{k} = {_toml_value(v)}" for k, v in val.items())
        return f"{{{items}}}"
    return str(val)


def read_toml(path: str) -> dict:
    """Read and parse a TOML file."""
    p = Path(path)
    if not p.exists():
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)
    try:
        with open(p, "rb") as f:
            return tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        print(f"Error: invalid TOML: {e}", file=sys.stderr)
        sys.exit(1)


def resolve_key(data: dict, key: str):
    """Resolve a dotted key path into nested dicts."""
    parts = key.split(".")
    current = data
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current


def cmd_validate(args):
    """Validate a TOML file."""
    p = Path(args.file)
    if not p.exists():
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    try:
        with open(p, "rb") as f:
            data = tomllib.load(f)
        keys = _count_keys(data)
        tables = _count_tables(data)
        print(f"✓ Valid TOML: {args.file}")
        print(f"  Top-level keys: {len(data)}")
        print(f"  Total keys: {keys}")
        print(f"  Nested tables: {tables}")
    except tomllib.TOMLDecodeError as e:
        print(f"✗ Invalid TOML: {args.file}")
        print(f"  Error: {e}")
        sys.exit(1)


def _count_keys(d, n=0):
    for v in d.values():
        n += 1
        if isinstance(v, dict):
            n = _count_keys(v, n)
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    n = _count_keys(item, n)
    return n


def _count_tables(d, n=0):
    for v in d.values():
        if isinstance(v, dict):
            n += 1
            n = _count_tables(v, n)
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    n += 1
                    n = _count_tables(item, n)
    return n


def cmd_query(args):
    """Query a specific key from a TOML file."""
    data = read_toml(args.file)
    result = resolve_key(data, args.key)
    if result is None:
        print(f"Key not found: {args.key}", file=sys.stderr)
        sys.exit(1)
    if isinstance(result, (dict, list)):
        print(json.dumps(result, indent=2))
    else:
        print(result)


def cmd_to_json(args):
    """Convert TOML to JSON."""
    data = read_toml(args.file)
    indent = None if args.compact else 2
    output = json.dumps(data, indent=indent, default=str)
    if args.output:
        Path(args.output).write_text(output + "\n")
        print(f"Written to {args.output}")
    else:
        print(output)


def cmd_to_toml(args):
    """Convert JSON to TOML."""
    p = Path(args.file)
    if not p.exists():
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    try:
        data = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    output = toml_dumps(data)
    if args.output:
        Path(args.output).write_text(output + "\n")
        print(f"Written to {args.output}")
    else:
        print(output)


def cmd_keys(args):
    """List all keys in a TOML file."""
    data = read_toml(args.file)
    keys = _collect_keys(data)
    for k in keys:
        print(k)
    print(f"\n{len(keys)} key(s) total")


def _collect_keys(d, prefix=""):
    keys = []
    for k, v in d.items():
        full = f"{prefix}.{k}" if prefix else k
        keys.append(full)
        if isinstance(v, dict):
            keys.extend(_collect_keys(v, full))
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    keys.extend(_collect_keys(item, f"{full}[{i}]"))
    return keys


def cmd_merge(args):
    """Merge multiple TOML files (later files override earlier)."""
    merged = {}
    for f in args.files:
        data = read_toml(f)
        _deep_merge(merged, data)

    output = toml_dumps(merged)
    if args.output:
        Path(args.output).write_text(output + "\n")
        print(f"Merged {len(args.files)} files → {args.output}")
    else:
        print(output)


def _deep_merge(base, override):
    for k, v in override.items():
        if k in base and isinstance(base[k], dict) and isinstance(v, dict):
            _deep_merge(base[k], v)
        else:
            base[k] = v


def main():
    parser = argparse.ArgumentParser(description="TOML toolkit — validate, query, convert, and merge TOML files")
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # validate
    p_val = sub.add_parser("validate", help="Validate a TOML file")
    p_val.add_argument("file", help="TOML file to validate")
    p_val.set_defaults(func=cmd_validate)

    # query
    p_q = sub.add_parser("query", help="Query a key from a TOML file")
    p_q.add_argument("file", help="TOML file")
    p_q.add_argument("key", help="Dotted key path (e.g., tool.poetry.name)")
    p_q.set_defaults(func=cmd_query)

    # to-json
    p_json = sub.add_parser("to-json", help="Convert TOML to JSON")
    p_json.add_argument("file", help="TOML file to convert")
    p_json.add_argument("-o", "--output", help="Output file (default: stdout)")
    p_json.add_argument("--compact", action="store_true", help="Compact JSON output")
    p_json.set_defaults(func=cmd_to_json)

    # to-toml
    p_toml = sub.add_parser("to-toml", help="Convert JSON to TOML")
    p_toml.add_argument("file", help="JSON file to convert")
    p_toml.add_argument("-o", "--output", help="Output file (default: stdout)")
    p_toml.set_defaults(func=cmd_to_toml)

    # keys
    p_keys = sub.add_parser("keys", help="List all keys in a TOML file")
    p_keys.add_argument("file", help="TOML file")
    p_keys.set_defaults(func=cmd_keys)

    # merge
    p_merge = sub.add_parser("merge", help="Merge multiple TOML files")
    p_merge.add_argument("files", nargs="+", help="TOML files to merge (later overrides earlier)")
    p_merge.add_argument("-o", "--output", help="Output file (default: stdout)")
    p_merge.set_defaults(func=cmd_merge)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)
    args.func(args)


if __name__ == "__main__":
    main()
