# Mock Data Generator

Generate realistic fake/mock data for testing and development. Supports names, emails, addresses, phone numbers, UUIDs, dates, lorem ipsum, credit cards, companies, and more. Output as JSON, CSV, or SQL INSERT statements.

## Installation

```bash
clawhub install jrv-mock-data
```

## Usage

```bash
# Generate 10 fake users as JSON
python3 scripts/mock_data.py user --count 10
# Generate fake email addresses
python3 scripts/mock_data.py email --count 5
```

## Requirements

- Python 3.7+

## License

MIT
