# Architecture Decision Record: DB-Specific Shim Variants

## ADR-011: DB-Specific Shim Variants

### Status

ACCEPTED

### Date

2026-06-05

### Author

Evergreen Image Registry Team

### Context

Database images (PostgreSQL, MySQL, MariaDB, MongoDB, Redis) need capabilities beyond basic health checks: scheduled
backups, replication management, schema migrations, and cache invalidation. The general-purpose health-shim handles
health probes and metrics but does not provide database-specific operations.

Embedding all database operations into a single monolithic shim binary would create a large binary with unnecessary code
for non-database images. Cache images need different operations than database images.

### Decision

Create feature-flagged shim binaries specialized by workload type.

**Shim variants:**

| Variant     | Binary        | Features                                  | Images                    |
| ----------- | ------------- | ----------------------------------------- | ------------------------- |
| health-shim | `health-shim` | Health probes, metrics, signal forwarding | Proxies, tools, exporters |
| db-shim     | `shim`        | + Backup, replication, migration, audit   | PostgreSQL, MySQL, etc.   |
| cache-shim  | `shim`        | + Cache invalidation, eviction, metrics   | Redis, Memcached, etc.    |

**Feature flags via env vars:**

```bash
# Database shim features
SHIM_BACKUP_ENABLED="true"
SHIM_BACKUP_DB_HOST="localhost"
SHIM_BACKUP_DB_PORT="5432"
SHIM_REPLICATION_ENABLED="false"
SHIM_MIGRATION_ENABLED="false"
SHIM_VAULT_ENABLED="false"
SHIM_AUDIT_ENABLED="true"

# Cache shim features
SHIM_CACHE_ENABLED="true"
SHIM_CACHE_MAX_ENTRIES="10000"
SHIM_CACHE_DEFAULT_TTL="300"
SHIM_CACHE_EVICTION="lru"
```

**Binary source:**

All shim variants are built from the same Rust workspace (`evergreenshim/`) with Cargo feature flags:

```toml
[features]
default = ["health"]
health = []
db = ["health", "tokio-cron", "sqlx"]
cache = ["health", "lru-cache"]
```

### Consequences

**Positive:**

- Smaller binaries — each variant includes only needed code
- Clear separation of concerns — db operations vs. cache operations
- Feature flags enable per-image customization without code changes
- Shared core (health probes, metrics, signal forwarding) across all variants

**Negative:**

- Three separate binaries to maintain and version
- Feature flag complexity — need to test all combinations
- Users must select the correct variant for their image

**Risks:**

- Feature flag misconfiguration could disable critical backup operations
- Variant version skew between images using different shim versions

### Related ADRs

- ADR-010: Scratch-Based Images with Embedded Health-Shim
- ADR-012: ShimBus Event System

### Related Standards

| Standard             | Relevance                     |
| -------------------- | ----------------------------- |
| NIST SP 800-190      | 3.2 - Container monitoring    |
| CIS Docker Benchmark | 4.6 - Container health checks |
