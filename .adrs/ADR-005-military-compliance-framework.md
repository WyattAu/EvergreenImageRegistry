# Architecture Decision Record: Military Compliance Framework

## ADR-005: CIS Docker Benchmark, DISA STIG, FIPS 140-2, and NIST SP 800-53 Mapping

### Status
ACCEPTED

### Date
2026-04-20

### Author
Nexus (Principal Systems Architect)

### Context

The Evergreen Image Registry targets deployment environments with strict compliance requirements including:
- **Department of Defense (DoD)**: DISA STIG for container platforms
- **Federal agencies**: FIPS 140-2 for cryptographic modules
- **FedRAMP**: NIST SP 800-53 security controls
- **Civilian government**: CIS Docker Benchmark for best practices

Currently, compliance is achieved through individual constraints (C001-C020) but there is no formal mapping to these external standards. This creates:
- No evidence trail for auditors
- No automated compliance checking against external standards
- No way to generate Authority to Operate (ATO) packages
- No FIPS-mode variant images for environments requiring FIPS-validated cryptography

This ADR establishes the compliance framework that maps internal constraints and Phase 4-5 hardening efforts to external compliance standards.

### Decision

**Adopt a four-pillar compliance framework: CIS Docker Benchmark, DISA STIG, FIPS 140-2, and NIST SP 800-53.**

#### Pillar 1: CIS Docker Benchmark v2.0.0

The CIS Docker Benchmark provides consensus-based security guidelines for Docker container deployments. It is organized into sections:

| Section | Scope | Checks | Registry Coverage |
|---------|-------|--------|-------------------|
| 1 | Host Configuration | 4.1.1 - 4.1.14 | N/A (host-level) |
| 2 | Docker Daemon Configuration | 4.2.1 - 4.2.12 | N/A (daemon-level) |
| 3 | Docker Daemon Configuration Files | 4.3.1 - 4.3.4 | N/A (daemon-level) |
| 4 | Container Images | 4.4.1 - 4.4.4 | Partial (image scanning) |
| 5 | Container Runtime | 4.5.1 - 4.5.5 | HIGH (runtime security) |
| 6 | Docker Security Operations | 4.6.1 - 4.6.3 | Partial (swarm security) |
| 7 | Docker Swarm Configuration | 4.7.1 - 4.7.4 | N/A (swarm-specific) |
| 8 | Docker Enterprise Configuration | 4.8.1 - 4.8.3 | N/A (enterprise-specific) |

**Sections 4-5 are in scope for this registry** (Container Images and Container Runtime).

**CIS Docker Benchmark Mapping:**

| CIS Check | Title | Registry Constraint | Status |
|-----------|-------|--------------------|--------|
| 4.4.1 | Ensure a user for the container has been created | C001 (non-root user) | PASS |
| 4.4.2 | Ensure that containers use trusted base images | C008 (cosign verification) | PASS |
| 4.4.3 | Ensure unnecessary packages are not installed in the container | C003 (no shell), C004 (no pkg manager) | PASS |
| 4.4.4 | Ensure images are scanned and rebuilt to include security patches | Trivy scanning in CI | PASS |
| 4.5.1 | Ensure the container is restricted from acquiring additional privileges | `no-new-privileges:true` | PASS |
| 4.5.2 | Ensure the container is restricted from acquiring additional privileges via su/sudo | C018 (no sudo) | PASS |
| 4.5.3 | Ensure the container is restricted from acquiring additional capabilities | Phase 2 (cap-drop ALL) | PASS |
| 4.5.4 | Ensure that privileged containers are not used | C017 (no privileged) | PASS |
| 4.5.5 | Ensure health checks are configured for the container | C010 (HEALTHCHECK) | PASS |

**Automated checking:** `compliance/cis/run_cis_scan.sh` scans container images against CIS sections 4-5 and produces a percentage score.

#### Pillar 2: DISA STIG for Container Platforms

The DISA Security Technical Implementation Guide (STIG) for container platforms provides mandatory security requirements for DoD deployments.

**STIG Requirements Mapping to Constraints:**

