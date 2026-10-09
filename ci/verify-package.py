#!/usr/bin/env python3
"""Check verified standalone archive inputs and reject workspace/build debris."""
import hashlib
import pathlib
import tarfile
import tomllib

root = pathlib.Path(__file__).resolve().parents[1]
manifest = tomllib.loads((root / "Cargo.toml").read_text())
package = manifest["package"]
assert package["publish"] is False, "preparation must remain unpublished"
name = f'{package["name"]}-{package["version"]}'
archive = root / "target" / "package" / f"{name}.crate"
required = {"Cargo.toml", "Cargo.lock", "build.rs", "src/lib.rs",
            "src/cyclonedx.rs", "LICENSE", "LICENSE-APACHE", "NOTICE",
            "README.md", "PROVENANCE.md", "tests/cyclonedx_1_7_test.rs",
            "tests/existing_versions.rs"}
required.update(str(p.relative_to(root)) for p in (root / "schemas").glob("*.json"))
required.update(str(p.relative_to(root)) for p in (root / "tests" / "fixtures").glob("*.json"))
assert len(list((root / "schemas").glob("*.json"))) == 5
with tarfile.open(archive) as tar:
    contents = {m.name.removeprefix(name + "/") for m in tar.getmembers()}
    assert required <= contents, f"missing: {required - contents}"
    assert "schemas/cryptography-defs.schema.json" in contents
    for path in contents:
        assert not any(part in {"target", "cargo-sbom", "serde-spdx"}
                       for part in pathlib.PurePosixPath(path).parts), path
        assert not path.endswith(".profraw"), path
    for path in sorted(required - {"Cargo.toml"}):
        data = tar.extractfile(name + "/" + path).read()
        assert data == (root / path).read_bytes(), path
        print(hashlib.sha256(data).hexdigest(), path)
print(f"PASS {archive}: {len(contents)} files, all required inputs present")
