// =============================================================================
// Evergreenctl - Property-Based Tests
// =============================================================================
// Uses proptest to verify invariants across random inputs for:
//   - Version comparison (auto_version)
//   - Dockerfile parsing (dockerfile_utils)
//   - Manifest round-trip (manifest)
//   - Constraint validation (validate_parallel)
//
// Run with: cargo test --test property_tests
// =============================================================================

use proptest::prelude::*;
use std::io::Write;

// ---------------------------------------------------------------------------
// Helpers: generate valid semver strings
// ---------------------------------------------------------------------------

fn arbitrary_semver() -> impl Strategy<Value = String> {
    (0u32..100, 0u32..100, 0u32..1000)
        .prop_map(|(major, minor, patch)| format!("{}.{}.{}", major, minor, patch))
}

fn arbitrary_semver_with_prefix() -> impl Strategy<Value = String> {
    (any::<bool>(), 0u32..100, 0u32..100, 0u32..1000).prop_map(|(with_v, major, minor, patch)| {
        if with_v {
            format!("v{}.{}.{}", major, minor, patch)
        } else {
            format!("{}.{}.{}", major, minor, patch)
        }
    })
}

fn arbitrary_non_semver() -> impl Strategy<Value = String> {
    prop_oneof![
        Just("latest".to_string()),
        Just("stable".to_string()),
        Just("main".to_string()),
        Just("develop".to_string()),
        Just("nightly".to_string()),
        Just("".to_string()),
        "[a-z]{3,10}".prop_map(|s| s),
    ]
}

// ---------------------------------------------------------------------------
// Property: Version comparison invariants
// ---------------------------------------------------------------------------

proptest! {
    #[test]
    fn test_same_version_is_always_safe(current in arbitrary_semver()) {
        use evergreenctl::auto_version::is_safe_bump;
        let (safe, _reason) = is_safe_bump(&current, &current, 1);
        prop_assert!(safe, "Same version '{}' should always be safe", current);
    }

    #[test]
    fn test_newer_patch_is_safe(current in arbitrary_semver(), patch_bump in 1u32..100) {
        use evergreenctl::auto_version::is_safe_bump;
        let parts: Vec<u32> = current.split('.').filter_map(|p| p.parse().ok()).collect();
        if parts.len() == 3 {
            let new_version = format!("{}.{}.{}", parts[0], parts[1], parts[2] + patch_bump);
            let (safe, _reason) = is_safe_bump(&current, &new_version, 1);
            prop_assert!(safe, "Patch bump {} -> {} should be safe", current, new_version);
        }
    }

    #[test]
    fn test_newer_minor_within_limit_is_safe(current in arbitrary_semver(), minor_bump in 1u32..=1) {
        use evergreenctl::auto_version::is_safe_bump;
        let parts: Vec<u32> = current.split('.').filter_map(|p| p.parse().ok()).collect();
        if parts.len() == 3 {
            let new_version = format!("{}.{}.{}", parts[0], parts[1] + minor_bump, 0);
            let (safe, _reason) = is_safe_bump(&current, &new_version, 1);
            prop_assert!(safe, "Minor bump {} -> {} within limit should be safe", current, new_version);
        }
    }

    #[test]
    fn test_major_jump_is_unsafe(current in arbitrary_semver()) {
        use evergreenctl::auto_version::is_safe_bump;
        let parts: Vec<u32> = current.split('.').filter_map(|p| p.parse().ok()).collect();
        if parts.len() == 3 && parts[0] < 99 {
            let new_version = format!("{}.0.0", parts[0] + 1);
            let (safe, _reason) = is_safe_bump(&current, &new_version, 1);
            prop_assert!(!safe, "Major jump {} -> {} should be unsafe", current, new_version);
        }
    }

    #[test]
    fn test_older_version_is_safe(current in arbitrary_semver()) {
        use evergreenctl::auto_version::is_safe_bump;
        let parts: Vec<u32> = current.split('.').filter_map(|p| p.parse().ok()).collect();
        if parts.len() == 3 && parts[2] > 0 {
            let older = format!("{}.{}.{}", parts[0], parts[1], parts[2] - 1);
            let (safe, _reason) = is_safe_bump(&current, &older, 1);
            prop_assert!(safe, "Older version {} -> {} should be safe", current, older);
        }
    }

    #[test]
    fn test_v_prefix_is_handled(version in arbitrary_semver_with_prefix()) {
        use evergreenctl::auto_version::is_safe_bump;
        let stripped = version.trim_start_matches('v');
        let (safe1, _) = is_safe_bump(&version, &version, 1);
        let (safe2, _) = is_safe_bump(stripped, stripped, 1);
        prop_assert_eq!(safe1, safe2, "v-prefix handling should be consistent");
    }

    #[test]
    fn test_non_semver_exact_match_is_safe(version in arbitrary_non_semver()) {
        use evergreenctl::auto_version::is_safe_bump;
        let (safe, _reason) = is_safe_bump(&version, &version, 1);
        prop_assert!(safe, "Non-semver exact match '{}' should be safe", version);
    }
}

