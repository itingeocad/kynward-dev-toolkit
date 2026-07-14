#!/usr/bin/env python3
"""Check basic Markdown structure for public documentation files.

This tool is intentionally small and dependency-free. It verifies that Markdown
files have a top-level heading and do not contain tab-indented lines. It is a
starting point for public documentation validation and can be extended later.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable


def iter_markdown_files(root: Path) -> Iterable[Path]:
    """Yield Markdown files below the given root directory."""
    for path in sorted(root.rglob("*.md")):
        if any(part.startswith(".") for part in path.parts):
            continue
        yield path


def check_file(path: Path) -> list[str]:
    """Return a list of validation errors for one Markdown file."""
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if not lines:
        errors.append("file is empty")
        return errors

    first_non_empty = next((line for line in lines if line.strip()), "")
    if not first_non_empty.startswith("# "):
        errors.append("missing top-level '# ' heading")

    for index, line in enumerate(lines, start=1):
        if line.startswith("\t"):
            errors.append(f"line {index}: tab indentation is not allowed")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Check basic Markdown structure.")
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Directory to scan. Defaults to the current directory.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"error: path does not exist: {root}")
        return 2

    had_errors = False
    for path in iter_markdown_files(root):
        errors = check_file(path)
        if errors:
            had_errors = True
            rel_path = path.relative_to(root)
            for error in errors:
                print(f"{rel_path}: {error}")

    if had_errors:
        return 1

    print("Markdown structure check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
