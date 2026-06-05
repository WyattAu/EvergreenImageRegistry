# Architecture Decision Record: ShimBus Event System

## ADR-012: ShimBus Event System

### Status

ACCEPTED

### Date

2026-06-05

### Author

Evergreen Image Registry Team

### Context

Cross-shim coordination is needed in multi-container environments. Examples:

- A backup completion event should trigger encryption of the backup archive
- A database failover event should notify dependent services
- A cache invalidation event should propagate to all cache nodes
- A metrics threshold breach should trigger alerting

Without a coordination mechanism, each shim operates in isolation. External coordination via Redis, NATS, or other
message brokers adds operational complexity and latency for in-pod communication.

### Decision

Implement a dual-mode event system using Tokio broadcast channels (in-process) with an optional Redis bridge
(cross-pod).

**Architecture:**

```
┌──────────────────────────────────────────────────┐
│  Pod                                            │
│                                                 │
│  ┌──────────┐    ShimBus    ┌──────────┐        │
│  │ db-shim  │◄─────────────►│cache-shim│        │
│  └──────────┘  Tokio channel └──────────┘        │
│       │                          │               │
│       └──────────┬───────────────┘               │
│                  │                               │
│         ┌────────▼────────┐                      │
│         │  Redis Bridge   │  (optional)          │
│         └────────┬────────┘                      │
└──────────────────┼──────────────────────────────┘
                   │
        ┌──────────▼──────────┐
        │  Other Pods         │
        │  (db-shim, cache)   │
        └─────────────────────┘
```

**Event types:**

```rust
pub enum ShimEvent {
    // Database events
    BackupCompleted { job_id: String, size_bytes: u64 },
    BackupFailed { job_id: String, error: String },
    ReplicationLag { lag_ms: u64 },
    MigrationCompleted { version: u64 },

    // Cache events
    CacheInvalidated { key: String },
    CacheEvicted { key: String, reason: EvictionReason },

    // System events
    HealthDegraded { component: String, details: String },
    HealthRecovered { component: String },
}
```

**In-process mode (default):**

```rust
use tokio::sync::broadcast;

let (tx, rx) = broadcast::channel::<ShimEvent>(256);
```

- Zero-latency delivery
- No external dependencies
- Works within a single pod
- Buffer size: 256 events (configurable)

**Redis bridge mode (optional):**

```bash
SHIM_EVENT_BRIDGE="redis"
SHIM_EVENT_REDIS_URL="redis://redis:6379"
SHIM_EVENT_CHANNEL="shimbus:events"
```

- Cross-pod event propagation
- Requires Redis instance
- Adds ~1-2ms latency
- Enables multi-replica coordination

### Consequences

**Positive:**

- In-process events are zero-latency (Tokio broadcast channel)
- Redis bridge enables multi-pod coordination when needed
- Feature-flagged — Redis bridge is optional
- Type-safe events via Rust enum
- Backpressure via bounded channel

**Negative:**

- Redis bridge adds operational dependency
- Event serialization/deserialization overhead for Redis bridge
- Bounded channel may drop events under high load (logged as warning)

**Risks:**

- Redis availability affects cross-pod coordination (mitigated by fallback to in-process only)
- Event ordering not guaranteed across pods (acceptable for async operations)

### Related ADRs

- ADR-010: Scratch-Based Images with Embedded Health-Shim
- ADR-011: DB-Specific Shim Variants
- ADR-013: TOML Configuration with Env Var Override

### Related Standards

| Standard         | Relevance                     |
| ---------------- | ----------------------------- |
| OpenTelemetry    | Event correlation and tracing |
| CNCF CloudEvents | Event format compatibility    |
