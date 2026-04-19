# Cross-Paper Traceability Matrix

## Document Metadata

| Attribute | Value |
|-----------|-------|
| Document ID | TRACE-MATRIX-001 |
| Version | 1.0.0 |
| Status | APPROVED |
| Created | 2026-04-19 |

---

## Yellow Paper to Yellow Paper Dependencies

| Source YP | Target YP | Dependency Type | Elements |
|-----------|-----------|-----------------|----------|
| YP-SUPPLY-CHAIN-001 | YP-SEC-HARDENING-001 | provides-axioms | AX-SEC-001, AX-SEC-002 |
| YP-OBSERVABILITY-001 | YP-SEC-HARDENING-001 | uses-axioms | AX-SEC-001 |

## Yellow Paper to Blue Paper Mapping

| Yellow Paper | Blue Paper | Elements Used | Verification |
|--------------|------------|---------------|--------------|
| YP-SEC-HARDENING-001 | BP-IMAGE-REGISTRY-001 | THM-001, ALG-001 | Unit + Proof |
| YP-VULN-SCAN-001 | BP-IMAGE-REGISTRY-001 | THM-002, ALG-002 | Unit + Integration |
| YP-SUPPLY-CHAIN-001 | BP-SECURITY-001 | THM-003, ALG-003 | Unit + Integration |
| YP-OBSERVABILITY-001 | BP-IMAGE-REGISTRY-001 | THM-004 | Unit |

## Blue Paper to Blue Paper Dependencies

| Blue Paper | Depends On | Interface |
|------------|-----------|-----------|
| BP-IMAGE-REGISTRY-001 | BP-SECURITY-001 | IF-SEC-SCAN-001 |
| BP-SECURITY-001 | None | N/A |

## Requirement Coverage by Papers

| Requirement | Yellow Paper(s) | Blue Paper(s) | Test Coverage |
|-------------|-----------------|---------------|---------------|
| REQ-SEC-001 (Non-root) | YP-SEC-HARDENING-001 | BP-IMAGE-REGISTRY-001 | TV-HARD-001 |
| REQ-SEC-002 (Read-only) | YP-SEC-HARDENING-001 | BP-IMAGE-REGISTRY-001 | TV-HARD-002 |
| REQ-SEC-003 (No shell) | YP-SEC-HARDENING-001 | BP-IMAGE-REGISTRY-001 | TV-HARD-003 |
| REQ-SEC-004 (No pkg mgr) | YP-SEC-HARDENING-001 | BP-IMAGE-REGISTRY-001 | TV-HARD-004 |
| REQ-SEC-005 (Static) | YP-SEC-HARDENING-001 | BP-IMAGE-REGISTRY-001 | TV-HARD-005 |
| REQ-SEC-006 (Stripped) | YP-SEC-HARDENING-001 | BP-IMAGE-REGISTRY-001 | TV-HARD-006 |
| REQ-SEC-007 (0 CVEs) | YP-VULN-SCAN-001 | BP-SECURITY-001 | TV-HARD-007 |
| REQ-SEC-008 (Cosign) | YP-SUPPLY-CHAIN-001 | BP-SECURITY-001 | TV-HARD-008 |
| REQ-SEC-009 (SBOM) | YP-SUPPLY-CHAIN-001 | BP-SECURITY-001 | TV-HARD-009 |
| REQ-LOG-001 (JSON logs) | YP-OBSERVABILITY-001 | BP-IMAGE-REGISTRY-001 | N/A |
| REQ-METRICS-001 (Prometheus) | YP-OBSERVABILITY-001 | BP-IMAGE-REGISTRY-001 | N/A |

## Standard Compliance Traceability

| Standard | Requirement | Yellow Paper | Blue Paper | Evidence |
|-----------|-------------|-------------|------------|------------|
| NIST SP 800-190 | Container security | YP-SEC-HARDENING-001 | BP-IMAGE-REGISTRY-001 | Test vectors |
| NIST SP 800-53 | Security controls | YP-VULN-SCAN-001 | BP-SECURITY-001 | Scan reports |
| FIPS 140-2 | Signing | YP-SUPPLY-CHAIN-001 | BP-SECURITY-001 | Key cert |
| OCI Image Spec | Image format | YP-SEC-HARDENING-001 | BP-IMAGE-REGISTRY-001 | Manifest |
| SLSA Level 3 | Supply chain | YP-SUPPLY-CHAIN-001 | BP-SECURITY-001 | Attestations |

## Test Vector Coverage

| Category | Yellow Paper | Test Vectors | Coverage % |
|----------|--------------|--------------|-------------|
| Nominal | YP-SEC-HARDENING-001 | TV-HARD-001..010 | 40% |
| Boundary | YP-SEC-HARDENING-001 | TV-HARD-003,006 | 20% |
| Adversarial | YP-SEC-HARDENING-001 | TV-HARD-011 | 15% |
| Regression | All | N/A | 10% |
| Random | All | N/A | 15% |

## Verification Status

| Element | Type | Status | Last Verified |
|---------|------|--------|---------------|
| AX-SEC-001 | Axiom | VERIFIED | 2026-04-19 |
| AX-SEC-002 | Axiom | VERIFIED | 2026-04-19 |
| THM-001 | Theorem | VERIFIED | 2026-04-19 |
| THM-002 | Theorem | PENDING | N/A |
| ALG-001 | Algorithm | VERIFIED | 2026-04-19 |
| ALG-002 | Algorithm | PENDING | N/A |

---

## Document Control

| Version | Date | Changes |
|----------|------|---------|
| 1.0.0 | 2026-04-19 | Initial creation |

**END OF TRACEABILITY MATRIX**