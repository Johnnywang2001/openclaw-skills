#!/usr/bin/env python3
"""Scan WiFi networks, analyze signal strength, and diagnose connectivity.

Cross-platform: macOS (airport/networksetup) and Linux (nmcli/iwlist).
No external dependencies — uses only the Python standard library.
"""

import argparse
import json
import os
import platform
import re
import subprocess
import sys
import time

IS_MACOS = platform.system() == "Darwin"
IS_LINUX = platform.system() == "Linux"

AIRPORT_PATH = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"


def run_cmd(cmd, timeout=15):
    """Run a command and return stdout."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout
        )
        return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return ""


def scan_macos():
    """Scan WiFi networks on macOS using airport."""
    # Check if airport binary exists
    if not os.path.exists(AIRPORT_PATH):
        # Try alternative
        output = run_cmd(["system_profiler", "SPAirPortDataType"])
        if not output:
            print("Error: Cannot find airport utility.", file=sys.stderr)
            return []

    output = run_cmd([AIRPORT_PATH, "-s"])
    if not output:
        print("Error: WiFi scan failed. Ensure WiFi is enabled.", file=sys.stderr)
        return []

    networks = []
    lines = output.strip().split("\n")
    if len(lines) < 2:
        return []

    # Parse header to find column positions
    header = lines[0]
    # airport -s output is fixed-width
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        # Parse: SSID BSSID RSSI CHANNEL HT CC SECURITY
        # SSID can contain spaces so we parse from the right
        parts = line.rsplit(None, 6)
        if len(parts) < 7:
            # Try with fewer fields
            parts = line.rsplit(None, 5)
            if len(parts) < 6:
                continue
            ssid = parts[0]
            bssid = parts[1]
            try:
                rssi = int(parts[2])
            except ValueError:
                continue
            channel = parts[3]
            security = parts[-1] if len(parts) > 4 else "Unknown"
        else:
            ssid = parts[0]
            bssid = parts[1]
            try:
                rssi = int(parts[2])
            except ValueError:
                continue
            channel = parts[3]
            security = parts[6]

        networks.append({
            "ssid": ssid,
            "bssid": bssid,
            "signal": rssi,
            "channel": channel,
            "security": security,
        })

    return networks


def scan_linux():
    """Scan WiFi networks on Linux using nmcli."""
    # Try nmcli first
    output = run_cmd(["nmcli", "-t", "-f", "SSID,BSSID,SIGNAL,CHAN,SECURITY", "dev", "wifi", "list"])
    if output:
        networks = []
        for line in output.strip().split("\n"):
            if not line:
                continue
            parts = line.split(":")
            if len(parts) >= 5:
                try:
                    signal = int(parts[2])
                    # nmcli gives signal as percentage; convert to approximate dBm
                    rssi = int(-100 + signal * 0.6) if signal <= 100 else signal
                except ValueError:
                    rssi = 0
                networks.append({
                    "ssid": parts[0] or "<hidden>",
                    "bssid": parts[1],
                    "signal": rssi,
                    "channel": parts[3],
                    "security": parts[4] or "Open",
                })
        return networks

    # Fallback to iwlist
    output = run_cmd(["sudo", "iwlist", "wlan0", "scan"])
    if not output:
        print("Error: WiFi scan failed. Install nmcli or run with sudo.", file=sys.stderr)
        return []

    networks = []
    current = {}
    for line in output.split("\n"):
        line = line.strip()
        if "Cell" in line and "Address:" in line:
            if current:
                networks.append(current)
            current = {"bssid": line.split("Address:")[1].strip()}
        elif "ESSID:" in line:
            current["ssid"] = line.split("ESSID:")[1].strip('"')
        elif "Signal level=" in line:
            match = re.search(r"Signal level=(-?\d+)", line)
            if match:
                current["signal"] = int(match.group(1))
        elif "Channel:" in line:
            match = re.search(r"Channel:(\d+)", line)
            if match:
                current["channel"] = match.group(1)
        elif "Encryption key:" in line:
            current["security"] = "Encrypted" if "on" in line else "Open"
    if current:
        networks.append(current)
    return networks


def scan_networks():
    """Scan networks on the current platform."""
    if IS_MACOS:
        return scan_macos()
    elif IS_LINUX:
        return scan_linux()
    else:
        print(f"Error: Unsupported platform ({platform.system()}). Use macOS or Linux.", file=sys.stderr)
        return []


def signal_quality(rssi):
    """Convert RSSI to human-readable quality."""
    if rssi >= -50:
        return "Excellent"
    elif rssi >= -60:
        return "Good"
    elif rssi >= -70:
        return "Fair"
    elif rssi >= -80:
        return "Weak"
    else:
        return "Very Weak"


def signal_bar(rssi):
    """Create a visual signal bar."""
    # Normalize: -100 dBm = 0%, -30 dBm = 100%
    pct = max(0, min(100, (rssi + 100) * 100 // 70))
    filled = pct // 10
    return "█" * filled + "░" * (10 - filled)


def cmd_scan(args):
    """Scan and display WiFi networks."""
    networks = scan_networks()
    if not networks:
        print("No networks found.")
        return

    if args.sort == "signal":
        networks.sort(key=lambda n: n.get("signal", -999), reverse=True)
    elif args.sort == "ssid":
        networks.sort(key=lambda n: n.get("ssid", "").lower())
    elif args.sort == "channel":
        networks.sort(key=lambda n: str(n.get("channel", "")))

    if args.json:
        print(json.dumps(networks, indent=2))
        return

    # Table display
    print(f"{'SSID':<30} {'Signal':>7} {'Quality':<10} {'Channel':>7}  {'Security'}")
    print("─" * 80)
    for net in networks:
        ssid = net.get("ssid", "<hidden>")[:29]
        rssi = net.get("signal", 0)
        ch = net.get("channel", "?")
        sec = net.get("security", "?")
        quality = signal_quality(rssi)
        bar = signal_bar(rssi)
        print(f"{ssid:<30} {rssi:>4}dBm {bar} {quality:<10} {ch:>4}  {sec}")

    print(f"\n{len(networks)} network(s) found.")


def get_current_connection_macos():
    """Get current WiFi connection on macOS."""
    # Try airport -I
    output = run_cmd([AIRPORT_PATH, "-I"])
    if not output:
        return None

    info = {}
    for line in output.split("\n"):
        line = line.strip()
        if ":" in line:
            key, _, val = line.partition(":")
            info[key.strip()] = val.strip()

    return {
        "ssid": info.get("SSID", "Not connected"),
        "bssid": info.get("BSSID", "Unknown"),
        "signal": int(info.get("agrCtlRSSI", "0")),
        "noise": int(info.get("agrCtlNoise", "0")),
        "channel": info.get("channel", "?"),
        "tx_rate": info.get("lastTxRate", "?"),
        "security": info.get("link auth", "?"),
    }


def get_current_connection_linux():
    """Get current WiFi connection on Linux."""
    output = run_cmd(["nmcli", "-t", "-f", "ACTIVE,SSID,BSSID,SIGNAL,CHAN,SECURITY", "dev", "wifi"])
    if not output:
        return None
    for line in output.strip().split("\n"):
        parts = line.split(":")
        if parts[0] == "yes" and len(parts) >= 6:
            try:
                signal = int(parts[3])
                rssi = int(-100 + signal * 0.6)
            except ValueError:
                rssi = 0
            return {
                "ssid": parts[1],
                "bssid": parts[2],
                "signal": rssi,
                "channel": parts[4],
                "security": parts[5],
            }
    return None


def cmd_status(args):
    """Show current WiFi connection status."""
    if IS_MACOS:
        conn = get_current_connection_macos()
    elif IS_LINUX:
        conn = get_current_connection_linux()
    else:
        print("Unsupported platform.", file=sys.stderr)
        return

    if not conn or conn.get("ssid") == "Not connected":
        print("Not connected to any WiFi network.")
        return

    if args.json:
        conn["quality"] = signal_quality(conn.get("signal", 0))
        print(json.dumps(conn, indent=2))
        return

    rssi = conn.get("signal", 0)
    print("Current WiFi Connection")
    print("═" * 40)
    print(f"  SSID:     {conn.get('ssid', '?')}")
    print(f"  BSSID:    {conn.get('bssid', '?')}")
    print(f"  Signal:   {rssi} dBm ({signal_quality(rssi)})")
    print(f"  Bar:      {signal_bar(rssi)}")
    if "noise" in conn:
        print(f"  Noise:    {conn['noise']} dBm")
        snr = rssi - conn["noise"]
        print(f"  SNR:      {snr} dB")
    print(f"  Channel:  {conn.get('channel', '?')}")
    if "tx_rate" in conn:
        print(f"  TX Rate:  {conn['tx_rate']} Mbps")
    print(f"  Security: {conn.get('security', '?')}")


def cmd_channels(args):
    """Analyze channel usage and suggest best channel."""
    networks = scan_networks()
    if not networks:
        print("No networks found for channel analysis.")
        return

    # Count networks per channel
    channel_counts = {}
    for net in networks:
        ch = str(net.get("channel", "?"))
        # Normalize — take primary channel
        ch_primary = ch.split(",")[0].strip()
        try:
            ch_num = int(ch_primary)
        except ValueError:
            continue
        channel_counts[ch_num] = channel_counts.get(ch_num, 0) + 1

    if args.json:
        print(json.dumps(channel_counts, indent=2))
        return

    # 2.4 GHz channels: 1-14
    # 5 GHz channels: 36, 40, 44, 48, 52, 56, 60, 64, 100, 104, ...
    ghz24 = {k: v for k, v in channel_counts.items() if k <= 14}
    ghz5 = {k: v for k, v in channel_counts.items() if k > 14}

    print("WiFi Channel Analysis")
    print("═" * 50)

    if ghz24:
        print("\n2.4 GHz Channels:")
        for ch in sorted(ghz24.keys()):
            count = ghz24[ch]
            bar = "█" * count
            print(f"  Ch {ch:>2}: {bar} ({count} network{'s' if count != 1 else ''})")
        # Recommend least congested non-overlapping channel (1, 6, 11)
        non_overlap = {ch: ghz24.get(ch, 0) for ch in [1, 6, 11]}
        best_24 = min(non_overlap, key=non_overlap.get)
        print(f"\n  Recommended 2.4 GHz channel: {best_24} ({non_overlap[best_24]} networks)")

    if ghz5:
        print("\n5 GHz Channels:")
        for ch in sorted(ghz5.keys()):
            count = ghz5[ch]
            bar = "█" * count
            print(f"  Ch {ch:>3}: {bar} ({count} network{'s' if count != 1 else ''})")
        best_5 = min(ghz5, key=ghz5.get)
        print(f"\n  Least congested 5 GHz channel: {best_5} ({ghz5[best_5]} networks)")

    if not ghz24 and not ghz5:
        print("  No channel data available.")


def cmd_monitor(args):
    """Monitor signal strength over time."""
    count = args.count
    interval = args.interval

    print(f"Monitoring WiFi signal ({count} samples, {interval}s interval)...")
    print(f"{'#':>3} {'Time':>8} {'Signal':>7} {'Quality':<10} {'Bar'}")
    print("─" * 50)

    samples = []
    for i in range(count):
        if IS_MACOS:
            conn = get_current_connection_macos()
        elif IS_LINUX:
            conn = get_current_connection_linux()
        else:
            print("Unsupported platform.", file=sys.stderr)
            return

        if not conn:
            print(f"{i+1:>3} Not connected")
            continue

        rssi = conn.get("signal", 0)
        samples.append(rssi)
        ts = time.strftime("%H:%M:%S")
        quality = signal_quality(rssi)
        bar = signal_bar(rssi)
        print(f"{i+1:>3} {ts:>8} {rssi:>4}dBm {quality:<10} {bar}")

        if i < count - 1:
            time.sleep(interval)

    if samples:
        avg = sum(samples) / len(samples)
        mn = min(samples)
        mx = max(samples)
        print(f"\nSummary: avg={avg:.0f}dBm  min={mn}dBm  max={mx}dBm  ({signal_quality(int(avg))})")

        if args.json:
            print(json.dumps({
                "samples": samples,
                "avg": round(avg, 1),
                "min": mn,
                "max": mx,
                "quality": signal_quality(int(avg)),
            }, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Scan WiFi networks, analyze signal, and diagnose connectivity."
    )
    sub = parser.add_subparsers(dest="command", help="Command")

    # scan
    p_scan = sub.add_parser("scan", help="List visible WiFi networks")
    p_scan.add_argument("--json", action="store_true", help="Output as JSON")
    p_scan.add_argument("--sort", choices=["signal", "ssid", "channel"], default="signal",
                        help="Sort by field (default: signal)")

    # status
    p_status = sub.add_parser("status", help="Show current connection details")
    p_status.add_argument("--json", action="store_true", help="Output as JSON")

    # channels
    p_ch = sub.add_parser("channels", help="Analyze channel congestion")
    p_ch.add_argument("--json", action="store_true", help="Output as JSON")

    # monitor
    p_mon = sub.add_parser("monitor", help="Track signal strength over time")
    p_mon.add_argument("--count", "-n", type=int, default=10, help="Number of samples")
    p_mon.add_argument("--interval", "-i", type=float, default=1, help="Seconds between samples")
    p_mon.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    dispatch = {
        "scan": cmd_scan,
        "status": cmd_status,
        "channels": cmd_channels,
        "monitor": cmd_monitor,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
