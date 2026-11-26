#!/usr/bin/env python3
"""Write one robot pickup line to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The line is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, and enforces the
competition gate: a single line of 1 to 200 characters, not only
white space.
"""

import os
import sys
from pathlib import Path

LINE = (
    "I don't have a heart, just a battery, and it has been at 100% "
    "since you walked in. My cooling fan finds that very suspicious."
)

MIN_CHARS = 1
MAX_CHARS = 200
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate: one line, 1 to 200 chars.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"line is {chars} characters, outside 1-200")
    if not text.strip():
        raise ValueError("line is only white space")
    if "\n" in text:
        raise ValueError("line must be a single line")
    return chars


def write_entry(text: str, path: Path) -> int:
    """Write the line to the output target, creating parent dirs as needed.

    Writes the text exactly as given (no trailing newline added), and
    returns the number of characters written.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return len(text)


def main() -> int:
    try:
        chars = validate(LINE)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path()
    written = write_entry(LINE, path)
    print(f"wrote {written} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
