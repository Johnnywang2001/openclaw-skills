# HTTP Client

Make HTTP requests from the command line with support for auth (Bearer, Basic, API key), custom headers, JSON/form body, response formatting, timing, and history logging. A curl replacement with agent-friendly output.

## Installation

```bash
clawhub install jrv-http-client
```

## Usage

```bash
# Simple GET request
python3 scripts/http_client.py GET https://httpbin.org/get
# POST with JSON body
python3 scripts/http_client.py POST https://httpbin.org/post --json '{"name": "test"}'
```

## Requirements

- Python 3.7+

## License

MIT
