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

The library retains upstream author credit and history. It was initially
cloned from a local extraction workspace; the review repository is now
https://github.com/scm-rs/cyclonedx-rs. The docs.rs URL remains a planned
publication destination. This is not an official handover, and the upstream
release remains preferred.

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
Maintainers should reconcile the intended baseline and decide whether a narrowly
reviewed upstream-compatible fix is needed; no schema/generator change was made
to hide this limitation. Binding and round-trip tests are not an authoritative
JSON Schema conformance suite.

## Release decisions deliberately pending

The working 0.10.1 and `publish = false` must not be treated as publication
approval. Name availability, first release version, ownership, exact source
commits, downstream release line and type-identity semver review, registry
conversion, database/schema/QA gates, and release schedule/freeze require
maintainer approval. Only the library review commit and preparation-branch push
have been authorized. Crate publication, release tags, merges, PR creation,
downstream pushes, issue comments, and credentials/ownership changes are not
authorized by that review-repository approval.
