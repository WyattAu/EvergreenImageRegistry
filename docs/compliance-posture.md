# EIR Compliance Posture

> **Last Updated:** July 2026  
> **Status:** Evidence-generating, not certified

## Important Disclaimer

EIR is a **community/self-hosted project**. It is NOT:
- FIPS 140-2/3 certified (NIST CMVP certification requires accredited lab testing)
- STIG certified (DISA accreditation required)
- SOC 2 audited (independent CPA audit required)
- FedRAMP authorized (GSA authorization required)

EIR **CAN** provide:
- Automated evidence collection for compliance frameworks
- Scanning and gap analysis
- Documentation of controls and their implementation status
- Configuration baselines that align with compliance requirements

Organizations pursuing formal certification can use EIR's evidence as input to their own certification process.

## Current Compliance Status

| Framework | Status | Evidence Available | Path to Certification |
|-----------|--------|--------------------|-----------------------|
| **FIPS 140-2/3** | 🟡 Evidence | FIPS readiness scan results | Requires NIST CMVP lab testing of crypto modules |
| **CIS Docker Benchmark** | 🟡 Evidence | CIS scan results per image | Self-attestation or third-party assessment |
| **DISA STIG** | 🟡 Evidence | STIG hardening profiles | Requires DISA SRG review and approval |
| **NIST 800-53 (ATO)** | 🟡 Evidence | Controls mapping | Requires Authorizing Official approval |
| **SOC 2** | 🔴 Not started | N/A | Requires independent CPA audit |
| **PCI DSS** | 🔴 Not started | N/A | Requires QSA assessment |
| **FedRAMP** | 🔴 Not started | N/A | Requires 3PAO assessment + GSA authorization |

## FIPS 140-2/3

### What EIR Provides
- `scripts/fips_scan.sh` — Scans images for OpenSSL FIPS capability
- `compliance/fips/` — Implementation plans for 30 critical images
- Wolfi-based images use glibc with FIPS-capable OpenSSL

### What EIR Cannot Provide
- NIST CMVP certification of the OpenSSL FIPS module
- FIPS certificate numbers
- Entropy validation (requires hardware-specific testing)

### Recommendation
Use EIR FIPS scan results as evidence in your own FIPS assessment. The wolfi-fips base images from Chainguard have undergone more rigorous FIPS validation.

## CIS Docker Benchmark

### What EIR Provides
- `scripts/cis_scan.sh` — Automated CIS benchmark checks per image
- Checks implemented:
  - CIS 4.1: Non-root user
  - CIS 4.6: HEALTHCHECK present
  - SUID/SGID file audit
  - Shell presence audit

### What EIR Cannot Provide
- Full CIS benchmark coverage (network, host-level controls)
- Continuous monitoring platform
- Third-party attestation

## DISA STIG

### What EIR Provides
- `compliance/stig/` — STIG hardening profiles
- Security labels on Dockerfiles (`evergreen.security.*`)
- Configuration baselines for common STIG requirements

### What EIR Cannot Provide
- DISA SRG (Security Requirements Guide) compliance
- STIG review and approval
- Continuous STIG monitoring (SCAP scanning)

## NIST 800-53 (ATO)

### What EIR Provides
- `compliance/ato/` — Controls mapping to NIST 800-53 families
- Supply chain artifacts (SBOM, signatures, provenance) satisfy:
  - CM-3: Configuration Change Control
  - CM-5: Access Restrictions for Change
  - CM-6: Configuration Settings
  - CM-8: Information System Component Inventory
  - SA-12: Supply Chain Protection
  - SI-7: Software, Firmware, and Information Integrity

### What EIR Cannot Provide
- Full NIST 800-53 control implementation
- Authorizing Official (AO) approval
- System Security Plan (SSP) — template only
- Plan of Action and Milestones (POA&M) — template only
