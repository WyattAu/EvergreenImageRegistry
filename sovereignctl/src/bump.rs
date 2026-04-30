use std::path::Path;
use std::process::Command;
use anyhow::{Result, Context};
use crate::manifest::Manifest;
use crate::generate::DockerfileGenerator;

pub fn cmd_bump(image: &str, new_version: &str, dry_run: bool) -> Result<()> {
    let image_dir = Path::new("images").join(image);
    let manifest_path = image_dir.join("manifest.toml");
    let dockerfile_path = image_dir.join("Dockerfile");

    if !manifest_path.exists() {
        anyhow::bail!("Manifest not found: {}", manifest_path.display());
    }

    let mut manifest = Manifest::from_file(&manifest_path)?;
    let old_version = manifest.image.version.clone();

    println!("Image: {}", image);
    println!("  Current version: {}", old_version);
    println!("  New version:     {}", new_version);

    let old_manifest_content = std::fs::read_to_string(&manifest_path)?;
    let old_dockerfile_content = if dockerfile_path.exists() {
        Some(std::fs::read_to_string(&dockerfile_path)?)
    } else {
        None
    };

    manifest.image.version = new_version.to_string();

    if !old_version.is_empty() {
        manifest.source.url = manifest.source.url.replace(&old_version, new_version);
        for url in manifest.source.fallback_urls.iter_mut() {
            *url = url.replace(&old_version, new_version);
        }
    }

    let gen = DockerfileGenerator::new(manifest.clone());
    let new_dockerfile = gen.generate()?;

    let new_manifest_content = toml::to_string_pretty(&manifest)
        .context("Failed to serialize manifest")?;

    if dry_run {
        println!("\n--- Manifest changes ---");
        print_diff(&old_manifest_content, &new_manifest_content);

        if let Some(ref old_df) = old_dockerfile_content {
            println!("\n--- Dockerfile changes ---");
            print_diff(old_df, &new_dockerfile);
        }

        println!("\nDry run complete. No files were modified.");
        return Ok(());
    }

    std::fs::write(&manifest_path, &new_manifest_content)?;
    std::fs::write(&dockerfile_path, &new_dockerfile)?;

    println!("\n--- Manifest changes ---");
    print_diff(&old_manifest_content, &new_manifest_content);

    if let Some(ref old_df) = old_dockerfile_content {
        println!("\n--- Dockerfile changes ---");
        print_diff(old_df, &new_dockerfile);
    }

    println!("\nUpdated {} from {} to {}", image, old_version, new_version);

    Ok(())
}

fn print_diff(old: &str, new: &str) {
    let old_file = "/tmp/sovereignctl_old";
    let new_file = "/tmp/sovereignctl_new";

    let _ = std::fs::write(old_file, old);
    let _ = std::fs::write(new_file, new);

    let output = Command::new("diff")
        .arg("-u")
        .arg(old_file)
        .arg(new_file)
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
            println!("  (diff not available: {})", e);
        }
    }

    let _ = std::fs::remove_file(old_file);
    let _ = std::fs::remove_file(new_file);
}
