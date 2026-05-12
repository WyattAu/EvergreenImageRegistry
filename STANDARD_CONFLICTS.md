# Standard Conflicts and Resolutions

## Document Metadata

| Attribute | Value |
|-----------|-------|
| Document ID | STANDARD-CONFLICTS-001 |
| Version | 2.0.0 |
| Status | APPROVED |
| Created | 2026-04-19 |
| Last Updated | 2026-04-22 |

### Change Log

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-19 | Initial creation (3 conflicts) |
| **2.0.0** | **2026-04-22** | **Fixed ADR references (Conflict Set 8). Added 6 new internal conflicts (Sets 4-9). All 9 conflicts resolved and cross-referenced to unified REQUIREMENTS.md v4.0.0.** |

---

## Identified Standard Conflicts

### CONFLICT-001: NIST SP 800-190 vs CIS Docker Benchmark

| Aspect | NIST SP 800-190 | CIS Docker | Resolution |
|--------|---------------|-----------|-----------|
| Base image | Minimal | Updated | CIS: prefer updated — **Implemented via universal preference order (ADR-007)** |
| CVE tolerance | 0 critical | Updated priority | NIST: 0 critical — **C007: Zero Critical/High CVEs** |
| Privilege dropping | Recommended | Required | Use most restrictive: CIS — **C001: Non-root UID 65532** |

**Resolution Documented:** [ADR-005](.adrs/ADR-005-military-compliance-framework.md)
**Implemented In:** [REQUIREMENTS.md](.specs/archive/REQUIREMENTS-v4.0.0.md) Part II §2.1 (C001, C007)

### CONFLICT-002: FIPS 140-2 vs SLSA Level 3

| Aspect | FIPS 140-2 | SLSA Level 3 | Resolution |
|--------|-----------|-------------|-----------|
| Key management | HSM required | Software acceptable | FIPS: HSM required |
| Signing algorithm | FIPS approved | Any | Use FIPS-approved |
| Key ceremony | Required | Not specified | FIPS: required |

**Resolution Documented:** [ADR-005](.adrs/ADR-005-military-compliance-framework.md)
**Implemented In:** [REQUIREMENTS.md](.specs/archive/REQUIREMENTS-v4.0.0.md) Part VIII §8.1 (Compliance Framework)

### CONFLICT-003: Container Size vs Security

| Aspect | Minimal Size | Full Hardening | Resolution |
|--------|-------------|---------------|---------|
| Base image | scratch | distroless | **Universal preference order (ADR-007)** |
| Static linking | Yes | Recommended | Both: preferred — **C005** |
| Debug symbols | No | Explicit | Both: stripped — **C006** |

**Resolution Documented:** [ADR-005](.adrs/ADR-005-military-compliance-framework.md)
**Implemented In:** [REQUIREMENTS.md](.specs/archive/REQUIREMENTS-v4.0.0.md) Part I §1.1 (Preference Order), Part IV §4.2 (Size Limits)

### CONFLICT-004: Image Size Limits Inconsistent

| Source | Tier 1 | Tier 2 | Tier 3 |
|--------|--------|--------|--------|
| newrequirements.md v2.0.0 | <50MB | <200MB | Not specified |
| YP-SEC-HARDENING-001 | 50MB | 200MB | 500MB |
| REQUIREMENTS.md v3.0.0 | Not specified | Not specified | Not specified |

**Resolution:** Use YP-SEC-HARDENING-001 values (most granular). Tier 1 ≤50MB, Tier 2 ≤200MB, Tier 3 ≤500MB.

**Implemented In:** [REQUIREMENTS.md](.specs/archive/REQUIREMENTS-v4.0.0.md) Part IV §4.2

### CONFLICT-005: Base Image Tier Mapping Mismatched

| Source | Tier 1 | Tier 2 | Tier 3 |
|--------|--------|--------|--------|
| REQUIREMENTS.md v3.0.0 | scratch/distroless | wolfi | debian-slim |
| newrequirements.md v2.0.0 | Scratch/Distroless | Wolfi-based Distroless | Alpine/Wolfi |
| ADR-004 | scratch/distroless | debian-slim/wolfi | official/other |

