# Smoke Test Template

Use this template for public-safe prototype and tooling smoke tests.

## Test ID

```text
SMOKE-000
```

## Purpose

Describe what this smoke test verifies.

## Scope

List the tool, data fixture, or workflow under test.

## Preconditions

- Repository is checked out locally.
- Required runtime or interpreter is installed.
- Test data is synthetic and public-safe.

## Steps

1. Run the command or open the relevant file.
2. Perform the action under test.
3. Observe the output.
4. Record any warnings or failures.

## Expected result

Describe the expected successful result.

## Failure notes

Record any failure, unexpected warning, missing file, invalid output, or unclear error message.

## Public safety check

- [ ] No private Kynward content is required.
- [ ] No private paths are printed.
- [ ] No secrets or credentials are required.
- [ ] The test can be shared publicly.