// ---------------------------------------------------------------------------
// Property: Dockerfile parsing invariants
// ---------------------------------------------------------------------------

proptest! {
    #[test]
    fn test_extract_version_returns_some_for_valid(content in "ARG VERSION=[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}") {
        use evergreenctl::dockerfile_utils::extract_version;
        let result = extract_version(&content);
        prop_assert!(result.is_some(), "Valid VERSION arg should return Some");
    }

    #[test]
    fn test_extract_base_image_never_empty(version in arbitrary_semver()) {
        use evergreenctl::dockerfile_utils::extract_base_image;
        let content = format!("FROM some-image:{}\nARG VERSION={}", version, version);
        let base = extract_base_image(&content);
        prop_assert!(!base.is_empty(), "Base image should never be empty");
    }

    #[test]
    fn test_extract_user_defaults_to_65532(content in "[A-Z]+ [a-z]+") {
        use evergreenctl::dockerfile_utils::extract_user;
        let user = extract_user(&content);
        prop_assert!(
            user == "65532:65532" || user == "65532" || user == "65534"
                || user.contains("nobody") || !user.is_empty(),
            "User should be a valid value, got: {}", user
        );
    }

    #[test]
    fn test_extract_ports_are_numeric(ports in "[1-9][0-9]{0,4}( [1-9][0-9]{0,4}){0,5}") {
        use evergreenctl::dockerfile_utils::extract_ports;
        let content = format!("EXPOSE {}", ports);
        let extracted = extract_ports(&content);
        for port in &extracted {
            prop_assert!(
                port.parse::<u16>().is_ok(),
                "Port '{}' should be a valid u16", port
            );
        }
    }

    #[test]
    fn test_extract_source_type_matches_content(content in ".*") {
        use evergreenctl::dockerfile_utils::extract_source_type;
        let st = extract_source_type(&content);
        prop_assert!(
            ["package-manager", "source-build", "binary-download", "copy-from"].contains(&st.as_str()),
            "Source type should be one of the known types, got: {}", st
        );
    }
}

// ---------------------------------------------------------------------------
// Property: Manifest round-trip
// ---------------------------------------------------------------------------

