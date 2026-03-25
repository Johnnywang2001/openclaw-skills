#!/usr/bin/env python3
"""HTTP status code reference and URL header analyzer.

Lookup HTTP status codes, check URL response headers, and analyze security headers.
No external dependencies — uses urllib from stdlib.
"""

import argparse
import json
import ssl
import sys
import urllib.request
import urllib.error

# Complete HTTP status code database
STATUS_CODES = {
    100: ("Continue", "Server received headers, client should proceed with body."),
    101: ("Switching Protocols", "Server is switching protocols as requested (e.g., WebSocket upgrade)."),
    102: ("Processing", "Server received and is processing the request (WebDAV)."),
    103: ("Early Hints", "Preload resources while server prepares the response."),
    200: ("OK", "Request succeeded."),
    201: ("Created", "Request succeeded and a new resource was created."),
    202: ("Accepted", "Request accepted for processing, but not completed yet."),
    203: ("Non-Authoritative Information", "Response from a transforming proxy, not the origin server."),
    204: ("No Content", "Request succeeded but there's no content to return."),
    205: ("Reset Content", "Like 204, but tells the client to reset its document view."),
    206: ("Partial Content", "Server is delivering part of the resource (Range header)."),
    207: ("Multi-Status", "Multiple status codes for multiple operations (WebDAV)."),
    208: ("Already Reported", "Members of a DAV binding already enumerated."),
    226: ("IM Used", "Server fulfilled a GET with instance-manipulations applied."),
    300: ("Multiple Choices", "Multiple possible responses; client should choose one."),
    301: ("Moved Permanently", "Resource has been permanently moved to a new URL."),
    302: ("Found", "Resource temporarily at a different URL (commonly used for redirects)."),
    303: ("See Other", "Response to the request can be found at another URL via GET."),
    304: ("Not Modified", "Resource hasn't changed since last request (caching)."),
    305: ("Use Proxy", "Deprecated. Resource must be accessed through the specified proxy."),
    307: ("Temporary Redirect", "Like 302, but the method and body must not change."),
    308: ("Permanent Redirect", "Like 301, but the method and body must not change."),
    400: ("Bad Request", "Server cannot process the request due to client error."),
    401: ("Unauthorized", "Authentication required. Include valid credentials."),
    402: ("Payment Required", "Reserved for future use (sometimes used for paywalls)."),
    403: ("Forbidden", "Server understood but refuses to authorize the request."),
    404: ("Not Found", "Server cannot find the requested resource."),
    405: ("Method Not Allowed", "HTTP method is not allowed for this resource."),
    406: ("Not Acceptable", "No content matching Accept headers found."),
    407: ("Proxy Authentication Required", "Authentication with the proxy is required."),
    408: ("Request Timeout", "Server timed out waiting for the request."),
    409: ("Conflict", "Request conflicts with the current state of the resource."),
    410: ("Gone", "Resource is permanently gone (unlike 404, this is intentional)."),
    411: ("Length Required", "Server requires Content-Length header."),
    412: ("Precondition Failed", "Preconditions in request headers were not met."),
    413: ("Payload Too Large", "Request body is larger than the server will accept."),
    414: ("URI Too Long", "Request URI is longer than the server will interpret."),
    415: ("Unsupported Media Type", "Media format of the request is not supported."),
    416: ("Range Not Satisfiable", "Range specified in request cannot be fulfilled."),
    417: ("Expectation Failed", "Expect header requirements cannot be met."),
    418: ("I'm a Teapot", "Server refuses to brew coffee because it's a teapot (RFC 2324)."),
    421: ("Misdirected Request", "Request was directed at a server unable to respond."),
    422: ("Unprocessable Entity", "Request was well-formed but has semantic errors (WebDAV)."),
    423: ("Locked", "Resource is locked (WebDAV)."),
    424: ("Failed Dependency", "Request failed due to a previous request failure (WebDAV)."),
    425: ("Too Early", "Server unwilling to risk processing a request that might be replayed."),
    426: ("Upgrade Required", "Client should switch to a different protocol (e.g., TLS)."),
    428: ("Precondition Required", "Origin server requires the request to be conditional."),
    429: ("Too Many Requests", "Rate limited. Slow down and retry after the specified time."),
    431: ("Request Header Fields Too Large", "Request headers are too large."),
    451: ("Unavailable For Legal Reasons", "Resource blocked for legal reasons (censorship, DMCA)."),
    500: ("Internal Server Error", "Server encountered an unexpected error."),
    501: ("Not Implemented", "Server does not support the requested functionality."),
    502: ("Bad Gateway", "Server acting as gateway received an invalid response."),
    503: ("Service Unavailable", "Server is down for maintenance or overloaded."),
    504: ("Gateway Timeout", "Server acting as gateway didn't get a timely response."),
    505: ("HTTP Version Not Supported", "HTTP version in request is not supported."),
    506: ("Variant Also Negotiates", "Content negotiation resulted in a circular reference."),
    507: ("Insufficient Storage", "Server cannot store the representation (WebDAV)."),
    508: ("Loop Detected", "Infinite loop detected while processing the request (WebDAV)."),
    510: ("Not Extended", "Further extensions to the request are required."),
    511: ("Network Authentication Required", "Client needs to authenticate for network access (captive portal)."),
}

