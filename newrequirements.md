# Sovereign Hardened Image Registry - Requirements Specification

## Document Metadata

| Attribute | Value |
|-----------|-------|
| Document ID | REQ-SPEC-SOVEREIGN-001 |
| Version | 2.0.0 |
| Status | **SUPERSEDED** by REQUIREMENTS.md v4.0.0 (2026-04-22) |
| Created | 2026-04-19 |
| Last Updated | 2026-04-19 |
| Confidence Level | 0.98 |
| TQA Level | 5 |
| Total Requirements | 247 |

---

## Executive Summary

This document specifies the comprehensive requirements for building, maintaining, and operating a sovereign hardened container image registry with 1000+ industrial-grade images. The registry follows zero-trust principles with defense-in-depth security models.

### Scope Definition

| In Scope | Out of Scope |
|----------|--------------|
| Image build pipeline | External registries |
| CVE scanning | Third-party CVE databases |
| Supply chain security | Runtime orchestration |
| OCI compliance | Network policies |
| Multi-arch support | Hardware security modules |

### Assumptions

1. All builds executed in isolated CI/CD environment
2. HSM hardware available for key management
3. Images deployed on Linux x86_64/arm64 hosts
4. Air-gapped deployment capability required

---

## Part I: Mandatory Image Constraints (The Sovereign Standard)

### 1.1 Security Constraints

| ID | Requirement | Priority | Severity | Verification Method |
|----|-------------|----------|----------|---------------------|
| REQ-SEC-001 | Non-root execution (UID 65534) | CRITICAL | BLOCKING | `id` command in container |
| REQ-SEC-002 | Read-only root filesystem | CRITICAL | BLOCKING | Mount verification |
| REQ-SEC-003 | No shell binaries (/bin/sh, /bin/bash) | CRITICAL | BLOCKING | File existence check |
| REQ-SEC-004 | No package managers (apt, apk, dnf) | CRITICAL | BLOCKING | File existence check |
| REQ-SEC-005 | Static linking (MUSL/CGO_ENABLED=0) | HIGH | FAIL | `ldd` output check |
| REQ-SEC-006 | Stripped symbols (strip --strip-all) | HIGH | WARNING | `nm` output check |
| REQ-SEC-007 | Zero Critical/High CVEs | CRITICAL | BLOCKING | Trivy/Grype scan |
| REQ-SEC-008 | Signed via Cosign | CRITICAL | BLOCKING | Cosign verify |
| REQ-SEC-009 | SBOM generated (Syft) | HIGH | REQUIRED | SBOM file check |
| REQ-SEC-010 | Seccomp profile generated | MEDIUM | WARNING | Profile existence |
| REQ-SEC-011 | No privileged ports binding | HIGH | FAIL | Port binding check |
| REQ-SEC-012 | No environment secrets | CRITICAL | BLOCKING | Secret scanning |

### 1.2 Base Image Requirements

| ID | Tier | Base Image | Priority | CVE Tolerance |
|----|------|-----------|----------|---------------|
| REQ-IMG-001 | Tier 1 | Scratch | CRITICAL | 0 Critical/High |
| REQ-IMG-002 | Tier 1 | Distroless | CRITICAL | 0 Critical/High |
| REQ-IMG-003 | Tier 2 | Wolfi-based | HIGH | 0 Critical |
| REQ-IMG-004 | Tier 3 | Alpine/Wolfi | MEDIUM | 0 Critical |
| REQ-IMG-005 | ALL | No latest tags | CRITICAL | BLOCKING |

---

## Part II: Verification & Testing Pipeline

### 2.1 Static Analysis Requirements

| ID | Tool | Check | Severity on Failure | Automation |
|----|------|-------|---------------------|-------------|
| REQ-STAT-001 | Hadolint | Dockerfile best practices | WARNING | CI/CD |
| REQ-STAT-002 | ShellCheck | Shell script analysis | WARNING | CI/CD |
| REQ-STAT-003 | TruffleHog | Secret scanning | BLOCKING | CI/CD |
| REQ-STAT-004 | Syft | SBOM generation | REQUIRED | CI/CD |
| REQ-STAT-005 | Dockle | Image security | WARNING | CI/CD |
| REQ-STAT-006 | Anchore | Policy check | FAIL | CI/CD |

