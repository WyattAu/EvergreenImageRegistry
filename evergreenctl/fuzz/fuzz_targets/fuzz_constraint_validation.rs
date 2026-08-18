#![no_main]
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    if let Ok(content) = std::str::from_utf8(data) {
        // Split input into name|version|dockerfile sections
        let parts: Vec<&str> = content.splitn(3, '|').collect();
        let name = parts.first().unwrap_or(&"fuzz");
        let version = parts.get(1).unwrap_or(&"0.0.0");
        let dockerfile = parts.get(2).unwrap_or(&"");

        // Build a constraint context from fuzzed input
        let ctx = evergreenctl::validate_parallel::ConstraintContext {
            name,
            tier: 2,
            manifest_exists: true,
            manifest_name: name.to_string(),
            manifest_version: version.to_string(),
            manifest_source_url: String::new(),
            manifest_base: "scratch".into(),
            manifest_tier: "2".into(),
            dockerfile_exists: !dockerfile.is_empty(),
            dockerfile_content: dockerfile.to_string(),
            sbom_exists: false,
            sbom_valid: false,
        };

        // Fuzz constraint checking — must never panic
        let results = evergreenctl::validate_parallel::check_constraints(&ctx);

        // Verify all results have valid fields
        for r in &results {
            assert!(!r.code.is_empty());
            assert!(!r.message.is_empty());
            assert!(!r.image.is_empty());
        }
    }
});
