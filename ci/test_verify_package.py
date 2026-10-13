"""Regression tests for release metadata and standalone archive guards."""
import io
import pathlib
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest


class VerifyPackageTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix="cyclonedx-package-check-")
        self.addCleanup(directory.cleanup)
        self.root = pathlib.Path(directory.name)
        self.script = self.root / "ci" / "verify-package.py"
        self.script.parent.mkdir()
        shutil.copyfile(pathlib.Path(__file__).with_name("verify-package.py"), self.script)
        self.files = {
            path: b"fixture\n"
            for path in [
                "Cargo.lock", "build.rs", "src/lib.rs", "src/cyclonedx.rs",
                "LICENSE", "LICENSE-APACHE", "NOTICE", "README.md", "PROVENANCE.md",
                "RELEASING.md", "CHANGELOG.md",
                "tests/cyclonedx_1_7_test.rs", "tests/existing_versions.rs",
                "tests/fixtures/cyclonedx-1.4.json",
                "tests/fixtures/cyclonedx-1.5.json",
                "tests/fixtures/cyclonedx-1.6.json",
                "schemas/cyclonedx_1_4.json", "schemas/cyclonedx_1_5.json",
                "schemas/cyclonedx_1_6.json", "schemas/cyclonedx_1_7.json",
                "schemas/cryptography-defs.schema.json",
            ]
        }
        for path, data in self.files.items():
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        self.manifest = self.root / "Cargo.toml"
        self.write_manifest()
        self.files["Cargo.toml"] = self.manifest.read_bytes()
        self.files["Cargo.toml.orig"] = self.manifest.read_bytes()
        self.archive = self.root / "target/package/cyclonedx-rs-0.10.1.crate"
        self.archive.parent.mkdir(parents=True)
        self.write_archive()

    def write_manifest(self, publication='publish = ["crates-io"]', name="cyclonedx-rs"):
        self.manifest.write_text(
            f'[package]\nname = "{name}"\nversion = "0.10.1"\n{publication}\n'
        )

    def write_archive(self):
        with tarfile.open(self.archive, "w:gz") as archive:
            for path, data in self.files.items():
                member = tarfile.TarInfo(f"cyclonedx-rs-0.10.1/{path}")
                member.size = len(data)
                archive.addfile(member, io.BytesIO(data))

    def verify(self):
        return subprocess.run(
            [sys.executable, str(self.script)],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_valid_release_archive(self):
        result = self.verify()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_rejects_non_crates_io_publication(self):
        for publication in [
            "", "publish = false", "publish = true", "publish = []",
            'publish = ["other"]', 'publish = ["crates-io", "other"]',
        ]:
            with self.subTest(publication=publication):
                self.write_manifest(publication)
                result = self.verify()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("release must target crates.io only", result.stderr)

    def test_rejects_wrong_package_name(self):
        self.write_manifest(name="serde-cyclonedx")
        result = self.verify()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unexpected release package name", result.stderr)

    def test_rejects_stale_original_manifest(self):
        self.files["Cargo.toml.orig"] = b"old manifest\n"
        self.write_archive()
        result = self.verify()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Cargo.toml.orig", result.stderr)

    def test_rejects_missing_schema(self):
        del self.files["schemas/cryptography-defs.schema.json"]
        self.write_archive()
        result = self.verify()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing:", result.stderr)

    def test_rejects_missing_fixture(self):
        del self.files["tests/fixtures/cyclonedx-1.4.json"]
        self.write_archive()
        result = self.verify()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing:", result.stderr)

    def test_rejects_changed_fixture(self):
        self.files["tests/fixtures/cyclonedx-1.4.json"] = b"changed\n"
        self.write_archive()
        result = self.verify()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("tests/fixtures/cyclonedx-1.4.json", result.stderr)

    def test_rejects_symlinked_license(self):
        target = self.root / "vendored-license"
        target.write_bytes((self.root / "LICENSE").read_bytes())
        (self.root / "LICENSE").unlink()
        (self.root / "LICENSE").symlink_to(target)
        result = self.verify()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("regular vendored file", result.stderr)


if __name__ == "__main__":
    unittest.main()
