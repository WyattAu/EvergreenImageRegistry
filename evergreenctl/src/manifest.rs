use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::path::Path;

use crate::error::{EvergreenError, Result};

/// Manifest representation matching the actual TOML format used in the registry.
///
/// The TOML structure is:
/// ```toml
/// [metadata]
/// name = "redis"
/// version = "7.4.1"
/// description = "..."
/// vendor = "..."
/// source = "https://github.com/redis/redis"
/// license = "BSD-3-Clause"
/// tier = "1"
///
/// [build]
/// base = "cgr.dev/chainguard/wolfi-base:latest"
/// user = "65532:65532"
/// stopsignal = "SIGTERM"
///
/// [source]
/// type = "package-manager"
/// url = "https://github.com/redis/redis/archive/..."
///
/// [runtime]
/// entrypoint = ["sh", "-c", "redis"]
///
/// [ports]
/// expose = [6379, 9101]
///
/// [labels]
/// "org.opencontainers.image.title" = "redis"
/// ```
#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Manifest {
    #[serde(default)]
    pub metadata: Metadata,
    #[serde(default)]
    pub build: Build,
    #[serde(default)]
    pub source: SourceSection,
    #[serde(default)]
    pub runtime: RuntimeSection,
    #[serde(default)]
    pub ports: PortsSection,
    #[serde(default)]
    pub labels: HashMap<String, String>,
}

#[derive(Debug, Serialize, Deserialize, Clone, Default)]
pub struct Metadata {
    #[serde(default)]
    pub name: String,
    #[serde(default)]
    pub version: String,
    #[serde(default)]
    pub description: String,
    #[serde(default)]
    pub vendor: String,
    #[serde(default)]
    pub source: String,
    #[serde(default)]
    pub license: String,
    #[serde(default)]
    pub tier: String,
    #[serde(default)]
    pub deprecated: bool,
}

#[derive(Debug, Serialize, Deserialize, Clone, Default)]
pub struct Build {
    #[serde(default)]
    pub base: String,
    #[serde(default)]
    pub user: String,
    #[serde(default)]
    pub stopsignal: String,
    #[serde(default)]
    pub multiarch: bool,
}

#[derive(Debug, Serialize, Deserialize, Clone, Default)]
pub struct SourceSection {
    #[serde(default, rename = "type")]
    pub source_type: String,
    #[serde(default)]
    pub url: String,
}

#[derive(Debug, Serialize, Deserialize, Clone, Default)]
pub struct RuntimeSection {
    #[serde(default)]
    pub entrypoint: Vec<String>,
}

#[derive(Debug, Serialize, Deserialize, Clone, Default)]
pub struct PortsSection {
    #[serde(default, deserialize_with = "deserialize_port_specs")]
    pub expose: Vec<String>,
}

fn deserialize_port_specs<'de, D>(de: D) -> std::result::Result<Vec<String>, D::Error>
where
    D: serde::Deserializer<'de>,
{
    #[derive(Deserialize)]
    #[serde(untagged)]
    enum PortSpec {
        Num(u16),
        Str(String),
    }

    let specs: Vec<PortSpec> = Vec::deserialize(de)?;
    Ok(specs
        .into_iter()
        .map(|p| match p {
            PortSpec::Num(n) => n.to_string(),
            PortSpec::Str(s) => s,
        })
        .collect())
}

impl Manifest {
    pub fn from_file(path: &Path) -> Result<Self> {
        let content = std::fs::read_to_string(path).map_err(|e| EvergreenError::ReadError {
            path: path.to_path_buf(),
            source: e,
        })?;
        let manifest: Manifest = toml::from_str(&content).map_err(|e| {
            EvergreenError::ManifestParseError {
                path: path.to_path_buf(),
                reason: e.to_string(),
            }
        })?;
        Ok(manifest)
    }

    pub fn to_file(&self, path: &Path) -> Result<()> {
        let content = toml::to_string_pretty(self).map_err(|e| {
            EvergreenError::ManifestParseError {
                path: path.to_path_buf(),
                reason: format!("serialization failed: {e}"),
            }
        })?;
        std::fs::write(path, content).map_err(|e| EvergreenError::WriteError {
            path: path.to_path_buf(),
            source: e,
        })?;
        Ok(())
    }

