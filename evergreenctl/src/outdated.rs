use anyhow::{Context, Result};
use std::collections::HashMap;
use std::path::Path;
use std::time::Duration;

// ── Cache types ──────────────────────────────────────────────────────────

type Cache = HashMap<String, CacheEntry>;

#[derive(serde::Serialize, serde::Deserialize)]
struct CacheEntry {
    tag: String,
    checked_at: String,
}

fn load_cache(cache_path: &Path) -> Cache {
    if cache_path.exists() {
        let data = std::fs::read_to_string(cache_path).unwrap_or_default();
        serde_json::from_str(&data).unwrap_or_default()
    } else {
        HashMap::new()
    }
}

fn save_cache(cache_path: &Path, cache: &Cache) -> Result<()> {
    if let Some(parent) = cache_path.parent() {
        std::fs::create_dir_all(parent)?;
    }
    let data = serde_json::to_string_pretty(cache)?;
    std::fs::write(cache_path, data)?;
    Ok(())
}

fn is_cache_fresh(entry: &CacheEntry) -> bool {
    if let Ok(checked_at) = chrono::DateTime::parse_from_rfc3339(&entry.checked_at) {
        let age = chrono::Utc::now().signed_duration_since(checked_at);
        age.num_hours() < 24
    } else {
        false
    }
}

// ── Main command ─────────────────────────────────────────────────────────

pub async fn cmd_outdated(images_dir: &str, check_all: bool) -> Result<()> {
    let dir = Path::new(images_dir);
    if !dir.exists() {
        anyhow::bail!("Images directory not found: {}", images_dir);
    }

    let github_token = std::env::var("GITHUB_TOKEN").ok();
    let authenticated = github_token.is_some();
    let sleep_duration = if authenticated {
        Duration::from_millis(100)
    } else {
        Duration::from_secs(1)
    };

    let mut headers = reqwest::header::HeaderMap::new();
    if let Some(token) = &github_token {
        headers.insert(
            reqwest::header::AUTHORIZATION,
            reqwest::header::HeaderValue::from_str(&format!("Bearer {}", token))
                .context("Invalid GITHUB_TOKEN value")?,
        );
    }

    let client = reqwest::Client::builder()
        .user_agent(crate::USER_AGENT)
        .default_headers(headers)
        .build()?;

    let cache_path = Path::new("target").join("outdated_cache.json");
    let mut cache: Cache = load_cache(&cache_path);

    println!(
        "Checked: {}",
        chrono::Local::now().format("%Y-%m-%d %H:%M:%S UTC%:z")
    );
    println!();

    // Count GitHub-backed images to warn about rate limits
    let mut github_count: usize = 0;
    for entry in std::fs::read_dir(dir)? {
        let entry = entry?;
        let path = entry.path();
        if !path.is_dir() {
            continue;
        }
        let manifest_path = path.join("manifest.toml");
        if manifest_path.exists() {
            if let Ok(manifest) = crate::manifest::Manifest::from_file(&manifest_path) {
                if manifest.github_repo().is_some() {
                    github_count += 1;
                }
            }
        }
    }

    if !authenticated && github_count > 60 {
        eprintln!(
            "WARNING: {} GitHub-backed images found but no GITHUB_TOKEN is set. \
             Unauthenticated requests are limited to 60/hr. \
             Set GITHUB_TOKEN env var to increase the limit to 5,000/hr.",
            github_count
        );
    }

    let mut entries: Vec<OutdatedEntry> = Vec::new();
    let mut has_github = false;

    for entry in std::fs::read_dir(dir)? {
        let entry = entry?;
        let path = entry.path();
        if !path.is_dir() {
            continue;
        }

        let name = path
            .file_name()
            .unwrap_or_default()
            .to_string_lossy()
            .to_string();
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

        let github_repo = manifest.github_repo();

        if let Some(repo) = &github_repo {
            has_github = true;
            let current = manifest.version().to_string();

            // Check cache first
            if let Some(cached) = cache.get(repo) {
                if is_cache_fresh(cached) {
                    let status = compare_versions(&current, &cached.tag);
                    entries.push(OutdatedEntry {
                        name,
                        current,
                        latest: cached.tag.clone(),
                        status,
                    });
                    continue;
                }
            }

            let latest = match query_latest_release(&client, repo, sleep_duration).await {
                Ok(tag) => {
                    cache.insert(
                        repo.clone(),
                        CacheEntry {
                            tag: tag.clone(),
                            checked_at: chrono::Utc::now().to_rfc3339(),
                        },
                    );
                    tag
                }
                Err(e) => {
                    entries.push(OutdatedEntry {
                        name,
                        current,
                        latest: format!("ERROR: {}", e),
                        status: "ERROR".to_string(),
                    });
                    tokio::time::sleep(sleep_duration).await;
                    continue;
                }
            };

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
                current: manifest.version().to_string(),
                latest: "-".to_string(),
                status: "NO-GITHUB".to_string(),
            });
        }
    }

    if let Err(e) = save_cache(&cache_path, &cache) {
        eprintln!("Warning: failed to save cache: {}", e);
    }

    println!(
        "{:<30} {:<15} {:<15} {:<12}",
        "IMAGE", "CURRENT", "LATEST", "STATUS"
    );
    println!("{}", "-".repeat(72));

    for e in &entries {
        println!(
            "{:<30} {:<15} {:<15} {:<12}",
            e.name, e.current, e.latest, e.status
        );
    }

    let total = entries.len();
    let ok = entries.iter().filter(|e| e.status == "OK").count();
    let outdated = entries.iter().filter(|e| e.status == "OUTDATED").count();
    let errors = entries.iter().filter(|e| e.status == "ERROR").count();

    println!(
        "\nSummary: {} images checked, {} up-to-date, {} outdated, {} errors",
        total, ok, outdated, errors
    );

    if !has_github && !check_all {
        println!("Hint: use --all to check images without GitHub repos");
    }

    Ok(())
}

