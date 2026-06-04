# Architecture Decision Record: Rust Health-Shim as Entrypoint

## ADR-009: Scratch-Image Observability via Rust Entry shim

### Status

PROPOSED

### Date

2026-06-04

### Author

Nexus (Principal Systems Architect)

### Context

The Evergreen Image Registry contains 986 container images. 333 use `FROM scratch` (static binaries), 426 have
`HEALTHCHECK NONE`, and only 2 images are wired to the existing Go health-shim.

**The core problem:** Scratch images have no shell, so standard HEALTHCHECK `CMD` instructions fail. Database and proxy
images need health probes, metrics, and process management — but adding a shell violates Pillar I (Security &
Minimalism).

**Existing solution (Go health-shim):**

- ~2MB statically compiled Go binary
- Wraps CLI health checks (`pg_isready`, `redis-cli ping`)
- Runs as PID > 1 alongside the application
- Requires `--init` flag or `shareProcessNamespace: true`
- Only wired into 2 images out of ~150 that need it

**Limitations of current approach:**

1. Go binary is ~2MB (large for scratch images)
2. Requires separate PID management (`--init` flag)
3. Not the entrypoint — additional process orchestration needed
4. Manual per-image wiring (100+ Dockerfiles)

**Industry context (2026):**

- OpenTelemetry graduated from CNCF (78% production adoption)
- eBPF-based zero-code instrumentation is mature (OBI/Beyla)
- Kubernetes probes are stable (no new probe types coming)
- Structured JSON stdout is the logging standard
- tini is the consensus PID1 choice (but we can do better)

### Decision

#### 1. Rewrite health-shim in Rust

Replace the Go health-shim with a Rust implementation:

| Metric           | Go (current)              | Rust (proposed)                 |
| ---------------- | ------------------------- | ------------------------------- |
| Binary size      | ~2MB                      | ~200-300KB (musl + LTO + strip) |
| Memory footprint | ~5MB RSS                  | ~1-2MB RSS                      |
| Startup time     | ~10ms                     | ~1ms                            |
| Attack surface   | GC, runtime, reflect      | None (no runtime)               |
| Process model    | Multi-process with --init | Single entrypoint               |

**Rust dependencies:**

- `tokio` — async runtime
- `axum` — HTTP server (~50KB)
- `prometheus-client` — metrics format
- `nix` — signal handling, process management
- `serde` — config parsing from env vars

**Binary size budget:**

| Component            | Size           |
| -------------------- | -------------- |
| Tokio runtime        | ~100KB         |
| Axum HTTP            | ~50KB          |
| Prometheus client    | ~30KB          |
| Application logic    | ~20KB          |
| **Total (stripped)** | **~200-300KB** |

#### 2. Health-shim IS the Entry point (PID 1)

```
┌─────────────────────────────────────┐
│  FROM scratch                       │
│                                     │
│  /app/health-shim (Rust, ~300KB)    │  ← Entry point (PID 1)
│  /app/main-binary (Go/Rust/C)       │  ← Application (child)
│                                     │
│  Port 9101: /livez /readyz /metrics │  ← health-shim serves
│  Port APP:  application traffic     │  ← main-binary serves
└─────────────────────────────────────┘
```

**How it works:**

1. health-shim starts as PID 1
2. It parses config from env vars (HEALTH_CMD, READY_CMD, etc.)
3. It forks the main binary as a child process
4. It starts HTTP server on `:9101` for health/metrics
5. It forwards signals (SIGTERM, SIGINT) to the child
6. It monitors the child process and updates health status
7. If child crashes, health-shim exits with non-zero code → K8s restarts pod

**No shell required** — pure binary orchestration.

#### 3. Process Monitoring, Not Supervision

health-shim monitors the child process but does NOT restart it:

- **Monitor**: Track child PID, exit code, memory usage
- **Forward**: SIGTERM, SIGINT → child process
- **Report**: Update /livez, /readyz based on child state
- **Exit**: If child crashes, exit with child's exit code

**Rationale:** Kubernetes handles restarts via restart policy. Process supervision inside containers is an anti-pattern
(community consensus: let the orchestrator handle it).

#### 4. Layered Health Check Strategy

For database and proxy images, use a layered approach:

| Layer                  | Check                                         | Speed     | Accuracy |
| ---------------------- | --------------------------------------------- | --------- | -------- |
| **L1: PID monitoring** | Is child process alive?                       | <1ms      | Basic    |
| **L2: TCP socket**     | Is the service port open?                     | ~1ms      | Medium   |
| **L3: CLI exec**       | Does `pg_isready` / `redis-cli ping` succeed? | ~10-100ms | High     |
| **L4: HTTP probe**     | Does `/metrics` return 200?                   | ~50-200ms | Highest  |

**Configuration via env vars:**

```bash
# L1: Always checked (PID monitoring)
HEALTH_CMD=""  # Empty = PID-only check

# L2: TCP socket check
HEALTH_CMD="tcp:5432"  # PostgreSQL

# L3: CLI exec check
HEALTH_CMD="exec:pg_isready -U postgres"  # PostgreSQL
HEALTH_CMD="exec:redis-cli ping"           # Redis
HEALTH_CMD="exec:mysqladmin ping"          # MySQL

# L4: HTTP probe (if app has /metrics)
HEALTH_CMD="http:localhost:8080/metrics"   # Traefik, Nginx
```

