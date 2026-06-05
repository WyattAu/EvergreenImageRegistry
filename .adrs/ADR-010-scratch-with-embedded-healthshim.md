# Architecture Decision Record: Scratch-Based Images with Embedded Health-Shim

## ADR-010: Scratch-Based Images with Embedded Health-Shim

### Status

ACCEPTED

### Date

2026-06-05

### Author

Evergreen Image Registry Team

### Context

The Evergreen Image Registry contains 986 container images. 333 use `FROM scratch` (static binaries), and 426 have
`HEALTHCHECK NONE`. Scratch images have no shell, so standard `HEALTHCHECK CMD` instructions that rely on `/bin/sh` fail
at runtime. Database and proxy images need health probes, metrics, and process management — but adding a shell violates
Pillar I (Security & Minimalism).

The registry needs a unified approach to provide health checks, signal forwarding, and metrics in scratch-based images
without introducing shells or package managers.

### Decision

Embed the health-shim binary as PID 1 in all scratch-based images that serve network traffic.

**How it works:**

```
FROM scratch

/app/health-shim (Rust, ~300KB)    ← Entry point (PID 1)
/app/main-binary (Go/Rust/C)       ← Application (child)

Port 9101: /livez /readyz /metrics ← health-shim serves
Port APP:  application traffic     ← main-binary serves
```

1. health-shim starts as PID 1
2. It parses config from env vars (HEALTH_CMD, READY_CMD, etc.)
3. It forks the main binary as a child process
4. It starts HTTP server on `:9101` for health/metrics
5. It forwards signals (SIGTERM, SIGINT) to the child
6. It monitors the child process and updates health status
7. If child crashes, health-shim exits with non-zero code → orchestrator restarts

**Shim variants:**

| Variant     | Binary         | Use Case                         |
| ----------- | -------------- | -------------------------------- |
| health-shim | `/health-shim` | General-purpose (proxies, tools) |
| db-shim     | `/shim`        | Databases (backup, replication)  |
| cache-shim  | `/shim`        | Caches (invalidation, metrics)   |

**Configuration via env vars:**

```bash
HEALTH_CMD="tcp:5432"                  # TCP socket check
HEALTH_CMD="exec:pg_isready -U postgres"  # CLI exec check
HEALTH_CMD="http:localhost:8080/metrics"   # HTTP probe
READY_CMD="redis-cli ping"             # Readiness check
```

**Layered health check strategy:**

| Layer              | Check                                         | Speed     | Accuracy |
| ------------------ | --------------------------------------------- | --------- | -------- |
| L1: PID monitoring | Is child process alive?                       | <1ms      | Basic    |
| L2: TCP socket     | Is the service port open?                     | ~1ms      | Medium   |
| L3: CLI exec       | Does `pg_isready` / `redis-cli ping` succeed? | ~10-100ms | High     |
| L4: HTTP probe     | Does `/metrics` return 200?                   | ~50-200ms | Highest  |

### Consequences

**Positive:**

- No shell required in scratch images — pure binary orchestration
- Single binary entrypoint — no `--init` flag needed
- Process monitoring built-in (no external init system)
- Layered health checks (PID + TCP + CLI + HTTP)
- Unified pattern across all scratch images
- ~200-300KB binary size (musl + LTO + strip)

**Negative:**

- Per-image configuration required (env vars for HEALTH_CMD, etc.)
- CLI exec requires the database CLI binary in the image (adds ~1-5MB)
- Adds a dependency on the shim binary for all scratch images

**Risks:**

- Rust cross-compilation for musl targets can be tricky (mitigated by Docker buildx)
- CLI exec adds latency (~10-100ms per check) — acceptable for 30s probe intervals
- Some databases may not have CLI health tools (mitigated by TCP fallback)

### Related ADRs

- ADR-001: HEALTHCHECK Strategy (superseded by this ADR for scratch images)
- ADR-009: Rust Health-Shim as Entrypoint (detailed design)
- ADR-011: DB-Specific Shim Variants

### Related Standards

| Standard             | Relevance                         |
| -------------------- | --------------------------------- |
| CIS Docker Benchmark | 4.6 - Container health checks     |
| Kubernetes API       | Probe endpoints (/livez, /readyz) |
| OpenMetrics 1.0.0    | Metrics format                    |
