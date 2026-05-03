# Evergreen Hardened Image Registry — Unified Requirements Specification

## Document Metadata

| Attribute | Value |
|-----------|-------|
| Document ID | REQ-SPEC-SOVEREIGN-UNIFIED-001 |
| Version | 4.0.0 |
| Status | APPROVED |
| Created | 2026-04-19 |
| Last Updated | 2026-04-22 |
| Author | Nexus (Principal Systems Architect) |
| Confidence Level | 0.99 |
| TQA Level | 5 |
| Supersedes | REQUIREMENTS.md v3.0.0, newrequirements.md v2.0.0 |

### Change Log

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-19 | Initial constraint checklist |
| 2.0.0 | 2026-04-19 | Added base image priority, scaling requirements |
| 3.0.0 | 2026-04-19 | Added test requirements, CI pipeline specs |
| 3.5.0 | 2026-04-19 | Parallel requirements spec (newrequirements.md) |
| **4.0.0** | **2026-04-22** | **Unified spec. Resolved 9 conflict sets. Added observability architecture. Universal base image order. UID 65532. debian-slim banned. /livez /readyz /startupz on :9101. mTLS strategy. slog/tracing logging.** |

---

## Executive Summary

This document is the **single source of truth** for all requirements governing the Evergreen Hardened Image Registry. It supersedes all prior requirements documents. Every conflict identified in the v3.0.0/v3.5.0 era has been resolved herein.

**Mission:** Industrial-grade hardened container image registry with 1,012+ images for HFT desks and military contractors.

**Principles:** Zero-trust, defense-in-depth, minimal attack surface, provable correctness.

---

## Part I: Base Image Policy

### 1.1 Universal Preference Order

All images **must** use the most secure base image that supports the workload. The preference order is **not tier-based** — it applies to every image regardless of operational tier.

```
scratch > wolfi > RHEL UBI micro > RHEL UBI minimal > RHEL UBI standard
```

| Priority | Base Image | Registry | libc | Package Manager | Typical Size | Use When |
|----------|-----------|----------|------|-----------------|-------------|----------|
| **1 (BEST)** | `scratch` | — | none | none | 0 MB | Static binary, no runtime deps |
| **2** | `wolfi` | `cgr.dev/chainguard/wolfi-base` | musl | apk | ~5 MB | Needs dynamic linking, shell for entrypoint |
| **3** | RHEL UBI micro | `registry.access.redhat.com/ubi9/ubi-micro` | glibc | microdnf | ~30 MB | Needs glibc, FIPS crypto modules |
| **4** | RHEL UBI minimal | `registry.access.redhat.com/ubi9/ubi-minimal` | glibc | dnf | ~90 MB | Needs packages not in micro |
| **5 (FALLBACK)** | RHEL UBI standard | `registry.access.redhat.com/ubi9/ubi` | glibc | dnf | ~210 MB | Complex package dependencies only |

### 1.2 Banned Base Images

| Image | Reason | Exception |
|-------|--------|-----------|
| **Alpine Linux** | musl CVE history, outdated packages, insecure default config | **None.** Not even as a final-stage runtime. Acceptable as discarded build-stage only. |
| **Debian Slim** | glibc CVE surface, large attack surface, poor minimal-image hygiene | **None.** Replaced by wolfi (smaller, more secure) or UBI (FIPS-capable). |
| **Ubuntu** | Large attack surface, automatic updates | None |
| **CentOS** | EOL, no security updates | None |
| **Amazon Linux** | AWS vendor lock-in | None |

### 1.3 Fallback Documentation

When an image cannot use the preferred base image, the reason **must** be documented:

```dockerfile
LABEL evergreen.base.image="ubi-minimal"
LABEL evergreen.base.fallback_reason="wolfi lacks package: libpq-dev-16"
```

### 1.4 Version Pinning

- All base images **must** use specific digest or version tags
- Exception: `wolfi-base:latest` with hadolint suppress (wolfi is a rolling release; `latest` IS the version)
- Build-stage images may use any tag (they are discarded)

---

## Part II: Security Constraints (C001-C030)

### 2.1 CRITICAL Constraints (BLOCKING — build fails if violated)

