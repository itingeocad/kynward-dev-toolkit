# Kynward Dev Toolkit

Kynward Dev Toolkit is a public open-source companion repository for developer tooling extracted from the private Kynward game project.

The goal of this repository is to provide safe, reusable tools for Godot prototype development, documentation workflows, validation helpers, smoke-test checklists, and data inspection utilities without exposing private game content, lore, commercial assets, or unreleased product materials.

## Scope

This repository is intended for:

- developer tooling;
- documentation checks;
- validation helpers;
- smoke-test workflows;
- data inspection utilities;
- Godot prototype support scripts;
- contributor-friendly project maintenance workflows.

This repository is not intended to publish the full Kynward game.

## Out of scope

The following materials are not part of this open-source toolkit unless explicitly stated in a specific file or directory:

- final Kynward game code;
- private lore and narrative canon;
- worldbuilding materials;
- campaign content;
- final art, logos, icons, music, sound, fonts, screenshots, mockups, and other non-code assets;
- commercial design documents;
- private roadmap details;
- secrets, credentials, local environment files, or deployment data.

## Relationship to Kynward

Kynward is a fantasy world, settlement, travel, and generation simulation game project. This toolkit contains only the public developer tooling surface that can be shared safely.

The main game repository may remain private while this toolkit evolves as an open-source project.

## Repository layout

```text
.github/              GitHub issue templates and workflows
assets/               Public placeholder assets only, if explicitly licensed
docs/                 Public documentation and project notes
examples/             Small public examples and fixtures
tools/                Developer tools and validation helpers
```

## Current status

This repository is in the initial open-source setup stage.

The first milestone is to establish a safe public toolkit boundary and add small, useful developer tools that do not depend on private Kynward content.

## Usage

Current checks are dependency-free Python scripts:

```bash
python tools/markdown_structure_check.py .
python tools/markdown_link_check.py .
python tools/json_fixture_validate.py examples/sample_world_fixture.json
```

See [docs/USAGE.md](docs/USAGE.md) for details.

## Public safety

Before adding files to this repository, review [docs/PUBLIC_BOUNDARY_CHECKLIST.md](docs/PUBLIC_BOUNDARY_CHECKLIST.md).

Do not publish private lore, final assets, private roadmap details, credentials, local environment files, or unreleased commercial game data.

## License

Source code, tooling code, configuration files, and public developer documentation in this repository are licensed under the Apache License 2.0 unless a file or directory explicitly states otherwise.

The Kynward name, logos, setting, lore, narrative materials, visual identity, and non-code assets are not granted for reuse under the Apache License 2.0 unless explicitly stated.

See [LICENSE](LICENSE) and [NOTICE](NOTICE).
