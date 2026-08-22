// =============================================================================
// Evergreenctl - Command Dispatcher
// =============================================================================
// Encapsulates all command execution logic, keeping main.rs minimal.
// Each command is dispatched to its dedicated module function.
// =============================================================================

use clap::CommandFactory;
use rusqlite::params;
use std::path::Path;

use crate::cli::{Cli, Commands};

/// Execute the given command and return any errors.
///
/// This is the single entry point for all command logic. `main.rs` only
/// handles CLI parsing, path validation, and error reporting.
pub async fn execute(command: Commands) -> anyhow::Result<()> {
    match command {
        Commands::Discover {
            image,
            repo,
            version,
        } => handle_discover(&image, repo.as_deref(), version.as_deref()).await,

        Commands::Verify { path } => handle_verify(&path),

        Commands::Generate { image_dir } => {
            crate::generate::cmd_generate(&image_dir)?;
            Ok(())
        }

        Commands::Drift { image_dir } => {
            crate::drift::cmd_drift(&image_dir)?;
            Ok(())
        }

        Commands::Diff {
            image_dir,
            generated,
        } => handle_diff(&image_dir, generated),

        Commands::Sign { image_dir } => {
            crate::sign::cmd_sign(&image_dir)?;
            Ok(())
        }

        Commands::Snapshot { image_dir } => {
            crate::snapshot::cmd_snapshot(&image_dir)?;
            Ok(())
        }

        Commands::Audit { path, format } => handle_audit(&path, &format),

        Commands::Migrate { path, dry_run } => {
            let images_dir = Path::new(&path);
            let migrated = crate::migrate::migrate_all(images_dir, dry_run)?;
            println!("Migrated {} images", migrated.len());
            Ok(())
        }

        Commands::Validate { path } => handle_validate(&path),

        Commands::VerifyAll { path } => {
            let exit_code = crate::verify_all::cmd_verify_all(&path)?;
            if exit_code != 0 {
                std::process::exit(exit_code);
            }
            Ok(())
        }

        Commands::Outdated { path, all } => {
            crate::outdated::cmd_outdated(&path, all).await?;
            Ok(())
        }

        Commands::Bump {
            image,
            new_version,
            dry_run,
        } => {
            crate::bump::cmd_bump(&image, &new_version, dry_run)?;
            Ok(())
        }

        Commands::PinDigests { path, dry_run } => {
            crate::pin_digests::cmd_pin_digests(&path, dry_run)?;
            Ok(())
        }

        Commands::CiDiff { base } => {
            crate::ci_diff::cmd_ci_diff(&base)?;
            Ok(())
        }

        Commands::Report { format, images_dir } => handle_report(&format, &images_dir),

        Commands::Deprecated {
            list,
            mark,
            unmark,
            images_dir,
        } => handle_deprecated(list, mark.as_deref(), unmark.as_deref(), &images_dir),

        Commands::Changelog {
            images_dir,
            since,
            limit,
        } => {
            crate::changelog::cmd_changelog(&images_dir, since, limit)?;
            Ok(())
        }

        Commands::ValidateStrict { images_dir } => {
            crate::validate_strict::cmd_validate_strict(&images_dir)?;
            Ok(())
        }

        Commands::ValidateParallel { images_dir, format } => {
            handle_validate_parallel(&images_dir, &format)
        }

        Commands::AutoVersion {
            images_dir,
            dry_run,
            allow_major,
            format,
        } => handle_auto_version(&images_dir, dry_run, allow_major, &format).await,

        Commands::Index {
            images_dir,
            db_path,
        } => {
            let db_path = Path::new(&db_path);
            let conn = crate::registry_index::open_index(db_path)?;
            let count = crate::registry_index::build_index(&conn, Path::new(&images_dir))?;
            println!("Indexed {} images into {}", count, db_path.display());
            Ok(())
        }

        Commands::IndexUpdate {
            images_dir,
            db_path,
        } => {
            let db_path = Path::new(&db_path);
            let conn = crate::registry_index::open_index(db_path)?;
            let (added, updated, unchanged) =
                crate::registry_index::update_index_incremental(&conn, Path::new(&images_dir))?;
            println!(
                "Incremental update: {} added, {} updated, {} unchanged",
                added, updated, unchanged
            );
            Ok(())
        }

        Commands::IndexStats { db_path, format } => handle_index_stats(&db_path, &format),

        Commands::IndexQuery {
            db_path,
            tier,
            source_type,
            format,
        } => handle_index_query(&db_path, tier, source_type.as_deref(), &format),

        Commands::Dashboard { db_path, output } => {
            let db_path = Path::new(&db_path);
            let conn = crate::registry_index::open_index(db_path)?;
            let data = crate::dashboard::collect_dashboard_data(&conn)?;
            let html = crate::dashboard::generate_dashboard_html(&data);
            std::fs::write(&output, &html)?;
            println!("Dashboard generated: {}", output);
            println!(
                "Open in browser: file://{}",
                std::fs::canonicalize(&output)?.display()
            );
            Ok(())
        }

        Commands::Completion { shell } => {
            let mut cmd = Cli::command();
            clap_complete::generate(shell, &mut cmd, "evergreenctl", &mut std::io::stdout());
            Ok(())
        }
    }
}

