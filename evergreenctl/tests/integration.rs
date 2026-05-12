// =============================================================================
// Evergreenctl Integration Tests
// =============================================================================
// Tests that validate full workflows across multiple modules.
// Run with: cargo test --test integration
// =============================================================================

use std::fs;
use tempfile::TempDir;

// =============================================================================
// Test 1: Manifest round-trip - Dockerfile to manifest and back
// =============================================================================

#[test]
fn test_manifest_round_trip() {
    use evergreenctl::manifest::Manifest;
    use evergreenctl::migrate::dockerfile_to_manifest;

    let dir = TempDir::new().unwrap();
    let df_path = dir.path().join("Dockerfile");
    let manifest_path = dir.path().join("manifest.toml");

    // Create a realistic multi-stage Dockerfile
    let dockerfile_content = r#"# syntax=docker/dockerfile:1
FROM debian:bookworm-slim@sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa AS builder
ARG VERSION=1.2.3
RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://example.com/releases/v${VERSION}/app-linux-amd64.tar.gz -o app.tar.gz

FROM scratch
COPY --from=builder /app /app
USER 65532:65532
ENTRYPOINT ["/app", "serve"]
CMD ["--port", "8080"]
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD ["/app", "health"]
LABEL org.opencontainers.image.title="roundtrip-test"
LABEL org.opencontainers.image.description="Integration test image"
LABEL org.opencontainers.image.source="https://github.com/test/roundtrip"
LABEL org.opencontainers.image.version="1.2.3"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
STOPSIGNAL SIGTERM
"#;

    fs::write(&df_path, dockerfile_content).unwrap();

    // Step 1: Convert Dockerfile to Manifest struct
    let manifest =
        dockerfile_to_manifest(&df_path, "roundtrip-test").expect("should parse Dockerfile");

    // Step 2: Write manifest to TOML file
    manifest
        .to_file(&manifest_path)
        .expect("should write manifest");

    // Step 3: Read manifest back from file
    let parsed = Manifest::from_file(&manifest_path).expect("should re-parse manifest");

    // Verify metadata source (GitHub URL from OCI labels)
    assert_eq!(parsed.metadata.source, "https://github.com/test/roundtrip");
    // source_url() returns the download URL, not the OCI source
    assert!(
        parsed.source_url().contains("example.com"),
        "source_url should be the download URL, got: {}",
        parsed.source_url()
    );
    assert_eq!(parsed.base_image(), "scratch");
    assert_eq!(parsed.user(), "65532:65532");
    assert_eq!(parsed.stop_signal(), "SIGTERM");

    // Verify entrypoint
    let entry = parsed.entrypoint();
    assert!(
        entry.contains(&"/app".to_string()),
        "entrypoint: {:?}",
        entry
    );
    assert!(
        entry.contains(&"serve".to_string()),
        "entrypoint should contain subcommand: {:?}",
        entry
    );

    // Verify exposed ports
    let ports = parsed.exposed_ports();
    assert!(
        ports.contains(&8080),
        "should expose port 8080, got: {:?}",
        ports
    );

    // Verify labels
    assert_eq!(parsed.label("evergreen.security.cap-drop"), Some("ALL"));
    assert_eq!(
        parsed.label("evergreen.security.no-new-privileges"),
        Some("true")
    );
}

// =============================================================================
// Test 2: Audit detects stub patterns in Dockerfiles
// =============================================================================

#[test]
fn test_audit_detects_stub_patterns() {
    use evergreenctl::audit::{audit_dockerfile, ImageStatus};

    let dir = TempDir::new().unwrap();

    // Create a stub Dockerfile (sleep infinity, no real binary download)
    let stub_path = dir.path().join("Dockerfile");
    fs::write(
        &stub_path,
        r#"FROM scratch
CMD sleep infinity
"#,
    )
    .unwrap();

    let result = audit_dockerfile(&stub_path, "stub-image").unwrap();
    assert_eq!(
        result.status,
        ImageStatus::Stub,
        "Dockerfile with sleep infinity should be classified as Stub"
    );

    // Create a real Dockerfile (binary download, real entrypoint)
    let real_dir = TempDir::new().unwrap();
    let real_path = real_dir.path().join("Dockerfile");
    fs::write(
        &real_path,
        r#"FROM wolfi-base:latest@sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa AS builder
ARG VERSION=1.0.0
RUN curl -fsSL https://example.com/v${VERSION}/app.tar.gz -o app.tar.gz && \
    tar xzf app.tar.gz -C /usr/local/bin/

FROM scratch
COPY --from=builder /usr/local/bin/app /app
USER 65532:65532
ENTRYPOINT ["/app"]
HEALTHCHECK NONE
"#,
    )
    .unwrap();

    let result = audit_dockerfile(&real_path, "real-image").unwrap();
    assert_eq!(
        result.status,
        ImageStatus::Real,
        "Dockerfile with real binary download should be Real"
    );
}

// =============================================================================
// Test 3: Audit detects RUN && syntax issues
// =============================================================================

