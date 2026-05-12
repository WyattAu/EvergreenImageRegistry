use anyhow::{Context, Result};
use regex::Regex;
use std::collections::HashMap;
use std::path::Path;
use tracing::{info, warn};

use crate::manifest::*;

fn extract_download_url(content: &str) -> Option<String> {
    let re = Regex::new("(?:curl|wget)\\s+[^\"]*\"?(https?://[^\"'\\s]+)\"?").unwrap();
    re.captures(content)
        .and_then(|c| c.get(1))
        .map(|m| m.as_str().to_string())
}

fn extract_ports(content: &str) -> Vec<u16> {
    let re = Regex::new(r"EXPOSE\s+([\d\s/]+)").unwrap();
    let mut ports = Vec::new();
    for cap in re.captures_iter(content) {
        for part in cap[1].split_whitespace() {
            if let Some(port_str) = part.split('/').next() {
                if let Ok(port) = port_str.parse::<u16>() {
                    ports.push(port);
                }
            }
        }
    }
    ports.sort();
    ports.dedup();
    ports
}

fn extract_entrypoint(content: &str) -> Vec<String> {
    let re = Regex::new(r"ENTRYPOINT\s+\[([^\]]+)\]").unwrap();
    re.captures(content)
        .and_then(|c| c.get(1))
        .map(|m| {
            m.as_str()
                .split(',')
                .map(|s| s.trim().trim_matches('"').to_string())
                .filter(|s| !s.is_empty())
                .collect()
        })
        .unwrap_or_else(|| vec!["/app/entrypoint".to_string()])
}

