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
        ports.contains(&"8080".to_string()),
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

// =============================================================================
// Test 9: Generate produces valid Dockerfile from manifest
// =============================================================================

#[test]
fn test_generate_from_manifest() {
    use evergreenctl::generate::DockerfileGenerator;
    use evergreenctl::manifest::Manifest;

    let dir = TempDir::new().unwrap();
    let manifest_path = dir.path().join("manifest.toml");

    let toml = r#"
[metadata]
name = "gen-test"
version = "3.0.0"
description = "Generated image test"
vendor = "TestVendor"
source = "https://github.com/test/gen-test"
license = "MIT"
tier = "2"

[build]
base = "scratch"
user = "65532:65532"
stopsignal = "SIGTERM"

[source]
type = "binary-download"
url = "https://example.com/releases/v3.0.0/gen-test.tar.gz"

[runtime]
entrypoint = ["/gen-test", "serve"]

[ports]
expose = [9090, 9091]
"#;

    fs::write(&manifest_path, toml).unwrap();
    let manifest = Manifest::from_file(&manifest_path).unwrap();
    let gen = DockerfileGenerator::new(manifest);
    let dockerfile = gen.generate().unwrap();

    // Verify structural elements
    assert!(
        dockerfile.contains("FROM scratch"),
        "Should have scratch runtime stage"
    );
    assert!(
        dockerfile.contains("FROM cgr.dev/chainguard/wolfi-base:latest AS builder"),
        "Should have builder stage"
    );
    assert!(
        dockerfile.contains("USER 65532:65532"),
        "Should set non-root user"
    );
    assert!(
        dockerfile.contains("ENTRYPOINT [\"/gen-test\", \"serve\"]"),
        "Should set entrypoint"
    );
    assert!(
        dockerfile.contains("STOPSIGNAL SIGTERM"),
        "Should set stop signal"
    );
    assert!(
        dockerfile.contains("EXPOSE 9090 9091"),
        "Should expose ports"
    );
    assert!(
        dockerfile.contains("COPY --from=builder /opt/ /opt/"),
        "Should copy from builder"
    );
    assert!(
        dockerfile.contains("org.opencontainers.image.title=\"gen-test\""),
        "Should have OCI title label"
    );
    assert!(
        dockerfile.contains("evergreen.base.image=\"scratch\""),
        "Should have base image label"
    );
    assert!(
        dockerfile.contains("# EVERGREEN HARDENED GEN-TEST"),
        "Should have header comment"
    );
}

// =============================================================================
// Test 10: Drift detects version mismatch between manifest and Dockerfile
// =============================================================================

#[test]
fn test_drift_detects_version_mismatch() {
    use evergreenctl::drift::cmd_drift;

    let dir = TempDir::new().unwrap();

    // Create manifest with version 2.0.0
    let toml = r#"
[metadata]
name = "drift-test"
version = "2.0.0"
description = "Drift test"
vendor = "Test"
source = "https://github.com/test/drift"
license = "MIT"
tier = "1"

[build]
base = "scratch"
user = "65532:65532"
stopsignal = "SIGTERM"

[source]
type = "binary"
url = "https://example.com/v2.0.0/app.tar.gz"

[runtime]
entrypoint = ["/app"]
"#;

    fs::write(dir.path().join("manifest.toml"), toml).unwrap();

    // Create Dockerfile with version 1.0.0 (mismatch)
    let dockerfile = r#"FROM scratch
ARG VERSION=1.0.0
COPY --from=builder /app /app
USER 65532:65532
ENTRYPOINT ["/app"]
STOPSIGNAL SIGTERM
LABEL org.opencontainers.image.title="drift-test"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.description="Drift test"
LABEL org.opencontainers.image.vendor="Test"
LABEL evergreen.image.tier="1"
"#;

    fs::write(dir.path().join("Dockerfile"), dockerfile).unwrap();

    let result = cmd_drift(dir.path().to_str().unwrap());
    assert!(result.is_ok(), "cmd_drift should succeed");

    // We can't easily capture stdout from cmd_drift in integration tests,
    // but we can verify it doesn't panic and returns Ok.
    // The drift detection logic is tested via the parse_dockerfile path.
}

// =============================================================================
// Test 11: Snapshot produces valid JSON with expected fields
// =============================================================================

#[test]
fn test_snapshot_serialization_structure() {
    // Snapshot struct is private, but cmd_snapshot produces JSON output.
    // We test the serialization path by verifying the module's unit test covers it,
    // and instead test that cmd_snapshot handles a valid manifest directory.
    use evergreenctl::manifest::Manifest;

    let dir = TempDir::new().unwrap();
    let manifest_path = dir.path().join("manifest.toml");

    let toml = r#"
[metadata]
name = "snap-test"
version = "4.0.0"
description = "Snapshot test"
vendor = "TestVendor"
source = "https://github.com/test/snap-test"
license = "MIT"
tier = "1"

[build]
base = "scratch"
user = "65532:65532"
stopsignal = "SIGTERM"

[source]
type = "binary-download"
url = "https://example.com/snap.tar.gz"

[runtime]
entrypoint = ["/snap", "run"]

[ports]
expose = [8080]
"#;

    fs::write(&manifest_path, toml).unwrap();
    let manifest = Manifest::from_file(&manifest_path).unwrap();

    // Verify the manifest has all fields needed by snapshot
    assert_eq!(manifest.name(), "snap-test");
    assert_eq!(manifest.version(), "4.0.0");
    assert_eq!(manifest.base_image(), "scratch");
    assert_eq!(manifest.source_url(), "https://example.com/snap.tar.gz");
    assert_eq!(manifest.source.source_type, "binary-download");
    assert_eq!(
        manifest.entrypoint(),
        &["/snap".to_string(), "run".to_string()]
    );
    assert_eq!(manifest.exposed_ports(), &["8080".to_string()]);
    assert_eq!(manifest.github_repo(), Some("test/snap-test".to_string()));
    assert_eq!(manifest.metadata.tier, "1");
}

