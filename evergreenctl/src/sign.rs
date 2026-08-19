use crate::manifest::Manifest;
use anyhow::{Context, Result};
use std::path::Path;

pub fn cmd_sign(image_dir: &str) -> Result<()> {
    let dir = Path::new(image_dir);
    let manifest_path = dir.join("manifest.toml");
    let dockerfile_path = dir.join("Dockerfile");

    let (name, version, _base_image) = if manifest_path.exists() {
        let manifest = Manifest::from_file(&manifest_path)
            .with_context(|| format!("Failed to read manifest from {}", manifest_path.display()))?;
        (
            manifest.name().to_string(),
            manifest.version().to_string(),
            manifest.base_image().to_string(),
        )
    } else if dockerfile_path.exists() {
        let content = std::fs::read_to_string(&dockerfile_path).with_context(|| {
            format!(
                "Failed to read Dockerfile from {}",
                dockerfile_path.display()
            )
        })?;
        let name = dir
            .file_name()
            .map(|n| n.to_string_lossy().to_string())
            .unwrap_or_else(|| "unknown".to_string());
        let version = extract_version(&content).unwrap_or_else(|| "latest".to_string());
        let base = extract_base_image(&content);
        (name, version, base)
    } else {
        anyhow::bail!("No manifest.toml or Dockerfile found in {}", dir.display());
    };

    let registry = std::env::var("EVERGREEN_REGISTRY")
        .unwrap_or_else(|_| "ghcr.io/wyattau/evergreenimageregistry".to_string());
    let full_ref = format!("{}/{}:{}", registry, name, version);

    println!("# Cosign signing commands for {}:{}", name, version);
    println!();
    println!("# 1. Sign the image (attaches signature to the image)");
    println!("cosign sign --yes {} \\", full_ref);
    println!(
        "  --annotation \"org.opencontainers.image.title={}\" \\",
        name
    );
    println!(
        "  --annotation \"org.opencontainers.image.version={}\" \\",
        version
    );
    // Parse manifest once for annotations (avoid double-parse)
    let (manifest_source, manifest_tier) = if manifest_path.exists() {
        match Manifest::from_file(&manifest_path) {
            Ok(m) => (
                m.source_url().to_string(),
                if m.metadata.tier.is_empty() {
                    "standard".to_string()
                } else {
                    m.metadata.tier.clone()
                },
            ),
            Err(_) => (String::new(), "standard".to_string()),
        }
    } else {
        (String::new(), "standard".to_string())
    };

    println!(
        "  --annotation \"org.opencontainers.image.source={}\" \\",
        if manifest_source.is_empty() {
            "https://github.com/WyattAu/EvergreenImageRegistry"
        } else {
            &manifest_source
        }
    );
    println!("  --annotation \"evergreen.image.tier={}\"", manifest_tier);
    println!();

    println!("# 2. Attach SBOM (SPDX format)");
    println!("cosign attach sbom --sbom spdx.json {}", full_ref);
    println!();

    println!("# 3. Generate and attach SBOM using syft");
    println!(
        "syft {} -o spdx-json > sbom-{}-{}.spdx.json",
        full_ref, name, version
    );
    println!(
        "cosign attach sbom --sbom sbom-{}-{}.spdx.json {}",
        name, version, full_ref
    );
    println!();

    println!("# 4. Verify the signature");
    println!("cosign verify --key cosign.pub {}", full_ref);
    println!();

    println!("# 5. Verify with SBOM");
    println!("cosign verify-attestation --key cosign.pub {}", full_ref);

    Ok(())
}

use crate::dockerfile_utils::{extract_base_image, extract_version};

#[cfg(test)]
mod tests {
    use crate::dockerfile_utils::{extract_base_image, extract_version};

    #[test]
    fn test_extract_version_basic() {
        let content = "FROM scratch\nARG VERSION=1.0.0\nRUN echo hi";
        assert_eq!(extract_version(content), Some("1.0.0".to_string()));
    }

    #[test]
    fn test_extract_version_no_version() {
        let content = "FROM scratch\nRUN echo hi";
        assert_eq!(extract_version(content), None);
    }

    #[test]
    fn test_extract_base_multistage() {
        let content = "FROM scratch AS builder\nRUN echo hi\nFROM scratch";
        assert_eq!(extract_base_image(content), "scratch");
    }

    #[test]
    fn test_extract_base_with_digest() {
        let content = "FROM cgr.dev/chainguard/wolfi-base:latest@sha256:abc123";
        assert_eq!(
            extract_base_image(content),
            "cgr.dev/chainguard/wolfi-base:latest@sha256:abc123"
        );
    }

    #[test]
    fn test_extract_base_no_from() {
        let content = "RUN echo hi";
        assert_eq!(extract_base_image(content), "scratch");
    }
}