// ── Output row ───────────────────────────────────────────────────────────

struct OutdatedEntry {
    name: String,
    current: String,
    latest: String,
    status: String,
}

// ── GitHub API ───────────────────────────────────────────────────────────

#[derive(serde::Deserialize)]
struct GithubRelease {
    tag_name: String,
}

async fn query_latest_release(
    client: &reqwest::Client,
    repo: &str,
    sleep_duration: Duration,
) -> Result<String> {
    let url = format!("https://api.github.com/repos/{}/releases/latest", repo);

    let mut attempt = 0u32;
    loop {
        let resp = client
            .get(&url)
            .header("Accept", "application/vnd.github+json")
            .send()
            .await
            .context("Failed to query GitHub API")?;

        if resp.status() == reqwest::StatusCode::TOO_MANY_REQUESTS {
            let retry_after = resp
                .headers()
                .get("Retry-After")
                .and_then(|v| v.to_str().ok())
                .and_then(|v| v.parse::<u64>().ok())
                .unwrap_or(60);
            eprintln!("Rate limited (429), sleeping {}s...", retry_after);
            tokio::time::sleep(Duration::from_secs(retry_after)).await;
            attempt += 1;
            if attempt > 3 {
                anyhow::bail!("Too many retries after being rate limited");
            }
            continue;
        }

        if !resp.status().is_success() {
            anyhow::bail!("GitHub API returned {}", resp.status());
        }

        let remaining = resp
            .headers()
            .get("X-RateLimit-Remaining")
            .and_then(|v| v.to_str().ok())
            .and_then(|v| v.parse::<u32>().ok());

        let release: GithubRelease = resp.json().await?;

        tokio::time::sleep(sleep_duration).await;

        if let Some(rem) = remaining {
            if rem < 10 {
                eprintln!("Rate limit low ({} remaining), sleeping 60s...", rem);
                tokio::time::sleep(Duration::from_secs(60)).await;
            }
        }

        return Ok(release.tag_name.trim_start_matches('v').to_string());
    }
}

// ── Version comparison ───────────────────────────────────────────────────

pub fn compare_versions(current: &str, latest: &str) -> String {
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

// ── Tests ────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_compare_versions_ok() {
        assert_eq!(compare_versions("1.0.0", "1.0.0"), "OK");
        assert_eq!(compare_versions("2.0.0", "1.0.0"), "OK");
        assert_eq!(compare_versions("1.0.0", "2.0.0"), "OUTDATED");
        assert_eq!(compare_versions("1.2.3", "1.2.4"), "OUTDATED");
        assert_eq!(compare_versions("1.2.4", "1.2.3"), "OK");
    }

    #[test]
    fn test_compare_versions_non_semver() {
        assert_eq!(compare_versions("v1", "v1"), "OK");
        assert_eq!(compare_versions("v1", "v2"), "OUTDATED");
        assert_eq!(compare_versions("abc", "abc"), "OK");
        assert_eq!(compare_versions("abc", "def"), "OUTDATED");
    }

    #[test]
    fn test_compare_versions_mixed() {
        // One parseable, one not
        assert_eq!(compare_versions("1.0.0", "abc"), "OUTDATED");
        assert_eq!(compare_versions("abc", "1.0.0"), "OUTDATED");
    }
}
