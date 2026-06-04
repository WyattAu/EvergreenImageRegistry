# Architecture Decision Record: Observability Architecture

## ADR-006: Metrics, Health Probes, Structured Logging, and mTLS Strategy

### Status

ACCEPTED

### Date

2026-04-22

### Author

Nexus (Principal Systems Architect)

### Context

The Evergreen Image Registry contains 1,012+ container images deployed across HFT desks and military environments. The
existing images have **zero** observability instrumentation:

- 0/1,012 images configure metrics endpoints
- 0/1,012 images configure structured logging
- 0/1,012 declare STOPSIGNAL
- 0/1,012 use an init system
- 6/1,012 use shell-form HEALTHCHECK (blocks scratch migration)

The operational environment uses:

- **Istio ambient mesh** with ztunnel for node-level mTLS
- **VictoriaMetrics** for metrics storage (via vmagent scraper)
- **VictoriaLogs** for log storage (via Vector DaemonSet)
- **Grafana** for visualization

### Decision

#### 1. Single Observability Port: 9101

All images with HTTP capability serve observability on **port 9101** with these endpoints:

| Endpoint    | Purpose                            | K8s Probe        | Response           |
| ----------- | ---------------------------------- | ---------------- | ------------------ |
| `/metrics`  | Prometheus/OpenMetrics text format | —                | 200 + metrics body |
| `/livez`    | Liveness — process is alive        | `livenessProbe`  | 200 if alive       |
| `/readyz`   | Readiness — accepting traffic      | `readinessProbe` | 200 if ready       |
| `/startupz` | Startup — initialization complete  | `startupProbe`   | 200 if started     |

**Port 9101 chosen over 9090:**

- 9090 is Prometheus server default — confusion risk
- 9101 follows the `9100+offset` convention (9100 = Node Exporter default)

#### 2. mTLS Strategy: Native First, ztunnel Fallback

```
┌─────────────────────────────────────────────────────────┐
│ Decision Tree                                           │
│                                                         │
│ Can the app serve TLS natively?                         │
│   YES → App handles mTLS (Go http.ServeTLS,             │
│          Rust axum-server::bind_rustls)                 │
│          Certs via ENV: EVERGREEN_TLS_CERT_PATH,        │
│          EVERGREEN_TLS_KEY_PATH, EVERGREEN_TLS_CA_PATH  │
│                                                         │
│   NO  → App serves plaintext on :9101                   │
│          ztunnel (Istio ambient) encrypts at node level  │
│          vmagent scrapes through mesh (mTLS terminated) │
│                                                         │
│ No /metrics at all?                                     │
│   → Label: evergreen.metrics.native="false"             │
│   → Only cAdvisor/container runtime metrics available    │
└─────────────────────────────────────────────────────────┘
```

**Why no sidecar:**

- Envoy sidecar adds 15-20MB RAM per pod
- At 1,012 pods, that's ~16GB cluster-wide overhead
- Istio ambient mesh with ztunnel already provides node-level encryption
- Network policy on :9101 is simpler with pod-local traffic (ztunnel handles cross-pod)

#### 3. Structured Logging by Language

| Language                   | Framework                             | Output                              | Configuration                 |
| -------------------------- | ------------------------------------- | ----------------------------------- | ----------------------------- |
| Go (540 images)            | `log/slog` (stdlib, Go 1.21+)         | JSON to stdout, one object per line | `EVERGREEN_LOG_LEVEL` ENV var |
| Rust (~50 images)          | `tracing` + `tracing-subscriber` JSON | JSON to stdout, one event per line  | `RUST_LOG` ENV var            |
| Package-based (470 images) | Native application format             | Native to stdout                    | Application-native ENV vars   |

**Rules:**

- One JSON object per line (or one log line per event for native format)
- No pretty-print
- No multi-line stack traces in structured output
- No sensitive data (passwords, tokens, PII)
- Log level configurable at runtime via environment variable

**Vector DaemonSet** handles transformation of native-format logs (Redis, PostgreSQL, Nginx, Java) to JSON downstream.
This is an infrastructure concern, not an image concern.

#### 4. Health Shim for Scratch Images

Database and proxy images without native HTTP servers include a compiled Rust binary (`health-shim-rs`) that serves as
the container entry point (PID 1):

