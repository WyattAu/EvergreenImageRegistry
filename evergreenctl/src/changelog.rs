use anyhow::Result;
use std::path::Path;
use std::process::Command;

pub fn cmd_changelog(images_dir: &str, since_days: u64) -> Result<()> {
    let dir = Path::new(images_dir);
    if !dir.exists() {
        anyhow::bail!("Images directory not found: {}", images_dir);
    }

    let since_date = chrono::Local::now() - chrono::Duration::days(since_days as i64);
    let since_str = since_date.format("%Y-%m-%d");

    println!("# Changelog (since {})\n", since_str);
    println!("| Image | Version | Change |");
    println!("|-------|---------|--------|");

    let output = Command::new("git")
        .args([
            "log",
            &format!("--since={since_str}"),
            "--oneline",
            "--",
            &format!("{}/*/", images_dir),
        ])
        .output()?;

    let log = String::from_utf8_lossy(&output.stdout);
    let mut entries: Vec<Vec<&str>> = Vec::new();

    for line in log.lines() {
        let parts: Vec<&str> = line.splitn(3, '|').collect();
        if parts.len() >= 3 {
            entries.push(parts);
        }
    }

    for entry in entries.iter().take(50) {
        println!(
            "| {} | {} | {} |",
            entry[0].trim(),
            entry[1].trim(),
            entry[2].trim()
        );
    }

    if entries.len() > 50 {
        println!("\n... and {} more entries", entries.len() - 50);
    }

    println!("\nTotal changes: {}", entries.len());
    Ok(())
}

#[cfg(test)]
mod tests {
    #[test]
    fn test_cmd_changelog_invalid_dir() {
        let result = super::cmd_changelog("/nonexistent", 7);
        assert!(result.is_err());
    }
}
