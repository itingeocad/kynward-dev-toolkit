# Tools

This directory contains public-safe developer tools for Kynward Dev Toolkit.

Tools in this directory must be:

- generic enough to work without the private Kynward game repository;
- documented with English comments and descriptions;
- safe to publish;
- free of private lore, assets, credentials, or local machine paths.

## Planned tools

- Markdown structure checker.
- Documentation link checker.
- JSON validation helper.
- Smoke-test report helper.

## Usage rule

Each tool should include a short usage example and should fail with clear, actionable error messages.

## Tests

The Markdown checkers have dependency-free unit-style tests (Python standard
library only). Run them from the repository root:

```bash
python3 -m unittest tools.test_markdown_checkers -v
```

or directly:

```bash
python3 tools/test_markdown_checkers.py
```

The tests cover:

- valid Markdown (no errors);
- missing top-level heading (flagged);
- tab indentation (flagged);
- empty file (flagged);
- broken local relative link (flagged);
- valid local link (no errors);
- external URL, image link, and anchor link (all ignored).

All fixtures are synthetic Markdown files in temporary directories.