    /// Extract GitHub owner/repo from the metadata.source URL if it points to github.com.
    pub fn github_repo(&self) -> Option<String> {
        let url = if !self.metadata.source.is_empty() {
            &self.metadata.source
        } else if !self.source.url.is_empty() {
            &self.source.url
        } else {
            return None;
        };

        // Match https://github.com/owner/repo or http://github.com/owner/repo
        for prefix in &["https://github.com/", "http://github.com/"] {
            if let Some(rest) = url.strip_prefix(prefix) {
                // Remove trailing path components to get owner/repo
                let parts: Vec<&str> = rest.split('/').collect();
                if parts.len() >= 2 {
                    return Some(format!("{}/{}", parts[0], parts[1]));
                }
            }
        }
        None
    }

    /// Get the tier as a number (1-3), defaulting to 3 if parsing fails.
    pub fn tier_num(&self) -> u8 {
        self.metadata.tier.parse::<u8>().unwrap_or(3)
    }

    /// Get the image name (convenience alias for metadata.name).
    pub fn name(&self) -> &str {
        &self.metadata.name
    }

    /// Get the image version (convenience alias for metadata.version).
    pub fn version(&self) -> &str {
        &self.metadata.version
    }

    /// Get the source download URL.
    pub fn source_url(&self) -> &str {
        &self.source.url
    }

    /// Get the base image string from the build section.
    pub fn base_image(&self) -> &str {
        &self.build.base
    }

    /// Get the user string from the build section.
    pub fn user(&self) -> &str {
        &self.build.user
    }

    /// Get the stop signal from the build section.
    pub fn stop_signal(&self) -> &str {
        &self.build.stopsignal
    }

    /// Get the entrypoint from the runtime section.
    pub fn entrypoint(&self) -> &[String] {
        &self.runtime.entrypoint
    }

    /// Get the exposed ports.
    pub fn exposed_ports(&self) -> &[String] {
        &self.ports.expose
    }

    /// Get a label value by key.
    pub fn label(&self, key: &str) -> Option<&str> {
        self.labels.get(key).map(|s| s.as_str())
    }