**Resolution:** **Eliminated tier-based mapping entirely.** See ADR-007 — universal preference order applies to all tiers: scratch > wolfi > UBI micro > UBI minimal > UBI standard.

**Implemented In:** [REQUIREMENTS.md](.specs/archive/REQUIREMENTS-v4.0.0.md) Part I §1.1, [ADR-007](.adrs/ADR-007-base-image-preference-order.md)

### CONFLICT-006: HEALTHCHECK Form (Shell vs Exec)

| Source | Position |
|--------|----------|
| ADR-001 | exec-form only for scratch/distroless |
| newrequirements.md v2.0.0 | shell-form acceptable for debian-slim (Category D) |
| 6 current Dockerfiles | shell-form HEALTHCHECK (redis, postgresql, rabbitmq, mongodb, mariadb, valkey) |

**Resolution:** **Replaced Docker HEALTHCHECK instruction with HTTP health probes.** All images serve /livez, /readyz, /startupz on port 9101. See ADR-006.

**Implemented In:** [REQUIREMENTS.md](.specs/archive/REQUIREMENTS-v4.0.0.md) Part III §3.1, [ADR-006](.adrs/ADR-006-observability-architecture.md)

### CONFLICT-007: Init System (C016 "No Init" vs tini)

| Source | Position |
|--------|----------|
| REQUIREMENTS.md v3.0.0 C016 | No init system |
| ADR-004 §evergreen.hft.init | tini allowed |
| YP-CONTAINER-HARDENING-BENCHMARKS-001 | "Use tini explicitly" |
| 2 Java images (kafka, keycloak) | No init system (PID 1 signal handling risk) |

**Resolution:** No init system **baked into the image** (C023). Runtime injects init via `docker run --init` or K8s `shareProcessNamespace: true`. The image never contains tini/dumb-init/systemd.

**Implemented In:** [REQUIREMENTS.md](.specs/archive/REQUIREMENTS-v4.0.0.md) Part II §2.2 (C023)

### CONFLICT-008: STANDARD_CONFLICTS.md Wrong ADR References

| Conflict | Old Reference | Correct Reference | Status |
|----------|-------------|-------------------|--------|
| CONFLICT-001 | ADR-001 | ADR-005 | **Fixed** |
| CONFLICT-002 | ADR-002 | ADR-005 | **Fixed** |
| CONFLICT-003 | ADR-003 | ADR-005 | **Fixed** |

**Resolution:** All three conflicts are resolved in ADR-005 (Military Compliance Framework). Updated references in this document.

### CONFLICT-009: C003 "No Shell" vs debian-slim Retention

| Source | Position |
|--------|----------|
| REQUIREMENTS.md v3.0.0 C003 | No shell (CRITICAL) |
| ADR-003 | 42 images keep debian-slim with shell; removal "best-effort" |

**Resolution:** debian-slim **permanently banned** (ADR-007). C003 is now base-image-dependent:
- scratch: No shell (enforced — no OS)
- wolfi: BusyBox ash present (acceptable — needed for entrypoint scripts)
- UBI micro/minimal/standard: bash present (acceptable — needed for entrypoint and debugging)

**Implemented In:** [REQUIREMENTS.md](.specs/archive/REQUIREMENTS-v4.0.0.md) Part I §1.2 (Ban), Part II §2.1 (C003 note)

---

## Priority Resolution Hierarchy

When standards conflict, use the following priority:

1. **Safety-Critical** (IEC 61508, ISO 26262, DO-178C, NIST SP 800-53)
2. **Regulatory** (FIPS 140-2, GDPR, CCPA, DISA STIG)
3. **Industry Standard** (CIS Docker, OCI Image Spec, NIST SP 800-190)
4. **Best Practice** (Vendor recommendations, community guidelines)
5. **Internal Policy** (This registry's requirements)

**Same-Priority Resolution:** Document both requirements → Analyze impact → Apply most restrictive → Create ADR → Update compliance matrix.

---

## Document Control

| Version | Date | Changes |
|----------|------|---------|
| 1.0.0 | 2026-04-19 | Initial creation (3 conflicts) |
| 2.0.0 | 2026-04-22 | Fixed ADR references. Added conflicts 4-9. Cross-referenced to REQUIREMENTS.md v4.0.0. |

**END OF STANDARD CONFLICTS**
