use crate::manifest::Manifest;
use anyhow::{Context, Result};
use std::path::Path;
use std::process::Command;

pub fn cmd_bump(image: &str, new_version: &str, dry_run: bool) -> Result<()> {
    let image_dir = Path::new("images").join(image);
    let manifest_path = image_dir.join("manifest.toml");
    let dockerfile_path = image_dir.join("Dockerfile");
    let checksums_path = image_dir.join("CHECKSUMS");

    if !dockerfile_path.exists() {
        anyhow::bail!("Dockerfile not found: {}", dockerfile_path.display());
    }

    let has_manifest = manifest_path.exists();
    let has_checksums = checksums_path.exists();

    let old_version = if has_manifest {
        let manifest = Manifest::from_file(&manifest_path)?;
        manifest.version().to_string()
    } else {
        extract_version_from_dockerfile(&dockerfile_path)?
    };

    println!("Image: {}", image);
    println!("  Current version: {}", old_version);
    println!("  New version:     {}", new_version);

    if has_manifest {
        bump_with_manifest(
            &manifest_path,
            &dockerfile_path,
            &old_version,
            new_version,
            dry_run,
        )?;
    } else {
        bump_dockerfile_only(&dockerfile_path, &old_version, new_version, dry_run)?;
    }

    if has_checksums {
        bump_checksums_file(&checksums_path, &old_version, new_version, dry_run)?;
    }

    println!(
        "\nUpdated {} from {} to {}",
        image, old_version, new_version
    );

    Ok(())
}

fn extract_version_from_dockerfile(dockerfile_path: &Path) -> Result<String> {
    let content = std::fs::read_to_string(dockerfile_path)?;
    for line in content.lines() {
        if let Some(version) = line.strip_prefix("ARG VERSION=") {
            let version = version.split_whitespace().next().unwrap_or(version);
            return Ok(version.to_string());
        }
    }
    anyhow::bail!("Could not find ARG VERSION in Dockerfile");
}

fn bump_with_manifest(
    manifest_path: &Path,
    dockerfile_path: &Path,
    old_version: &str,
    new_version: &str,
    dry_run: bool,
) -> Result<()> {
    let mut manifest = Manifest::from_file(manifest_path)?;

    let old_manifest_content = std::fs::read_to_string(manifest_path)?;
    let old_dockerfile_content = std::fs::read_to_string(dockerfile_path).ok();

    manifest.metadata.version = new_version.to_string();

    if !old_version.is_empty() {
        manifest.source.url = manifest.source.url.replace(old_version, new_version);
        if !manifest.metadata.source.is_empty() {
            manifest.metadata.source = manifest.metadata.source.replace(old_version, new_version);
        }
    }

    let new_manifest_content =
        toml::to_string_pretty(&manifest).context("Failed to serialize manifest")?;

    if dry_run {
        println!("\n--- Manifest changes ---");
        print_diff(&old_manifest_content, &new_manifest_content);

        if old_dockerfile_content.is_some() {
            println!("\n--- Dockerfile changes ---");
            println!("  (Dockerfile not auto-updated in dry-run; bump --dry-run only shows manifest diff)");
        }
        return Ok(());
    }

    std::fs::write(manifest_path, &new_manifest_content)?;

    println!("\n--- Manifest changes ---");
    print_diff(&old_manifest_content, &new_manifest_content);

    Ok(())
}

fn bump_dockerfile_only(
    dockerfile_path: &Path,
    old_version: &str,
    new_version: &str,
    dry_run: bool,
) -> Result<()> {
    let content = std::fs::read_to_string(dockerfile_path)?;
    let mut new_content = String::new();

    for line in content.lines() {
        if line.starts_with("ARG VERSION=") {
            new_content.push_str(&format!("ARG VERSION={}\n", new_version));
        } else if !old_version.is_empty() && line.contains(old_version) {
            let replaced = line.replace(old_version, new_version);
            new_content.push_str(&replaced);
            new_content.push('\n');
        } else {
            new_content.push_str(line);
            new_content.push('\n');
        }
    }

    if dry_run {
        println!("\n--- Dockerfile changes ---");
        print_diff(&content, &new_content);
        return Ok(());
    }

    std::fs::write(dockerfile_path, &new_content)?;

    println!("\n--- Dockerfile changes ---");
    print_diff(&content, &new_content);

    Ok(())
}

fn bump_checksums_file(
    checksums_path: &Path,
    old_version: &str,
    new_version: &str,
    dry_run: bool,
) -> Result<()> {
    let content = std::fs::read_to_string(checksums_path)?;
    let mut new_content = String::new();

    for line in content.lines() {
        if line.starts_with("version = ") || line.starts_with("last_verified = ") {
            if line.contains("version = ") {
                new_content.push_str(&format!("version = \"{}\"\n", new_version));
            } else {
                let now = chrono::Utc::now().format("%Y-%m-%dT%H:%M:%SZ").to_string();
                new_content.push_str(&format!("last_verified = \"{}\"\n", now));
            }
        } else if line.starts_with("expected_sha256 = ") {
            new_content.push_str("expected_sha256 = \"NEEDS_UPDATE\"\n");
        } else if !old_version.is_empty() && line.contains(old_version) {
            let replaced = line.replace(old_version, new_version);
            new_content.push_str(&replaced);
            new_content.push('\n');
        } else {
            new_content.push_str(line);
            new_content.push('\n');
        }
    }

    if dry_run {
        println!("\n--- CHECKSUMS changes ---");
        print_diff(&content, &new_content);
        return Ok(());
    }

    std::fs::write(checksums_path, &new_content)?;

    println!("\n--- CHECKSUMS changes ---");
    print_diff(&content, &new_content);

    Ok(())
}

fn print_diff(old: &str, new: &str) {
    let tmp_dir = std::env::temp_dir();
    let pid = std::process::id();
    let old_file = tmp_dir.join(format!("evergreenctl_old_{pid}"));
    let new_file = tmp_dir.join(format!("evergreenctl_new_{pid}"));

    let _ = std::fs::write(&old_file, old);
    let _ = std::fs::write(&new_file, new);

    let output = Command::new("diff")
        .arg("-u")
        .arg(&old_file)
        .arg(&new_file)
        .output();

    match output {
        Ok(output) => {
            if output.status.success() {
                println!("  (no changes)");
            } else {
                let diff_text = String::from_utf8_lossy(&output.stdout);
                for line in diff_text.lines() {
                    if line.starts_with("---") || line.starts_with("+++") {
                        continue;
                    }
                    if line.starts_with('-') && !line.starts_with("---") {
                        println!("  \x1b[31m{}\x1b[0m", line);
                    } else if line.starts_with('+') && !line.starts_with("+++") {
                        println!("  \x1b[32m{}\x1b[0m", line);
                    } else {
                        println!("  {}", line);
                    }
                }
            }
        }
        Err(e) => {
            // Fallback: inline diff when external tool unavailable
            for (i, (old_line, new_line)) in old.lines().zip(new.lines()).enumerate() {
                if old_line != new_line {
                    println!("  L{}: -{}", i + 1, old_line);
                    println!("       +{}", new_line);
                }
            }
            if old.lines().count() != new.lines().count() {
                println!(
                    "  (line count differs: {} vs {})",
                    old.lines().count(),
                    new.lines().count()
                );
            }
            if e.kind() != std::io::ErrorKind::NotFound {
                println!("  (diff error: {})", e);
            }
        }
    }

    let _ = std::fs::remove_file(&old_file);
    let _ = std::fs::remove_file(&new_file);
}
