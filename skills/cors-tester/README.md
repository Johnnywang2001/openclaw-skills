# CORS Tester

Test and debug CORS (Cross-Origin Resource Sharing) configurations on live URLs. Use when checking if a server returns correct CORS headers, debugging CORS errors, testing preflight OPTIONS requests, verifying allowed origins/methods/headers, or auditing CORS security posture. Also use when generating CORS configurations for Apache, Nginx, Express, or other frameworks.

## Installation

```bash
clawhub install cors-tester
```

## Usage

```bash
# Test CORS headers on a URL
python3 scripts/cors_tester.py test https://api.example.com/data --origin https://myapp.com
# Test preflight (OPTIONS) request
python3 scripts/cors_tester.py preflight https://api.example.com/data --origin https://myapp.com --method POST --header "Content-Type"
```

## Requirements

- Python 3.7+

## License

MIT