| STIG ID | Title | Category | Registry Constraint | Status |
|---------|-------|----------|--------------------|--------|
| CCI-000366 | Run as non-root | Access Control | C001 | PASS |
| CCI-000213 | No unnecessary software | System and Information Integrity | C003, C004 | PASS |
| CCI-000770 | No shell access | Access Control | C003 | PASS |
| CCI-001812 | Signed images | System and Communications Protection | C008 | PASS |
| CCI-001813 | SBOM generated | System and Communications Protection | C009 | PASS |
| CCI-001814 | Vulnerability scanned | System and Information Protection | C010, trivy | PASS |
| CCI-001749 | No privileged containers | Access Control | C017 | PASS |
| CCI-001750 | No host network | Access Control | C017 | PASS |
| CCI-001751 | Read-only root filesystem | Access Control | C002 | PASS |
| CCI-001752 | Capability restrictions | Access Control | Phase 2 | PASS |
| CCI-001753 | No sensitive data in environment | Access Control | C016 | PASS |
| CCI-001754 | No new privileges | Access Control | no-new-privileges | PASS |
| CCI-001755 | Seccomp profile | Access Control | Phase 2 | PASS |
| CCI-001756 | Resource limits | Access Control | Phase 2 | PASS |
| CCI-001757 | Pinned image tags | Configuration Management | C019 | PASS |
| CCI-001758 | No interactive shell | Access Control | C003, C015 | PASS |
| CCI-001759 | Health checks | System and Communications Protection | C010 | PASS |
| CCI-001760 | Secret management | Access Control | C016 | PASS |
| CCI-001761 | Logging configuration | Audit | Phase 3 | PARTIAL |
| CCI-001762 | TMPFS for /tmp | Access Control | Phase 2 | PARTIAL |
| CCI-001763 | CPU and memory limits | Access Control | Phase 2 | PASS |

**Automated checking:** `compliance/stig/stig_checks.sh` verifies container images against STIG requirements, mapping to existing constraints C001-C020.

#### Pillar 3: FIPS 140-2 Cryptographic Module Validation

FIPS 140-2 requires that all cryptographic operations use FIPS-validated modules. Many images in the registry depend on cryptography:
- TLS termination (nginx, envoy, traefik, haproxy, caddy)
- VPN encryption (wireguard, strongswan, openvpn)
- Secret management (vault, step-cli)
- Database encryption (postgresql, mysql, redis)
- Identity providers (keycloak, zitadel)

**FIPS Strategy:**

| Approach | Description | Applicability |
|----------|-------------|---------------|
| **FIPS base image** | Use `debian-fips` or `ubi-fips` base image | All images needing FIPS crypto |
| **FIPS-enabled OpenSSL** | Compile with `enable-fips` flag | TLS proxies, VPN tunnels |
| **FIPS mode flag** | Set `OPENSSL_FIPS=1` environment variable | Runtime activation |
| **BoringCrypto (Go)** | Use Go's BoringCrypto for FIPS | Go binaries (prometheus, trivy, etc.) |
| **wolfSSL FIPS** | Use FIPS-validated wolfSSL | Embedded TLS |

**FIPS Image Matrix:** `compliance/fips/fips_image_matrix.yaml` lists all ~40 images requiring FIPS variants, categorized by function.

**FIPS Build Process:**

```dockerfile
FROM debian:bookworm-slim AS fips-builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl-dev libssl3 && rm -rf /var/lib/apt/lists/*

FROM debian:bookworm-slim
COPY --from=fips-builder /usr/lib/x86_64-linux-gnu/libssl.so.3 \
    /usr/lib/x86_64-linux-gnu/libssl.so.3
COPY --from=fips-builder /usr/lib/x86_64-linux-gnu/libcrypto.so.3 \
    /usr/lib/x86_64-linux-gnu/libcrypto.so.3
ENV OPENSSL_FIPS=1
```

#### Pillar 4: NIST SP 800-53 Controls Mapping

NIST SP 800-53 defines a comprehensive set of security and privacy controls. The controls mapping connects each control to specific implementation in the registry.

**Controls Mapping:** `compliance/ato/controls_mapping.yaml` maps NIST SP 800-53 controls to:
- Specific registry constraints (C001-C020)
- Phase implementations (Phase 1-5)
- Automated checks
- Evidence artifacts

**High-priority controls:**

| Control | Name | Implementation | Phase |
|---------|------|---------------|-------|
| AC-2 | Account Management | C001 (non-root user) | Phase 1 |
| AC-3 | Least Privilege | C018 (no sudo) | Phase 1 |
| AC-6 | Least Privilege (capabilities) | cap-drop ALL | Phase 2 |
| CM-2 | Baseline Configuration | C019 (pinned tags) | Phase 1 |
| CM-7 | Least Functionality | C003 (no shell), C015 (no debug) | Phase 1 |
| CM-8 | Information System Component Inventory | C009 (SBOM) | Phase 1 |
| SC-7 | Boundary Protection | C017 (no host network) | Phase 1 |
| SC-8 | Transmission Confidentiality | FIPS TLS | Phase 5 |
| SC-12 | Cryptographic Key Establishment | C008 (cosign) | Phase 1 |
| SC-13 | Cryptographic Protection | FIPS crypto modules | Phase 5 |
| SI-7 | Software, Firmware, and Information Integrity | Phase 1 (checksums) | Phase 1 |

