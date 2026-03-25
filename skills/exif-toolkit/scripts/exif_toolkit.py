#!/usr/bin/env python3
"""Read, strip, and inspect EXIF metadata from image files.

Requires Pillow (auto-installed if missing).
"""

import argparse
import json
import os
import sys
import subprocess

try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
except ImportError:
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--user", "--break-system-packages", "Pillow", "-q"],
        stderr=subprocess.DEVNULL,
    )
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".webp", ".heic", ".heif"}


def get_exif_data(image_path):
    """Extract EXIF data as a readable dict."""
    if not os.path.isfile(image_path):
        print(f"Error: File not found: {image_path}", file=sys.stderr)
        sys.exit(1)
    img = Image.open(image_path)
    exif_raw = img.getexif()
    if not exif_raw:
        return {}

    exif_data = {}
    for tag_id, value in exif_raw.items():
        tag_name = TAGS.get(tag_id, f"Unknown({tag_id})")
        # Handle bytes and other non-serializable types
        if isinstance(value, bytes):
            try:
                value = value.decode("utf-8", errors="replace")
            except Exception:
                value = f"<bytes: {len(value)} bytes>"
        elif isinstance(value, (tuple, list)):
            value = [str(v) for v in value]
        exif_data[tag_name] = value

    # Parse GPS info specially
    gps_ifd = exif_raw.get_ifd(0x8825)
    if gps_ifd:
        gps_data = {}
        for key, val in gps_ifd.items():
            tag_name = GPSTAGS.get(key, f"GPSUnknown({key})")
            if isinstance(val, bytes):
                try:
                    val = val.decode("utf-8", errors="replace")
                except Exception:
                    val = f"<bytes: {len(val)} bytes>"
            gps_data[tag_name] = val
        exif_data["GPSInfo"] = gps_data

    return exif_data


def convert_to_degrees(value):
    """Convert GPS coordinates to degrees."""
    try:
        d = float(value[0])
        m = float(value[1])
        s = float(value[2])
        return d + (m / 60.0) + (s / 3600.0)
    except (TypeError, IndexError, ValueError):
        return None


def get_gps_coords(image_path):
    """Extract GPS coordinates from an image."""
    img = Image.open(image_path)
    exif_raw = img.getexif()
    if not exif_raw:
        return None

    gps_ifd = exif_raw.get_ifd(0x8825)
    if not gps_ifd:
        return None

    gps_data = {}
    for key, val in gps_ifd.items():
        tag_name = GPSTAGS.get(key, key)
        gps_data[tag_name] = val

    lat = gps_data.get("GPSLatitude")
    lat_ref = gps_data.get("GPSLatitudeRef")
    lon = gps_data.get("GPSLongitude")
    lon_ref = gps_data.get("GPSLongitudeRef")

    if not all([lat, lat_ref, lon, lon_ref]):
        return None

    lat_deg = convert_to_degrees(lat)
    lon_deg = convert_to_degrees(lon)

    if lat_deg is None or lon_deg is None:
        return None

    if lat_ref == "S":
        lat_deg = -lat_deg
    if lon_ref == "W":
        lon_deg = -lon_deg

    return lat_deg, lon_deg


def make_serializable(obj):
    """Convert EXIF data to JSON-serializable format."""
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [make_serializable(v) for v in obj]
    elif isinstance(obj, bytes):
        return f"<bytes: {len(obj)} bytes>"
    elif isinstance(obj, (int, float, str, bool, type(None))):
        return obj
    else:
        return str(obj)


def cmd_read(args):
    """Read and display EXIF data."""
    exif = get_exif_data(args.image)
    if not exif:
        print(f"No EXIF data found in: {args.image}")
        return

    if args.tags:
        exif = {k: v for k, v in exif.items() if k in args.tags}
        if not exif:
            print(f"None of the requested tags found in: {args.image}")
            return

    if args.json:
        print(json.dumps(make_serializable(exif), indent=2, default=str))
    else:
        print(f"EXIF data for: {args.image}\n{'=' * 50}")
        for tag, value in sorted(exif.items()):
            if isinstance(value, dict):
                print(f"  {tag}:")
                for k, v in value.items():
                    print(f"    {k}: {v}")
            else:
                print(f"  {tag}: {value}")