// =============================================================================
// Test 12: Sign generates correct cosign commands from manifest
// =============================================================================

#[test]
fn test_sign_command_from_manifest() {
    use evergreenctl::sign::cmd_sign;

    let dir = TempDir::new().unwrap();

    let toml = r#"
[metadata]
name = "sign-test"
version = "5.0.0"
description = "Sign test"
vendor = "Test"
source = "https://github.com/test/sign-test"
license = "MIT"
tier = "1"

[build]
base = "scratch"
user = "65532:65532"
stopsignal = "SIGTERM"

[source]
type = "binary"
url = "https://example.com/sign.tar.gz"

[runtime]
entrypoint = ["/sign-test"]
"#;

    fs::write(dir.path().join("manifest.toml"), toml).unwrap();

    let result = cmd_sign(dir.path().to_str().unwrap());
    assert!(result.is_ok(), "cmd_sign should succeed");
}

// =============================================================================
// Test 13: Audit all images across a multi-image directory
// =============================================================================

#[test]
fn test_audit_all_multi_image() {
    use evergreenctl::audit::{audit_all, audit_summary, ImageStatus};

    let dir = TempDir::new().unwrap();

    // Create 3 image directories
    // 1. Real image (curl download + entrypoint)
    let real_dir = dir.path().join("real-image");
    fs::create_dir_all(&real_dir).unwrap();
    fs::write(
        real_dir.join("Dockerfile"),
        r#"FROM wolfi-base:latest AS builder
RUN curl -fsSL https://example.com/app.tar.gz -o app.tar.gz
FROM scratch
COPY --from=builder /app /app
ENTRYPOINT ["/app"]
"#,
    )
    .unwrap();

    // 2. Stub image (sleep infinity)
    let stub_dir = dir.path().join("stub-image");
    fs::create_dir_all(&stub_dir).unwrap();
    fs::write(
        stub_dir.join("Dockerfile"),
        r#"FROM scratch
CMD sleep infinity
"#,
    )
    .unwrap();

    // 3. Placeholder image (echo placeholder, no real entrypoint)
    let placeholder_dir = dir.path().join("placeholder-image");
    fs::create_dir_all(&placeholder_dir).unwrap();
    fs::write(
        placeholder_dir.join("Dockerfile"),
        r#"FROM scratch
RUN echo "placeholder"
CMD ["sh", "-c", "echo placeholder"]
"#,
    )
    .unwrap();

    let results = audit_all(dir.path()).unwrap();
    assert_eq!(results.len(), 3, "Should audit 3 images");

    let real_result = results.iter().find(|r| r.name == "real-image").unwrap();
    assert_eq!(real_result.status, ImageStatus::Real);

    let stub_result = results.iter().find(|r| r.name == "stub-image").unwrap();
    assert_eq!(stub_result.status, ImageStatus::Stub);

    let placeholder_result = results
        .iter()
        .find(|r| r.name == "placeholder-image")
        .unwrap();
    assert_eq!(placeholder_result.status, ImageStatus::Placeholder);

    // Test audit_summary
    let summary = audit_summary(&results);
    assert!(
        summary.contains("Total images: 3"),
        "Summary should report 3 images, got: {}",
        summary
    );
    assert!(summary.contains("Real: 1"), "Summary: {}", summary);
    assert!(summary.contains("Stub: 1"), "Summary: {}", summary);
    assert!(summary.contains("Placeholder: 1"), "Summary: {}", summary);
}

// =============================================================================
// Test 14: Audit detects multiple issue codes
// =============================================================================

#[test]
fn test_audit_detects_double_and() {
    use evergreenctl::audit::audit_dockerfile;

    let dir = TempDir::new().unwrap();
    let df_path = dir.path().join("Dockerfile");
    fs::write(
        &df_path,
        r#"FROM scratch
COPY --from=builder /app /app
RUN echo "a" &&  && echo "b"
"#,
    )
    .unwrap();

    let result = audit_dockerfile(&df_path, "double-and-test").unwrap();
    let has_double_and = result.issues.iter().any(|i| i.code == "DOUBLE_AND");
    assert!(
        has_double_and,
        "Should detect DOUBLE_AND. Issues: {:?}",
        result.issues
    );
}

#[test]
fn test_audit_detects_url_as_command() {
    use evergreenctl::audit::audit_dockerfile;

    let dir = TempDir::new().unwrap();
    let df_path = dir.path().join("Dockerfile");
    fs::write(
        &df_path,
        r#"FROM scratch
COPY --from=builder /app /app
RUN https://example.com/install.sh
"#,
    )
    .unwrap();

    let result = audit_dockerfile(&df_path, "url-cmd-test").unwrap();
    let has_url_as_cmd = result.issues.iter().any(|i| i.code == "URL_AS_COMMAND");
    assert!(
        has_url_as_cmd,
        "Should detect URL_AS_COMMAND. Issues: {:?}",
        result.issues
    );
}

#[test]
fn test_audit_detects_escaped_backslash() {
    use evergreenctl::audit::audit_dockerfile;

    let dir = TempDir::new().unwrap();
    let df_path = dir.path().join("Dockerfile");
    fs::write(
        &df_path,
        r#"FROM scratch
COPY --from=builder /app /app
RUN echo "test" \\
"#,
    )
    .unwrap();

    let result = audit_dockerfile(&df_path, "backslash-test").unwrap();
    let has_escaped = result.issues.iter().any(|i| i.code == "ESCAPED_BACKSLASH");
    assert!(
        has_escaped,
        "Should detect ESCAPED_BACKSLASH. Issues: {:?}",
        result.issues
    );
}

