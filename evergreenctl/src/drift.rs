// =============================================================================
// Evergreenctl - Drift Detection
// =============================================================================
// Detects differences between manifest.toml and the actual Dockerfile.
// Uses shared extraction functions from dockerfile_utils to avoid duplication.
// =============================================================================

use crate::dockerfile_utils::{extract_base_image, extract_entrypoint, extract_ports,
    extract_stop_signal, extract_user, extract_version, extract_all_labels};
use crate::manifest::Manifest;
use anyhow::{Context, Result};
use std::collections::HashSet;
use std::path::Path;

pub fn cmd_drift(image_dir: &str) -> Result<()> {
    let dir = Path::new(image_dir);
    let manifest_path = dir.join("manifest.toml");
    let dockerfile_path = dir.join("Dockerfile");

    let manifest = Manifest::from_file(&manifest_path)
        .with_context(|| format!("Failed to read manifest from {}", manifest_path.display()))?;
    let dockerfile_content = std::fs::read_to_string(&dockerfile_path).with_context(|| {
        format!(
            "Failed to read Dockerfile from {}",
            dockerfile_path.display()
        )
    })?;

    let mut drifts: Vec<String> = Vec::new();

    // Version drift
    if let Some(df_ver) = extract_version(&dockerfile_content) {
        if df_ver != manifest.version() {
            drifts.push(format!(
                "VERSION: manifest={}, dockerfile={}",
                manifest.version(),
                df_ver
            ));
        }
    } else {
        drifts.push(format!(
            "VERSION: manifest={}, dockerfile=(not found)",
            manifest.version()
        ));
    }

    // Base image drift
    let df_base = extract_base_image(&dockerfile_content);
    if df_base != manifest.base_image() {
        drifts.push(format!(
            "BASE IMAGE: manifest={}, dockerfile={}",
            manifest.base_image(),
            df_base
        ));
    }

    // User drift
    let df_user = extract_user(&dockerfile_content);
    let expected_user = manifest.user();
    if df_user != expected_user {
        drifts.push(format!(
            "USER: manifest={}, dockerfile={}",
            expected_user, df_user
        ));
    }

    // Stop signal drift
    let df_stop = extract_stop_signal(&dockerfile_content);
    let expected_stop = manifest.stop_signal();
    if df_stop != expected_stop {
        drifts.push(format!(
            "STOPSIGNAL: manifest={}, dockerfile={}",
            expected_stop, df_stop
        ));
    }

    // Entry point drift
    let df_ep_parts = extract_entrypoint(&dockerfile_content);
    let expected_ep = format!(
        "[{}]",
        manifest
            .entrypoint()
            .iter()
            .map(|p| format!("\"{}\"", p))
            .collect::<Vec<_>>()
            .join(", ")
    );
    let actual_ep = format!(
        "[{}]",
        df_ep_parts
            .iter()
            .map(|p| format!("\"{}\"", p))
            .collect::<Vec<_>>()
            .join(", ")
    );
    if actual_ep != expected_ep {
        drifts.push(format!(
            "ENTRYPOINT:\n  manifest:  {}\n  dockerfile: {}",
            expected_ep, actual_ep
        ));
    }

    // Exposed ports drift
    let df_ports: HashSet<String> = extract_ports(&dockerfile_content)
        .into_iter()
        .collect();
    let expected_ports: HashSet<String> = manifest
        .exposed_ports()
        .iter()
        .map(|p| p.to_string())
        .collect();

    let missing_ports: Vec<_> = expected_ports.difference(&df_ports).collect();
    let extra_ports: Vec<_> = df_ports.difference(&expected_ports).collect();
    if !missing_ports.is_empty() {
        drifts.push(format!(
            "EXPOSE missing ports: {}",
            missing_ports
                .iter()
                .map(|s| s.as_str())
                .collect::<Vec<_>>()
                .join(", ")
        ));
    }
    if !extra_ports.is_empty() {
        drifts.push(format!(
            "EXPOSE extra ports: {}",
            extra_ports
                .iter()
                .map(|s| s.as_str())
                .collect::<Vec<_>>()
                .join(", ")
        ));
    }

    // Label drift
    let expected_labels = vec![
        (
            "org.opencontainers.image.title",
            manifest.name().to_string(),
        ),
        (
            "org.opencontainers.image.version",
            manifest.version().to_string(),
        ),
        (
            "org.opencontainers.image.description",
            manifest.metadata.description.clone(),
        ),
        (
            "org.opencontainers.image.vendor",
            manifest.metadata.vendor.clone(),
        ),
        ("evergreen.image.tier", manifest.metadata.tier.clone()),
    ];

    let df_label_map = extract_all_labels(&dockerfile_content);
    for (key, expected_val) in &expected_labels {
        if let Some(actual_val) = df_label_map.get(*key) {
            if actual_val != expected_val {
                drifts.push(format!(
                    "LABEL {}: manifest=\"{}\", dockerfile=\"{}\"",
                    key, expected_val, actual_val
                ));
            }
        } else {
            drifts.push(format!(
                "LABEL {}: manifest=\"{}\", dockerfile=(missing)",
                key, expected_val
            ));
        }
    }

    if drifts.is_empty() {
        println!("No drift detected between manifest.toml and Dockerfile.");
    } else {
        println!("Drift detected ({} differences):", drifts.len());
        for d in &drifts {
            println!("  - {}", d);
        }
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_drift_no_differences() {
        let dir = std::env::temp_dir().join("evergreen_drift_test_no_diff");
        let _ = std::fs::create_dir_all(&dir);

        std::fs::write(
            dir.join("manifest.toml"),
            r#"
name = "test-image"
version = "1.0.0"
source_url = "https://github.com/test/repo"
source_type = "binary-download"
build_type = "binary-download"
user = "65532:65532"
base_image = "scratch"
entrypoint = ["/app"]
exposed_ports = ["8080"]

[metadata]
description = "Test image"
vendor = "Test"
tier = "standard"
"#,
        )
        .unwrap();

        std::fs::write(
            dir.join("Dockerfile"),
            r#"FROM scratch
ARG VERSION=1.0.0
USER 65532:65532
STOPSIGNAL SIGTERM
ENTRYPOINT ["/app"]
EXPOSE 8080
LABEL org.opencontainers.image.title="test-image"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.description="Test image"
LABEL org.opencontainers.image.vendor="Test"
LABEL evergreen.image.tier="standard"
"#,
        )
        .unwrap();

        let result = cmd_drift(dir.to_str().unwrap());
        assert!(result.is_ok());

        let _ = std::fs::remove_dir_all(&dir);
    }

    #[test]
    fn test_drift_version_mismatch() {
        let dir = std::env::temp_dir().join("evergreen_drift_test_ver");
        let _ = std::fs::create_dir_all(&dir);

        std::fs::write(
            dir.join("manifest.toml"),
            r#"
name = "test-image"
version = "1.0.0"
source_url = "https://github.com/test/repo"
source_type = "binary-download"
build_type = "binary-download"
user = "65532:65532"
base_image = "scratch"
entrypoint = ["/app"]
exposed_ports = ["8080"]

[metadata]
description = "Test image"
vendor = "Test"
tier = "standard"
"#,
        )
        .unwrap();

        std::fs::write(
            dir.join("Dockerfile"),
            r#"FROM scratch
ARG VERSION=2.0.0
USER 65532:65532
ENTRYPOINT ["/app"]
EXPOSE 8080
LABEL org.opencontainers.image.title="test-image"
LABEL org.opencontainers.image.version="2.0.0"
LABEL org.opencontainers.image.description="Test image"
LABEL org.opencontainers.image.vendor="Test"
LABEL evergreen.image.tier="standard"
"#,
        )
        .unwrap();

        let result = cmd_drift(dir.to_str().unwrap());
        assert!(result.is_ok());

        let _ = std::fs::remove_dir_all(&dir);
    }

    #[test]
    fn test_drift_missing_version_in_dockerfile() {
        let dir = std::env::temp_dir().join("evergreen_drift_test_missing_ver");
        let _ = std::fs::create_dir_all(&dir);

        std::fs::write(
            dir.join("manifest.toml"),
            r#"
name = "test-image"
version = "1.0.0"
source_url = "https://github.com/test/repo"
source_type = "binary-download"
build_type = "binary-download"
user = "65532:65532"
base_image = "scratch"
entrypoint = ["/app"]
exposed_ports = ["8080"]

[metadata]
description = "Test image"
vendor = "Test"
tier = "standard"
"#,
        )
        .unwrap();

        std::fs::write(
            dir.join("Dockerfile"),
            r#"FROM scratch
USER 65532:65532
ENTRYPOINT ["/app"]
EXPOSE 8080
LABEL org.opencontainers.image.title="test-image"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.description="Test image"
LABEL org.opencontainers.image.vendor="Test"
LABEL evergreen.image.tier="standard"
"#,
        )
        .unwrap();

        let result = cmd_drift(dir.to_str().unwrap());
        assert!(result.is_ok());

        let _ = std::fs::remove_dir_all(&dir);
    }

    #[test]
    fn test_drift_port_mismatch() {
        let dir = std::env::temp_dir().join("evergreen_drift_test_port");
        let _ = std::fs::create_dir_all(&dir);

        std::fs::write(
            dir.join("manifest.toml"),
            r#"
name = "test-image"
version = "1.0.0"
source_url = "https://github.com/test/repo"
source_type = "binary-download"
build_type = "binary-download"
user = "65532:65532"
base_image = "scratch"
entrypoint = ["/app"]
exposed_ports = ["8080"]

[metadata]
description = "Test image"
vendor = "Test"
tier = "standard"
"#,
        )
        .unwrap();

        std::fs::write(
            dir.join("Dockerfile"),
            r#"FROM scratch
ARG VERSION=1.0.0
USER 65532:65532
ENTRYPOINT ["/app"]
EXPOSE 8080 9090
LABEL org.opencontainers.image.title="test-image"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.description="Test image"
LABEL org.opencontainers.image.vendor="Test"
LABEL evergreen.image.tier="standard"
"#,
        )
        .unwrap();

        let result = cmd_drift(dir.to_str().unwrap());
        assert!(result.is_ok());

        let _ = std::fs::remove_dir_all(&dir);
    }
}
