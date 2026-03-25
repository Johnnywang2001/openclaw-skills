# Timezone Toolkit

Convert times between timezones, show world clocks, find meeting overlap across zones, and look up UTC offsets and DST status. Use when converting between timezones (e.g., "what's 3 PM EST in Tokyo?"), showing current time across cities, planning meetings across timezones, checking DST status, or listing available timezone names. Supports 500+ IANA timezones plus common aliases (EST, PST, IST, JST, etc.). No external dependencies — uses Python's built-in zoneinfo.

## Installation

```bash
clawhub install timezone-toolkit
```

## Usage

```bash
# Convert time between zones
python3 scripts/timezone_toolkit.py convert 15:30 --from EST --to PST JST UTC
# World clock (default cities)
python3 scripts/timezone_toolkit.py now
```

## Requirements

- Python 3.9+ (no external dependencies)

## License

MIT