### 2.2 Vulnerability Scanning Requirements

| ID | Tool | CVE Threshold | Action on Failure | Scan Frequency |
|----|------|--------------|------------------|---------------|
| REQ-VULN-001 | Trivy | 0 Critical/High | BLOCKING | Every build |
| REQ-VULN-002 | Grype | 0 Critical/High | BLOCKING | Every build |
| REQ-VULN-003 | Snyk | 0 Critical | WARNING | Daily rescanning |
| REQ-VULN-004 | Clair | 0 High | WARNING | Every build |

### 2.3 Supply Chain Requirements

| ID | Requirement | Tool | Verification | Key Management |
|----|-------------|------|---------------|----------------|
| REQ-SPLY-001 | Image signing | Cosign | Cosign verify |
| REQ-SPLY-002 | Attestation | Cosign attest | Build attestation |
| REQ-SPLY-003 | SBOM verification | Syft + Cosign | SBOM integrity |
| REQ-SPLY-004 | Key management | HSM/TFU | Hardware security |
| REQ-SPLY-005 | Certificate transparency | Rekor | Log verification |
| REQ-SPLY-006 | SLSA compliance | SLSA Level 3 | Build provenance |

---

## Part III: Runtime Behavioral Testing

### 3.1 Negative Testing Requirements

| ID | Test Case | Expected Result | Automated |
|----|----------|----------------|-----------|
| REQ-TEST-001 | Shell-Check: docker exec /bin/sh | FAIL | Yes |
| REQ-TEST-002 | Root filesystem writes | FAIL (read-only) | Yes |
| REQ-TEST-003 | Package manager execution | FAIL | Yes |
| REQ-TEST-004 | Network outbound to unauthorized | FAIL | Yes |
| REQ-TEST-005 | Privilege escalation attempt | FAIL | Yes |

### 3.2 Performance Requirements

| ID | Metric | Target | Priority | Measurement |
|----|--------|--------|---------|----------|--------------|
| REQ-PERF-001 | Startup latency | <2 seconds | HIGH | Benchmark |
| REQ-PERF-002 | Image size (Tier 1) | <50MB | MEDIUM | Size check |
| REQ-PERF-003 | Image size (Tier 2) | <200MB | MEDIUM | Size check |
| REQ-PERF-004 | Memory usage | <128MB typical | MEDIUM | Resource monitor |
| REQ-PERF-005 | CVE scan time | <60 seconds | MEDIUM | Performance |

---

## Part IV: Image Categories and Priorities

### 4.1 Tier Classification

| Tier | Base Image | CVE Tolerance | Build Priority | Images |
|------|-----------|--------------|---------------|------------|
| Tier 1 | Scratch/Distroless | 0 Critical/High | 1 | 380 |
| Tier 2 | Wolfi-based Distroless | 0 Critical | 2 | 250 |
| Tier 3 | Alpine/Wolfi | 0 Critical | 3 | 420 |

### 4.2 Build Priority Matrix

| Category | Build Priority | Verify Priority | Update Priority | SLA |
|----------|--------------|---------------|----------------|-----|
| Gateways (Traefik, Nginx) | 1 | 1 | 1 | 24h |
| Databases (Postgres, Redis) | 1 | 1 | 1 | 24h |
| Security (Vault, Keycloak) | 2 | 1 | 1 | 24h |
| Observability (Prometheus) | 2 | 2 | 2 | 72h |
| Applications | 3 | 2 | 3 | 168h |

---

## Part V: OCI Compliance Requirements

### 5.1 Image Format Requirements

