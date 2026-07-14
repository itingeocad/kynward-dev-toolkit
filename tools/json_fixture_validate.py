#!/usr/bin/env python3
"""Validate public synthetic Kynward-style JSON fixtures.

This validator is intentionally small and dependency-free. It checks only the
public sample fixture shape used by this repository. It must not depend on the
private Kynward game repository or on private game data.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REQUIRED_TOP_LEVEL_FIELDS = ("schema_version", "world", "zones", "regions", "places", "connections")
ENTITY_LIST_FIELDS = ("zones", "regions", "places", "connections")


class ValidationErrorCollector:
    """Collect validation errors with consistent formatting."""

    def __init__(self) -> None:
        self.errors: list[str] = []

    def add(self, message: str) -> None:
        """Add one validation error."""
        self.errors.append(message)

    def extend(self, messages: list[str]) -> None:
        """Add multiple validation errors."""
        self.errors.extend(messages)

    @property
    def ok(self) -> bool:
        """Return whether no validation errors were collected."""
        return not self.errors


def load_json(path: Path) -> Any:
    """Load a JSON file and return decoded data."""
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_top_level(data: Any, errors: ValidationErrorCollector) -> None:
    """Validate the top-level fixture structure."""
    if not isinstance(data, dict):
        errors.add("top-level value must be an object")
        return

    for field in REQUIRED_TOP_LEVEL_FIELDS:
        if field not in data:
            errors.add(f"missing required top-level field: {field}")

    world = data.get("world")
    if not isinstance(world, dict):
        errors.add("world must be an object")
    elif not world.get("id"):
        errors.add("world.id is required")

    for field in ENTITY_LIST_FIELDS:
        value = data.get(field)
        if not isinstance(value, list):
            errors.add(f"{field} must be a list")


def collect_ids(data: dict[str, Any], field: str, errors: ValidationErrorCollector) -> set[str]:
    """Collect unique entity IDs from one list field."""
    ids: set[str] = set()
    value = data.get(field, [])
    if not isinstance(value, list):
        return ids

    for index, item in enumerate(value):
        if not isinstance(item, dict):
            errors.add(f"{field}[{index}] must be an object")
            continue

        entity_id = item.get("id")
        if not isinstance(entity_id, str) or not entity_id.strip():
            errors.add(f"{field}[{index}].id is required")
            continue

        if entity_id in ids:
            errors.add(f"duplicate id in {field}: {entity_id}")
        ids.add(entity_id)

    return ids


def validate_named_entities(data: dict[str, Any], field: str, errors: ValidationErrorCollector) -> None:
    """Validate common name fields for public sample entities."""
    value = data.get(field, [])
    if not isinstance(value, list):
        return

    for index, item in enumerate(value):
        if not isinstance(item, dict):
            continue
        name = item.get("name")
        if not isinstance(name, str) or not name.strip():
            errors.add(f"{field}[{index}].name is required")


def validate_references(data: dict[str, Any], errors: ValidationErrorCollector) -> None:
    """Validate references between synthetic public sample entities."""
    zone_ids = collect_ids(data, "zones", errors)
    region_ids = collect_ids(data, "regions", errors)
    place_ids = collect_ids(data, "places", errors)
    collect_ids(data, "connections", errors)

    for index, region in enumerate(data.get("regions", [])):
        if not isinstance(region, dict):
            continue
        zone_id = region.get("zone_id")
        if zone_id not in zone_ids:
            errors.add(f"regions[{index}].zone_id references missing zone: {zone_id}")

    for index, place in enumerate(data.get("places", [])):
        if not isinstance(place, dict):
            continue
        region_id = place.get("region_id")
        if region_id not in region_ids:
            errors.add(f"places[{index}].region_id references missing region: {region_id}")

    for index, connection in enumerate(data.get("connections", [])):
        if not isinstance(connection, dict):
            continue
        endpoints = connection.get("places")
        if not isinstance(endpoints, list) or len(endpoints) != 2:
            errors.add(f"connections[{index}].places must contain exactly two place IDs")
            continue
        for place_id in endpoints:
            if place_id not in place_ids:
                errors.add(f"connections[{index}].places references missing place: {place_id}")


def validate_fixture(data: Any) -> list[str]:
    """Return a list of validation errors for one decoded fixture."""
    errors = ValidationErrorCollector()
    validate_top_level(data, errors)
    if not isinstance(data, dict):
        return errors.errors

    for field in ("zones", "regions", "places"):
        validate_named_entities(data, field, errors)

    validate_references(data, errors)
    return errors.errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a public synthetic JSON fixture.")
    parser.add_argument("fixture", help="Path to a JSON fixture file.")
    args = parser.parse_args()

    fixture_path = Path(args.fixture).resolve()
    if not fixture_path.exists():
        print(f"error: fixture does not exist: {fixture_path}")
        return 2

    try:
        data = load_json(fixture_path)
    except json.JSONDecodeError as exc:
        print(f"{fixture_path}: invalid JSON: {exc}")
        return 1

    errors = validate_fixture(data)
    if errors:
        for error in errors:
            print(f"{fixture_path}: {error}")
        return 1

    print(f"JSON fixture validation passed: {fixture_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