| ID | Constraint | Description | Verification | Resolves Conflict |
|----|-----------|-------------|--------------|-------------------|
| **C001** | Non-root execution | UID 65532 (nonroot). Never 0. | `docker inspect --format '{{.Config.User}}'` | Set 3 (UID 65534→65532) |
| **C002** | Read-only root filesystem | Must operate with `--read-only` flag | `docker run --rm --read-only $IMG touch /test` must fail | — |
| **C003** | No shell in final image (scratch/wolfi-micro) | /bin/sh, /bin/bash must not exist | `docker run --rm $IMG test -f /bin/sh` must fail | Set 9 (tier-aware) |
| **C004** | No package manager in final image | apt, apk, dnf, yum must not exist | File existence check | — |
| **C007** | Zero Critical/High CVEs | 0 CVEs rated CRITICAL or HIGH | Trivy scan | — |
| **C008** | Image signed via Cosign | Signature verification must pass | `cosign verify` | — |
| **C012** | No embedded secrets | No hardcoded credentials, API keys, tokens | TruffleHog scan | — |

### 2.2 HIGH Constraints (REQUIRED — build warns, may block)

| ID | Constraint | Description | Verification | Resolves Conflict |
|----|-----------|-------------|--------------|-------------------|
| **C005** | Static linking preferred | Binary should be statically linked where possible | `ldd /app/binary` returns "not a dynamic executable" | Set 1 (C005 unmapped) |
| **C006** | Stripped symbols | No debug symbols in final binary | `nm /app/binary` returns minimal output | Set 1 (C006 unmapped) |
| **C009** | SBOM generated | Syft SBOM in SPDX JSON format | `syft $IMG -o spdx-json` produces output | Set 1 (C009 unmapped) |
| **C010** | Health endpoints on :9101 | /livez, /readyz, /startupz served on port 9101 | HTTP GET to endpoints | Set 1 (C010 unmapped), Set 6 (HEALTHCHECK→HTTP) |
| **C013** | OCI compliant | OCI Image Spec v1.0+ manifest | Manifest field validation | Set 1 (C013 unmapped) |
| **C014** | Minimal packages | <50 installed packages for non-scratch images | Package count via dpkg/rpm/apk | Set 1 (C014 unmapped) |
| **C015** | No debug tools | gdb, strace, ltrace removed | Binary existence check | — |
| **C021** | Observability port exposed | EXPOSE 9101 in Dockerfile | Dockerfile static analysis | New |
| **C022** | Structured logging configured | Go: slog. Rust: tracing. Package: native format. | Log output validation | New |
| **C023** | No init system baked into image | No tini, dumb-init, systemd in Dockerfile | Dockerfile inspection | Set 7 (runtime --init) |

### 2.3 MEDIUM Constraints (RECOMMENDED — tracked, not blocking)

| ID | Constraint | Description | Verification | Resolves Conflict |
|----|-----------|-------------|--------------|-------------------|
| **C011** | Signal handling | Graceful SIGTERM shutdown within 10s | Kill test | — |
| **C016** | No heavyweight init system | No systemd, openrc, runit baked in | Process check | Set 7 (runtime injects init) |
| **C017** | No Docker socket | /var/run/docker.sock must not exist | File existence check | Set 1 (C017 was C008 in test_framework) |
| **C018** | No sudo/su | No privilege escalation binaries | File existence check | Set 1 (C018 was C005 in test_framework) |
| **C019** | Immutable tags | Tags never overwritten | Label check: `oci.image.immutable` | — |
| **C020** | Reproducible build | Same source produces same image hash | Build reproducibility check | — |
| **C024** | STOPSIGNAL declared | STOPSIGNAL SIGTERM in Dockerfile | Dockerfile static analysis | New |
| **C025** | Base image label | `evergreen.base.image` label present | Label check | New |
| **C026** | mTLS capability label | `evergreen.metrics.tls: native|ztunnel` | Label check | New |
| **C027** | No exposed ports except 9101 | EXPOSE only declares necessary ports | Dockerfile static analysis | Set 1 (C027 was C006 in test_framework) |
| **C028** | No writable /tmp or /var | VOLUME declarations for writable dirs | Dockerfile inspection | New |
| **C029** | Seccomp profile compatible | No disallowed syscalls in entrypoint | Profile check | — |
| **C030** | Capabilities dropped | ALL capabilities dropped by default | Capabilities check | — |

### 2.4 Constraint ID Mapping (Conflict Set 1 Resolution)

The v3.0.0 test_framework.sh had constraint IDs that did not match REQUIREMENTS.md. This table shows the correct mapping:

