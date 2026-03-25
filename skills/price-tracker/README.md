# Price Tracker

Track product prices from web pages and alert on price changes. Monitor Amazon, eBay, and any URL by extracting price data, storing history, and detecting drops. Use when monitoring prices, tracking deals, setting price alerts, comparing historical prices, or building a price watchlist.

## Installation

```bash
clawhub install price-tracker
```

## Usage

```bash
# Add a product to track
python3 scripts/price_tracker.py add "https://example.com/product" --name "Widget Pro"
# Check current prices for all tracked items
python3 scripts/price_tracker.py check
```

## Requirements

- Python 3.7+

## License

MIT
