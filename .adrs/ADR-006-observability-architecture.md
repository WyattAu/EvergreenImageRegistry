# Architecture Decision Record: Observability Architecture

## ADR-006: Metrics, Health Probes, Structured Logging, and mTLS Strategy

### Status
ACCEPTED

### Date
2026-04-22

### Author
Nexus (Principal Systems Architect)

### Context

The Evergreen Image Registry contains 1,012+ container images deployed across HFT desks and military environments. The existing images have **zero** observability instrumentation:
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

| Endpoint | Purpose | K8s Probe | Response |
|----------|---------|-----------|----------|
| `/metrics` | Prometheus/OpenMetrics text format | — | 200 + metrics body |
| `/livez` | Liveness — process is alive | `livenessProbe` | 200 if alive |
| `/readyz` | Readiness — accepting traffic | `readinessProbe` | 200 if ready |
| `/startupz` | Startup — initialization complete | `startupProbe` | 200 if started |

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

| Language | Framework | Output | Configuration |
|----------|-----------|--------|---------------|
| Go (540 images) | `log/slog` (stdlib, Go 1.21+) | JSON to stdout, one object per line | `EVERGREEN_LOG_LEVEL` ENV var |
| Rust (~50 images) | `tracing` + `tracing-subscriber` JSON | JSON to stdout, one event per line | `RUST_LOG` ENV var |
| Package-based (470 images) | Native application format | Native to stdout | Application-native ENV vars |

**Rules:**
- One JSON object per line (or one log line per event for native format)
- No pretty-print
- No multi-line stack traces in structured output
- No sensitive data (passwords, tokens, PII)
- Log level configurable at runtime via environment variable

**Vector DaemonSet** handles transformation of native-format logs (Redis, PostgreSQL, Nginx, Java) to JSON downstream. This is an infrastructure concern, not an image concern.

#### 4. Health Shim for Database Images

Database images without native HTTP servers (PostgreSQL, Redis, MariaDB, MongoDB, Valkey, Kafka, ZooKeeper) include a compiled Go binary (`health-shim`) that:

1. Wraps native CLI health checks (`pg_isready`, `redis-cli ping`, etc.)
2. Exposes `/livez`, `/readyz`, `/startupz` on :9101
3. Runs as PID > 1 alongside the database (PID 1)
4. Container uses runtime `--init` flag for proper signal handling

**Implementation:**
```go
// health-shim serves /livez, /readyz, /startupz on :9101
// by wrapping native health check commands
package main

import (
    "net/http"
    "os/exec"
    "log/slog"
)
```

The shim binary is ~2MB statically compiled, included in the Dockerfile's final stage.

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
- ~150 database images need health-shim binary
- ~470 package-based images need entrypoint modifications for log format
- Total effort: ~1,012 Dockerfile modifications

**Risks:**
- Some upstream Go projects may not easily support slog (CGO, custom loggers)
- Health shim adds a secondary process to database containers (mitigated by --init flag)
- Port 9101 must be allowed in network policies for vmagent

### Alternatives Considered

| Alternative | Rejected Because |
|-------------|-----------------|
| Envoy sidecar per pod | 15-20MB overhead per pod, 16GB cluster-wide at 1,012 pods |
| Port 9090 | Conflicts with Prometheus server default |
| Per-language log agents | Adds container complexity, Vector DaemonSet covers this |
| Docker HEALTHCHECK instruction only | Not K8s-native, shell-form blocks scratch, exec-form limited |
| Unified /health endpoint | K8s convention is /livez, /readyz, /startupz (separate concerns) |

### Related Standards

| Standard | Relevance |
|----------|-----------|
| NIST SP 800-92 | Log management |
| CIS Docker Benchmark 5.14 | Container logging |
| OpenMetrics 1.0.0 | Metrics format |
| Kubernetes API | Probe endpoints |

### Related ADRs

| ADR | Relationship |
|-----|-------------|
| ADR-001 | HEALTHCHECK strategy (superseded by this ADR for /livez /readyz /startupz) |
| ADR-005 | Military compliance (observability supports audit requirements) |
| ADR-007 | Base image order (affects which images can embed health endpoints) |

### Related Requirements

| REQ ID | Requirement |
|--------|------------|
| C010 | Health endpoints on :9101 |
| C021 | Observability port exposed |
| C022 | Structured logging configured |
| C026 | mTLS capability label |
| REQ-LOG-001..003 | Logging requirements |
| REQ-MET-001..003 | Metrics requirements |
| REQ-HLT-001..003 | Health check requirements |
