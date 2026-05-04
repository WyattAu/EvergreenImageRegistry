use anyhow::{Context, Result};
use sha2::{Digest, Sha256, Sha512};
use tracing::info;

/// Compute SHA-256 of a file
pub fn sha256_file(path: &std::path::Path) -> Result<String> {
    let mut file = std::fs::File::open(path)
        .with_context(|| format!("Failed to open file: {}", path.display()))?;
    let mut hasher = Sha256::new();
    std::io::copy(&mut file, &mut hasher)?;
    Ok(hex::encode(hasher.finalize()))
}

/// Compute SHA-512 of a file
pub fn sha512_file(path: &std::path::Path) -> Result<String> {
    let mut file = std::fs::File::open(path)
        .with_context(|| format!("Failed to open file: {}", path.display()))?;
    let mut hasher = Sha512::new();
    std::io::copy(&mut file, &mut hasher)?;
    Ok(hex::encode(hasher.finalize()))
}

/// Compute checksum using specified algorithm
pub fn compute_checksum(path: &std::path::Path, algorithm: &str) -> Result<String> {
    match algorithm.to_lowercase().as_str() {
        "sha256" => sha256_file(path),
        "sha512" => sha512_file(path),
        other => anyhow::bail!("Unsupported checksum algorithm: {}", other),
    }
}

/// Verify a file's checksum against an expected value
pub fn verify_checksum(
    path: &std::path::Path,
    algorithm: &str,
    expected: &str,
) -> Result<VerifyResult> {
    let computed = compute_checksum(path, algorithm)?;

    let computed_clean = computed.to_lowercase();
    let expected_clean = expected.to_lowercase();

    let matches = computed_clean == expected_clean;

    Ok(VerifyResult {
        algorithm: algorithm.to_string(),
        expected: expected_clean,
        computed: computed_clean,
        matches,
    })
}

#[derive(Debug, Clone)]
pub struct VerifyResult {
    pub algorithm: String,
    pub expected: String,
    pub computed: String,
    pub matches: bool,
}

impl std::fmt::Display for VerifyResult {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        if self.matches {
            write!(
                f,
                "✓ {} MATCHES (expected: {}...)",
                self.algorithm,
                &self.expected[..16.min(self.expected.len())]
            )
        } else {
            write!(
                f,
                "✗ {} MISMATCH\n  expected: {}\n  computed: {}",
                self.algorithm, self.expected, self.computed
            )
        }
    }
}

/// Download a file and verify its checksum
pub async fn download_and_verify(
    client: &reqwest::Client,
    url: &str,
    dest: &std::path::Path,
    algorithm: &str,
    expected: &str,
) -> Result<VerifyResult> {
    info!("Downloading: {}", url);

    let resp = client
        .get(url)
        .header("User-Agent", "evergreenctl/0.1.0")
        .send()
        .await
        .context("Download failed")?;

    if !resp.status().is_success() {
        anyhow::bail!("Download returned status: {}", resp.status());
    }

    let bytes = resp.bytes().await.context("Failed to read response body")?;

    if let Some(parent) = dest.parent() {
        std::fs::create_dir_all(parent)?;
    }

    std::fs::write(dest, &bytes)
        .with_context(|| format!("Failed to write to: {}", dest.display()))?;

    info!("Downloaded {} bytes to {}", bytes.len(), dest.display());

    let result = verify_checksum(dest, algorithm, expected)?;

    if !result.matches {
        let _ = std::fs::remove_file(dest);
    }

    Ok(result)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sha256_empty() {
        let dir = std::env::temp_dir().join("evergreenctl_test");
        let _ = std::fs::create_dir_all(&dir);
        let path = dir.join("test_empty");
        std::fs::write(&path, "").unwrap();
        let hash = sha256_file(&path).unwrap();
        assert_eq!(
            hash,
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        );
        let _ = std::fs::remove_file(&path);
    }

    #[test]
    fn test_sha256_hello() {
        let dir = std::env::temp_dir().join("evergreenctl_test");
        let _ = std::fs::create_dir_all(&dir);
        let path = dir.join("test_hello");
        std::fs::write(&path, "hello").unwrap();
        let hash = sha256_file(&path).unwrap();
        assert_eq!(
            hash,
            "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        );
        let _ = std::fs::remove_file(&path);
    }

    #[test]
    fn test_verify_match() {
        let dir = std::env::temp_dir().join("evergreenctl_test");
        let _ = std::fs::create_dir_all(&dir);
        let path = dir.join("test_verify");
        std::fs::write(&path, "hello").unwrap();
        let result = verify_checksum(
            &path,
            "sha256",
            "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
        )
        .unwrap();
        assert!(result.matches);
        let _ = std::fs::remove_file(&path);
    }
}