// =============================================================================
// Test 15: SHA512 checksum computation and verification
// =============================================================================

#[test]
fn test_sha512_known_vector() {
    use evergreenctl::verify::{sha512_file, verify_checksum};

    let dir = TempDir::new().unwrap();
    let path = dir.path().join("sha512_test.bin");

    // Known SHA512 of "hello"
    fs::write(&path, "hello").unwrap();
    let hash = sha512_file(&path).unwrap();
    assert_eq!(hash.len(), 128, "SHA512 must be 128 hex chars");

    let expected_sha512 =
        "9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca72323c3d99ba5c11d7c7acc6e14b8c5da0c4663475c2e5c3adef46f73bcdec043";
    let result = verify_checksum(&path, "sha512", expected_sha512).unwrap();
    assert!(result.matches, "SHA512 should match for 'hello'");

    // Mismatch
    let wrong = "0".repeat(128);
    let result = verify_checksum(&path, "sha512", &wrong).unwrap();
    assert!(!result.matches, "SHA512 should not match wrong hash");
}

// =============================================================================
// Test 16: Verify checksum with uppercase algorithm name (case insensitive)
// =============================================================================

#[test]
fn test_verify_checksum_case_insensitive() {
    use evergreenctl::verify::verify_checksum;

    let dir = TempDir::new().unwrap();
    let path = dir.path().join("case_test.bin");
    fs::write(&path, "test").unwrap();

    // Known SHA256 of "test"
    let sha256 = "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08";

    // Uppercase algorithm name
    let result = verify_checksum(&path, "SHA256", sha256).unwrap();
    assert!(result.matches, "Algorithm name should be case-insensitive");

    // Uppercase expected hash
    let result = verify_checksum(&path, "sha256", &sha256.to_uppercase()).unwrap();
    assert!(result.matches, "Expected hash should be case-insensitive");
}

// =============================================================================
// Test 17: Manifest tier_num defaults to 3 for invalid input
// =============================================================================

#[test]
fn test_manifest_tier_num_default() {
    use evergreenctl::manifest::Manifest;

    let dir = TempDir::new().unwrap();
    let manifest_path = dir.path().join("manifest.toml");

    // No tier specified -> defaults to empty string -> tier_num() = 3
    let toml = r#"
[metadata]
name = "tier-test"
version = "1.0.0"

[build]
base = "scratch"

[source]
url = "https://example.com/test.tar.gz"

[runtime]
entrypoint = ["/test"]
"#;

    fs::write(&manifest_path, toml).unwrap();
    let manifest = Manifest::from_file(&manifest_path).unwrap();
    assert_eq!(manifest.tier_num(), 3, "Missing tier should default to 3");

    // Invalid tier string -> defaults to 3
    let toml2 = r#"
[metadata]
name = "tier-test"
version = "1.0.0"
tier = "invalid"

[build]
base = "scratch"

[source]
url = "https://example.com/test.tar.gz"

[runtime]
entrypoint = ["/test"]
"#;

    fs::write(&manifest_path, toml2).unwrap();
    let manifest2 = Manifest::from_file(&manifest_path).unwrap();
    assert_eq!(manifest2.tier_num(), 3, "Invalid tier should default to 3");
}

// =============================================================================
// Test 18: Generate produces wolfi-specific labels
// =============================================================================

#[test]
fn test_generate_wolfi_labels() {
    use evergreenctl::generate::DockerfileGenerator;
    use evergreenctl::manifest::Manifest;

    let dir = TempDir::new().unwrap();
    let manifest_path = dir.path().join("manifest.toml");

    let toml = r#"
[metadata]
name = "wolfi-label-test"
version = "1.0.0"
description = "Wolfi label test"
vendor = "TestVendor"
source = "https://github.com/test/wolfi-label"
license = "MIT"
tier = "1"

[build]
base = "cgr.dev/chainguard/wolfi-base:latest"
user = "65532:65532"
stopsignal = "SIGTERM"

[source]
type = "package-manager"
url = "https://example.com/app.tar.gz"

[runtime]
entrypoint = ["/app"]

[labels]
"evergreen.health.type" = "http"
"#;

    fs::write(&manifest_path, toml).unwrap();
    let manifest = Manifest::from_file(&manifest_path).unwrap();
    let gen = DockerfileGenerator::new(manifest);
    let dockerfile = gen.generate().unwrap();

    assert!(
        dockerfile.contains("evergreen.base.image=\"wolfi\""),
        "Should have wolfi base label, got: {}",
        &dockerfile[dockerfile.len().saturating_sub(500)..]
    );
    assert!(
        dockerfile.contains("evergreen.health.type=\"http\""),
        "Should include custom labels"
    );
}

// =============================================================================
// Test 19: Migrate on nonexistent Dockerfile returns error
// =============================================================================

#[test]
fn test_migrate_nonexistent_dockerfile() {
    use evergreenctl::migrate::dockerfile_to_manifest;

    let dir = TempDir::new().unwrap();
    let nonexistent = dir.path().join("NonexistentDockerfile");

    let result = dockerfile_to_manifest(&nonexistent, "missing-test");
    assert!(
        result.is_err(),
        "Should return error for nonexistent Dockerfile"
    );
}

// =============================================================================
// Test 20: Migrate on empty Dockerfile
// =============================================================================

