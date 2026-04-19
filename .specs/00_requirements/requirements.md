# Requirements Specification - Sovereign Hardened Image Registry

## Document Metadata

| Attribute | Value |
|-----------|-------|
| Document ID | REQ-SPEC-001 |
| Version | 1.0.0 |
| Status | APPROVED |
| Created | 2026-04-19 |
| Confidence Level | 0.95 |

---

## 1. Requirements Overview

This document specifies requirements for building and maintaining a sovereign hardened container image registry with 1000+ images.

---

## 2. Mandatory Image Constraints (The Sovereign Standard)

### 2.1 Security Constraints

| ID | Requirement | Priority | Verification |
|----|-------------|----------|-------------|
| REQ-SEC-001 | Non-root execution (UID 65534) | CRITICAL | User ID check |
| REQ-SEC-002 | Read-only root filesystem | CRITICAL | Mount verification |
| REQ-SEC-003 | No shell (/bin/sh, /bin/bash) | CRITICAL | File existence check |
| REQ-SEC-004 | No package manager (apt, apk, dnf) | CRITICAL | File existence check |
| REQ-SEC-005 | Static linking (MUSL/CGO_ENABLED=0) | HIGH | ldd output check |
| REQ-SEC-006 | Stripped symbols (strip --strip-all) | HIGH | nm output check |
| REQ-SEC-007 | Zero Critical/High CVEs | CRITICAL | Trivy/Grype scan |
| REQ-SEC-008 | Signed via Cosign | CRITICAL | Cosign verify |
| REQ-SEC-009 | SBOM generated (Syft) | HIGH | SBOM file check |
| REQ-SEC-010 | Seccomp profile generated | MEDIUM | Profile existence |

### 2.2 Base Image Requirements

| ID | Requirement | Tier | Priority |
|----|-------------|------|----------|
| REQ-IMG-001 | Scratch base | Tier 1 | CRITICAL |
| REQ-IMG-002 | Distroless base | Tier 1/2 | CRITICAL |
| REQ-IMG-003 | Alpine/Wolfi base | Tier 3 | HIGH |
| REQ-IMG-004 | No latest tags | ALL | CRITICAL |

---

## 3. Verification & Testing Pipeline

### 3.1 Static Analysis Requirements

| ID | Tool | Check | Severity on Failure |
|----|------|-------|---------------------|
| REQ-STAT-001 | Hadolint | Dockerfile best practices | WARNING |
| REQ-STAT-002 | ShellCheck | Shell script analysis | WARNING |
| REQ-STAT-003 | TruffleHog | Secret scanning | BLOCKING |
| REQ-STAT-004 | Syft | SBOM generation | REQUIRED |

### 3.2 Vulnerability Scanning Requirements

| ID | Tool | CVE Threshold | Action on Failure |
|----|------|--------------|-------------------|
| REQ-VULN-001 | Trivy | 0 Critical/High | BLOCKING |
| REQ-VULN-002 | Grype | 0 Critical/High | BLOCKING |

### 3.3 Supply Chain Requirements

| ID | Requirement | Tool | Verification |
|----|-------------|------|--------------|
| REQ-SPLY-001 | Image signing | Cosign |
| REQ-SPLY-002 | Key management | HSM preferred |
| REQ-SPLY-003 | SBOM verification | Syft + Cosign |

---

## 4. Runtime Behavioral Testing

### 4.1 Negative Testing Requirements

| ID | Test | Expected Result |
|----|------|-----------------|
| REQ-TEST-001 | Shell-Check: docker exec /bin/sh | FAIL |
| REQ-TEST-002 | Root filesystem writes | FAIL (read-only) |
| REQ-TEST-003 | Package manager execution | FAIL |

### 4.2 Performance Requirements

| ID | Metric | Target | Priority |
|----|--------|--------|---------|
| REQ-PERF-001 | Startup latency | <2 seconds | HIGH |
| REQ-PERF-002 | Image size | <100MB typical | MEDIUM |
| REQ-PERF-003 | Memory usage | <128MB typical | MEDIUM |

---

## 5. Image Categories and Priorities

### 5.1 Tier Classification

| Tier | Base Image | CVE Tolerance | Image Count |
|------|------------|--------------|-------------|
| Tier 1 | Scratch/Distroless | 0 Critical/High | 380 |
| Tier 2 | Wolfi-based Distroless | 0 Critical/High | 250 |
| Tier 3 | Alpine/Wolfi | 0 Critical/High | 420 |

### 5.2 Priority Matrix

| Image Type | Build Priority | Verify Priority | Update Priority |
|------------|----------------|-----------------|------------------|
| Gateways (Traefik, Nginx) | 1 | 1 | 1 |
| Databases (Postgres, Redis) | 1 | 1 | 1 |
| Security (Vault, Keycloak) | 2 | 1 | 1 |
| Observability (Prometheus) | 2 | 2 | 2 |
| Applications | 3 | 2 | 3 |

---

## 6. Traceability Requirements

### 6.1 Required Traceability

| From | To | Method |
|------|----|--------|
| Requirements | Images | Category mapping |
| Images | Test Vectors | Automated testing |
| Scan Results | Evidence | Repository |
| SBOM | Source Code | Commit hash |

---

## 7. Compliance Requirements

### 7.1 Standards Compliance

| Standard | Requirement | Implementation |
|----------|-------------|----------------|
| NIST SP 800-190 | Container security | All images |
| CIS Docker | Configuration | Hardened Dockerfiles |
| OCI Image Spec | Image format | All images |
| FIPS 140-2 | Signing | Cosign with HSM |

---

## 8. Acceptance Criteria

### 8.1 Success Criteria

| ID | Criteria | Verification Method |
|----|----------|----------------------|
| ACC-001 | All Tier 1 images pass CVE scan | Automated |
| ACC-002 | 100% signed images | Cosign verify |
| ACC-003 | SBOM for all images | Syft output |
| ACC-004 | Seccomp profiles generated | Profile existence |
| ACC-005 | Runtime tests pass | Automated testing |

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-04-19 | Nexus | Initial creation |