| REQUIREMENTS.md ID | Old test_framework.sh ID | Test Logic | New ID in Unified Spec |
|---------------------|--------------------------|------------|----------------------|
| C001 | C001 | Non-root UID | C001 (unchanged) |
| C002 | C002 | Read-only filesystem | C002 (unchanged) |
| C003 | C003 | No shell | C003 (unchanged) |
| C004 | C004 | No package manager | C004 (unchanged) |
| C005 | — | Static linking | C005 (restored from REQUIREMENTS.md) |
| C006 | — | Stripped symbols | C006 (restored from REQUIREMENTS.md) |
| — | C005 (old) | No sudo/su | **C018** (moved to MEDIUM) |
| — | C006 (old) | No network on startup | **C027** (new) |
| C007 | — | Zero CVEs | C007 (restored from REQUIREMENTS.md) |
| C008 | — | Image signed | C008 (restored from REQUIREMENTS.md) |
| — | C007 (old) | Minimal packages | **C014** (moved to HIGH) |
| — | C008 (old) | No Docker socket | **C017** (moved to MEDIUM) |
| C009 | — | SBOM generated | C009 (restored from REQUIREMENTS.md) |
| C010 | — | Health check | C010 (restored, now means :9101 endpoints) |
| — | C009 (old) | No init system | **C023** (HIGH, no baked init) |
| — | C010 (old) | Health check (Docker HEALTHCHECK) | C010 (merged) |
| — | C011 (old) | No debug tools | **C015** (moved to HIGH) |
| — | C012 (old) | Immutable tags | **C019** (moved to MEDIUM) |
| — | C013 (old) | Signed images | C008 (merged) |
| — | C014 (old) | OCI compliance | **C013** (moved to HIGH) |

---

## Part III: Observability Architecture

### 3.1 Port 9101 — Single Observability Port

All images that expose an HTTP server **must** serve the following endpoints on port **9101**:

| Endpoint | Purpose | Response | K8s Probe Mapping |
|----------|---------|----------|-------------------|
| `/metrics` | Prometheus/OpenMetrics | 200 + text/plain metrics | — |
| `/livez` | Liveness probe | 200 if process is alive | `livenessProbe.httpGet` |
| `/readyz` | Readiness probe | 200 if accepting traffic | `readinessProbe.httpGet` |
| `/startupz` | Startup probe | 200 if initialization complete | `startupProbe.httpGet` |

### 3.2 Metrics Format

- Format: Prometheus text exposition format (OpenMetrics 1.0.0 preferred)
- All metrics **must** include standard labels: `image_name`, `image_version`, `build_commit`
- Metric names **must** follow Prometheus naming conventions: `evergreen_<subsystem>_<metric>_<unit>`

### 3.3 mTLS Strategy

| Application Capability | Strategy |
|----------------------|----------|
| Application can serve TLS natively (Go `http.ServeTLS`, Rust `axum-server::bind_rustls`) | **Application handles mTLS.** Certs provided via ENV vars: `SOVEREIGN_TLS_CERT_PATH`, `SOVEREIGN_TLS_KEY_PATH`, `SOVEREIGN_TLS_CA_PATH`. |
| Application cannot serve TLS (databases, no HTTP server) | **ztunnel at node level** (Istio ambient mesh). Application serves plaintext on :9101. Mesh encrypts all pod traffic. |
| Application has no /metrics endpoint at all | Label `evergreen.metrics.native: "false"`. No per-app metrics. Only cAdvisor/container runtime metrics available. |

### 3.4 Health Shim for Database Images

Database images that lack a native HTTP server (PostgreSQL, Redis, MariaDB, MongoDB, Valkey, Kafka, ZooKeeper) **must** include a tiny Go health shim binary that:

1. Wraps the native CLI health check (`pg_isready`, `redis-cli ping`, etc.)
2. Exposes `/livez`, `/readyz`, `/startupz` on port 9101
3. Runs as a secondary process (PID > 1) alongside the database
4. The container uses runtime `--init` flag for proper PID 1 signal handling

### 3.5 Structured Logging

| Language | Framework | Output Format | Configuration |
|----------|-----------|---------------|---------------|
| **Go** (540 images) | `log/slog` (stdlib, Go 1.21+) | JSON to stdout, one object per line | `SOVEREIGN_LOG_LEVEL` ENV var (debug/info/warn/error) |
| **Rust** (~50 images) | `tracing` + `tracing-subscriber` JSON layer | JSON to stdout, one event per line | `RUST_LOG` ENV var (trace/debug/info/warn/error) |
| **Package-based** (470 images) | Native application format | Native format to stdout | Application-native ENV vars |

