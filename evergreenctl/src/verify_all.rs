use anyhow::{Context, Result};
use regex::Regex;
use std::path::Path;

#[derive(Debug, Clone, PartialEq)]
enum Category {
    DirectDownload,
    PackageManager,
    CopyFrom,
    BaseImage,
}

struct VerifyEntry {
    name: String,
    category: Category,
    has_checksum: bool,
    algo: String,
    status: String,
}

pub fn cmd_verify_all(images_dir: &str) -> Result<i32> {
    let dir = Path::new(images_dir);
    if !dir.exists() {
        anyhow::bail!("Images directory not found: {}", images_dir);
    }

    let mut entries: Vec<VerifyEntry> = Vec::new();

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
        let dockerfile = path.join("Dockerfile");
        let manifest_path = path.join("manifest.toml");

        if !dockerfile.exists() {
            continue;
        }

        let content = std::fs::read_to_string(&dockerfile)
            .with_context(|| format!("Failed to read: {}", dockerfile.display()))?;

        let category = classify(&content);
        let has_checksum = has_checksum(&content, &manifest_path);
        let algo = checksum_algo(&content, &manifest_path);

        let status = match (&category, has_checksum) {
            (Category::PackageManager, _) => "N/A".to_string(),
            (Category::CopyFrom, _) => "N/A".to_string(),
            (Category::BaseImage, _) => "N/A".to_string(),
            (_, true) => "VERIFIED".to_string(),
            (_, false) => "MISSING".to_string(),
        };

        entries.push(VerifyEntry {
            name,
            category,
            has_checksum,
            algo,
            status,
        });
    }

    println!(
        "{:<30} {:<20} {:<12} {:<10}",
        "IMAGE", "TYPE", "CHECKSUM", "STATUS"
    );
    println!("{}", "-".repeat(72));

    for e in &entries {
        let type_str = match e.category {
            Category::DirectDownload => "direct-download",
            Category::PackageManager => "package-manager",
            Category::CopyFrom => "copy-from",
            Category::BaseImage => "base-image",
        };
        let checksum_str = if e.has_checksum { &e.algo } else { "-" };
        println!(
            "{:<30} {:<20} {:<12} {:<10}",
            e.name, type_str, checksum_str, e.status
        );
    }

    let total = entries.len();
    let direct = entries
        .iter()
        .filter(|e| e.category == Category::DirectDownload)
        .count();
    let pkg_mgr = entries
        .iter()
        .filter(|e| e.category == Category::PackageManager)
        .count();
    let copy_from = entries
        .iter()
        .filter(|e| e.category == Category::CopyFrom)
        .count();
    let base = entries
        .iter()
        .filter(|e| e.category == Category::BaseImage)
        .count();
    let verified = entries.iter().filter(|e| e.status == "VERIFIED").count();
    let missing = entries.iter().filter(|e| e.status == "MISSING").count();

    println!("\nSummary");
    println!("=======");
    println!("Total images: {}", total);
    println!("Direct downloads: {}", direct);
    println!("  - With checksum: {}", verified);
    println!("  - Missing checksum: {}", missing);
    println!("Package manager: {}", pkg_mgr);
    println!("COPY --from (re-wrap): {}", copy_from);
    println!("Base images: {}", base);

    if missing > 0 {
        Ok(1)
    } else {
        Ok(0)
    }
}

fn classify(content: &str) -> Category {
    let copy_re = Regex::new(r"COPY\s+--from=\S+").unwrap();
    if copy_re.is_match(content) && !has_build_runs(content) {
        return Category::CopyFrom;
    }

    if (content.contains("apk add")
        || content.contains("apt-get install")
        || content.contains("pip install")
        || content.contains("npm install"))
        && !has_direct_download(content)
    {
        return Category::PackageManager;
    }

    if !has_build_runs(content) && !has_direct_download(content) {
        return Category::BaseImage;
    }

    Category::DirectDownload
}

fn has_build_runs(content: &str) -> bool {
    let skip = ["addgroup", "adduser", "chown", "mkdir", "chmod"];
    for line in content.lines() {
        let trimmed = line.trim();
        if trimmed.starts_with("RUN ") && !skip.iter().any(|s| trimmed.contains(s)) {
            return true;
        }
    }
    false
}

fn has_direct_download(content: &str) -> bool {
    let re = Regex::new(r"(?:curl|wget)\s+.*https?://").unwrap();
    re.is_match(content)
}

fn has_checksum(content: &str, manifest_path: &Path) -> bool {
    if manifest_path.exists() {
        if let Ok(manifest) = crate::manifest::Manifest::from_file(manifest_path) {
            return !manifest.source.checksum.expected.is_empty();
        }
    }

    content.contains("sha256sum -c")
        || content.contains("sha512sum -c")
        || content.contains("sha256sum --check")
}

fn checksum_algo(content: &str, manifest_path: &Path) -> String {
    if manifest_path.exists() {
        if let Ok(manifest) = crate::manifest::Manifest::from_file(manifest_path) {
            if !manifest.source.checksum.expected.is_empty() {
                return manifest.source.checksum.algorithm.clone();
            }
        }
    }

    if content.contains("sha512") {
        "sha512".to_string()
    } else {
        "sha256".to_string()
    }
}
