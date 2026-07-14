#!/usr/bin/env python3
"""Unit-style tests for the Markdown structure and local-link checkers.

These tests are intentionally dependency-free (Python standard library only)
so they run anywhere without installing extra packages:

    python3 -m unittest tools.test_markdown_checkers -v

or, from within the ``tools/`` directory:

    python3 -m unittest test_markdown_checkers -v

or simply:

    python3 tools/test_markdown_checkers.py

All fixtures are synthetic Markdown files created in temporary directories.
No private Kynward content, external URLs, or local machine paths are used.
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Make sibling checker modules importable regardless of how this file is run.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from markdown_structure_check import check_file as structure_check  # noqa: E402
from markdown_link_check import check_file as link_check  # noqa: E402


class MarkdownStructureCheckTests(unittest.TestCase):
    """Cover the five expected scenarios for the structure checker."""

    def _write(self, root: Path, name: str, text: str) -> Path:
        path = root / name
        path.write_text(text, encoding="utf-8")
        return path

    def test_valid_markdown_has_no_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(Path(tmp), "valid.md", "# Title\n\nSome public content.\n")
            self.assertEqual(structure_check(path), [])

    def test_missing_top_level_heading_is_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(Path(tmp), "no_heading.md", "Just text, no heading.\n")
            errors = structure_check(path)
            self.assertTrue(
                any("missing top-level '# ' heading" in e for e in errors),
                f"expected missing-heading error, got {errors!r}",
            )

    def test_tab_indentation_is_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(Path(tmp), "tabbed.md", "# Title\n\n\tindented with a tab\n")
            errors = structure_check(path)
            self.assertTrue(
                any("tab indentation is not allowed" in e for e in errors),
                f"expected tab-indentation error, got {errors!r}",
            )

    def test_empty_file_is_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(Path(tmp), "empty.md", "")
            errors = structure_check(path)
            self.assertTrue(
                any("file is empty" in e for e in errors),
                f"expected empty-file error, got {errors!r}",
            )


class MarkdownLinkCheckTests(unittest.TestCase):
    """Cover valid links, broken links, and ignored link kinds."""

    def _root(self, tmp: str) -> Path:
        return Path(tmp)

    def test_broken_local_link_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            md = root / "doc.md"
            md.write_text("[docs](./missing.md)\n", encoding="utf-8")
            errors = link_check(root, md)
            self.assertTrue(
                any("missing local link target" in e for e in errors),
                f"expected broken-link error, got {errors!r}",
            )

    def test_valid_local_link_has_no_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "present.md").write_text("# Present\n", encoding="utf-8")
            md = root / "doc.md"
            md.write_text("[docs](./present.md)\n", encoding="utf-8")
            self.assertEqual(link_check(root, md), [])

    def test_external_url_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            md = root / "doc.md"
            md.write_text("[site](https://example.com/page)\n", encoding="utf-8")
            self.assertEqual(link_check(root, md), [])

    def test_image_link_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            md = root / "doc.md"
            # Even though ./missing.png does not exist, image links are skipped.
            md.write_text("![diagram](./missing.png)\n", encoding="utf-8")
            self.assertEqual(link_check(root, md), [])

    def test_anchor_link_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            md = root / "doc.md"
            md.write_text("[section](#section-heading)\n", encoding="utf-8")
            self.assertEqual(link_check(root, md), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
