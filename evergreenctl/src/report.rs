use anyhow::{Context, Result};
use serde::Serialize;
use std::collections::HashMap;
use std::path::Path;
use walkdir::WalkDir;

#[derive(Debug, Serialize)]
pub struct HealthReport {
    pub total_images: usize,
    pub by_category: HashMap<String, usize>,
    pub by_tier: HashMap<String, usize>,
    pub digest_pinned_from: usize,
    pub unpinned_from: usize,
    pub healthcheck_none: usize,
    pub healthcheck_real: usize,
    pub deprecated_count: usize,
    pub health_score: f64,
}

struct ImageStats {
    has_digest_pin: bool,
    has_healthcheck_none: bool,
    has_real_healthcheck: bool,
    is_deprecated: bool,
    category: String,
    tier: String,
}

fn categorize_image(manifest: &crate::manifest::Manifest) -> String {
    if let Some(cat) = manifest.label("org.opencontainers.image.category") {
        return cat.to_string();
    }
    if !manifest.metadata.description.is_empty() {
        return "uncategorized".to_string();
    }
    "uncategorized".to_string()
}

fn analyze_image(image_dir: &Path) -> Result<ImageStats> {
    let manifest_path = image_dir.join("manifest.toml");
    let dockerfile_path = image_dir.join("Dockerfile");

    let mut stats = ImageStats {
        has_digest_pin: false,
        has_healthcheck_none: false,
        has_real_healthcheck: false,
        is_deprecated: false,
        category: "uncategorized".to_string(),
        tier: "3".to_string(),
    };

    if manifest_path.exists() {
        let manifest = crate::manifest::Manifest::from_file(&manifest_path)?;
        stats.category = categorize_image(&manifest);
        stats.tier = if manifest.metadata.tier.is_empty() {
            "3".to_string()
        } else {
            manifest.metadata.tier.clone()
        };
        stats.is_deprecated = manifest.metadata.deprecated;
    }

    if dockerfile_path.exists() {
        let content = std::fs::read_to_string(&dockerfile_path)
            .with_context(|| format!("Failed to read {}", dockerfile_path.display()))?;

        for line in content.lines() {
            let trimmed = line.trim().to_uppercase();
            if trimmed.starts_with("FROM ") && line.contains("@sha256:") {
                stats.has_digest_pin = true;
            }
            if trimmed.contains("HEALTHCHECK NONE") {
                stats.has_healthcheck_none = true;
            } else if trimmed.starts_with("HEALTHCHECK") && !trimmed.contains("NONE") {
                stats.has_real_healthcheck = true;
            }
        }
    }

    Ok(stats)
}

pub fn generate_report(images_dir: &Path) -> Result<HealthReport> {
    let mut all_stats: Vec<ImageStats> = Vec::new();

    for entry in WalkDir::new(images_dir)
        .min_depth(1)
        .max_depth(1)
        .sort_by_file_name()
    {
        let entry = entry?;
        let path = entry.path();
        if !path.is_dir() {
            continue;
        }
        let has_manifest = path.join("manifest.toml").exists();
        let has_dockerfile = path.join("Dockerfile").exists();
        if !has_manifest && !has_dockerfile {
            continue;
        }

        match analyze_image(path) {
            Ok(stats) => all_stats.push(stats),
            Err(e) => {
                tracing::warn!("Skipping {}: {}", path.display(), e);
            }
        }
    }

    let total = all_stats.len();
    let mut by_category: HashMap<String, usize> = HashMap::new();
    let mut by_tier: HashMap<String, usize> = HashMap::new();
    let mut digest_pinned = 0usize;
    let mut unpinned = 0usize;
    let mut healthcheck_none = 0usize;
    let mut healthcheck_real = 0usize;
    let mut deprecated = 0usize;
    let mut passing = 0usize;

    for stats in &all_stats {
        *by_category.entry(stats.category.clone()).or_insert(0) += 1;
        *by_tier.entry(stats.tier.clone()).or_insert(0) += 1;

        if stats.has_digest_pin {
            digest_pinned += 1;
        } else {
            unpinned += 1;
        }

        if stats.has_healthcheck_none {
            healthcheck_none += 1;
        }
        if stats.has_real_healthcheck {
            healthcheck_real += 1;
        }

        if stats.is_deprecated {
            deprecated += 1;
        }

        if stats.has_digest_pin && !stats.has_healthcheck_none && !stats.is_deprecated {
            passing += 1;
        }
    }

    let health_score = if total > 0 {
        passing as f64 / total as f64 * 100.0
    } else {
        0.0
    };

    Ok(HealthReport {
        total_images: total,
        by_category,
        by_tier,
        digest_pinned_from: digest_pinned,
        unpinned_from: unpinned,
        healthcheck_none,
        healthcheck_real,
        deprecated_count: deprecated,
        health_score,
    })
}

