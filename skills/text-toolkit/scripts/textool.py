#!/usr/bin/env python3
"""Text manipulation toolkit: case conversion, counting, slugify, reverse, truncate, wrap, and more."""

import argparse
import sys
import re
import json
import unicodedata


def to_slug(text):
    """Convert text to URL-friendly slug."""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def to_camel(text):
    """Convert to camelCase."""
    words = re.split(r"[\s_\-]+", text.strip())
    if not words:
        return ""
    return words[0].lower() + "".join(w.capitalize() for w in words[1:])


def to_pascal(text):
    """Convert to PascalCase."""
    words = re.split(r"[\s_\-]+", text.strip())
    return "".join(w.capitalize() for w in words)


def to_snake(text):
    """Convert to snake_case."""
    # Handle camelCase / PascalCase input
    text = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", text)
    text = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", text)
    text = re.sub(r"[\s\-]+", "_", text)
    return text.lower().strip("_")


def to_kebab(text):
    """Convert to kebab-case."""
    return to_snake(text).replace("_", "-")


def to_constant(text):
    """Convert to CONSTANT_CASE."""
    return to_snake(text).upper()


def to_title(text):
    """Smart title case (lowercase minor words)."""
    minor = {"a", "an", "the", "and", "but", "or", "nor", "for", "in", "on", "at", "to", "by", "of", "with", "is"}
    words = text.split()
    result = []
    for i, word in enumerate(words):
        if i == 0 or word.lower() not in minor:
            result.append(word.capitalize())
        else:
            result.append(word.lower())
    return " ".join(result)


def count_stats(text):
    """Count characters, words, lines, sentences, paragraphs."""
    chars = len(text)
    chars_no_space = len(text.replace(" ", "").replace("\n", "").replace("\t", ""))
    words = len(text.split())
    lines = text.count("\n") + (1 if text and not text.endswith("\n") else 0)
    sentences = len(re.findall(r"[.!?]+(?:\s|$)", text))
    paragraphs = len([p for p in text.split("\n\n") if p.strip()])
    return {
        "characters": chars,
        "characters_no_spaces": chars_no_space,
        "words": words,
        "lines": lines,
        "sentences": sentences,
        "paragraphs": paragraphs,
    }


def reverse_text(text):
    return text[::-1]


def reverse_words(text):
    return " ".join(text.split()[::-1])


def truncate_text(text, length, suffix="..."):
    if len(text) <= length:
        return text
    return text[: length - len(suffix)] + suffix


def wrap_text(text, width=80):
    """Simple word wrap."""
    lines = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            lines.append("")
            continue
        words = paragraph.split()
        current = ""
        for word in words:
            if current and len(current) + 1 + len(word) > width:
                lines.append(current)
                current = word
            else:
                current = f"{current} {word}" if current else word
        if current:
            lines.append(current)
    return "\n".join(lines)


def extract_emails(text):
    return re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)


def extract_urls(text):
    return re.findall(r"https?://[^\s<>\"']+", text)


def remove_duplicates(text):
    """Remove duplicate lines."""
    seen = set()
    result = []
    for line in text.splitlines():
        if line not in seen:
            seen.add(line)
            result.append(line)
    return "\n".join(result)


def sort_lines(text, reverse=False):
    lines = text.splitlines()
    return "\n".join(sorted(lines, reverse=reverse))


def get_input(args_text, read_stdin=True):
    """Get input text from args or stdin."""
    if args_text:
        return " ".join(args_text)
    if read_stdin and not sys.stdin.isatty():
        return sys.stdin.read()
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Text manipulation toolkit: case conversion, stats, slugify, extract, and more."
    )
    subparsers = parser.add_subparsers(dest="command")

    # Case conversions
    for cmd, help_text in [
        ("upper", "Convert to UPPERCASE"),
        ("lower", "Convert to lowercase"),
        ("title", "Convert to Smart Title Case"),
        ("slug", "Convert to url-friendly-slug"),
        ("camel", "Convert to camelCase"),
        ("pascal", "Convert to PascalCase"),
        ("snake", "Convert to snake_case"),
        ("kebab", "Convert to kebab-case"),
        ("constant", "Convert to CONSTANT_CASE"),
    ]:
        p = subparsers.add_parser(cmd, help=help_text)
        p.add_argument("text", nargs="*", help="Input text (or pipe via stdin)")

    # Count/stats
    p_count = subparsers.add_parser("count", help="Count chars, words, lines, sentences")
    p_count.add_argument("text", nargs="*")
    p_count.add_argument("--json", action="store_true", dest="output_json")

    # Reverse
    p_rev = subparsers.add_parser("reverse", help="Reverse text or words")
    p_rev.add_argument("text", nargs="*")
    p_rev.add_argument("--words", action="store_true", help="Reverse word order instead of characters")

    # Truncate
    p_trunc = subparsers.add_parser("truncate", help="Truncate text to length")
    p_trunc.add_argument("length", type=int, help="Max length")
    p_trunc.add_argument("text", nargs="*")
    p_trunc.add_argument("--suffix", default="...", help="Truncation suffix (default: ...)")

    # Wrap
    p_wrap = subparsers.add_parser("wrap", help="Word wrap text")
    p_wrap.add_argument("text", nargs="*")
    p_wrap.add_argument("--width", type=int, default=80, help="Line width (default: 80)")

    # Extract
    p_extract = subparsers.add_parser("extract", help="Extract emails or URLs from text")
    p_extract.add_argument("type", choices=["emails", "urls"], help="What to extract")
    p_extract.add_argument("text", nargs="*")

    # Dedup
    p_dedup = subparsers.add_parser("dedup", help="Remove duplicate lines")
    p_dedup.add_argument("text", nargs="*")

    # Sort
    p_sort = subparsers.add_parser("sort", help="Sort lines alphabetically")
    p_sort.add_argument("text", nargs="*")
    p_sort.add_argument("--reverse", "-r", action="store_true")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Get input text
    text_args = getattr(args, "text", None)
    text = get_input(text_args)

    if text is None:
        print("Error: No input text provided. Pass as argument or pipe via stdin.", file=sys.stderr)
        sys.exit(1)

    # Execute command
    if args.command == "upper":
        print(text.upper())
    elif args.command == "lower":
        print(text.lower())
    elif args.command == "title":
        print(to_title(text))
    elif args.command == "slug":
        print(to_slug(text))
    elif args.command == "camel":
        print(to_camel(text))
    elif args.command == "pascal":
        print(to_pascal(text))
    elif args.command == "snake":
        print(to_snake(text))
    elif args.command == "kebab":
        print(to_kebab(text))
    elif args.command == "constant":
        print(to_constant(text))
    elif args.command == "count":
        stats = count_stats(text)
        if getattr(args, "output_json", False):
            print(json.dumps(stats, indent=2))
        else:
            for k, v in stats.items():
                print(f"  {k.replace('_', ' ').title()}: {v}")
    elif args.command == "reverse":
        if args.words:
            print(reverse_words(text))
        else:
            print(reverse_text(text))
    elif args.command == "truncate":
        print(truncate_text(text, args.length, args.suffix))
    elif args.command == "wrap":
        print(wrap_text(text, args.width))
    elif args.command == "extract":
        if args.type == "emails":
            for e in extract_emails(text):
                print(e)
        else:
            for u in extract_urls(text):
                print(u)
    elif args.command == "dedup":
        print(remove_duplicates(text))
    elif args.command == "sort":
        print(sort_lines(text, reverse=args.reverse))


if __name__ == "__main__":
    main()
