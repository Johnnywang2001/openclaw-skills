# Color Toolkit

Convert, analyze, and generate colors from the CLI. Supports HEX, RGB, HSL, HSV, CMYK conversion, WCAG contrast ratio checking (AA/AAA compliance), palette generation (complementary, analogous, triadic, split-complementary, monochromatic), color manipulation (lighten/darken/saturate/desaturate), mixing, random generation, and CSS named color lookup. Use when the user needs color conversions, accessibility contrast checks, palette generation, or color manipulation. Zero external dependencies.

## Installation

```bash
clawhub install color-toolkit
```

## Usage

```bash
# Convert between formats (accepts #hex, rgb(), hsl(), CSS names, or r,g,b)
python3 scripts/color_toolkit.py convert '#ff6347'
python3 scripts/color_toolkit.py convert tomato
python3 scripts/color_toolkit.py convert 'rgb(52, 152, 219)'
```

## Requirements

- Python 3 (no external dependencies)

## License

MIT
