[![CI](https://github.com/scm-rs/cyclonedx-rs/actions/workflows/ci.yaml/badge.svg)](https://github.com/scm-rs/cyclonedx-rs/actions/workflows/ci.yaml)

# cyclonedx-rs

Serde-compatible Rust models and builders for reading and writing CycloneDX
Software Bills of Materials (SBOMs), supporting specification versions 1.4–1.7
using JSON schemas from the official specification release **1.7.2**.

A standalone fork of **Paul Sastrasinh's
[serde-cyclonedx](https://github.com/psastras/sbom-rs)**, preserving its generated
APIs and upstream attribution.

Minimum supported Rust version: **1.91.0**. CI also checks stable Rust.

## Releases

Releases follow the [SCM-RS shared release workflow](https://github.com/scm-rs/shared-workflows).
Pushing a version tag (`vX.Y.Z`) runs CI, generates release notes from
Conventional Commits, creates a GitHub release, and publishes to crates.io. The
tag version must match the package version. After publication,
[docs.rs](https://docs.rs/cyclonedx-rs) builds the API documentation.

## Models and usage

Modules `cyclonedx::v_1_4`, `v_1_5`, `v_1_6`, and `v_1_7` retain upstream
APIs, builders, serialization, and features. The package is `cyclonedx-rs`;
the default Rust import is `cyclonedx_rs`:

```rust
use cyclonedx_rs::cyclonedx::v_1_7::CycloneDx;

let bom: CycloneDx = serde_json::from_str(r#"{
  "bomFormat": "CycloneDX", "specVersion": "1.7", "version": 1
}"#).unwrap();
assert_eq!(bom.spec_version, "1.7");
```

```rust
use cyclonedx_rs::cyclonedx::v_1_4::CycloneDxBuilder;

let bom = CycloneDxBuilder::default()
  .bom_format("CycloneDX")
  .spec_version("1.4")
  .version(1)
  .build()
  .unwrap();
```

Development consumers may alias this package as `serde-cyclonedx`. An alias
keeps import spelling, **not Rust type identity**: the original package and
this fork's types are not interchangeable. Walker and Trustify must resolve
the same package version and source.

## Scope and limitations

Models are generated at build time from the vendored schemas by the unchanged
upstream generator. Parsing and typed round trips are **not full JSON Schema
validation**: constraints are not all enforced, unknown fields may be ignored,
and unvendored SPDX/signature references retain upstream string aliases.
Successful deserialization also does not establish downstream persistence.

All five vendored JSON schemas are exact copies from specification release
1.7.2. Maintenance-release numbers identify schema snapshots; 1.7 documents
still use `"specVersion": "1.7"`. See [Schema sources and updates](schemas/README.md)
for the pinned source commit and update process.

The legacy standalone `algorithmFamily: "KMAC"` value from the original 1.7 tag
is rejected, following the correction included in the maintenance releases
([specification #844](https://github.com/CycloneDX/specification/pull/844)).
KMAC MAC variants belong to `SHA-3`; the KMAC-based KDF belongs to `SP800-108`.
Legacy-family compatibility and silent normalization are not provided.

Tests include upstream's four 1.7 regressions (citations, `isExternal`, crypto
enums, ML-KEM builders and `3DES`), explicit cryptography-family compatibility
checks, and direct 1.4/1.5/1.6 compatibility tests. There is no CLI or SPDX
library in this repository.

## Local checks and CI

Run the standard Rust checks locally:

```sh
cargo fmt --check
cargo check --all-targets --all-features --locked
cargo test --all-features --locked
cargo clippy --all-targets --all-features --locked -- -D warnings
```

CI follows the SCM-RS preflight and platform-matrix checks: formatting, tests,
Clippy, and all-feature checks on stable and the declared MSRV across Linux,
macOS, and Windows. Until a registry baseline exists, PR semver checks compare
against the target branch's same-identity `cyclonedx-rs` package, not the
original `serde-cyclonedx` package.

## Licensing

Library source: MIT, **Copyright (c) 2023 Paul Sastrasinh**; see [LICENSE](LICENSE).
Vendored CycloneDX schemas: Apache-2.0, OWASP Foundation; see
[LICENSE-APACHE](LICENSE-APACHE) and [NOTICE](NOTICE).
