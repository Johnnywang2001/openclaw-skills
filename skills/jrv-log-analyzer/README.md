# Log Analyzer

Analyze log files to detect error patterns, aggregate by severity, group repeated errors by fingerprint, and flag anomaly time windows. Use when asked to analyze logs, find errors in log files, debug server issues from logs, summarize log output, or identify error spikes. Supports syslog, application logs, nginx/apache logs, and any text-based log format.

## Installation

```bash
clawhub install jrv-log-analyzer
```

## Usage

```bash
python3 scripts/analyze_logs.py <logfile>
python3 scripts/analyze_logs.py app.log --top 20 --severity ERROR
python3 scripts/analyze_logs.py server.log --json --since "2026-03-01"
```

## Requirements

- Python 3.7+

## License

MIT
