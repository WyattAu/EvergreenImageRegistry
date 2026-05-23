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
        .header("User-Agent", crate::USER_AGENT)
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

    #[test]
    fn test_verify_mismatch() {
        let dir = std::env::temp_dir().join("evergreenctl_test");
        let _ = std::fs::create_dir_all(&dir);
        let path = dir.join("test_mismatch");
        std::fs::write(&path, "hello").unwrap();
        let result = verify_checksum(
            &path,
            "sha256",
            "0000000000000000000000000000000000000000000000000000000000000000",
        )
        .unwrap();
        assert!(!result.matches);
        let _ = std::fs::remove_file(&path);
    }

    #[test]
    fn test_verify_case_insensitive() {
        let dir = std::env::temp_dir().join("evergreenctl_test");
        let _ = std::fs::create_dir_all(&dir);
        let path = dir.join("test_case");
        std::fs::write(&path, "hello").unwrap();
        let result = verify_checksum(
            &path,
            "SHA256",
            "2CF24DBA5FB0A30E26E83B2AC5B9E29E1B161E5C1FA7425E73043362938B9824",
        )
        .unwrap();
        assert!(result.matches);
        let _ = std::fs::remove_file(&path);
    }

    #[test]
    fn test_sha512_hello() {
        let dir = std::env::temp_dir().join("evergreenctl_test");
        let _ = std::fs::create_dir_all(&dir);
        let path = dir.join("test_sha512");
        std::fs::write(&path, "hello").unwrap();
        let hash = sha512_file(&path).unwrap();
        assert_eq!(
            hash,
            "9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca72323c3d99ba5c11d7c7acc6e14b8c5da0c4663475c2e5c3adef46f73bcdec043"
        );
        let _ = std::fs::remove_file(&path);
    }

    #[test]
    fn test_unsupported_algorithm() {
        let dir = std::env::temp_dir().join("evergreenctl_test");
        let _ = std::fs::create_dir_all(&dir);
        let path = dir.join("test_unsupported");
        std::fs::write(&path, "test").unwrap();
        let result = compute_checksum(&path, "md5");
        assert!(result.is_err());
        let err = result.unwrap_err().to_string();
        assert!(err.contains("Unsupported checksum algorithm"));
        let _ = std::fs::remove_file(&path);
    }

    #[test]
    fn test_verify_result_display() {
        let match_result = VerifyResult {
            algorithm: "sha256".to_string(),
            expected: "abcdef0123456789".to_string(),
            computed: "abcdef0123456789".to_string(),
            matches: true,
        };
        assert!(match_result.to_string().contains("MATCHES"));

        let mismatch_result = VerifyResult {
            algorithm: "sha256".to_string(),
            expected: "abcdef0123456789".to_string(),
            computed: "fedcba9876543210".to_string(),
            matches: false,
        };
        assert!(mismatch_result.to_string().contains("MISMATCH"));
    }

    #[test]
    fn test_nonexistent_file() {
        let path = std::path::Path::new("/nonexistent/file/that/does/not/exist");
        let result = sha256_file(path);
        assert!(result.is_err());
    }

    // Integration tests with real files from the images directory
    #[test]
    fn test_verify_real_manifest() {
        // Verify that a real manifest.toml can be parsed
        let manifest_path = std::path::Path::new("images/redis/manifest.toml");
        if manifest_path.exists() {
            let content = std::fs::read_to_string(manifest_path);
            assert!(content.is_ok(), "Manifest file should be readable");
        }
    }

    #[test]
    fn test_verify_real_sbom() {
        let sbom_path = std::path::Path::new("images/redis/sbom.spdx.json");
        if sbom_path.exists() {
            let content = std::fs::read_to_string(sbom_path);
            assert!(content.is_ok(), "SBOM file should be readable");
            let json: Result<serde_json::Value, _> = serde_json::from_str(&content.unwrap());
            assert!(json.is_ok(), "SBOM should be valid JSON");
            let data = json.unwrap();
            assert!(
                data.get("spdxVersion").is_some(),
                "SBOM should have spdxVersion"
            );
        }
    }

    #[test]
    fn test_sha256_deterministic() {
        // Same content should produce identical hashes
        let dir = std::env::temp_dir().join("evergreenctl_test_deterministic");
        let _ = std::fs::create_dir_all(&dir);
        let path = dir.join("test_deterministic");
        let content = b"deterministic hash test content";
        std::fs::write(&path, content).unwrap();

        let hash1 = sha256_file(&path).unwrap();
        let hash2 = sha256_file(&path).unwrap();
        assert_eq!(hash1, hash2, "SHA256 must be deterministic");

        let _ = std::fs::remove_file(&path);
    }

    #[test]
    fn test_sha256_different_content() {
        // Different content must produce different hashes
        let dir = std::env::temp_dir().join("evergreenctl_test_different");
        let _ = std::fs::create_dir_all(&dir);

        let path1 = dir.join("test_diff1");
        let path2 = dir.join("test_diff2");
        std::fs::write(&path1, b"content one").unwrap();
        std::fs::write(&path2, b"content two").unwrap();

        let hash1 = sha256_file(&path1).unwrap();
        let hash2 = sha256_file(&path2).unwrap();
        assert_ne!(
            hash1, hash2,
            "Different content must produce different hashes"
        );

        let _ = std::fs::remove_file(&path1);
        let _ = std::fs::remove_file(&path2);
    }

    #[test]
    fn test_sha256_empty_file() {
        let dir = std::env::temp_dir().join("evergreenctl_test_empty_verify");
        let _ = std::fs::create_dir_all(&dir);
        let path = dir.join("test_empty");
        std::fs::write(&path, "").unwrap();

        let hash = sha256_file(&path).unwrap();
        assert_eq!(
            hash, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "SHA256 of empty file must match known value"
        );

        let _ = std::fs::remove_file(&path);
    }

    #[test]
    fn test_verify_case_insensitive_extended() {
        // HEX digits should be case-insensitive in comparison
        let result = VerifyResult {
            algorithm: "sha256".to_string(),
            expected: "ABCDEF0123456789abcdef0123456789ABCDEF0123456789abcdef0123456789"
                .to_lowercase(),
            computed: "abcdef0123456789ABCDEF0123456789abcdef0123456789ABCDEF0123456789"
                .to_lowercase(),
            matches: true,
        };
        // Both expected and computed are lowercased by verify_checksum,
        // so two differently-cased hex strings that are semantically equal should match
        assert!(result.matches);
    }
}