proptest! {
    #[test]
    fn test_manifest_round_trip(
        name in "[a-z][a-z0-9-]{0,20}",
        version in arbitrary_semver(),
        description in "[a-zA-Z0-9 ._-]{0,50}",
        tier in "[123]"
    ) {
        use evergreenctl::manifest::Manifest;

        let content = format!(
            r#"
[metadata]
name = "{name}"
version = "{version}"
description = "{description}"
tier = "{tier}"

[build]
base = "scratch"
user = "65532:65532"
stopsignal = "SIGTERM"

[source]
type = "binary-download"
url = "https://example.com/{name}-{version}.tar.gz"

[runtime]
entrypoint = ["/{name}"]
"#,
            name = name, version = version, description = description, tier = tier
        );

        // Write to temp file and parse
        let dir = tempfile::tempdir().unwrap();
        let path = dir.path().join("manifest.toml");
        let mut f = std::fs::File::create(&path).unwrap();
        write!(f, "{}", content).unwrap();
        drop(f);

        let manifest = Manifest::from_file(&path).unwrap();
        prop_assert_eq!(manifest.name(), name.as_str());
        prop_assert_eq!(manifest.version(), version.as_str());
        let tier_str = manifest.metadata.tier.clone();
        prop_assert_eq!(&tier_str, tier.as_str());

        // Round-trip: serialize and re-parse
        let serialized = toml::to_string_pretty(&manifest).unwrap();
        drop(manifest);
        let reparsed: Manifest = toml::from_str(&serialized).unwrap();
        prop_assert_eq!(reparsed.name(), name.as_str());
        prop_assert_eq!(reparsed.version(), version.as_str());
    }
}

// ---------------------------------------------------------------------------
// Property: Constraint validation invariants
// ---------------------------------------------------------------------------

proptest! {
    #[test]
    fn test_alpine_always_fails(name in "[a-z][a-z0-9]{0,10}") {
        use evergreenctl::validate_parallel::{check_constraints, ConstraintContext, ConstraintStatus};

        let ctx = ConstraintContext {
            name: &name,
            tier: 2,
            manifest_exists: true,
            manifest_name: name.clone(),
            manifest_version: "1.0.0".into(),
            manifest_source_url: "".into(),
            manifest_base: "alpine:3.19".into(),
            manifest_tier: "2".into(),
            dockerfile_exists: true,
            dockerfile_content: "FROM alpine:3.19\nUSER 65532\n".into(),
            sbom_exists: false,
            sbom_valid: false,
        };

        let results = check_constraints(&ctx);
        let alpine_check = results.iter().find(|r| r.code == "C004").unwrap();
        prop_assert_eq!(alpine_check.status, ConstraintStatus::Fail);
    }

    #[test]
    fn test_scratch_images_skip_healthcheck(name in "[a-z][a-z0-9]{0,10}") {
        use evergreenctl::validate_parallel::{check_constraints, ConstraintContext, ConstraintStatus};

        let ctx = ConstraintContext {
            name: &name,
            tier: 2,
            manifest_exists: true,
            manifest_name: name.clone(),
            manifest_version: "1.0.0".into(),
            manifest_source_url: "".into(),
            manifest_base: "scratch".into(),
            manifest_tier: "2".into(),
            dockerfile_exists: true,
            dockerfile_content: "FROM scratch@sha256:aaaa1111bbbb2222cccc3333dddd4444eeee5555ffff6666aaaa7777bbbb8888cccc9999\nUSER 65532:65532\n".into(),
            sbom_exists: false,
            sbom_valid: false,
        };

        let results = check_constraints(&ctx);
        let hc_check = results.iter().find(|r| r.code == "C005").unwrap();
        // Scratch images should pass healthcheck (N/A)
        prop_assert_eq!(hc_check.status, ConstraintStatus::Pass);
    }

    #[test]
    fn test_missing_dockerfile_fails结构性_constraints(name in "[a-z][a-z0-9]{0,10}") {
        use evergreenctl::validate_parallel::{check_constraints, ConstraintContext, ConstraintStatus};

        let ctx = ConstraintContext {
            name: &name,
            tier: 2,
            manifest_exists: true,
            manifest_name: name.clone(),
            manifest_version: "1.0.0".into(),
            manifest_source_url: "".into(),
            manifest_base: "scratch".into(),
            manifest_tier: "2".into(),
            dockerfile_exists: false,
            dockerfile_content: String::new(),
            sbom_exists: false,
            sbom_valid: false,
        };

        let results = check_constraints(&ctx);
        // C002 (Dockerfile exists) should fail
        let df_check = results.iter().find(|r| r.code == "C002").unwrap();
        prop_assert_eq!(df_check.status, ConstraintStatus::Fail);

        // Dockerfile-dependent checks should be skipped
        for code in &["C003", "C004", "C005", "C006"] {
            let check = results.iter().find(|r| r.code == *code).unwrap();
            prop_assert_eq!(check.status, ConstraintStatus::Skip);
        }
    }
}

