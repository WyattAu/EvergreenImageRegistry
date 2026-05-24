use anyhow::Result;
use std::path::Path;
use std::process::Command;

pub fn cmd_changelog(images_dir: &str, since_days: u64, limit: usize) -> Result<()> {
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
            r#"--format=%h|%s|%an"#,
            "--",
            &format!("{}/*/", images_dir),
        ])
        .output()?;

    let log = String::from_utf8_lossy(&output.stdout);
    let mut entries: Vec<Vec<&str>> = Vec::new();

    for line in log.lines() {
        let parts: Vec<&str> = line.splitn(3, '|').collect();
        if parts.len() >= 2 {
            entries.push(parts);
        }
    }

    for entry in entries.iter().take(limit) {
        let hash = entry.first().map(|s| s.trim()).unwrap_or("");
        let subject = entry.get(1).map(|s| s.trim()).unwrap_or("");
        let author = entry.get(2).map(|s| s.trim()).unwrap_or("-");
        println!("| {hash} | {subject} | {author} |");
    }

    if entries.len() > limit {
        println!("\n... and {} more entries", entries.len() - limit);
    }

    println!("\nTotal changes: {}", entries.len());
    Ok(())
}

#[cfg(test)]
mod tests {
    #[test]
    fn test_cmd_changelog_invalid_dir() {
        let result = super::cmd_changelog("/nonexistent", 7, 50);
        assert!(result.is_err());
    }
}
