#![no_main]
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    if let Ok(content) = std::str::from_utf8(data) {
        // Split input into two version strings
        let parts: Vec<&str> = content.splitn(2, '|').collect();
        if parts.len() == 2 {
            let (current, latest) = (parts[0], parts[1]);

            // Fuzz version comparison — must never panic
            let _ = evergreenctl::auto_version::is_safe_bump(current, latest, 1);
            let _ = evergreenctl::auto_version::is_safe_bump(current, latest, 255);

            // Also fuzz semver parsing
            let _ = semver::Version::parse(current);
            let _ = semver::Version::parse(latest);
        }
    }
});
