#!/usr/bin/env python3
"""Audit project dependencies for outdated packages across multiple ecosystems."""

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Timeout for registry requests
REQUEST_TIMEOUT = 10


def fetch_json(url: str) -> dict | None:
    """Fetch JSON from a URL."""
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "dep-audit/1.0"})
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


def parse_version(v: str) -> tuple:
    """Parse version string into comparable tuple."""
    # Strip leading v, ^, ~, >=, etc.
    clean = re.sub(r'^[^0-9]*', '', v.strip())
    parts = []
    for p in clean.split(".")[:3]:
        m = re.match(r'(\d+)', p)
        parts.append(int(m.group(1)) if m else 0)
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts)


def classify_update(current: str, latest: str) -> str:
    """Classify update as major, minor, or patch."""
    cur = parse_version(current)
    lat = parse_version(latest)
    if lat[0] > cur[0]:
        return "major"
    elif lat[1] > cur[1]:
        return "minor"
    elif lat[2] > cur[2]:
        return "patch"
    return "current"


# --- NPM ---

def parse_package_json(path: str) -> list[dict]:
    """Parse package.json and extract dependencies."""
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as e:
        return [{"name": "ERROR", "current": str(e), "latest": "", "update": "error"}]

    deps = {}
    for section in ("dependencies", "devDependencies"):
        if section in data:
            for name, version in data[section].items():
                deps[name] = {"name": name, "current": version, "section": section}
    return list(deps.values())


def check_npm(name: str) -> str:
    """Get latest version from npm registry."""
    data = fetch_json(f"https://registry.npmjs.org/{name}/latest")
    if data and "version" in data:
        return data["version"]
    return ""


# --- PyPI ---

def parse_requirements_txt(path: str) -> list[dict]:
    """Parse requirements.txt."""
    deps = []
    try:
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("-"):
                continue
            # Handle ==, >=, ~=, etc.
            m = re.match(r'^([a-zA-Z0-9_.-]+)\s*([><=~!]+\s*[\d.]+)?', line)
            if m:
                name = m.group(1)
                version = m.group(2).strip().lstrip("=<>~!").strip() if m.group(2) else "unpinned"
                deps.append({"name": name, "current": version})
    except Exception as e:
        return [{"name": "ERROR", "current": str(e), "latest": "", "update": "error"}]
    return deps


def parse_pyproject_toml(path: str) -> list[dict]:
    """Parse pyproject.toml dependencies (basic parsing without toml library)."""
    deps = []
    try:
        content = Path(path).read_text(encoding="utf-8")
        # Find [project] dependencies or [tool.poetry.dependencies]
        in_deps = False
        for line in content.splitlines():
            stripped = line.strip()
            if stripped in ("[project]", "[tool.poetry.dependencies]"):
                in_deps = False  # will look for dependencies key
            if "dependencies" in stripped and "=" in stripped:
                in_deps = True
                continue
            if in_deps:
                if stripped.startswith("]"):
                    in_deps = False
                    continue
                if stripped.startswith("[") and not stripped.startswith('["'):
                    in_deps = False
                    continue
                # Parse "package>=1.0" or "package==1.0"
                m = re.match(r'^["\']?([a-zA-Z0-9_.-]+)\s*([><=~!]+\s*[\d.]+)?', stripped.strip('",\' '))
                if m:
                    name = m.group(1)
                    version = m.group(2).strip().lstrip("=<>~!").strip() if m.group(2) else "unpinned"
                    deps.append({"name": name, "current": version})
    except Exception as e:
        return [{"name": "ERROR", "current": str(e), "latest": "", "update": "error"}]
    return deps


def check_pypi(name: str) -> str:
    """Get latest version from PyPI."""
    data = fetch_json(f"https://pypi.org/pypi/{name}/json")
    if data and "info" in data and "version" in data["info"]:
        return data["info"]["version"]
    return ""


# --- RubyGems ---

def parse_gemfile(path: str) -> list[dict]:
    """Parse Gemfile for gem declarations."""
    deps = []
    try:
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = re.match(r"gem\s+['\"]([^'\"]+)['\"]\s*(?:,\s*['\"]([^'\"]+)['\"])?", line)
            if m:
                name = m.group(1)
                version = m.group(2) if m.group(2) else "unpinned"
                version = re.sub(r'^[~>=<]+\s*', '', version)
                deps.append({"name": name, "current": version})
    except Exception as e:
        return [{"name": "ERROR", "current": str(e), "latest": "", "update": "error"}]
    return deps


def check_rubygems(name: str) -> str:
    """Get latest version from RubyGems."""
    data = fetch_json(f"https://rubygems.org/api/v1/gems/{name}.json")
    if data and "version" in data:
        return data["version"]
    return ""


