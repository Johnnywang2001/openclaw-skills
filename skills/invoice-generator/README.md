# Invoice Generator

Generate professional PDF invoices from natural language or structured data. Use when the user asks to create an invoice, bill a client, generate a receipt, track payments, or manage invoicing. Supports line items, tax calculation, discounts, multiple currencies, recurring invoices, and payment tracking. Outputs clean PDF invoices ready to send.

## Installation

```bash
clawhub install invoice-generator
```

## Usage

```bash
python3 scripts/invoice.py create \
  --client "Acme Corp" \
  --items "Web Development,40h,$150" "Hosting Setup,1,$500" \
  --tax 7 \
```

## Requirements

- Python 3.7+

## License

MIT
