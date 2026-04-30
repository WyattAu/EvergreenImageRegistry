use std::path::Path;
use std::process::Command;
use anyhow::{Result, Context};

pub fn cmd_ci_diff(base_ref: &str) -> Result<()> {
    let output = Command::new("git")
        .args(["diff", base_ref, "--name-only", "--", "images/"])
        .output()
        .context("Failed to run git diff")?;

    if !output.status.success() {
        let stderr = String::from_utf8_lossy(&output.stderr);
        anyhow::bail!("git diff failed: {}", stderr);
    }

    let changed_files: Vec<String> = String::from_utf8_lossy(&output.stdout)
        .lines()
        .filter(|l| !l.is_empty())
        .map(|l| l.to_string())
        .collect();

    if changed_files.is_empty() {
        println!("No changes detected in images/ directory since {}", base_ref);
        return Ok(());
    }

    println!("Changed files since {}:", base_ref);
    println!("{}", "-".repeat(60));

    let mut changes: Vec<ChangeEntry> = Vec::new();

    for file_path in &changed_files {
        let path = Path::new(file_path);
        let image_name = path
            .iter()
            .nth(1)
            .and_then(|s| s.to_str())
            .unwrap_or("unknown");

        let file_name = path.file_name().and_then(|s| s.to_str()).unwrap_or("");

        let diff_output = Command::new("git")
            .args(["diff", base_ref, "--", file_path])
            .output()
            .ok();

        let diff_text = diff_output
            .as_ref()
            .map(|o| String::from_utf8_lossy(&o.stdout).to_string())
            .unwrap_or_default();

        let classification = classify_change(file_name, &diff_text);

        println!("  {} ({})", file_path, classification.change_type);

        for detail in &classification.details {
            println!("    - {}", detail);
        }

        changes.push(ChangeEntry {
            file: file_path.clone(),
            image: image_name.to_string(),
            classification,
        });
    }

    println!("\nSummary");
    println!("=======");
    let version_bumps = changes
        .iter()
        .filter(|c| c.classification.change_type == "version-bump")
        .count();
    let url_fixes = changes
        .iter()
        .filter(|c| c.classification.change_type == "url-fix")
        .count();
    let checksum_updates = changes
        .iter()
        .filter(|c| c.classification.change_type == "checksum-update")
        .count();
    let structural = changes
        .iter()
        .filter(|c| c.classification.change_type == "structural-change")
        .count();
    let new_images = changes
        .iter()
        .filter(|c| c.classification.change_type == "new-image")
        .count();

    println!("Total changes: {}", changes.len());
    println!("Version bumps: {}", version_bumps);
    println!("URL fixes: {}", url_fixes);
    println!("Checksum updates: {}", checksum_updates);
    println!("Structural changes: {}", structural);
    println!("New images: {}", new_images);

    Ok(())
}

struct ChangeEntry {
    #[allow(dead_code)]
    file: String,
    #[allow(dead_code)]
    image: String,
    classification: ChangeClassification,
}

struct ChangeClassification {
    change_type: String,
    details: Vec<String>,
}

fn classify_change(_file_name: &str, diff: &str) -> ChangeClassification {
    let mut details = Vec::new();

    let is_new_file = diff.lines().any(|l| l.contains("new file"));

    if is_new_file {
        return ChangeClassification {
            change_type: "new-image".to_string(),
            details: vec!["New file added".to_string()],
        };
    }

    let added_or_removed: Vec<&str> = diff
        .lines()
        .filter(|l| {
            (l.starts_with('-') || l.starts_with('+'))
                && !l.starts_with("---")
                && !l.starts_with("+++")
        })
        .collect();

    let has_version_change = added_or_removed.iter().any(|l| l.contains("VERSION"));
    let has_url_change = added_or_removed
        .iter()
        .any(|l| l.contains("http://") || l.contains("https://"));
    let has_checksum_change = added_or_removed
        .iter()
        .any(|l| l.contains("sha256") || l.contains("sha512") || l.contains("expected"));

    let change_type = if has_version_change {
        if has_checksum_change {
            details.push("Version and checksum updated".to_string());
        } else {
            details.push("Version updated".to_string());
        }
        "version-bump"
    } else if has_checksum_change {
        details.push("Checksum updated".to_string());
        "checksum-update"
    } else if has_url_change {
        details.push("URL changed".to_string());
        "url-fix"
    } else {
        details.push("Structure or configuration changed".to_string());
        "structural-change"
    };

    ChangeClassification {
        change_type: change_type.to_string(),
        details,
    }
}
