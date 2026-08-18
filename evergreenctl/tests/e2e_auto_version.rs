// =============================================================================
// Evergreenctl - End-to-End Tests for 5k+ Scale Features
// =============================================================================
// Tests the full pipeline: auto-version, registry index, parallel validation.
// Run with: cargo test --test e2e_auto_version
// =============================================================================

use std::fs;
use tempfile::TempDir;

// ---------------------------------------------------------------------------
// Helper: create a realistic image directory
// ---------------------------------------------------------------------------

fn create_test_image(
    tmp: &TempDir,
    name: &str,
    version: &str,
    tier: &str,
    source_type: &str,
    base: &str,
    with_sbom: bool,
) {
    let dir = tmp.path().join(name);
    fs::create_dir_all(&dir).unwrap();

    // Manifest
    let manifest = format!(
        r#"
[metadata]
name = "{name}"
version = "{version}"
description = "Test image {name}"
vendor = "TestVendor"
source = "https://github.com/test/{name}"
license = "MIT"
tier = "{tier}"

[build]
base = "{base}"
user = "65532:65532"
stopsignal = "SIGTERM"

[source]
type = "{source_type}"
url = "https://example.com/{name}-{version}.tar.gz"

[runtime]
entrypoint = ["/{name}"]

[ports]
expose = [8080]
"#,
        name = name,
        version = version,
        tier = tier,
        source_type = source_type,
        base = base,
    );
    fs::write(dir.join("manifest.toml"), manifest).unwrap();

    // Dockerfile
    let df = if base == "scratch" {
        format!(
            r#"FROM {base}@sha256:aaaa1111bbbb2222cccc3333dddd4444eeee5555ffff6666aaaa7777bbbb8888cccc9999
ARG VERSION={version}
COPY --from=builder /usr/local/bin/{name} /{name}
USER 65532:65532
ENTRYPOINT ["/{name}"]
HEALTHCHECK CMD ["/{name}", "health"]
STOPSIGNAL SIGTERM
LABEL org.opencontainers.image.title="{name}"
LABEL org.opencontainers.image.version="{version}"
LABEL org.opencontainers.image.description="Test image {name}"
LABEL evergreen.image.tier="{tier}"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
"#,
            base = base,
            version = version,
            name = name,
            tier = tier,
        )
    } else {
        format!(
            r#"FROM {base}
ARG VERSION={version}
RUN apk add --no-cache {name}
USER 65532:65532
ENTRYPOINT ["/{name}"]
HEALTHCHECK CMD ["/{name}", "health"]
STOPSIGNAL SIGTERM
LABEL org.opencontainers.image.title="{name}"
LABEL org.opencontainers.image.version="{version}"
LABEL org.opencontainers.image.description="Test image {name}"
LABEL evergreen.image.tier="{tier}"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
"#,
            base = base,
            version = version,
            name = name,
            tier = tier,
        )
    };
    fs::write(dir.join("Dockerfile"), df).unwrap();

    // SBOM
    if with_sbom {
        let sbom = serde_json::json!({
            "spdxVersion": "SPDX-2.3",
            "packages": [
                {"name": name, "versionInfo": version},
                {"name": "curl", "versionInfo": "8.0.0"}
            ]
        });
        fs::write(
            dir.join("sbom.spdx.json"),
            serde_json::to_string_pretty(&sbom).unwrap(),
        )
        .unwrap();
    }
}

// ---------------------------------------------------------------------------
// Test 1: SQLite Registry Index — build and query
// ---------------------------------------------------------------------------

