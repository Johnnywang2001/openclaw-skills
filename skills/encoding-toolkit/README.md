# Encoding Toolkit

Multi-format encoder, decoder, and hasher supporting Base64, Base64URL, Base32, Hex, URL-encoding, HTML entities, ROT13, Binary, and ASCII85. Also computes MD5, SHA-1, SHA-256, SHA-512, and SHA3-256 hashes. Can auto-detect encoding format. Use when encoding or decoding data, computing file or string hashes, converting between formats, or identifying unknown encoded strings.

## Installation

```bash
clawhub install encoding-toolkit
```

## Usage

```bash
# Encode
python3 scripts/encode_decode.py encode base64 "Hello World"
python3 scripts/encode_decode.py encode url "hello world & goodbye"
python3 scripts/encode_decode.py encode hex "Hello"
```

## Requirements

- Python 3 (no external dependencies)

## License

MIT
