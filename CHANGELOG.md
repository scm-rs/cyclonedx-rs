# Changelog

## 0.10.1

First standalone release of `cyclonedx-rs`, a library-only fork of Paul
Sastrasinh's `serde-cyclonedx` from `sbom-rs`.

- Provides schema-generated Serde models and builders for CycloneDX 1.4–1.7,
  preserving the inherited generated APIs.
- Includes CycloneDX 1.7 models for fields such as citations and `isExternal`,
  with direct deserialize, round-trip and builder regression tests.
- Enables Serde derive explicitly for standalone consumers.
- Requires Rust 1.91.0; checks stable/MSRV on Linux, macOS and Windows.
- Packages all required schema/build inputs, fixtures, licenses and attribution.
- Uses the `cyclonedx-rs` package and `cyclonedx_rs` default Rust import. Consumers
  may keep the `serde-cyclonedx` dependency alias, but the original and fork types
  are not interchangeable. There is no CLI or SPDX library in this release.

### Known limitations

The inherited crypto definitions follow the later specification baseline recorded
in `PROVENANCE.md`, rather than the older 1.7 tag. They reject the older literal
`algorithmFamily: "KMAC"` after the specification project's deliberate removal
of the redundant standalone family (#824/#844). Compatibility with that older
representation is deferred; this release does not change schemas or the generator.

Parsing and typed round trips are not full JSON Schema validation and do not prove
preservation of unknown fields or downstream persistence of every 1.7 field.
