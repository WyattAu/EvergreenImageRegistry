use clap::{Parser, Subcommand};
use std::path::Path;

#[derive(Parser)]
#[command(name = "sovereignctl")]
#[command(about = "Sovereign image registry management toolchain")]
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
    /// Generate Dockerfile from manifest
    Generate {
        /// Path to manifest file
        manifest: String,
        /// Output Dockerfile path
        #[arg(short, long)]
        output: Option<String>,
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
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt::init();

    let cli = Cli::parse();

    match cli.command {
        Commands::Discover { image, repo, version } => {
            let client = reqwest::Client::builder()
                .user_agent("sovereignctl/0.1.0")
                .build()?;

            if let Some(repo_str) = repo {
                let parts: Vec<&str> = repo_str.split('/').collect();
                if parts.len() == 2 {
                    let sources = sovereignctl::discover::discover_github_release(
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
                    if let Ok(manifest) = sovereignctl::migrate::dockerfile_to_manifest(&dockerfile, &image) {
                        println!("Extracted manifest for {}:", image);
                        println!("  Version: {}", manifest.image.version);
                        println!("  Type: {:?}", manifest.image.image_type);
                        println!("  URL: {}", manifest.source.url);
                        println!("  Base: {}", manifest.build.base.image);
                        println!("  Entrypoint: {:?}", manifest.runtime.entrypoint);

                        // Probe the URL
                        let probe = sovereignctl::discover::probe_url(&client, &manifest.source.url).await?;
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
                let manifest = sovereignctl::manifest::Manifest::from_file(path)?;
                println!("Manifest: {}", path.display());
                println!("  Name: {}", manifest.image.name);
                println!("  Version: {}", manifest.image.version);
                println!("  Checksum: {} {}", manifest.source.checksum.algorithm, manifest.source.checksum.expected);
                if manifest.source.checksum.expected.is_empty() {
                    println!("  WARNING: No checksum configured");
                }
            } else if path.is_dir() {
                let mut verified = 0;
                let mut missing = 0;
                for entry in std::fs::read_dir(path)? {
                    let entry = entry?;
                    let manifest_path = entry.path().join("manifest.toml");
                    if manifest_path.exists() {
                        match sovereignctl::manifest::Manifest::from_file(&manifest_path) {
                            Ok(m) => {
                                if m.source.checksum.expected.is_empty() {
                                    println!("MISSING: {} (no checksum)", m.image.name);
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
                println!("\nVerified: {}, Missing checksums: {}", verified, missing);
            }
        }

        Commands::Generate { manifest, output } => {
            let manifest_path = Path::new(&manifest);
            let manifest = sovereignctl::manifest::Manifest::from_file(manifest_path)?;
            let gen = sovereignctl::generate::DockerfileGenerator::new(manifest);
            let dockerfile = gen.generate()?;

            let output_path = match output {
                Some(o) => Path::new(&o).to_path_buf(),
                None => manifest_path.parent().unwrap_or(Path::new(".")).join("Dockerfile"),
            };

            std::fs::write(&output_path, &dockerfile)?;
            println!("Generated Dockerfile: {}", output_path.display());
        }

        Commands::Audit { path, format } => {
            let images_dir = Path::new(&path);
            let results = sovereignctl::audit::audit_all(images_dir)?;

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
                            sovereignctl::audit::ImageStatus::Real => {
                                if r.issues.is_empty() {
                                    println!("  ✓ {}", r.name);
                                } else {
                                    println!("  ~ {} ({} warnings)", r.name, r.issues.len());
                                    for issue in &r.issues {
                                        println!("    - [{}] {} (line {:?})", issue.severity, issue.code, issue.line);
                                    }
                                }
                            }
                            sovereignctl::audit::ImageStatus::Placeholder => {
                                println!("  ⚠ {} (placeholder)", r.name);
                            }
                            sovereignctl::audit::ImageStatus::Stub => {
                                println!("  ✗ {} (stub)", r.name);
                            }
                            sovereignctl::audit::ImageStatus::Error => {
                                println!("  ✗ {} (error)", r.name);
                                for issue in &r.issues {
                                    println!("    - [{}] {} (line {:?})", issue.severity, issue.code, issue.line);
                                }
                            }
                        }
                    }
                    println!("\n{}", sovereignctl::audit::audit_summary(&results));
                }
            }
        }

        Commands::Migrate { path, dry_run } => {
            let images_dir = Path::new(&path);
            let migrated = sovereignctl::migrate::migrate_all(images_dir, dry_run)?;
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
                let dockerfile_path = entry.path().join("Dockerfile");

                if !manifest_path.exists() {
                    missing += 1;
                    continue;
                }

                match sovereignctl::manifest::Manifest::from_file(&manifest_path) {
                    Ok(m) => {
                        // Validate the manifest
                        match m.validate() {
                            Ok(()) => {
                                valid += 1;
                            }
                            Err(e) => {
                                println!("INVALID: {} - {}", m.image.name, e);
                                invalid += 1;
                            }
                        }
                    }
                    Err(e) => {
                        println!("PARSE ERROR: {} - {}", manifest_path.display(), e);
                        invalid += 1;
                    }
                }
            }

            println!("\nValidation complete: {} valid, {} invalid, {} missing manifests", valid, invalid, missing);
        }
    }

    Ok(())
}
