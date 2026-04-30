use std::path::Path;
use std::time::Duration;
use anyhow::{Result, Context};
use serde::Deserialize;

pub async fn cmd_outdated(images_dir: &str, check_all: bool) -> Result<()> {
    let dir = Path::new(images_dir);
    if !dir.exists() {
        anyhow::bail!("Images directory not found: {}", images_dir);
    }

    let client = reqwest::Client::builder()
        .user_agent("sovereignctl/1.0.0")
        .build()?;

    println!("Checked: {}", chrono::Local::now().format("%Y-%m-%d %H:%M:%S UTC%:z"));
    println!();

    let mut entries: Vec<OutdatedEntry> = Vec::new();
    let mut has_github = false;

    for entry in std::fs::read_dir(dir)? {
        let entry = entry?;
        let path = entry.path();
        if !path.is_dir() {
            continue;
        }

        let name = path.file_name().unwrap_or_default().to_string_lossy().to_string();
        let manifest_path = path.join("manifest.toml");

        if !manifest_path.exists() && !check_all {
            continue;
        }

        if !manifest_path.exists() {
            entries.push(OutdatedEntry {
                name,
                current: "-".to_string(),
                latest: "-".to_string(),
                status: "NO-MANIFEST".to_string(),
            });
            continue;
        }

        let manifest = match crate::manifest::Manifest::from_file(&manifest_path) {
            Ok(m) => m,
            Err(_) => {
                entries.push(OutdatedEntry {
                    name,
                    current: "-".to_string(),
                    latest: "-".to_string(),
                    status: "PARSE-ERROR".to_string(),
                });
                continue;
            }
        };

        let github_repo = manifest.source.github_repo.clone();

        if let Some(repo) = &github_repo {
            has_github = true;
            let current = manifest.image.version.clone();

            let latest = match query_latest_release(&client, repo).await {
                Ok(tag) => tag,
                Err(e) => {
                    entries.push(OutdatedEntry {
                        name,
                        current,
                        latest: format!("ERROR: {}", e),
                        status: "ERROR".to_string(),
                    });
                    tokio::time::sleep(Duration::from_secs(1)).await;
                    continue;
                }
            };

            tokio::time::sleep(Duration::from_secs(1)).await;

            let status = compare_versions(&current, &latest);
            entries.push(OutdatedEntry {
                name,
                current,
                latest,
                status,
            });
        } else if check_all {
            entries.push(OutdatedEntry {
                name,
                current: manifest.image.version,
                latest: "-".to_string(),
                status: "NO-GITHUB".to_string(),
            });
        }
    }

    println!("{:<30} {:<15} {:<15} {:<12}", "IMAGE", "CURRENT", "LATEST", "STATUS");
    println!("{}", "-".repeat(72));

    for e in &entries {
        println!("{:<30} {:<15} {:<15} {:<12}", e.name, e.current, e.latest, e.status);
    }

    let total = entries.len();
    let ok = entries.iter().filter(|e| e.status == "OK").count();
    let outdated = entries.iter().filter(|e| e.status == "OUTDATED").count();
    let errors = entries.iter().filter(|e| e.status == "ERROR").count();

    println!("\nSummary: {} images checked, {} up-to-date, {} outdated, {} errors",
        total, ok, outdated, errors);

    if !has_github && !check_all {
        println!("Hint: use --all to check images without GitHub repos");
    }

    Ok(())
}

struct OutdatedEntry {
    name: String,
    current: String,
    latest: String,
    status: String,
}

#[derive(Deserialize)]
struct GithubRelease {
    tag_name: String,
}

async fn query_latest_release(client: &reqwest::Client, repo: &str) -> Result<String> {
    let url = format!("https://api.github.com/repos/{}/releases/latest", repo);
    let resp = client
        .get(&url)
        .header("Accept", "application/vnd.github+json")
        .send()
        .await
        .context("Failed to query GitHub API")?;

    if !resp.status().is_success() {
        anyhow::bail!("GitHub API returned {}", resp.status());
    }

    let release: GithubRelease = resp.json().await?;
    Ok(release.tag_name.trim_start_matches('v').to_string())
}

fn compare_versions(current: &str, latest: &str) -> String {
    let c = semver::Version::parse(current);
    let l = semver::Version::parse(latest);

    match (c, l) {
        (Ok(cv), Ok(lv)) => {
            if cv >= lv {
                "OK".to_string()
            } else {
                "OUTDATED".to_string()
            }
        }
        _ => {
            if current == latest {
                "OK".to_string()
            } else {
                "OUTDATED".to_string()
            }
        }
    }
}
