# EXIF Toolkit

Read, write, and strip EXIF/image metadata from photos and images. Use when asked to view image metadata, check photo GPS coordinates, remove EXIF data for privacy, inspect camera settings, or analyze image properties. Supports JPEG, PNG, TIFF, WebP, and HEIC.

## Installation

```bash
clawhub install exif-toolkit
```

## Usage

```bash
# View all EXIF data from an image
python3 scripts/exif_toolkit.py read photo.jpg
# View specific tags
python3 scripts/exif_toolkit.py read photo.jpg --tags Make Model DateTime GPSInfo
```

## Requirements

- Python 3.7+
- Pillow (auto-installed)

## License

MIT
