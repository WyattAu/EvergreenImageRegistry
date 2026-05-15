# Architecture Decision Record: Upstream Base Image Exception Policy

## ADR-008: Upstream Base Image Exception Policy

### Status

ACCEPTED

### Date

2026-04-22

### Author

Nexus (Principal Systems Architect)

### Context

ADR-007 establishes a strict base image preference order (scratch → wolfi → RHEL UBI micro → RHEL UBI minimal → RHEL UBI
standard) and bans Alpine, Debian Slim, Ubuntu, CentOS, and Amazon Linux.

However, 16 images in the registry use upstream base images that violate this policy. These images fall outside our
direct control because they provide pre-built binaries, are maintained by third parties, or embed complex dependency
chains that cannot be trivially rebuilt on wolfi or scratch.

Attempting to force ADR-007 compliance on these 16 images would require:

- Forking and maintaining upstream builds (high cost, low ROI)
- Rebuilding complex dependency trees (e.g., GitLab CE embeds 200+ packages)
- Duplicating work already done by well-maintained upstream projects
- Risking functionality regressions in critical infrastructure

A blanket ban is impractical. A structured exception framework with monitoring and documentation is the responsible
approach.

### Decision

#### Exception Categories

| Category              | Count | Description                                                   | Example Images                              |
| --------------------- | ----- | ------------------------------------------------------------- | ------------------------------------------- |
| A — LinuxServer.io    | 6     | Third-party Alpine-based images with no alternative upstream  | lidarr, prowlarr, radarr, sonarr            |
| B — Official upstream | 5     | Vendor-maintained images with opaque build systems            | drone, gitlab-ce, jellyfin, openhab, pulsar |
| C — Internal/custom   | 2     | Custom images with unclear provenance requiring investigation | milvus-etcd, milvus-minio                   |
| D — Migratable        | 3     | Images that CAN be migrated to compliant base images          | oxidized, python-alpine, python-slim        |

#### Per-Category Policy

**Category A — LinuxServer.io (Accepted Exception)**

- Accept upstream Alpine-based image as-is
- Wrap with health-shim (per ADR-006) to provide `/livez`, `/readyz`, `/startupz` on `:9101`
- Add evergreen labels for visibility and audit trail
- Pin to specific image digest (not tag) for reproducibility
- Monitor upstream for CVEs via Trivy weekly scan
- SLA: patches applied within 72h of upstream fix

**Category B — Official upstream (Accepted Exception)**

- Accept vendor-maintained base image as-is
- Add evergreen labels
- Pin to specific digest
- Monitor for CVEs via Trivy weekly scan
- Evaluate quarterly for migration feasibility (vendor may switch to compliant base)
- SLA: patches applied within 72h of upstream fix; critical CVEs within 24h

**Category C — Internal/custom (Under Investigation)**

- Investigate upstream source and provenance
- Remap to proper upstream sources where possible
- If remappable to a compliant base image, migrate per Category D
- If not remappable, escalate to Category A or B policy
- Deadline: 30 days for investigation

**Category D — Migratable (Migrate Immediately)**

- Migrate to wolfi-base per ADR-007 preference order
- Rewrite Dockerfile using apk package manager
- Follow evergreen label schema (ADR-004)
- No exception required — these images comply with ADR-007 post-migration

#### Required Labels for Exceptions (Category A & B)

All exception images must carry these labels:

```dockerfile
LABEL evergreen.base.image="<actual-upstream-image>"
LABEL evergreen.base.exception="true"
LABEL evergreen.base.exception.category="A|B"
LABEL evergreen.base.exception.reason="<why compliance is not possible>"
LABEL evergreen.base.fallback_reason="<upstream provides pre-built binaries>"
LABEL evergreen.base.exception.approved-by="Nexus"
LABEL evergreen.base.exception.approved-date="2026-04-22"
```

#### Monitoring Requirements

| Requirement                | Frequency   | Tool                    | Escalation                            |
| -------------------------- | ----------- | ----------------------- | ------------------------------------- |
| CVE scan of upstream image | Weekly      | Trivy                   | 72h patch SLA                         |
| Digest pin validation      | Every build | cosign verify           | Block build on mismatch               |
| Upstream version check     | Weekly      | GitHub Actions          | PR to update digest                   |
| Exception audit review     | Quarterly   | Manual                  | Remove exception if upstream migrates |
| Base image size tracking   | Monthly     | docker manifest inspect | Flag if image grows >20%              |

### Consequences

**Positive:**

- Structured, auditable exception process replaces ad-hoc decisions
- Category D eliminates 3 non-compliant images immediately
- Category C investigation resolves provenance gaps
- Monitoring ensures exceptions don't become permanent blindly
- Evergreen labels make exception status machine-readable

**Negative:**

- 13 images remain on non-compliant base images (Categories A, B, C pending)
- Additional CI pipeline complexity for exception monitoring
- Exception labels add Dockerfile verbosity
- Category A LinuxServer.io images remain on Alpine despite ADR-007 ban

**Risks:**

| Risk                            | Mitigation                                                               |
| ------------------------------- | ------------------------------------------------------------------------ |
| Exceptions become permanent     | Quarterly audit review with mandatory justification                      |
| Upstream abandons image         | Fallback plan: rebuild from source or find alternative                   |
| CVE in upstream base not caught | Weekly Trivy scan + critical CVE 24h SLA                                 |
| Digest pin drift                | cosign verify in CI blocks builds on mismatch                            |
| Exception scope creep           | Only Nexus can approve new exceptions; all exceptions require ADR update |

### Alternatives Considered

| Alternative             | Rejected Because                                                        |
| ----------------------- | ----------------------------------------------------------------------- |
| Ban all exceptions      | Requires forking 13 upstream projects; unsustainable maintenance burden |
| Migrate all to wolfi    | Not possible for pre-built binaries (GitLab CE, Jellyfin, etc.)         |
| No documentation        | Exception status would be invisible; no audit trail                     |
| Self-built alternatives | Duplicates upstream work; introduces regression risk; no bandwidth      |

### Related Standards

| Standard                 | Relevance                                              |
| ------------------------ | ------------------------------------------------------ |
| NIST SP 800-190 §4.1     | Risk acceptance for non-minimal base images            |
| CIS Docker Benchmark 4.1 | Documented exception for base image selection          |
| DISA STIG                | Risk acceptance documentation for non-compliant images |

### Related ADRs

| ADR     | Relationship                                                         |
| ------- | -------------------------------------------------------------------- |
| ADR-007 | Base image preference order (this ADR defines exceptions to ADR-007) |
| ADR-006 | Observability (exception images must still have health shim)         |
| ADR-004 | HFT label schema (exception labels extend the schema)                |
| ADR-005 | Military compliance (exceptions require documented risk acceptance)  |

### Related Requirements

| REQ ID      | Requirement                                                   |
| ----------- | ------------------------------------------------------------- |
| Part I §1.1 | Base image preference order (exceptions documented here)      |
| Part I §1.2 | Banned base images (exceptions documented with justification) |
| C025        | Base image label required (extended with exception labels)    |