**Rules for all images:**
- One JSON object per line (or one log line per event)
- No pretty-print, no multi-line stack traces in structured output
- No sensitive data (passwords, tokens, PII) in log output
- Log level configurable via environment variable at runtime

---

## Part IV: Image Tier Classification

### 4.1 Tier Definitions

Tier determines **operational priority**, not base image selection. Every image uses the base image preference order from Part I regardless of tier.

| Tier | Description | SLA | Monitoring | Update Frequency |
|------|------------|-----|------------|-----------------|
| **Tier 1** | Critical trading/mission infrastructure | 24h fix | Real-time alerts, 15s scrape | Immediate on CVE |
| **Tier 2** | Supporting services | 72h fix | Standard alerts, 30s scrape | Within 24h of CVE |
| **Tier 3** | Utilities, tooling, development | 168h fix | Daily digest, 60s scrape | Weekly cadence |

### 4.2 Image Size Limits

| Tier | Maximum Size | Source |
|------|-------------|--------|
| Tier 1 | ≤ 50 MB | YP-SEC-HARDENING-001 |
| Tier 2 | ≤ 200 MB | YP-SEC-HARDENING-001 |
| Tier 3 | ≤ 500 MB | YP-SEC-HARDENING-001 |

### 4.3 Tier Labels

Every image **must** declare its tier:

```dockerfile
LABEL evergreen.image.tier="1"
```

---

## Part V: Verification & Testing

### 5.1 Static Analysis

| ID | Tool | Check | Severity on Failure |
|----|------|-------|---------------------|
| REQ-STAT-001 | Hadolint | Dockerfile best practices | WARNING |
| REQ-STAT-002 | ShellCheck | Shell script analysis | WARNING |
| REQ-STAT-003 | TruffleHog | Secret scanning | BLOCKING |
| REQ-STAT-004 | Syft | SBOM generation | REQUIRED |
| REQ-STAT-005 | Dockle | Image security posture | WARNING |
| REQ-STAT-006 | Anchore | Policy compliance | FAIL |

### 5.2 Vulnerability Scanning

| ID | Tool | CVE Threshold | Action on Failure | Frequency |
|----|------|--------------|-------------------|-----------|
| REQ-VULN-001 | Trivy | 0 Critical/High | BLOCKING | Every build |
| REQ-VULN-002 | Grype | 0 Critical/High | BLOCKING | Every build |
| REQ-VULN-003 | Snyk | 0 Critical | WARNING | Daily |
| REQ-VULN-004 | Clair | 0 High | WARNING | Every build |

### 5.3 Supply Chain

| ID | Requirement | Tool | Verification |
|----|------------|------|--------------|
| REQ-SPLY-001 | Image signing | Cosign | `cosign verify` |
| REQ-SPLY-002 | Build attestation | Cosign attest | Attestation check |
| REQ-SPLY-003 | SBOM integrity | Syft + Cosign | Cross-verification |
| REQ-SPLY-004 | Key management | HSM/TFU | Hardware-backed |
| REQ-SPLY-005 | Certificate transparency | Rekor | Log verification |
| REQ-SPLY-006 | SLSA compliance | SLSA Level 3 | Build provenance |

### 5.4 Negative Tests

| ID | Test Case | Expected Result | Automated |
|----|----------|----------------|-----------|
| REQ-TEST-001 | Shell access: `docker exec /bin/sh` | FAIL (exit non-zero) | Yes |
| REQ-TEST-002 | Root filesystem write | FAIL (read-only) | Yes |
| REQ-TEST-003 | Package manager execution | FAIL | Yes |
| REQ-TEST-004 | Privilege escalation | FAIL | Yes |
| REQ-TEST-005 | Secret in environment | Detected by TruffleHog | Yes |

---

## Part VI: OCI Compliance

### 6.1 Image Format

| ID | Requirement | Specification | Verification |
|----|------------|----------------|---------------|
| REQ-OCI-001 | OCI Image Spec v1.0+ | Manifest format | manifest.json |
| REQ-OCI-002 | Multi-arch manifests | amd64 + arm64 | `docker manifest inspect` |
| REQ-OCI-003 | Image annotations | OCI standard | Annotation check |
| REQ-OCI-004 | Layer compression | gzip or zstd | Layer inspection |

### 6.2 Required Labels