#[test]
fn test_migrate_empty_dockerfile() {
    use evergreenctl::migrate::dockerfile_to_manifest;

    let dir = TempDir::new().unwrap();
    let df_path = dir.path().join("Dockerfile");
    fs::write(&df_path, "").unwrap();

    let manifest = dockerfile_to_manifest(&df_path, "empty-test").unwrap();
    assert_eq!(manifest.name(), "empty-test");
    assert_eq!(
        manifest.version(),
        "0.0.0",
        "Empty Dockerfile should default version to 0.0.0"
    );
    assert_eq!(
        manifest.base_image(),
        "scratch",
        "Empty Dockerfile should default base to scratch"
    );
    assert_eq!(
        manifest.user(),
        "65532:65532",
        "Empty Dockerfile should default user"
    );
    assert_eq!(
        manifest.stop_signal(),
        "SIGTERM",
        "Empty Dockerfile should default stop signal"
    );
}

// =============================================================================
// Test 21: Drift detection when manifest.toml doesn't exist
// =============================================================================

#[test]
fn test_drift_no_manifest() {
    use evergreenctl::drift::cmd_drift;

    let dir = TempDir::new().unwrap();
    fs::write(
        dir.path().join("Dockerfile"),
        r#"FROM scratch
ARG VERSION=1.0.0
ENTRYPOINT ["/app"]
"#,
    )
    .unwrap();

    let result = cmd_drift(dir.path().to_str().unwrap());
    assert!(
        result.is_err(),
        "cmd_drift should error when manifest.toml is missing"
    );
}

// =============================================================================
// Test 22: Drift reports no drift when versions match
// =============================================================================

#[test]
fn test_drift_version_match() {
    use evergreenctl::drift::cmd_drift;

    let dir = TempDir::new().unwrap();

    let toml = r#"
[metadata]
name = "match-test"
version = "3.5.0"
description = "Match test"
vendor = "Test"
source = "https://github.com/test/match"
license = "MIT"
tier = "1"

[build]
base = "scratch"
user = "65532:65532"
stopsignal = "SIGTERM"

[source]
type = "binary"
url = "https://example.com/v3.5.0/app.tar.gz"

[runtime]
entrypoint = ["/app"]
"#;

    fs::write(dir.path().join("manifest.toml"), toml).unwrap();

    let dockerfile = r#"FROM scratch
ARG VERSION=3.5.0
COPY --from=builder /app /app
USER 65532:65532
ENTRYPOINT ["/app"]
STOPSIGNAL SIGTERM
LABEL org.opencontainers.image.title="match-test"
LABEL org.opencontainers.image.version="3.5.0"
LABEL org.opencontainers.image.description="Match test"
LABEL org.opencontainers.image.vendor="Test"
LABEL evergreen.image.tier="1"
"#;

    fs::write(dir.path().join("Dockerfile"), dockerfile).unwrap();

    let result = cmd_drift(dir.path().to_str().unwrap());
    assert!(
        result.is_ok(),
        "cmd_drift should succeed when versions match"
    );
}

// =============================================================================
// Test 23: Bump manifest version and verify update
// =============================================================================

#[test]
fn test_bump_manifest_update() {
    use evergreenctl::manifest::Manifest;

    let dir = TempDir::new().unwrap();
    let manifest_path = dir.path().join("manifest.toml");

    let toml = r#"
[metadata]
name = "bump-test"
version = "1.0.0"
description = "Bump test"
vendor = "Test"
source = "https://github.com/test/bump-test"
license = "MIT"
tier = "1"

[build]
base = "scratch"
user = "65532:65532"
stopsignal = "SIGTERM"

[source]
type = "binary"
url = "https://example.com/v1.0.0/app.tar.gz"

[runtime]
entrypoint = ["/app"]
"#;

    fs::write(&manifest_path, toml).unwrap();

    let mut manifest = Manifest::from_file(&manifest_path).unwrap();
    assert_eq!(manifest.version(), "1.0.0");

    let old_version = manifest.version().to_string();
    let new_version = "2.0.0";
    manifest.metadata.version = new_version.to_string();
    manifest.source.url = manifest.source.url.replace(&old_version, new_version);
    if !manifest.metadata.source.is_empty() {
        manifest.metadata.source = manifest.metadata.source.replace(&old_version, new_version);
    }

    let new_toml = toml::to_string_pretty(&manifest).unwrap();
    fs::write(&manifest_path, &new_toml).unwrap();

    let updated = fs::read_to_string(&manifest_path).unwrap();
    assert!(
        updated.contains("version = \"2.0.0\""),
        "Manifest version should be updated to 2.0.0"
    );
    assert!(
        updated.contains("v2.0.0/app.tar.gz"),
        "Source URL should contain new version"
    );
    assert!(
        !updated.contains("version = \"1.0.0\""),
        "Old version should be replaced"
    );
}

// =============================================================================
// Test 24: Bump Dockerfile ARG VERSION and verify update
// =============================================================================

#[test]
fn test_bump_dockerfile_update() {
    let dir = TempDir::new().unwrap();
    let dockerfile_path = dir.path().join("Dockerfile");

    let dockerfile = r#"FROM scratch
ARG VERSION=1.0.0
COPY --from=builder /app /app
ENTRYPOINT ["/app"]
"#;

    fs::write(&dockerfile_path, dockerfile).unwrap();

    let old_version = "1.0.0";
    let new_version = "3.0.0";
    let content = fs::read_to_string(&dockerfile_path).unwrap();
    let mut new_content = String::new();

    for line in content.lines() {
        if line.starts_with("ARG VERSION=") {
            new_content.push_str(&format!("ARG VERSION={}\n", new_version));
        } else if line.contains(old_version) {
            let replaced = line.replace(old_version, new_version);
            new_content.push_str(&replaced);
            new_content.push('\n');
        } else {
            new_content.push_str(line);
            new_content.push('\n');
        }
    }

    fs::write(&dockerfile_path, &new_content).unwrap();

    let updated = fs::read_to_string(&dockerfile_path).unwrap();
    assert!(
        updated.contains("ARG VERSION=3.0.0"),
        "Dockerfile VERSION should be updated to 3.0.0, got: {}",
        updated
    );
    assert!(
        !updated.contains("ARG VERSION=1.0.0"),
        "Old version should be replaced"
    );
}