// ---------------------------------------------------------------------------
// Individual command handlers (extracted from match arms)
// ---------------------------------------------------------------------------

async fn handle_discover(
    image: &str,
    repo: Option<&str>,
    version: Option<&str>,
) -> anyhow::Result<()> {
    let client = reqwest::Client::builder()
        .user_agent(crate::USER_AGENT)
        .build()?;

    if let Some(repo_str) = repo {
        let parts: Vec<&str> = repo_str.split('/').collect();
        if parts.len() == 2 {
            let sources = crate::discover::discover_github_release(
                &client, parts[0], parts[1], version, None,
            )
            .await?;

            if sources.is_empty() {
                println!("No release assets found for {}/{}", parts[0], parts[1]);
            } else {
                println!("Found {} assets for {}:", sources.len(), repo_str);
                for s in &sources {
                    println!("  URL: {}", s.url);
                    println!("  Version: {}", s.version);
                    if let Some(size) = s.size_bytes {
                        println!("  Size: {} bytes", size);
                    }
                }
            }
        } else {
            anyhow::bail!("Invalid repo format, expected owner/repo");
        }
    } else {
        let dockerfile = Path::new("images").join(image).join("Dockerfile");
        if dockerfile.exists() {
            if let Ok(manifest) = crate::migrate::dockerfile_to_manifest(&dockerfile, image) {
                println!("Extracted manifest for {}:", image);
                println!("  Version: {}", manifest.metadata.version);
                println!("  Source: {}", manifest.metadata.source);
                println!("  Base: {}", manifest.build.base);
                println!("  Entrypoint: {:?}", manifest.runtime.entrypoint);

                let probe = crate::discover::probe_url(&client, &manifest.source.url).await?;
                println!("  URL accessible: {}", probe.accessible);
                if let Some(len) = probe.content_length {
                    println!("  Content-Length: {} bytes", len);
                }
            }
        } else {
            anyhow::bail!("Dockerfile not found at {}", dockerfile.display());
        }
    }
    Ok(())
}

fn handle_diff(image_dir: &str, show_generated: bool) -> anyhow::Result<()> {
    let dir = Path::new(image_dir);
    let manifest_path = dir.join("manifest.toml");
    let dockerfile_path = dir.join("Dockerfile");

    if !manifest_path.exists() {
        anyhow::bail!("No manifest.toml found at {}", manifest_path.display());
    }

    let manifest = crate::manifest::Manifest::from_file(&manifest_path)?;
    let gen = crate::generate::DockerfileGenerator::new(manifest.clone());
    let generated = gen.generate()?;

    if show_generated || !dockerfile_path.exists() {
        // Just show the generated Dockerfile
        println!("Generated Dockerfile for {}:", manifest.name());
        println!("---");
        println!("{}", generated);
        return Ok(());
    }

    // Show diff between generated and actual
    let actual = std::fs::read_to_string(&dockerfile_path)?;

    let name = manifest.name();
    println!("Diff: {} (generated vs actual)", name);
    println!("=== Generated (from manifest.toml) ===");
    println!("---");

    // Simple line-by-line diff
    let gen_lines: Vec<&str> = generated.lines().collect();
    let act_lines: Vec<&str> = actual.lines().collect();

    let mut diffs = 0;
    let max_lines = gen_lines.len().max(act_lines.len());

    for i in 0..max_lines {
        let gen_line = gen_lines.get(i).unwrap_or(&"");
        let act_line = act_lines.get(i).unwrap_or(&"");

        if gen_line != act_line {
            diffs += 1;
            if gen_line.is_empty() {
                println!("- {}", act_line);
            } else if act_line.is_empty() {
                println!("+ {}", gen_line);
            } else {
                println!("- {}", act_line);
                println!("+ {}", gen_line);
            }
        }
    }

    println!("---");
    if diffs == 0 {
        println!("No differences found.");
    } else {
        println!("{} line(s) differ.", diffs);
    }

    Ok(())
}