# --- Orchestrator ---

ECOSYSTEMS = {
    "package.json": {"parser": parse_package_json, "checker": check_npm, "ecosystem": "npm"},
    "requirements.txt": {"parser": parse_requirements_txt, "checker": check_pypi, "ecosystem": "pypi"},
    "pyproject.toml": {"parser": parse_pyproject_toml, "checker": check_pypi, "ecosystem": "pypi"},
    "Gemfile": {"parser": parse_gemfile, "checker": check_rubygems, "ecosystem": "rubygems"},
}


def audit_file(filepath: str, filename: str) -> dict:
    """Audit a single dependency file."""
    eco = ECOSYSTEMS[filename]
    deps = eco["parser"](filepath)
    checker = eco["checker"]

    # Check latest versions concurrently
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {}
        for dep in deps:
            if dep.get("update") == "error":
                results.append(dep)
                continue
            futures[executor.submit(checker, dep["name"])] = dep

        for future in as_completed(futures):
            dep = futures[future]
            latest = future.result()
            dep["latest"] = latest
            if not latest:
                dep["update"] = "unknown"
            elif dep["current"] == "unpinned":
                dep["update"] = "unpinned"
                dep["latest"] = latest
            else:
                dep["update"] = classify_update(dep["current"], latest)
            results.append(dep)

    results.sort(key=lambda d: {"major": 0, "minor": 1, "unpinned": 2, "patch": 3, "current": 4, "unknown": 5, "error": 6}.get(d.get("update", ""), 9))

    outdated = sum(1 for d in results if d.get("update") in ("major", "minor", "patch", "unpinned"))
    return {
        "file": filepath,
        "ecosystem": eco["ecosystem"],
        "total": len(results),
        "outdated": outdated,
        "dependencies": results,
    }


def find_dep_files(dirpath: str) -> list[tuple[str, str]]:
    """Find dependency files in a directory."""
    found = []
    for fname in ECOSYSTEMS:
        fpath = os.path.join(dirpath, fname)
        if os.path.isfile(fpath):
            found.append((fpath, fname))
    return found


def format_text(reports: list[dict], outdated_only: bool = False) -> str:
    """Format audit reports as human-readable text."""
    if not reports:
        return "No dependency files found."

    output = []
    for report in reports:
        output.append(f"\n{'='*65}")
        output.append(f"File: {report['file']} ({report['ecosystem']})")
        output.append(f"Total: {report['total']} | Outdated: {report['outdated']}")
        output.append(f"{'='*65}")

        if not report["dependencies"]:
            output.append("  No dependencies found.")
            continue

        output.append(f"  {'PACKAGE':<30} {'CURRENT':<14} {'LATEST':<14} {'STATUS'}")
        output.append(f"  {'-'*72}")

        for dep in report["dependencies"]:
            update = dep.get("update", "unknown")
            if outdated_only and update in ("current", "unknown"):
                continue
            icon = {
                "major": "🔴",
                "minor": "🟡",
                "patch": "🔵",
                "unpinned": "⚠️ ",
                "current": "✅",
                "unknown": "❓",
                "error": "❌",
            }.get(update, "  ")
            output.append(f"  {icon} {dep['name']:<28} {dep.get('current','?'):<14} {dep.get('latest','?'):<14} {update}")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Audit project dependencies for outdated packages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s .
  %(prog)s package.json
  %(prog)s requirements.txt --format json
  %(prog)s . --outdated-only
""",
    )
    parser.add_argument("target", help="Dependency file or directory to scan")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format (default: text)")
    parser.add_argument("--outdated-only", action="store_true", help="Only show outdated packages")
    args = parser.parse_args()

    target = Path(args.target)
    if not target.exists():
        print(f"Error: '{args.target}' not found", file=sys.stderr)
        sys.exit(1)

    reports = []
    if target.is_dir():
        files = find_dep_files(str(target))
        if not files:
            print("No dependency files found in directory.", file=sys.stderr)
            sys.exit(1)
        for fpath, fname in files:
            reports.append(audit_file(fpath, fname))
    else:
        fname = target.name
        # Allow fuzzy matching: e.g. "dev-requirements.txt" → "requirements.txt"
        if fname not in ECOSYSTEMS:
            matched = None
            for key in ECOSYSTEMS:
                if key in fname or fname.endswith(key):
                    matched = key
                    break
            if matched:
                fname = matched
            else:
                print(f"Error: Unsupported file '{fname}'. Supported: {', '.join(ECOSYSTEMS.keys())}", file=sys.stderr)
                sys.exit(1)
        reports.append(audit_file(str(target), fname))

    if args.format == "json":
        print(json.dumps(reports, indent=2))
    else:
        print(format_text(reports, args.outdated_only))


if __name__ == "__main__":
    main()
