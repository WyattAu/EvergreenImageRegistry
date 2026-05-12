use crate::manifest::Manifest;
use anyhow::{Context, Result};
use serde::Serialize;
use std::path::Path;

#[derive(Debug, Serialize)]
struct Snapshot {
    image_name: String,
    image_version: String,
    base_image: String,
    source_url: String,
    source_type: String,
    entrypoint: Vec<String>,
    exposed_ports: Vec<u16>,
    tier: String,
    github_repo: Option<String>,
    generated_at: String,
}

pub fn cmd_snapshot(image_dir: &str) -> Result<()> {
    let dir = Path::new(image_dir);
    let manifest_path = dir.join("manifest.toml");
    let manifest = Manifest::from_file(&manifest_path)
        .with_context(|| format!("Failed to read manifest from {}", manifest_path.display()))?;

    let snapshot = Snapshot {
        image_name: manifest.name().to_string(),
        image_version: manifest.version().to_string(),
        base_image: manifest.base_image().to_string(),
        source_url: manifest.source_url().to_string(),
        source_type: manifest.source.source_type.clone(),
        entrypoint: manifest.entrypoint().to_vec(),
        exposed_ports: manifest.exposed_ports().to_vec(),
        tier: manifest.metadata.tier.clone(),
        github_repo: manifest.github_repo(),
        generated_at: chrono::Utc::now().to_rfc3339(),
    };

    let json = serde_json::to_string_pretty(&snapshot)?;
    println!("{}", json);

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_snapshot_serialization() {
        let snap = Snapshot {
            image_name: "redis".to_string(),
            image_version: "7.4.1".to_string(),
            base_image: "scratch".to_string(),
            source_url: "https://example.com/redis.tar.gz".to_string(),
            source_type: "binary-download".to_string(),
            entrypoint: vec!["/redis".to_string()],
            exposed_ports: vec![6379],
            tier: "1".to_string(),
            github_repo: Some("redis/redis".to_string()),
            generated_at: "2026-01-01T00:00:00+00:00".to_string(),
        };
        let json = serde_json::to_string(&snap).unwrap();
        assert!(json.contains("redis"));
        assert!(json.contains("7.4.1"));
        assert!(json.contains("redis/redis"));
    }
}
