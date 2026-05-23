use anyhow::{Context, Result};
use serde::Deserialize;
use tracing::{debug, info, warn};

#[derive(Debug, Deserialize)]
struct GithubRelease {
    tag_name: String,
    assets: Vec<GithubAsset>,
    #[allow(dead_code)]
    html_url: String,
}

#[derive(Debug, Deserialize)]
struct GithubAsset {
    name: String,
    browser_download_url: String,
    size: u64,
}

#[derive(Debug, Clone)]
pub struct DiscoveredSource {
    pub url: String,
    pub version: String,
    pub size_bytes: Option<u64>,
    pub content_type: Option<String>,
    pub source: String,
}

pub async fn discover_github_release(
    client: &reqwest::Client,
    owner: &str,
    repo: &str,
    version: Option<&str>,
    asset_pattern: Option<&str>,
) -> Result<Vec<DiscoveredSource>> {
    let url = if let Some(ver) = version {
        format!(
            "https://api.github.com/repos/{}/{}/releases/tags/{}",
            owner, repo, ver
        )
    } else {
        format!(
            "https://api.github.com/repos/{}/{}/releases/latest",
            owner, repo
        )
    };

    info!(
        "Probing GitHub: {}/{} (version: {:?})",
        owner, repo, version
    );

    let resp = client
        .get(&url)
        .header("Accept", "application/vnd.github+json")
        .header("User-Agent", crate::USER_AGENT)
        .send()
        .await
        .context("Failed to query GitHub API")?;

    if !resp.status().is_success() {
        anyhow::bail!("GitHub API returned status {}", resp.status());
    }

    let release: GithubRelease = resp.json().await?;

    let mut sources = Vec::new();
    for asset in &release.assets {
        if let Some(pattern) = asset_pattern {
            if !asset.name.contains(pattern) {
                continue;
            }
        }
        if asset.name.contains("linux") && asset.name.contains("amd64") {
            sources.push(DiscoveredSource {
                url: asset.browser_download_url.clone(),
                version: release.tag_name.trim_start_matches('v').to_string(),
                size_bytes: Some(asset.size),
                content_type: Some("application/octet-stream".to_string()),
                source: format!("github:{}/{}", owner, repo),
            });
        }
    }

    if sources.is_empty() {
        for asset in &release.assets {
            if let Some(pattern) = asset_pattern {
                if !asset.name.contains(pattern) {
                    continue;
                }
            }
            sources.push(DiscoveredSource {
                url: asset.browser_download_url.clone(),
                version: release.tag_name.trim_start_matches('v').to_string(),
                size_bytes: Some(asset.size),
                content_type: Some("application/octet-stream".to_string()),
                source: format!("github:{}/{}", owner, repo),
            });
        }
    }

    Ok(sources)
}

pub async fn probe_url(client: &reqwest::Client, url: &str) -> Result<ProbeResult> {
    debug!("Probing URL: {}", url);

    let result = client
        .head(url)
        .header("User-Agent", crate::USER_AGENT)
        .send()
        .await;

    match result {
        Ok(resp) => {
            let status = resp.status().as_u16();
            let content_length = resp
                .headers()
                .get("content-length")
                .and_then(|v| v.to_str().ok())
                .and_then(|v| v.parse::<u64>().ok());
            let content_type = resp
                .headers()
                .get("content-type")
                .and_then(|v| v.to_str().ok())
                .map(|s| s.to_string());

            Ok(ProbeResult {
                accessible: status == 200,
                status_code: status,
                content_length,
                content_type,
            })
        }
        Err(e) => {
            warn!("Probe failed for {}: {}", url, e);
            Ok(ProbeResult {
                accessible: false,
                status_code: 0,
                content_length: None,
                content_type: None,
            })
        }
    }
}

#[derive(Debug, Clone)]
pub struct ProbeResult {
    pub accessible: bool,
    pub status_code: u16,
    pub content_length: Option<u64>,
    pub content_type: Option<String>,
}

pub async fn discover_with_fallbacks(
    client: &reqwest::Client,
    url_patterns: &[String],
) -> Result<DiscoveredSource> {
    for url in url_patterns {
        let probe = probe_url(client, url).await?;
        if probe.accessible && probe.content_length.is_some_and(|len| len > 1024) {
            info!(
                "Found working URL: {} ({} bytes)",
                url,
                probe.content_length.unwrap_or(0)
            );
            return Ok(DiscoveredSource {
                url: url.clone(),
                version: String::new(),
                size_bytes: probe.content_length,
                content_type: probe.content_type,
                source: "probe".to_string(),
            });
        }
    }
    anyhow::bail!("No working URL found among {} patterns", url_patterns.len())
}

pub fn extract_github_repo(url: &str) -> Option<(String, String)> {
    let url = url.trim_end_matches(".git");

    let patterns = [
        "https://github.com/",
        "http://github.com/",
        "git://github.com/",
    ];

    for prefix in &patterns {
        if let Some(rest) = url.strip_prefix(prefix) {
            let parts: Vec<&str> = rest.split('/').take(2).collect();
            if parts.len() == 2 {
                return Some((parts[0].to_string(), parts[1].to_string()));
            }
        }
    }
    None
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_extract_github_repo() {
        assert_eq!(
            extract_github_repo("https://github.com/prometheus/node_exporter"),
            Some(("prometheus".to_string(), "node_exporter".to_string()))
        );
        assert_eq!(
            extract_github_repo("https://github.com/prometheus/node_exporter.git"),
            Some(("prometheus".to_string(), "node_exporter".to_string()))
        );
        assert_eq!(extract_github_repo("https://example.com/foo"), None);
    }
}
