# Architecture Decision Record: TOML Configuration with Env Var Override

## ADR-013: TOML Configuration with Env Var Override

### Status

ACCEPTED

### Date

2026-06-05

### Author

Evergreen Image Registry Team

### Context

Shim binaries need runtime configuration for health check commands, backup schedules, cache settings, and metrics
endpoints. Configuration must be:

1. Changeable without rebuilding the image
2. Compatible with 12-factor app methodology
3. Backward compatible with existing env-var-only configuration
4. Human-readable and version-controllable

### Decision

Load configuration from `shim.toml` at startup, with environment variables overriding file values.

**Configuration loading order:**

1. Compiled defaults (hardcoded in Rust binary)
2. `shim.toml` file (if present)
3. Environment variables (highest priority)

**shim.toml example:**

```toml
[health]
cmd = "tcp:5432"
ready_cmd = "pg_isready -U postgres"
interval_secs = 10
timeout_secs = 5
start_period_secs = 30
retries = 5

[metrics]
enabled = true
port = 9101
path = "/metrics"

[backup]
enabled = false
db_host = "localhost"
db_port = "5432"
cron = "0 2 * * *"

[cache]
enabled = false
max_entries = 10000
default_ttl_secs = 300
eviction = "lru"

[events]
bridge = "none"  # "none" or "redis"
redis_url = ""
channel = "shimbus:events"
```

**Env var override mapping:**

| Env Var                  | TOML Path           | Example                  |
| ------------------------ | ------------------- | ------------------------ |
| `HEALTH_CMD`             | `health.cmd`        | `tcp:5432`               |
| `READY_CMD`              | `health.ready_cmd`  | `pg_isready -U postgres` |
| `SHIM_METRICS_ENABLED`   | `metrics.enabled`   | `true`                   |
| `SHIM_BACKUP_ENABLED`    | `backup.enabled`    | `true`                   |
| `SHIM_BACKUP_DB_HOST`    | `backup.db_host`    | `localhost`              |
| `SHIM_CACHE_ENABLED`     | `cache.enabled`     | `true`                   |
| `SHIM_CACHE_MAX_ENTRIES` | `cache.max_entries` | `10000`                  |
| `SHIM_EVENT_BRIDGE`      | `events.bridge`     | `redis`                  |

**Parsing implementation:**

```rust
use serde::Deserialize;
use std::path::Path;

#[derive(Deserialize, Default)]
struct ShimConfig {
    health: HealthConfig,
    metrics: MetricsConfig,
    backup: BackupConfig,
    cache: CacheConfig,
    events: EventsConfig,
}

impl ShimConfig {
    fn load() -> Self {
        // 1. Start with compiled defaults
        let mut config = Self::default();

        // 2. Override with TOML file if present
        if let Ok(content) = std::fs::read_to_string("shim.toml") {
            if let Ok(file_config) = toml::from_str::<ShimConfig>(&content) {
                config.merge(file_config);
            }
        }

        // 3. Override with environment variables (highest priority)
        config.apply_env_overrides();

        config
    }
}
```

### Consequences

**Positive:**

- 12-factor compliant — env vars take precedence
- Backward compatible — existing env-var-only images continue working
- Human-readable config file for complex configurations
- Version-controllable — `shim.toml` can be committed alongside Dockerfile
- Type-safe parsing via serde

**Negative:**

- Two configuration mechanisms to document
- TOML file adds a layer to the configuration chain
- Env var names must be stable for backward compatibility

**Risks:**

- TOML file syntax errors could prevent startup (mitigated by logging and fallback to defaults)
- Env var override semantics must be clearly documented

### Related ADRs

- ADR-010: Scratch-Based Images with Embedded Health-Shim
- ADR-012: ShimBus Event System
- ADR-014: Musl Static Binaries

### Related Standards

| Standard       | Relevance                 |
| -------------- | ------------------------- |
| 12-Factor App  | III - Config, XI - Logs   |
| OCI Image Spec | Configuration annotations |
