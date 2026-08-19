// =============================================================================
// Evergreenctl - Typed Error Definitions
// =============================================================================
// Replaces anyhow string errors with structured, matchable error types.
// Each error variant carries enough context for programmatic handling
// (retry decisions, user-facing messages, CI exit codes).
//
// Pattern: Library modules return `Result<T, EvergreenError>`.
//          main.rs converts via `.map_err(|e| anyhow::anyhow!("{e}"))`
//          or uses `?` with the From impl.
// =============================================================================

use std::path::PathBuf;

/// Top-level error type for the evergreenctl crate.
#[derive(Debug, thiserror::Error)]
pub enum EvergreenError {
    // --- Filesystem errors ---
    #[error("file not found: {path}")]
    FileNotFound { path: PathBuf },

    #[error("failed to read {path}: {source}")]
    ReadError {
        path: PathBuf,
        source: std::io::Error,
    },

    #[error("failed to write {path}: {source}")]
    WriteError {
        path: PathBuf,
        source: std::io::Error,
    },

    #[error("directory not found: {path}")]
    DirectoryNotFound { path: PathBuf },

    // --- Manifest errors ---
    #[error("manifest not found at {path}")]
    ManifestNotFound { path: PathBuf },

    #[error("failed to parse manifest at {path}: {reason}")]
    ManifestParseError { path: PathBuf, reason: String },

    #[error("manifest validation failed for '{image}': {reason}")]
    ManifestValidationError { image: String, reason: String },

    // --- Dockerfile errors ---
    #[error("Dockerfile not found at {path}")]
    DockerfileNotFound { path: PathBuf },

    #[error("failed to parse Dockerfile at {path}: {reason}")]
    DockerfileParseError { path: PathBuf, reason: String },

    // --- SBOM errors ---
    #[error("SBOM not found at {path}")]
    SbomNotFound { path: PathBuf },

    #[error("SBOM validation failed at {path}: {reason}")]
    SbomValidationError { path: PathBuf, reason: String },

    // --- Version errors ---
    #[error("no ARG VERSION found in {path}")]
    MissingVersion { path: PathBuf },

    #[error("version mismatch for '{image}': manifest={manifest_version}, dockerfile={dockerfile_version}")]
    VersionMismatch {
        image: String,
        manifest_version: String,
        dockerfile_version: String,
    },

    #[error("unsafe version bump: {reason}")]
    UnsafeVersionBump { reason: String },

    // --- Validation errors ---
    #[error("validation failed: {message}")]
    ValidationFailed { message: String },

    #[error("constraint {code} failed for '{image}': {message}")]
    ConstraintViolation {
        code: String,
        image: String,
        message: String,
    },

    #[error("Alpine base image detected in '{image}' (FORBIDDEN)")]
    AlpineDetected { image: String },

    #[error("path traversal detected: '{path}'")]
    PathTraversal { path: String },

    #[error("invalid image name '{name}': {reason}")]
    InvalidImageName { name: String, reason: String },

    // --- Network/API errors ---
    #[error("GitHub API error for '{repo}': {reason}")]
    GitHubApiError { repo: String, reason: String },

    #[error("rate limited by GitHub API, retry after {retry_after_secs}s")]
    RateLimited { retry_after_secs: u64 },

    #[error("download failed for {url}: {reason}")]
    DownloadError { url: String, reason: String },

    // --- Checksum errors ---
    #[error("checksum mismatch for {path}: expected {expected}, got {computed}")]
    ChecksumMismatch {
        path: PathBuf,
        expected: String,
        computed: String,
    },

    #[error("unsupported checksum algorithm: {algorithm}")]
    UnsupportedAlgorithm { algorithm: String },

    // --- Index/Database errors ---
    #[error("database error: {0}")]
    DatabaseError(String),

    // --- Drift errors ---
    #[error("drift detected in '{image}': {details}")]
    DriftDetected { image: String, details: String },

    // --- Configuration errors ---
    #[error("image '{image}' not found in registry")]
    ImageNotFound { image: String },

    #[error("no GitHub source configured for '{image}'")]
    NoGitHubSource { image: String },

    // --- Build errors ---
    #[error("Dockerfile generation failed for '{image}': {reason}")]
    GenerationFailed { image: String, reason: String },
}

/// Convenience alias for Results using EvergreenError.
pub type Result<T> = std::result::Result<T, EvergreenError>;

// --- From implementations for ergonomic error conversion ---

impl From<std::io::Error> for EvergreenError {
    fn from(e: std::io::Error) -> Self {
        EvergreenError::ReadError {
            path: PathBuf::from("<unknown>"),
            source: e,
        }
    }
}

impl From<toml::de::Error> for EvergreenError {
    fn from(e: toml::de::Error) -> Self {
        EvergreenError::ManifestParseError {
            path: PathBuf::from("<unknown>"),
            reason: e.to_string(),
        }
    }
}

impl From<serde_json::Error> for EvergreenError {
    fn from(e: serde_json::Error) -> Self {
        EvergreenError::SbomValidationError {
            path: PathBuf::from("<unknown>"),
            reason: e.to_string(),
        }
    }
}

// Note: EvergreenError automatically converts to anyhow::Error via the
// blanket impl `From<E: std::error::Error + Send + Sync + 'static>`
// since thiserror::Error derives std::error::Error. No explicit From needed.

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_error_display() {
        let err = EvergreenError::AlpineDetected {
            image: "test-img".into(),
        };
        assert!(err.to_string().contains("Alpine"));
        assert!(err.to_string().contains("test-img"));
    }

    #[test]
    fn test_error_into_anyhow() {
        let err = EvergreenError::FileNotFound {
            path: PathBuf::from("/foo"),
        };
        let anyhow_err: anyhow::Error = err.into();
        assert!(anyhow_err.to_string().contains("file not found"));
    }

    #[test]
    fn test_io_error_conversion() {
        let io_err = std::io::Error::new(std::io::ErrorKind::NotFound, "nope");
        let err: EvergreenError = io_err.into();
        assert!(matches!(err, EvergreenError::ReadError { .. }));
    }

    #[test]
    fn test_constraint_violation_display() {
        let err = EvergreenError::ConstraintViolation {
            code: "C004".into(),
            image: "redis".into(),
            message: "Alpine detected".into(),
        };
        let msg = err.to_string();
        assert!(msg.contains("C004"));
        assert!(msg.contains("redis"));
    }
}