#[test]
fn test_e2e_registry_index_build_and_query() {
    let tmp = TempDir::new().unwrap();

    // Create 5 test images across tiers
    create_test_image(&tmp, "redis", "7.4.1", "1", "binary-download", "scratch", true);
    create_test_image(&tmp, "nginx", "1.27.1", "2", "pkg-install", "cgr.dev/chainguard/wolfi-base:latest", true);
    create_test_image(&tmp, "postgres", "16.4", "1", "chainguard-repack", "cgr.dev/chainguard/wolfi-base:latest", true);
    create_test_image(&tmp, "curl", "8.9.0", "3", "pkg-install", "cgr.dev/chainguard/wolfi-base:latest", false);
    create_test_image(&tmp, "old-image", "0.1.0", "3", "binary-download", "scratch", true);

    // Build index
    let db_path = tmp.path().join("test.db");
    let conn = evergreenctl::registry_index::open_index(&db_path).unwrap();
    let indexed = evergreenctl::registry_index::build_index(&conn, tmp.path()).unwrap();
    assert_eq!(indexed, 5, "Should index 5 images");

    // Query stats
    let stats = evergreenctl::registry_index::get_stats(&conn).unwrap();
    assert_eq!(stats.total_images, 5);
    assert_eq!(*stats.by_tier.get("tier1").unwrap_or(&0), 2);
    assert_eq!(*stats.by_tier.get("tier2").unwrap_or(&0), 1);
    assert_eq!(*stats.by_tier.get("tier3").unwrap_or(&0), 2);
    assert_eq!(stats.with_sbom, 4);
    assert_eq!(stats.deprecated_count, 0);

    // Query by tier
    let tier1 = evergreenctl::registry_index::query_by_tier(&conn, 1).unwrap();
    assert_eq!(tier1.len(), 2);
    let names: Vec<&str> = tier1.iter().map(|r| r.name.as_str()).collect();
    assert!(names.contains(&"redis"));
    assert!(names.contains(&"postgres"));

    // Format stats
    let text = evergreenctl::registry_index::format_stats_text(&stats);
    assert!(text.contains("Total images: 5"));
    assert!(text.contains("SBOM Coverage:"));
}

// ---------------------------------------------------------------------------
// Test 2: Parallel Validation — full pipeline
// ---------------------------------------------------------------------------

#[test]
fn test_e2e_parallel_validation() {
    let tmp = TempDir::new().unwrap();

    // Create mix of compliant and non-compliant images
    create_test_image(&tmp, "good-image", "1.0.0", "1", "binary-download", "scratch", true);
    // Create another-good manually with digest-pinned FROM for full compliance
    let good2_dir = tmp.path().join("another-good");
    fs::create_dir_all(&good2_dir).unwrap();
    fs::write(
        good2_dir.join("Dockerfile"),
        "FROM cgr.dev/chainguard/wolfi-base:latest@sha256:bbbb2222cccc3333dddd4444eeee5555ffff6666aaaa7777bbbb8888cccc9999aaaa\nARG VERSION=2.0.0\nRUN apk add --no-cache another-good\nUSER 65532:65532\nENTRYPOINT [\"/another-good\"]\nHEALTHCHECK CMD [\"/another-good\", \"health\"]\nSTOPSIGNAL SIGTERM\nLABEL org.opencontainers.image.title=\"another-good\"\nLABEL org.opencontainers.image.version=\"2.0.0\"\nLABEL evergreen.image.tier=\"2\"\nLABEL evergreen.security.cap-drop=\"ALL\"\nLABEL evergreen.security.no-new-privileges=\"true\"\n",
    )
    .unwrap();
    fs::write(
        good2_dir.join("manifest.toml"),
        "[metadata]\nname = \"another-good\"\nversion = \"2.0.0\"\ntier = \"2\"\n\n[build]\nbase = \"cgr.dev/chainguard/wolfi-base:latest\"\n\n[source]\ntype = \"pkg-install\"\nurl = \"https://example.com/test.tar.gz\"\n\n[runtime]\nentrypoint = [\"/another-good\"]\n",
    )
    .unwrap();
    fs::write(
        good2_dir.join("sbom.spdx.json"),
        serde_json::to_string_pretty(&serde_json::json!({"spdxVersion": "SPDX-2.3", "packages": []})).unwrap(),
    )
    .unwrap();

    // Create a bad image (Alpine base)
    let bad_dir = tmp.path().join("alpine-bad");
    fs::create_dir_all(&bad_dir).unwrap();
    fs::write(
        bad_dir.join("Dockerfile"),
        "FROM alpine:3.19\nRUN apk add curl\nUSER 65532\n",
    )
    .unwrap();
    let bad_manifest = r#"
[metadata]
name = "alpine-bad"
version = "1.0.0"
tier = "2"

[build]
base = "alpine:3.19"

[source]
type = "pkg-install"
url = "https://example.com/test.tar.gz"

[runtime]
entrypoint = ["/app"]
"#;
    fs::write(bad_dir.join("manifest.toml"), bad_manifest).unwrap();

    // Run parallel validation
    let report = evergreenctl::validate_parallel::validate_all_parallel(
        tmp.path().to_str().unwrap(),
    )
    .unwrap();

    assert_eq!(report.total_images, 3);
    assert_eq!(report.images_failed, 1); // alpine-bad should fail
    assert!(report.total_violations > 0);

    // Verify the failure is for the alpine image
    let failed: Vec<&str> = report
        .image_results
        .iter()
        .filter(|r| r.status == evergreenctl::validate_parallel::ImageStatus::Fail)
        .map(|r| r.name.as_str())
        .collect();
    assert!(failed.contains(&"alpine-bad"));

    // Verify C004 (Alpine) is the failure
    let alpine_result = report
        .image_results
        .iter()
        .find(|r| r.name == "alpine-bad")
        .unwrap();
    let c004 = alpine_result
        .violations
        .iter()
        .find(|v| v.code == "C004")
        .unwrap();
    assert_eq!(
        c004.status,
        evergreenctl::validate_parallel::ConstraintStatus::Fail
    );

    // Format report
    let text = evergreenctl::validate_parallel::format_report_text(&report);
    assert!(text.contains("alpine-bad"));
}

