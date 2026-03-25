---
name: wifi-scanner
description: Scan and analyze nearby WiFi networks, check signal strength, and diagnose connectivity issues. Use when asked to find available WiFi networks, check signal quality, troubleshoot WiFi, compare network speeds, find the best channel, or analyze wireless interference. Supports macOS and Linux. Also triggers on "scan wifi", "list networks", "wifi signal", "wifi channels", "best wifi channel", or "network diagnostics".
---

# wifi-scanner

Scan WiFi networks, analyze signal strength, and diagnose connectivity.

## Quick Start

```bash
# Scan available WiFi networks
python3 scripts/wifi_scanner.py scan

# Show current connection info
python3 scripts/wifi_scanner.py status

# Analyze channel usage (find best channel)
python3 scripts/wifi_scanner.py channels

# Show signal quality over time (5 samples, 2s interval)
python3 scripts/wifi_scanner.py monitor --count 5 --interval 2

# Output as JSON
python3 scripts/wifi_scanner.py scan --json

# Sort by signal strength
python3 scripts/wifi_scanner.py scan --sort signal
```

## Commands

| Command | Description |
|---------|-------------|
| `scan` | List all visible WiFi networks with SSID, signal, channel, security |
| `status` | Show current WiFi connection details |
| `channels` | Analyze channel congestion, suggest best channel |
| `monitor` | Track signal strength over time |

## Options

| Flag | Description |
|------|-------------|
| `--json` | Output as JSON |
| `--sort FIELD` | Sort by: signal, ssid, channel (with `scan`) |
| `--count N` | Number of samples (with `monitor`, default: 10) |
| `--interval SECS` | Seconds between samples (with `monitor`, default: 1) |

## Platform Support

- **macOS**: Uses `airport` and `networksetup` (built-in, no install needed)
- **Linux**: Uses `nmcli` or `iwlist` (typically pre-installed)
