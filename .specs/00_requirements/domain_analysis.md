# Domain Analysis - Sovereign Hardened Image Registry

## Document Metadata

| Attribute | Value |
|-----------|-------|
| Document ID | REQ-DOMAIN-001 |
| Version | 1.0.0 |
| Status | APPROVED |
| Created | 2026-04-19 |
| Author | Nexus Systems Architect |
| Confidence Level | 0.95 |
| TQA Level | 4 |

---

## 1. Executive Summary

The Evergreen Image Registry is designed as a sovereign hardened container image registry providing industrial-grade security-hardened container images. The domain covers the full lifecycle of building, verifying, signing, and maintaining 1000+ container images with zero-trust security principles.

---

## 2. Applicable Standards

### 2.1 Primary Standards

| Standard | Domain | Relevance | Clauses |
|----------|--------|-----------|---------|
| NIST SP 800-53 | Security & Privacy Controls | Container hardening, supply chain security | AC-6, AU-2, AU-3, SC-3, SC-4, SC-8, SI-2, SI-3, SA-10 |
| NIST SP 800-190 | Container Security | Image vulnerability, configuration, runtime | All |
| FIPS 140-2/3 | Cryptographic Modules | Image signing, encryption | Module validation |
| ISO/IEC 27001 | Information Security | Management system | A.8.2, A.8.12, A.14.2 |
| CIS Docker Benchmark | Container Hardening | Configuration benchmarks | All levels |
| PCI-DSS | Payment Data | If storing credentials | Req 6.3, 6.4, 8.2 |
| GDPR | EU Data Protection | If processing EU data | Art 25, 32, 33 |

### 2.2 Compliance Matrix

| Requirement ID | Standard | Clause | Requirement | Implementation Priority |
|----------------|----------|--------|-------------|----------------------|
| SEC-001 | NIST SP 800-53 | SC-4 | Information flow enforcement | CRITICAL |
| SEC-002 | NIST SP 800-53 | SC-8 | Transmission confidentiality | CRITICAL |
| SEC-003 | NIST SP 800-53 | SI-2 | Flaw remediation | CRITICAL |
| SEC-004 | NIST SP 800-190 | 2.1 | Base image requirements | CRITICAL |
| SEC-005 | NIST SP 800-190 | 2.2 | Image configuration | CRITICAL |
| SEC-006 | NIST SP 800-190 | 2.3 | Application origin | CRITICAL |
| SEC-007 | NIST SP 800-190 | 3.1 | Container runtime | CRITICAL |
| SEC-008 | NIST SP 800-190 | 3.2 | Hosted container | CRITICAL |
| SEC-009 | CIS Docker | 1.1 | Container Host Configuration | CRITICAL |
| SEC-010 | CIS Docker | 2.1 | Container Images | CRITICAL |
| SEC-011 | FIPS 140-2 | 4 | Cryptographic module | HIGH |
| SEC-012 | ISO 27001 | A.8.12 | Code security | CRITICAL |

---

## 3. Multi-Lingual Requirements

### 3.1 Primary Languages

| Language | Resources | TQA Level | Use Case |
|----------|-----------|-----------|----------|
| EN | Docker Official, GitHub, upstream | 5 | Primary documentation |
| ZH | cnblogs.com, zhihu, csdn | 3 | Chinese community support |
| DE | heise, techcommunity | 3 | European enterprise support |
| FR | LeMonde, lesnumeriques | 3 | French community support |
| JP | jp.internet.com, gihyo | 3 | Japanese community support |

### 3.2 Internationalization Coverage

| Image Category | EN Priority | ZH Priority | DE Priority | JP Priority |
|----------------|------------|------------|-------------|-------------|
| Core Infrastructure | 100% | 60% | 80% | 60% |
| Databases | 100% | 40% | 60% | 40% |
| Security | 100% | 80% | 90% | 80% |
| Applications | 100% | 30% | 50% | 30% |

---

## 4. Domain Specific Analysis

### 4.1 Core Domain

**Primary:** Container Image Registry Management
**Sub-domains:**
- Container image hardening (distroless, scratch)
- Vulnerability scanning and remediation
- Image signing and verification
- Supply chain security
- Runtime security enforcement