pub fn format_text(report: &HealthReport) -> String {
    let mut out = String::new();
    out.push_str("Registry Health Report\n");
    out.push_str("====================\n\n");
    out.push_str(&format!("Total images: {}\n\n", report.total_images));

    out.push_str("By Category:\n");
    let mut cats: Vec<_> = report.by_category.iter().collect();
    cats.sort_by_key(|(k, _)| *k);
    for (cat, count) in cats {
        out.push_str(&format!("  {}: {}\n", cat, count));
    }

    out.push_str("\nBy Tier:\n");
    let mut tiers: Vec<_> = report.by_tier.iter().collect();
    tiers.sort_by_key(|(k, _)| (*k).clone());
    for (tier, count) in tiers {
        out.push_str(&format!("  Tier {}: {}\n", tier, count));
    }

    out.push_str(&format!(
        "\nDigest-pinned FROM: {}\n",
        report.digest_pinned_from
    ));
    out.push_str(&format!("Unpinned FROM: {}\n", report.unpinned_from));
    out.push_str(&format!("HEALTHCHECK NONE: {}\n", report.healthcheck_none));
    out.push_str(&format!("Real HEALTHCHECK: {}\n", report.healthcheck_real));
    out.push_str(&format!("Deprecated: {}\n", report.deprecated_count));
    out.push_str(&format!("\nHealth Score: {:.1}%\n", report.health_score));

    out
}

#[cfg(test)]
mod tests {
    use super::*;

    fn create_image_dir(
        tmp: &tempfile::TempDir,
        name: &str,
        manifest_content: Option<&str>,
        dockerfile_content: Option<&str>,
    ) {
        let dir = tmp.path().join(name);
        std::fs::create_dir_all(&dir).unwrap();
        if let Some(mc) = manifest_content {
            std::fs::write(dir.join("manifest.toml"), mc).unwrap();
        }
        if let Some(dc) = dockerfile_content {
            std::fs::write(dir.join("Dockerfile"), dc).unwrap();
        }
    }

    #[test]
    fn test_report_with_temp_image_dirs() {
        let tmp = tempfile::tempdir().unwrap();

        create_image_dir(
            &tmp,
            "redis",
            Some(
                r#"
[metadata]
name = "redis"
version = "7.4.1"
tier = "1"

[build]
base = "cgr.dev/chainguard/wolfi-base:latest"

[source]
url = "https://example.com/redis.tar.gz"

[runtime]
entrypoint = ["/redis"]
"#,
            ),
            Some("FROM cgr.dev/chainguard/wolfi-base:latest@sha256:abc123\nHEALTHCHECK CMD curl -f http://localhost:6379\n"),
        );

        create_image_dir(
            &tmp,
            "nginx",
            Some(
                r#"
[metadata]
name = "nginx"
version = "1.27"
tier = "1"

[build]
base = "cgr.dev/chainguard/wolfi-base:latest"

[source]
url = "https://example.com/nginx.tar.gz"

[runtime]
entrypoint = ["/nginx"]
"#,
            ),
            Some("FROM cgr.dev/chainguard/wolfi-base:latest\nHEALTHCHECK NONE\n"),
        );

        let report = generate_report(tmp.path()).unwrap();
        assert_eq!(report.total_images, 2);
        assert_eq!(report.digest_pinned_from, 1);
        assert_eq!(report.unpinned_from, 1);
        assert_eq!(report.healthcheck_none, 1);
        assert_eq!(report.healthcheck_real, 1);
    }