| Label | Required | Format | Example |
|-------|----------|--------|---------|
| `org.opencontainers.image.title` | YES | String | `redis` |
| `org.opencontainers.image.vendor` | YES | String | `evergreen` |
| `org.opencontainers.image.version` | YES | SemVer | `7.2.4` |
| `org.opencontainers.image.source` | YES | URL | `https://github.com/...` |
| `evergreen.image.tier` | YES | `1`, `2`, or `3` | `1` |
| `evergreen.base.image` | YES | Base image name | `scratch`, `wolfi`, `ubi-micro`, etc. |
| `evergreen.base.fallback_reason` | If applicable | Free text | `wolfi lacks libpq-dev` |
| `evergreen.metrics.native` | YES | `true` or `false` | `true` |
| `evergreen.metrics.tls` | YES | `native` or `ztunnel` | `native` |
| `evergreen.health.type` | YES | `http` or `exec` | `http` |
| `evergreen.health.command` | If exec type | Command string | `pg_isready -U postgres` |

---

## Part VII: Container Runtime Requirements

### 7.1 Security Profiles

| ID | Profile | Enforcement | Requirement |
|----|---------|-------------|-------------|
| REQ-RT-001 | seccomp | REQUIRED | Syscall filtering |
| REQ-RT-002 | AppArmor/SELinux | REQUIRED | Confinement |
| REQ-RT-003 | capabilities | ALL dropped | Capability management |
| REQ-RT-004 | no-new-privileges | REQUIRED | Security flag |

### 7.2 Resource Limits (Recommended Defaults)

| ID | Resource | Default | Notes |
|----|----------|---------|-------|
| REQ-RES-001 | memory | 512 MB | Per-container limit |
| REQ-RES-002 | cpu | 1.0 | Per-container limit |
| REQ-RES-003 | pids | 512 | Per-container limit |
| REQ-RES-004 | open files | 1024 | Per-container limit |

---

## Part VIII: Compliance Framework

### 8.1 Standards Mapping

| Standard | Scope | Evidence Location |
|----------|-------|-------------------|
| NIST SP 800-190 | Container security | `.specs/09_compliance/` |
| NIST SP 800-53 | Security controls | `compliance/ato/` |
| CIS Docker Benchmark v2.0.0 | Hardening | `compliance/cis/` |
| DISA STIG | DoD requirements | `compliance/stig/` |
| FIPS 140-2 | Cryptographic modules | `compliance/fips/` |
| OCI Image Spec v1.0 | Image format | Build verification |
| SLSA Level 3 | Supply chain | Build attestations |
| GDPR | Data handling | Policy documents |

### 8.2 Audit Requirements

| ID | Requirement | Frequency | Retention |
|----|------------|-----------|-----------|
| REQ-AUD-001 | Build audit trail | Every build | 2 years |
| REQ-AUD-002 | CVE scan logs | Every scan | 1 year |
| REQ-AUD-003 | SBOM archive | Every build | Permanent |
| REQ-AUD-004 | Key management log | All operations | Permanent |

---

## Part IX: CI/CD Pipeline

### 9.1 Pipeline Stages

1. **Discovery** — Find all Dockerfiles dynamically
2. **Lint** — Hadolint, ShellCheck, markdown, YAML validation
3. **Build** — Multi-arch Docker build (amd64 + arm64)
4. **Constraint Test** — C001-C030 verification via test_framework.sh
5. **Functional Test** — Per-image tests from test_config.yaml
6. **Security Scan** — Trivy + Grype CVE scanning
7. **SBOM** — Syft generation in SPDX format
8. **Sign** — Cosign signing and attestation
9. **Push** — GHCR.io push with immutable tags

### 9.2 Quality Gates

| Gate | Criteria | Action on Failure |
|------|----------|-------------------|
| GATE-001 | All CRITICAL constraints pass (C001-C004, C007, C008, C012) | BLOCK |
| GATE-002 | Cosign signature verified | BLOCK |
| GATE-003 | SBOM generated | WARN |
| GATE-004 | Functional tests pass | BLOCK |
| GATE-005 | Zero Critical CVEs | BLOCK |
| GATE-006 | OCI compliant | BLOCK |

---

## Part X: Scaling & Operations

### 10.1 Image Count Target

- **Current:** 1,012 functional images
- **Target:** 1,050+ images (see requiredimages.md)
- **Strategy:** Depth-first hardening, then breadth expansion

### 10.2 Deployment Compatibility

| Platform | Minimum Version |
|----------|----------------|
| Docker | 20.10+ |
| Podman | 3.4+ |
| Kubernetes | 1.21+ |
| k3s | 1.21+ |

### 10.3 Update Cadence

