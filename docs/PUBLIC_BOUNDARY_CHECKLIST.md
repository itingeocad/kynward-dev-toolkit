# Public Boundary Checklist

Use this checklist before adding files or examples to this public repository.

The purpose is to keep this toolkit useful while avoiding accidental publication of private Kynward game material.

## Safe by default

The following content is usually safe when it is generic, synthetic, and public:

- dependency-free developer tools;
- documentation checkers;
- validation helpers;
- smoke-test templates;
- synthetic sample fixtures;
- generic Godot tooling notes;
- public workflow documentation;
- small examples that do not reveal private game implementation details.

## Requires review

Review carefully before publishing:

- extracted scripts from the private game repository;
- data structure examples derived from private game data;
- roadmap or planning text;
- screenshots or visual mockups;
- names that could reveal private setting or lore;
- configuration files;
- build scripts copied from private workflows.

## Do not publish

Do not publish the following unless there is a separate explicit approval:

- private lore or narrative canon;
- campaign content;
- unreleased mechanics;
- final game art;
- logos, icons, screenshots, mockups, music, sound, or fonts;
- commercial design documents;
- private roadmap details;
- credentials, tokens, keys, passwords, cookies, or session data;
- local environment files;
- deployment hostnames, private IPs, or internal paths;
- third-party content without a compatible license;
- generated assets without a clear license and provenance.

## Review questions

Before committing a file, answer:

1. Does this file depend on the private Kynward game repository?
2. Does it reveal private lore, setting, or roadmap details?
3. Does it contain final art, brand assets, screenshots, or audio?
4. Does it contain secrets, credentials, hostnames, local paths, or deployment data?
5. Does it include third-party content with unclear licensing?
6. Can this file be useful to an external contributor without private context?
7. Is the file written in English for public repository use?

If any answer is unclear, do not publish the file until it has been reviewed.

## Preferred public example style

Use synthetic names and small examples:

```text
sample_world
sample_zone
sample_region
sample_place_a
sample_place_b
sample_connection
```

Avoid names from the private game setting or unreleased story material.