fn extract_description(content: &str) -> String {
    let re = Regex::new(r#"org\.opencontainers\.image\.description="([^"]+)""#).unwrap();
    re.captures(content)
        .and_then(|c| c.get(1))
        .map(|m| m.as_str().to_string())
        .unwrap_or_else(|| "Evergreen hardened container image".to_string())
}

fn extract_source_type(content: &str) -> String {
    if content.contains("apk add") || content.contains("apt-get install") {
        "package-manager".to_string()
    } else if content.contains("git clone") {
        "source-build".to_string()
    } else if content.contains("curl ") || content.contains("wget ") {
        "binary-download".to_string()
    } else {
        "copy-from".to_string()
    }
}

/// Parse an existing Dockerfile and extract manifest fields
pub fn dockerfile_to_manifest(dockerfile_path: &Path, image_name: &str) -> Result<Manifest> {
    let content = std::fs::read_to_string(dockerfile_path)
        .with_context(|| format!("Failed to read Dockerfile: {}", dockerfile_path.display()))?;

    let version = extract_version(&content);
    let download_url = extract_download_url(&content);
    let ports = extract_ports(&content);
    let entrypoint = extract_entrypoint(&content);
    let description = extract_description(&content);
    let vendor = extract_vendor(&content);
    let tier = extract_tier(&content);
    let github_source = extract_github_source(&content);
    let runtime_base_image = extract_base_image(&content);
    let stop_signal = extract_stop_signal(&content);
    let source_type = extract_source_type(&content);
    let labels = extract_all_labels(&content);

    // Derive build base (for images that are scratch or use specific base)
    let build_base = if runtime_base_image.contains("scratch") {
        "scratch".to_string()
    } else if runtime_base_image.contains("wolfi") {
        runtime_base_image.clone()
    } else {
        // Default to wolfi-base for all others
        "cgr.dev/chainguard/wolfi-base:latest".to_string()
    };

    // Determine build user (default to wolfi standard)
    let build_user = extract_user(&content);

    Ok(Manifest {
        metadata: Metadata {
            name: image_name.to_string(),
            version,
            description,
            vendor,
            source: github_source.unwrap_or_default(),
            license: String::new(),
            tier: tier.to_string(),
        },
        build: Build {
            base: build_base,
            user: build_user,
            stopsignal: stop_signal,
        },
        source: SourceSection {
            source_type,
            url: download_url
                .unwrap_or_else(|| format!("https://example.com/{}/latest.tar.gz", image_name)),
        },
        runtime: RuntimeSection { entrypoint },
        ports: PortsSection { expose: ports },
        labels,
    })
}

fn extract_version(content: &str) -> String {
    let re = Regex::new(r#"ARG\s+VERSION="?([^"\s]+)"?"#).unwrap();
    re.captures(content)
        .and_then(|c| c.get(1))
        .map(|m| m.as_str().to_string())
        .unwrap_or_else(|| "0.0.0".to_string())
}

fn extract_vendor(content: &str) -> String {
    let re = Regex::new(r#"org\.opencontainers\.image\.vendor="([^"]+)""#).unwrap();
    re.captures(content)
        .and_then(|c| c.get(1))
        .map(|m| m.as_str().to_string())
        .unwrap_or_else(|| "Unknown".to_string())
}

fn extract_tier(content: &str) -> u8 {
    let re = Regex::new(r#"evergreen\.image\.tier="(\d+)""#).unwrap();
    re.captures(content)
        .and_then(|c| c.get(1))
        .and_then(|m| m.as_str().parse::<u8>().ok())
        .unwrap_or(3)
}

fn extract_github_source(content: &str) -> Option<String> {
    let re = Regex::new(r#"https?://github\.com/([^/""\s]+/[^/""\s]+)"#).unwrap();
    re.captures(content)
        .and_then(|c| c.get(0))
        .map(|m| m.as_str().trim_end_matches('/').to_string())
}

fn extract_base_image(content: &str) -> String {
    let re = Regex::new(r"FROM\s+([\S]+)").unwrap();
    re.captures_iter(content)
        .last()
        .and_then(|c| c.get(1))
        .map(|m| m.as_str().to_string())
        .unwrap_or_else(|| "scratch".to_string())
}

fn extract_user(content: &str) -> String {
    let re = Regex::new(r"USER\s+(\S+)").unwrap();
    re.captures_iter(content)
        .last()
        .and_then(|c| c.get(1))
        .map(|m| m.as_str().to_string())
        .unwrap_or_else(|| "65532:65532".to_string())
}

fn extract_stop_signal(content: &str) -> String {
    let re = Regex::new(r"STOPSIGNAL\s+(\S+)").unwrap();
    re.captures(content)
        .and_then(|c| c.get(1))
        .map(|m| m.as_str().to_string())
        .unwrap_or_else(|| "SIGTERM".to_string())
}

fn extract_all_labels(content: &str) -> HashMap<String, String> {
    let mut labels = HashMap::new();
    let re = Regex::new(r#"([a-zA-Z0-9_.-]+)="([^"]+)""#).unwrap();
    for cap in re.captures_iter(content) {
        let key = cap[1].to_string();
        let val = cap[2].to_string();
        // Only include meaningful labels (skip build-time instructions)
        if key.contains('.') && !key.starts_with("ARG") {
            labels.insert(key, val);
        }
    }
    labels
}

/// Migrate all images: generate manifests from existing Dockerfiles
pub fn migrate_all(images_dir: &Path, dry_run: bool) -> Result<Vec<String>> {
    let mut migrated = Vec::new();

    for entry in std::fs::read_dir(images_dir)? {
        let entry = entry?;
        let dockerfile = entry.path().join("Dockerfile");
        if !dockerfile.exists() {
            continue;
        }

        let name = entry.file_name().to_string_lossy().to_string();
        let manifest_path = entry.path().join("manifest.toml");

        match dockerfile_to_manifest(&dockerfile, &name) {
            Ok(manifest) => {
                if dry_run {
                    info!("[DRY-RUN] Would generate manifest for: {}", name);
                } else {
                    manifest.to_file(&manifest_path)?;
                    info!("Generated manifest for: {}", name);
                }
                migrated.push(name);
            }
            Err(e) => {
                warn!("Failed to migrate {}: {}", name, e);
            }
        }
    }

    Ok(migrated)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_extract_version() {
        assert_eq!(extract_version("ARG VERSION=1.0.0"), "1.0.0");
        assert_eq!(extract_version("ARG VERSION=\"2.0.0\""), "2.0.0");
        assert_eq!(extract_version("FROM scratch"), "0.0.0");
    }

    #[test]
    fn test_extract_ports_single() {
        assert_eq!(extract_ports("EXPOSE 8080"), vec![8080]);
    }

    #[test]
    fn test_extract_ports_multiple() {
        let ports = extract_ports("EXPOSE 8080 9090");
        assert!(ports.contains(&8080));
        assert!(ports.contains(&9090));
    }

    #[test]
    fn test_extract_ports_with_protocol() {
        assert_eq!(extract_ports("EXPOSE 8080/tcp"), vec![8080]);
    }

    #[test]
    fn test_extract_entrypoint() {
        assert_eq!(
            extract_entrypoint("ENTRYPOINT [\"/app\", \"--flag\"]"),
            vec!["/app".to_string(), "--flag".to_string()]
        );
    }

    #[test]
    fn test_extract_entrypoint_single() {
        assert_eq!(
            extract_entrypoint("ENTRYPOINT [\"/binary\"]"),
            vec!["/binary".to_string()]
        );
    }

    #[test]
    fn test_extract_source_type_binary() {
        assert_eq!(
            extract_source_type("RUN curl -fsSL \"https://example.com/file.tar.gz\""),
            "binary-download"
        );
    }

    #[test]
    fn test_extract_source_type_package_manager() {
        assert_eq!(
            extract_source_type("RUN apk add --no-cache curl"),
            "package-manager"
        );
    }

    #[test]
    fn test_extract_source_type_source_build() {
        assert_eq!(
            extract_source_type("RUN git clone --depth 1 https://github.com/owner/repo.git /src"),
            "source-build"
        );
    }

    #[test]
    fn test_extract_base_image() {
        assert_eq!(
            extract_base_image(
                "FROM scratch AS builder\nRUN echo hi\nFROM cgr.dev/chainguard/wolfi-base:latest"
            ),
            "cgr.dev/chainguard/wolfi-base:latest"
        );
    }

    #[test]
    fn test_dockerfile_to_manifest_basic() {
        let dir = std::env::temp_dir().join("evergreen_migrate_test");
        let _ = std::fs::create_dir_all(&dir);
        let df_path = dir.join("Dockerfile");
        let content = r#"# Test Dockerfile
FROM cgr.dev/chainguard/wolfi-base:latest AS builder
ARG VERSION=1.0.0
RUN curl -fsSL "https://github.com/test/app/releases/download/v1.0.0/app.tar.gz" -o /app.tar.gz

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=1.0.0
COPY --from=builder /opt/ /opt/
USER 65532:65532
EXPOSE 8080
ENTRYPOINT ["/app"]
STOPSIGNAL SIGTERM
LABEL org.opencontainers.image.title="test-app"
LABEL org.opencontainers.image.version="1.0.0"
LABEL evergreen.image.tier="1"
LABEL evergreen.health.type="http"
"#;
        std::fs::write(&df_path, content).unwrap();
        let manifest = dockerfile_to_manifest(&df_path, "test-app").unwrap();

        assert_eq!(manifest.name(), "test-app");
        assert_eq!(manifest.version(), "1.0.0");
        assert_eq!(
            manifest.base_image(),
            "cgr.dev/chainguard/wolfi-base:latest"
        );
        assert_eq!(manifest.user(), "65532:65532");
        assert_eq!(manifest.stop_signal(), "SIGTERM");
        assert_eq!(&manifest.entrypoint(), &["/app".to_string()]);
        assert_eq!(manifest.exposed_ports(), &[8080]);
        assert_eq!(manifest.source.source_type, "binary-download");
        assert_eq!(manifest.metadata.tier, "1");
    }
}
