#![no_main]
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    if let Ok(content) = std::str::from_utf8(data) {
        // Fuzz all Dockerfile parsing functions
        let _ = evergreenctl::dockerfile_utils::extract_version(content);
        let _ = evergreenctl::dockerfile_utils::extract_base_image(content);
        let _ = evergreenctl::dockerfile_utils::extract_user(content);
        let _ = evergreenctl::dockerfile_utils::extract_stop_signal(content);
        let _ = evergreenctl::dockerfile_utils::extract_description(content);
        let _ = evergreenctl::dockerfile_utils::extract_vendor(content);
        let _ = evergreenctl::dockerfile_utils::extract_tier(content);
        let _ = evergreenctl::dockerfile_utils::extract_github_source(content);
        let _ = evergreenctl::dockerfile_utils::extract_download_url(content);
        let _ = evergreenctl::dockerfile_utils::extract_ports(content);
        let _ = evergreenctl::dockerfile_utils::extract_entrypoint(content);
        let _ = evergreenctl::dockerfile_utils::extract_source_type(content);
        let _ = evergreenctl::dockerfile_utils::extract_all_labels(content);
    }
});
