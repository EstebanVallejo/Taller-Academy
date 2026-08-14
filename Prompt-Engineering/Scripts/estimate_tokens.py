#!/usr/bin/env python3
"""Estimate the token count of a text file.

Usage:
    python3 estimate_tokens.py notes.md
    python3 estimate_tokens.py notes.md --exact
    cat notes.md | python3 estimate_tokens.py

The estimate uses the ~4-characters-per-token rule of thumb and needs no
API key. --exact additionally calls the Anthropic count_tokens endpoint,
which requires the `anthropic` package and ANTHROPIC_API_KEY.
"""

import argparse
import sys

# Rule of thumb from the Day 1 theory: a token is roughly four characters
# of English text. Code, non-English text, and unusual formatting tokenize
# less efficiently, so treat this as a planning figure, not a guarantee.
CHARS_PER_TOKEN = 4

DEFAULT_MODEL = "claude-opus-5"


def read_input(path: str | None) -> str:
    """Read from a file, or from stdin when no path is given."""
    if path is None:
        if sys.stdin.isatty():
            sys.exit("No input. Pass a file path or pipe text via stdin.")
        return sys.stdin.read()
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read()
    except FileNotFoundError:
        sys.exit(f"File not found: {path}")
    except UnicodeDecodeError:
        sys.exit(f"Not a UTF-8 text file: {path}")


def exact_token_count(text: str, model: str) -> int:
    """Ask the API for the true token count for this model."""
    try:
        import anthropic
    except ImportError:
        sys.exit("--exact needs the SDK. Run: pip install anthropic")

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment
    try:
        result = client.messages.count_tokens(
            model=model,
            messages=[{"role": "user", "content": text}],
        )
    except anthropic.AuthenticationError:
        sys.exit("Authentication failed. Is ANTHROPIC_API_KEY set correctly?")
    except anthropic.APIError as error:
        sys.exit(f"API error: {error}")
    return result.input_tokens


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Estimate the token count of a text file."
    )
    parser.add_argument("path", nargs="?", help="file to read (default: stdin)")
    parser.add_argument(
        "--exact",
        action="store_true",
        help="also fetch the exact count from the API",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"model to count against (default: {DEFAULT_MODEL})",
    )
    args = parser.parse_args()

    text = read_input(args.path)
    characters = len(text)
    words = len(text.split())
    estimate = characters // CHARS_PER_TOKEN

    label = args.path or "(stdin)"
    print(f"Source:            {label}")
    print(f"Characters:        {characters:,}")
    print(f"Words:             {words:,}")
    print(f"Estimated tokens:  {estimate:,}  (~{CHARS_PER_TOKEN} chars/token)")

    if args.exact:
        actual = exact_token_count(text, args.model)
        print(f"Exact tokens:      {actual:,}  ({args.model})")
        if actual:
            error_pct = (estimate - actual) / actual * 100
            direction = "over" if error_pct > 0 else "under"
            print(f"Estimate was:      {abs(error_pct):.1f}% {direction}")


if __name__ == "__main__":
    main()