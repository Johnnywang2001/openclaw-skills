#!/usr/bin/env python3
"""Network speed test using public endpoints. Measures download speed, upload speed, and latency."""

import argparse
import sys
import time
import json
import urllib.request
import urllib.error
import ssl
import socket
import tempfile
import os


# Public test endpoints (no auth required)
DOWNLOAD_URLS = [
    ("Cloudflare", "https://speed.cloudflare.com/__down?bytes=10000000"),
    ("Cloudflare-25M", "https://speed.cloudflare.com/__down?bytes=25000000"),
]

UPLOAD_URL = "https://speed.cloudflare.com/__up"

PING_HOSTS = [
    ("Cloudflare DNS", "1.1.1.1", 443),
    ("Google DNS", "8.8.8.8", 443),
    ("Quad9 DNS", "9.9.9.9", 443),
]


def create_ssl_context():
    ctx = ssl.create_default_context()
    return ctx


def measure_latency(host, port, count=5):
    """Measure TCP connection latency (ping-like)."""
    times = []
    for _ in range(count):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            start = time.monotonic()
            sock.connect((host, port))
            elapsed = (time.monotonic() - start) * 1000  # ms
            times.append(elapsed)
            sock.close()
        except Exception:
            pass
        time.sleep(0.1)

    if not times:
        return None
    return {
        "min_ms": round(min(times), 2),
        "avg_ms": round(sum(times) / len(times), 2),
        "max_ms": round(max(times), 2),
        "samples": len(times),
    }


def measure_download(url, label, timeout=30):
    """Measure download speed."""
    ctx = create_ssl_context()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "net-speed-test/1.0"})
        start = time.monotonic()
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            data = resp.read()
        elapsed = time.monotonic() - start
        bytes_received = len(data)
        speed_mbps = (bytes_received * 8) / (elapsed * 1_000_000)
        return {
            "label": label,
            "bytes": bytes_received,
            "seconds": round(elapsed, 3),
            "mbps": round(speed_mbps, 2),
        }
    except Exception as e:
        return {"label": label, "error": str(e)}


def measure_upload(url, size_bytes=2_000_000, timeout=30):
    """Measure upload speed by POSTing random data."""
    ctx = create_ssl_context()
    data = os.urandom(size_bytes)
    try:
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "User-Agent": "net-speed-test/1.0",
                "Content-Type": "application/octet-stream",
            },
            method="POST",
        )
        start = time.monotonic()
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            resp.read()
        elapsed = time.monotonic() - start
        speed_mbps = (size_bytes * 8) / (elapsed * 1_000_000)
        return {
            "bytes_sent": size_bytes,
            "seconds": round(elapsed, 3),
            "mbps": round(speed_mbps, 2),
        }
    except Exception as e:
        return {"error": str(e)}


def format_speed(mbps):
    if mbps >= 1000:
        return f"{mbps / 1000:.2f} Gbps"
    return f"{mbps:.2f} Mbps"


def main():
    parser = argparse.ArgumentParser(
        description="Network speed test. Measures download speed, upload speed, and latency using public endpoints."
    )
    parser.add_argument("--download-only", action="store_true", help="Only test download speed")
    parser.add_argument("--upload-only", action="store_true", help="Only test upload speed")
    parser.add_argument("--ping-only", action="store_true", help="Only test latency")
    parser.add_argument("--json", action="store_true", dest="output_json", help="Output as JSON")
    parser.add_argument("--quick", action="store_true", help="Quick test (smaller download, fewer pings)")
    args = parser.parse_args()

    run_all = not (args.download_only or args.upload_only or args.ping_only)
    results = {}

    # Latency
    if run_all or args.ping_only:
        if not args.output_json:
            print("Testing latency...")
        ping_results = []
        hosts = PING_HOSTS[:2] if args.quick else PING_HOSTS
        ping_count = 3 if args.quick else 5
        for label, host, port in hosts:
            r = measure_latency(host, port, count=ping_count)
            if r:
                r["host"] = label
                ping_results.append(r)
                if not args.output_json:
                    print(f"  {label}: {r['avg_ms']:.1f} ms (min {r['min_ms']:.1f}, max {r['max_ms']:.1f})")
            else:
                if not args.output_json:
                    print(f"  {label}: timeout")
        results["latency"] = ping_results

    # Download
    if run_all or args.download_only:
        if not args.output_json:
            print("Testing download speed...")
        dl_tests = DOWNLOAD_URLS[:1] if args.quick else DOWNLOAD_URLS
        dl_results = []
        for label, url in dl_tests:
            r = measure_download(url, label)
            dl_results.append(r)
            if not args.output_json:
                if "error" in r:
                    print(f"  {label}: ERROR - {r['error']}")
                else:
                    print(f"  {label}: {format_speed(r['mbps'])} ({r['bytes'] / 1_000_000:.1f} MB in {r['seconds']}s)")
        results["download"] = dl_results

    # Upload
    if run_all or args.upload_only:
        if not args.output_json:
            print("Testing upload speed...")
        upload_size = 1_000_000 if args.quick else 2_000_000
        r = measure_upload(UPLOAD_URL, size_bytes=upload_size)
        results["upload"] = r
        if not args.output_json:
            if "error" in r:
                print(f"  Upload: ERROR - {r['error']}")
            else:
                print(f"  Upload: {format_speed(r['mbps'])} ({r['bytes_sent'] / 1_000_000:.1f} MB in {r['seconds']}s)")

    # Summary
    if not args.output_json and run_all:
        print("\n--- Summary ---")
        if results.get("latency"):
            avg_latency = sum(p["avg_ms"] for p in results["latency"]) / len(results["latency"])
            print(f"  Latency:  {avg_latency:.1f} ms (avg)")
        if results.get("download"):
            best_dl = max((d for d in results["download"] if "mbps" in d), key=lambda x: x["mbps"], default=None)
            if best_dl:
                print(f"  Download: {format_speed(best_dl['mbps'])}")
        if results.get("upload") and "mbps" in results["upload"]:
            print(f"  Upload:   {format_speed(results['upload']['mbps'])}")

    if args.output_json:
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
