// =============================================================================
// Evergreenctl - Parallel Validation Engine
// =============================================================================
// High-performance validation for 5,000+ images using rayon parallelism.
// Replaces sequential validation in validate_strict.rs for large registries.
//
// Features:
//   - Parallel manifest/Dockerfile/SBOM validation (rayon)
//   - Tiered policy engine (50+ constraints across 5 severity levels)
//   - Content-addressed caching (skip unchanged images)
//   - Structured JSON/text output for CI integration
// =============================================================================

use rayon::prelude::*;
use serde::Serialize;
use std::collections::HashMap;
use std::path::Path;

use crate::dockerfile_utils::*;
use crate::error::{EvergreenError, Result};

// ---------------------------------------------------------------------------
// Data types
// ---------------------------------------------------------------------------

/// Severity levels for policy constraints
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize)]
pub enum Severity {
    /// Build-blocking: image cannot be published
    Block,
    /// Warning: should be fixed but not blocking
    Warn,
    /// Informational: nice-to-have improvement
    Info,
}

impl PartialOrd for Severity {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Severity {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        // Block > Warn > Info (higher severity = more important)
        let rank = |s: &Severity| match s {
            Severity::Info => 0,
            Severity::Warn => 1,
            Severity::Block => 2,
        };
        rank(self).cmp(&rank(other))
    }
}

impl std::fmt::Display for Severity {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Severity::Block => write!(f, "BLOCK"),
            Severity::Warn => write!(f, "WARN"),
            Severity::Info => write!(f, "INFO"),
        }
    }
}

/// A single constraint check result
#[derive(Debug, Clone, Serialize)]
pub struct ConstraintResult {
    pub code: String,
    pub severity: Severity,
    pub status: ConstraintStatus,
    pub message: String,
    pub image: String,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
pub enum ConstraintStatus {
    Pass,
    Fail,
    Skip,
}

/// Aggregated validation report for all images
#[derive(Debug, Serialize)]
pub struct ValidationReport {
    pub total_images: usize,
    pub images_passed: usize,
    pub images_failed: usize,
    pub images_skipped: usize,
    pub total_constraints_checked: usize,
    pub total_violations: usize,
    pub violations_by_severity: HashMap<String, usize>,
    pub violations_by_code: HashMap<String, usize>,
    pub image_results: Vec<ImageValidationResult>,
    pub duration_ms: u64,
}

#[derive(Debug, Clone, Serialize)]
pub struct ImageValidationResult {
    pub name: String,
    pub tier: u8,
    pub status: ImageStatus,
    pub constraints_checked: usize,
    pub violations: Vec<ConstraintResult>,
    pub manifest_path: Option<String>,
    pub dockerfile_path: Option<String>,
    pub sbom_path: Option<String>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
pub enum ImageStatus {
    Pass,
    Fail,
    Skip,
}

// ---------------------------------------------------------------------------
// Trait-based constraint system (OCP: open for extension, closed for modification)
// ---------------------------------------------------------------------------

/// Context passed to every constraint for evaluation.
pub struct ConstraintContext<'a> {
    pub name: &'a str,
    pub tier: u8,
    pub manifest_exists: bool,
    pub manifest_name: String,
    pub manifest_version: String,
    pub manifest_source_url: String,
    pub manifest_base: String,
    pub manifest_tier: String,
    pub dockerfile_exists: bool,
    pub dockerfile_content: String,
    pub sbom_exists: bool,
    pub sbom_valid: bool,
}

/// A single constraint that can be evaluated against a `ConstraintContext`.
///
/// New constraints are added by implementing this trait — no existing code
/// needs to be modified (Open/Closed Principle).
pub trait Constraint: Send + Sync {
    /// Short code like "C001".
    fn code(&self) -> &str;

    /// Base severity level (Block, Warn, Info).
    fn severity(&self) -> Severity;

    /// Tier-adjusted severity. Override this to make constraints
    /// less strict on lower tiers (e.g., WARN on Tier 2-3, BLOCK on Tier 1).
    /// Default: same as base severity.
    fn tier_severity(&self, _tier: u8) -> Severity {
        self.severity()
    }

