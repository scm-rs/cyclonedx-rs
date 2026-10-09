//! Direct binding tests, not CLI execution or full schema conformance.
use anyhow::Result;
use cyclonedx_rs::cyclonedx::{v_1_4, v_1_5, v_1_6};
use pretty_assertions::assert_eq;
use serde::{de::DeserializeOwned, Serialize};
use serde_json::Value;

fn preserves_selected_fields<T>(input: &str, spec: &str) -> Result<()>
where
  T: DeserializeOwned + Serialize + PartialEq + std::fmt::Debug,
{
  let original: Value = serde_json::from_str(input)?;
  let typed: T = serde_json::from_str(input)?;
  let output = serde_json::to_value(&typed)?;
  let reparsed: T = serde_json::from_value(output.clone())?;
  assert_eq!(typed, reparsed);
  assert_eq!(output["bomFormat"], "CycloneDX");
  assert_eq!(output["specVersion"], spec);
  assert_eq!(output["serialNumber"], original["serialNumber"]);
  assert_eq!(output["version"], original["version"]);
  let components = original["components"].as_array().unwrap();
  assert!(!components.is_empty());
  assert_eq!(
    output["components"].as_array().unwrap().len(),
    components.len()
  );
  for (i, component) in components.iter().enumerate() {
    for field in [
      "name",
      "version",
      "bom-ref",
      "purl",
      "licenses",
      "externalReferences",
    ] {
      assert_eq!(output["components"][i][field], component[field]);
    }
  }
  assert_eq!(output["dependencies"], original["dependencies"]);
  assert_eq!(
    output["metadata"]["timestamp"],
    original["metadata"]["timestamp"]
  );
  assert_eq!(
    output["metadata"]["component"]["name"],
    original["metadata"]["component"]["name"]
  );
  Ok(())
}

#[test]
fn cyclonedx_1_4_fixture() -> Result<()> {
  preserves_selected_fields::<v_1_4::CycloneDx>(
    include_str!("fixtures/cargo-binary-1.4.json"),
    "1.4",
  )
}

#[test]
fn cyclonedx_1_5_fixture() -> Result<()> {
  preserves_selected_fields::<v_1_5::CycloneDx>(
    include_str!("fixtures/cargo-binary-1.5.json"),
    "1.5",
  )
}

#[test]
fn cyclonedx_1_6_fixture() -> Result<()> {
  preserves_selected_fields::<v_1_6::CycloneDx>(
    include_str!("fixtures/cargo-binary-1.6.json"),
    "1.6",
  )
}
