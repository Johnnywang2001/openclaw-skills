---
name: price-tracker
description: Track product prices from web pages and alert on price changes. Monitor Amazon, eBay, and any URL by extracting price data, storing history, and detecting drops. Use when monitoring prices, tracking deals, setting price alerts, comparing historical prices, or building a price watchlist. Triggers on "track price", "price monitor", "watch this product", "alert me when price drops", "price history", "deal tracker".
---

# Price Tracker

Monitor product prices from any web page. Extract prices, track changes over time, and detect drops.

## Quick Start

```bash
# Add a product to track
python3 scripts/price_tracker.py add "https://example.com/product" --name "Widget Pro"

# Check current prices for all tracked items
python3 scripts/price_tracker.py check

# Check a single URL without tracking
python3 scripts/price_tracker.py peek "https://example.com/product"

# View price history
python3 scripts/price_tracker.py history

# List tracked products
python3 scripts/price_tracker.py list

# Remove a tracked product
python3 scripts/price_tracker.py remove 1

# JSON output
python3 scripts/price_tracker.py check --format json
```

## How It Works

1. **add** — Register a URL to track with an optional friendly name
2. **check** — Fetch current prices for all tracked items, record history, flag changes
3. **peek** — One-shot price extraction from any URL (no tracking)
4. **history** — Show price change timeline for tracked items
5. **list** — Show all tracked URLs
6. **remove** — Stop tracking a product by ID

## Price Extraction

Extracts prices using multiple strategies:
- JSON-LD structured data (`@type: Product/Offer`)
- Open Graph `product:price` meta tags
- Common price CSS class patterns
- Schema.org markup
- Currency-prefixed number detection ($ £ €)

## Data Storage

Price data is stored in `~/.price-tracker/data.json`. History entries include timestamp, price, and currency.