1. Parses config from env vars (HEALTH_CMD, READY_CMD, LISTEN)
2. Forks the main binary as a child process
3. Exposes `/livez`, `/readyz`, `/startupz`, `/metrics` on :9101
4. Forwards signals (SIGTERM, SIGINT) to the child
5. Monitors child process; exits with non-zero code on crash (K8s restarts pod)

**Layered health check strategy:**

| Layer | Check          | Speed     | Use Case                                   |
| ----- | -------------- | --------- | ------------------------------------------ |
| L1    | PID monitoring | <1ms      | All images (always active)                 |
| L2    | TCP socket     | ~1ms      | Quick port check                           |
| L3    | CLI exec       | ~10-100ms | Database readiness (pg_isready, redis-cli) |
| L4    | HTTP probe     | ~50-200ms | Application health (if /metrics exists)    |

**Most robust for databases: L1 + L3 (PID + CLI exec)**

The Rust shim binary is ~200-300KB statically compiled (musl + LTO + strip), included in the Dockerfile's final stage.
Per-arch builds for x86_64 and aarch64.

**Scope:** health-shim handles health and metrics only. Logs go to stdout (Vector DaemonSet handles collection). Traces
use eBPF (OBI/Beyla) at kernel level. See ADR-009 for full architecture.

### Consequences

**Positive:**

- Uniform observability across all 1,012 images
- K8s-native probe pattern (/livez, /readyz, /startupz)
- vmagent can scrape all images consistently
- Vector DaemonSet handles log transformation (no per-image log config)
- No sidecar overhead
- mTLS handled at the right level (native when possible, ztunnel when not)

**Negative:**

- ~400 scratch Go binaries need `slog` instrumentation added to source
- ~150 database/proxy images need health-shim-rs binary wired in
- ~470 package-based images need entrypoint modifications for log format
- Total effort: ~1,012 Dockerfile modifications
- CLI exec health checks add ~10-100ms latency per probe (acceptable for 30s intervals)

**Risks:**

- Some upstream Go projects may not easily support slog (CGO, custom loggers)
- Rust cross-compilation for musl targets requires Docker buildx (mitigated)
- CLI exec requires database CLI binary in image (adds ~1-5MB per image)
- Port 9101 must be allowed in network policies for vmagent

### Alternatives Considered

| Alternative                         | Rejected Because                                                 |
| ----------------------------------- | ---------------------------------------------------------------- |
| Envoy sidecar per pod               | 15-20MB overhead per pod, 16GB cluster-wide at 1,012 pods        |
| Port 9090                           | Conflicts with Prometheus server default                         |
| Per-language log agents             | Adds container complexity, Vector DaemonSet covers this          |
| Docker HEALTHCHECK instruction only | Not K8s-native, shell-form blocks scratch, exec-form limited     |
| Go health-shim (current)            | 2MB binary, requires --init, multi-process model (see ADR-009)   |
| tini as PID1 + health-shim sidecar  | Adds container complexity; tini doesn't solve health checks      |
| Unified /health endpoint            | K8s convention is /livez, /readyz, /startupz (separate concerns) |

### Related Standards

| Standard                  | Relevance         |
| ------------------------- | ----------------- |
| NIST SP 800-92            | Log management    |
| CIS Docker Benchmark 5.14 | Container logging |
| OpenMetrics 1.0.0         | Metrics format    |
| Kubernetes API            | Probe endpoints   |

### Related ADRs

| ADR     | Relationship                                                               |
| ------- | -------------------------------------------------------------------------- |
| ADR-001 | HEALTHCHECK strategy (superseded by this ADR for /livez /readyz /startupz) |
| ADR-005 | Military compliance (observability supports audit requirements)            |
| ADR-007 | Base image order (affects which images can embed health endpoints)         |
| ADR-009 | Rust health-shim entrypoint (extends health-shim section of this ADR)      |

### Related Requirements

| REQ ID           | Requirement                   |
| ---------------- | ----------------------------- |
| C010             | Health endpoints on :9101     |
| C021             | Observability port exposed    |
| C022             | Structured logging configured |
| C026             | mTLS capability label         |
| REQ-LOG-001..003 | Logging requirements          |
| REQ-MET-001..003 | Metrics requirements          |
| REQ-HLT-001..003 | Health check requirements     |
