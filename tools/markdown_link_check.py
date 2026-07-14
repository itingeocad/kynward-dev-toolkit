#!/usr/bin/env python3
"""Check local Markdown links in public documentation files.

This tool is intentionally dependency-free. It scans Markdown files, extracts
inline local links, and reports links that point to missing repository files.
External URLs, anchors-only links, mail links, and image links are ignored.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable

LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
EXTERNAL_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "tel:",
)


def iter_markdown_files(root: Path) -> Iterable[Path]:
    """Yield Markdown files below the given root directory."""
    for path in sorted(root.rglob("*.md")):
        if any(part.startswith(".") for part in path.relative_to(root).parts):
            continue
        yield path


def normalize_link_target(raw_target: str) -> str:
    """Remove optional Markdown title, query string, and anchor from a target."""
    target = raw_target.strip()
    if " " in target and not target.startswith("<"):
        target = target.split(" ", 1)[0]
    target = target.strip("<>")
    target = target.split("?", 1)[0]
    target = target.split("#", 1)[0]
    return target


def should_ignore_target(target: str) -> bool:
    """Return whether a link target is outside local file validation scope."""
    if not target:
        return True
    lowered = target.lower()
    if lowered.startswith(EXTERNAL_PREFIXES):
        return True
    if lowered.startswith("#"):
        return True
    return False


def resolve_target(markdown_file: Path, target: str) -> Path:
    """Resolve a local link target relative to a Markdown file."""
    return (markdown_file.parent / target).resolve()


def check_file(root: Path, markdown_file: Path) -> list[str]:
    """Return validation errors for one Markdown file."""
    errors: list[str] = []
    text = markdown_file.read_text(encoding="utf-8")

    for line_number, line in enumerate(text.splitlines(), start=1):
        for match in LINK_PATTERN.finditer(line):
            target = normalize_link_target(match.group(1))
            if should_ignore_target(target):
                continue

            resolved = resolve_target(markdown_file, target)
            if not resolved.exists():
                rel_file = markdown_file.relative_to(root)
                errors.append(f"{rel_file}:{line_number}: missing local link target: {target}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Check local Markdown links.")
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

    all_errors: list[str] = []
    for markdown_file in iter_markdown_files(root):
        all_errors.extend(check_file(root, markdown_file))

    if all_errors:
        for error in all_errors:
            print(error)
        return 1

    print("Markdown local link check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
