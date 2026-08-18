use clap::{CommandFactory, Parser, Subcommand};
use rusqlite::params;
use std::path::{Path, PathBuf};

/// Validate a path argument to prevent path traversal attacks.
/// Returns the canonicalized absolute path, or an error if the path is invalid
/// or attempts to escape the allowed directory boundaries.
fn validate_path(path: &str, allowed_root: Option<&Path>) -> anyhow::Result<PathBuf> {
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

#[derive(Parser)]
#[command(name = "evergreenctl")]
#[command(about = "Evergreen image registry management toolchain")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
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
    /// Build/rebuild SQLite registry index
    Index {
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

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt::init();

    let cli = Cli::parse();

    // Validate all path arguments for traversal attacks
    // This applies to every subcommand that accepts a path
    match &cli.command {
        Commands::Discover { image, .. } => {
            validate_path(image, None)?;
        }
        Commands::Verify { path } => {
            validate_path(path, None)?;
        }
        Commands::Generate { image_dir } => {
            validate_path(image_dir, None)?;
        }
        Commands::Drift { image_dir } => {
            validate_path(image_dir, None)?;
        }
        Commands::Sign { image_dir } => {
            validate_path(image_dir, None)?;
        }
        Commands::Snapshot { image_dir } => {
            validate_path(image_dir, None)?;
        }
        Commands::Audit { path, .. } => {
            validate_path(path, None)?;
        }
        Commands::Migrate { path, .. } => {
            validate_path(path, None)?;
        }
        Commands::Validate { path } => {
            validate_path(path, None)?;
        }
        Commands::VerifyAll { path } => {
            validate_path(path, None)?;
        }
        Commands::Outdated { path, .. } => {
            validate_path(path, None)?;
        }
        Commands::Bump { image, .. } => {
            // Bump uses image name (not a full path), validate it's a simple name
            if image.contains('/') || image.contains("..") || image.starts_with('.') {
                anyhow::bail!(
                    "Invalid image name '{}': must be a simple name without path separators",
                    image
                );
            }
        }
        Commands::PinDigests { path, .. } => {
            validate_path(path, None)?;
        }
        Commands::Deprecated { images_dir, .. } => {
            validate_path(images_dir, None)?;
        }
        Commands::Changelog { images_dir, .. } => {
            validate_path(images_dir, None)?;
        }
        Commands::ValidateStrict { images_dir } => {
            validate_path(images_dir, None)?;
        }
        Commands::ValidateParallel { images_dir, .. } => {
            validate_path(images_dir, None)?;
        }
        Commands::AutoVersion { images_dir, .. } => {
            validate_path(images_dir, None)?;
        }
        Commands::Index { images_dir, .. } => {
            validate_path(images_dir, None)?;
        }
        _ => {} // CiDiff, Report, Completion, IndexStats, IndexQuery don't take user path args
    }

    match cli.command {
        Commands::Discover {
            image,
            repo,
            version,
        } => {
            let client = reqwest::Client::builder()
                .user_agent(evergreenctl::USER_AGENT)
                .build()?;

            if let Some(repo_str) = repo {
                let parts: Vec<&str> = repo_str.split('/').collect();
                if parts.len() == 2 {
                    let sources = evergreenctl::discover::discover_github_release(
                        &client,
                        parts[0],
                        parts[1],
                        version.as_deref(),
                        None,
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
                // Try to discover from existing Dockerfile
                let dockerfile = Path::new("images").join(&image).join("Dockerfile");
                if dockerfile.exists() {
                    if let Ok(manifest) =
                        evergreenctl::migrate::dockerfile_to_manifest(&dockerfile, &image)
                    {
                        println!("Extracted manifest for {}:", image);
                        println!("  Version: {}", manifest.metadata.version);
                        println!("  Source: {}", manifest.metadata.source);
                        println!("  Base: {}", manifest.build.base);
                        println!("  Entrypoint: {:?}", manifest.runtime.entrypoint);

                        // Probe the URL
                        let probe =
                            evergreenctl::discover::probe_url(&client, &manifest.source.url)
                                .await?;
                        println!("  URL accessible: {}", probe.accessible);
                        if let Some(len) = probe.content_length {
                            println!("  Content-Length: {} bytes", len);
                        }
                    }
                } else {
                    anyhow::bail!("Dockerfile not found at {}", dockerfile.display());
                }
            }
        }

        Commands::Verify { path } => {
            let path = Path::new(&path);
            if path.is_file() {
                let manifest = evergreenctl::manifest::Manifest::from_file(path)?;
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
                        match evergreenctl::manifest::Manifest::from_file(&manifest_path) {
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
        }

        Commands::Generate { image_dir } => {
            evergreenctl::generate::cmd_generate(&image_dir)?;
        }

        Commands::Drift { image_dir } => {
            evergreenctl::drift::cmd_drift(&image_dir)?;
        }

        Commands::Sign { image_dir } => {
            evergreenctl::sign::cmd_sign(&image_dir)?;
        }

        Commands::Snapshot { image_dir } => {
            evergreenctl::snapshot::cmd_snapshot(&image_dir)?;
        }

        Commands::Audit { path, format } => {
            let images_dir = Path::new(&path);
            let results = evergreenctl::audit::audit_all(images_dir)?;

            match format.as_str() {
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
                            evergreenctl::audit::ImageStatus::Real => {
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
                            evergreenctl::audit::ImageStatus::Placeholder => {
                                println!("  ⚠ {} (placeholder)", r.name);
                            }
                            evergreenctl::audit::ImageStatus::Stub => {
                                println!("  ✗ {} (stub)", r.name);
                            }
                            evergreenctl::audit::ImageStatus::Error => {
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
                    println!("\n{}", evergreenctl::audit::audit_summary(&results));
                }
            }
        }

        Commands::Migrate { path, dry_run } => {
            let images_dir = Path::new(&path);
            let migrated = evergreenctl::migrate::migrate_all(images_dir, dry_run)?;
            println!("Migrated {} images", migrated.len());
        }

        Commands::Validate { path } => {
            let images_dir = Path::new(&path);
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

                match evergreenctl::manifest::Manifest::from_file(&manifest_path) {
                    Ok(m) => {
                        // Validate that essential fields are populated
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
        }

        Commands::VerifyAll { path } => {
            let exit_code = evergreenctl::verify_all::cmd_verify_all(&path)?;
            if exit_code != 0 {
                std::process::exit(exit_code);
            }
        }

        Commands::Outdated { path, all } => {
            evergreenctl::outdated::cmd_outdated(&path, all).await?;
        }

        Commands::Bump {
            image,
            new_version,
            dry_run,
        } => {
            evergreenctl::bump::cmd_bump(&image, &new_version, dry_run)?;
        }

        Commands::PinDigests { path, dry_run } => {
            evergreenctl::pin_digests::cmd_pin_digests(&path, dry_run)?;
        }

        Commands::CiDiff { base } => {
            evergreenctl::ci_diff::cmd_ci_diff(&base)?;
        }

        Commands::Report { format, images_dir } => {
            let images_dir = Path::new(&images_dir);
            let report = evergreenctl::report::generate_report(images_dir)?;

            match format.as_str() {
                "json" => {
                    println!("{}", serde_json::to_string_pretty(&report)?);
                }
                _ => {
                    println!("{}", evergreenctl::report::format_text(&report));
                }
            }
        }

        Commands::Deprecated {
            list,
            mark,
            unmark,
            images_dir,
        } => {
            let images_dir = Path::new(&images_dir);

            if list {
                let deprecated = evergreenctl::deprecated::list_deprecated(images_dir)?;
                if deprecated.is_empty() {
                    println!("No deprecated images found.");
                } else {
                    println!("Deprecated images ({}):", deprecated.len());
                    for img in &deprecated {
                        println!("  {}", img.name);
                    }
                }
            } else if let Some(image) = mark {
                evergreenctl::deprecated::mark_deprecated(images_dir, &image)?;
            } else if let Some(image) = unmark {
                evergreenctl::deprecated::unmark_deprecated(images_dir, &image)?;
            } else {
                anyhow::bail!(
                    "No operation specified. Use --list, --mark <image>, or --unmark <image>"
                );
            }
        }

        Commands::Changelog {
            images_dir,
            since,
            limit,
        } => {
            evergreenctl::changelog::cmd_changelog(&images_dir, since, limit)?;
        }

        Commands::ValidateStrict { images_dir } => {
            evergreenctl::validate_strict::cmd_validate_strict(&images_dir)?;
        }

        Commands::ValidateParallel { images_dir, format } => {
            let report = evergreenctl::validate_parallel::validate_all_parallel(&images_dir)?;
            match format.as_str() {
                "json" => {
                    println!("{}", serde_json::to_string_pretty(&report)?);
                }
                _ => {
                    println!("{}", evergreenctl::validate_parallel::format_report_text(&report));
                }
            }
            if report.images_failed > 0 {
                anyhow::bail!(
                    "{} images failed validation ({} violations)",
                    report.images_failed, report.total_violations
                );
            }
        }

        Commands::AutoVersion { images_dir, dry_run, allow_major, format } => {
            let report = evergreenctl::auto_version::run_auto_version(
                &images_dir, dry_run, allow_major
            ).await?;
            match format.as_str() {
                "json" => {
                    println!("{}", serde_json::to_string_pretty(&report)?);
                }
                _ => {
                    println!("{}", evergreenctl::auto_version::format_report_text(&report));
                }
            }
            if report.images_failed > 0 {
                anyhow::bail!(
                    "{} images failed auto-version check",
                    report.images_failed
                );
            }
        }

        Commands::Index { images_dir, db_path } => {
            let db_path = Path::new(&db_path);
            let conn = evergreenctl::registry_index::open_index(db_path)?;
            let count = evergreenctl::registry_index::build_index(&conn, Path::new(&images_dir))?;
            println!("Indexed {} images into {}", count, db_path.display());
        }

        Commands::IndexStats { db_path, format } => {
            let db_path = Path::new(&db_path);
            let conn = evergreenctl::registry_index::open_index(db_path)?;
            let stats = evergreenctl::registry_index::get_stats(&conn)?;
            match format.as_str() {
                "json" => {
                    println!("{}", serde_json::to_string_pretty(&stats)?);
                }
                _ => {
                    println!("{}", evergreenctl::registry_index::format_stats_text(&stats));
                }
            }
        }

        Commands::IndexQuery { db_path, tier, source_type, format } => {
            let db_path = Path::new(&db_path);
            let conn = evergreenctl::registry_index::open_index(db_path)?;

            if let Some(t) = tier {
                let records = evergreenctl::registry_index::query_by_tier(&conn, t)?;
                match format.as_str() {
                    "json" => {
                        println!("{}", serde_json::to_string_pretty(&records)?);
                    }
                    _ => {
                        println!("Tier {} images ({}):", t, records.len());
                        for r in &records {
                            let status = r.build_status.as_deref().unwrap_or("unknown");
                            println!("  {:<30} {:<15} {:<20} {}", r.name, r.version, r.source_type, status);
                        }
                    }
                }
            } else if let Some(st) = source_type {
                let mut stmt = conn.prepare(
                    "SELECT name, version, tier, source_type, build_status
                     FROM images WHERE source_type = ?1 ORDER BY name"
                )?;
                let records: Vec<(String, String, i32, String, Option<String>)> = stmt
                    .query_map(params![st], |row| {
                        Ok((row.get(0)?, row.get(1)?, row.get(2)?, row.get(3)?, row.get(4)?))
                    })?
                    .collect::<Result<Vec<_>, _>>()?;
                match format.as_str() {
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
        }

        Commands::Completion { shell } => {
            let mut cmd = Cli::command();
            clap_complete::generate(shell, &mut cmd, "evergreenctl", &mut std::io::stdout());
        }
    }

    Ok(())
}