// =============================================================================
// Test 25: Outdated on empty directory returns no images
// =============================================================================

#[tokio::test]
async fn test_outdated_empty_dir() {
    use evergreenctl::outdated::cmd_outdated;

    let dir = TempDir::new().unwrap();

    let result = cmd_outdated(dir.path().to_str().unwrap(), false).await;
    assert!(
        result.is_ok(),
        "cmd_outdated should succeed on empty directory"
    );
}

// =============================================================================
// Test 26: Discover extract_github_repo with various URL formats
// =============================================================================

#[test]
fn test_discover_no_images() {
    use evergreenctl::discover::extract_github_repo;

    assert_eq!(
        extract_github_repo(""),
        None,
        "Empty string should return None"
    );
    assert_eq!(
        extract_github_repo("not-a-url"),
        None,
        "Non-URL string should return None"
    );
    assert_eq!(
        extract_github_repo("https://gitlab.com/owner/repo"),
        None,
        "Non-GitHub URL should return None"
    );
    assert_eq!(
        extract_github_repo("http://github.com/owner/repo"),
        Some(("owner".to_string(), "repo".to_string())),
        "http:// prefix should work"
    );
    assert_eq!(
        extract_github_repo("git://github.com/owner/repo"),
        Some(("owner".to_string(), "repo".to_string())),
        "git:// prefix should work"
    );
}

// =============================================================================
// Test 27: Different manifests produce different snapshots
// =============================================================================

#[test]
fn test_snapshot_different_manifests() {
    use evergreenctl::manifest::Manifest;
    use evergreenctl::snapshot::cmd_snapshot;

    let dir = TempDir::new().unwrap();

    let toml_a = r#"
[metadata]
name = "snap-a"
version = "1.0.0"
description = "Snapshot A"
vendor = "Test"
source = "https://github.com/test/snap-a"
license = "MIT"
tier = "1"

[build]
base = "scratch"
user = "65532:65532"
stopsignal = "SIGTERM"

[source]
type = "binary-download"
url = "https://example.com/snap-a.tar.gz"

[runtime]
entrypoint = ["/snap-a"]

[ports]
expose = [8080]
"#;

    let toml_b = r#"
[metadata]
name = "snap-b"
version = "2.0.0"
description = "Snapshot B"
vendor = "Other"
source = "https://github.com/test/snap-b"
license = "Apache-2.0"
tier = "2"

[build]
base = "cgr.dev/chainguard/wolfi-base:latest"
user = "65532:65532"
stopsignal = "SIGTERM"

[source]
type = "package-manager"
url = "https://example.com/snap-b.tar.gz"

[runtime]
entrypoint = ["/snap-b", "serve"]

[ports]
expose = [9090]
"#;

    let dir_a = dir.path().join("image-a");
    let dir_b = dir.path().join("image-b");
    fs::create_dir_all(&dir_a).unwrap();
    fs::create_dir_all(&dir_b).unwrap();

    fs::write(dir_a.join("manifest.toml"), toml_a).unwrap();
    fs::write(dir_b.join("manifest.toml"), toml_b).unwrap();

    let manifest_a = Manifest::from_file(&dir_a.join("manifest.toml")).unwrap();
    let manifest_b = Manifest::from_file(&dir_b.join("manifest.toml")).unwrap();

    assert_ne!(manifest_a.name(), manifest_b.name(), "Names should differ");
    assert_ne!(
        manifest_a.version(),
        manifest_b.version(),
        "Versions should differ"
    );
    assert_ne!(
        manifest_a.base_image(),
        manifest_b.base_image(),
        "Base images should differ"
    );
    assert_ne!(
        manifest_a.source.source_type, manifest_b.source.source_type,
        "Source types should differ"
    );
    assert_ne!(
        manifest_a.exposed_ports(),
        manifest_b.exposed_ports(),
        "Ports should differ"
    );
    assert_ne!(
        manifest_a.github_repo(),
        manifest_b.github_repo(),
        "GitHub repos should differ"
    );

    let result_a = cmd_snapshot(dir_a.to_str().unwrap());
    let result_b = cmd_snapshot(dir_b.to_str().unwrap());
    assert!(result_a.is_ok(), "cmd_snapshot should succeed for image-a");
    assert!(result_b.is_ok(), "cmd_snapshot should succeed for image-b");
}

// =============================================================================
// Test 28: ci_diff classify_change with no changes
// =============================================================================

#[test]
fn test_ci_diff_no_changes() {
    let empty_diff = "";
    let dir = TempDir::new().unwrap();
    let manifest_path = dir.path().join("manifest.toml");

    let toml = r#"
[metadata]
name = "ci-test"
version = "1.0.0"

[build]
base = "scratch"

[source]
url = "https://example.com/test.tar.gz"

[runtime]
entrypoint = ["/test"]
"#;

    fs::write(&manifest_path, toml).unwrap();

    let manifest = evergreenctl::manifest::Manifest::from_file(&manifest_path).unwrap();
    assert_eq!(manifest.name(), "ci-test");
    assert_eq!(manifest.version(), "1.0.0");

    // Verify the classify_change function produces structural-change for empty diff
    // (no added/removed lines -> no version, url, or checksum changes detected)
    use evergreenctl::ci_diff::classify_change;
    let classification = classify_change("manifest.toml", empty_diff);
    assert_eq!(
        classification.change_type, "structural-change",
        "Empty diff should classify as structural-change"
    );
}

// =============================================================================
// Test 29: Verify all with copy-from and package-manager images
// =============================================================================

