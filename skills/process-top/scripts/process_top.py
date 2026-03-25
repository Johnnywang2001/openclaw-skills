#!/usr/bin/env python3
"""Process monitor — list, search, and analyze running processes.

Cross-platform (macOS/Linux). Uses /proc on Linux and `ps` command as fallback.
No external dependencies required.
"""

import argparse
import json
import os
import platform
import re
import subprocess
import sys


def get_processes() -> list[dict]:
    """Get list of running processes using ps command."""
    try:
        result = subprocess.run(
            ["ps", "aux"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            print(f"Error running ps: {result.stderr}", file=sys.stderr)
            sys.exit(1)
    except FileNotFoundError:
        print("Error: 'ps' command not found", file=sys.stderr)
        sys.exit(1)

    lines = result.stdout.strip().split("\n")
    if len(lines) < 2:
        return []

    processes = []
    header = lines[0]
    for line in lines[1:]:
        parts = line.split(None, 10)
        if len(parts) < 11:
            continue
        processes.append({
            "user": parts[0],
            "pid": int(parts[1]),
            "cpu": float(parts[2]),
            "mem": float(parts[3]),
            "vsz": int(parts[4]),
            "rss": int(parts[5]),
            "tty": parts[6],
            "stat": parts[7],
            "start": parts[8],
            "time": parts[9],
            "command": parts[10],
        })
    return processes


def human_kb(kb: int) -> str:
    """Convert KB to human-readable."""
    if kb < 1024:
        return f"{kb} KB"
    elif kb < 1024 * 1024:
        return f"{kb / 1024:.1f} MB"
    else:
        return f"{kb / (1024 * 1024):.1f} GB"


def cmd_list(args):
    """List top processes by CPU or memory."""
    procs = get_processes()

    sort_key = args.sort
    if sort_key not in ("cpu", "mem", "rss", "pid"):
        sort_key = "cpu"

    procs.sort(key=lambda p: p.get(sort_key, 0), reverse=True)
    limit = args.limit or 20

    if args.json:
        print(json.dumps(procs[:limit], indent=2))
        return

    print(f"{'PID':>7}  {'USER':<12}  {'CPU%':>5}  {'MEM%':>5}  {'RSS':>9}  COMMAND")
    print(f"{'-' * 80}")
    for p in procs[:limit]:
        cmd = p["command"][:50]
        print(f"{p['pid']:>7}  {p['user']:<12}  {p['cpu']:>5.1f}  {p['mem']:>5.1f}  {human_kb(p['rss']):>9}  {cmd}")
    print(f"\nShowing top {min(limit, len(procs))} of {len(procs)} processes (sorted by {sort_key})")


def cmd_search(args):
    """Search for processes by name or pattern."""
    procs = get_processes()
    pattern = re.compile(args.pattern, re.IGNORECASE)
    matches = [p for p in procs if pattern.search(p["command"]) or pattern.search(p["user"])]

    if args.json:
        print(json.dumps(matches, indent=2))
        return

    if not matches:
        print(f"No processes matching '{args.pattern}'")
        return

    print(f"Processes matching '{args.pattern}':")
    print(f"{'PID':>7}  {'USER':<12}  {'CPU%':>5}  {'MEM%':>5}  {'RSS':>9}  COMMAND")
    print(f"{'-' * 80}")
    for p in matches:
        cmd = p["command"][:50]
        print(f"{p['pid']:>7}  {p['user']:<12}  {p['cpu']:>5.1f}  {p['mem']:>5.1f}  {human_kb(p['rss']):>9}  {cmd}")
    print(f"\n{len(matches)} match(es)")


def cmd_summary(args):
    """Show system process summary."""
    procs = get_processes()

    total_cpu = sum(p["cpu"] for p in procs)
    total_rss = sum(p["rss"] for p in procs)
    users = set(p["user"] for p in procs)

    # Count by state
    states = {}
    for p in procs:
        s = p["stat"][0] if p["stat"] else "?"
        state_name = {
            "R": "Running", "S": "Sleeping", "D": "Disk wait",
            "Z": "Zombie", "T": "Stopped", "I": "Idle",
            "U": "Uninterruptible"
        }.get(s, s)
        states[state_name] = states.get(state_name, 0) + 1

    # Top CPU consumers
    by_cpu = sorted(procs, key=lambda p: p["cpu"], reverse=True)[:5]
    # Top memory consumers
    by_mem = sorted(procs, key=lambda p: p["rss"], reverse=True)[:5]

    if args.json:
        print(json.dumps({
            "total_processes": len(procs),
            "total_cpu_percent": round(total_cpu, 1),
            "total_rss_kb": total_rss,
            "unique_users": len(users),
            "states": states,
            "top_cpu": by_cpu[:5],
            "top_mem": by_mem[:5],
        }, indent=2))
        return

    print(f"Process Summary")
    print(f"{'=' * 50}")
    print(f"Total processes:  {len(procs)}")
    print(f"Total CPU usage:  {total_cpu:.1f}%")
    print(f"Total RSS memory: {human_kb(total_rss)}")
    print(f"Active users:     {len(users)}")
    print()

    print("Process states:")
    for state, count in sorted(states.items(), key=lambda x: -x[1]):
        print(f"  {state:<18} {count}")
    print()

    print("Top 5 CPU consumers:")
    for p in by_cpu:
        print(f"  {p['cpu']:>5.1f}%  PID {p['pid']:<7}  {p['command'][:45]}")
    print()

    print("Top 5 memory consumers:")
    for p in by_mem:
        print(f"  {human_kb(p['rss']):>9}  PID {p['pid']:<7}  {p['command'][:45]}")


def cmd_tree(args):
    """Show process count grouped by command name."""
    procs = get_processes()
    groups: dict[str, dict] = {}
    for p in procs:
        cmd_name = p["command"].split()[0].split("/")[-1]
        if cmd_name not in groups:
            groups[cmd_name] = {"count": 0, "cpu": 0.0, "rss": 0}
        groups[cmd_name]["count"] += 1
        groups[cmd_name]["cpu"] += p["cpu"]
        groups[cmd_name]["rss"] += p["rss"]

    sort_key = args.sort or "rss"
    sorted_groups = sorted(groups.items(), key=lambda x: x[1].get(sort_key, 0), reverse=True)
    limit = args.limit or 20

    if args.json:
        print(json.dumps(dict(sorted_groups[:limit]), indent=2))
        return

    print(f"{'COMMAND':<25}  {'COUNT':>5}  {'CPU%':>6}  {'RSS':>10}")
    print(f"{'-' * 55}")
    for name, info in sorted_groups[:limit]:
        print(f"{name:<25}  {info['count']:>5}  {info['cpu']:>6.1f}  {human_kb(info['rss']):>10}")
    print(f"\n{len(groups)} unique commands, {len(procs)} total processes")


def main():
    parser = argparse.ArgumentParser(description="Process monitor — list, search, and analyze running processes")
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # list
    p_list = sub.add_parser("list", help="List top processes")
    p_list.add_argument("--sort", choices=["cpu", "mem", "rss", "pid"], default="cpu", help="Sort by field")
    p_list.add_argument("--limit", type=int, default=20, help="Number of processes to show")
    p_list.add_argument("--json", action="store_true", help="Output as JSON")
    p_list.set_defaults(func=cmd_list)

    # search
    p_search = sub.add_parser("search", help="Search processes by name/pattern")
    p_search.add_argument("pattern", help="Regex pattern to match against command or user")
    p_search.add_argument("--json", action="store_true", help="Output as JSON")
    p_search.set_defaults(func=cmd_search)

    # summary
    p_sum = sub.add_parser("summary", help="System process summary")
    p_sum.add_argument("--json", action="store_true", help="Output as JSON")
    p_sum.set_defaults(func=cmd_summary)

    # group
    p_tree = sub.add_parser("group", help="Group processes by command name")
    p_tree.add_argument("--sort", choices=["count", "cpu", "rss"], default="rss", help="Sort groups by")
    p_tree.add_argument("--limit", type=int, default=20, help="Number of groups to show")
    p_tree.add_argument("--json", action="store_true", help="Output as JSON")
    p_tree.set_defaults(func=cmd_tree)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)
    args.func(args)


if __name__ == "__main__":
    main()