    pub fn manifest_path(images_dir: &Path, name: &str) -> std::path::PathBuf {
        images_dir.join(name).join("manifest.toml")
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;
    use tempfile::NamedTempFile;

    fn write_manifest(content: &str) -> NamedTempFile {
        let mut f = NamedTempFile::new().unwrap();
        write!(f, "{}", content).unwrap();
        f
    }

    #[test]
    fn test_parse_minimal_manifest() {
        let content = r#"
[metadata]
name = "test"
version = "1.0.0"

[build]
base = "scratch"

[source]
url = "https://example.com/test.tar.gz"

[runtime]
entrypoint = ["/test"]
"#;
        let f = write_manifest(content);
        let m = Manifest::from_file(f.path()).unwrap();
        assert_eq!(m.name(), "test");
        assert_eq!(m.version(), "1.0.0");
        assert_eq!(m.base_image(), "scratch");
        assert_eq!(m.source_url(), "https://example.com/test.tar.gz");
        assert_eq!(m.entrypoint(), &["/test".to_string()]);
    }

    #[test]
    fn test_parse_full_manifest() {
        let content = r#"
[metadata]
name = "redis"
version = "7.4.1"
description = "Redis in-memory store"
vendor = "Redis"
source = "https://github.com/redis/redis"
license = "BSD-3-Clause"
tier = "1"

[build]
base = "cgr.dev/chainguard/wolfi-base:latest"
user = "65532:65532"
stopsignal = "SIGTERM"

[source]
type = "package-manager"
url = "https://github.com/redis/redis/archive/refs/tags/7.4.1.tar.gz"

[runtime]
entrypoint = ["sh", "-c", "redis"]

[ports]
expose = [6379, 9101]

[labels]
"org.opencontainers.image.title" = "redis"
"evergreen.image.tier" = "1"
"#;
        let f = write_manifest(content);
        let m = Manifest::from_file(f.path()).unwrap();
        assert_eq!(m.name(), "redis");
        assert_eq!(m.version(), "7.4.1");
        assert_eq!(m.metadata.description, "Redis in-memory store");
        assert_eq!(m.metadata.vendor, "Redis");
        assert_eq!(m.metadata.license, "BSD-3-Clause");
        assert_eq!(m.tier_num(), 1);
        assert_eq!(m.user(), "65532:65532");
        assert_eq!(m.stop_signal(), "SIGTERM");
        assert_eq!(m.exposed_ports(), &["6379".to_string(), "9101".to_string()]);
        assert_eq!(m.label("org.opencontainers.image.title"), Some("redis"));
        assert_eq!(m.label("nonexistent"), None);
    }

    #[test]
    fn test_parse_empty_manifest() {
        let content = "";
        let f = write_manifest(content);
        let m = Manifest::from_file(f.path()).unwrap();
        assert!(m.name().is_empty());
        assert!(m.version().is_empty());
        assert!(m.base_image().is_empty());
    }

    #[test]
    fn test_github_repo_from_metadata_source() {
        let content = r#"
[metadata]
name = "redis"
source = "https://github.com/redis/redis"

[build]
base = "scratch"

[source]
url = "https://example.com/download.tar.gz"

[runtime]
entrypoint = ["/redis"]
"#;
        let f = write_manifest(content);
        let m = Manifest::from_file(f.path()).unwrap();
        assert_eq!(m.github_repo(), Some("redis/redis".to_string()));
    }

    #[test]
    fn test_github_repo_from_source_url() {
        let content = r#"
[metadata]
name = "nginx"

[build]
base = "scratch"

[source]
url = "https://github.com/nginx/nginx/releases/download/v1.27.1/nginx.tar.gz"

[runtime]
entrypoint = ["/nginx"]
"#;
        let f = write_manifest(content);
        let m = Manifest::from_file(f.path()).unwrap();
        assert_eq!(m.github_repo(), Some("nginx/nginx".to_string()));
    }

    #[test]
    fn test_github_repo_no_github() {
        let content = r#"
[metadata]
name = "test"

[build]
base = "scratch"

[source]
url = "https://example.com/download.tar.gz"

[runtime]
entrypoint = ["/test"]
"#;
        let f = write_manifest(content);
        let m = Manifest::from_file(f.path()).unwrap();
        assert_eq!(m.github_repo(), None);
    }

    #[test]
    fn test_tier_num_valid() {
        let content = r#"
[metadata]
name = "test"
tier = "2"

[build]
base = "scratch"

[source]
url = "https://example.com/test.tar.gz"

[runtime]
entrypoint = ["/test"]
"#;
        let f = write_manifest(content);
        let m = Manifest::from_file(f.path()).unwrap();
        assert_eq!(m.tier_num(), 2);
    }

    #[test]
    fn test_tier_num_invalid_defaults_to_3() {
        let content = r#"
[metadata]
name = "test"
tier = "invalid"

[build]
base = "scratch"

[source]
url = "https://example.com/test.tar.gz"

[runtime]
entrypoint = ["/test"]
"#;
        let f = write_manifest(content);
        let m = Manifest::from_file(f.path()).unwrap();
        assert_eq!(m.tier_num(), 3);
    }

    #[test]
    fn test_round_trip() {
        let content = r#"
[metadata]
name = "test"
version = "1.0.0"

[build]
base = "scratch"

[source]
url = "https://example.com/test.tar.gz"

[runtime]
entrypoint = ["/test"]
"#;
        let f = write_manifest(content);
        let m = Manifest::from_file(f.path()).unwrap();

        let f2 = NamedTempFile::new().unwrap();
        m.to_file(f2.path()).unwrap();
        let m2 = Manifest::from_file(f2.path()).unwrap();

        assert_eq!(m.name(), m2.name());
        assert_eq!(m.version(), m2.version());
        assert_eq!(m.base_image(), m2.base_image());
        assert_eq!(m.source_url(), m2.source_url());
    }

    #[test]
    fn test_source_type_field() {
        let content = r#"
[metadata]
name = "test"

[build]
base = "scratch"

[source]
type = "package-manager"
url = "https://example.com/test.tar.gz"

[runtime]
entrypoint = ["/test"]
"#;
        let f = write_manifest(content);
        let m = Manifest::from_file(f.path()).unwrap();
        assert_eq!(m.source.source_type, "package-manager");
    }
}