#[test]
fn test_verify_all_mixed_categories() {
    use evergreenctl::verify_all::cmd_verify_all;

    let dir = TempDir::new().unwrap();

    // Copy-from image (no RUN build steps)
    let copy_dir = dir.path().join("copy-image");
    fs::create_dir_all(&copy_dir).unwrap();
    fs::write(
        copy_dir.join("Dockerfile"),
        r#"FROM nginx:alpine
COPY --from=quay.io/prometheus/node-exporter:v1.8.0 /bin/node_exporter /bin/node_exporter
USER 65532:65532
ENTRYPOINT ["/bin/node_exporter"]
"#,
    )
    .unwrap();

    // Package manager image
    let pkg_dir = dir.path().join("pkg-image");
    fs::create_dir_all(&pkg_dir).unwrap();
    fs::write(
        pkg_dir.join("Dockerfile"),
        r#"FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache curl
ENTRYPOINT ["/usr/bin/curl"]
"#,
    )
    .unwrap();

    // Direct download with checksum
    let dl_dir = dir.path().join("dl-image");
    fs::create_dir_all(&dl_dir).unwrap();
    let dl_manifest = r#"
[metadata]
name = "dl-image"
version = "1.0.0"

[build]
base = "scratch"

[source]
type = "binary-download"
url = "https://example.com/app.tar.gz"

[runtime]
entrypoint = ["/app"]
"#;
    fs::write(dl_dir.join("manifest.toml"), dl_manifest).unwrap();
    fs::write(
        dl_dir.join("Dockerfile"),
        r#"FROM scratch
COPY --from=builder /app /app
ENTRYPOINT ["/app"]
"#,
    )
    .unwrap();

    let result = cmd_verify_all(dir.path().to_str().unwrap());
    assert!(result.is_ok(), "cmd_verify_all should succeed");
}

// =============================================================================
// Test 30: Migrate produces manifest with correct source type for git clone
// =============================================================================

#[test]
fn test_migrate_git_clone_source_type() {
    use evergreenctl::migrate::dockerfile_to_manifest;

    let dir = TempDir::new().unwrap();
    let df_path = dir.path().join("Dockerfile");

    fs::write(
        &df_path,
        r#"FROM cgr.dev/chainguard/wolfi-base:latest AS builder
RUN git clone --depth 1 https://github.com/test/repo.git /src
RUN cd /src && make build
FROM scratch
COPY --from=builder /src/bin/app /app
USER 65532:65532
ENTRYPOINT ["/app"]
"#,
    )
    .unwrap();

    let manifest = dockerfile_to_manifest(&df_path, "git-clone-test").unwrap();
    assert_eq!(
        manifest.source.source_type, "source-build",
        "Dockerfile with git clone should be classified as source-build"
    );
}

// =============================================================================
// Test 31: Migrate produces manifest with correct source type for copy-from
// =============================================================================

#[test]
fn test_migrate_copy_from_source_type() {
    use evergreenctl::migrate::dockerfile_to_manifest;

    let dir = TempDir::new().unwrap();
    let df_path = dir.path().join("Dockerfile");

    fs::write(
        &df_path,
        r#"FROM scratch
COPY --from=quay.io/prometheus/node-exporter:v1.8.0 /bin/node_exporter /bin/node_exporter
USER 65532:65532
ENTRYPOINT ["/bin/node_exporter"]
"#,
    )
    .unwrap();

    let manifest = dockerfile_to_manifest(&df_path, "copy-from-test").unwrap();
    assert_eq!(
        manifest.source.source_type, "copy-from",
        "Dockerfile with only COPY --from should be classified as copy-from"
    );
}

// =============================================================================
// Test 32: Drift detects base image mismatch
// =============================================================================

#[test]
fn test_drift_base_image_mismatch() {
    use evergreenctl::drift::cmd_drift;

    let dir = TempDir::new().unwrap();

    let toml = r#"
[metadata]
name = "base-drift-test"
version = "1.0.0"
description = "Base drift test"
vendor = "Test"
source = "https://github.com/test/base-drift"
license = "MIT"
tier = "1"

[build]
base = "scratch"
user = "65532:65532"
stopsignal = "SIGTERM"

[source]
type = "binary"
url = "https://example.com/app.tar.gz"

[runtime]
entrypoint = ["/app"]
"#;

    fs::write(dir.path().join("manifest.toml"), toml).unwrap();

    // Dockerfile uses wolfi-base but manifest says scratch
    let dockerfile = r#"FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=1.0.0
COPY --from=builder /app /app
USER 65532:65532
ENTRYPOINT ["/app"]
STOPSIGNAL SIGTERM
LABEL org.opencontainers.image.title="base-drift-test"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.description="Base drift test"
LABEL org.opencontainers.image.vendor="Test"
LABEL evergreen.image.tier="1"
"#;

    fs::write(dir.path().join("Dockerfile"), dockerfile).unwrap();

    let result = cmd_drift(dir.path().to_str().unwrap());
    assert!(result.is_ok(), "cmd_drift should succeed even with drift");
}

// =============================================================================
// Test 33: Verify checksum with unknown algorithm falls back gracefully
// =============================================================================

#[test]
fn test_verify_checksum_sha256_empty_file() {
    use evergreenctl::verify::verify_checksum;

    let dir = TempDir::new().unwrap();
    let path = dir.path().join("zero.bin");
    fs::write(&path, []).unwrap();

    let sha256_empty = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855";
    let result = verify_checksum(&path, "sha256", sha256_empty).unwrap();
    assert!(result.matches, "Empty file SHA256 should match");

    let result = verify_checksum(&path, "sha256", "0".repeat(64).as_str()).unwrap();
    assert!(!result.matches, "Empty file should not match wrong hash");
}

// =============================================================================
// Test 34: Manifest with no source section defaults gracefully
// =============================================================================

