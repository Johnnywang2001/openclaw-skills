#!/usr/bin/env python3
"""
yaml_toolkit.py - Full-featured YAML toolkit for OpenClaw agents.

Commands:
  validate  - Check YAML syntax
  format    - Pretty-print YAML
  to-json   - Convert YAML to JSON
  from-json - Convert JSON to YAML
  get       - Query a value by dot-path
  set       - Set a value at dot-path
  merge     - Deep-merge multiple YAML files
  lint      - Validate keys against a schema
  keys      - List all keys as dot-paths
  minify    - Output compact YAML
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("[ERROR] PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


def load_yaml_file(path):
    """Load a YAML file, returning parsed content."""
    p = Path(path)
    if not p.exists():
        print(f"[ERROR] File not found: {path}", file=sys.stderr)
        sys.exit(2)
    try:
        content = p.read_text(encoding="utf-8")
        return yaml.safe_load(content) or {}
    except yaml.YAMLError as e:
        print(f"[ERROR] YAML parse error in {path}: {e}", file=sys.stderr)
        sys.exit(2)


def load_yaml_text(text):
    """Load YAML from a string."""
    try:
        return yaml.safe_load(text) or {}
    except yaml.YAMLError as e:
        print(f"[ERROR] YAML parse error: {e}", file=sys.stderr)
        sys.exit(2)


def dump_yaml(obj, indent=2, allow_unicode=True):
    """Dump an object to YAML string."""
    return yaml.dump(obj, default_flow_style=False, allow_unicode=allow_unicode,
                     indent=indent, sort_keys=False)


def get_by_path(obj, path):
    """Get a value from a nested dict by dot-path like 'server.host'."""
    keys = path.split(".")
    current = obj
    for key in keys:
        if not isinstance(current, dict):
            return None, False
        # Support array index like 'items[0]'
        if "[" in key:
            base, idx = key.rstrip("]").split("[")
            try:
                current = current[base][int(idx)]
            except (KeyError, IndexError, TypeError):
                return None, False
        else:
            if key not in current:
                return None, False
            current = current[key]
    return current, True


def set_by_path(obj, path, value):
    """Set a value in a nested dict by dot-path, creating intermediate dicts."""
    keys = path.split(".")
    current = obj
    for key in keys[:-1]:
        if key not in current or not isinstance(current[key], dict):
            current[key] = {}
        current = current[key]
    # Try to coerce value to appropriate type
    final_key = keys[-1]
    if isinstance(value, str):
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                if value.lower() in ("true", "yes"):
                    value = True
                elif value.lower() in ("false", "no"):
                    value = False
    current[final_key] = value
    return obj


def deep_merge(base, override):
    """Deep-merge two dicts. override takes precedence."""
    if not isinstance(base, dict) or not isinstance(override, dict):
        return override
    result = dict(base)
    for key, val in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(val, dict):
            result[key] = deep_merge(result[key], val)
        else:
            result[key] = val
    return result


def flatten_keys(obj, prefix=""):
    """Flatten all keys as dot-paths."""
    keys = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            full_key = f"{prefix}.{k}" if prefix else str(k)
            if isinstance(v, (dict, list)):
                keys.extend(flatten_keys(v, full_key))
            else:
                keys.append(full_key)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            full_key = f"{prefix}[{i}]"
            if isinstance(v, (dict, list)):
                keys.extend(flatten_keys(v, full_key))
            else:
                keys.append(full_key)
    return keys


def write_output(content, output_path=None):
    """Write content to stdout or a file."""
    if output_path:
        Path(output_path).write_text(content, encoding="utf-8")
        print(f"[OK] Written to {output_path}")
    else:
        print(content, end="")


def cmd_validate(args):
    """Validate YAML syntax."""
    p = Path(args.file)
    if not p.exists():
        print(f"[ERROR] File not found: {args.file}", file=sys.stderr)
        sys.exit(2)
    try:
        content = p.read_text(encoding="utf-8")
        # Load all documents
        docs = list(yaml.safe_load_all(content))
        doc_count = len([d for d in docs if d is not None])
        print(f"[OK] Valid YAML — {doc_count} document(s) in {args.file}")
        sys.exit(0)
    except yaml.YAMLError as e:
        print(f"[FAIL] Invalid YAML in {args.file}:")
        if hasattr(e, "problem_mark"):
            mark = e.problem_mark
            print(f"  Line {mark.line + 1}, column {mark.column + 1}: {e.problem}")
        else:
            print(f"  {e}")
        sys.exit(1)


def cmd_format(args):
    """Format/pretty-print YAML."""
    obj = load_yaml_file(args.file)
    indent = getattr(args, "indent", 2)
    output = dump_yaml(obj, indent=indent)
    write_output(output, getattr(args, "output", None))


def cmd_to_json(args):
    """Convert YAML to JSON."""
    obj = load_yaml_file(args.file)
    output = json.dumps(obj, indent=2, default=str, ensure_ascii=False) + "\n"
    write_output(output, getattr(args, "output", None))


def cmd_from_json(args):
    """Convert JSON to YAML."""
    p = Path(args.file)
    if not p.exists():
        print(f"[ERROR] File not found: {args.file}", file=sys.stderr)
        sys.exit(2)
    try:
        obj = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON parse error: {e}", file=sys.stderr)
        sys.exit(2)
    indent = getattr(args, "indent", 2)
    output = dump_yaml(obj, indent=indent)
    write_output(output, getattr(args, "output", None))


def cmd_get(args):
    """Get a value by dot-path."""
    obj = load_yaml_file(args.file)
    value, found = get_by_path(obj, args.path)
    if not found:
        print(f"[ERROR] Key not found: {args.path}", file=sys.stderr)
        sys.exit(1)
    if isinstance(value, (dict, list)):
        print(dump_yaml(value), end="")
    else:
        print(value)


def cmd_set(args):
    """Set a value by dot-path."""
    obj = load_yaml_file(args.file)
    updated = set_by_path(obj, args.path, args.value)
    indent = getattr(args, "indent", 2)
    output = dump_yaml(updated, indent=indent)
    write_output(output, getattr(args, "output", None))


def cmd_merge(args):
    """Deep-merge multiple YAML files."""
    if len(args.files) < 2:
        print("[ERROR] Merge requires at least 2 files.", file=sys.stderr)
        sys.exit(2)
    result = load_yaml_file(args.files[0])
    for f in args.files[1:]:
        override = load_yaml_file(f)
        result = deep_merge(result, override)
    indent = getattr(args, "indent", 2)
    output = dump_yaml(result, indent=indent)
    write_output(output, getattr(args, "output", None))


def cmd_lint(args):
    """Lint YAML files for common issues: duplicate keys, tabs, syntax errors, trailing whitespace.

    If --schema is provided, validates keys against the schema YAML instead.
    Supports directories (recursive scan of .yaml/.yml files) and --strict mode.
    """
    # Schema-based lint (backwards-compatible)
    if getattr(args, "schema", None):
        obj = load_yaml_file(args.file)
        schema = load_yaml_file(args.schema)

        errors = []

        def check_schema(data, schema_node, path=""):
            if not isinstance(schema_node, dict):
                return
            required = schema_node.get("_required", [])
            allowed = schema_node.get("_allowed", None)
            for req_key in required:
                full = f"{path}.{req_key}" if path else req_key
                if req_key not in (data if isinstance(data, dict) else {}):
                    errors.append(f"Missing required key: {full}")
            if allowed is not None and isinstance(data, dict):
                for k in data:
                    if k not in allowed and not k.startswith("_"):
                        full = f"{path}.{k}" if path else k
                        errors.append(f"Unexpected key: {full}")
            if isinstance(schema_node, dict) and isinstance(data, dict):
                for k, v in schema_node.items():
                    if k.startswith("_"):
                        continue
                    if k in data and isinstance(v, dict):
                        check_schema(data[k], v, f"{path}.{k}" if path else k)

        check_schema(obj, schema)

        if errors:
            print(f"[FAIL] Lint errors in {args.file}:")
            for e in errors:
                print(f"  - {e}")
            sys.exit(1)
        else:
            print(f"[OK] {args.file} passes lint check.")
        return

    # File-level lint: duplicate keys, tabs, syntax errors, strict checks
    import os

    strict = getattr(args, "strict", False)
    output_json = getattr(args, "json", False)
    quiet = getattr(args, "quiet", False)
    target = args.file

    # Collect files to lint
    files_to_lint = []
    if os.path.isdir(target):
        for root, dirs, files in os.walk(target):
            for fn in sorted(files):
                if fn.endswith((".yaml", ".yml")):
                    files_to_lint.append(os.path.join(root, fn))
    else:
        files_to_lint.append(target)

    all_results = []
    any_invalid = False

    for file_path in files_to_lint:
        result = {"file": file_path, "valid": True, "issues": []}

        if not os.path.isfile(file_path):
            result["valid"] = False
            result["issues"].append({"level": "error", "message": f"File not found: {file_path}"})
            all_results.append(result)
            any_invalid = True
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            result["valid"] = False
            result["issues"].append({"level": "error", "message": f"Cannot read file: {e}"})
            all_results.append(result)
            any_invalid = True
            continue

        if not content.strip():
            result["issues"].append({"level": "warning", "message": "File is empty"})
            all_results.append(result)
            continue

        # Check for tabs
        for i, line in enumerate(content.splitlines(), 1):
            if "\t" in line:
                result["issues"].append({
                    "level": "warning",
                    "message": f"Line {i}: Tab character found (YAML should use spaces)"
                })

        # Strict checks
        if strict:
            for i, line in enumerate(content.splitlines(), 1):
                if line != line.rstrip():
                    result["issues"].append({
                        "level": "info",
                        "message": f"Line {i}: Trailing whitespace"
                    })
                if len(line) > 256:
                    result["issues"].append({
                        "level": "warning",
                        "message": f"Line {i}: Very long line ({len(line)} chars)"
                    })

        # Parse YAML for syntax errors
        try:
            docs = list(yaml.safe_load_all(content))
            doc_count = len([d for d in docs if d is not None])
            if doc_count > 1:
                result["issues"].append({
                    "level": "info",
                    "message": f"Multi-document YAML: {doc_count} documents"
                })
        except yaml.YAMLError as e:
            result["valid"] = False
            msg = str(e)
            if hasattr(e, "problem_mark"):
                mark = e.problem_mark
                msg = f"Line {mark.line + 1}, Column {mark.column + 1}: {e.problem}"
            result["issues"].append({"level": "error", "message": msg})
            all_results.append(result)
            any_invalid = True
            continue

        # Check for duplicate keys
        class DuplicateKeyLoader(yaml.SafeLoader):
            pass

        dupes = []

        def check_duplicates(loader, node):
            mapping = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node)
                if key in mapping:
                    dupes.append(f"Duplicate key '{key}' at line {key_node.start_mark.line + 1}")
                mapping[key] = loader.construct_object(value_node)
            return mapping

        DuplicateKeyLoader.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, check_duplicates
        )

        try:
            yaml.load(content, Loader=DuplicateKeyLoader)
        except Exception:
            pass

        for d in dupes:
            result["valid"] = False
            result["issues"].append({"level": "error", "message": d})
            any_invalid = True

        if not result["valid"]:
            any_invalid = True
        all_results.append(result)

    # Output
    if output_json:
        print(json.dumps(all_results, indent=2))
    else:
        for result in all_results:
            status = "✓" if result["valid"] else "✗"
            print(f"{status} {result['file']}")
            for issue in result["issues"]:
                if quiet and issue["level"] != "error":
                    continue
                prefix = {"error": "  ERROR", "warning": "  WARN ", "info": "  INFO "}.get(issue["level"], "  ")
                print(f"{prefix}: {issue['message']}")

    sys.exit(1 if any_invalid else 0)


def cmd_keys(args):
    """List all keys as dot-paths."""
    obj = load_yaml_file(args.file)
    keys = flatten_keys(obj)
    if not keys:
        print("(empty document)")
    else:
        for k in keys:
            print(k)


def cmd_minify(args):
    """Output compact YAML."""
    obj = load_yaml_file(args.file)
    output = yaml.dump(obj, default_flow_style=True, allow_unicode=True) + "\n"
    write_output(output, getattr(args, "output", None))


def main():
    parser = argparse.ArgumentParser(
        description="Full-featured YAML toolkit — validate, format, convert, query, merge.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  validate config.yaml
  format config.yaml
  to-json config.yaml
  from-json data.json
  get config.yaml server.host
  set config.yaml server.port 8080
  merge base.yaml override.yaml
  lint config.yaml --schema schema.yaml
  keys config.yaml
  minify config.yaml
        """
    )
    parser.add_argument("--output", "-o", help="Write output to file instead of stdout")
    parser.add_argument("--indent", type=int, default=2, help="YAML indentation spaces (default: 2)")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # validate
    p_val = subparsers.add_parser("validate", help="Check YAML syntax")
    p_val.add_argument("file", help="YAML file to validate")

    # format
    p_fmt = subparsers.add_parser("format", help="Pretty-print YAML")
    p_fmt.add_argument("file", help="YAML file to format")

    # to-json
    p_toj = subparsers.add_parser("to-json", help="Convert YAML to JSON")
    p_toj.add_argument("file", help="YAML file to convert")

    # from-json
    p_fj = subparsers.add_parser("from-json", help="Convert JSON to YAML")
    p_fj.add_argument("file", help="JSON file to convert")

    # get
    p_get = subparsers.add_parser("get", help="Get value at dot-path")
    p_get.add_argument("file", help="YAML file")
    p_get.add_argument("path", help="Dot-path (e.g. server.host)")

    # set
    p_set = subparsers.add_parser("set", help="Set value at dot-path")
    p_set.add_argument("file", help="YAML file")
    p_set.add_argument("path", help="Dot-path (e.g. server.port)")
    p_set.add_argument("value", help="New value to set")

    # merge
    p_mrg = subparsers.add_parser("merge", help="Deep-merge YAML files")
    p_mrg.add_argument("files", nargs="+", help="YAML files to merge (left to right)")

    # lint
    p_lnt = subparsers.add_parser("lint", help="Lint YAML files for issues (or validate against schema)")
    p_lnt.add_argument("file", help="YAML file or directory to lint")
    p_lnt.add_argument("--schema", default=None, help="Schema YAML file (if provided, validates keys against schema)")
    p_lnt.add_argument("--strict", action="store_true", help="Strict mode: check trailing whitespace, long lines")
    p_lnt.add_argument("--json", action="store_true", help="Output results as JSON")
    p_lnt.add_argument("--quiet", action="store_true", help="Only show errors, suppress info/warnings")

    # keys
    p_keys = subparsers.add_parser("keys", help="List all keys as dot-paths")
    p_keys.add_argument("file", help="YAML file")

    # minify
    p_min = subparsers.add_parser("minify", help="Compact YAML output")
    p_min.add_argument("file", help="YAML file to minify")

    args = parser.parse_args()

    commands = {
        "validate": cmd_validate,
        "format": cmd_format,
        "to-json": cmd_to_json,
        "from-json": cmd_from_json,
        "get": cmd_get,
        "set": cmd_set,
        "merge": cmd_merge,
        "lint": cmd_lint,
        "keys": cmd_keys,
        "minify": cmd_minify,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