fn handle_verify(path: &str) -> anyhow::Result<()> {
    let path = Path::new(path);
    if path.is_file() {
        let manifest = crate::manifest::Manifest::from_file(path)?;
        println!("Manifest: {}", path.display());
        println!("  Name: {}", manifest.name());
        println!("  Version: {}", manifest.version());
        println!("  Source URL: {}", manifest.source_url());
        println!("  GitHub Repo: {:?}", manifest.github_repo());
        if manifest.source_url().is_empty() {
            println!("  WARNING: No source URL configured");
        }
    } else if path.is_dir() {
        let mut verified = 0;
        let mut missing = 0;
        for entry in std::fs::read_dir(path)? {
            let entry = entry?;
            let manifest_path = entry.path().join("manifest.toml");
            if manifest_path.exists() {
                match crate::manifest::Manifest::from_file(&manifest_path) {
                    Ok(m) => {
                        if m.source_url().is_empty() {
                            println!("MISSING: {} (no source URL)", m.name());
                            missing += 1;
                        } else {
                            verified += 1;
                        }
                    }
                    Err(e) => {
                        println!("ERROR: {} - {}", manifest_path.display(), e);
                    }
                }
            }
        }
        println!("\nVerified: {}, Missing source URL: {}", verified, missing);
    }
    Ok(())
}

fn handle_audit(path: &str, format: &str) -> anyhow::Result<()> {
    let images_dir = Path::new(path);
    let results = crate::audit::audit_all(images_dir)?;

    match format {
        "json" => {
            println!("{}", serde_json::to_string_pretty(&results)?);
        }
        "tsv" => {
            println!("name\tstatus\tissues");
            for r in &results {
                println!("{}\t{:?}\t{}", r.name, r.status, r.issues.len());
            }
        }
        _ => {
            for r in &results {
                match r.status {
                    crate::audit::ImageStatus::Real => {
                        if r.issues.is_empty() {
                            println!("  ✓ {}", r.name);
                        } else {
                            println!("  ~ {} ({} warnings)", r.name, r.issues.len());
                            for issue in &r.issues {
                                println!(
                                    "    - [{}] {} (line {:?})",
                                    issue.severity, issue.code, issue.line
                                );
                            }
                        }
                    }
                    crate::audit::ImageStatus::Placeholder => {
                        println!("  ⚠ {} (placeholder)", r.name);
                    }
                    crate::audit::ImageStatus::Stub => {
                        println!("  ✗ {} (stub)", r.name);
                    }
                    crate::audit::ImageStatus::Error => {
                        println!("  ✗ {} (error)", r.name);
                        for issue in &r.issues {
                            println!(
                                "    - [{}] {} (line {:?})",
                                issue.severity, issue.code, issue.line
                            );
                        }
                    }
                }
            }
            println!("\n{}", crate::audit::audit_summary(&results));
        }
    }
    Ok(())
}

