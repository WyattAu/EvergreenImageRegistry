// =============================================================================
// Evergreenctl - CLI Definition
// =============================================================================
// Separates CLI structure (Clap derive macros) from command execution logic.
// This module contains ONLY the CLI definition and path validation.
// =============================================================================

use clap::{Parser, Subcommand};
use std::path::{Path, PathBuf};

/// Validate a path argument to prevent path traversal attacks.
/// Returns the canonicalized absolute path, or an error if the path is invalid
/// or attempts to escape the allowed directory boundaries.
pub fn validate_path(path: &str, allowed_root: Option<&Path>) -> anyhow::Result<PathBuf> {
    let p = Path::new(path);

    // Reject paths with traversal components
    for component in p.components() {
        match component {
            std::path::Component::ParentDir => {
                anyhow::bail!(
                    "Path traversal detected: '{}' contains '..' component",
                    path
                );
            }
            std::path::Component::Normal(c) => {
                // Reject hidden directories (starting with .)
                if let Some(s) = c.to_str() {
                    if s.starts_with('.') && s != "." {
                        anyhow::bail!(
                            "Hidden path component rejected: '{}'",
                            path
                        );
                    }
                }
            }
            _ => {}
        }
    }

    // If an allowed root is specified, verify the path doesn't escape it
    if let Some(root) = allowed_root {
        if let Ok(canonical) = p.canonicalize() {
            if !canonical.starts_with(root) {
                anyhow::bail!(
                    "Path '{}' escapes allowed root '{}'",
                    path,
                    root.display()
                );
            }
            return Ok(canonical);
        }
        // If canonicalize fails (path doesn't exist yet), validate the prefix
        let root_str = root.to_string_lossy();
        let path_str = p.to_string_lossy();
        if !path_str.starts_with(&*root_str) {
            // Relative paths within images/ are OK
            if !p.is_relative() {
                anyhow::bail!(
                    "Path '{}' is outside allowed root '{}'",
                    path,
                    root.display()
                );
            }
        }
    }

    Ok(p.to_path_buf())
}

/// Validate an image name (simple name without path separators).
pub fn validate_image_name(name: &str) -> anyhow::Result<()> {
    if name.contains('/') || name.contains("..") || name.starts_with('.') {
        anyhow::bail!(
            "Invalid image name '{}': must be a simple name without path separators",
            name
        );
    }
    Ok(())
}

#[derive(Parser)]
#[command(name = "evergreenctl")]
#[command(about = "Evergreen image registry management toolchain")]
pub struct Cli {
    #[command(subcommand)]
    pub command: Commands,
}