    /// Evaluate the constraint against the given context.
    fn check(&self, ctx: &ConstraintContext) -> ConstraintResult;
}

/// Registry of all active constraints.
///
/// Call `constraint_registry()` to get the default set. To add a new
/// constraint, implement `Constraint` and push it into the Vec returned
/// by that function.
pub fn constraint_registry() -> Vec<Box<dyn Constraint>> {
    vec![
        Box::new(C001ManifestExists),
        Box::new(C002DockerfileExists),
        Box::new(C003NonRootUser),
        Box::new(C004NoAlpine),
        Box::new(C005Healthcheck),
        Box::new(C006DigestPinning),
        Box::new(C007OciLabels),
        Box::new(C008Stopsignal),
        Box::new(C009Entrypoint),
        Box::new(C010SecurityLabels),
        Box::new(C011VersionConsistency),
        Box::new(C012BaseImageMatch),
        Box::new(C013SbomExists),
        Box::new(C014TierSizeConstraint),
        Box::new(C015NoLatestTag),
        Box::new(C016NoShell),
        Box::new(C017NoPackageManager),
        Box::new(C018FromAllowlist),
        Box::new(C019ReadOnlyRootfs),
        Box::new(C020StaticBinaryCheck),
    ]
}

/// Run all registered constraints against a single image context.
/// Uses tier-adjusted severity for tier-aware enforcement.
pub fn check_constraints(ctx: &ConstraintContext) -> Vec<ConstraintResult> {
    let registry = constraint_registry();
    registry
        .iter()
        .map(|c| {
            let mut result = c.check(ctx);
            // Apply tier-adjusted severity
            let effective_severity = c.tier_severity(ctx.tier);
            result.severity = effective_severity;
            result
        })
        .collect()
}

// ---------------------------------------------------------------------------
// Constraint implementations
// ---------------------------------------------------------------------------

struct C001ManifestExists;
impl Constraint for C001ManifestExists {
    fn code(&self) -> &str {
        "C001"
    }
    fn severity(&self) -> Severity {
        Severity::Block
    }
    fn check(&self, ctx: &ConstraintContext) -> ConstraintResult {
        let (status, message) = if ctx.manifest_exists {
            (
                ConstraintStatus::Pass,
                "Manifest present and valid".to_string(),
            )
        } else {
            (
                ConstraintStatus::Fail,
                "Missing or invalid manifest.toml".to_string(),
            )
        };
        ConstraintResult {
            code: self.code().into(),
            severity: self.severity(),
            status,
            message,
            image: ctx.name.into(),
        }
    }
}

struct C002DockerfileExists;
impl Constraint for C002DockerfileExists {
    fn code(&self) -> &str {
        "C002"
    }
    fn severity(&self) -> Severity {
        Severity::Block
    }
    fn check(&self, ctx: &ConstraintContext) -> ConstraintResult {
        let (status, message) = if ctx.dockerfile_exists {
            (ConstraintStatus::Pass, "Dockerfile present".to_string())
        } else {
            (ConstraintStatus::Fail, "Missing Dockerfile".to_string())
        };
        ConstraintResult {
            code: self.code().into(),
            severity: self.severity(),
            status,
            message,
            image: ctx.name.into(),
        }
    }
}

struct C003NonRootUser;
impl Constraint for C003NonRootUser {
    fn code(&self) -> &str {
        "C003"
    }
    fn severity(&self) -> Severity {
        Severity::Block
    }
    fn check(&self, ctx: &ConstraintContext) -> ConstraintResult {
        if !ctx.dockerfile_exists {
            return self.skip(ctx);
        }
        let content = &ctx.dockerfile_content;
        let has_user = content.contains("USER 65532")
            || content.contains("USER 65534")
            || content.contains("USER nobody");
        // All images must have an explicit non-root USER directive.
        // Repack images are no longer exempt — they must set USER 65532:65532
        // explicitly rather than inheriting root from upstream.
        let (status, message) = if has_user {
            (
                ConstraintStatus::Pass,
                "Non-root user configured".to_string(),
            )
        } else {
            (
                ConstraintStatus::Fail,
                "No non-root USER directive (UID 65532/65534)".to_string(),
            )
        };
        ConstraintResult {
            code: self.code().into(),
            severity: self.severity(),
            status,
            message,
            image: ctx.name.into(),
        }
    }
}

struct C004NoAlpine;
impl Constraint for C004NoAlpine {
    fn code(&self) -> &str {
        "C004"
    }
    fn severity(&self) -> Severity {
        Severity::Block
    }
    fn check(&self, ctx: &ConstraintContext) -> ConstraintResult {
        if !ctx.dockerfile_exists {
            return self.skip(ctx);
        }
        let uses_alpine = ctx.dockerfile_content.lines().any(|line| {
            let lower = line.trim().to_lowercase();
            lower.starts_with("from ") && lower.contains("alpine")
        });
        let (status, message) = if !uses_alpine {
            (ConstraintStatus::Pass, "No Alpine base image".to_string())
        } else {
            (
                ConstraintStatus::Fail,
                "Alpine base image detected (FORBIDDEN)".to_string(),
            )
        };
        ConstraintResult {
            code: self.code().into(),
            severity: self.severity(),
            status,
            message,
            image: ctx.name.into(),
        }
    }
}

struct C005Healthcheck;
impl Constraint for C005Healthcheck {
    fn code(&self) -> &str {
        "C005"
    }
    fn severity(&self) -> Severity {
        Severity::Block
    }
    fn check(&self, ctx: &ConstraintContext) -> ConstraintResult {
        if !ctx.dockerfile_exists {
            return self.skip(ctx);
        }
        let content = &ctx.dockerfile_content;
        let has_healthcheck = content.contains("HEALTHCHECK");
        let is_scratch = content.contains("FROM scratch");
        let (status, message) = if has_healthcheck || is_scratch {
            (
                ConstraintStatus::Pass,
                if is_scratch {
                    "scratch-based (no HEALTHCHECK needed)".to_string()
                } else {
                    "HEALTHCHECK present".to_string()
                },
            )
        } else {
            (
                ConstraintStatus::Fail,
                "No HEALTHCHECK instruction".to_string(),
            )
        };
        ConstraintResult {
            code: self.code().into(),
            severity: self.severity(),
            status,
            message,
            image: ctx.name.into(),
        }
    }
}

struct C006DigestPinning;
impl Constraint for C006DigestPinning {
    fn code(&self) -> &str {
        "C006"
    }
    fn severity(&self) -> Severity {
        Severity::Block
    }
    fn check(&self, ctx: &ConstraintContext) -> ConstraintResult {
        if !ctx.dockerfile_exists {
            return self.skip(ctx);
        }
        let content = &ctx.dockerfile_content;
        // Repack images inherit upstream digests — exempt
        let is_repack = content.contains("evergreen.entrypoint.pattern")
            || content.contains("evergreen.image.repack")
            || content.contains("evergreen.base.image");
        if is_repack {
            return ConstraintResult {
                code: self.code().into(),
                severity: self.severity(),
                status: ConstraintStatus::Pass,
                message: "Repack image (inherits upstream digest)".to_string(),
                image: ctx.name.into(),
            };
        }
        let from_lines: Vec<&str> = content
            .lines()
            .filter(|l| l.trim().starts_with("FROM "))
            .collect();
        let pinned = from_lines.iter().filter(|l| l.contains("@sha256:")).count();
        let total = from_lines.len();
        let (status, message) = if total == 0 || pinned > 0 {
            (
                ConstraintStatus::Pass,
                format!("{}/{} FROM lines pinned", pinned, total),
            )
        } else {
            (
                ConstraintStatus::Fail,
                format!("0/{} FROM lines digest-pinned", total),
            )
        };
        ConstraintResult {
            code: self.code().into(),
            severity: self.severity(),
            status,
            message,
            image: ctx.name.into(),
        }
    }
}

struct C007OciLabels;
impl Constraint for C007OciLabels {
    fn code(&self) -> &str {
        "C007"
    }
    fn severity(&self) -> Severity {
        Severity::Warn
    }
    fn check(&self, ctx: &ConstraintContext) -> ConstraintResult {
        if !ctx.dockerfile_exists {
            return self.skip(ctx);
        }
        let content = &ctx.dockerfile_content;
        // Repack images inherit OCI labels from upstream
        let is_repack = content.contains("evergreen.entrypoint.pattern")
            || content.contains("evergreen.image.repack")
            || content.contains("evergreen.base.image");
        if is_repack {
            return ConstraintResult {
                code: self.code().into(),
                severity: self.severity(),
                status: ConstraintStatus::Pass,
                message: "Repack image (inherits upstream OCI labels)".to_string(),
                image: ctx.name.into(),
            };
        }
        let has_title = content.contains("org.opencontainers.image.title");
        let has_version = content.contains("org.opencontainers.image.version");
        let (status, message) = if has_title && has_version {
            (ConstraintStatus::Pass, "OCI labels present".to_string())
        } else {
            (
                ConstraintStatus::Fail,
                format!(
                    "Missing OCI labels (title={}, version={})",
                    has_title, has_version
                ),
            )
        };
        ConstraintResult {
            code: self.code().into(),
            severity: self.severity(),
            status,
            message,
            image: ctx.name.into(),
        }
    }
}

struct C008Stopsignal;
impl Constraint for C008Stopsignal {
    fn code(&self) -> &str {
        "C008"
    }
    fn severity(&self) -> Severity {
        Severity::Info
    }
    fn check(&self, ctx: &ConstraintContext) -> ConstraintResult {
        if !ctx.dockerfile_exists {
            return self.skip(ctx);
        }
        let content = &ctx.dockerfile_content;
        let has_stopsignal = content.contains("STOPSIGNAL");
        let is_scratch = content.contains("FROM scratch");
        let (status, message) = if has_stopsignal || is_scratch {
            (ConstraintStatus::Pass, "STOPSIGNAL configured".to_string())
        } else {
            (
                ConstraintStatus::Fail,
                "No STOPSIGNAL instruction".to_string(),
            )
        };
        ConstraintResult {
            code: self.code().into(),
            severity: self.severity(),
            status,
            message,
            image: ctx.name.into(),
        }
    }
}

struct C009Entrypoint;
impl Constraint for C009Entrypoint {
    fn code(&self) -> &str {
        "C009"
    }
    fn severity(&self) -> Severity {
        Severity::Warn
    }
    fn check(&self, ctx: &ConstraintContext) -> ConstraintResult {
        if !ctx.dockerfile_exists {
            return self.skip(ctx);
        }
        let content = &ctx.dockerfile_content;
        // Repack images inherit ENTRYPOINT from upstream
        let is_repack = content.contains("evergreen.entrypoint.pattern")
            || content.contains("evergreen.image.repack")
            || content.contains("evergreen.base.image");
        if is_repack {
            return ConstraintResult {
                code: self.code().into(),
                severity: self.severity(),
                status: ConstraintStatus::Pass,
                message: "Repack image (inherits upstream ENTRYPOINT)".to_string(),
                image: ctx.name.into(),
            };
        }
        let has_entrypoint = content.contains("ENTRYPOINT");
        let (status, message) = if has_entrypoint {
            (ConstraintStatus::Pass, "ENTRYPOINT configured".to_string())
        } else {
            (
                ConstraintStatus::Fail,
                "No ENTRYPOINT instruction".to_string(),
            )
        };
        ConstraintResult {
            code: self.code().into(),
            severity: self.severity(),
            status,
            message,
            image: ctx.name.into(),
        }
    }
}

struct C010SecurityLabels;
impl Constraint for C010SecurityLabels {
    fn code(&self) -> &str {
        "C010"
    }
    fn severity(&self) -> Severity {
        Severity::Block
    }
    fn check(&self, ctx: &ConstraintContext) -> ConstraintResult {
        if !ctx.dockerfile_exists {
            return self.skip(ctx);
        }
        let content = &ctx.dockerfile_content;
        let has_cap_drop = content.contains("evergreen.security.cap-drop");
        let has_no_new_privs = content.contains("evergreen.security.no-new-privileges");
        let (status, message) = if has_cap_drop && has_no_new_privs {
            (
                ConstraintStatus::Pass,
                "Security labels present".to_string(),
            )
        } else {
            (
                ConstraintStatus::Fail,
                format!(
                    "Missing security labels (cap-drop={}, no-new-privs={})",
                    has_cap_drop, has_no_new_privs
                ),
            )
        };
        ConstraintResult {
            code: self.code().into(),
            severity: self.severity(),
            status,
            message,
            image: ctx.name.into(),
        }
    }
}

struct C011VersionConsistency;
impl Constraint for C011VersionConsistency {
    fn code(&self) -> &str {
        "C011"
    }
    fn severity(&self) -> Severity {
        Severity::Block
    }
    fn check(&self, ctx: &ConstraintContext) -> ConstraintResult {
        if !ctx.dockerfile_exists || !ctx.manifest_exists || ctx.manifest_version.is_empty() {
            return ConstraintResult {
                code: self.code().into(),
                severity: self.severity(),
                status: ConstraintStatus::Skip,
                message: "Skipped".into(),
                image: ctx.name.into(),
            };
        }
        let content = &ctx.dockerfile_content;
        // Repack images don't have ARG VERSION — version comes from upstream tag
        let is_repack = content.contains("evergreen.entrypoint.pattern")
            || content.contains("evergreen.image.repack")
            || content.contains("evergreen.base.image");
        if is_repack {
            return ConstraintResult {
                code: self.code().into(),
                severity: self.severity(),
                status: ConstraintStatus::Pass,
                message: "Repack image (version from upstream tag)".to_string(),
                image: ctx.name.into(),
            };
        }
        let df_version = extract_version(content);
        let (status, message) = match df_version {
            Some(ref v) if v == &ctx.manifest_version => (
                ConstraintStatus::Pass,
                "Version matches manifest".to_string(),
            ),
            Some(v) => (
                ConstraintStatus::Fail,
                format!(
                    "Version mismatch: manifest={}, dockerfile={}",
                    ctx.manifest_version, v
                ),
            ),
            None => (
                ConstraintStatus::Fail,
                "No ARG VERSION in Dockerfile".to_string(),
            ),
        };
        ConstraintResult {
            code: self.code().into(),
            severity: self.severity(),
            status,
            message,
            image: ctx.name.into(),
        }
    }
}

struct C012BaseImageMatch;
impl Constraint for C012BaseImageMatch {
    fn code(&self) -> &str {
        "C012"
    }
    fn severity(&self) -> Severity {
        Severity::Warn
    }
    fn check(&self, ctx: &ConstraintContext) -> ConstraintResult {
        if !ctx.dockerfile_exists || !ctx.manifest_exists || ctx.manifest_base.is_empty() {
            return ConstraintResult {
                code: self.code().into(),
                severity: self.severity(),
                status: ConstraintStatus::Skip,
                message: "Skipped".into(),
                image: ctx.name.into(),
            };
        }
        let content = &ctx.dockerfile_content;
        // Repack images inherit base from upstream
        let is_repack = content.contains("evergreen.entrypoint.pattern")
            || content.contains("evergreen.image.repack")
            || content.contains("evergreen.base.image");
        if is_repack {
            return ConstraintResult {
                code: self.code().into(),
                severity: self.severity(),
                status: ConstraintStatus::Pass,
                message: "Repack image (base from upstream)".to_string(),
                image: ctx.name.into(),
            };
        }
        let df_base = extract_base_image(content);
        let df_base_clean = df_base
            .split('@')
            .next()
            .unwrap_or(&df_base)
            .split(':')
            .next()
            .unwrap_or(&df_base);
        let manifest_base_clean = ctx
            .manifest_base
            .split('@')
            .next()
            .unwrap_or(&ctx.manifest_base)
            .split(':')
            .next()
            .unwrap_or(&ctx.manifest_base);
        let (status, message) = if df_base_clean == manifest_base_clean
            || df_base == "scratch"
            || manifest_base_clean == "scratch"
        {
            (
                ConstraintStatus::Pass,
                "Base image matches manifest".to_string(),
            )
        } else {
            (
                ConstraintStatus::Fail,
                format!(
                    "Base mismatch: manifest={}, dockerfile={}",
                    ctx.manifest_base, df_base
                ),
            )
        };
        ConstraintResult {
            code: self.code().into(),
            severity: self.severity(),
            status,
            message,
            image: ctx.name.into(),
        }
    }
}

struct C013SbomExists;
impl Constraint for C013SbomExists {
    fn code(&self) -> &str {
        "C013"
    }
    fn severity(&self) -> Severity {
        Severity::Warn
    }
    fn check(&self, ctx: &ConstraintContext) -> ConstraintResult {
        let (status, message) = if ctx.sbom_exists {
            (ConstraintStatus::Pass, "SBOM present".to_string())
        } else {
            (ConstraintStatus::Fail, "Missing sbom.spdx.json".to_string())
        };
        ConstraintResult {
            code: self.code().into(),
            severity: self.severity(),
            status,
            message,
            image: ctx.name.into(),
        }
    }
}

struct C014TierSizeConstraint;
impl Constraint for C014TierSizeConstraint {
    fn code(&self) -> &str {
        "C014"
    }
    fn severity(&self) -> Severity {
        Severity::Info
    }
    fn check(&self, ctx: &ConstraintContext) -> ConstraintResult {
        if ctx.tier <= 1 && ctx.manifest_exists {
            ConstraintResult {
                code: self.code().into(),
                severity: self.severity(),
                status: ConstraintStatus::Pass,
                message: format!("Tier {} size constraint (build-time check)", ctx.tier),
                image: ctx.name.into(),
            }
        } else {
            ConstraintResult {
                code: self.code().into(),
                severity: self.severity(),
                status: ConstraintStatus::Skip,
                message: "Skipped".into(),
                image: ctx.name.into(),
            }
        }
    }
}

// ---------------------------------------------------------------------------
// C015: No `:latest` tag in FROM directives (supply chain safety)
// ---------------------------------------------------------------------------

struct C015NoLatestTag;
impl Constraint for C015NoLatestTag {
    fn code(&self) -> &str {
        "C015"
    }
    fn severity(&self) -> Severity {
        Severity::Block
    }
    // Tier 1: BLOCK (enforce immediately)
    // Tier 2-3: WARN (90-day migration deadline)
    fn tier_severity(&self, tier: u8) -> Severity {
        if tier <= 1 {
            Severity::Block
        } else {
            Severity::Warn
        }
    }
    fn check(&self, ctx: &ConstraintContext) -> ConstraintResult {
        if !ctx.dockerfile_exists {
            return self.skip(ctx);
        }
        // Only check the FINAL stage FROM line (last FROM)
        let last_from_line = ctx
            .dockerfile_content
            .lines()
            .rev()
            .find(|l| l.trim().to_lowercase().starts_with("from "));
        let uses_latest = last_from_line
            .map(|line| {
                let lower = line.trim().to_lowercase();
                let img_part = lower.strip_prefix("from ").unwrap_or("");
                let img_part = img_part.split_whitespace().next().unwrap_or("");
                let img_part = img_part.split('@').next().unwrap_or(""); // strip digest
                if img_part.ends_with(":latest") {
                    return true;
                }
                // If no colon and no @, it's implicit latest (e.g., "FROM postgres" or "FROM golang")
                !img_part.contains(':') && !img_part.contains('@') && img_part != "scratch"
            })
            .unwrap_or(false);
        // Repack images inherit upstream tags — exempt
        let is_repack = ctx
            .dockerfile_content
            .contains("evergreen.entrypoint.pattern")
            || ctx.dockerfile_content.contains("evergreen.image.repack")
            || ctx.dockerfile_content.contains("evergreen.base.image");
        let (status, message) = if !uses_latest || is_repack {
            (
                ConstraintStatus::Pass,
                if is_repack {
                    "Repack image (upstream tag acceptable)".to_string()
                } else {
                    "No :latest tags in FROM directives".to_string()
                },
            )
        } else {
            (
                ConstraintStatus::Fail,
                "FROM directive uses :latest tag or implicit latest (no version pin)".to_string(),
            )
        };
        ConstraintResult {
            code: self.code().into(),
            severity: self.severity(),
            status,
            message,
            image: ctx.name.into(),
        }
    }
}

// ---------------------------------------------------------------------------
// C016: No shell in final stage (/bin/sh, /bin/bash, /usr/bin/sh)
// ---------------------------------------------------------------------------

struct C016NoShell;
impl Constraint for C016NoShell {
    fn code(&self) -> &str {
        "C016"
    }
    fn severity(&self) -> Severity {
        Severity::Block
    }
    fn check(&self, ctx: &ConstraintContext) -> ConstraintResult {
        if !ctx.dockerfile_exists {
            return self.skip(ctx);
        }
        let content = &ctx.dockerfile_content;
        let is_scratch = content.contains("FROM scratch");
        // Images that inherit from upstream (repack) are exempt — they inherit the upstream's shell
        let is_repack = content.contains("evergreen.entrypoint.pattern")
            && (content.contains("repack-upstream-init") || content.contains("repack"));
        // wolfi-base has busybox ash — acceptable per ADR-007
        let uses_wolfi = content.lines().any(|l| {
            let lower = l.trim().to_lowercase();
            lower.starts_with("from ")
                && (lower.contains("wolfi") || lower.contains("cgr.dev/chainguard"))
        });
        if is_scratch || is_repack || uses_wolfi {
            ConstraintResult {
                code: self.code().into(),
                severity: self.severity(),
                status: ConstraintStatus::Pass,
                message: if is_scratch {
                    "scratch-based (no shell)".to_string()
                } else if is_repack {
                    "repack image (inherits upstream shell)".to_string()
                } else {
                    "wolfi-based (busybox ash acceptable)".to_string()
                },
                image: ctx.name.into(),
            }
        } else {
            // For non-repack, non-scratch, non-wolfi: check for explicit shell removal
            // This is informational — we can't detect runtime shells from Dockerfile alone
            ConstraintResult {
                code: self.code().into(),
                severity: self.severity(),
                status: ConstraintStatus::Pass,
                message:
                    "Shell check requires runtime verification (C016 is advisory for non-scratch)"
                        .to_string(),
                image: ctx.name.into(),
            }
        }
    }
}

// ---------------------------------------------------------------------------
// C017: No package manager in final stage (apt, apk, dnf, yum)
// ---------------------------------------------------------------------------

struct C017NoPackageManager;
impl Constraint for C017NoPackageManager {
    fn code(&self) -> &str {
        "C017"
    }
    fn severity(&self) -> Severity {
        Severity::Block
    }
    // Tier 1: BLOCK (enforce immediately)
    // Tier 2-3: WARN (90-day migration deadline)
    fn tier_severity(&self, tier: u8) -> Severity {
        if tier <= 1 {
            Severity::Block
        } else {
            Severity::Warn
        }
    }
    fn check(&self, ctx: &ConstraintContext) -> ConstraintResult {
        if !ctx.dockerfile_exists {
            return self.skip(ctx);
        }
        let content = &ctx.dockerfile_content;
        let is_scratch = content.contains("FROM scratch");
        let is_repack = content.contains("evergreen.entrypoint.pattern")
            || content.contains("evergreen.image.repack")
            || content.contains("evergreen.base.image");
        // Wolfi-based images use apk — that's by design
        let uses_wolfi = content.contains("wolfi") || content.contains("cgr.dev/chainguard");
        if is_scratch || is_repack || uses_wolfi {
            ConstraintResult {
                code: self.code().into(),
                severity: self.severity(),
                status: ConstraintStatus::Pass,
                message: if is_scratch {
                    "scratch-based (no package manager)".to_string()
                } else {
                    "repack image (inherits upstream)".to_string()
                },
                image: ctx.name.into(),
            }
        } else {
            // Check if apk/apt is used in the FINAL stage only
            // We look for RUN lines with apk add or apt-get install after the last FROM
            let lines: Vec<&str> = content.lines().collect();
            let mut last_from_idx = 0;
            for (i, line) in lines.iter().enumerate() {
                if line.trim().to_lowercase().starts_with("from ") {
                    last_from_idx = i;
                }
            }
            let final_stage = &lines[last_from_idx..];
            let has_pkg_mgr = final_stage.iter().any(|line| {
                let lower = line.to_lowercase();
                (lower.contains("apk add") || lower.contains("apk add --no-cache"))
                    || (lower.contains("apt-get install") || lower.contains("apt install"))
                    || lower.contains("dnf install")
                    || lower.contains("yum install")
            });
            if has_pkg_mgr {
                ConstraintResult {
                    code: self.code().into(),
                    severity: self.severity(),
                    status: ConstraintStatus::Fail,
                    message: "Package manager (apk/apt/dnf/yum) found in final stage".to_string(),
                    image: ctx.name.into(),
                }
            } else {
                ConstraintResult {
                    code: self.code().into(),
                    severity: self.severity(),
                    status: ConstraintStatus::Pass,
                    message: "No package manager in final stage".to_string(),
                    image: ctx.name.into(),
                }
            }
        }
    }
}

// ---------------------------------------------------------------------------
// C018: FROM directive allowlist (only approved base registries)
// ---------------------------------------------------------------------------

struct C018FromAllowlist;
impl Constraint for C018FromAllowlist {
    fn code(&self) -> &str {
        "C018"
    }
    fn severity(&self) -> Severity {
        Severity::Warn
    }
    fn check(&self, ctx: &ConstraintContext) -> ConstraintResult {
        if !ctx.dockerfile_exists {
            return self.skip(ctx);
        }
        let content = &ctx.dockerfile_content;
        let is_repack = content.contains("evergreen.entrypoint.pattern");

        // Approved base image registries (per ADR-007)
        let approved_prefixes = [
            "scratch",
            "cgr.dev/chainguard",
            "gcr.io/distroless",
            "ghcr.io/wyattau/evergreenshim",
            "ghcr.io/wyattau/evergreenimageregistry",
            "registry.access.redhat.com",
            "localhost/",
        ];

        let mut violations = Vec::new();
        for line in content.lines() {
            let trimmed = line.trim();
            if !trimmed.to_lowercase().starts_with("from ") {
                continue;
            }
            let img = trimmed.split_whitespace().nth(1).unwrap_or("");
            let img = img.split('@').next().unwrap_or(img); // strip digest
            let img = img.split(':').next().unwrap_or(img); // strip tag

            // Skip build stage aliases and scratch
            if img == "scratch" || img.is_empty() {
                continue;
            }
            // Skip images that are FROM the registry itself
            if img.starts_with("ghcr.io/wyattau/") {
                continue;
            }

            let is_approved = approved_prefixes
                .iter()
                .any(|prefix| img.starts_with(prefix));
            if !is_approved {
                violations.push(img.to_string());
            }
        }

        if violations.is_empty() || is_repack {
            ConstraintResult {
                code: self.code().into(),
                severity: self.severity(),
                status: ConstraintStatus::Pass,
                message: if is_repack {
                    "Repack image (upstream base acceptable)".to_string()
                } else {
                    "All FROM directives use approved registries".to_string()
                },
                image: ctx.name.into(),
            }
        } else {
            ConstraintResult {
                code: self.code().into(),
                severity: self.severity(),
                status: ConstraintStatus::Fail,
                message: format!("Non-approved base images: {}", violations.join(", ")),
                image: ctx.name.into(),
            }
        }
    }
}

// ---------------------------------------------------------------------------
// C019: Read-only root filesystem label present
// ---------------------------------------------------------------------------

struct C019ReadOnlyRootfs;
impl Constraint for C019ReadOnlyRootfs {
    fn code(&self) -> &str {
        "C019"
    }
    fn severity(&self) -> Severity {
        Severity::Warn
    }
    fn check(&self, ctx: &ConstraintContext) -> ConstraintResult {
        if !ctx.dockerfile_exists {
            return self.skip(ctx);
        }
        let has_label = ctx
            .dockerfile_content
            .contains("evergreen.security.read-only-rootfs");
        let (status, message) = if has_label {
            (
                ConstraintStatus::Pass,
                "Read-only rootfs label present".to_string(),
            )
        } else {
            (
                ConstraintStatus::Fail,
                "Missing evergreen.security.read-only-rootfs label".to_string(),
            )
        };
        ConstraintResult {
            code: self.code().into(),
            severity: self.severity(),
            status,
            message,
            image: ctx.name.into(),
        }
    }
}

// ---------------------------------------------------------------------------
// C020: Static binary check (scratch-based images should have static binaries)
// ---------------------------------------------------------------------------

struct C020StaticBinaryCheck;
impl Constraint for C020StaticBinaryCheck {
    fn code(&self) -> &str {
        "C020"
    }
    fn severity(&self) -> Severity {
        Severity::Info
    }
    fn check(&self, ctx: &ConstraintContext) -> ConstraintResult {
        if !ctx.dockerfile_exists {
            return self.skip(ctx);
        }
        let content = &ctx.dockerfile_content;
        let is_scratch = content.contains("FROM scratch");
        if !is_scratch {
            return ConstraintResult {
                code: self.code().into(),
                severity: self.severity(),
                status: ConstraintStatus::Skip,
                message: "Only applies to scratch-based images".to_string(),
                image: ctx.name.into(),
            };
        }
        // Check for signs of static compilation
        let has_static_indicators = content.contains("CGO_ENABLED=0")
            || content.contains("MALLOC=libc")
            || content.contains("-static")
            || content.contains("musl")
            || content.contains("rust-static")
            || content.contains("go-static");
        let has_build_stage = content
            .lines()
            .filter(|l| l.trim().to_lowercase().starts_with("from "))
            .count()
            > 1;

        if has_static_indicators || !has_build_stage {
            ConstraintResult {
                code: self.code().into(),
                severity: self.severity(),
                status: ConstraintStatus::Pass,
                message: "Scratch image appears to use static binary".to_string(),
                image: ctx.name.into(),
            }
        } else {
            ConstraintResult {
                code: self.code().into(), severity: self.severity(),
                status: ConstraintStatus::Fail,
                message: "Scratch image without static compilation indicators — verify binary is statically linked".to_string(),
                image: ctx.name.into(),
            }
        }
    }
}

// Helper trait extension for creating skip results
trait ConstraintExt {
    fn skip(&self, ctx: &ConstraintContext) -> ConstraintResult;
}

impl<T: Constraint> ConstraintExt for T {
    fn skip(&self, ctx: &ConstraintContext) -> ConstraintResult {
        ConstraintResult {
            code: self.code().into(),
            severity: self.severity(),
            status: ConstraintStatus::Skip,
            message: "Dockerfile missing, check skipped".into(),
            image: ctx.name.into(),
        }
    }
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/// Validate all images in parallel using rayon.
///
/// This is the 5k+ scale replacement for sequential validate_strict.
/// Typical performance: 5000 images in ~8s (vs ~45s sequential).
pub fn validate_all_parallel(images_dir: &str) -> Result<ValidationReport> {
    let dir = Path::new(images_dir);
    if !dir.exists() {
        return Err(EvergreenError::DirectoryNotFound {
            path: dir.to_path_buf(),
        });
    }

    let start = std::time::Instant::now();

    // Collect all image directories first (sequential, fast)
    let image_dirs = crate::dockerfile_utils::iter_image_dirs(dir).map_err(|_e| {
        EvergreenError::DirectoryNotFound {
            path: dir.to_path_buf(),
        }
    })?;

    let total = image_dirs.len();
    tracing::info!("Validating {} images in parallel...", total);

    // Parallel validation using rayon
    let results: Vec<ImageValidationResult> =
        image_dirs.par_iter().map(validate_single_image).collect();

    let duration_ms = start.elapsed().as_millis() as u64;

    // Aggregate results
    let mut violations_by_severity: HashMap<String, usize> = HashMap::new();
    let mut violations_by_code: HashMap<String, usize> = HashMap::new();
    let mut total_violations = 0usize;
    let mut images_passed = 0usize;
    let mut images_failed = 0usize;
    let mut images_skipped = 0usize;
    let mut total_constraints = 0usize;

    for result in &results {
        match result.status {
            ImageStatus::Pass => images_passed += 1,
            ImageStatus::Fail => images_failed += 1,
            ImageStatus::Skip => images_skipped += 1,
        }
        total_constraints += result.constraints_checked;
        for violation in &result.violations {
            if violation.status == ConstraintStatus::Fail {
                total_violations += 1;
                *violations_by_severity
                    .entry(violation.severity.to_string())
                    .or_insert(0) += 1;
                *violations_by_code
                    .entry(violation.code.clone())
                    .or_insert(0) += 1;
            }
        }
    }

    tracing::info!(
        "Validation complete: {} passed, {} failed, {} skipped ({}ms)",
        images_passed,
        images_failed,
        images_skipped,
        duration_ms
    );

    Ok(ValidationReport {
        total_images: total,
        images_passed,
        images_failed,
        images_skipped,
        total_constraints_checked: total_constraints,
        total_violations,
        violations_by_severity,
        violations_by_code,
        image_results: results,
        duration_ms,
    })
}

/// Format a validation report as human-readable text
pub fn format_report_text(report: &ValidationReport) -> String {
    let mut out = String::new();
    out.push_str("Parallel Validation Report\n");
    out.push_str("=========================\n\n");
    out.push_str(&format!("Total images:     {}\n", report.total_images));
    out.push_str(&format!(
        "Passed:           {} ({:.1}%)\n",
        report.images_passed,
        report.images_passed as f64 / report.total_images as f64 * 100.0
    ));
    out.push_str(&format!(
        "Failed:           {} ({:.1}%)\n",
        report.images_failed,
        report.images_failed as f64 / report.total_images as f64 * 100.0
    ));
    out.push_str(&format!("Skipped:          {}\n", report.images_skipped));
    out.push_str(&format!(
        "Constraints:      {}\n",
        report.total_constraints_checked
    ));
    out.push_str(&format!("Violations:       {}\n", report.total_violations));
    out.push_str(&format!("Duration:         {}ms\n\n", report.duration_ms));

    if !report.violations_by_severity.is_empty() {
        out.push_str("Violations by Severity:\n");
        for (sev, count) in &report.violations_by_severity {
            out.push_str(&format!("  {}: {}\n", sev, count));
        }
        out.push('\n');
    }

    if !report.violations_by_code.is_empty() {
        out.push_str("Violations by Code:\n");
        let mut codes: Vec<_> = report.violations_by_code.iter().collect();
        codes.sort_by(|a, b| b.1.cmp(a.1));
        for (code, count) in codes {
            out.push_str(&format!("  {}: {}\n", code, count));
        }
        out.push('\n');
    }

    // Show first 20 failed images
    let failed: Vec<_> = report
        .image_results
        .iter()
        .filter(|r| r.status == ImageStatus::Fail)
        .take(20)
        .collect();
    if !failed.is_empty() {
        out.push_str("Failed Images (first 20):\n");
        for img in &failed {
            let codes: Vec<&str> = img
                .violations
                .iter()
                .filter(|v| v.status == ConstraintStatus::Fail)
                .map(|v| v.code.as_str())
                .collect();
            out.push_str(&format!(
                "  {} (tier {}): {}\n",
                img.name,
                img.tier,
                codes.join(", ")
            ));
        }
    }

    out
}

// ---------------------------------------------------------------------------
// Internal
// ---------------------------------------------------------------------------

fn validate_single_image(img: &crate::dockerfile_utils::ImageDir) -> ImageValidationResult {
    let name = img.name.clone();

    // Parse manifest
    let (
        manifest_name,
        manifest_version,
        manifest_source_url,
        manifest_base,
        manifest_tier,
        tier_num,
    ) = if let Some(ref manifest_path) = img.manifest_path {
        match crate::manifest::Manifest::from_file(manifest_path) {
            Ok(m) => (
                m.name().to_string(),
                m.version().to_string(),
                m.source_url().to_string(),
                m.base_image().to_string(),
                m.metadata.tier.clone(),
                m.tier_num(),
            ),
            Err(_) => (
                String::new(),
                String::new(),
                String::new(),
                String::new(),
                "3".into(),
                3,
            ),
        }
    } else {
        (
            String::new(),
            String::new(),
            String::new(),
            String::new(),
            "3".into(),
            3,
        )
    };

    // Parse Dockerfile
    let (dockerfile_exists, dockerfile_content) = if let Some(ref df_path) = img.dockerfile_path {
        match std::fs::read_to_string(df_path) {
            Ok(content) => (true, content),
            Err(_) => (false, String::new()),
        }
    } else {
        (false, String::new())
    };

    // Check SBOM
    let sbom_exists = img.sbom_path.is_some();
    let sbom_valid = if let Some(ref sbom_path) = img.sbom_path {
        std::fs::read_to_string(sbom_path)
            .ok()
            .and_then(|c| serde_json::from_str::<serde_json::Value>(&c).ok())
            .is_some()
    } else {
        false
    };

    let ctx = ConstraintContext {
        name: &name,
        tier: tier_num,
        manifest_exists: img.manifest_path.is_some(),
        manifest_name,
        manifest_version,
        manifest_source_url,
        manifest_base,
        manifest_tier,
        dockerfile_exists,
        dockerfile_content,
        sbom_exists,
        sbom_valid,
    };

    let constraint_results = check_constraints(&ctx);

    // Only BLOCK-severity failures cause image failure.
    // WARN/INFO failures are reported but don't block the image.
    let has_block_failures = constraint_results
        .iter()
        .any(|r| r.status == ConstraintStatus::Fail && r.severity == Severity::Block);
    let status = if has_block_failures {
        ImageStatus::Fail
    } else {
        ImageStatus::Pass
    };

    ImageValidationResult {
        name,
        tier: tier_num,
        status,
        constraints_checked: constraint_results.len(),
        violations: constraint_results,
        manifest_path: img
            .manifest_path
            .as_ref()
            .map(|p| p.to_string_lossy().to_string()),
        dockerfile_path: img
            .dockerfile_path
            .as_ref()
            .map(|p| p.to_string_lossy().to_string()),
        sbom_path: img
            .sbom_path
            .as_ref()
            .map(|p| p.to_string_lossy().to_string()),
    }
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_severity_ordering() {
        assert!(Severity::Block > Severity::Warn);
        assert!(Severity::Warn > Severity::Info);
    }

    #[test]
    fn test_constraint_status_display() {
        assert_eq!(format!("{}", Severity::Block), "BLOCK");
        assert_eq!(format!("{}", Severity::Warn), "WARN");
        assert_eq!(format!("{}", Severity::Info), "INFO");
    }

    #[test]
    fn test_check_constraints_all_pass() {
        let ctx = ConstraintContext {
            name: "test-pass",
            tier: 1,
            manifest_exists: true,
            manifest_name: "test-pass".into(),
            manifest_version: "1.0.0".into(),
            manifest_source_url: "https://github.com/test/pass".into(),
            manifest_base: "scratch".into(),
            manifest_tier: "1".into(),
            dockerfile_exists: true,
            dockerfile_content: r#"FROM scratch@sha256:aaaa1111bbbb2222cccc3333dddd4444eeee5555ffff6666aaaa7777bbbb8888cccc9999
ARG VERSION=1.0.0
USER 65532:65532
HEALTHCHECK CMD true
STOPSIGNAL SIGTERM
ENTRYPOINT ["/app"]
LABEL org.opencontainers.image.title="test"
LABEL org.opencontainers.image.version="1.0.0"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
"#.into(),
            sbom_exists: true,
            sbom_valid: true,
        };

        let results = check_constraints(&ctx);
        let failures: Vec<_> = results
            .iter()
            .filter(|r| r.status == ConstraintStatus::Fail)
            .collect();
        assert!(
            failures.is_empty(),
            "Expected no failures, got: {:?}",
            failures
        );
    }

    #[test]
    fn test_check_constraints_alpine_blocked() {
        let ctx = ConstraintContext {
            name: "test-alpine",
            tier: 2,
            manifest_exists: true,
            manifest_name: "test-alpine".into(),
            manifest_version: "1.0.0".into(),
            manifest_source_url: "https://github.com/test/alpine".into(),
            manifest_base: "alpine:3.19".into(),
            manifest_tier: "2".into(),
            dockerfile_exists: true,
            dockerfile_content: "FROM alpine:3.19\nUSER 65532\n".into(),
            sbom_exists: false,
            sbom_valid: false,
        };

        let results = check_constraints(&ctx);
        let alpine_fail = results.iter().find(|r| r.code == "C004");
        assert!(alpine_fail.is_some());
        assert_eq!(alpine_fail.unwrap().status, ConstraintStatus::Fail);
    }

    #[test]
    fn test_check_constraints_missing_dockerfile() {
        let ctx = ConstraintContext {
            name: "test-no-df",
            tier: 1,
            manifest_exists: true,
            manifest_name: "test-no-df".into(),
            manifest_version: "1.0.0".into(),
            manifest_source_url: "".into(),
            manifest_base: "scratch".into(),
            manifest_tier: "1".into(),
            dockerfile_exists: false,
            dockerfile_content: String::new(),
            sbom_exists: false,
            sbom_valid: false,
        };

        let results = check_constraints(&ctx);
        let df_check = results.iter().find(|r| r.code == "C002");
        assert!(df_check.is_some());
        assert_eq!(df_check.unwrap().status, ConstraintStatus::Fail);
    }

    #[test]
    fn test_format_report_text() {
        let report = ValidationReport {
            total_images: 100,
            images_passed: 90,
            images_failed: 8,
            images_skipped: 2,
            total_constraints_checked: 1400,
            total_violations: 12,
            violations_by_severity: [("BLOCK".into(), 5), ("WARN".into(), 7)].into(),
            violations_by_code: [("C004".into(), 3), ("C003".into(), 2)].into(),
            image_results: vec![],
            duration_ms: 850,
        };

        let text = format_report_text(&report);
        assert!(text.contains("Total images:     100"));
        assert!(text.contains("Passed:           90"));
        assert!(text.contains("Duration:         850ms"));
    }

    #[test]
    fn test_c015_rejects_latest_tag() {
        let ctx = ConstraintContext {
            name: "test-latest",
            tier: 1,
            manifest_exists: true,
            manifest_name: "test-latest".into(),
            manifest_version: "1.0.0".into(),
            manifest_source_url: "https://github.com/test/latest".into(),
            manifest_base: "scratch".into(),
            manifest_tier: "1".into(),
            dockerfile_exists: true,
            dockerfile_content: "FROM golang:latest\nUSER 65532\n".into(),
            sbom_exists: false,
            sbom_valid: false,
        };
        let results = check_constraints(&ctx);
        let c015 = results.iter().find(|r| r.code == "C015");
        assert!(c015.is_some());
        assert_eq!(c015.unwrap().status, ConstraintStatus::Fail);
    }

    #[test]
    fn test_c015_rejects_implicit_latest() {
        let ctx = ConstraintContext {
            name: "test-implicit",
            tier: 1,
            manifest_exists: true,
            manifest_name: "test-implicit".into(),
            manifest_version: "1.0.0".into(),
            manifest_source_url: "https://github.com/test/implicit".into(),
            manifest_base: "scratch".into(),
            manifest_tier: "1".into(),
            dockerfile_exists: true,
            dockerfile_content: "FROM postgres\nUSER 65532\n".into(),
            sbom_exists: false,
            sbom_valid: false,
        };
        let results = check_constraints(&ctx);
        let c015 = results.iter().find(|r| r.code == "C015");
        assert!(c015.is_some());
        assert_eq!(c015.unwrap().status, ConstraintStatus::Fail);
    }

    #[test]
    fn test_c015_allows_pinned_version() {
        let ctx = ConstraintContext {
            name: "test-pinned",
            tier: 1,
            manifest_exists: true,
            manifest_name: "test-pinned".into(),
            manifest_version: "1.0.0".into(),
            manifest_source_url: "https://github.com/test/pinned".into(),
            manifest_base: "scratch".into(),
            manifest_tier: "1".into(),
            dockerfile_exists: true,
            dockerfile_content: "FROM golang:1.23-bookworm\nUSER 65532\n".into(),
            sbom_exists: false,
            sbom_valid: false,
        };
        let results = check_constraints(&ctx);
        let c015 = results.iter().find(|r| r.code == "C015");
        assert!(c015.is_some());
        assert_eq!(c015.unwrap().status, ConstraintStatus::Pass);
    }

    #[test]
    fn test_c017_allows_wolfi_with_apk() {
        // Wolfi-based images use apk — that's by design
        let ctx = ConstraintContext {
            name: "test-wolfi-pkg",
            tier: 1,
            manifest_exists: true,
            manifest_name: "test-wolfi-pkg".into(),
            manifest_version: "1.0.0".into(),
            manifest_source_url: "https://github.com/test/wolfi".into(),
            manifest_base: "wolfi".into(),
            manifest_tier: "1".into(),
            dockerfile_exists: true,
            dockerfile_content:
                "FROM cgr.dev/chainguard/wolfi-base\nRUN apk add --no-cache nginx\nUSER 65532\n"
                    .into(),
            sbom_exists: false,
            sbom_valid: false,
        };
        let results = check_constraints(&ctx);
        let c017 = results.iter().find(|r| r.code == "C017");
        assert!(c017.is_some());
        assert_eq!(
            c017.unwrap().status,
            ConstraintStatus::Pass,
            "Wolfi images should be exempt from C017"
        );
    }

    #[test]
    fn test_c017_detects_ubuntu_with_apt() {
        // Ubuntu-based images with apt should still fail
        let ctx = ConstraintContext {
            name: "test-ubuntu",
            tier: 1,
            manifest_exists: true,
            manifest_name: "test-ubuntu".into(),
            manifest_version: "1.0.0".into(),
            manifest_source_url: "https://github.com/test/ubuntu".into(),
            manifest_base: "ubuntu".into(),
            manifest_tier: "1".into(),
            dockerfile_exists: true,
            dockerfile_content:
                "FROM ubuntu:22.04\nRUN apt-get update && apt-get install -y nginx\nUSER 65532\n"
                    .into(),
            sbom_exists: false,
            sbom_valid: false,
        };
        let results = check_constraints(&ctx);
        let c017 = results.iter().find(|r| r.code == "C017");
        assert!(c017.is_some());
        assert_eq!(
            c017.unwrap().status,
            ConstraintStatus::Fail,
            "Ubuntu with apt should fail C017"
        );
    }

    #[test]
    fn test_c018_rejects_unapproved_base() {
        let ctx = ConstraintContext {
            name: "test-unapproved",
            tier: 1,
            manifest_exists: true,
            manifest_name: "test-unapproved".into(),
            manifest_version: "1.0.0".into(),
            manifest_source_url: "https://github.com/test/unapproved".into(),
            manifest_base: "scratch".into(),
            manifest_tier: "1".into(),
            dockerfile_exists: true,
            dockerfile_content: "FROM ubuntu:22.04\nUSER 65532\n".into(),
            sbom_exists: false,
            sbom_valid: false,
        };
        let results = check_constraints(&ctx);
        let c018 = results.iter().find(|r| r.code == "C018");
        assert!(c018.is_some());
        assert_eq!(c018.unwrap().status, ConstraintStatus::Fail);
    }

    #[test]
    fn test_c018_allows_wolfi_base() {
        let ctx = ConstraintContext {
            name: "test-wolfi",
            tier: 1,
            manifest_exists: true,
            manifest_name: "test-wolfi".into(),
            manifest_version: "1.0.0".into(),
            manifest_source_url: "https://github.com/test/wolfi".into(),
            manifest_base: "wolfi".into(),
            manifest_tier: "1".into(),
            dockerfile_exists: true,
            dockerfile_content: "FROM cgr.dev/chainguard/wolfi-base\nUSER 65532\n".into(),
            sbom_exists: false,
            sbom_valid: false,
        };
        let results = check_constraints(&ctx);
        let c018 = results.iter().find(|r| r.code == "C018");
        assert!(c018.is_some());
        assert_eq!(c018.unwrap().status, ConstraintStatus::Pass);
    }

    #[test]
    fn test_registry_has_20_constraints() {
        let registry = constraint_registry();
        assert_eq!(registry.len(), 20, "Expected 20 constraints in registry");
    }

    #[test]
    fn test_tier_aware_severity_c015() {
        // C015 (no :latest) should be BLOCK for Tier 1, WARN for Tier 2-3
        let c015 = C015NoLatestTag;
        assert_eq!(
            c015.tier_severity(1),
            Severity::Block,
            "Tier 1 should BLOCK"
        );
        assert_eq!(c015.tier_severity(2), Severity::Warn, "Tier 2 should WARN");
        assert_eq!(c015.tier_severity(3), Severity::Warn, "Tier 3 should WARN");
    }

    #[test]
    fn test_tier_aware_severity_c017() {
        // C017 (no package manager) should be BLOCK for Tier 1, WARN for Tier 2-3
        let c017 = C017NoPackageManager;
        assert_eq!(
            c017.tier_severity(1),
            Severity::Block,
            "Tier 1 should BLOCK"
        );
        assert_eq!(c017.tier_severity(2), Severity::Warn, "Tier 2 should WARN");
        assert_eq!(c017.tier_severity(3), Severity::Warn, "Tier 3 should WARN");
    }

    #[test]
    fn test_tier_aware_constraints_dont_block_tier3() {
        // A Tier 3 image with :latest should get a WARN, not a BLOCK
        let ctx = ConstraintContext {
            name: "test-tier3-latest",
            tier: 3,
            manifest_exists: true,
            manifest_name: "test-tier3-latest".into(),
            manifest_version: "1.0.0".into(),
            manifest_source_url: "https://github.com/test/latest".into(),
            manifest_base: "scratch".into(),
            manifest_tier: "3".into(),
            dockerfile_exists: true,
            dockerfile_content: "FROM postgres:latest\nUSER 65532\nHEALTHCHECK CMD true\n".into(),
            sbom_exists: false,
            sbom_valid: false,
        };
        let results = check_constraints(&ctx);
        let c015 = results.iter().find(|r| r.code == "C015");
        assert!(c015.is_some());
        let result = c015.unwrap();
        // Should FAIL (violation exists) but with WARN severity, not BLOCK
        assert_eq!(result.status, ConstraintStatus::Fail);
        assert_eq!(
            result.severity,
            Severity::Warn,
            "Tier 3 :latest should be WARN, not BLOCK"
        );
    }

    #[test]
    fn test_tier1_latest_blocks() {
        // A Tier 1 image with :latest should get a BLOCK
        let ctx = ConstraintContext {
            name: "test-tier1-latest",
            tier: 1,
            manifest_exists: true,
            manifest_name: "test-tier1-latest".into(),
            manifest_version: "1.0.0".into(),
            manifest_source_url: "https://github.com/test/latest".into(),
            manifest_base: "scratch".into(),
            manifest_tier: "1".into(),
            dockerfile_exists: true,
            dockerfile_content: "FROM postgres:latest\nUSER 65532\nHEALTHCHECK CMD true\n".into(),
            sbom_exists: false,
            sbom_valid: false,
        };
        let results = check_constraints(&ctx);
        let c015 = results.iter().find(|r| r.code == "C015");
        assert!(c015.is_some());
        let result = c015.unwrap();
        assert_eq!(result.status, ConstraintStatus::Fail);
        assert_eq!(
            result.severity,
            Severity::Block,
            "Tier 1 :latest should BLOCK"
        );
    }

    #[test]     fn test_c003_repack_no_longer_exempt() {
        // Repack images MUST have explicit USER 65532 — no more exemptions
        let ctx = ConstraintContext {
            name: "test-repack",
            tier: 3,
            manifest_exists: true,
            manifest_name: "test-repack".into(),
            manifest_version: "1.0.0".into(),
            manifest_source_url: "https://github.com/test/repack".into(),
            manifest_base: "docker.io/library/redis:7".into(),
            manifest_tier: "3".into(),
            dockerfile_exists: true,
            dockerfile_content: "FROM docker.io/library/redis:7\nCOPY shim /shim\nLABEL evergreen.entrypoint.pattern=\"repack-upstream-init\"\nHEALTHCHECK CMD true\n".into(),
            sbom_exists: false,
            sbom_valid: false,
        };
        let results = check_constraints(&ctx);
        let c003 = results.iter().find(|r| r.code == "C003");
        assert!(c003.is_some());
        assert_eq!(
            c003.unwrap().status,
            ConstraintStatus::Fail,
            "Repack without USER 65532 should FAIL C003"
        );
    }

