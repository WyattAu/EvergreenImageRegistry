// =============================================================================
// Evergreenctl - Shared Dockerfile Parsing Utilities
// =============================================================================
// Consolidates duplicated Dockerfile extraction functions previously scattered
// across drift.rs, sign.rs, bump.rs, and migrate.rs.
//
// All functions operate on &str content (no filesystem I/O) to enable unit
// testing and composition. For file-based extraction, see the convenience
// wrappers at the bottom of this module.
// =============================================================================

use anyhow::{Context, Result};
use std::path::{Path, PathBuf};

use crate::patterns::*;

// ---------------------------------------------------------------------------
// Core extraction functions (operate on &str content)
// ---------------------------------------------------------------------------

/// Extract the version string from `ARG VERSION=...` in a Dockerfile.
///
/// Returns `None` if no VERSION arg is found.
pub fn extract_version(content: &str) -> Option<String> {
    RE_ARG_VERSION
        .captures(content)
        .and_then(|c| c.get(1))
        .map(|m| m.as_str().to_string())
}

/// Extract the final-stage base image from `FROM` directives.
///
/// Iterates all `FROM` lines and returns the last one (the runtime stage).
/// Returns `"scratch"` if no FROM is found.
pub fn extract_base_image(content: &str) -> String {
    RE_FROM_IMAGE
        .captures_iter(content)
        .last()
        .and_then(|c| c.get(1))
        .map(|m| m.as_str().to_string())
        .unwrap_or_else(|| "scratch".to_string())
}

/// Extract the USER directive from a Dockerfile.
///
/// Returns the last USER directive (runtime stage). Defaults to `"65532:65532"`.
pub fn extract_user(content: &str) -> String {
    RE_USER
        .captures_iter(content)
        .last()
        .and_then(|c| c.get(1))
        .map(|m| m.as_str().to_string())
        .unwrap_or_else(|| "65532:65532".to_string())
}

/// Extract the STOPSIGNAL directive from a Dockerfile.
///
/// Returns `"SIGTERM"` if not found.
pub fn extract_stop_signal(content: &str) -> String {
    RE_STOPSIGNAL
        .captures(content)
        .and_then(|c| c.get(1))
        .map(|m| m.as_str().to_string())
        .unwrap_or_else(|| "SIGTERM".to_string())
}

/// Extract the OCI description label value.
///
/// Returns `"Evergreen hardened container image"` if not found.
pub fn extract_description(content: &str) -> String {
    RE_DESCRIPTION_LABEL
        .captures(content)
        .and_then(|c| c.get(1))
        .map(|m| m.as_str().to_string())
        .unwrap_or_else(|| "Evergreen hardened container image".to_string())
}

/// Extract the OCI vendor label value.
///
/// Returns `"Unknown"` if not found.
pub fn extract_vendor(content: &str) -> String {
    RE_VENDOR_LABEL
        .captures(content)
        .and_then(|c| c.get(1))
        .map(|m| m.as_str().to_string())
        .unwrap_or_else(|| "Unknown".to_string())
}

/// Extract the evergreen tier label value as a u8.
///
/// Returns `3` (lowest tier) if not found or unparseable.
pub fn extract_tier(content: &str) -> u8 {
    RE_TIER_LABEL
        .captures(content)
        .and_then(|c| c.get(1))
        .and_then(|m| m.as_str().parse::<u8>().ok())
        .unwrap_or(3)
}

/// Extract a GitHub source URL (owner/repo format) from label values.
///
/// Returns `None` if no GitHub URL is found.
pub fn extract_github_source(content: &str) -> Option<String> {
    RE_GITHUB_SOURCE
        .captures(content)
        .and_then(|c| c.get(0))
        .map(|m| m.as_str().trim_end_matches('/').to_string())
}

/// Extract the download URL from curl/wget commands.
///
/// Returns `None` if no download command is found.
pub fn extract_download_url(content: &str) -> Option<String> {
    RE_DOWNLOAD_URL
        .captures(content)
        .and_then(|c| c.get(1))
        .map(|m| m.as_str().to_string())
}

