use std::path::Path;
use anyhow::{Result, Context};
use regex::Regex;
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
        .unwrap_or_else(|| "Sovereign hardened container image".to_string())
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
    let github_repo = extract_github_repo_from_dockerfile(&content);
    let base_image = extract_base_image(&content);
    let category = extract_category(&content);
    let health_type = extract_health_type(&content);
    let stop_signal = extract_stop_signal(&content);

    // Determine image type from Dockerfile patterns
    let image_type = determine_image_type(&content);

    // Determine base image hierarchy
    let build_base = determine_base_image(&base_image, &image_type);

    // Determine runtime packages
    let runtime_packages = extract_runtime_packages(&content);

    // Build artifacts (COPY --from=builder)
    let artifacts = extract_artifacts(&content);

    // Build commands
    let build_commands = extract_build_commands(&content);

    // Compliance labels
    let compliance = extract_compliance_labels(&content);

    // Determine workdir
    let workdir = extract_workdir(&content);

    Ok(Manifest {
        image: ImageMeta {
            name: image_name.to_string(),
            image_type,
            tier,
            version: version.clone(),
            description,
            vendor,
            source_url: github_repo.clone().map(|r| format!("https://github.com/{}", r)),
            category: Some(category),
        },
        source: Source {
            url: download_url.unwrap_or_else(|| format!("https://example.com/{}/{}.tar.gz", image_name, version)),
            fallback_urls: vec![],
            checksum: Checksum {
                algorithm: "sha256".to_string(),
                expected: String::new(),  // Needs to be populated
                source: String::new(),
            },
            strategy: DownloadStrategy::Curl,
            github_repo,
        },
        build: BuildConfig {
            base: build_base,
            stages: vec![],
            env: std::collections::HashMap::new(),
            builder_packages: vec![],
            runtime_packages,
            build_args: std::collections::HashMap::new(),
            pre_build_commands: vec![],
            build_commands,
            post_build_commands: vec![],
            artifacts,
        },
        runtime: RuntimeConfig {
            user: "65532:65532".to_string(),
            workdir,
            entrypoint,
            cmd: vec![],
            ports,
            volumes: vec![],
            stop_signal,
            env: std::collections::HashMap::new(),
        },
        health: HealthConfig {
            health_type,
            path: String::new(),
            port: None,
            interval_seconds: 30,
            timeout_seconds: 5,
            retries: 3,
        },
        observability: ObservabilityConfig {
            metrics_port: 9101,
            metrics_path: "/metrics".to_string(),
        },
        compliance,
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
    let re = Regex::new(r#"sovereign\.image\.tier="(\d+)""#).unwrap();
    re.captures(content)
        .and_then(|c| c.get(1))
        .and_then(|m| m.as_str().parse::<u8>().ok())
        .unwrap_or(3)
}

fn extract_github_repo_from_dockerfile(content: &str) -> Option<String> {
    let re = Regex::new(r#"github\.com/([^/""\s]+/[^/""\s]+)"#).unwrap();
    re.captures(content)
        .and_then(|c| c.get(1))
        .map(|m| {
            m.as_str()
                .trim_end_matches(".git")
                .trim_end_matches('/')
                .to_string()
        })
}

fn extract_base_image(content: &str) -> String {
    // Get the last FROM line (runtime stage)
    let re = Regex::new(r"FROM\s+([\S]+)").unwrap();
    re.captures_iter(content)
        .last()
        .and_then(|c| c.get(1))
        .map(|m| m.as_str().to_string())
        .unwrap_or_else(|| "scratch".to_string())
}

fn extract_category(content: &str) -> String {
    let re = Regex::new(r#"sovereign\.image\.category="([^"]+)""#).unwrap();
    re.captures(content)
        .and_then(|c| c.get(1))
        .map(|m| m.as_str().to_string())
        .unwrap_or_else(|| "other".to_string())
}

fn extract_health_type(content: &str) -> String {
    let re = Regex::new(r#"sovereign\.health\.type="([^"]+)""#).unwrap();
    re.captures(content)
        .and_then(|c| c.get(1))
        .map(|m| m.as_str().to_string())
        .unwrap_or_else(|| "none".to_string())
}

fn extract_stop_signal(content: &str) -> String {
    let re = Regex::new(r"STOPSIGNAL\s+(\S+)").unwrap();
    re.captures(content)
        .and_then(|c| c.get(1))
        .map(|m| m.as_str().to_string())
        .unwrap_or_else(|| "SIGTERM".to_string())
}

fn extract_runtime_packages(content: &str) -> Vec<String> {
    let mut packages = Vec::new();
    // Look for apk add in the last FROM stage
    let re = Regex::new(r"apk\s+add\s+--no-cache\s+([^\n|]+)").unwrap();
    if let Some(cap) = re.captures_iter(content).last() {
        for pkg in cap[1].split_whitespace() {
            packages.push(pkg.to_string());
        }
    }
    packages
}

fn extract_artifacts(content: &str) -> Vec<Artifact> {
    let re = Regex::new(r"COPY\s+--from=\S+\s+(\S+)\s+(\S+)").unwrap();
    re.captures_iter(content)
        .map(|cap| Artifact {
            source: cap[1].to_string(),
            destination: cap[2].to_string(),
        })
        .collect()
}

fn extract_build_commands(content: &str) -> Vec<String> {
    // Extract non-boilerplate RUN commands from builder stages
    let commands = Vec::new();
    let _in_builder = false;

    for line in content.lines() {
        let trimmed = line.trim();
        if trimmed.starts_with("FROM") && (trimmed.contains("builder") || trimmed.contains("debian") || trimmed.contains("golang") || trimmed.contains("rust")) {
            // Builder stage
        }
    }
    commands
}

fn extract_compliance_labels(content: &str) -> ComplianceConfig {
    let mut labels = std::collections::HashMap::new();
    let re = Regex::new(r#"sovereign\.([a-zA-Z0-9_.]+)="([^"]+)""#).unwrap();
    for cap in re.captures_iter(content) {
        labels.insert(cap[1].to_string(), cap[2].to_string());
    }
    ComplianceConfig {
        standards: vec![],
        labels,
    }
}

fn extract_workdir(content: &str) -> String {
    let re = Regex::new(r"WORKDIR\s+(\S+)").unwrap();
    re.captures_iter(content)
        .last()
        .and_then(|c| c.get(1))
        .map(|m| m.as_str().to_string())
        .unwrap_or_else(|| "/app".to_string())
}

fn determine_image_type(content: &str) -> ImageType {
    if content.contains("go build") || content.contains("golang:") {
        ImageType::SourceBuildGo
    } else if content.contains("cargo build") || content.contains("rust:") {
        ImageType::SourceBuildRust
    } else if content.contains("cmake") || content.contains("make -j") || content.contains("gcc") {
        ImageType::SourceBuildC
    } else if content.contains("npm install") || content.contains("nodejs") {
        ImageType::NodeNpm
    } else if content.contains("pip install") || content.contains("python3") {
        ImageType::PythonPip
    } else if content.contains("java") || content.contains("jdk") || content.contains(".jar") {
        ImageType::SourceBuildJava
    } else if content.contains("index.html") || content.contains("www-src") {
        ImageType::WebUi
    } else {
        ImageType::BinaryDownload
    }
}

fn determine_base_image(current_base: &str, image_type: &ImageType) -> BaseImage {
    if current_base.contains("scratch") {
        return BaseImage {
            image: "scratch".to_string(),
            purpose: "Minimal static binary".to_string(),
        };
    }
    match image_type {
        ImageType::SourceBuildJava => BaseImage {
            image: "cgr.dev/chainguard/wolfi-base:latest".to_string(),
            purpose: "JVM runtime".to_string(),
        },
        ImageType::NodeNpm => BaseImage {
            image: "cgr.dev/chainguard/wolfi-base:latest".to_string(),
            purpose: "Node.js runtime".to_string(),
        },
        ImageType::PythonPip => BaseImage {
            image: "cgr.dev/chainguard/wolfi-base:latest".to_string(),
            purpose: "Python runtime".to_string(),
        },
        _ => BaseImage {
            image: "cgr.dev/chainguard/wolfi-base:latest".to_string(),
            purpose: "Minimal runtime".to_string(),
        },
    }
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
