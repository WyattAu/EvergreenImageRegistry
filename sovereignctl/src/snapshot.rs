use crate::manifest::Manifest;
use anyhow::{Context, Result};
use serde::Serialize;
use std::path::Path;

#[derive(Debug, Serialize)]
struct Snapshot {
    image_name: String,
    image_version: String,
    base_image: BaseImageInfo,
    downloads: Vec<DownloadInfo>,
    build_args: Vec<BuildArgInfo>,
    generated_at: String,
}

#[derive(Debug, Serialize)]
struct BaseImageInfo {
    image: String,
    purpose: String,
}

#[derive(Debug, Serialize)]
struct DownloadInfo {
    url: String,
    fallback_urls: Vec<String>,
    checksum_algorithm: String,
    checksum_expected: String,
    strategy: String,
}

#[derive(Debug, Serialize)]
struct BuildArgInfo {
    name: String,
    value: String,
}

pub fn cmd_snapshot(image_dir: &str) -> Result<()> {
    let dir = Path::new(image_dir);
    let manifest_path = dir.join("manifest.toml");
    let manifest = Manifest::from_file(&manifest_path)
        .with_context(|| format!("Failed to read manifest from {}", manifest_path.display()))?;

    let snapshot = Snapshot {
        image_name: manifest.image.name.clone(),
        image_version: manifest.image.version.clone(),
        base_image: BaseImageInfo {
            image: manifest.build.base.image.clone(),
            purpose: manifest.build.base.purpose.clone(),
        },
        downloads: vec![DownloadInfo {
            url: manifest.source.url.clone(),
            fallback_urls: manifest.source.fallback_urls.clone(),
            checksum_algorithm: manifest.source.checksum.algorithm.clone(),
            checksum_expected: manifest.source.checksum.expected.clone(),
            strategy: format!("{:?}", manifest.source.strategy).to_lowercase(),
        }],
        build_args: manifest
            .build
            .build_args
            .iter()
            .map(|(k, v)| BuildArgInfo {
                name: k.clone(),
                value: v.clone(),
            })
            .collect(),
        generated_at: chrono::Utc::now().to_rfc3339(),
    };

    let json = serde_json::to_string_pretty(&snapshot)?;
    println!("{}", json);

    Ok(())
}