/// Extract EXPOSE ports from a Dockerfile.
///
/// Returns a sorted, deduplicated list of port strings.
pub fn extract_ports(content: &str) -> Vec<String> {
    let mut ports = Vec::new();
    for cap in RE_EXPOSE_PORTS.captures_iter(content) {
        for part in cap[1].split_whitespace() {
            if let Some(port_str) = part.split('/').next() {
                if let Ok(port) = port_str.parse::<u16>() {
                    ports.push(port.to_string());
                }
            }
        }
    }
    ports.sort();
    ports.dedup();
    ports
}

/// Extract ENTRYPOINT exec form arguments.
///
/// Returns a vec of strings from `ENTRYPOINT ["arg1", "arg2"]`.
/// Falls back to `["/app/entrypoint"]` if no ENTRYPOINT is found.
pub fn extract_entrypoint(content: &str) -> Vec<String> {
    RE_ENTRYPOINT
        .captures(content)
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

/// Determine the source build type from Dockerfile content.
///
/// Classifies as: `"package-manager"`, `"source-build"`, `"binary-download"`,
/// or `"copy-from"`.
pub fn extract_source_type(content: &str) -> String {
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

/// Extract all key="value" label pairs from a Dockerfile.
///
/// Only includes labels with a `.` in the key (OCI-style labels).
pub fn extract_all_labels(content: &str) -> std::collections::HashMap<String, String> {
    let mut labels = std::collections::HashMap::new();
    for cap in RE_KEY_VALUE_LABEL.captures_iter(content) {
        let key = cap[1].to_string();
        let val = cap[2].to_string();
        // Only include meaningful labels (skip build-time instructions)
        if key.contains('.') && !key.starts_with("ARG") {
            labels.insert(key, val);
        }
    }
    labels
}

// ---------------------------------------------------------------------------
// Convenience file-based wrappers
// ---------------------------------------------------------------------------

/// Read a Dockerfile and extract the version from ARG VERSION=.
///
/// Returns an error if the file cannot be read or no version is found.
pub fn extract_version_from_file(path: &Path) -> Result<String> {
    let content = std::fs::read_to_string(path)
        .with_context(|| format!("Failed to read Dockerfile: {}", path.display()))?;
    extract_version(&content)
        .with_context(|| format!("No ARG VERSION found in {}", path.display()))
}

/// Read a Dockerfile and extract the base image from the final FROM.
///
/// Returns an error if the file cannot be read.
pub fn extract_base_from_file(path: &Path) -> Result<String> {
    let content = std::fs::read_to_string(path)
        .with_context(|| format!("Failed to read Dockerfile: {}", path.display()))?;
    Ok(extract_base_image(&content))
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// Image directory iterator
// ---------------------------------------------------------------------------

/// Represents a discovered image directory with its key files.
pub struct ImageDir {
    pub name: String,
    pub path: PathBuf,
    pub manifest_path: Option<PathBuf>,
    pub dockerfile_path: Option<PathBuf>,
    pub sbom_path: Option<PathBuf>,
}

impl ImageDir {
    /// Load the manifest from this image directory.
    ///
    /// Returns `None` if no manifest.toml exists, or an error if parsing fails.
    pub fn manifest(&self) -> Option<Result<crate::manifest::Manifest>> {
        self.manifest_path.as_ref().map(|p| {
            crate::manifest::Manifest::from_file(p)
                .with_context(|| format!("Failed to parse manifest for {}", self.name))
        })
    }

    /// Read the Dockerfile content for this image directory.
    ///
    /// Returns `None` if no Dockerfile exists, or an error if reading fails.
    pub fn dockerfile_content(&self) -> Option<Result<String>> {
        self.dockerfile_path.as_ref().map(|p| {
            std::fs::read_to_string(p)
                .with_context(|| format!("Failed to read Dockerfile for {}", self.name))
        })
    }
}

/// Iterate over image subdirectories in a root directory.
///
/// Yields `ImageDir` entries sorted by name. Non-directory entries and
/// directories without a Dockerfile are skipped.
pub fn iter_image_dirs(images_dir: &Path) -> Result<Vec<ImageDir>> {
    let mut dirs = Vec::new();
    for entry in std::fs::read_dir(images_dir)
        .with_context(|| format!("Failed to read directory: {}", images_dir.display()))?
    {
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

        // Skip directories without a Dockerfile
        if !dockerfile_path.exists() {
            continue;
        }

        dirs.push(ImageDir {
            name,
            path,
            manifest_path: manifest_path.exists().then_some(manifest_path),
            dockerfile_path: Some(dockerfile_path),
            sbom_path: sbom_path.exists().then_some(sbom_path),
        });
    }
    dirs.sort_by(|a, b| a.name.cmp(&b.name));
    Ok(dirs)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_extract_version_basic() {
        assert_eq!(extract_version("ARG VERSION=1.0.0"), Some("1.0.0".to_string()));
    }

    #[test]
    fn test_extract_version_quoted() {        assert_eq!(extract_version("ARG VERSION=\"2.0.0\""), Some("2.0.0".to_string()));
    }

    #[test]
    fn test_extract_version_missing() {
        assert_eq!(extract_version("FROM scratch"), None);
    }

    #[test]
    fn test_extract_base_image_single_from() {
        assert_eq!(
            extract_base_image("FROM cgr.dev/chainguard/wolfi-base:latest"),
            "cgr.dev/chainguard/wolfi-base:latest"
        );
    }

    #[test]
    fn test_extract_base_image_multistage() {
        let content = "FROM golang:1.23 AS builder\nRUN go build\nFROM scratch";
        assert_eq!(extract_base_image(content), "scratch");
    }

    #[test]
    fn test_extract_base_image_with_digest() {
        let content = "FROM cgr.dev/chainguard/wolfi-base:latest@sha256:abc123";
        assert_eq!(
            extract_base_image(content),
            "cgr.dev/chainguard/wolfi-base:latest@sha256:abc123"
        );
    }

    #[test]
    fn test_extract_base_image_empty() {
        assert_eq!(extract_base_image(""), "scratch");
    }

    #[test]
    fn test_extract_user_basic() {
        assert_eq!(extract_user("USER 65532:65532"), "65532:65532");
    }

    #[test]
    fn test_extract_user_last_wins() {
        let content = "USER root\nRUN something\nUSER 65532";
        assert_eq!(extract_user(content), "65532");
    }

    #[test]
    fn test_extract_user_missing() {
        assert_eq!(extract_user("FROM scratch"), "65532:65532");
    }

    #[test]
    fn test_extract_stop_signal_basic() {
        assert_eq!(extract_stop_signal("STOPSIGNAL SIGTERM"), "SIGTERM");
    }

    #[test]
    fn test_extract_stop_signal_missing() {
        assert_eq!(extract_stop_signal("FROM scratch"), "SIGTERM");
    }

    #[test]
    fn test_extract_description_basic() {
        let content = "LABEL org.opencontainers.image.description=\"Redis in-memory store\"";
        assert_eq!(
            extract_description(content),
            "Redis in-memory store"
        );
    }

    #[test]
    fn test_extract_description_missing() {
        assert_eq!(
            extract_description("FROM scratch"),
            "Evergreen hardened container image"
        );
    }

    #[test]
    fn test_extract_vendor_basic() {
        let content = "LABEL org.opencontainers.image.vendor=\"Redis\"";
        assert_eq!(extract_vendor(content), "Redis");
    }

    #[test]
    fn test_extract_vendor_missing() {
        assert_eq!(extract_vendor("FROM scratch"), "Unknown");
    }

    #[test]
    fn test_extract_tier_basic() {
        let content = "LABEL evergreen.image.tier=\"1\"";
        assert_eq!(extract_tier(content), 1);
    }

    #[test]
    fn test_extract_tier_missing() {
        assert_eq!(extract_tier("FROM scratch"), 3);
    }

    #[test]
    fn test_extract_github_source_basic() {
        let content = "LABEL org.opencontainers.image.source=\"https://github.com/test/repo\"";
        assert_eq!(
            extract_github_source(content),
            Some("https://github.com/test/repo".to_string())
        );
    }

    #[test]
    fn test_extract_github_source_missing() {
        assert_eq!(extract_github_source("FROM scratch"), None);
    }

    #[test]
    fn test_extract_download_url_basic() {
        let content = "RUN curl -fsSL \"https://example.com/app.tar.gz\" -o /tmp/app.tar.gz";
        assert_eq!(
            extract_download_url(content),
            Some("https://example.com/app.tar.gz".to_string())
        );
    }

    #[test]
    fn test_extract_download_url_missing() {
        assert_eq!(extract_download_url("RUN echo hi"), None);
    }

    #[test]
    fn test_extract_ports_single() {
        assert_eq!(extract_ports("EXPOSE 8080"), vec!["8080".to_string()]);
    }

    #[test]
    fn test_extract_ports_multiple() {
        let ports = extract_ports("EXPOSE 8080 9090");
        assert!(ports.contains(&"8080".to_string()));
        assert!(ports.contains(&"9090".to_string()));
    }

    #[test]
    fn test_extract_ports_with_protocol() {
        assert_eq!(extract_ports("EXPOSE 8080/tcp"), vec!["8080".to_string()]);
    }

    #[test]
    fn test_extract_entrypoint_basic() {
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
    fn test_extract_entrypoint_missing() {
        assert_eq!(
            extract_entrypoint("FROM scratch"),
            vec!["/app/entrypoint".to_string()]
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
            extract_source_type("RUN git clone --depth 1 https://github.com/test/repo.git /src"),
            "source-build"
        );
    }

    #[test]
    fn test_extract_source_type_binary_download() {
        assert_eq!(
            extract_source_type("RUN curl -fsSL https://example.com/app.tar.gz"),
            "binary-download"
        );
    }

    #[test]
    fn test_extract_source_type_copy_from() {
        assert_eq!(
            extract_source_type("COPY --from=quay.io/app:latest /app /app"),
            "copy-from"
        );
    }

    #[test]
    fn test_extract_all_labels() {
        let content = "LABEL org.opencontainers.image.title=\"test\" version=\"1.0\"";
        let labels = extract_all_labels(content);
        assert_eq!(
            labels.get("org.opencontainers.image.title"),
            Some(&"test".to_string())
        );
        // "version" doesn't contain a dot, so it's excluded
        assert!(!labels.contains_key("version"));
    }

    #[test]
    fn test_extract_version_from_file() {
        let dir = std::env::temp_dir().join("evergreen_utils_test");
        let _ = std::fs::create_dir_all(&dir);
        let path = dir.join("Dockerfile");
        std::fs::write(&path, "FROM scratch\nARG VERSION=3.2.1\n").unwrap();
        assert_eq!(extract_version_from_file(&path).unwrap(), "3.2.1");
        let _ = std::fs::remove_file(&path);
    }

    #[test]
    fn test_extract_version_from_file_missing_version() {
        let dir = std::env::temp_dir().join("evergreen_utils_test2");
        let _ = std::fs::create_dir_all(&dir);
        let path = dir.join("Dockerfile");
        std::fs::write(&path, "FROM scratch\n").unwrap();
        assert!(extract_version_from_file(&path).is_err());
        let _ = std::fs::remove_file(&path);
    }

    #[test]
    fn test_extract_base_from_file() {
        let dir = std::env::temp_dir().join("evergreen_utils_test3");
        let _ = std::fs::create_dir_all(&dir);
        let path = dir.join("Dockerfile");
        std::fs::write(&path, "FROM golang:1.23 AS builder\nFROM scratch\n").unwrap();
        assert_eq!(extract_base_from_file(&path).unwrap(), "scratch");
        let _ = std::fs::remove_file(&path);
    }
}
