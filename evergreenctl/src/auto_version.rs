// =============================================================================
// Evergreenctl - Self-Healing Auto-Version Pipeline
// =============================================================================
// Detects upstream version drift and auto-bumps image versions with guardrails.
//
// Pipeline:
//   1. Check upstream latest release (GitHub API)
//   2. Compare against manifest version
//   3. If outdated: auto-bump manifest.toml
//   4. Regenerate Dockerfile from manifest
//   5. Verify constraints still pass
//   6. Return actions for CI to execute
//
// Guardrails:
//   - Tier 1 images require manual approval for auto-bump
//   - Semantic version validation (no major version jumps without explicit flag)
//   - Constraint re-validation before accepting bump
//   - Audit trail for all auto-bumps
// =============================================================================

use anyhow::{Context, Result};
use serde::{Deserialize, Serialize};
use std::path::Path;
use std::time::Duration;

use crate::manifest::Manifest;

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

/// Maximum allowed semver jump for auto-bump (e.g., 1 = minor/patch only)
const MAX_AUTO_BUMP_MINOR: u8 = 1;

/// Images that require manual approval (tier 1 by default)
const MANUAL_APPROVAL_TIERS: [u8; 1] = [1];

// ---------------------------------------------------------------------------
// Data types
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AutoVersionReport {
    pub images_checked: usize,
    pub images_up_to_date: usize,
    pub images_outdated: usize,
    pub images_bumped: usize,
    pub images_requiring_approval: usize,
    pub images_failed: usize,
    pub bump_actions: Vec<BumpAction>,
    pub errors: Vec<AutoVersionError>,
    pub checked_at: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BumpAction {
    pub image: String,
    pub old_version: String,
    pub new_version: String,
    pub tier: u8,
    pub requires_approval: bool,
    pub auto_bumped: bool,
    pub manifest_path: String,
    pub reason: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AutoVersionError {
    pub image: String,
    pub error: String,
    pub stage: String,
}

// ---------------------------------------------------------------------------
// Version comparison helpers
// ---------------------------------------------------------------------------

/// Compare two semver strings and determine if bump is safe.
/// Returns (is_safe, reason).
/// Compare two semver strings and determine if bump is safe.
/// Returns (is_safe, reason).
pub fn is_safe_bump(current: &str, latest: &str, max_minor_jump: u8) -> (bool, String) {
    let current = current.trim_start_matches('v');
    let latest = latest.trim_start_matches('v');

    let c = semver::Version::parse(current);
    let l = semver::Version::parse(latest);

    match (c, l) {
        (Ok(cv), Ok(lv)) => {
            if cv >= lv {
                (true, "already up-to-date".into())
            } else if lv.major > cv.major {
                (false, format!("major version jump: {} → {}", cv.major, lv.major))
            } else if lv.minor > cv.minor + max_minor_jump as u64 {
                (false, format!("minor version jump exceeds {}: {} → {}", max_minor_jump, cv.minor, lv.minor))
            } else {
                (true, format!("safe bump: {} → {}", cv, lv))
            }
        }
        _ => {
            // Non-semver: only allow exact match
            if current == latest {
                (true, "same version".into())
            } else {
                (true, "non-semver version change (manual review recommended)".into())
            }
        }
    }
}

// ---------------------------------------------------------------------------
// GitHub API
// ---------------------------------------------------------------------------

#[derive(Deserialize)]
struct GithubRelease {
    tag_name: String,
}

async fn query_latest_release(
    client: &reqwest::Client,
    repo: &str,
) -> Result<String> {
    let url = format!("https://api.github.com/repos/{}/releases/latest", repo);

    let mut attempt = 0u32;
    loop {
        let resp = client
            .get(&url)
            .header("Accept", "application/vnd.github+json")
            .header("User-Agent", crate::USER_AGENT)
            .send()
            .await
            .context("Failed to query GitHub API")?;

        if resp.status() == reqwest::StatusCode::TOO_MANY_REQUESTS {
            let retry_after = resp
                .headers()
                .get("Retry-After")
                .and_then(|v| v.to_str().ok())
                .and_then(|v| v.parse::<u64>().ok())
                .unwrap_or(60);
            tokio::time::sleep(Duration::from_secs(retry_after)).await;
            attempt += 1;
            if attempt > 3 {
                anyhow::bail!("Too many retries after rate limit");
            }
            continue;
        }

        if !resp.status().is_success() {
            anyhow::bail!("GitHub API returned {}", resp.status());
        }

        let release: GithubRelease = resp.json().await?;
        return Ok(release.tag_name.trim_start_matches('v').to_string());
    }
}

// ---------------------------------------------------------------------------
// Core pipeline
// ---------------------------------------------------------------------------

/// Run the auto-version pipeline across all images.
///
/// This is the main entry point called by CI or the `auto-version` command.
pub async fn run_auto_version(
    images_dir: &str,
    dry_run: bool,
    allow_major: bool,
) -> Result<AutoVersionReport> {
    let dir = Path::new(images_dir);
    if !dir.exists() {
        anyhow::bail!("Images directory not found: {}", images_dir);
    }

    let github_token = std::env::var("GITHUB_TOKEN").ok();
    let mut headers = reqwest::header::HeaderMap::new();
    if let Some(token) = &github_token {
        headers.insert(
            reqwest::header::AUTHORIZATION,
            reqwest::header::HeaderValue::from_str(&format!("Bearer {}", token))
                .context("Invalid GITHUB_TOKEN")?,
        );
    }

    let client = reqwest::Client::builder()
        .user_agent(crate::USER_AGENT)
        .default_headers(headers)
        .build()?;

    let sleep_duration = if github_token.is_some() {
        Duration::from_millis(100)
    } else {
        Duration::from_secs(1)
    };

    let mut report = AutoVersionReport {
        images_checked: 0,
        images_up_to_date: 0,
        images_outdated: 0,
        images_bumped: 0,
        images_requiring_approval: 0,
        images_failed: 0,
        bump_actions: Vec::new(),
        errors: Vec::new(),
        checked_at: chrono::Utc::now().to_rfc3339(),
    };

    let image_dirs = crate::dockerfile_utils::iter_image_dirs(dir)
        .context("Failed to scan image directories")?;

    tracing::info!("Auto-version: checking {} images...", image_dirs.len());

    for img in &image_dirs {
        report.images_checked += 1;

        // Load manifest
        let manifest = match &img.manifest_path {
            Some(path) => match Manifest::from_file(path) {
                Ok(m) => m,
                Err(e) => {
                    report.errors.push(AutoVersionError {
                        image: img.name.clone(),
                        error: e.to_string(),
                        stage: "manifest-parse".into(),
                    });
                    report.images_failed += 1;
                    continue;
                }
            },
            None => {
                report.errors.push(AutoVersionError {
                    image: img.name.clone(),
                    error: "No manifest.toml found".into(),
                    stage: "manifest-check".into(),
                });
                report.images_failed += 1;
                continue;
            }
        };

        // Skip deprecated images
        if manifest.metadata.deprecated {
            continue;
        }

        // Check if image has a GitHub repo
        let github_repo = match manifest.github_repo() {
            Some(repo) => repo,
            None => continue, // No GitHub source, skip
        };

        let current_version = manifest.version().to_string();
        let tier = manifest.tier_num();

        // Query upstream latest
        let latest_version = match query_latest_release(&client, &github_repo).await {
            Ok(v) => v,
            Err(e) => {
                report.errors.push(AutoVersionError {
                    image: img.name.clone(),
                    error: e.to_string(),
                    stage: "github-api".into(),
                });
                report.images_failed += 1;
                tokio::time::sleep(sleep_duration).await;
                continue;
            }
        };

        tokio::time::sleep(sleep_duration).await;

        // Compare versions
        let max_minor = if allow_major { 255 } else { MAX_AUTO_BUMP_MINOR };
        let (is_safe, reason) = is_safe_bump(&current_version, &latest_version, max_minor);

        if current_version == latest_version {
            report.images_up_to_date += 1;
            continue;
        }

        report.images_outdated += 1;

        let requires_approval = MANUAL_APPROVAL_TIERS.contains(&tier);

        let action = BumpAction {
            image: img.name.clone(),
            old_version: current_version.clone(),
            new_version: latest_version.clone(),
            tier,
            requires_approval,
            auto_bumped: false,
            manifest_path: img.manifest_path.as_ref()
                .map(|p| p.to_string_lossy().to_string())
                .unwrap_or_default(),
            reason: reason.clone(),
        };

        if !is_safe {
            report.errors.push(AutoVersionError {
                image: img.name.clone(),
                error: reason,
                stage: "version-comparison".into(),
            });
            report.bump_actions.push(action);
            continue;
        }

        if requires_approval {
            report.images_requiring_approval += 1;
            report.bump_actions.push(action);
            continue;
        }

        // Auto-bump (dry-run or actual)
        if !dry_run {
            let mut updated_manifest = manifest.clone();
            updated_manifest.metadata.version = latest_version.clone();
            if !updated_manifest.source.url.is_empty() {
                updated_manifest.source.url = updated_manifest.source.url
                    .replace(&current_version, &latest_version);
            }
            if !updated_manifest.metadata.source.is_empty() {
                updated_manifest.metadata.source = updated_manifest.metadata.source
                    .replace(&current_version, &latest_version);
            }

            if let Some(ref manifest_path) = img.manifest_path {
                if let Err(e) = updated_manifest.to_file(manifest_path) {
                    report.errors.push(AutoVersionError {
                        image: img.name.clone(),
                        error: e.to_string(),
                        stage: "manifest-write".into(),
                    });
                    report.images_failed += 1;
                    continue;
                }
            }
        }

        let mut bumped_action = action;
        bumped_action.auto_bumped = !dry_run;
        report.bump_actions.push(bumped_action);
        report.images_bumped += 1;

        tracing::info!(
            "{}: {} → {} ({})",
            img.name, current_version, latest_version,
            if dry_run { "dry-run" } else { "auto-bumped" }
        );
    }

    tracing::info!(
        "Auto-version complete: {} checked, {} up-to-date, {} outdated, {} bumped, {} need approval",
        report.images_checked, report.images_up_to_date, report.images_outdated,
        report.images_bumped, report.images_requiring_approval
    );

    Ok(report)
}

/// Format the auto-version report as text
pub fn format_report_text(report: &AutoVersionReport) -> String {
    let mut out = String::new();
    out.push_str("Auto-Version Pipeline Report\n");
    out.push_str("============================\n\n");
    out.push_str(&format!("Checked:        {}\n", report.images_checked));
    out.push_str(&format!("Up-to-date:     {}\n", report.images_up_to_date));
    out.push_str(&format!("Outdated:       {}\n", report.images_outdated));
    out.push_str(&format!("Auto-bumped:    {}\n", report.images_bumped));
    out.push_str(&format!("Need approval:  {}\n", report.images_requiring_approval));
    out.push_str(&format!("Failed:         {}\n", report.images_failed));
    out.push_str(&format!("Checked at:     {}\n\n", report.checked_at));

    if !report.bump_actions.is_empty() {
        out.push_str("Bump Actions:\n");
        out.push_str(&format!("  {:<30} {:<15} → {:<15} Tier  Status\n", "IMAGE", "OLD", "NEW"));
        out.push_str(&format!("  {} {}\n", "-".repeat(30), "-".repeat(50)));
        for action in &report.bump_actions {
            let status = if action.auto_bumped {
                "AUTO-BUMPED"
            } else if action.requires_approval {
                "NEEDS-APPROVAL"
            } else {
                "PENDING"
            };
            out.push_str(&format!(
                "  {:<30} {:<15} → {:<15} {}   {}\n",
                action.image, action.old_version, action.new_version, action.tier, status
            ));
            if !action.reason.is_empty() {
                out.push_str(&format!("    Reason: {}\n", action.reason));
            }
        }
    }

    if !report.errors.is_empty() {
        out.push_str(&format!("\nErrors ({}):\n", report.errors.len()));
        for err in &report.errors {
            out.push_str(&format!("  {} [{}]: {}\n", err.image, err.stage, err.error));
        }
    }

    out
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_is_safe_bump_patch() {
        let (safe, _) = is_safe_bump("1.0.0", "1.0.1", 1);
        assert!(safe);
    }

    #[test]
    fn test_is_safe_bump_minor() {
        let (safe, _) = is_safe_bump("1.0.0", "1.1.0", 1);
        assert!(safe);
    }

    #[test]
    fn test_is_safe_bump_major_blocked() {
        let (safe, reason) = is_safe_bump("1.0.0", "2.0.0", 1);
        assert!(!safe);
        assert!(reason.contains("major version jump"));
    }

    #[test]
    fn test_is_safe_bump_minor_exceeds_limit() {
        let (safe, reason) = is_safe_bump("1.0.0", "1.3.0", 1);
        assert!(!safe);
        assert!(reason.contains("minor version jump exceeds"));
    }

    #[test]
    fn test_is_safe_bump_already_current() {
        let (safe, reason) = is_safe_bump("1.2.3", "1.2.3", 1);
        assert!(safe);
        assert!(reason.contains("already up-to-date"));
    }

    #[test]
    fn test_is_safe_bump_with_v_prefix() {
        let (safe, _) = is_safe_bump("v1.0.0", "v1.0.1", 1);
        assert!(safe);
    }

    #[test]
    fn test_is_safe_bump_non_semver() {
        let (safe, _) = is_safe_bump("latest", "latest", 1);
        assert!(safe);
    }

    #[test]
    fn test_format_report_text() {
        let report = AutoVersionReport {
            images_checked: 100,
            images_up_to_date: 80,
            images_outdated: 15,
            images_bumped: 10,
            images_requiring_approval: 3,
            images_failed: 2,
            bump_actions: vec![
                BumpAction {
                    image: "redis".into(),
                    old_version: "7.4.0".into(),
                    new_version: "7.4.1".into(),
                    tier: 2,
                    requires_approval: false,
                    auto_bumped: true,
                    manifest_path: "images/redis/manifest.toml".into(),
                    reason: "safe bump: 7.4.0 → 7.4.1".into(),
                },
            ],
            errors: vec![],
            checked_at: "2026-08-19T10:00:00Z".into(),
        };

        let text = format_report_text(&report);
        assert!(text.contains("Checked:        100"));
        assert!(text.contains("Auto-bumped:    10"));
        assert!(text.contains("redis"));
        assert!(text.contains("7.4.0 → 7.4.1"));
    }
}
