# Usage Guide

This guide shows how to run the public toolkit checks locally.

All commands use repository-relative paths and public files from this repository only.

## Requirements

- Python 3.10 or newer is recommended.
- No third-party Python packages are required for the current tools.

## Clone the repository

```bash
git clone https://github.com/itingeocad/kynward-dev-toolkit.git
cd kynward-dev-toolkit
```
## Windows PowerShell Notes

If `python` is not available on Windows, use the `py` launcher instead.

### Run the checks:

```powershell
py tools/markdown_structure_check.py .
py tools/markdown_link_check.py .
py tools/json_fixture_validate.py examples/sample_world_fixture.json
```

The expected output is the same as shown below for each tool.

If you have GitHub CLI installed, you can also clone using:

```powershell
gh repo clone itingeocad/kynward-dev-toolkit
cd kynward-dev-toolkit
```
## Check Markdown structure

```bash
python tools/markdown_structure_check.py .
```

Expected successful output:

```text
Markdown structure check passed.
```

This check verifies that public Markdown files have a top-level heading and avoid tab-indented lines.

## Check local Markdown links

```bash
python tools/markdown_link_check.py .
```

Expected successful output:

```text
Markdown local link check passed.
```

This check verifies local relative Markdown links. External links are ignored.

## Validate the sample JSON fixture

```bash
python tools/json_fixture_validate.py examples/sample_world_fixture.json
```

Expected successful output:

```text
JSON fixture validation passed: <absolute path>
```

The fixture is synthetic and public-safe. It is not copied from the private Kynward game repository.

## Run all current checks manually

```bash
python tools/markdown_structure_check.py .
python tools/markdown_link_check.py .
python tools/json_fixture_validate.py examples/sample_world_fixture.json
```

## Failure behavior

The tools print validation errors to standard output and exit with a non-zero status code when a check fails.

## Public safety rule

Do not use these tools to publish or validate private Kynward lore, private roadmap details, final art, logos, screenshots, credentials, local environment files, or unreleased commercial game data.
