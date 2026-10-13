# Extraction provenance and preparation boundaries

- Original repository: https://github.com/psastras/sbom-rs
- Validated source: `9f1b93aea2e55929ddb2140014432db23afe25fb`
  (`release/serde-cyclonedx-1.7`, upstream release proposal #446).
- Upstream main rechecked: `13ec94359d297aab8bbac8bdd73b38d415526fae`.
- History-preserving subtree split of `serde-cyclonedx` in a fresh local clone:
  `85547a34ec54bd685e9dfba54048227e8d3f8a62`.
- Review branch: `prepare/cyclonedx-rs`. The initial extraction was prepared
  without implementation commits; the user subsequently authorized a library
  preparation commit and push to `scm-rs/cyclonedx-rs` for review only.
- MIT license, rustfmt policy, four direct 1.7 tests, and the sibling
  `tests/examples/cargo-binary/sbom.cyclonedx.json` fixture were copied from
  that exact source revision. The 1.5 and 1.6 test fixtures are derived from
  the same 1.4 fixture by changing only `specVersion` (and JSON formatting),
  not purported upstream CLI output for those versions.

`build.rs`, `src/cyclonedx.rs`, and every schema are unchanged from the source.
The explicit Serde derive dependency is preserved. Metadata, crate-local docs,
independent lockfile/tests/CI, licensing notices and package-content checks are
preparation changes only. No CLI, SPDX crate, or release workflow is included.
The inherited `LICENSE -> ../LICENSE` workspace symlink was replaced with a
regular file containing the complete, unchanged upstream MIT text so fresh
standalone Git checkouts do not depend on a parent workspace license. Package
verification also rejects license/notice symlinks.

The library retains upstream author credit and history. It was initially
cloned from a local extraction workspace; the review repository is now
https://github.com/scm-rs/cyclonedx-rs. API documentation is built by docs.rs
after publication. This is not an official handover; upstream serde-cyclonedx
remains a separately maintained and versioned package.

## Licensing provenance

The CycloneDX BOM schemas explicitly state Apache License 2.0 in `$comment`.
The cryptography definitions come from the same CycloneDX specification.
`LICENSE-APACHE` was retrieved read-only from
https://github.com/CycloneDX/specification/blob/1.7/LICENSE and retains its
OWASP Foundation attribution. `NOTICE` documents all five vendored inputs.
No schema content was changed. Cargo's `MIT AND Apache-2.0` describes the
combined archive; library code remains MIT, without relicensing. Release review
should reconfirm third-party notice completeness.

## Schema baseline review

All schema bytes remain unchanged from the validated sbom-rs source revision.
They are not claimed to be byte-identical to the specification's tag `1.7`.
The vendored cryptography definitions are semantically equal to specification
master at `1ce97b2a7b8cf2429da248560d2aa671c6bce74a`, including its omission
of `KMAC`, which appears in tag `1.7`. A separate compatibility probe confirmed
that the inherited generated enum rejects `algorithmFamily: "KMAC"`.
The specification project tracked the ambiguity in
[#824](https://github.com/CycloneDX/specification/issues/824) and intentionally
removed the redundant family in merged
[#844](https://github.com/CycloneDX/specification/pull/844), folding the KMAC-based
KDF into SP800-108. This does not remove KMAC as a cryptographic construction.

The first fork release preserves the inherited definitions without schema or
generator changes. Accepting the older standalone KMAC representation is deferred
to a follow-up. Binding and round-trip tests are not an authoritative JSON Schema
conformance suite, and this release does not claim complete equivalence to tag
`1.7` or downstream persistence of every field.

## First fork release

The first release version is 0.10.1 and its registry target is restricted to
crates.io. Release preparation changes metadata, documentation and package checks;
the generated API inputs, explicit Serde derive dependency, licenses and attribution
remain intact. See [RELEASING.md](RELEASING.md) for the manual release process.

Publication, release tags, repository administration and crate ownership changes
are separate operator actions, not side effects of preparing or running CI.
Downstream registry conversion and walker release/version decisions remain
separate from publishing this library.