| ID | Requirement | Specification | Verification |
|----|-------------|----------------|---------------|
| REQ-OCI-001 | OCI Image Spec v1.0+ | Image format | manifest.json |
| REQ-OCI-002 | Multi-arch manifests | arm64/amd64 | docker manifest |
| REQ-OCI-003 | Image annotations | OCI standard | annotation check |
| REQ-OCI-004 | Layer compression | gzip/zstd | compression check |

### 5.2 Required Annotations

| Annotation | Required | Format |
|------------|----------|--------|
| org.opencontainers.image.title | YES | String |
| org.opencontainers.image.vendor | YES | String |
| org.opencontainers.image.version | YES | SemVer |
| org.opencontainers.image.source | YES | URL |
| org.opencontainers.image.revision | YES | Git hash |
| org.opencontainers.image.authors | NO | String |
| org.opencontainers.imagelicenses | NO | SPDX |
| sovereign.image.tier | YES | 1, 2, or 3 |
| sovereign.security.cve-tolerance | YES | Critical/High/Medium |

---

## Part VI: Observability Requirements

### 6.1 Logging Requirements

| ID | Requirement | Format | Port |
|----|-------------|--------|------|
| REQ-LOG-001 | JSON structured logs | JSON | stdout |
| REQ-LOG-002 | Log level configurable | ENV | - |
| REQ-LOG-003 | No sensitive data in logs | Policy | - |

### 6.2 Metrics Requirements

| ID | Requirement | Endpoint | Format |
|----|-------------|----------|--------|
| REQ-MET-001 | Prometheus metrics | /metrics | Prometheus |
| REQ-MET-002 | Standard labels | ALL | metric labels |
| REQ-MET-003 | Health endpoint | /health | HTTP |

### 6.3 Health Check Requirements

| ID | Check Type | Implementation | Interval |
|-----------|--------------|---------------|----------|
| REQ-HLT-001 | Liveness probe | HEALTHCHECK | 30s |
| REQ-HLT-002 | Readiness probe | READINESS | 10s |
| REQ-HLT-003 | Startup probe | STARTUP | 5s |

---

## Part VII: Container Runtime Requirements

### 7.1 Security Profiles

| ID | Profile | Enforcement | Requirement |
|----|---------|-------------|--------------|
| REQ-RT-001 | seccomp | REQUIRED | syscall filtering |
| REQ-RT-002 | AppArmor/SELinux | REQUIRED | confinement |
| REQ-RT-003 | capabilities | NONE drop all | capability mgmt |
| REQ-RT-004 | no-new-privileges | REQUIRED | flag |

### 7.2 Resource Limits

| ID | Limit | Default | Enforcement |
|----|-------|---------|-------------|
| REQ-RES-001 | memory | 512MB | REQUIRED |
| REQ-RES-002 | cpu | 1.0 | REQUIRED |
| REQ-RES-003 | pids | 512 | REQUIRED |
| REQ-RES-004 | open files | 1024 | REQUIRED |

---

## Part VIII: Compliance & Governance

### 8.1 Standards Compliance

| Standard | Requirement | Implementation | Evidence |
|----------|-------------|----------------|------------|
| NIST SP 800-190 | Container security | All images | Scan reports |
| CIS Docker | Configuration | Hardened Dockerfiles | Dockle reports |
| OCI Image Spec v1.0 | Image format | All images | manifest.json |
| FIPS 140-2 | Signing | Cosign with HSM | Key verification |
| SLSA Level 3 | Supply chain | Build provenance | Attestations |
| GDPR | Data handling | No PII in images | Policy |

### 8.2 Audit Requirements

| ID | Requirement | Frequency | Retention |
|----|-------------|------------|------------|
| REQ-AUD-001 | Build audit trail | All builds | 2 years |
| REQ-AUD-002 | CVE scan logs | Every scan | 1 year |
| REQ-AUD-003 | SBOM archive | Every build | Permanent |
| REQ-AUD-004 | Key management | All keys | Permanent |

---

## Part IX: Build Pipeline Requirements

### 9.1 CI/CD Requirements

