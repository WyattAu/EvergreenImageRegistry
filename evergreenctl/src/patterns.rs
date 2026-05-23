//! Centralized regex patterns for evergreenctl.
//!
//! All Regex instances are compiled once via LazyLock and reused across modules.
//! This avoids repeated regex compilation on every function call.

use regex::Regex;
use std::sync::LazyLock;

// --- migrate.rs patterns ---

/// Extract download URL from curl/wget commands.
/// Captures group 1: the URL.
pub static RE_DOWNLOAD_URL: LazyLock<Regex> =
    LazyLock::new(|| Regex::new("(?:curl|wget)\\s+[^\"]*\"?(https?://[^\"'\\s]+)\"?").unwrap());

/// Extract EXPOSE ports from Dockerfile.
/// Captures group 1: port list (space-separated, may include /tcp /udp).
pub static RE_EXPOSE_PORTS: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r"EXPOSE\s+([\d\s/]+)").unwrap());

/// Extract ENTRYPOINT exec form.
/// Captures group 1: comma-separated quoted args.
pub static RE_ENTRYPOINT: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r"ENTRYPOINT\s+\[([^\]]+)\]").unwrap());

/// Extract OCI description label value.
/// Captures group 1: description text.
pub static RE_DESCRIPTION_LABEL: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r#"org\.opencontainers\.image\.description="([^"]+)""#).unwrap());

/// Extract ARG VERSION value from Dockerfile.
/// Captures group 1: version string.
pub static RE_ARG_VERSION: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r#"ARG\s+VERSION="?([^"\s]+)"?"#).unwrap());

/// Extract OCI vendor label value.
/// Captures group 1: vendor name.
pub static RE_VENDOR_LABEL: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r#"org\.opencontainers\.image\.vendor="([^"]+)""#).unwrap());

/// Extract evergreen tier label value.
/// Captures group 1: tier number.
pub static RE_TIER_LABEL: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r#"evergreen\.image\.tier="(\d+)""#).unwrap());

/// Extract GitHub source URL.
/// Captures group 0: full URL.
pub static RE_GITHUB_SOURCE: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r#"https?://github\.com/([^/""\s]+/[^/""\s]+)"#).unwrap());

/// Extract FROM base image (last match = final stage).
/// Captures group 1: image reference.
pub static RE_FROM_IMAGE: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r"FROM\s+([\S]+)").unwrap());

/// Extract USER directive (last match wins).
/// Captures group 1: user[:group].
pub static RE_USER: LazyLock<Regex> = LazyLock::new(|| Regex::new(r"USER\s+(\S+)").unwrap());

/// Extract STOPSIGNAL directive.
/// Captures group 1: signal name.
pub static RE_STOPSIGNAL: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r"STOPSIGNAL\s+(\S+)").unwrap());

/// Extract all key="value" label pairs.
/// Captures group 1: key, group 2: value.
pub static RE_KEY_VALUE_LABEL: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r#"([a-zA-Z0-9_.-]+)="([^"]+)""#).unwrap());

// --- verify_all.rs patterns ---

/// Detect COPY --from directives.
pub static RE_COPY_FROM: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r"COPY\s+--from=\S+").unwrap());

/// Detect curl/wget download commands with URLs.
pub static RE_DOWNLOAD_CMD: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r"(?:curl|wget)\s+.*https?://").unwrap());
