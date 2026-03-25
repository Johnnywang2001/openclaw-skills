# File Hasher

Compute, verify, and compare file hashes using MD5, SHA-1, SHA-256, SHA-512, and more. Use when checking file integrity, verifying downloads against expected checksums, comparing files for equality, generating checksums for directories, hashing strings, or validating checksum files (sha256sum/md5sum format). Supports BSD and standard output formats, JSON output, multi-algorithm hashing, and recursive directory scanning. No external dependencies.

## Installation

```bash
clawhub install file-hasher
```

## Usage

```bash
# Hash a file (SHA-256)
python3 scripts/file_hasher.py hash myfile.txt
# Verify a download
python3 scripts/file_hasher.py verify image.iso -e abc123def456...
```

## Requirements

- Python 3 (no external dependencies)

## License

MIT
