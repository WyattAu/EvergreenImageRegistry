pub mod audit;
pub mod bump;
pub mod changelog;
pub mod ci_diff;
pub mod deprecated;
pub mod discover;
pub mod drift;
pub mod generate;
pub mod manifest;
pub mod migrate;
pub mod outdated;
pub mod patterns;
pub mod pin_digests;
pub mod report;
pub mod sign;
pub mod snapshot;
pub mod validate_strict;
pub mod verify;
pub mod verify_all;

/// User-Agent header value, derived from Cargo.toml version at compile time.
pub const USER_AGENT: &str = concat!("evergreenctl/", env!("CARGO_PKG_VERSION"));