SECURITY_HEADERS = {
    "strict-transport-security": ("HSTS", "Forces HTTPS connections. Recommended: max-age=31536000; includeSubDomains"),
    "content-security-policy": ("CSP", "Controls resource loading. Prevents XSS and injection attacks."),
    "x-content-type-options": ("X-CTO", "Prevents MIME sniffing. Should be: nosniff"),
    "x-frame-options": ("XFO", "Prevents clickjacking. Should be: DENY or SAMEORIGIN"),
    "x-xss-protection": ("X-XSS", "Legacy XSS filter. Modern browsers use CSP instead."),
    "referrer-policy": ("Referrer", "Controls how much referrer info is sent with requests."),
    "permissions-policy": ("Permissions", "Controls browser feature access (camera, mic, geolocation)."),
    "cross-origin-opener-policy": ("COOP", "Isolates browsing context from cross-origin documents."),
    "cross-origin-resource-policy": ("CORP", "Controls which origins can load the resource."),
    "cross-origin-embedder-policy": ("COEP", "Requires resources to opt-in to being loaded cross-origin."),
}


def cmd_lookup(args):
    """Look up an HTTP status code."""
    code = args.code

    if code == 0:
        # Show all codes
        current_group = None
        for c in sorted(STATUS_CODES.keys()):
            group = c // 100
            if group != current_group:
                current_group = group
                labels = {1: "Informational", 2: "Success", 3: "Redirection", 4: "Client Error", 5: "Server Error"}
                print(f"\n{group}xx — {labels.get(group, 'Unknown')}")
                print("-" * 50)
            name, desc = STATUS_CODES[c]
            print(f"  {c}  {name}")
        return

    if code in STATUS_CODES:
        name, desc = STATUS_CODES[code]
        group = code // 100
        labels = {1: "Informational", 2: "Success", 3: "Redirection", 4: "Client Error", 5: "Server Error"}

        if args.json:
            print(json.dumps({"code": code, "name": name, "description": desc, "category": labels.get(group, "Unknown")}))
            return

        print(f"HTTP {code} — {name}")
        print(f"Category: {labels.get(group, 'Unknown')} ({group}xx)")
        print(f"\n{desc}")
    else:
        print(f"Unknown status code: {code}", file=sys.stderr)
        # Show nearest codes
        nearby = [c for c in STATUS_CODES if abs(c - code) <= 5]
        if nearby:
            print(f"Did you mean: {', '.join(str(c) for c in nearby)}?")
        sys.exit(1)


def cmd_search(args):
    """Search status codes by keyword."""
    query = args.query.lower()
    matches = []
    for code, (name, desc) in STATUS_CODES.items():
        if query in name.lower() or query in desc.lower() or query == str(code):
            matches.append((code, name, desc))

    if not matches:
        print(f"No status codes matching '{args.query}'")
        sys.exit(0)

    if args.json:
        print(json.dumps([{"code": c, "name": n, "description": d} for c, n, d in matches], indent=2))
        return

    print(f"Status codes matching '{args.query}':")
    print("-" * 60)
    for code, name, desc in matches:
        print(f"  {code}  {name}")
        print(f"       {desc}")


def cmd_check(args):
    """Check a URL's response headers."""
    url = args.url
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        ctx = ssl.create_default_context()
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", "http-status-ref/1.0")
        resp = urllib.request.urlopen(req, timeout=10, context=ctx)
        status = resp.status
        headers = dict(resp.headers)
    except urllib.error.HTTPError as e:
        status = e.code
        headers = dict(e.headers)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps({"url": url, "status": status, "headers": headers}, indent=2))
        return

    name, desc = STATUS_CODES.get(status, ("Unknown", ""))
    print(f"URL:    {url}")
    print(f"Status: {status} {name}")
    print()

    if args.security:
        print("Security Headers Audit:")
        print("-" * 60)
        present = 0
        for header_name, (short, explanation) in SECURITY_HEADERS.items():
            value = None
            for h, v in headers.items():
                if h.lower() == header_name:
                    value = v
                    break
            if value:
                present += 1
                print(f"  ✓ {short:<14} {value[:60]}")
            else:
                print(f"  ✗ {short:<14} MISSING — {explanation}")
        score = present / len(SECURITY_HEADERS) * 100
        print(f"\nSecurity score: {present}/{len(SECURITY_HEADERS)} ({score:.0f}%)")
    else:
        print("Response Headers:")
        print("-" * 60)
        for h, v in headers.items():
            print(f"  {h}: {v[:80]}")


def main():
    parser = argparse.ArgumentParser(description="HTTP status code reference and URL header analyzer")
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # lookup
    p_lookup = sub.add_parser("lookup", help="Look up an HTTP status code (use 0 to list all)")
    p_lookup.add_argument("code", type=int, help="HTTP status code (or 0 for all)")
    p_lookup.add_argument("--json", action="store_true", help="Output as JSON")
    p_lookup.set_defaults(func=cmd_lookup)

    # search
    p_search = sub.add_parser("search", help="Search status codes by keyword")
    p_search.add_argument("query", help="Keyword to search (e.g., 'redirect', 'cache', 'auth')")
    p_search.add_argument("--json", action="store_true", help="Output as JSON")
    p_search.set_defaults(func=cmd_search)

    # check
    p_check = sub.add_parser("check", help="Check a URL's response status and headers")
    p_check.add_argument("url", help="URL to check (https:// added if missing)")
    p_check.add_argument("--security", action="store_true", help="Audit security headers")
    p_check.add_argument("--json", action="store_true", help="Output as JSON")
    p_check.set_defaults(func=cmd_check)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)
    args.func(args)


if __name__ == "__main__":
    main()
