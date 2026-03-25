#!/usr/bin/env python3
"""Track product prices from web pages and detect price changes."""

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path.home() / ".price-tracker"
DATA_FILE = DATA_DIR / "data.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def load_data() -> dict:
    """Load tracked products data."""
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"products": [], "next_id": 1}


def save_data(data: dict):
    """Save tracked products data."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def fetch_page(url: str) -> str:
    """Fetch HTML content from a URL."""
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"URL error: {e.reason}")
    except Exception as e:
        raise RuntimeError(f"Fetch error: {e}")


def extract_price(html: str) -> dict | None:
    """Extract price from HTML using multiple strategies."""

    # Strategy 1: JSON-LD structured data
    json_ld_pattern = r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>'
    for match in re.finditer(json_ld_pattern, html, re.DOTALL | re.IGNORECASE):
        try:
            data = json.loads(match.group(1))
            if isinstance(data, list):
                data = data[0] if data else {}
            price_info = _extract_from_jsonld(data)
            if price_info:
                return price_info
        except (json.JSONDecodeError, KeyError):
            continue

    # Strategy 2: Open Graph meta tags
    og_price = re.search(r'<meta\s+(?:property|name)=["\']product:price:amount["\']\s+content=["\']([^"\']+)', html, re.IGNORECASE)
    og_currency = re.search(r'<meta\s+(?:property|name)=["\']product:price:currency["\']\s+content=["\']([^"\']+)', html, re.IGNORECASE)
    if og_price:
        try:
            price = float(og_price.group(1).replace(",", ""))
            currency = og_currency.group(1) if og_currency else "USD"
            return {"price": price, "currency": currency}
        except ValueError:
            pass

    # Strategy 3: Common price patterns in HTML
    price_patterns = [
        # data-price attribute
        r'data-price=["\'](\d+[.,]?\d*)["\']',
        # itemprop="price"
        r'itemprop=["\']price["\'][^>]*content=["\']([^"\']+)',
        # Common price class names
        r'class=["\'][^"\']*(?:price|Price|product-price|sale-price|current-price)[^"\']*["\'][^>]*>\s*(?:<[^>]+>)*\s*[\$£€¥]?\s*(\d{1,7}[.,]\d{2})',
        # Price with currency symbol
        r'[\$£€]\s*(\d{1,7}(?:,\d{3})*(?:\.\d{2})?)',
    ]

    for pattern in price_patterns:
        m = re.search(pattern, html, re.IGNORECASE)
        if m:
            price_str = m.group(1).replace(",", "")
            try:
                price = float(price_str)
                if 0.01 <= price <= 999999.99:
                    # Detect currency from context
                    currency = _detect_currency(html)
                    return {"price": price, "currency": currency}
            except ValueError:
                continue

    return None


def _extract_from_jsonld(data: dict) -> dict | None:
    """Extract price from JSON-LD structured data."""
    if not isinstance(data, dict):
        return None

    # Direct offer
    if data.get("@type") in ("Product", "IndividualProduct"):
        offers = data.get("offers", {})
        if isinstance(offers, list):
            offers = offers[0] if offers else {}
        if isinstance(offers, dict):
            price = offers.get("price") or offers.get("lowPrice")
            if price:
                try:
                    return {
                        "price": float(str(price).replace(",", "")),
                        "currency": offers.get("priceCurrency", "USD"),
                    }
                except ValueError:
                    pass

    # Check nested
    for key in ("offers", "mainEntity", "itemListElement"):
        nested = data.get(key)
        if isinstance(nested, dict):
            result = _extract_from_jsonld(nested)
            if result:
                return result
        elif isinstance(nested, list):
            for item in nested[:3]:
                if isinstance(item, dict):
                    result = _extract_from_jsonld(item)
                    if result:
                        return result

    return None


def _detect_currency(html: str) -> str:
    """Detect currency from page content."""
    if "£" in html:
        return "GBP"
    if "€" in html:
        return "EUR"
    if "¥" in html:
        return "JPY"
    if "₹" in html:
        return "INR"
    if "R$" in html:
        return "BRL"
    return "USD"


# --- Commands ---

def cmd_add(args):
    """Add a product URL to track."""
    data = load_data()
    # Check for duplicate
    for p in data["products"]:
        if p["url"] == args.url:
            print(f"Already tracking this URL (ID: {p['id']})")
            return

    product = {
        "id": data["next_id"],
        "name": args.name or args.url[:60],
        "url": args.url,
        "history": [],
        "added": datetime.now(timezone.utc).isoformat(),
    }

    # Try to get initial price
    try:
        html = fetch_page(args.url)
        price_info = extract_price(html)
        if price_info:
            product["history"].append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "price": price_info["price"],
                "currency": price_info["currency"],
            })
            print(f"Added: {product['name']} — Current price: {price_info['currency']} {price_info['price']:.2f}")
        else:
            print(f"Added: {product['name']} — Could not extract initial price (will retry on check)")
    except RuntimeError as e:
        print(f"Added: {product['name']} — Fetch warning: {e}")

    data["products"].append(product)
    data["next_id"] += 1
    save_data(data)


def cmd_check(args):
    """Check current prices for all tracked products."""
    data = load_data()
    if not data["products"]:
        print("No products being tracked. Use 'add' to start tracking.")
        return

    results = []
    for product in data["products"]:
        try:
            html = fetch_page(product["url"])
            price_info = extract_price(html)
        except RuntimeError as e:
            results.append({"id": product["id"], "name": product["name"], "error": str(e)})
            continue

        if not price_info:
            results.append({"id": product["id"], "name": product["name"], "error": "Could not extract price"})
            continue

        # Compare with last known price
        last_price = product["history"][-1]["price"] if product["history"] else None
        change = None
        change_pct = None
        if last_price is not None and last_price != price_info["price"]:
            change = price_info["price"] - last_price
            change_pct = (change / last_price) * 100

        # Record new entry
        product["history"].append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "price": price_info["price"],
            "currency": price_info["currency"],
        })

        result = {
            "id": product["id"],
            "name": product["name"],
            "price": price_info["price"],
            "currency": price_info["currency"],
        }
        if change is not None:
            result["change"] = round(change, 2)
            result["change_pct"] = round(change_pct, 1)
        results.append(result)

    save_data(data)

    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            if "error" in r:
                print(f"  ❌ [{r['id']}] {r['name']}: {r['error']}")
            elif "change" in r:
                arrow = "📉" if r["change"] < 0 else "📈"
                print(f"  {arrow} [{r['id']}] {r['name']}: {r['currency']} {r['price']:.2f} ({r['change']:+.2f}, {r['change_pct']:+.1f}%)")
            else:
                print(f"  💲 [{r['id']}] {r['name']}: {r['currency']} {r['price']:.2f}")


def cmd_peek(args):
    """One-shot price extraction from a URL."""
    try:
        html = fetch_page(args.url)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    price_info = extract_price(html)
    if price_info:
        if args.format == "json":
            print(json.dumps(price_info, indent=2))
        else:
            print(f"Price: {price_info['currency']} {price_info['price']:.2f}")
    else:
        print("Could not extract price from this page.", file=sys.stderr)
        sys.exit(1)


def cmd_history(args):
    """Show price history for tracked products."""
    data = load_data()
    if not data["products"]:
        print("No products being tracked.")
        return

    if args.format == "json":
        print(json.dumps([{"id": p["id"], "name": p["name"], "history": p["history"]} for p in data["products"]], indent=2))
        return

    for product in data["products"]:
        print(f"\n[{product['id']}] {product['name']}")
        if not product["history"]:
            print("  No price history yet.")
            continue
        print(f"  {'DATE':<22} {'PRICE':<14} {'CHANGE'}")
        print(f"  {'-'*50}")
        prev = None
        for entry in product["history"]:
            ts = entry["timestamp"][:19].replace("T", " ")
            price = entry["price"]
            change_str = ""
            if prev is not None:
                diff = price - prev
                if diff != 0:
                    change_str = f"{diff:+.2f}"
            print(f"  {ts:<22} {entry.get('currency', 'USD')} {price:<10.2f} {change_str}")
            prev = price


def cmd_list(args):
    """List all tracked products."""
    data = load_data()
    if not data["products"]:
        print("No products being tracked.")
        return

    if args.format == "json":
        print(json.dumps([{"id": p["id"], "name": p["name"], "url": p["url"], "entries": len(p["history"])} for p in data["products"]], indent=2))
        return

    print(f"{'ID':<5} {'NAME':<40} {'ENTRIES':<8} URL")
    print("-" * 80)
    for p in data["products"]:
        print(f"{p['id']:<5} {p['name'][:38]:<40} {len(p['history']):<8} {p['url'][:50]}")


def cmd_remove(args):
    """Remove a tracked product."""
    data = load_data()
    original_count = len(data["products"])
    data["products"] = [p for p in data["products"] if p["id"] != args.id]
    if len(data["products"]) < original_count:
        save_data(data)
        print(f"Removed product ID {args.id}")
    else:
        print(f"No product found with ID {args.id}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Track product prices from web pages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s add "https://example.com/product" --name "Widget"
  %(prog)s check
  %(prog)s peek "https://example.com/product"
  %(prog)s history
  %(prog)s list
  %(prog)s remove 1
""",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # add
    p_add = sub.add_parser("add", help="Add a product URL to track")
    p_add.add_argument("url", help="Product page URL")
    p_add.add_argument("--name", help="Friendly product name")
    p_add.add_argument("--format", choices=["text", "json"], default="text")

    # check
    p_check = sub.add_parser("check", help="Check current prices for tracked items")
    p_check.add_argument("--format", choices=["text", "json"], default="text")

    # peek
    p_peek = sub.add_parser("peek", help="One-shot price extraction from a URL")
    p_peek.add_argument("url", help="Product page URL")
    p_peek.add_argument("--format", choices=["text", "json"], default="text")

    # history
    p_hist = sub.add_parser("history", help="Show price change history")
    p_hist.add_argument("--format", choices=["text", "json"], default="text")

    # list
    p_list = sub.add_parser("list", help="List tracked products")
    p_list.add_argument("--format", choices=["text", "json"], default="text")

    # remove
    p_remove = sub.add_parser("remove", help="Remove a tracked product")
    p_remove.add_argument("id", type=int, help="Product ID to remove")

    args = parser.parse_args()

    commands = {
        "add": cmd_add,
        "check": cmd_check,
        "peek": cmd_peek,
        "history": cmd_history,
        "list": cmd_list,
        "remove": cmd_remove,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
