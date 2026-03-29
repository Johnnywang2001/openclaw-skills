# Network Speed Test

Measure network download speed, upload speed, and latency from the command line. Uses Cloudflare speed test endpoints and public DNS for latency measurements. No external dependencies — pure Python with stdlib only. Use when checking internet speed, diagnosing slow connections, measuring latency/jitter, or benchmarking network performance.

## Installation

```bash
clawhub install network-speed-test
```

## Usage

```bash
python3 scripts/speed_test.py --all
python3 scripts/speed_test.py --all --json
```

```bash
python3 scripts/speed_test.py --download
python3 scripts/speed_test.py --upload
python3 scripts/speed_test.py --latency
```

```bash
python3 scripts/speed_test.py --all --quick           # 5 MB down, 1 MB up, 3 pings
python3 scripts/speed_test.py --download --size 25   # 25 MB download test
python3 scripts/speed_test.py --all --size 50         # 50 MB download, 25 MB upload
```

## Requirements

- Python 3 (no external dependencies)

## License

MIT