fn handle_validate(path: &str) -> anyhow::Result<()> {
    let images_dir = Path::new(path);
    let mut valid = 0;
    let mut invalid = 0;
    let mut missing = 0;

    for entry in std::fs::read_dir(images_dir)? {
        let entry = entry?;
        let manifest_path = entry.path().join("manifest.toml");

        if !manifest_path.exists() {
            missing += 1;
            continue;
        }

        match crate::manifest::Manifest::from_file(&manifest_path) {
            Ok(m) => {
                let name_ok = !m.name().is_empty();
                let version_ok = !m.version().is_empty();
                let source_ok = !m.source_url().is_empty();
                let base_ok = !m.base_image().is_empty();

                if name_ok && version_ok && source_ok && base_ok {
                    valid += 1;
                } else {
                    let issues = vec![
                        (!name_ok).then_some("name"),
                        (!version_ok).then_some("version"),
                        (!source_ok).then_some("source_url"),
                        (!base_ok).then_some("base"),
                    ]
                    .into_iter()
                    .flatten()
                    .collect::<Vec<_>>()
                    .join(", ");
                    println!("INVALID: {} - missing: {}", m.name(), issues);
                    invalid += 1;
                }
            }
            Err(e) => {
                println!("PARSE ERROR: {} - {}", manifest_path.display(), e);
                invalid += 1;
            }
        }
    }

    println!(
        "\nValidation complete: {} valid, {} invalid, {} missing manifests",
        valid, invalid, missing
    );
    Ok(())
}

fn handle_report(format: &str, images_dir: &str) -> anyhow::Result<()> {
    let images_dir = Path::new(images_dir);
    let report = crate::report::generate_report(images_dir)?;

    match format {
        "json" => {
            println!("{}", serde_json::to_string_pretty(&report)?);
        }
        _ => {
            println!("{}", crate::report::format_text(&report));
        }
    }
    Ok(())
}

fn handle_deprecated(
    list: bool,
    mark: Option<&str>,
    unmark: Option<&str>,
    images_dir: &str,
) -> anyhow::Result<()> {
    let images_dir = Path::new(images_dir);

    if list {
        let deprecated = crate::deprecated::list_deprecated(images_dir)?;
        if deprecated.is_empty() {
            println!("No deprecated images found.");
        } else {
            println!("Deprecated images ({}):", deprecated.len());
            for img in &deprecated {
                println!("  {}", img.name);
            }
        }
    } else if let Some(image) = mark {
        crate::deprecated::mark_deprecated(images_dir, image)?;
    } else if let Some(image) = unmark {
        crate::deprecated::unmark_deprecated(images_dir, image)?;
    } else {
        anyhow::bail!("No operation specified. Use --list, --mark <image>, or --unmark <image>");
    }
    Ok(())
}

fn handle_validate_parallel(images_dir: &str, format: &str) -> anyhow::Result<()> {
    let report = crate::validate_parallel::validate_all_parallel(images_dir)?;
    match format {
        "json" => {
            println!("{}", serde_json::to_string_pretty(&report)?);
        }
        _ => {
            println!("{}", crate::validate_parallel::format_report_text(&report));
        }
    }
    if report.images_failed > 0 {
        anyhow::bail!(
            "{} images failed validation ({} violations)",
            report.images_failed,
            report.total_violations
        );
    }
    Ok(())
}

async fn handle_auto_version(
    images_dir: &str,
    dry_run: bool,
    allow_major: bool,
    format: &str,
) -> anyhow::Result<()> {
    let report = crate::auto_version::run_auto_version(images_dir, dry_run, allow_major).await?;
    match format {
        "json" => {
            println!("{}", serde_json::to_string_pretty(&report)?);
        }
        _ => {
            println!("{}", crate::auto_version::format_report_text(&report));
        }
    }
    if report.images_failed > 0 {
        anyhow::bail!("{} images failed auto-version check", report.images_failed);
    }
    Ok(())
}

fn handle_index_stats(db_path: &str, format: &str) -> anyhow::Result<()> {
    let db_path = Path::new(db_path);
    let conn = crate::registry_index::open_index(db_path)?;
    let stats = crate::registry_index::get_stats(&conn)?;
    match format {
        "json" => {
            println!("{}", serde_json::to_string_pretty(&stats)?);
        }
        _ => {
            println!("{}", crate::registry_index::format_stats_text(&stats));
        }
    }
    Ok(())
}

