---
name: net-speed-test
description: Test network speed from the command line. Measures download speed, upload speed, and latency (ping) using Cloudflare and public DNS endpoints. No API key or external dependencies required. Use when checking internet speed, diagnosing slow connections, measuring bandwidth, or benchmarking network performance.
---

# Network Speed Test

Measure download speed, upload speed, and latency using public endpoints. Zero dependencies beyond Python stdlib.

## Quick Start

```bash
# Full test (latency + download + upload)
python3 scripts/speedtest.py

# Quick test (smaller payloads, fewer pings)
python3 scripts/speedtest.py --quick

# Individual tests
python3 scripts/speedtest.py --download-only
python3 scripts/speedtest.py --upload-only
python3 scripts/speedtest.py --ping-only

# JSON output
python3 scripts/speedtest.py --json
```

## What It Measures

- **Latency** — TCP connection time to Cloudflare, Google, and Quad9 DNS (min/avg/max ms)
- **Download** — Speed downloading 10-25 MB from Cloudflare speed test endpoint
- **Upload** — Speed uploading 2 MB to Cloudflare

## Flags

- `--quick` — smaller payloads, fewer ping samples (faster results)
- `--download-only` / `--upload-only` / `--ping-only` — run specific test
- `--json` — structured JSON output

## Example Output

```
Testing latency...
  Cloudflare DNS: 4.2 ms (min 3.8, max 5.1)
  Google DNS: 6.1 ms (min 5.5, max 7.2)
Testing download speed...
  Cloudflare: 245.32 Mbps (10.0 MB in 0.326s)
Testing upload speed...
  Upload: 48.71 Mbps (2.0 MB in 0.328s)

--- Summary ---
  Latency:  5.2 ms (avg)
  Download: 245.32 Mbps
  Upload:   48.71 Mbps
```

## Requirements

- Python 3.7+ (no external dependencies)
- Internet connection