### 4.2 Technical Boundaries

| Boundary | Definition | In-Scope |
|----------|------------|----------|
| Input | Source code, Dockerfiles | Yes |
| Processing | Build, scan, sign, verify | Yes |
| Output | Signed, verified container images | Yes |
| Storage | OCI registry distribution | Yes |
| Runtime | Container orchestration | Out of scope |

### 4.3 Domain Constraints

| ID | Constraint | Value | Source |
|----|------------|-------|--------|
| DC-001 | Max CVE tolerance | 0 Critical/High | Tier 1 requirement |
| DC-002 | Image signing | Cosign required | Supply chain |
| DC-003 | Base image | Scratch/Distroless preferred | Hardening |
| DC-004 | Non-root execution | UID 65534 | Security |
| DC-005 | Size limit | <100MB typical | Performance |

---

## 5. Risk Assessment

### 5.1 Domain-Specific Risks

| Risk ID | Risk | Probability | Impact | Mitigation |
|--------|------|-------------|--------|------------|
| DR-001 | Supply chain attack | High | Critical | Cosign verification |
| DR-002 | Zero-day CVE | Med | Critical | 24h rescanning |
| DR-003 | Kernel incompatibility | Low | High | Version testing |
| DR-004 | Signing key compromise | Low | Critical | HSM storage |
| DR-005 | Image drift/rot | High | High | Continuous rescanning |

### 5.2 Critical Path Risks (CPR)

| CPR ID | Risk | Phase | Impact |
|-------|------|-------|--------|
| CPR-001 | Build infrastructure availability | Phase 1 | High |
| CPR-002 | CVE scanner accuracy | Phase 1 | High |
| CPR-003 | Supply chain security | Phase 2 | Critical |
| CPR-004 | Performance regression | Phase 4 | Medium |

---

## 6. Capability Requirements

### 6.1 Required Capabilities

| Capability | Tool | Priority | Phase |
|-----------|------|----------|-------|
| Build | Docker/BuildKit | CRITICAL | -0.5 |
| Scan | Trivy/Grype | CRITICAL | 0 |
| Sign | Cosign | CRITICAL | 0 |
| Verify | Cosign/Clair | CRITICAL | 0 |
| SBOM | Syft | CRITICAL | 0 |
| Test | Docker/Compose | CRITICAL | 5 |
| Container orchestration | Docker Compose / K8s | HIGH | 5 |

### 6.2 Tool Requirements

| Tool | Min Version | Purpose |
|------|-------------|---------|
| docker | 20.10+ | Building images |
| trivy | 0.44+ | Vulnerability scanning |
| grype | 0.60+ | Alternative scanning |
| cosign | 1.11+ | Image signing |
| syft | 0.68+ | SBOM generation |
| hadolint | 2.10+ | Dockerfile linting |

---

## 7. Stakeholder Analysis

| Stakeholder | Role | Concerns | Priority |
|------------|------|----------|----------|
| Security Operations | Primary | Zero trust, CVE-free | CRITICAL |
| DevOps Engineers | Secondary | Easy integration | HIGH |
| Compliance Officers | Secondary | Audit trail, evidence | HIGH |
| End Users | Tertiary | Documentation, support | MEDIUM |

---

## 8. Verification Summary

This domain analysis confirms:
- Applicability of NIST SP 800-190, NIST SP 800-53, CIS Docker
- Multi-lingual requirement scope defined
- Supply chain security as primary risk
- 100% image signing requirement
- Continuous vulnerability rescanning requirement

**Conclusion:** Domain is well-defined for sovereign hardened image registry with clear compliance requirements.

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-04-19 | Nexus | Initial creation |

---

## Appendix A: Glossary

| Term | Definition |
|------|-----------|
| Distroless | Minimal container image with only application and dependencies |
| Scratch | Empty base image with no OS |
| SBOM | Software Bill of Materials |
| CVE | Common Vulnerabilities and Exposures |
| OCI | Open Container Initiative |
| Cosign | Container image signing tool |
| Trivy | Vulnerability scanner for containers |
| Grype | Alternative vulnerability scanner |
| Wolfi | Melange-built minimal Linux distribution |