# Releasing cyclonedx-rs

Releases are manual. CI builds, tests and verifies packages with read-only
permissions; it does not publish or create tags. The first fork release version
is **0.10.1**, with Rust **1.91.0** as its minimum.

## Before publication

1. Review the exact source commit and first-release metadata. Confirm its license
   notices and the documented inherited schema baseline. The first release keeps
   the existing definitions; older standalone KMAC-family compatibility is a
   follow-up, not a prerequisite code change.
2. Establish the normal `main` branch and review release changes there. The initial
   repository used `prepare/cyclonedx-rs` as its default review branch; changing
   the remote/default branch is an explicit repository-admin action, not part of
   local preparation. Use a PR or manual CI dispatch for a release-preparation
   branch, since arbitrary preparation pushes are outside the push triggers.
3. Require successful stable/MSRV checks on Linux, macOS and Windows, plus the
   verified package job, for the final release revision. A previous preparation
   run is not evidence for an untested release revision.
4. Confirm a crates.io account with publishing access and the intended additional
   owners/team. A GitHub repository does not reserve the crate name. Check name
   availability immediately before the first upload; do not publish a placeholder.
5. Work from a clean checkout of the reviewed commit. Keep the tracked Cargo.lock
   and all schema/build inputs. Confirm the version and registry target:

   ```sh
   git status --short
   git rev-parse HEAD
   cargo metadata --no-deps --format-version 1 --locked
   ```

   `Cargo.toml` must name `cyclonedx-rs`, declare the approved version, and restrict
   `publish` to `["crates-io"]`. The package checker enforces the name/target and
   compares the archived original manifest to the source manifest.

## Validate the exact package

```sh
cargo check --all-targets --all-features --locked
cargo test --all-features --locked
cargo clippy --all-targets --all-features --locked -- -D warnings
cargo fmt --all -- --check
cargo +1.91.0 check --all-targets --all-features --locked
cargo +1.91.0 test --all-features --locked
cargo +1.91.0 clippy --all-targets --all-features --locked -- -D warnings
cargo package --list --locked
cargo package --locked
python3 -m unittest discover -s ci -p 'test_*.py'
python3 ci/verify-package.py
cargo publish --dry-run --locked --registry crates-io
```

Inspect the archive and test an independent consumer extracted from it on stable
and Rust 1.91.0, without a consumer-side Serde derive workaround. Include a 1.7
parse/round-trip/builder check. Record the source SHA, lockfile and archive hash.
Do not use `--no-verify`.

Local uncommitted preparation may use `--allow-dirty` for package/dry-run checks,
but that is not the release procedure. Repeat packaging/dry-run checks from the
clean, reviewed commit before an upload. Cargo adds VCS metadata during packaging,
so a dirty preparation archive is not the final release archive.

## Publish — requires separate approval

The commands in this section have registry/remote side effects. Run them only
once the exact version/commit and publication are approved. Use existing secure
credential handling; never commit or paste registry tokens into source or logs.

```sh
cargo publish --locked --registry crates-io
```

A published name/version is immutable: it cannot be overwritten. If a request
has an ambiguous result, check the registry before retrying. A dry run neither
uploads the crate nor reserves its name.

## Verify and record the release

1. Verify the exact version is available on crates.io and inspect its owner list.
   The first publishing account becomes the initial owner. Add the agreed
   individual owners or the verified GitHub team after publication; do not guess
   a team slug. Confirm required invitations/access are effective.
2. Create a fresh consumer outside the source workspace and install the exact
   registry version, for example `cyclonedx-rs = "=0.10.1"` plus `serde_json`.
   Use no path/Git overrides or patches. Check Cargo metadata for the registry
   source and run representative parse/round-trip/build tests on stable/MSRV.
3. Confirm docs.rs builds successfully and its 0.10.1 examples/links work.
4. Tag the exact published source commit as `v0.10.1` and publish the GitHub release
   notes from `CHANGELOG.md`, only after approval for those remote actions. Check
   that the tag/version/source align; never tag a different or dirty revision.
5. After a registry baseline exists, evaluate the organization shared CI/semver
   workflow separately. Do not compare this crate to `serde-cyclonedx` as if the
   package identities were interchangeable.

Walker/Trustify registry conversion and walker release/threading decisions are
separate follow-ups. Both downstream graphs must resolve the same model package
version and source; Git and registry copies are not interchangeable Rust types.
