#!/usr/bin/env python3
"""Validate and lint YAML files. Reports syntax errors, duplicate keys, and structural issues."""

import argparse
import sys
import os
import json


def check_pyyaml():
    try:
        import yaml
        return True
    except ImportError:
        return False


def validate_yaml(file_path, strict=False, output_json=False):
    """Validate a single YAML file and return issues found."""
    import yaml

    issues = []
    result = {"file": file_path, "valid": True, "issues": []}

    if not os.path.isfile(file_path):
        result["valid"] = False
        result["issues"].append({"level": "error", "message": f"File not found: {file_path}"})
        return result

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        result["valid"] = False
        result["issues"].append({"level": "error", "message": f"Cannot read file: {e}"})
        return result

    if not content.strip():
        result["issues"].append({"level": "warning", "message": "File is empty"})
        return result

    # Check for tabs (YAML should use spaces)
    for i, line in enumerate(content.splitlines(), 1):
        if "\t" in line:
            result["issues"].append({
                "level": "warning",
                "message": f"Line {i}: Tab character found (YAML should use spaces for indentation)"
            })

    # Check for trailing whitespace
    if strict:
        for i, line in enumerate(content.splitlines(), 1):
            if line != line.rstrip():
                result["issues"].append({
                    "level": "info",
                    "message": f"Line {i}: Trailing whitespace"
                })

    # Parse YAML
    try:
        docs = list(yaml.safe_load_all(content))
        doc_count = len(docs)
        if doc_count > 1:
            result["issues"].append({
                "level": "info",
                "message": f"Multi-document YAML: {doc_count} documents found"
            })
    except yaml.YAMLError as e:
        result["valid"] = False
        msg = str(e)
        if hasattr(e, "problem_mark"):
            mark = e.problem_mark
            msg = f"Line {mark.line + 1}, Column {mark.column + 1}: {e.problem}"
        result["issues"].append({"level": "error", "message": msg})
        return result

    # Check for duplicate keys using a custom loader
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
        pass  # Parsing errors already caught above

    for d in dupes:
        result["valid"] = False
        result["issues"].append({"level": "error", "message": d})

    # Check for very long lines
    if strict:
        for i, line in enumerate(content.splitlines(), 1):
            if len(line) > 256:
                result["issues"].append({
                    "level": "warning",
                    "message": f"Line {i}: Very long line ({len(line)} chars)"
                })

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Validate and lint YAML files. Reports syntax errors, duplicate keys, and structural issues."
    )
    parser.add_argument("files", nargs="+", help="YAML file(s) to validate")
    parser.add_argument("--strict", action="store_true", help="Enable strict checks (trailing whitespace, long lines)")
    parser.add_argument("--json", action="store_true", dest="output_json", help="Output results as JSON")
    parser.add_argument("--quiet", action="store_true", help="Only output errors, suppress info/warnings")
    args = parser.parse_args()

    if not check_pyyaml():
        print("ERROR: PyYAML is required. Install with: pip3 install pyyaml", file=sys.stderr)
        sys.exit(1)

    all_results = []
    any_invalid = False

    for file_path in args.files:
        # Handle glob-like directories
        if os.path.isdir(file_path):
            for root, dirs, files in os.walk(file_path):
                for fn in sorted(files):
                    if fn.endswith((".yaml", ".yml")):
                        full = os.path.join(root, fn)
                        result = validate_yaml(full, strict=args.strict)
                        all_results.append(result)
                        if not result["valid"]:
                            any_invalid = True
        else:
            result = validate_yaml(file_path, strict=args.strict)
            all_results.append(result)
            if not result["valid"]:
                any_invalid = True

    if args.output_json:
        print(json.dumps(all_results, indent=2))
    else:
        for result in all_results:
            status = "✓" if result["valid"] else "✗"
            print(f"{status} {result['file']}")
            for issue in result["issues"]:
                if args.quiet and issue["level"] != "error":
                    continue
                prefix = {"error": "  ERROR", "warning": "  WARN ", "info": "  INFO "}.get(issue["level"], "  ")
                print(f"{prefix}: {issue['message']}")

    sys.exit(1 if any_invalid else 0)


if __name__ == "__main__":
    main()