// ---------------------------------------------------------------------------
// Test 3: Auto-Version — version comparison end-to-end
// ---------------------------------------------------------------------------

#[test]
fn test_e2e_auto_version_comparison() {
    // Test the full version comparison pipeline
    use evergreenctl::auto_version::is_safe_bump;

    // Patch bump should be safe
    let (safe, reason) = is_safe_bump("1.0.0", "1.0.1", 1);
    assert!(safe, "Patch bump should be safe: {}", reason);

    // Minor bump within limit should be safe
    let (safe, reason) = is_safe_bump("1.0.0", "1.1.0", 1);
    assert!(safe, "Minor bump within limit should be safe: {}", reason);

    // Major bump should be unsafe
    let (safe, reason) = is_safe_bump("1.0.0", "2.0.0", 1);
    assert!(!safe, "Major bump should be unsafe: {}", reason);

    // Minor bump exceeding limit should be unsafe
    let (safe, reason) = is_safe_bump("1.0.0", "1.3.0", 1);
    assert!(!safe, "Minor bump exceeding limit should be unsafe: {}", reason);

    // Same version should be safe (no-op)
    let (safe, _) = is_safe_bump("1.2.3", "1.2.3", 1);
    assert!(safe, "Same version should be safe");

    // V-prefix should be handled
    let (safe, _) = is_safe_bump("v1.0.0", "v1.0.1", 1);
    assert!(safe, "V-prefix should be handled");

    // Backward-compatible (current > latest) should be safe
    let (safe, _) = is_safe_bump("2.0.0", "1.0.0", 1);
    assert!(safe, "Backward-compatible should be safe");
}

// ---------------------------------------------------------------------------
// Test 4: Registry Index — build history tracking
// ---------------------------------------------------------------------------

#[test]
fn test_e2e_registry_index_build_history() {
    let tmp = TempDir::new().unwrap();
    let db_path = tmp.path().join("test.db");
    let conn = evergreenctl::registry_index::open_index(&db_path).unwrap();

    // Insert dummy images first (build_history has FK to images)
    conn.execute(
        "INSERT INTO images (name, version) VALUES ('redis', '1.0.0'), ('nginx', '1.0.0')",
        [],
    )
    .unwrap();

    // Record some build events
    evergreenctl::registry_index::record_build(
        &conn,
        "redis",
        "abc123",
        "def456",
        "pass",
        Some(45000),
        Some(12582912),
        Some(7),
    )
    .unwrap();

    evergreenctl::registry_index::record_build(
        &conn,
        "nginx",
        "ghi789",
        "jkl012",
        "fail",
        Some(30000),
        None,
        None,
    )
    .unwrap();

    // Query build history
    let mut stmt = conn
        .prepare("SELECT image_name, build_status FROM build_history ORDER BY image_name")
        .unwrap();
    let history: Vec<(String, String)> = stmt
        .query_map([], |row| Ok((row.get(0)?, row.get(1)?)))
        .unwrap()
        .collect::<Result<Vec<_>, _>>()
        .unwrap();

    assert_eq!(history.len(), 2);
    assert_eq!(history[0].0, "nginx");
    assert_eq!(history[0].1, "fail");
    assert_eq!(history[1].0, "redis");
    assert_eq!(history[1].1, "pass");
}