    #[test]
    fn test_report_mixed_categories() {
        let tmp = tempfile::tempdir().unwrap();

        create_image_dir(
            &tmp,
            "redis",
            Some(
                r#"
[metadata]
name = "redis"
version = "7.4.1"
tier = "1"

[labels]
"org.opencontainers.image.category" = "database"

[build]
base = "scratch"

[source]
url = "https://example.com/redis.tar.gz"

[runtime]
entrypoint = ["/redis"]
"#,
            ),
            Some("FROM scratch\n"),
        );

        create_image_dir(
            &tmp,
            "nginx",
            Some(
                r#"
[metadata]
name = "nginx"
version = "1.27"
tier = "2"

[labels]
"org.opencontainers.image.category" = "webserver"

[build]
base = "scratch"

[source]
url = "https://example.com/nginx.tar.gz"

[runtime]
entrypoint = ["/nginx"]
"#,
            ),
            Some("FROM scratch\n"),
        );

        create_image_dir(
            &tmp,
            "postgres",
            Some(
                r#"
[metadata]
name = "postgres"
version = "16"
tier = "1"

[labels]
"org.opencontainers.image.category" = "database"

[build]
base = "scratch"

[source]
url = "https://example.com/postgres.tar.gz"

[runtime]
entrypoint = ["/postgres"]
"#,
            ),
            Some("FROM scratch\n"),
        );

        let report = generate_report(tmp.path()).unwrap();
        assert_eq!(report.total_images, 3);
        assert_eq!(report.by_category.get("database"), Some(&2));
        assert_eq!(report.by_category.get("webserver"), Some(&1));
        assert_eq!(report.by_tier.get("1"), Some(&2));
        assert_eq!(report.by_tier.get("2"), Some(&1));
    }

    #[test]
    fn test_report_format_output() {
        let tmp = tempfile::tempdir().unwrap();

        create_image_dir(
            &tmp,
            "testimg",
            Some(
                r#"
[metadata]
name = "testimg"
version = "1.0"
tier = "1"

[build]
base = "scratch"

[source]
url = "https://example.com/test.tar.gz"

[runtime]
entrypoint = ["/test"]
"#,
            ),
            Some("FROM scratch@sha256:deadbeef\n"),
        );

        let report = generate_report(tmp.path()).unwrap();

        let json_output = serde_json::to_string_pretty(&report).unwrap();
        assert!(json_output.contains("total_images"));
        assert!(json_output.contains("health_score"));

        let text_output = format_text(&report);
        assert!(text_output.contains("Registry Health Report"));
        assert!(text_output.contains("Total images: 1"));
        assert!(text_output.contains("Health Score:"));
    }

    #[test]
    fn test_report_empty_directory() {
        let tmp = tempfile::tempdir().unwrap();
        let report = generate_report(tmp.path()).unwrap();
        assert_eq!(report.total_images, 0);
        assert_eq!(report.health_score, 0.0);
    }

    #[test]
    fn test_report_deprecated_count() {
        let tmp = tempfile::tempdir().unwrap();

        create_image_dir(
            &tmp,
            "oldimg",
            Some(
                r#"
[metadata]
name = "oldimg"
version = "1.0"
deprecated = true
tier = "3"

[build]
base = "scratch"

[source]
url = "https://example.com/old.tar.gz"

[runtime]
entrypoint = ["/old"]
"#,
            ),
            Some("FROM scratch@sha256:aaa\n"),
        );

        create_image_dir(
            &tmp,
            "newimg",
            Some(
                r#"
[metadata]
name = "newimg"
version = "2.0"
tier = "1"

[build]
base = "scratch"

[source]
url = "https://example.com/new.tar.gz"

[runtime]
entrypoint = ["/new"]
"#,
            ),
            Some("FROM scratch@sha256:bbb\n"),
        );

        let report = generate_report(tmp.path()).unwrap();
        assert_eq!(report.total_images, 2);
        assert_eq!(report.deprecated_count, 1);
        assert_eq!(report.health_score, 50.0);
    }
}
