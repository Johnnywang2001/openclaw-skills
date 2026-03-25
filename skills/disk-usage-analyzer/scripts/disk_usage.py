#!/usr/bin/env python3
"""Disk usage analyzer — scan directories, find large files, and get cleanup recommendations."""

import argparse
import json
import os
import sys
from collections import defaultdict
from pathlib import Path


def human_size(nbytes: float) -> str:
    """Convert bytes to human-readable string."""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(nbytes) < 1024:
            return f"{nbytes:.1f} {unit}"
        nbytes /= 1024
    return f"{nbytes:.1f} PB"


def scan_directory(path: str, depth: int = 1) -> dict:
    """Scan a directory and return size info."""
    root = Path(path).resolve()
    if not root.exists():
        print(f"Error: path does not exist: {root}", file=sys.stderr)
        sys.exit(1)

    dir_sizes = defaultdict(int)
    file_list = []
    ext_sizes = defaultdict(lambda: {"count": 0, "bytes": 0})
    total_bytes = 0
    total_files = 0
    total_dirs = 0
    errors = []

    for dirpath, dirnames, filenames in os.walk(str(root)):
        rel = os.path.relpath(dirpath, str(root))
        current_depth = 0 if rel == "." else rel.count(os.sep) + 1

        # Skip hidden dirs at top level to avoid .git etc unless explicitly scanning
        total_dirs += 1

        for fname in filenames:
            fpath = os.path.join(dirpath, fname)
            try:
                stat = os.lstat(fpath)
                if not os.path.islink(fpath):
                    size = stat.st_size
                else:
                    size = 0
            except (OSError, PermissionError) as e:
                errors.append(str(e))
                continue

            total_files += 1
            total_bytes += size

            # Track by extension
            ext = Path(fname).suffix.lower() or "(no ext)"
            ext_sizes[ext]["count"] += 1
            ext_sizes[ext]["bytes"] += size

            # Track file for top-N
            file_list.append({"path": os.path.relpath(fpath, str(root)), "bytes": size})

            # Aggregate into directory buckets up to requested depth
            parts = Path(os.path.relpath(dirpath, str(root))).parts
            if parts and parts[0] == ".":
                parts = parts[1:]
            bucket = str(Path(*parts[:depth])) if parts else "."
            dir_sizes[bucket] += size

    return {
        "root": str(root),
        "total_bytes": total_bytes,
        "total_files": total_files,
        "total_dirs": total_dirs,
        "dir_sizes": dict(dir_sizes),
        "ext_sizes": dict(ext_sizes),
        "files": file_list,
        "errors": errors,
    }


def cmd_scan(args):
    """Scan a directory and show usage summary."""
    data = scan_directory(args.path, depth=args.depth)

    if args.json:
        print(json.dumps(data, indent=2))
        return

    print(f"Disk Usage Report: {data['root']}")
    print(f"{'=' * 60}")
    print(f"Total size:  {human_size(data['total_bytes'])}")
    print(f"Files:       {data['total_files']:,}")
    print(f"Directories: {data['total_dirs']:,}")
    print()

    # Top directories
    sorted_dirs = sorted(data["dir_sizes"].items(), key=lambda x: x[1], reverse=True)
    limit = args.limit or 15
    print(f"Top {min(limit, len(sorted_dirs))} directories by size:")
    print(f"{'-' * 60}")
    for dname, dbytes in sorted_dirs[:limit]:
        pct = (dbytes / data["total_bytes"] * 100) if data["total_bytes"] > 0 else 0
        bar = "█" * int(pct / 2)
        print(f"  {human_size(dbytes):>10s}  {pct:5.1f}%  {bar}  {dname}")
    print()

    # Top files
    sorted_files = sorted(data["files"], key=lambda x: x["bytes"], reverse=True)
    print(f"Top {min(limit, len(sorted_files))} largest files:")
    print(f"{'-' * 60}")
    for f in sorted_files[:limit]:
        print(f"  {human_size(f['bytes']):>10s}  {f['path']}")
    print()

    # Extension breakdown
    sorted_exts = sorted(data["ext_sizes"].items(), key=lambda x: x[1]["bytes"], reverse=True)
    print(f"Top extensions by total size:")
    print(f"{'-' * 60}")
    for ext, info in sorted_exts[:10]:
        print(f"  {human_size(info['bytes']):>10s}  {info['count']:>6,} files  {ext}")

    if data["errors"]:
        print(f"\n⚠ {len(data['errors'])} errors encountered (permission denied, etc.)")