**Most robust option for databases: L1 + L3 (PID + CLI exec)**

- PID monitoring catches crashes immediately
- CLI exec validates the database is actually ready (not just port open)
- TCP-only is insufficient: databases listen on TCP even when recovering
- HTTP-only is insufficient: not all databases have HTTP endpoints

#### 5. Observability Scope

health-shim handles **health and metrics only**. Logs and traces are infrastructure concerns:

| Signal      | Handled By                | Why                                      |
| ----------- | ------------------------- | ---------------------------------------- |
| **Health**  | health-shim (port 9101)   | K8s probes need local endpoint           |
| **Metrics** | health-shim (port 9101)   | Prometheus scraping needs local endpoint |
| **Logs**    | stdout + Vector DaemonSet | Infrastructure handles transformation    |
| **Traces**  | eBPF (OBI) + OTel SDK     | Kernel-level, zero-code instrumentation  |

**Rationale:**

- Logs: Structured JSON to stdout is the standard. Vector/DaemonSet handles collection.
- Traces: eBPF (OBI/Beyla) provides zero-code instrumentation at kernel level.
- Metrics: Must be scraped by vmagent → needs local HTTP endpoint → health-shim serves it.
- Health: Must be checked by K8s → needs local HTTP endpoint → health-shim serves it.

**Future-proofing:** health-shim will support OTLP export as an option (gRPC push to OTel Collector), but Prometheus
scraping remains the primary metrics path for backward compatibility.

#### 6. Per-Arch Builds (Not Multi-Arch)

Build separate binaries for x86_64 and aarch64:

```dockerfile
# Builder stage
FROM rust:1.75-bookworm AS builder
ARG TARGETARCH
RUN target-triple=$(case $TARGETARCH in amd64) echo x86_64-unknown-linux-musl;; arm64) echo aarch64-unknown-linux-musl;; esac) && \
    rustup target add $target-triple && \
    cargo build --release --target $target-triple

# Final stage
FROM scratch
COPY --from=builder /app/target/$target-triple/release/health-shim /app/health-shim
```

**Rationale:** Per-arch builds are ~20% smaller than fat multi-arch binaries. The image is already per-arch (scratch +
static binary), so the shim should be too.

### Consequences

**Positive:**

- 10x smaller health-shim (~300KB vs ~2MB Go)
- Single binary entrypoint (no --init needed)
- Process monitoring built-in (no external init system)
- Layered health checks (PID + TCP + CLI + HTTP)
- Future-proof (OTLP export ready)
- Per-arch builds for minimum size

**Negative:**

- Rewrite required (Go → Rust)
- Per-image configuration (env vars for HEALTH_CMD, etc.)
- CLI exec requires the database CLI binary in the image (adds ~1-5MB)

**Risks:**

- Rust cross-compilation for musl targets can be tricky (mitigated by Docker buildx)
- CLI exec adds latency (~10-100ms per check) — acceptable for 30s probe intervals
- Some databases may not have CLI health tools (mitigated by TCP fallback)

### Implementation Priority

| Priority | Images                                           | Count | Reason                                     |
| -------- | ------------------------------------------------ | ----- | ------------------------------------------ |
| **P0**   | postgres, redis, mariadb, mysql, mongodb, valkey | ~15   | Core databases, highest operational impact |
| **P1**   | traefik, nginx, caddy, haproxy, envoy            | ~10   | Proxies/ingress, critical for traffic      |
| **P2**   | kafka, rabbitmq, nats, elasticsearch, opensearch | ~10   | Messaging/search, high operational impact  |
| **P3**   | Remaining database/proxy images                  | ~20   | Lower priority databases and proxies       |
| **P4**   | All other scratch images                         | ~280  | Static binaries, health-shim optional      |

### Alternatives Considered

| Alternative                               | Rejected Because                                            |
| ----------------------------------------- | ----------------------------------------------------------- |
| Keep Go health-shim                       | 2MB is large for scratch; GC pauses; multi-process model    |
| Use tini as PID1 + health-shim as sidecar | Adds container complexity; tini doesn't solve health checks |
| eBPF-only approach                        | Requires kernel support; not available in all environments  |
| Embed health endpoint in application      | Requires source code changes to every upstream project      |
| Remove health checks entirely             | Violates Pillar II (Reliability); K8s needs probes          |

### Related ADRs

| ADR     | Relationship                                                                  |
| ------- | ----------------------------------------------------------------------------- |
| ADR-001 | HEALTHCHECK strategy (superseded by this ADR for scratch images)              |
| ADR-006 | Observability architecture (this ADR extends health-shim section)             |
| ADR-007 | Base image preference (scratch stays; this ADR adds observability to scratch) |

### Related Standards

| Standard                 | Relevance                                    |
| ------------------------ | -------------------------------------------- |
| CIS Docker Benchmark 4.6 | Container health checks                      |
| Kubernetes API           | Probe endpoints (/livez, /readyz, /startupz) |
| OpenMetrics 1.0.0        | Metrics format                               |
| OpenTelemetry            | Future OTLP export compatibility             |