#[test]
fn test_audit_detects_run_double_ampersand() {
    use evergreenctl::audit::audit_dockerfile;

    let dir = TempDir::new().unwrap();
    let df_path = dir.path().join("Dockerfile");
    fs::write(
        &df_path,
        r#"FROM scratch
COPY --from=builder /app /app
RUN && echo "no command before &&"
"#,
    )
    .unwrap();

    let result = audit_dockerfile(&df_path, "bad-image").unwrap();
    let has_run_and = result.issues.iter().any(|i| i.code == "RUN_AND");
    assert!(
        has_run_and,
        "Should detect RUN && (no command before &&). Issues: {:?}",
        result.issues
    );
}

// =============================================================================
// Test 4: Pin-digests dry run does not modify files
// =============================================================================

#[test]
fn test_pin_digests_dry_run_no_modify() {
    use evergreenctl::pin_digests::cmd_pin_digests;

    let dir = TempDir::new().unwrap();
    let df_path = dir.path().join("Dockerfile");

    let dockerfile_content = r#"FROM wolfi-base:latest AS builder
RUN echo "build step"
FROM scratch
COPY --from=builder /app /app
"#;

    fs::write(&df_path, dockerfile_content).unwrap();
    let original = fs::read_to_string(&df_path).unwrap();

    // Run dry-run mode
    let result = cmd_pin_digests(
        dir.path().to_str().unwrap(),
        true, // dry_run
    );

    // Dry-run may fail if crane is not installed, but should not panic
    if let Err(e) = &result {
        eprintln!("Dry-run pin_digests (expected if crane unavailable): {}", e);
    }

    // File should be unchanged after dry-run
    let after = fs::read_to_string(&df_path).unwrap();
    assert_eq!(original, after, "Dry-run should not modify files");
}

// =============================================================================
// Test 5: Verify checksums with known test vectors
// =============================================================================

#[test]
fn test_verify_known_vectors() {
    use evergreenctl::verify::verify_checksum;

    let dir = TempDir::new().unwrap();

    // Test SHA256 - "Hello, World!"
    let hello_path = dir.path().join("hello.txt");
    fs::write(&hello_path, "Hello, World!").unwrap();

    let sha256_hello = "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f";
    let result = verify_checksum(&hello_path, "sha256", sha256_hello).unwrap();
    assert!(result.matches, "SHA256 should match");

    // Test mismatch
    let wrong_hash = "0000000000000000000000000000000000000000000000000000000000000000";
    let result = verify_checksum(&hello_path, "sha256", wrong_hash).unwrap();
    assert!(!result.matches, "Wrong hash should not match");

    // Test empty file
    let empty_path = dir.path().join("empty.txt");
    fs::write(&empty_path, "").unwrap();
    let sha256_empty = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855";
    let result = verify_checksum(&empty_path, "sha256", sha256_empty).unwrap();
    assert!(result.matches, "Empty file SHA256 should match");
}

// =============================================================================
// Test 6: Manifest parsing with minimal TOML
// =============================================================================

#[test]
fn test_manifest_minimal_parse() {
    use evergreenctl::manifest::Manifest;

    let dir = TempDir::new().unwrap();
    let manifest_path = dir.path().join("manifest.toml");

    let minimal_toml = r#"
[metadata]
name = "minimal-test"
version = "1.0.0"

[source]
type = "binary"
url = "https://github.com/test/minimal"

[binary]
name = "test-binary"
version_flag = "--version"
"#;

    fs::write(&manifest_path, minimal_toml).unwrap();
    let manifest = Manifest::from_file(&manifest_path).unwrap();

    assert_eq!(manifest.name(), "minimal-test");
    assert_eq!(manifest.version(), "1.0.0");
    assert_eq!(manifest.source_url(), "https://github.com/test/minimal");
}

// =============================================================================
// Test 7: SHA256 computation is deterministic
// =============================================================================

#[test]
fn test_sha256_deterministic() {
    use evergreenctl::verify::sha256_file;

    let dir = TempDir::new().unwrap();
    let path = dir.path().join("test.bin");

    let data = vec![0u8; 4096]; // 4KB of zeros
    fs::write(&path, &data).unwrap();

    let hash1 = sha256_file(&path).unwrap();
    let hash2 = sha256_file(&path).unwrap();

    assert_eq!(hash1, hash2, "SHA256 must be deterministic");
    assert_eq!(hash1.len(), 64, "SHA256 must be 64 hex chars");
}

// =============================================================================
// Test 8: GitHub repo extraction from manifest
// =============================================================================

#[test]
fn test_github_repo_extraction() {
    use evergreenctl::manifest::Manifest;

    let dir = TempDir::new().unwrap();
    let manifest_path = dir.path().join("manifest.toml");

    let toml = r#"
[metadata]
name = "test-image"
version = "2.0.0"

[source]
type = "binary"
url = "https://github.com/owner/repo"
"#;

    fs::write(&manifest_path, toml).unwrap();
    let manifest = Manifest::from_file(&manifest_path).unwrap();

    let repo = manifest.github_repo();
    assert_eq!(
        repo.as_deref(),
        Some("owner/repo"),
        "Should extract Github repo from source URL"
    );
}