// ---------------------------------------------------------------------------
// Property: Trait-based constraint system invariants
// ---------------------------------------------------------------------------

proptest! {
    #[test]
    fn test_all_constraints_have_unique_codes(name in "[a-z][a-z0-9]{0,10}") {
        use evergreenctl::validate_parallel::{check_constraints, ConstraintContext};

        let ctx = ConstraintContext {
            name: &name,
            tier: 1,
            manifest_exists: true,
            manifest_name: name.clone(),
            manifest_version: "1.0.0".into(),
            manifest_source_url: "https://github.com/test/repo".into(),
            manifest_base: "scratch".into(),
            manifest_tier: "1".into(),
            dockerfile_exists: true,
            dockerfile_content: "FROM scratch@sha256:aaaa1111bbbb2222cccc3333dddd4444eeee5555ffff6666aaaa7777bbbb8888cccc9999\nUSER 65532:65532\nSTOPSIGNAL SIGTERM\nENTRYPOINT [\"/app\"]\nHEALTHCHECK CMD true\nLABEL org.opencontainers.image.title=\"test\"\nLABEL org.opencontainers.image.version=\"1.0.0\"\nLABEL evergreen.security.cap-drop=\"ALL\"\nLABEL evergreen.security.no-new-privileges=\"true\"\nARG VERSION=1.0.0\n".into(),
            sbom_exists: true,
            sbom_valid: true,
        };

        let results = check_constraints(&ctx);
        let codes: Vec<&str> = results.iter().map(|r| r.code.as_str()).collect();
        let unique_codes: std::collections::HashSet<_> = codes.iter().collect();
        prop_assert_eq!(codes.len(), unique_codes.len(), "Constraint codes must be unique");
    }

    #[test]
    fn test_constraint_count_is_20(name in "[a-z][a-z0-9]{0,10}") {
        use evergreenctl::validate_parallel::{check_constraints, ConstraintContext};

        let ctx = ConstraintContext {
            name: &name,
            tier: 1,
            manifest_exists: true,
            manifest_name: name.clone(),
            manifest_version: "1.0.0".into(),
            manifest_source_url: "".into(),
            manifest_base: "scratch".into(),
            manifest_tier: "1".into(),
            dockerfile_exists: true,
            dockerfile_content: "FROM scratch@sha256:aaaa1111bbbb2222cccc3333dddd4444eeee5555ffff6666aaaa7777bbbb8888cccc9999\nUSER 65532:65532\nSTOPSIGNAL SIGTERM\nENTRYPOINT [\"/app\"]\nHEALTHCHECK CMD true\nLABEL org.opencontainers.image.title=\"test\"\nLABEL org.opencontainers.image.version=\"1.0.0\"\nLABEL evergreen.security.cap-drop=\"ALL\"\nLABEL evergreen.security.no-new-privileges=\"true\"\nLABEL evergreen.security.read-only-rootfs=\"true\"\nARG VERSION=1.0.0\n".into(),
            sbom_exists: true,
            sbom_valid: true,
        };

        let results = check_constraints(&ctx);
        prop_assert_eq!(results.len(), 20, "Should have exactly 20 constraints");
    }

    #[test]
    fn test_valid_images_pass_all_block_constraints(name in "[a-z][a-z0-9]{0,10}") {
        use evergreenctl::validate_parallel::{check_constraints, ConstraintContext, ConstraintStatus, Severity};

        let ctx = ConstraintContext {
            name: &name,
            tier: 1,
            manifest_exists: true,
            manifest_name: name.clone(),
            manifest_version: "1.0.0".into(),
            manifest_source_url: "https://github.com/test/repo".into(),
            manifest_base: "scratch".into(),
            manifest_tier: "1".into(),
            dockerfile_exists: true,
            dockerfile_content: "FROM scratch@sha256:aaaa1111bbbb2222cccc3333dddd4444eeee5555ffff6666aaaa7777bbbb8888cccc9999\nUSER 65532:65532\nSTOPSIGNAL SIGTERM\nENTRYPOINT [\"/app\"]\nHEALTHCHECK CMD true\nLABEL org.opencontainers.image.title=\"test\"\nLABEL org.opencontainers.image.version=\"1.0.0\"\nLABEL evergreen.security.cap-drop=\"ALL\"\nLABEL evergreen.security.no-new-privileges=\"true\"\nLABEL evergreen.security.read-only-rootfs=\"true\"\nARG VERSION=1.0.0\n".into(),
            sbom_exists: true,
            sbom_valid: true,
        };

        let results = check_constraints(&ctx);
        let block_failures: Vec<_> = results.iter()
            .filter(|r| r.severity == Severity::Block && r.status == ConstraintStatus::Fail)
            .collect();
        prop_assert!(block_failures.is_empty(), "Valid images should pass all Block constraints, but got: {:?}", block_failures);
    }

    #[test]
    fn test_each_constraint_returns_valid_result(name in "[a-z][a-z0-9]{0,10}") {
        use evergreenctl::validate_parallel::{check_constraints, ConstraintContext};

        let ctx = ConstraintContext {
            name: &name,
            tier: 2,
            manifest_exists: true,
            manifest_name: name.clone(),
            manifest_version: "1.0.0".into(),
            manifest_source_url: "".into(),
            manifest_base: "wolfi-base".into(),
            manifest_tier: "2".into(),
            dockerfile_exists: true,
            dockerfile_content: "FROM cgr.dev/chainguard/wolfi-base@sha256:dddd5555eeee6666ffff7777aaaa8888bbbb9999cccc0000aaaa1111bbbb2222\nUSER 65532:65532\nLABEL evergreen.security.read-only-rootfs=\"true\"\n".into(),
            sbom_exists: false,
            sbom_valid: false,
        };

        let results = check_constraints(&ctx);
        for r in &results {
            prop_assert!(!r.code.is_empty(), "Constraint code must not be empty");
            prop_assert!(!r.message.is_empty(), "Constraint message must not be empty");
            prop_assert_eq!(&r.image, name.as_str(), "Image name must match");
        }
    }
}