def cmd_find_large(args):
    """Find files larger than a threshold."""
    threshold = parse_size(args.threshold)
    data = scan_directory(args.path, depth=1)
    large = [f for f in data["files"] if f["bytes"] >= threshold]
    large.sort(key=lambda x: x["bytes"], reverse=True)

    if args.json:
        print(json.dumps(large, indent=2))
        return

    print(f"Files >= {human_size(threshold)} in {data['root']}:")
    print(f"{'-' * 60}")
    if not large:
        print("  (none found)")
    for f in large:
        print(f"  {human_size(f['bytes']):>10s}  {f['path']}")
    print(f"\nFound {len(large)} file(s)")


def cmd_duplicates(args):
    """Find files with identical sizes (potential duplicates)."""
    data = scan_directory(args.path, depth=1)

    # Group by size (quick heuristic — not hash-based but useful for large files)
    size_groups = defaultdict(list)
    min_size = parse_size(args.min_size) if args.min_size else 1_048_576  # default 1MB
    for f in data["files"]:
        if f["bytes"] >= min_size:
            size_groups[f["bytes"]].append(f["path"])

    dupes = {human_size(sz): paths for sz, paths in size_groups.items() if len(paths) > 1}

    if args.json:
        print(json.dumps(dupes, indent=2))
        return

    print(f"Potential duplicates (same size, >= {human_size(min_size)}):")
    print(f"{'-' * 60}")
    if not dupes:
        print("  (none found)")
    for sz, paths in sorted(dupes.items()):
        print(f"\n  [{sz}] ({len(paths)} files)")
        for p in paths:
            print(f"    {p}")


def parse_size(s: str) -> int:
    """Parse human size string like '100MB' to bytes."""
    s = s.strip().upper()
    multipliers = {"B": 1, "K": 1024, "KB": 1024, "M": 1024**2, "MB": 1024**2,
                   "G": 1024**3, "GB": 1024**3, "T": 1024**4, "TB": 1024**4}
    for suffix, mult in sorted(multipliers.items(), key=lambda x: -len(x[0])):
        if s.endswith(suffix):
            return int(float(s[:-len(suffix)]) * mult)
    return int(s)


def main():
    parser = argparse.ArgumentParser(
        description="Disk usage analyzer — scan directories, find large files, detect duplicates"
    )
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # scan
    p_scan = sub.add_parser("scan", help="Scan a directory and show usage breakdown")
    p_scan.add_argument("path", nargs="?", default=".", help="Directory to scan (default: .)")
    p_scan.add_argument("--depth", type=int, default=1, help="Directory grouping depth (default: 1)")
    p_scan.add_argument("--limit", type=int, default=15, help="Number of top items to show")
    p_scan.add_argument("--json", action="store_true", help="Output as JSON")
    p_scan.set_defaults(func=cmd_scan)

    # find-large
    p_large = sub.add_parser("find-large", help="Find files larger than a threshold")
    p_large.add_argument("path", nargs="?", default=".", help="Directory to scan")
    p_large.add_argument("--threshold", default="100MB", help="Minimum file size (e.g., 50MB, 1GB)")
    p_large.add_argument("--json", action="store_true", help="Output as JSON")
    p_large.set_defaults(func=cmd_find_large)

    # duplicates
    p_dup = sub.add_parser("duplicates", help="Find potential duplicate files (same size)")
    p_dup.add_argument("path", nargs="?", default=".", help="Directory to scan")
    p_dup.add_argument("--min-size", default="1MB", help="Minimum file size to consider (default: 1MB)")
    p_dup.add_argument("--json", action="store_true", help="Output as JSON")
    p_dup.set_defaults(func=cmd_duplicates)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)
    args.func(args)


if __name__ == "__main__":
    main()