#[derive(Subcommand)]
pub enum Commands {
    /// Find URLs for an image
    Discover {
        /// Image name to discover
        image: String,
        /// GitHub repo (owner/repo)
        #[arg(short, long)]
        repo: Option<String>,
        /// Version to look for
        #[arg(short, long)]
        version: Option<String>,
    },
    /// Verify checksums
    Verify {
        /// Path to manifest file or directory
        path: String,
    },
    /// Generate Dockerfile from manifest (outputs to stdout)
    Generate {
        /// Path to image directory containing manifest.toml
        image_dir: String,
    },
    /// Detect drift between manifest.toml and actual Dockerfile
    Drift {
        /// Path to image directory
        image_dir: String,
    },
    /// Generate Cosign signing commands for an image
    Sign {
        /// Path to image directory
        image_dir: String,
    },
    /// Generate a reproducibility snapshot as JSON
    Snapshot {
        /// Path to image directory
        image_dir: String,
    },
    /// Check for stubs/placeholders
    Audit {
        /// Path to images directory
        #[arg(default_value = "images")]
        path: String,
        /// Output format (text, json, tsv)
        #[arg(short, long, default_value = "text")]
        format: String,
    },
    /// Migrate existing Dockerfiles to manifests
    Migrate {
        /// Path to images directory
        #[arg(default_value = "images")]
        path: String,
        /// Dry run (don't write files)
        #[arg(short, long)]
        dry_run: bool,
    },
    /// Validate all manifests
    Validate {
        /// Path to images directory
        #[arg(default_value = "images")]
        path: String,
    },
    /// Verify all images for checksum coverage
    VerifyAll {
        /// Path to images directory
        #[arg(default_value = "images")]
        path: String,
    },
    /// Check for outdated versions
    Outdated {
        /// Path to images directory
        #[arg(default_value = "images")]
        path: String,
        /// Check all images, including those without GitHub repos
        #[arg(long)]
        all: bool,
    },
    /// Bump image version
    Bump {
        /// Image name
        image: String,
        /// New version
        new_version: String,
        /// Dry run (don't write files)
        #[arg(long)]
        dry_run: bool,
    },
    /// Pin all FROM digests to SHA256
    PinDigests {
        /// Path to image directory or images root
        #[arg(default_value = "images")]
        path: String,
        /// Dry run (don't modify files)
        #[arg(long)]
        dry_run: bool,
    },
    /// Show changes since last CI run
    CiDiff {
        /// Base git ref to compare against
        #[arg(long, default_value = "HEAD~1")]
        base: String,
    },
    /// Generate a JSON registry health report
    Report {
        /// Output format (json, text)
        #[arg(short, long, default_value = "json")]
        format: String,
        /// Path to images directory
        #[arg(long, default_value = "images")]
        images_dir: String,
    },
    /// List or mark deprecated images
    Deprecated {
        /// List deprecated images
        #[arg(long)]
        list: bool,
        /// Mark an image as deprecated
        #[arg(long, conflicts_with = "unmark")]
        mark: Option<String>,
        /// Remove deprecated flag from an image
        #[arg(long, conflicts_with = "mark")]
        unmark: Option<String>,
        /// Path to images directory
        #[arg(long, default_value = "images")]
        images_dir: String,
    },
    /// Generate changelog from git history
    Changelog {
        /// Path to images directory
        #[arg(long, default_value = "images")]
        images_dir: String,
        /// Number of days to look back
        #[arg(long, default_value = "30")]
        since: u64,
        /// Maximum number of entries to display
        #[arg(long, default_value = "50")]
        limit: usize,
    },
    /// Strict validation (manifest + Dockerfile + SBOM cross-reference)
    ValidateStrict {
        /// Path to images directory
        #[arg(long, default_value = "images")]
        images_dir: String,
    },
    /// Parallel validation (5k+ scale, uses rayon)
    ValidateParallel {
        /// Path to images directory
        #[arg(long, default_value = "images")]
        images_dir: String,
        /// Output format (text, json)
        #[arg(short, long, default_value = "text")]
        format: String,
    },
    /// Auto-version pipeline (detect upstream changes, auto-bump)
    AutoVersion {
        /// Path to images directory
        #[arg(long, default_value = "images")]
        images_dir: String,
        /// Dry run (don't write files)
        #[arg(long)]
        dry_run: bool,
        /// Allow major version jumps
        #[arg(long)]
        allow_major: bool,
        /// Output format (text, json)
        #[arg(short, long, default_value = "text")]
        format: String,
    },
    /// Build/rebuild SQLite registry index (full)
    Index {
        /// Path to images directory
        #[arg(long, default_value = "images")]
        images_dir: String,
        /// Path to SQLite database
        #[arg(long, default_value = ".registry.db")]
        db_path: String,
    },
    /// Incrementally update registry index (only changed images)
    IndexUpdate {
        /// Path to images directory
        #[arg(long, default_value = "images")]
        images_dir: String,
        /// Path to SQLite database
        #[arg(long, default_value = ".registry.db")]
        db_path: String,
    },
    /// Query registry index statistics
    IndexStats {
        /// Path to SQLite database
        #[arg(long, default_value = ".registry.db")]
        db_path: String,
        /// Output format (text, json)
        #[arg(short, long, default_value = "text")]
        format: String,
    },
    /// Generate HTML dashboard from registry index
    Dashboard {
        /// Path to SQLite database
        #[arg(long, default_value = ".registry.db")]
        db_path: String,
        /// Output file path
        #[arg(long, default_value = "dashboard.html")]
        output: String,
    },
    /// Query images by tier from registry index
    IndexQuery {
        /// Path to SQLite database
        #[arg(long, default_value = ".registry.db")]
        db_path: String,
        /// Filter by tier (1, 2, or 3)
        #[arg(long)]
        tier: Option<u8>,
        /// Filter by source type
        #[arg(long)]
        source_type: Option<String>,
        /// Output format (text, json)
        #[arg(short, long, default_value = "text")]
        format: String,
    },
    /// Generate shell completions
    Completion {
        #[arg(long, value_enum)]
        shell: clap_complete::Shell,
    },
}