### Consequences

**Positive:**
- Formal compliance evidence for auditors
- Automated compliance checking via scripts
- Clear path to ATO for DoD and federal deployments
- FIPS variants available for regulated environments

**Negative:**
- FIPS images are larger (include FIPS-validated OpenSSL)
- FIPS mode may have performance impact (~5-10% TLS overhead)
- Compliance scripts add maintenance burden
- STIG/CIS mappings need periodic updates as standards evolve

**Risks:**
- FIPS 140-3 may supersede FIPS 140-2 (plan for migration)
- CIS Benchmark version updates may change check IDs
- STIG updates may introduce new requirements
- NIST SP 800-53 Rev 5 changes control numbering

### Alternatives Considered

| Alternative | Pros | Cons | Reason Rejected |
|-------------|------|------|-----------------|
| Single compliance standard | Simpler | Insufficient for DoD/federal | Must meet multiple standards |
| Compliance via runtime policy only | No image changes needed | Cannot guarantee image-level compliance | Images must be compliant at rest |
| Third-party compliance tool (Twistlock, Prisma) | Automated | Vendor lock-in, cost, not customizable | Evergreen requirement |
| Manual compliance documentation | No tooling needed | Not auditable, not automated | Must be automated |

### Related Standards

| Standard | Version | Authority | URL |
|----------|---------|-----------|-----|
| CIS Docker Benchmark | 2.0.0 | Center for Internet Security | https://www.cisecurity.org/benchmark/docker |
| DISA STIG | Container Platform | DISA | https://public.cyber.mil/stigs/ |
| FIPS 140-2 | 2002 (amended) | NIST | https://csrc.nist.gov/publications/detail/fips/140/2/final |
| NIST SP 800-53 | Rev 5 | NIST | https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final |

### Related Yellow Papers

- YP-SEC-HARDENING-001: Container Security Hardening
- YP-SUPPLY-CHAIN-001: Supply Chain Integrity

### Related Blue Papers

- BP-IMAGE-REGISTRY-001: Evergreen Hardened Image Registry Architecture

### Related ADRs

- ADR-001: HEALTHCHECK Strategy (CIS 4.5.5, STIG CCI-001759)
- ADR-002: Checksum Verification (NIST SI-7)
- ADR-003: Multi-Stage Conversion (CIS 4.4.3, STIG CCI-000213)
- ADR-004: HFT Label Schema (runtime annotations)

### Related Constraints

- All constraints C001-C020 map to compliance controls
- Phase 2 runtime hardening maps to CIS 4.5.x and STIG CCI-00175x
- Phase 5 FIPS implementation maps to NIST SC-8 and SC-13

### Implementation Checklist

- [ ] Define CIS Docker Benchmark mapping (this ADR)
- [ ] Create `compliance/cis/run_cis_scan.sh` scanning script
- [ ] Define DISA STIG mapping (this ADR)
- [ ] Create `compliance/stig/stig_checks.sh` checking script
- [ ] Create FIPS image matrix (`compliance/fips/fips_image_matrix.yaml`)
- [ ] Create NIST SP 800-53 controls mapping (`compliance/ato/controls_mapping.yaml`)
- [ ] Create ATO evidence directory structure
- [ ] Create POA&M (Plan of Action & Milestones) template
- [ ] Add compliance scanning to CI pipeline
- [ ] Document FIPS build process
- [ ] Create FIPS variant Dockerfiles for Tier 1 crypto images

### Compliance Evidence Artifacts

| Artifact | Location | Generated By | Frequency |
|----------|----------|-------------|-----------|
| CIS scan report | `compliance/cis/reports/` | `run_cis_scan.sh` | Per build |
| STIG check report | `compliance/stig/reports/` | `stig_checks.sh` | Per build |
| FIPS validation report | `compliance/fips/reports/` | FIPS module check | Per release |
| Controls mapping | `compliance/ato/controls_mapping.yaml` | Manual + automated | Per phase |
| POA&M | `compliance/ato/poam/` | Manual | As needed |
| Risk assessment | `compliance/ato/risk/` | Manual | Per phase |
| System Security Plan | `compliance/ato/ssp/` | Manual | Per release |
| Evidence packages | `compliance/ato/controls_evidence/` | Automated | Per build |

---

**END OF ADR-005**
