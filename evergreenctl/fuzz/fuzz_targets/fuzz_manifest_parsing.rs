#![no_main]
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    if let Ok(content) = std::str::from_utf8(data) {
        // Fuzz manifest TOML parsing — must never panic
        let _ = content.parse::<evergreenctl::manifest::Manifest>();

        // Also fuzz the serde path
        let _ = toml::from_str::<evergreenctl::manifest::Manifest>(content);
    }
});
