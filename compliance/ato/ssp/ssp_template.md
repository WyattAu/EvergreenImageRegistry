# System Security Plan (SSP)

**System Name:** Evergreen Image Registry **Version:** 1.0.0 **Date:** 2026-04-20 **Classification:** UNCLASSIFIED //
FOUO **System Owner:** [TO BE COMPLETED] **Authorizing Official:** [TO BE COMPLETED] **Security Contact:** [TO BE
COMPLETED]

---

## 1. System Identification

### 1.1 System Name and Purpose

The Evergreen Image Registry is a hardened container image registry providing verified, reproducible container images
for deployment in environments requiring high security posture including military, government, and financial systems.

### 1.2 System Categorization

| FIPS 199 Impact Level | [LOW / MODERATE / HIGH] |
| --------------------- | ----------------------- |
| Confidentiality       | [TO BE COMPLETED]       |
| Integrity             | [TO BE COMPLETED]       |
| Availability          | [TO BE COMPLETED]       |

### 1.3 Registration Information

| Field             | Value             |
| ----------------- | ----------------- |
| System Identifier | [TO BE COMPLETED] |
| FIPS 199 Date     | [TO BE COMPLETED] |
| FISMA Reporting   | [TO BE COMPLETED] |

### 1.4 Related Systems

| System                  | Relationship                    |
| ----------------------- | ------------------------------- |
| GitHub (source control) | Source code hosting             |
| GitHub Actions (CI/CD)  | Build and verification pipeline |
| GHCR / Docker Hub       | Image distribution              |
| Trivy / Grype           | Vulnerability scanning          |
| Cosign                  | Image signing and verification  |

---

## 2. System Architecture

### 2.1 Container Registry Architecture

```
Source (Git)
    |
    v
CI Pipeline (GitHub Actions)
    |-> Build (multi-stage Dockerfiles)
    |-> Scan (Trivy, Grype, TruffleHog)
    |-> Sign (Cosign)
    |-> Test (CIS, STIG, FIPS validation)
    |-> SBOM (Syft -> SPDX)
    |-> Push (GHCR / private registry)
    v
Distribution
    |-> Online: GHCR / Docker Hub
    |-> Offline: Air-gap bundles (OCI tar)
```

### 2.2 Supply Chain

1. **Source**: Upstream binary download with SHA256 verification
2. **Build**: Multi-stage Dockerfiles from hardened base images
3. **Verification**: Checksum validation, vulnerability scanning, SBOM generation
4. **Signing**: Cosign keyless signatures (OIDC) or key-based
5. **Distribution**: Registry push with attestations
6. **Deployment**: Image pull with signature verification

### 2.3 Security Boundaries

| Boundary          | Trust Level | Controls                                        |
| ----------------- | ----------- | ----------------------------------------------- |
| Build environment | HIGH        | CI hardening, secret scanning, SAST             |
| Registry          | HIGH        | Image signing, SBOM, access control             |
| Runtime           | MEDIUM      | Non-root, read-only, capabilities restricted    |
| Air-gap bundle    | HIGH        | Checksums, offline verification, physical media |

---

## 3. Security Policy

### 3.1 Policy References

This SSP implements the security requirements defined in:

- `.specs/archive/REQUIREMENTS-v4.0.0.md` -- Unified requirements specification (v4.0.0)
- `.specs/02_architecture/` -- Architecture and design specifications
- `compliance/cis/` -- CIS Docker Benchmark compliance
- `compliance/stig/` — DISA STIG compliance
- `compliance/fips/` — FIPS 140-2 compliance

### 3.2 Security Requirements Summary