fn handle_index_query(
    db_path: &str,
    tier: Option<u8>,
    source_type: Option<&str>,
    format: &str,
) -> anyhow::Result<()> {
    let db_path = Path::new(db_path);
    let conn = crate::registry_index::open_index(db_path)?;

    if let Some(t) = tier {
        let records = crate::registry_index::query_by_tier(&conn, t)?;
        match format {
            "json" => {
                println!("{}", serde_json::to_string_pretty(&records)?);
            }
            _ => {
                println!("Tier {} images ({}):", t, records.len());
                for r in &records {
                    let status = r.build_status.as_deref().unwrap_or("unknown");
                    println!(
                        "  {:<30} {:<15} {:<20} {}",
                        r.name, r.version, r.source_type, status
                    );
                }
            }
        }
    } else if let Some(st) = source_type {
        let mut stmt = conn.prepare(
            "SELECT name, version, tier, source_type, build_status
             FROM images WHERE source_type = ?1 ORDER BY name",
        )?;
        let records: Vec<(String, String, i32, String, Option<String>)> = stmt
            .query_map(params![st], |row| {
                Ok((
                    row.get(0)?,
                    row.get(1)?,
                    row.get(2)?,
                    row.get(3)?,
                    row.get(4)?,
                ))
            })?
            .collect::<Result<Vec<_>, _>>()?;
        match format {
            "json" => {
                println!("{}", serde_json::to_string_pretty(&records)?);
            }
            _ => {
                println!("Source type '{}' images ({}):", st, records.len());
                for (name, ver, tier, _, status) in &records {
                    let s = status.as_deref().unwrap_or("unknown");
                    println!("  {:<30} {:<15} tier{} {}", name, ver, tier, s);
                }
            }
        }
    } else {
        anyhow::bail!("Specify --tier or --source-type to filter");
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::cli::Commands;

    #[tokio::test]
    async fn test_execute_ci_diff_no_crash() {
        // CiDiff delegates to ci_diff module — just verify it doesn't panic
        let result = execute(Commands::CiDiff {
            base: "HEAD~1".into(),
        })
        .await;
        // May fail (no git history in test env) but shouldn't panic
        let _ = result;
    }

    #[tokio::test]
    async fn test_execute_generate_invalid_dir() {
        let result = execute(Commands::Generate {
            image_dir: "/nonexistent/path".into(),
        })
        .await;
        assert!(result.is_err());
    }

    #[tokio::test]
    async fn test_execute_drift_invalid_dir() {
        let result = execute(Commands::Drift {
            image_dir: "/nonexistent/path".into(),
        })
        .await;
        assert!(result.is_err());
    }

    #[tokio::test]
    async fn test_execute_sign_invalid_dir() {
        let result = execute(Commands::Sign {
            image_dir: "/nonexistent/path".into(),
        })
        .await;
        assert!(result.is_err());
    }

    #[tokio::test]
    async fn test_execute_snapshot_invalid_dir() {
        let result = execute(Commands::Snapshot {
            image_dir: "/nonexistent/path".into(),
        })
        .await;
        assert!(result.is_err());
    }

    #[tokio::test]
    async fn test_execute_validate_invalid_dir() {
        let result = execute(Commands::Validate {
            path: "/nonexistent/path".into(),
        })
        .await;
        assert!(result.is_err());
    }

    #[tokio::test]
    async fn test_execute_index_invalid_dir() {
        let result = execute(Commands::Index {
            images_dir: "/nonexistent/path".into(),
            db_path: ":memory:".into(),
        })
        .await;
        assert!(result.is_err());
    }

    #[tokio::test]
    async fn test_execute_deprecated_no_operation() {
        let result = execute(Commands::Deprecated {
            list: false,
            mark: None,
            unmark: None,
            images_dir: "images".into(),
        })
        .await;
        assert!(result.is_err());
        assert!(result
            .unwrap_err()
            .to_string()
            .contains("No operation specified"));
    }

    #[tokio::test]
    async fn test_execute_index_query_no_filter() {
        let result = execute(Commands::IndexQuery {
            db_path: ":memory:".into(),
            tier: None,
            source_type: None,
            format: "text".into(),
        })
        .await;
        assert!(result.is_err());
        assert!(result
            .unwrap_err()
            .to_string()
            .contains("Specify --tier or --source-type"));
    }
}