| ID | Update Type | Frequency |
|----|------------|-----------|
| REQ-UPD-001 | CVE rescanning | Daily |
| REQ-UPD-002 | Base image updates | Weekly |
| REQ-UPD-003 | Dependency updates | Daily |
| REQ-UPD-004 | Security patches | Immediate |

---

## Part XI: Conflict Resolution Registry

This section documents all conflicts identified between v3.0.0 REQUIREMENTS.md and v3.5.0 newrequirements.md, and their resolutions in this unified spec.

| Set | Conflict | Resolution | Section |
|-----|----------|------------|---------|
| 1 | C005-C014 ID mismatch between REQUIREMENTS.md and test_framework.sh | Remapped test IDs. Orphaned checks became C017-C030. | Part II §2.4 |
| 2 | Alpine: NEVER (REQUIREMENTS.md) vs. referenced in newrequirements.md, requiredimages.md, YP | Alpine permanently banned. All references to be cleaned. | Part I §1.2 |
| 3 | UID 65534 vs 65532 | UID 65532 (Chainguard/wolfi standard). Updated all specs. | Part II §2.1 C001 |
| 4 | Image size limits inconsistent across docs | Tier 1 ≤50MB, Tier 2 ≤200MB, Tier 3 ≤500MB (from YP-SEC-HARDENING-001). | Part IV §4.2 |
| 5 | Base image tier mapping mismatched across 3 docs | Universal preference order, not tier-based. | Part I §1.1 |
| 6 | HEALTHCHECK shell-form vs exec-form | Replaced Docker HEALTHCHECK with HTTP /livez /readyz /startupz on :9101. | Part III §3.1 |
| 7 | Init system: C016 "No init" vs ADR-004 tini | No init baked into image (C023). Runtime --init flag injects init. | Part II §2.2 C023 |
| 8 | STANDARD_CONFLICTS.md references wrong ADRs | Fixed ADR references. See STANDARD_CONFLICTS.md v2.0.0. | Part XI |
| 9 | C003 "No shell" vs debian-slim retention | debian-slim banned. C003 applies to scratch/wolfi-micro. wolfi/UBI have shell for entrypoint (acceptable). | Part I §1.2, Part II §2.1 C003 |

---

## Appendix A: Pre-Build Checklist

- [ ] Base image follows preference order: scratch > wolfi > UBI micro > UBI minimal > UBI standard
- [ ] Alpine and debian-slim are NOT used in final stage
- [ ] Base image tag is pinned (or wolfi-base:latest with hadolint suppress)
- [ ] User created with UID 65532
- [ ] Shell removed (scratch/wolfi-micro) or acceptable (wolfi/UBI for entrypoint)
- [ ] Package manager removed from final stage
- [ ] EXPOSE 9101 declared
- [ ] Labels applied (tier, base image, metrics, health)
- [ ] STOPSIGNAL SIGTERM declared
- [ ] No init system in Dockerfile
- [ ] Download URLs verified current

## Appendix B: Verification Commands

```bash
# Security verification
docker inspect --format '{{.Config.User}}' <image>          # C001: Non-root
docker run --rm --read-only <image> touch /test              # C002: Read-only
docker run --rm <image> test -f /bin/sh                     # C003: No shell
docker run --rm <image> test -f /usr/bin/apk                # C004: No package manager

# Observability verification
docker run --rm <image> wget -qO- http://localhost:9101/metrics   # C010: Metrics
docker run --rm <image> wget -qO- http://localhost:9101/livez     # C010: Liveness
docker run --rm <image> wget -qO- http://localhost:9101/readyz    # C010: Readiness

# CVE scanning
trivy image --severity CRITICAL,HIGH <image>
grype <image>

# Signing verification
cosign verify <image>

# SBOM generation
syft <image> -o spdx-json
```

## Appendix C: References

| ID | Source | Relevance |
|----|--------|-----------|
| [^1] | NIST SP 800-190 | Container security |
| [^2] | CIS Docker Benchmark v2.0.0 | Hardening |
| [^3] | OCI Image Spec v1.0 | Image format |
| [^4] | SLSA Level 3 | Supply chain |
| [^5] | Cosign docs | Signing |
| [^6] | ADR-006 | Observability architecture |
| [^7] | ADR-007 | Base image preference order |

---

**END OF UNIFIED REQUIREMENTS SPECIFICATION**
**Classification: OPERATIONAL SECURITY — ZERO-TRUST**
**Supersedes: REQUIREMENTS.md v3.0.0, newrequirements.md v2.0.0**