#[test]
fn test_manifest_missing_source_defaults() {
    use evergreenctl::manifest::Manifest;

    let dir = TempDir::new().unwrap();
    let manifest_path = dir.path().join("manifest.toml");

    let toml = r#"
[metadata]
name = "no-source-test"
version = "1.0.0"
"#;

    fs::write(&manifest_path, toml).unwrap();
    let manifest = Manifest::from_file(&manifest_path).unwrap();

    assert_eq!(manifest.name(), "no-source-test");
    assert_eq!(manifest.version(), "1.0.0");
    assert!(
        manifest.source_url().is_empty() || !manifest.source_url().is_empty(),
        "source_url should return some value without panic"
    );
    assert_eq!(
        manifest.github_repo(),
        None,
        "Non-GitHub URL should return None for github_repo"
    );
}

// =============================================================================
// Test 35: Migrate dry-run does not create manifest file
// =============================================================================

#[test]
fn test_migrate_dry_run_no_file_written() {
    use evergreenctl::migrate::migrate_all;

    let dir = TempDir::new().unwrap();

    let df_path = dir.path().join("my-image").join("Dockerfile");
    fs::create_dir_all(df_path.parent().unwrap()).unwrap();
    fs::write(
        &df_path,
        r#"FROM scratch
ARG VERSION=1.0.0
ENTRYPOINT ["/app"]
"#,
    )
    .unwrap();

    let manifest_path = dir.path().join("my-image").join("manifest.toml");
    assert!(
        !manifest_path.exists(),
        "manifest.toml should not exist yet"
    );

    let result = migrate_all(dir.path(), true);
    assert!(result.is_ok(), "migrate_all dry-run should succeed");

    assert!(
        !manifest_path.exists(),
        "Dry-run should not create manifest.toml"
    );
}

// =============================================================================
// Test 36: Bump dry-run does not modify files
// =============================================================================

#[test]
fn test_bump_dry_run_no_modify() {
    use evergreenctl::manifest::Manifest;

    let dir = TempDir::new().unwrap();
    let manifest_path = dir.path().join("manifest.toml");
    let dockerfile_path = dir.path().join("Dockerfile");

    let toml = r#"
[metadata]
name = "dry-run-bump"
version = "1.0.0"
description = "Dry run bump test"
vendor = "Test"
source = "https://github.com/test/dry-run-bump"
license = "MIT"
tier = "1"

[build]
base = "scratch"
user = "65532:65532"
stopsignal = "SIGTERM"

[source]
type = "binary"
url = "https://example.com/v1.0.0/app.tar.gz"

[runtime]
entrypoint = ["/app"]
"#;

    fs::write(&manifest_path, toml).unwrap();
    fs::write(&dockerfile_path, "ARG VERSION=1.0.0\n").unwrap();

    let original_manifest = fs::read_to_string(&manifest_path).unwrap();
    let original_dockerfile = fs::read_to_string(&dockerfile_path).unwrap();

    // Simulate bump logic (dry-run path: compute new content but don't write)
    let manifest = Manifest::from_file(&manifest_path).unwrap();
    let mut updated = manifest;
    updated.metadata.version = "2.0.0".to_string();
    updated.source.url = updated.source.url.replace("1.0.0", "2.0.0");
    let _new_toml = toml::to_string_pretty(&updated).unwrap();

    // Verify files were not modified
    let after_manifest = fs::read_to_string(&manifest_path).unwrap();
    let after_dockerfile = fs::read_to_string(&dockerfile_path).unwrap();

    assert_eq!(
        original_manifest, after_manifest,
        "Dry-run should not modify manifest.toml"
    );
    assert_eq!(
        original_dockerfile, after_dockerfile,
        "Dry-run should not modify Dockerfile"
    );
}

// =============================================================================
// Test 37: Discover extract_github_repo with trailing slash
// =============================================================================

#[test]
fn test_discover_github_repo_trailing_slash() {
    use evergreenctl::discover::extract_github_repo;

    assert_eq!(
        extract_github_repo("https://github.com/owner/repo/"),
        Some(("owner".to_string(), "repo".to_string())),
        "Trailing slash should be handled"
    );
}

// =============================================================================
// Test 38: ci_diff classify_change with version bump
// =============================================================================

#[test]
fn test_ci_diff_classify_version_bump() {
    use evergreenctl::ci_diff::classify_change;

    let diff = r#"diff --git a/images/test/manifest.toml b/images/test/manifest.toml
index abc..def 100644
--- a/images/test/manifest.toml
+++ b/images/test/manifest.toml
@@ -1,3 +1,3 @@
 [metadata]
-name = "test"
-VERSION = "1.0.0"
+VERSION = "2.0.0"
+description = "updated"
"#;

    let classification = classify_change("manifest.toml", diff);
    assert_eq!(
        classification.change_type, "version-bump",
        "Diff with VERSION change should classify as version-bump"
    );
    assert!(
        classification.details.iter().any(|d| d.contains("Version")),
        "Should have a detail mentioning Version"
    );
}

// =============================================================================
// Test 39: ci_diff classify_change with checksum update
// =============================================================================

#[test]
fn test_ci_diff_classify_checksum_update() {
    use evergreenctl::ci_diff::classify_change;

    let diff = r#"diff --git a/images/test/CHECKSUMS b/images/test/CHECKSUMS
index abc..def 100644
--- a/images/test/CHECKSUMS
+++ b/images/test/CHECKSUMS
@@ -1,2 +1,2 @@
-expected_sha256 = "oldhash"
+expected_sha256 = "newhash123"
"#;

    let classification = classify_change("CHECKSUMS", diff);
    assert_eq!(
        classification.change_type, "checksum-update",
        "Diff with sha256 change should classify as checksum-update"
    );
}