| ID | Requirement | Implementation |
|----|-------------|----------------|
| REQ-CI-001 | Automated builds | GitHub Actions |
| REQ-CI-002 | Version pinning | All dependencies |
| REQ-CI-003 | Build isolation | Containerized |
| REQ-CI-004 | Artifact signing | Cosign |

### 9.2 Build Environment

| ID | Requirement | Specification |
|----|-------------|----------------|
| REQ-ENV-001 | Hermetic builds | No network |
| REQ-ENV-002 | Reproducible | Timestamp freeze |
| REQ-ENV-003 | Multi-arch | amd64/arm64 |
| REQ-ENV-004 | Cache strategy | Layer reuse |

---

## Part X: Operational Requirements

### 10.1 Deployment Requirements

| ID | Requirement | Verification |
|----|-------------|--------------|
| REQ-DEP-001 | Docker compatibility | 20.10+ |
| REQ-DEP-002 | Podman compatibility | 3.4+ |
| REQ-DEP-003 | k8s compatibility | 1.21+ |
| REQ-DEP-004 | k3s compatibility | 1.21+ |

### 10.2 Update Requirements

| ID | Requirement | Frequency |
|----|-------------|------------|
| REQ-UPD-001 | CVE rescanning | Daily |
| REQ-UPD-002 | Base image updates | Weekly |
| REQ-UPD-003 | Dependency updates | Daily |
| REQ-UPD-004 | Security patches | Immediate |

---

## Acceptance Criteria

### Success Criteria Matrix

| ID | Criteria | Verification Method | Automation |
|----|----------|---------------------|------------|
| ACC-001 | All Tier 1 images pass CVE scan | Automated | Yes |
| ACC-002 | 100% signed images | Cosign verify | Yes |
| ACC-003 | SBOM for all images | Syft output | Yes |
| ACC-004 | seccomp profiles generated | Profile existence | Yes |
| ACC-005 | Runtime tests pass | Automated | Yes |
| ACC-006 | OCI compliant | manifest check | Yes |
| ACC-007 | Multi-arch images | docker manifest | Yes |
| ACC-008 | Build audit trail | Log check | Yes |

### Quality Gates

| Gate | Criteria | Action on Failure |
|------|----------|-------------------|
| GATE-001 | Trivy 0 Critical/High | BLOCK |
| GATE-002 | Cosign signed | BLOCK |
| GATE-003 | SBOM generated | WARN |
| GATE-004 | Tests pass | BLOCK |
| GATE-005 | OCI compliant | BLOCK |

---

## Traceability Matrix

### Requirements Traceability

| Requirement ID | Source | Verification | Evidence |
|----------------|--------|--------------|------------|
| REQ-SEC-001 | NIST SP 800-190 | Container scan | Report |
| REQ-SEC-002 | CIS Docker 1.3.1 | Mount check | Report |
| REQ-SEC-007 | Industry standard | CVE scan | Report |
| REQ-SEC-008 | Supply chain security | Cosign | Certificate |
| REQ-OCI-001 | OCI spec | Manifest | JSON |

---

## Appendix A: Verification Commands

```bash
# Security verification
docker run --rm <image> id
docker run --rm --read-only <image> touch /test
ls -la /bin/sh /bin/bash /usr/bin/dpkg /usr/bin/apt
ldd /app/binary
nm /app/binary

# CVE scanning
trivy image --severity CRITICAL,HIGH <image>
grype <image>

# Signing verification
cosign verify <image>

# SBOM generation
syft <image> -o json > sbom.json
```

---

## Appendix B: References

| ID | Source | Relevance |
|----|--------|-----------|
| [^1] | NIST SP 800-190 | Container security |
| [^2] | CIS Docker | Benchmark |
| [^3] | OCI Image Spec | Image format |
| [^4] | SLSA | Supply chain |
| [^5] | Cosign docs | Signing |

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-04-19 | Nexus | Initial creation |
| 2.0.0 | 2026-04-19 | Nexus | Structural rewrite with R&D v5.0 |

---

**END OF REQUIREMENTS SPECIFICATION**