def cmd_strip(args):
    """Strip EXIF data from an image."""
    if not os.path.isfile(args.image):
        print(f"Error: File not found: {args.image}", file=sys.stderr)
        sys.exit(1)
    img = Image.open(args.image)

    # Create a new image without EXIF
    if hasattr(img, "get_flattened_data"):
        data = list(img.get_flattened_data())
    else:
        data = list(img.getdata())
    clean_img = Image.new(img.mode, img.size)
    clean_img.putdata(data)

    if args.inplace:
        output = args.image
    elif args.output:
        output = args.output
    else:
        base, ext = os.path.splitext(args.image)
        output = f"{base}_clean{ext}"

    # Determine format from extension
    fmt = None
    ext = os.path.splitext(output)[1].lower()
    fmt_map = {".jpg": "JPEG", ".jpeg": "JPEG", ".png": "PNG", ".tiff": "TIFF",
               ".tif": "TIFF", ".webp": "WebP"}
    fmt = fmt_map.get(ext, "JPEG")

    clean_img.save(output, format=fmt)
    print(f"Stripped EXIF → {output}")


def cmd_strip_dir(args):
    """Batch strip EXIF from all images in a directory."""
    src_dir = args.directory
    out_dir = args.output or os.path.join(src_dir, "stripped")
    os.makedirs(out_dir, exist_ok=True)

    count = 0
    for root, dirs, files in os.walk(src_dir):
        if not args.recursive and root != src_dir:
            continue
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext not in IMAGE_EXTENSIONS:
                continue
            src_path = os.path.join(root, fname)
            # Preserve relative structure
            rel = os.path.relpath(src_path, src_dir)
            dst_path = os.path.join(out_dir, rel)
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)

            try:
                img = Image.open(src_path)
                if hasattr(img, "get_flattened_data"):
                    data = list(img.get_flattened_data())
                else:
                    data = list(img.getdata())
                clean_img = Image.new(img.mode, img.size)
                clean_img.putdata(data)
                fmt_map = {".jpg": "JPEG", ".jpeg": "JPEG", ".png": "PNG",
                           ".tiff": "TIFF", ".tif": "TIFF", ".webp": "WebP"}
                fmt = fmt_map.get(ext, "JPEG")
                clean_img.save(dst_path, format=fmt)
                count += 1
            except Exception as e:
                print(f"  Error processing {src_path}: {e}", file=sys.stderr)

    print(f"Stripped EXIF from {count} image(s) → {out_dir}")


def cmd_gps(args):
    """Show GPS coordinates from an image."""
    coords = get_gps_coords(args.image)
    if coords:
        lat, lon = coords
        print(f"GPS Coordinates for: {args.image}")
        print(f"  Latitude:  {lat:.6f}")
        print(f"  Longitude: {lon:.6f}")
        print(f"  Google Maps: https://maps.google.com/?q={lat},{lon}")
    else:
        print(f"No GPS data found in: {args.image}")


def main():
    parser = argparse.ArgumentParser(
        description="Read, strip, and inspect EXIF metadata from images."
    )
    sub = parser.add_subparsers(dest="command", help="Command to run")

    # read
    p_read = sub.add_parser("read", help="Display EXIF metadata")
    p_read.add_argument("image", help="Image file path")
    p_read.add_argument("--tags", nargs="+", help="Filter specific EXIF tags")
    p_read.add_argument("--json", action="store_true", help="Output as JSON")

    # strip
    p_strip = sub.add_parser("strip", help="Remove EXIF data from an image")
    p_strip.add_argument("image", help="Image file path")
    p_strip.add_argument("--output", "-o", help="Output file path")
    p_strip.add_argument("--inplace", action="store_true", help="Modify in-place")

    # strip-dir
    p_sdir = sub.add_parser("strip-dir", help="Batch strip EXIF from directory")
    p_sdir.add_argument("directory", help="Directory with images")
    p_sdir.add_argument("--output", "-o", help="Output directory")
    p_sdir.add_argument("--recursive", "-r", action="store_true", help="Process subdirs")

    # gps
    p_gps = sub.add_parser("gps", help="Extract GPS coordinates")
    p_gps.add_argument("image", help="Image file path")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    dispatch = {
        "read": cmd_read,
        "strip": cmd_strip,
        "strip-dir": cmd_strip_dir,
        "gps": cmd_gps,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
