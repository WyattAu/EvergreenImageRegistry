use clap::{Parser, Subcommand};
use std::path::Path;

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
    /// Show changes since last CI run
    CiDiff {
        /// Base git ref to compare against
        #[arg(long, default_value = "HEAD~1")]
        base: String,
    },
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt::init();

    let cli = Cli::parse();

    match cli.command {
        Commands::Discover {
            image,
            repo,
            version,
        } => {
            let client = reqwest::Client::builder()
                .user_agent("evergreenctl/0.1.0")
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

        Commands::CiDiff { base } => {
            evergreenctl::ci_diff::cmd_ci_diff(&base)?;
        }
    }

    Ok(())
}
