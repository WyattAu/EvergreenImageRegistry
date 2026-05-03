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
            manifest.image.name.clone(),
            manifest.image.version.clone(),
            manifest.build.base.image.clone(),
        )
    } else if dockerfile_path.exists() {
        let content = std::fs::read_to_string(&dockerfile_path)
            .with_context(|| format!("Failed to read Dockerfile from {}", dockerfile_path.display()))?;
        let name = dir
            .file_name()
            .map(|n| n.to_string_lossy().to_string())
            .unwrap_or_else(|| "unknown".to_string());
        let version = extract_version_from_dockerfile(&content).unwrap_or_else(|| "latest".to_string());
        let base = extract_base_from_dockerfile(&content).unwrap_or_else(|| "unknown".to_string());
        (name, version, base)
    } else {
        anyhow::bail!(
            "No manifest.toml or Dockerfile found in {}",
            dir.display()
        );
    };

    let registry = "ghcr.io/evergreen";
    let full_ref = format!("{}/{}:{}", registry, name, version);

    println!("# Cosign signing commands for {}:{}", name, version);
    println!();
    println!("# 1. Sign the image (attaches signature to the image)");
    println!("cosign sign --yes {} \\", full_ref);
    println!("  --annotation \"org.opencontainers.image.title={}\" \\", name);
    println!("  --annotation \"org.opencontainers.image.version={}\" \\", version);
    println!("  --annotation \"org.opencontainers.image.source=\" \\");
    println!("  --annotation \"evergreen.image.tier=\"");
    println!();

    println!("# 2. Attach SBOM (SPDX format)");
    println!("cosign attach sbom --sbom spdx.json {}", full_ref);
    println!();

    println!("# 3. Generate and attach SBOM using syft");
    println!("syft {} -o spdx-json > sbom-{}-{}.spdx.json", full_ref, name, version);
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

fn extract_version_from_dockerfile(content: &str) -> Option<String> {
    for line in content.lines() {
        let line = line.trim();
        if line.starts_with("ARG VERSION=") {
            let ver = line.strip_prefix("ARG VERSION=")?.trim().to_string();
            return Some(ver);
        }
    }
    None
}

fn extract_base_from_dockerfile(content: &str) -> Option<String> {
    for line in content.lines() {
        let line = line.trim();
        if line.starts_with("FROM ") && !line.contains(" AS ") {
            let base = line.strip_prefix("FROM ")?.split_whitespace().next()?.to_string();
            return Some(base);
        }
    }
    None
}
