# Net Speed Test

Test network speed from the command line. Measures download speed, upload speed, and latency (ping) using Cloudflare and public DNS endpoints. No API key or external dependencies required. Use when checking internet speed, diagnosing slow connections, measuring bandwidth, or benchmarking network performance.

## Installation

```bash
clawhub install net-speed-test
```

## Usage

```bash
# Full test (latency + download + upload)
python3 scripts/speedtest.py
# Quick test (smaller payloads, fewer pings)
python3 scripts/speedtest.py --quick
```

## Requirements

- Python 3 (no external dependencies)

## License

MIT
