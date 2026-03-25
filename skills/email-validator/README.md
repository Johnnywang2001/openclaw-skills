# Email Validator

Validate email addresses with syntax checks (RFC 5322), MX record verification, disposable/temporary email detection, and common typo suggestions. Use when validating user signups, cleaning email lists, checking deliverability, or detecting throwaway addresses. Supports batch validation from file. No API keys required.

## Installation

```bash
clawhub install email-validator
```

## Usage

```bash
# Validate a single email
python3 scripts/email_validate.py user@example.com
# Validate multiple emails
python3 scripts/email_validate.py user@gmail.com admin@company.org test@mailinator.com
```

## Requirements

- Python 3.7+

## License

MIT