| Category                 | Requirement Source        | Implementation                           |
| ------------------------ | ------------------------- | ---------------------------------------- |
| Image integrity          | REQUIREMENTS.md C001-C005 | SHA256 checksums, Cosign signatures      |
| Vulnerability management | REQUIREMENTS.md C010-C015 | Trivy/Grype scanning in CI               |
| Access control           | REQUIREMENTS.md C018-C020 | Non-root, capabilities, seccomp          |
| Cryptography             | REQUIREMENTS.md C022-C025 | FIPS 140-2 variants, TLS 1.3             |
| Supply chain             | REQUIREMENTS.md C030-C035 | Provenance attestations, SBOM            |
| Hardening                | REQUIREMENTS.md C040-C045 | Distroless, read-only, no-new-privileges |

---

## 4. Controls Implementation

### 4.1 Controls Mapping Reference

See `compliance/ato/controls_mapping.yaml` for the full mapping of NIST SP 800-53 controls to implementation details.

### 4.2 Key Control Implementations

| Control | Description              | Implementation                            | Status            |
| ------- | ------------------------ | ----------------------------------------- | ----------------- |
| AC-6    | Least Privilege          | `cap_drop: ALL`, minimal `cap_add`        | Implemented       |
| AU-2    | Audit Logging            | Container stdout/stderr to log aggregator | Partial           |
| CM-2    | Baseline Configuration   | Multi-stage Dockerfiles, pinned versions  | Implemented       |
| CM-3    | Change Control           | Git-based, PR reviews, CI gates           | Partial           |
| IA-5    | Authentication           | Cosign verification, OIDC                 | Implemented       |
| RA-5    | Vulnerability Scanning   | Trivy + Grype in CI pipeline              | Implemented       |
| SA-11   | Developer Security       | Secret scanning (TruffleHog), SAST        | In Progress       |
| SC-8    | Transmission Protection  | TLS 1.3 enforced for all images           | Implemented       |
| SC-13   | Cryptographic Protection | FIPS 140-2 build variants                 | Planned (Phase 5) |
| SI-2    | Flaw Remediation         | Automated patching via base image bumps   | Implemented       |
| SI-7    | Software Verification    | SHA256 checksums, Cosign signatures       | Partial           |

---

## 5. Known Vulnerabilities

### 5.1 Current Vulnerability Status

| Category                         | Count             | Severity | Remediation           |
| -------------------------------- | ----------------- | -------- | --------------------- |
| Images with HIGH CVEs            | [TO BE COMPLETED] | HIGH     | Base image bump       |
| Images with unverified checksums | 52 of 115         | HIGH     | populate_checksums.py |
| Broken CI pipeline               | 1                 | MEDIUM   | Fix action references |

### 5.2 Accepted Risks

| Risk              | Justification     | Expiration        |
| ----------------- | ----------------- | ----------------- |
| [TO BE COMPLETED] | [TO BE COMPLETED] | [TO BE COMPLETED] |

---

## 6. POA&M

### 6.1 Plan of Action and Milestones

See `compliance/ato/poam/poam_current.yaml` for the current POA&M.

### 6.2 Summary

| Severity  | Open  | In Progress | Total |
| --------- | ----- | ----------- | ----- |
| High      | 3     | 2           | 5     |
| Medium    | 3     | 0           | 3     |
| Low       | 0     | 0           | 0     |
| **Total** | **6** | **2**       | **8** |

---

## Appendix A: Acronyms

| Acronym | Definition                                     |
| ------- | ---------------------------------------------- |
| ATO     | Authority to Operate                           |
| CKL     | Security Content Automation Protocol Checklist |
| CIS     | Center for Internet Security                   |
| DISA    | Defense Information Systems Agency             |
| FIPS    | Federal Information Processing Standards       |
| NIST    | National Institute of Standards and Technology |
| POA&M   | Plan of Action and Milestones                  |
| SBOM    | Software Bill of Materials                     |
| SSP     | System Security Plan                           |
| STIG    | Security Technical Implementation Guide        |
| VEX     | Vulnerability Exploitability eXchange          |

---

## Appendix B: Document History

| Version | Date       | Author    | Changes          |
| ------- | ---------- | --------- | ---------------- |
| 1.0.0   | 2026-04-20 | Generated | Initial template |

---

**END OF SYSTEM SECURITY PLAN**
