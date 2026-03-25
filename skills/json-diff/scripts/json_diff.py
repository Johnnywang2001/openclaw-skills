#!/usr/bin/env python3
"""Compare two JSON files and show structured differences.

Supports tree, flat, and JSON Patch (RFC 6902) output formats.
No external dependencies — uses only the Python standard library.
"""

import argparse
import json
import sys

# ANSI color codes
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
RESET = "\033[0m"
BOLD = "\033[1m"


def colorize(text, color, use_color=True):
    if not use_color:
        return text
    return f"{color}{text}{RESET}"


def deep_diff(old, new, path="", ignore_keys=None):
    """Recursively compare two objects, yielding (type, path, old_val, new_val)."""
    ignore_keys = ignore_keys or set()

    if isinstance(old, dict) and isinstance(new, dict):
        all_keys = set(old.keys()) | set(new.keys())
        for key in sorted(all_keys):
            if key in ignore_keys:
                continue
            child_path = f"{path}.{key}" if path else key
            if key not in old:
                yield ("added", child_path, None, new[key])
            elif key not in new:
                yield ("removed", child_path, old[key], None)
            else:
                yield from deep_diff(old[key], new[key], child_path, ignore_keys)
    elif isinstance(old, list) and isinstance(new, list):
        max_len = max(len(old), len(new))
        for i in range(max_len):
            child_path = f"{path}[{i}]"
            if i >= len(old):
                yield ("added", child_path, None, new[i])
            elif i >= len(new):
                yield ("removed", child_path, old[i], None)
            else:
                yield from deep_diff(old[i], new[i], child_path, ignore_keys)
    else:
        if old != new:
            yield ("changed", path, old, new)


def format_value(val):
    """Format a value for display."""
    if val is None:
        return "null"
    if isinstance(val, str):
        return json.dumps(val)
    if isinstance(val, (dict, list)):
        s = json.dumps(val, indent=2)
        if len(s) > 80:
            return json.dumps(val)[:77] + "..."
        return s
    return str(val)


def format_tree(diffs, use_color=True):
    """Format diffs as an indented tree."""
    lines = []
    for dtype, path, old_val, new_val in diffs:
        if dtype == "added":
            marker = colorize("+ ", GREEN, use_color)
            val_str = colorize(format_value(new_val), GREEN, use_color)
            lines.append(f"  {marker}{colorize(path, CYAN, use_color)}: {val_str}")
        elif dtype == "removed":
            marker = colorize("- ", RED, use_color)
            val_str = colorize(format_value(old_val), RED, use_color)
            lines.append(f"  {marker}{colorize(path, CYAN, use_color)}: {val_str}")
        elif dtype == "changed":
            marker = colorize("~ ", YELLOW, use_color)
            old_str = colorize(format_value(old_val), RED, use_color)
            new_str = colorize(format_value(new_val), GREEN, use_color)
            lines.append(f"  {marker}{colorize(path, CYAN, use_color)}: {old_str} → {new_str}")
    return "\n".join(lines)


def format_flat(diffs, use_color=True):
    """Format diffs as flat key paths."""
    lines = []
    for dtype, path, old_val, new_val in diffs:
        tag = colorize(f"[{dtype.upper():>7s}]", {
            "added": GREEN, "removed": RED, "changed": YELLOW
        }[dtype], use_color)
        if dtype == "added":
            lines.append(f"{tag} {path} = {format_value(new_val)}")
        elif dtype == "removed":
            lines.append(f"{tag} {path} = {format_value(old_val)}")
        else:
            lines.append(f"{tag} {path}: {format_value(old_val)} → {format_value(new_val)}")
    return "\n".join(lines)


def format_patch(diffs):
    """Format diffs as JSON Patch (RFC 6902)."""
    ops = []
    for dtype, path, old_val, new_val in diffs:
        json_path = "/" + path.replace(".", "/").replace("[", "/").replace("]", "")
        if dtype == "added":
            ops.append({"op": "add", "path": json_path, "value": new_val})
        elif dtype == "removed":
            ops.append({"op": "remove", "path": json_path})
        elif dtype == "changed":
            ops.append({"op": "replace", "path": json_path, "value": new_val})
    return json.dumps(ops, indent=2)


def format_summary(diffs, use_color=True):
    """Format a summary of changes."""
    counts = {"added": 0, "removed": 0, "changed": 0}
    for dtype, *_ in diffs:
        counts[dtype] += 1
    total = sum(counts.values())
    added = counts["added"]
    removed = counts["removed"]
    changed = counts["changed"]
    lines = [
        f"  {colorize(f'+{added}', GREEN, use_color)} added",
        f"  {colorize(f'-{removed}', RED, use_color)} removed",
        f"  {colorize(f'~{changed}', YELLOW, use_color)} changed",
        f"  {colorize(str(total), BOLD, use_color)} total differences",
    ]
    return "\n".join(lines)


def load_json(path_or_stdin):
    """Load JSON from a file path or stdin (-)."""
    if path_or_stdin == "-":
        return json.load(sys.stdin)
    with open(path_or_stdin) as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="Compare two JSON files and show differences."
    )
    parser.add_argument("old", help="First JSON file (or - for stdin)")
    parser.add_argument("new", help="Second JSON file")
    parser.add_argument(
        "--format", "-f",
        choices=["tree", "flat", "patch"],
        default="tree",
        help="Output format (default: tree)",
    )
    parser.add_argument(
        "--ignore-keys", "-i",
        nargs="+",
        default=[],
        help="Keys to ignore during comparison",
    )
    parser.add_argument(
        "--only",
        nargs="+",
        choices=["added", "removed", "changed"],
        help="Show only specific change types",
    )
    parser.add_argument(
        "--summary", "-s",
        action="store_true",
        help="Show change count summary only",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output",
    )
    parser.add_argument(
        "--exit-code", "-e",
        action="store_true",
        help="Exit 1 if differences found (for CI)",
    )
    args = parser.parse_args()

    try:
        old_data = load_json(args.old)
        new_data = load_json(args.new)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON — {e}", file=sys.stderr)
        sys.exit(2)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)

    ignore = set(args.ignore_keys)
    diffs = list(deep_diff(old_data, new_data, ignore_keys=ignore))

    if args.only:
        diffs = [d for d in diffs if d[0] in args.only]

    use_color = not args.no_color and sys.stdout.isatty()

    if not diffs:
        print("No differences found.")
        sys.exit(0)

    if args.summary:
        print(format_summary(diffs, use_color))
    elif args.format == "tree":
        print(format_tree(diffs, use_color))
    elif args.format == "flat":
        print(format_flat(diffs, use_color))
    elif args.format == "patch":
        print(format_patch(diffs))

    if args.exit_code and diffs:
        sys.exit(1)


if __name__ == "__main__":
    main()