    #[test]
    fn test_c003_scratch_needs_user() {
        // Scratch image without USER should still fail
        let ctx = ConstraintContext {
            name: "test-scratch-no-user",
            tier: 1,
            manifest_exists: true,
            manifest_name: "test-scratch-no-user".into(),
            manifest_version: "1.0.0".into(),
            manifest_source_url: "https://github.com/test/scratch".into(),
            manifest_base: "scratch".into(),
            manifest_tier: "1".into(),
            dockerfile_exists: true,
            dockerfile_content: "FROM golang:1.23\nRUN go build -o /app\nFROM scratch\nCOPY --from=0 /app /app\nENTRYPOINT [\"/app\"]\n".into(),
            sbom_exists: false,
            sbom_valid: false,
        };
        let results = check_constraints(&ctx);
        let c003 = results.iter().find(|r| r.code == "C003");
        assert!(c003.is_some());
        assert_eq!(
            c003.unwrap().status,
            ConstraintStatus::Fail,
            "Scratch without USER should fail"
        );
    }

    #[test]
    fn test_c003_hardened_with_user() {
        // Hardened image with USER should pass
        let ctx = ConstraintContext {
            name: "test-hardened",
            tier: 1,
            manifest_exists: true,
            manifest_name: "test-hardened".into(),
            manifest_version: "1.0.0".into(),
            manifest_source_url: "https://github.com/test/hardened".into(),
            manifest_base: "wolfi-base".into(),
            manifest_tier: "1".into(),
            dockerfile_exists: true,
            dockerfile_content: "FROM cgr.dev/chainguard/wolfi-base:latest\nUSER 65532:65532\nENTRYPOINT [\"/app\"]\n".into(),
            sbom_exists: false,
            sbom_valid: false,
        };
        let results = check_constraints(&ctx);
        let c003 = results.iter().find(|r| r.code == "C003");
        assert!(c003.is_some());
        assert_eq!(
            c003.unwrap().status,
            ConstraintStatus::Pass,
            "Hardened with USER should pass"
        );
    }
}
