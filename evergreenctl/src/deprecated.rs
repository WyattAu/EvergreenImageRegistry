use anyhow::{Context, Result};
use std::path::Path;
use walkdir::WalkDir;

#[derive(Debug)]
pub struct DeprecatedImage {
    pub name: String,
    pub manifest_path: std::path::PathBuf,
}

pub fn list_deprecated(images_dir: &Path) -> Result<Vec<DeprecatedImage>> {
    let mut deprecated = Vec::new();

    for entry in WalkDir::new(images_dir)
        .min_depth(1)
        .max_depth(1)
        .sort_by_file_name()
    {
        let entry = entry?;
        let path = entry.path();
        if !path.is_dir() {
            continue;
        }

        let manifest_path = path.join("manifest.toml");
        if !manifest_path.exists() {
            continue;
        }

        match crate::manifest::Manifest::from_file(&manifest_path) {
            Ok(manifest) => {
                if manifest.metadata.deprecated {
                    deprecated.push(DeprecatedImage {
                        name: entry.file_name().to_string_lossy().to_string(),
                        manifest_path,
                    });
                }
            }
            Err(e) => {
                tracing::warn!("Skipping {}: {}", manifest_path.display(), e);
            }
        }
    }

    Ok(deprecated)
}

pub fn mark_deprecated(images_dir: &Path, image: &str) -> Result<()> {
    // Validate image name to prevent path traversal
    if image.contains('/') || image.contains('\\') || image.contains("..") {
        anyhow::bail!("Invalid image name (path traversal detected): {}", image);
    }

    let manifest_path = images_dir.join(image).join("manifest.toml");

    if !manifest_path.exists() {
        anyhow::bail!("Manifest not found: {}", manifest_path.display());
    }

    let mut manifest = crate::manifest::Manifest::from_file(&manifest_path)
        .with_context(|| format!("Failed to read {}", manifest_path.display()))?;

    if manifest.metadata.deprecated {
        println!("{} is already marked as deprecated", image);
        return Ok(());
    }

    manifest.metadata.deprecated = true;
    manifest.to_file(&manifest_path)?;

    println!("Marked {} as deprecated", image);

    Ok(())
}

pub fn unmark_deprecated(images_dir: &Path, image: &str) -> Result<()> {
    // Validate image name to prevent path traversal
    if image.contains('/') || image.contains('\\') || image.contains("..") {
        anyhow::bail!("Invalid image name (path traversal detected): {}", image);
    }

    let manifest_path = images_dir.join(image).join("manifest.toml");

    if !manifest_path.exists() {
        anyhow::bail!("Manifest not found: {}", manifest_path.display());
    }

    let mut manifest = crate::manifest::Manifest::from_file(&manifest_path)
        .with_context(|| format!("Failed to read {}", manifest_path.display()))?;

    if !manifest.metadata.deprecated {
        println!("{} is not marked as deprecated", image);
        return Ok(());
    }

    manifest.metadata.deprecated = false;
    manifest.to_file(&manifest_path)?;

    println!("Removed deprecated flag from {}", image);

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn create_image_dir(tmp: &tempfile::TempDir, name: &str, manifest_content: &str) {
        let dir = tmp.path().join(name);
        std::fs::create_dir_all(&dir).unwrap();
        std::fs::write(dir.join("manifest.toml"), manifest_content).unwrap();
    }

    const BASE_MANIFEST: &str = r#"
[metadata]
name = "testimg"
version = "1.0"

[build]
base = "scratch"

[source]
url = "https://example.com/test.tar.gz"

[runtime]
entrypoint = ["/test"]
"#;

    #[test]
    fn test_list_no_deprecated() {
        let tmp = tempfile::tempdir().unwrap();

        create_image_dir(&tmp, "redis", BASE_MANIFEST);
        create_image_dir(&tmp, "nginx", BASE_MANIFEST);

        let result = list_deprecated(tmp.path()).unwrap();
        assert!(result.is_empty());
    }

    #[test]
    fn test_list_with_deprecated() {
        let tmp = tempfile::tempdir().unwrap();

        create_image_dir(&tmp, "redis", BASE_MANIFEST);

        let deprecated_manifest = r#"
[metadata]
name = "oldimg"
version = "1.0"
deprecated = true

[build]
base = "scratch"

[source]
url = "https://example.com/old.tar.gz"

[runtime]
entrypoint = ["/old"]
"#;
        create_image_dir(&tmp, "oldimg", deprecated_manifest);

        let result = list_deprecated(tmp.path()).unwrap();
        assert_eq!(result.len(), 1);
        assert_eq!(result[0].name, "oldimg");
    }

    #[test]
    fn test_mark_deprecated() {
        let tmp = tempfile::tempdir().unwrap();

        create_image_dir(&tmp, "redis", BASE_MANIFEST);

        mark_deprecated(tmp.path(), "redis").unwrap();

        let manifest =
            crate::manifest::Manifest::from_file(&tmp.path().join("redis").join("manifest.toml"))
                .unwrap();
        assert!(manifest.metadata.deprecated);
    }

    #[test]
    fn test_unmark_deprecated() {
        let tmp = tempfile::tempdir().unwrap();

        let deprecated_manifest = r#"
[metadata]
name = "oldimg"
version = "1.0"
deprecated = true

[build]
base = "scratch"

[source]
url = "https://example.com/old.tar.gz"

[runtime]
entrypoint = ["/old"]
"#;
        create_image_dir(&tmp, "oldimg", deprecated_manifest);

        unmark_deprecated(tmp.path(), "oldimg").unwrap();

        let manifest =
            crate::manifest::Manifest::from_file(&tmp.path().join("oldimg").join("manifest.toml"))
                .unwrap();
        assert!(!manifest.metadata.deprecated);
    }

    #[test]
    fn test_mark_already_deprecated() {
        let tmp = tempfile::tempdir().unwrap();

        let deprecated_manifest = r#"
[metadata]
name = "oldimg"
version = "1.0"
deprecated = true

[build]
base = "scratch"

[source]
url = "https://example.com/old.tar.gz"

[runtime]
entrypoint = ["/old"]
"#;
        create_image_dir(&tmp, "oldimg", deprecated_manifest);

        let result = mark_deprecated(tmp.path(), "oldimg");
        assert!(result.is_ok());
    }

    #[test]
    fn test_mark_nonexistent_image() {
        let tmp = tempfile::tempdir().unwrap();
        let result = mark_deprecated(tmp.path(), "nonexistent");
        assert!(result.is_err());
    }

    #[test]
    fn test_unmark_non_deprecated() {
        let tmp = tempfile::tempdir().unwrap();

        create_image_dir(&tmp, "redis", BASE_MANIFEST);

        let result = unmark_deprecated(tmp.path(), "redis");
        assert!(result.is_ok());
    }
}
