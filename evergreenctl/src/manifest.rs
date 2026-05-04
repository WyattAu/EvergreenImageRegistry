use anyhow::{Context, Result};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::path::Path;

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Manifest {
    pub image: ImageMeta,
    pub source: Source,
    pub build: BuildConfig,
    pub runtime: RuntimeConfig,
    pub health: HealthConfig,
    #[serde(default)]
    pub observability: ObservabilityConfig,
    #[serde(default)]
    pub compliance: ComplianceConfig,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct ImageMeta {
    pub name: String,
    #[serde(rename = "type")]
    pub image_type: ImageType,
    pub tier: u8,
    pub version: String,
    pub description: String,
    pub vendor: String,
    #[serde(default)]
    pub source_url: Option<String>,
    #[serde(default)]
    pub category: Option<String>,
}

#[derive(Debug, Serialize, Deserialize, Clone, PartialEq)]
#[serde(rename_all = "kebab-case")]
#[derive(Default)]
pub enum ImageType {
    #[default]
    BinaryDownload,
    SourceBuildGo,
    SourceBuildC,
    SourceBuildRust,
    SourceBuildJava,
    NodeNpm,
    PythonPip,
    WebUi,
    Database,
    MessageQueue,
    Monitoring,
    Networking,
    Security,
    Storage,
    Other,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Source {
    pub url: String,
    #[serde(default)]
    pub fallback_urls: Vec<String>,
    pub checksum: Checksum,
    #[serde(default)]
    pub strategy: DownloadStrategy,
    #[serde(default)]
    pub github_repo: Option<String>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Checksum {
    pub algorithm: String,
    pub expected: String,
    #[serde(default)]
    pub source: String,
}

#[derive(Debug, Serialize, Deserialize, Clone, Default)]
#[serde(rename_all = "kebab-case")]
pub enum DownloadStrategy {
    #[default]
    Curl,
    GitClone,
    Wget,
    NpmPack,
    PipDownload,
    AptGet,
    ApkAdd,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct BuildConfig {
    pub base: BaseImage,
    #[serde(default)]
    pub stages: Vec<BuildStage>,
    #[serde(default)]
    pub env: HashMap<String, String>,
    #[serde(default)]
    pub builder_packages: Vec<String>,
    #[serde(default)]
    pub runtime_packages: Vec<String>,
    #[serde(default)]
    pub build_args: HashMap<String, String>,
    #[serde(default)]
    pub pre_build_commands: Vec<String>,
    #[serde(default)]
    pub build_commands: Vec<String>,
    #[serde(default)]
    pub post_build_commands: Vec<String>,
    #[serde(default)]
    pub artifacts: Vec<Artifact>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct BaseImage {
    pub image: String,
    #[serde(default)]
    pub purpose: String,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct BuildStage {
    pub name: String,
    pub base: String,
    #[serde(default)]
    pub packages: Vec<String>,
    #[serde(default)]
    pub commands: Vec<String>,
    #[serde(default)]
    pub env: HashMap<String, String>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Artifact {
    pub source: String,
    pub destination: String,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct RuntimeConfig {
    #[serde(default = "default_user")]
    pub user: String,
    #[serde(default = "default_workdir")]
    pub workdir: String,
    pub entrypoint: Vec<String>,
    #[serde(default)]
    pub cmd: Vec<String>,
    #[serde(default)]
    pub ports: Vec<u16>,
    #[serde(default)]
    pub volumes: Vec<String>,
    #[serde(default = "default_stop_signal")]
    pub stop_signal: String,
    #[serde(default)]
    pub env: HashMap<String, String>,
}

fn default_user() -> String {
    "65532:65532".to_string()
}
fn default_workdir() -> String {
    "/app".to_string()
}
fn default_stop_signal() -> String {
    "SIGTERM".to_string()
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct HealthConfig {
    #[serde(rename = "type")]
    pub health_type: String,
    #[serde(default)]
    pub path: String,
    #[serde(default)]
    pub port: Option<u16>,
    #[serde(default)]
    pub interval_seconds: u32,
    #[serde(default)]
    pub timeout_seconds: u32,
    #[serde(default)]
    pub retries: u32,
}

#[derive(Debug, Serialize, Deserialize, Clone, Default)]
pub struct ObservabilityConfig {
    pub metrics_port: u16,
    #[serde(default = "default_metrics_path")]
    pub metrics_path: String,
}

fn default_metrics_path() -> String {
    "/metrics".to_string()
}

#[derive(Debug, Serialize, Deserialize, Clone, Default)]
pub struct ComplianceConfig {
    #[serde(default)]
    pub standards: Vec<String>,
    #[serde(default)]
    pub labels: HashMap<String, String>,
}

impl Manifest {
    pub fn from_file(path: &Path) -> Result<Self> {
        let content = std::fs::read_to_string(path)
            .with_context(|| format!("Failed to read manifest: {}", path.display()))?;
        let manifest: Manifest = toml::from_str(&content)
            .with_context(|| format!("Failed to parse manifest: {}", path.display()))?;
        manifest.validate()?;
        Ok(manifest)
    }

    pub fn to_file(&self, path: &Path) -> Result<()> {
        let content = toml::to_string_pretty(self).context("Failed to serialize manifest")?;
        std::fs::write(path, content)
            .with_context(|| format!("Failed to write manifest: {}", path.display()))?;
        Ok(())
    }

    pub fn validate(&self) -> Result<()> {
        if self.image.name.is_empty() {
            anyhow::bail!("image.name is required");
        }
        if self.image.version.is_empty() {
            anyhow::bail!("image.version is required");
        }
        if self.source.url.is_empty() {
            anyhow::bail!("source.url is required");
        }
        if !matches!(self.image.tier, 1..=3) {
            anyhow::bail!("image.tier must be 1, 2, or 3");
        }
        if self.runtime.entrypoint.is_empty() {
            anyhow::bail!("runtime.entrypoint is required");
        }
        if self.health.health_type.is_empty() {
            anyhow::bail!("health.type is required");
        }
        match self.health.health_type.as_str() {
            "http" | "tcp" | "exec" | "none" => {}
            other => anyhow::bail!(
                "Invalid health type: {} (must be http/tcp/exec/none)",
                other
            ),
        }
        Ok(())
    }

    pub fn manifest_path(images_dir: &Path, name: &str) -> std::path::PathBuf {
        images_dir.join(name).join("manifest.toml")
    }
}
