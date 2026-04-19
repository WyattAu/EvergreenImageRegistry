# Standard Conflicts and Resolutions

## Document Metadata

| Attribute | Value |
|-----------|-------|
| Document ID | STANDARD-CONFLICTS-001 |
| Version | 1.0.0 |
| Status | APPROVED |
| Created | 2026-04-19 |

---

## Identified Standard Conflicts

### CONFLICT-001: NIST SP 800-190 vs CIS Docker Benchmark

| Aspect | NIST SP 800-190 | CIS Docker | Resolution |
|--------|---------------|-----------|-----------|
| Base image | Minimal | Updated | CIS: prefer updated |
| CVE tolerance | 0 critical | Updated priority | NIST: 0 critical |
| Privilege dropping | Recommended | Required | Use most restrictive: CIS |

**Resolution Documented:** [ADR-001](.adrs/adr-001.md)

### CONFLICT-002: FIPS 140-2 vs SLSA Level 3

| Aspect | FIPS 140-2 | SLSA Level 3 | Resolution |
|--------|-----------|-------------|-----------|
| Key management | HSM required | Software acceptable | FIPS: HSM required |
| Signing algorithm | FIPS approved | Any | Use FIPS:approved |
| Key ceremony | Required | Not specified | FIPS: required |

**Resolution Documented:** [ADR-002](.adrs/adr-002.md)

### CONFLICT-003: Container Size vs Security

| Aspect | Minimal Size | Full Hardening | Resolution |
|--------|-------------|---------------|---------|
| Base image | scratch | distroless | Tier-based |
| Static linking | Yes | Recommended | Both: preferred |
| Debug symbols | No | Explicit | Both: required |

**Resolution Documented:** [ADR-003](.adrs/adr-003.md)

---

## Priority Resolution

When standards conflict, use the following priority hierarchy:

1. **Safety-Critical** (NIST SP 800-190, FIPS 140-2, ISO 26262)
2. **Regulatory** (GDPR, PCI-DSS)
3. **Industry Standard** (CIS Docker, OCI)
4. **Best Practice** (Vendor recommendations)

---

## Document Control

| Version | Date | Changes |
|----------|------|---------|
| 1.0.0 | 2026-04-19 | Initial creation |

**END OF STANDARD CONFLICTS**