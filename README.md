[![CI](https://github.com/scm-rs/cyclonedx-rs/actions/workflows/ci.yaml/badge.svg)](https://github.com/scm-rs/cyclonedx-rs/actions/workflows/ci.yaml)

# cyclonedx-rs — unpublished preparation fork

Standalone extraction of **Paul Sastrasinh's
[serde-cyclonedx](https://github.com/psastras/sbom-rs)**, retaining its generated
Serde models and builders. This is a fallback fork, not an official handover.
An upstream release remains the preferred production route. This repository
is available for review; no crate has been published. The
[documentation URL](https://docs.rs/cyclonedx-rs) is a planned location and will
become available only after an approved publication.

`publish = false` is intentional. **0.10.1 is only an unpublished working
version**, not an approved first release. Rust **1.91.0** is the compatibility
baseline; CI checks that version and stable. See [PROVENANCE.md](PROVENANCE.md).

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

The inherited cryptography definitions match specification master at
`1ce97b2a7b8cf2429da248560d2aa671c6bce74a`, not the older tag `1.7`.
For example, tag `1.7` includes `KMAC`, while these bindings reject that
algorithm family. This inherited schema-baseline question needs maintainer
review before release; the schemas were not silently updated. See
[PROVENANCE.md](PROVENANCE.md#schema-baseline-review).

Tests include upstream's four 1.7 regressions (citations, `isExternal`, crypto
enums, ML-KEM builders and `3DES`) and direct 1.4/1.5/1.6 compatibility tests.
There is no CLI or SPDX library in this repository.

## Local checks / CI

```sh
cargo check --all-targets --all-features --locked
cargo test --all-features --locked
cargo clippy --all-targets --all-features --locked -- -D warnings
cargo fmt --all -- --check
cargo package --list --locked
cargo package --locked
python3 ci/verify-package.py
cargo +1.91.0 check --all-targets --all-features --locked
cargo +1.91.0 test --all-features --locked
```

For uncommitted local changes, both package commands require `--allow-dirty`;
archive verification must remain enabled (never use `--no-verify`).

Preparation CI has read-only permissions and only build/test/lint/package jobs,
with stable/MSRV coverage on Linux, macOS and Windows. No publishing workflow,
tokens, OIDC, tags, or release jobs are enabled. The organization shared CI was
inspected, but its implicit registry semver baseline cannot exist for this new
package identity. Only that comparison is deferred for the first release;
all normal checks remain. Before adopting shared CI, establish a published
baseline (or explicitly approved same-identity Git baseline) and review the
original-to-fork public type identity change in downstreams. Do not compare
against registry `serde-cyclonedx` as if it were the renamed package.

## Licensing

Library source: MIT, **Copyright (c) 2023 Paul Sastrasinh**; see [LICENSE](LICENSE).
Vendored CycloneDX schemas: Apache-2.0, OWASP Foundation; see
[LICENSE-APACHE](LICENSE-APACHE) and [NOTICE](NOTICE). Schema bytes are unchanged.