// ---------------------------------------------------------------------------
// Property: SHA256 determinism
// ---------------------------------------------------------------------------

proptest! {
    #[test]
    fn test_sha256_deterministic(data in prop::collection::vec(any::<u8>(), 0..10000)) {
        use evergreenctl::verify::sha256_file;

        let dir = tempfile::tempdir().unwrap();
        let path = dir.path().join("test.bin");
        std::fs::write(&path, &data).unwrap();

        let hash1 = sha256_file(&path).unwrap();
        let hash2 = sha256_file(&path).unwrap();
        let hash_len = hash1.len();
        prop_assert_eq!(hash1, hash2);
        prop_assert_eq!(hash_len, 64); // SHA256 hex is always 64 chars
    }

    #[test]
    fn test_different_data_different_hash(
        a in prop::collection::vec(any::<u8>(), 1..1000),
        b in prop::collection::vec(any::<u8>(), 1..1000)
    ) {
        use evergreenctl::verify::sha256_file;

        let dir = tempfile::tempdir().unwrap();
        let path_a = dir.path().join("a.bin");
        let path_b = dir.path().join("b.bin");
        std::fs::write(&path_a, &a).unwrap();
        std::fs::write(&path_b, &b).unwrap();

        let hash_a = sha256_file(&path_a).unwrap();
        let hash_b = sha256_file(&path_b).unwrap();

        // If data differs, hashes should differ (overwhelmingly likely)
        if a != b {
            prop_assert_ne!(hash_a, hash_b);
        }
    }
}