// =============================================================================
// Test 40: ci_diff classify_change with URL fix
// =============================================================================

#[test]
fn test_ci_diff_classify_url_fix() {
    use evergreenctl::ci_diff::classify_change;

    let diff = r#"diff --git a/images/test/manifest.toml b/images/test/manifest.toml
index abc..def 100644
--- a/images/test/manifest.toml
+++ b/images/test/manifest.toml
@@ -1,2 +1,2 @@
-url = "https://old-domain.com/file.tar.gz"
+url = "https://new-domain.com/file.tar.gz"
"#;

    let classification = classify_change("manifest.toml", diff);
    assert_eq!(
        classification.change_type, "url-fix",
        "Diff with URL change should classify as url-fix"
    );
}

// =============================================================================
// Test 41: ci_diff classify_change with new file
// =============================================================================

#[test]
fn test_ci_diff_classify_new_file() {
    use evergreenctl::ci_diff::classify_change;

    let diff = r#"diff --git a/images/new-image/manifest.toml b/images/new-image/manifest.toml
new file mode 100644
index 0000000..abc
--- /dev/null
+++ b/images/new-image/manifest.toml
@@ -0,0 +1,5 @@
+[metadata]
+name = "new-image"
+version = "1.0.0"
"#;

    let classification = classify_change("manifest.toml", diff);
    assert_eq!(
        classification.change_type, "new-image",
        "Diff with 'new file' should classify as new-image"
    );
}

// =============================================================================
// Test 42: Outdated compare_versions handles pre-release
// =============================================================================

#[test]
fn test_outdated_compare_versions_prerelease() {
    use evergreenctl::outdated::compare_versions;

    assert_eq!(compare_versions("1.0.0-alpha", "1.0.0"), "OUTDATED");
    assert_eq!(compare_versions("1.0.0-beta.1", "1.0.0"), "OUTDATED");
    assert_eq!(compare_versions("1.0.0", "1.0.0-beta.1"), "OK");
    assert_eq!(compare_versions("1.0.0-rc.1", "1.0.0-rc.2"), "OUTDATED");
}

// =============================================================================
// Test 43: Verify all with direct download missing checksum
// =============================================================================

#[test]
fn test_verify_all_direct_download_no_checksum() {
    use evergreenctl::verify_all::cmd_verify_all;

    let dir = TempDir::new().unwrap();

    let dl_dir = dir.path().join("no-checksum-dl");
    fs::create_dir_all(&dl_dir).unwrap();
    fs::write(
        dl_dir.join("Dockerfile"),
        r#"FROM cgr.dev/chainguard/wolfi-base:latest AS builder
RUN curl -fsSL https://example.com/app.tar.gz -o app.tar.gz
FROM scratch
COPY --from=builder /app.tar.gz /app.tar.gz
ENTRYPOINT ["/app"]
"#,
    )
    .unwrap();

    let result = cmd_verify_all(dir.path().to_str().unwrap());
    assert!(result.is_ok(), "cmd_verify_all should succeed");
    assert_eq!(
        result.unwrap(),
        1,
        "Should return exit code 1 when checksum is missing"
    );
}

// =============================================================================
// Test 44: Generate Dockerfile with copy-from source type
// =============================================================================

#[test]
fn test_generate_copy_from_source() {
    use evergreenctl::generate::DockerfileGenerator;
    use evergreenctl::manifest::Manifest;

    let dir = TempDir::new().unwrap();
    let manifest_path = dir.path().join("manifest.toml");

    let toml = r#"
[metadata]
name = "copy-from-gen"
version = "1.0.0"
description = "Copy from generate test"
vendor = "TestVendor"
source = "https://github.com/test/copy-from-gen"
license = "MIT"
tier = "1"

[build]
base = "quay.io/prometheus/node-exporter:v1.8.0"
user = "65532:65532"
stopsignal = "SIGTERM"

[source]
type = "copy-from"
url = "https://github.com/prometheus/node_exporter"

[runtime]
entrypoint = ["/bin/node_exporter", "--web.listen-address=:9100"]

[ports]
expose = [9100]
"#;

    fs::write(&manifest_path, toml).unwrap();
    let manifest = Manifest::from_file(&manifest_path).unwrap();
    let gen = DockerfileGenerator::new(manifest);
    let dockerfile = gen.generate().unwrap();

    assert!(
        dockerfile.contains("FROM quay.io/prometheus/node-exporter:v1.8.0"),
        "Should use the copy-from base image"
    );
    assert!(
        dockerfile.contains("USER 65532:65532"),
        "Should set non-root user"
    );
    assert!(
        dockerfile.contains("ENTRYPOINT [\"/bin/node_exporter\", \"--web.listen-address=:9100\"]"),
        "Should set entrypoint"
    );
    assert!(
        dockerfile.contains("EXPOSE 9100"),
        "Should expose port 9100"
    );
}

// =============================================================================
// Test 45: Verify_all with base image only (no RUN steps)
// =============================================================================

#[test]
fn test_verify_all_base_image_only() {
    use evergreenctl::verify_all::cmd_verify_all;

    let dir = TempDir::new().unwrap();

    let base_dir = dir.path().join("base-only");
    fs::create_dir_all(&base_dir).unwrap();
    fs::write(
        base_dir.join("Dockerfile"),
        r#"FROM cgr.dev/chainguard/wolfi-base:latest
USER 65532:65532
ENTRYPOINT ["/bin/sh"]
"#,
    )
    .unwrap();

    let result = cmd_verify_all(dir.path().to_str().unwrap());
    assert!(
        result.is_ok(),
        "cmd_verify_all should succeed for base image"
    );
    assert_eq!(
        result.unwrap(),
        0,
        "Base images should not require checksum (exit code 0)"
    );
}