// ---------------------------------------------------------------------------
// Test 5: Policy Violations — record and query
// ---------------------------------------------------------------------------

#[test]
fn test_e2e_policy_violations() {
    let tmp = TempDir::new().unwrap();
    let db_path = tmp.path().join("test.db");
    let conn = evergreenctl::registry_index::open_index(&db_path).unwrap();

    // Insert dummy image first (FK constraint)
    conn.execute(
        "INSERT INTO images (name, version) VALUES ('alpine-bad', '1.0.0')",
        [],
    )
    .unwrap();

    // Record violations
    let violations = vec![
        evergreenctl::validate_parallel::ConstraintResult {
            code: "C004".into(),
            severity: evergreenctl::validate_parallel::Severity::Block,
            status: evergreenctl::validate_parallel::ConstraintStatus::Fail,
            message: "Alpine base detected".into(),
            image: "alpine-bad".into(),
        },
        evergreenctl::validate_parallel::ConstraintResult {
            code: "C005".into(),
            severity: evergreenctl::validate_parallel::Severity::Block,
            status: evergreenctl::validate_parallel::ConstraintStatus::Fail,
            message: "No HEALTHCHECK".into(),
            image: "alpine-bad".into(),
        },
    ];

    evergreenctl::registry_index::record_violations(&conn, "alpine-bad", &violations).unwrap();

    // Query violations
    let c004_violations = evergreenctl::registry_index::query_violations(&conn, "C004").unwrap();
    assert_eq!(c004_violations.len(), 1);
    assert_eq!(c004_violations[0].0, "alpine-bad");

    let c005_violations = evergreenctl::registry_index::query_violations(&conn, "C005").unwrap();
    assert_eq!(c005_violations.len(), 1);

    // Record again (should replace old violations)
    let new_violations = vec![evergreenctl::validate_parallel::ConstraintResult {
        code: "C004".into(),
        severity: evergreenctl::validate_parallel::Severity::Block,
        status: evergreenctl::validate_parallel::ConstraintStatus::Fail,
        message: "Alpine base detected (updated)".into(),
        image: "alpine-bad".into(),
    }];

    evergreenctl::registry_index::record_violations(&conn, "alpine-bad", &new_violations).unwrap();

    let c004_after = evergreenctl::registry_index::query_violations(&conn, "C004").unwrap();
    assert_eq!(c004_after.len(), 1, "Should have exactly 1 violation after re-recording");
}

// ---------------------------------------------------------------------------
// Test 6: Manifest round-trip through index
// ---------------------------------------------------------------------------

#[test]
fn test_e2e_manifest_to_index_round_trip() {
    let tmp = TempDir::new().unwrap();

    // Create a realistic image
    create_test_image(&tmp, "roundtrip-test", "3.0.0", "1", "binary-download", "scratch", true);

    // Build index
    let db_path = tmp.path().join("test.db");
    let conn = evergreenctl::registry_index::open_index(&db_path).unwrap();
    evergreenctl::registry_index::build_index(&conn, tmp.path()).unwrap();

    // Query the image
    let tier1 = evergreenctl::registry_index::query_by_tier(&conn, 1).unwrap();
    assert_eq!(tier1.len(), 1);

    let img = &tier1[0];
    assert_eq!(img.name, "roundtrip-test");
    assert_eq!(img.version, "3.0.0");
    assert_eq!(img.source_type, "binary-download");
    assert!(img.has_healthcheck);
    assert!(img.has_sbom);
    assert!(img.has_security_labels);
    assert!(img.digest_pinned);
}