/// Validate all path arguments for traversal attacks.
/// Returns Ok(true) if validation passed, Ok(false) for commands without paths.
pub fn validate_command_paths(command: &Commands) -> anyhow::Result<bool> {
    use Commands::*;

    match command {
        Discover { image, .. } => { validate_path(image, None)?; }
        Verify { path } => { validate_path(path, None)?; }
        Generate { image_dir } => { validate_path(image_dir, None)?; }
        Drift { image_dir } => { validate_path(image_dir, None)?; }
        Sign { image_dir } => { validate_path(image_dir, None)?; }
        Snapshot { image_dir } => { validate_path(image_dir, None)?; }
        Audit { path, .. } => { validate_path(path, None)?; }
        Migrate { path, .. } => { validate_path(path, None)?; }
        Validate { path } => { validate_path(path, None)?; }
        VerifyAll { path } => { validate_path(path, None)?; }
        Outdated { path, .. } => { validate_path(path, None)?; }
        Bump { image, .. } => { validate_image_name(image)?; }
        PinDigests { path, .. } => { validate_path(path, None)?; }
        Deprecated { images_dir, .. } => { validate_path(images_dir, None)?; }
        Changelog { images_dir, .. } => { validate_path(images_dir, None)?; }
        ValidateStrict { images_dir } => { validate_path(images_dir, None)?; }
        ValidateParallel { images_dir, .. } => { validate_path(images_dir, None)?; }
        AutoVersion { images_dir, .. } => { validate_path(images_dir, None)?; }
        Index { images_dir, .. } => { validate_path(images_dir, None)?; }
        _ => return Ok(false), // CiDiff, Report, Completion, IndexStats, IndexQuery don't take user path args
    }

    Ok(true)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_validate_path_simple() {
        let result = validate_path("images/redis", None);
        assert!(result.is_ok());
    }

    #[test]
    fn test_validate_path_traversal_rejected() {
        let result = validate_path("images/../etc/passwd", None);
        assert!(result.is_err());
        assert!(result.unwrap_err().to_string().contains("Path traversal"));
    }

    #[test]
    fn test_validate_path_hidden_dir_rejected() {
        let result = validate_path("images/.hidden/redis", None);
        assert!(result.is_err());
        assert!(result.unwrap_err().to_string().contains("Hidden path"));
    }

    #[test]
    fn test_validate_path_dot_accepted() {
        // Single dot is OK (current directory)
        let result = validate_path(".", None);
        assert!(result.is_ok());
    }

    #[test]
    fn test_validate_path_relative_accepted() {
        let result = validate_path("images/redis/Dockerfile", None);
        assert!(result.is_ok());
    }

    #[test]
    fn test_validate_image_name_simple() {
        assert!(validate_image_name("redis").is_ok());
        assert!(validate_image_name("nginx").is_ok());
        assert!(validate_image_name("my-image").is_ok());
    }

    #[test]
    fn test_validate_image_name_slash_rejected() {
        assert!(validate_image_name("../redis").is_err());
        assert!(validate_image_name("a/b").is_err());
    }

    #[test]
    fn test_validate_image_name_dot_rejected() {
        assert!(validate_image_name(".hidden").is_err());
        assert!(validate_image_name("redis/../../etc").is_err());
    }

    #[test]
    fn test_validate_command_paths_returns_true() {
        let cmd = Commands::Drift {
            image_dir: "images/redis".into(),
        };
        assert!(validate_command_paths(&cmd).unwrap());
    }

    #[test]
    fn test_validate_command_paths_returns_false_for_no_path() {
        let cmd = Commands::CiDiff {
            base: "HEAD~1".into(),
        };
        assert!(!validate_command_paths(&cmd).unwrap());
    }

    #[test]
    fn test_validate_command_paths_rejects_traversal() {
        let cmd = Commands::Verify {
            path: "../etc/passwd".into(),
        };
        assert!(validate_command_paths(&cmd).is_err());
    }
}
