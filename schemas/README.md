# Schema sources and updates

## Pinned baseline

All five JSON schemas are byte-for-byte copies from the official
[CycloneDX specification release 1.7.2][release], commit
[`349314a9d7671d7d2ca5b711a725f49a73979da6`][source].

| Local file in `schemas/` | Upstream file in `schema/` |
| --- | --- |
| `cyclonedx_1_4.json` | `bom-1.4.schema.json` |
| `cyclonedx_1_5.json` | `bom-1.5.schema.json` |
| `cyclonedx_1_6.json` | `bom-1.6.schema.json` |
| `cyclonedx_1_7.json` | `bom-1.7.schema.json` |
| `cryptography-defs.schema.json` | `cryptography-defs.schema.json` |

These inputs provide models for CycloneDX 1.4–1.7. Maintenance-release numbers
identify schema snapshots, not new document format versions: 1.7 documents
continue to use `"specVersion": "1.7"`. See [NOTICE](../NOTICE) for attribution.

## Generation and scope

`build.rs` reads the checked-in schemas, adapts some constructs for
`schemafy_lib`, and generates Rust models and builders in Cargo's `OUT_DIR`.
`src/cyclonedx.rs` exposes the `v_1_4`–`v_1_7` modules. The schemas are included
in the published crate; compilation and runtime do not download updates.

Matching these inputs does **not** establish full JSON Schema conformance.
The generator does not enforce every constraint, unknown fields may be ignored,
and unvendored SPDX/signature references retain inherited string aliases.
Parsing and typed round trips do not guarantee lossless preservation of
arbitrary input or downstream persistence. See
[Scope and limitations](../README.md#scope-and-limitations).

### KMAC compatibility

[Specification PR #844], included in release 1.7.1 and retained in 1.7.2,
removed the original 1.7 tag's ambiguous standalone `KMAC` family. The registry
places KMAC MAC variants under `SHA-3` and the KMAC-based KDF under `SP800-108`.
The bindings follow that correction: the historical `algorithmFamily: "KMAC"`
literal is rejected, not silently normalized. This is not a missing upstream
fix; accepting that literal would require a separate legacy-compatibility and
round-trip policy. Registry variant patterns are not an additional validator
provided by this library.

## Updating

1. Select an official specification release and pin its immutable commit.
   Retrieve the mapped files from that commit, not an unpinned `master` branch
   or a live schema URL. Review referenced subschemas together; shared inputs
   can affect more than one supported format version.
2. Update these files and the baseline above, preserving attribution in
   `NOTICE` and documenting any intentional local differences.
3. Review generated Rust API changes, run library and relevant downstream
   compatibility checks, and choose an appropriate crate release. Even a
   specification maintenance update can change public Rust types.

For a new format version, also add its generation call in `build.rs`, public
module in `src/cyclonedx.rs`, and regression tests. There is no automatic schema
updater; ordinary Cargo dependency updates do not refresh these files.

[release]: https://github.com/CycloneDX/specification/releases/tag/1.7.2
[source]: https://github.com/CycloneDX/specification/tree/349314a9d7671d7d2ca5b711a725f49a73979da6/schema
[Specification PR #844]: https://github.com/CycloneDX/specification/pull/844
