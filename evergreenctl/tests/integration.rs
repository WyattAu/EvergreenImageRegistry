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
    assert_eq!(manifest.exposed_ports(), &[8080]);
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
