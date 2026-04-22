# Architecture Decision Record: Universal Base Image Preference Order

## ADR-007: Base Image Selection Policy (Not Tier-Based)

### Status
ACCEPTED

### Date
2026-04-22

### Author
Nexus (Principal Systems Architect)

### Context

Prior to this ADR, base image selection was tied to operational tier:
- Tier 1 → scratch/distroless
- Tier 2 → wolfi
- Tier 3 → debian-slim (or Alpine)

This caused several problems:

1. **Tier 3 images that COULD run on scratch were forced to use debian-slim**, increasing attack surface unnecessarily
2. **Debian-slim was in the approved list** despite being less secure than wolfi (larger, more packages, glibc CVE surface)
3. **Alpine was referenced** in multiple specs despite being permanently banned
4. **FIPS requirements were confused** with tier assignments
5. **Three different documents** (REQUIREMENTS.md, newrequirements.md, ADR-004) had three different tier-to-image mappings

### Decision

#### Universal Preference Order

Base image selection is **decoupled from operational tier**. Every image uses the most secure base image that supports its workload:

```
scratch → wolfi → RHEL UBI micro → RHEL UBI minimal → RHEL UBI standard
```

| Priority | Base Image | Registry | libc | Pkg Mgr | Size | Use When |
|----------|-----------|----------|------|---------|------|----------|
| 1 | `scratch` | — | none | none | 0 MB | Static binary, zero runtime deps |
| 2 | `wolfi` | `cgr.dev/chainguard/wolfi-base` | musl | apk | ~5 MB | Dynamic linking, shell for entrypoint |
| 3 | RHEL UBI micro | `registry.access.redhat.com/ubi9/ubi-micro` | glibc | microdnf | ~30 MB | glibc required, FIPS crypto |
| 4 | RHEL UBI minimal | `registry.access.redhat.com/ubi9/ubi-minimal` | glibc | dnf | ~90 MB | Packages not in UBI micro |
| 5 | RHEL UBI standard | `registry.access.redhat.com/ubi9/ubi` | glibc | dnf | ~210 MB | Complex deps, last resort |

#### Decision Tree

```
Can the workload run as a static binary with zero deps?
  YES → scratch
  NO  → Does it need glibc (not musl-compatible)?
          YES → Does it need packages beyond microdnf?
                  YES → Does it need packages beyond UBI minimal?
                          YES → UBI standard
                          NO  → UBI minimal
                  NO  → UBI micro
          NO  → wolfi
```

#### Banned Base Images

| Image | Ban Reason | Any Exception? |
|-------|-----------|---------------|
| Alpine Linux | musl CVE history, outdated packages, insecure defaults | No. Build-stage only acceptable (discarded). |
| Debian Slim | Large attack surface, glibc CVEs, poor minimal-image hygiene | No. Replaced by wolfi or UBI. |
| Ubuntu | Large attack surface, unattended-upgrades in container | No |
| CentOS | EOL, no security updates | No |
| Amazon Linux | AWS vendor lock-in | No |

#### Fallback Documentation

When an image cannot use the highest-preference base image, the Dockerfile **must** declare why:

```dockerfile
LABEL sovereign.base.image="ubi-minimal"
LABEL sovereign.base.fallback_reason="wolfi lacks required package: libpq-dev-16"
```

#### wolfi First — Including FIPS

wolfi is preferred over RHEL UBI micro **in all cases**, including images that require FIPS-compliant cryptography. Rationale:
- wolfi is ~6x smaller than UBI micro (5MB vs 30MB)
- wolfi has a stronger security posture (Chainguard's zero-CVE policy)
- FIPS compliance can be achieved at the application level (Go's `crypto/fips140`, BoringCrypto) rather than at the OS level
- UBI micro's FIPS certification covers OS-level crypto modules, which is less relevant for application containers

#### Relationship to Tier

Tier determines **operational priority** (SLA, monitoring, update cadence). It does **not** determine base image. Examples:

| Image | Tier | Base Image | Why |
|-------|------|-----------|-----|
| Traefik | 1 | scratch | Static Go binary |
| Redis | 1 | wolfi | Needs musl-compatible redis-server binary |
| PostgreSQL | 1 | wolfi | Needs postgres packages + glibc-compatible binaries |
| Kafka | 2 | scratch | Static Go binary (confluent-kafka-go) |
| Jenkins | 3 | scratch | Static Go binary — even though Tier 3, scratch works |
| Grafana | 3 | wolfi | Needs glibc — falls to wolfi |
| Oracle JDK | 3 | UBI minimal | glibc + packages not in wolfi |

### Consequences

**Positive:**
- Simple, deterministic decision tree for base image selection
- Maximizes scratch usage (smallest attack surface) across ALL tiers
- Eliminates debian-slim and Alpine from the ecosystem entirely
- Single source of truth (this ADR + unified REQUIREMENTS.md)
- wolfi's security posture benefits all images, not just Tier 2

**Negative:**
- ~470 images currently using debian-slim must be migrated to wolfi or UBI
- Migration is not a sed replacement — different package managers, package names, paths
- Some images may need to fall to UBI minimal/standard due to package availability
- wolfi's apk package set is smaller than Debian's apt

**Risks:**
| Risk | Mitigation |
|------|-----------|
| Package availability gaps in wolfi | Fall to UBI micro/minimal with documented reason |
| musl vs glibc compatibility | Test all dynamic binaries against wolfi's musl |
| UBI requires Red Hat account for some packages | UBI base images are freely redistributable; only specific packages may need subscription |
| Migration breaks CI for 470 images | Batch migration with per-image CI validation |

### Alternatives Considered

| Alternative | Rejected Because |
|-------------|-----------------|
| Tier-based selection (status quo) | Forces insecure base images on lower-tier images that could use scratch |
| Keep debian-slim as fallback | wolfi is smaller, more secure, and covers the same use cases |
| UBI first for FIPS | FIPS achievable at application level; wolfi is 6x smaller |
| Alpine as tier-3 fallback | Permanently banned due to CVE history |

### Migration Plan

1. **Phase A:** Update all spec documents (this ADR, REQUIREMENTS.md, YP)
2. **Phase B:** Migrate Tier 1 debian-slim images to wolfi/UBI (highest priority)
3. **Phase C:** Migrate Tier 2 debian-slim images
4. **Phase D:** Migrate Tier 3 debian-slim images
5. **Phase E:** Clean all Alpine references from build stages where possible
6. **Phase F:** CI validation pass on all 1,012 images

### Related Standards

| Standard | Relevance |
|----------|-----------|
| NIST SP 800-190 §4.1 | Minimal container base |
| CIS Docker Benchmark 4.1 | Base image selection |
| DISA STIG | Container platform requirements |
| FIPS 140-2 | Cryptographic module validation |

### Related ADRs

| ADR | Relationship |
|-----|-------------|
| ADR-003 | Debian multi-stage strategy (superseded — debian-slim now banned) |
| ADR-004 | HFT label schema (UID updated to 65532, aligns with wolfi) |
| ADR-005 | Military compliance (FIPS addressed at application level) |
| ADR-006 | Observability (base image affects health shim availability) |

### Related Requirements

| REQ ID | Requirement |
|--------|------------|
| Part I §1.1 | Universal preference order |
| Part I §1.2 | Banned base images |
| C025 | Base image label required |
| C003 | No shell (tier-aware via base image choice) |
