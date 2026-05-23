use anyhow::Result;
use std::path::Path;

pub fn cmd_validate_strict(images_dir: &str) -> Result<()> {
    let dir = Path::new(images_dir);
    if !dir.exists() {
        anyhow::bail!("Images directory not found: {}", images_dir);
    }

    let mut errors = Vec::new();
    let mut warnings = Vec::new();

    for entry in std::fs::read_dir(dir)? {
        let entry = entry?;
        let path = entry.path();
        if !path.is_dir() {
            continue;
        }

        let name = path
            .file_name()
            .unwrap_or_default()
            .to_string_lossy()
            .to_string();
        let manifest_path = path.join("manifest.toml");
        let dockerfile_path = path.join("Dockerfile");
        let sbom_path = path.join("sbom.spdx.json");

        if !manifest_path.exists() {
            warnings.push(format!("{}: missing manifest.toml", name));
            continue;
        }

        let manifest = match crate::manifest::Manifest::from_file(&manifest_path) {
            Ok(m) => m,
            Err(e) => {
                errors.push(format!("{}: manifest parse error: {}", name, e));
                continue;
            }
        };

        if manifest.name().is_empty() {
            errors.push(format!("{}: empty name in manifest", name));
        }
        if manifest.version().is_empty() {
            errors.push(format!("{}: empty version in manifest", name));
        }
        if manifest.source_url().is_empty() {
            warnings.push(format!("{}: no source URL configured", name));
        }

        if !dockerfile_path.exists() {
            errors.push(format!("{}: missing Dockerfile", name));
            continue;
        }

        let df_content = match std::fs::read_to_string(&dockerfile_path) {
            Ok(c) => c,
            Err(e) => {
                errors.push(format!("{}: failed to read Dockerfile: {}", name, e));
                continue;
            }
        };
        for line in df_content.lines() {
            if let Some(ver) = line.strip_prefix("ARG VERSION=") {
                let df_ver = ver.split_whitespace().next().unwrap_or("");
                let manifest_ver = manifest.version();
                if !df_ver.is_empty() && df_ver != manifest_ver {
                    errors.push(format!(
                        "{}: version mismatch (Dockerfile={}, manifest={})",
                        name, df_ver, manifest_ver
                    ));
                }
                break;
            }
        }

        if !sbom_path.exists() {
            warnings.push(format!("{}: missing sbom.spdx.json", name));
            continue;
        }

        let sbom: serde_json::Value = match std::fs::read(&sbom_path) {
            Ok(data) => serde_json::from_slice(&data)?,
            Err(e) => {
                errors.push(format!("{}: SBOM parse error: {}", name, e));
                continue;
            }
        };

        if sbom.get("spdxVersion").and_then(|v| v.as_str()) != Some("SPDX-2.3") {
            warnings.push(format!("{}: SBOM version not SPDX-2.3", name));
        }

        let has_user = df_content.contains("USER 65532") || df_content.contains("USER 65534");
        if !has_user && !df_content.contains("FROM scratch") {
            warnings.push(format!("{}: no non-root USER directive", name));
        }

        let mut from_lines = 0;
        let mut pinned_lines = 0;
        for line in df_content.lines() {
            if line.trim().starts_with("FROM ") {
                from_lines += 1;
                if line.contains("@sha256:") {
                    pinned_lines += 1;
                }
            }
        }
        if from_lines > 0 && pinned_lines == 0 {
            warnings.push(format!(
                "{}: 0/{} FROM lines digest-pinned",
                name, from_lines
            ));
        }

        if !df_content.contains("HEALTHCHECK") && !df_content.contains("FROM scratch") {
            warnings.push(format!("{}: no HEALTHCHECK instruction", name));
        }
    }

    println!("Strict Validation Results");
    println!("=====================");
    println!("Errors: {}", errors.len());
    println!("Warnings: {}", warnings.len());

    if !warnings.is_empty() {
        println!("\nWarnings:");
        for w in &warnings {
            println!("  [WARN] {}", w);
        }
    }

    if !errors.is_empty() {
        println!("\nErrors:");
        for e in &errors {
            println!("  [ERROR] {}", e);
        }
        anyhow::bail!(
            "{} validation errors, {} warnings",
            errors.len(),
            warnings.len()
        );
    }

    println!("\nAll images passed strict validation.");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_cmd_validate_strict_invalid_dir() {
        let result = cmd_validate_strict("/nonexistent");
        assert!(result.is_err());
    }
}
