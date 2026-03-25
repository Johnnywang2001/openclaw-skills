---
name: exif-toolkit
description: Read, write, and strip EXIF/image metadata from photos and images. Use when asked to view image metadata, check photo GPS coordinates, remove EXIF data for privacy, inspect camera settings, or analyze image properties. Supports JPEG, PNG, TIFF, WebP, and HEIC. Also triggers on "photo info", "image details", "strip metadata", "where was this photo taken", or "camera settings".
---

# exif-toolkit

Read, edit, and strip EXIF metadata from image files using Python's Pillow library.

## Quick Start

```bash
# View all EXIF data from an image
python3 scripts/exif_toolkit.py read photo.jpg

# View specific tags
python3 scripts/exif_toolkit.py read photo.jpg --tags Make Model DateTime GPSInfo

# Strip all EXIF data (privacy-safe copy)
python3 scripts/exif_toolkit.py strip photo.jpg --output clean_photo.jpg

# Strip EXIF in-place
python3 scripts/exif_toolkit.py strip photo.jpg --inplace

# Batch strip all images in a directory
python3 scripts/exif_toolkit.py strip-dir ./photos --output ./clean_photos

# Export metadata as JSON
python3 scripts/exif_toolkit.py read photo.jpg --json

# Show GPS coordinates (if present)
python3 scripts/exif_toolkit.py gps photo.jpg
```

## Commands

| Command | Description |
|---------|-------------|
| `read` | Display EXIF metadata from an image |
| `strip` | Remove all EXIF data from an image |
| `strip-dir` | Batch strip EXIF from all images in a directory |
| `gps` | Extract and display GPS coordinates with map link |

## Options

| Flag | Description |
|------|-------------|
| `--tags TAG ...` | Filter specific EXIF tags (with `read`) |
| `--json` | Output as JSON (with `read`) |
| `--output FILE` | Output file path (with `strip`) |
| `--inplace` | Modify file in-place (with `strip`) |
| `--recursive` | Process subdirectories (with `strip-dir`) |

## Requirements

- Python 3.8+
- Pillow (`pip install Pillow`) — auto-installed if missing
