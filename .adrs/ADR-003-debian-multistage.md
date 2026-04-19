# Architecture Decision Record: Multi-Stage Conversion of Debian-Slim Images

## ADR-003: Converting Debian-Slim Images to Multi-Stage Scratch/Distroless Builds

### Status
ACCEPTED

### Date
2026-04-19

### Author
Nexus (Principal Systems Architect)

### Context

87 of 223 images (39%) use `debian:bookworm-slim` as their **final** base image. These images:

1. **Violate C003** (No shell): debian-slim inherits `/bin/sh` and `/bin/bash`
2. **Violate C004** (No package manager): `apt` remains available at runtime
3. **Have excessive attack surface**: glibc, OpenSSL, coreutils, and other OS packages
4. **Are larger than necessary**: Typical debian-slim image is 80-150MB vs <50MB for scratch

The constraint hierarchy (scratch > distroless > wolfi > debian-slim) mandates that debian-slim is a **last resort** fallback, not the default approach.

### Decision

**Convert eligible debian-slim images to multi-stage builds, copying only necessary artifacts to a scratch or distroless final stage.**

Images that **cannot** be converted will remain on debian-slim with documented justification and additional hardening steps.

#### Conversion Decision Tree

```
Is the software a single static binary?
├── YES → FROM scratch (copy binary + SSL certs + directories)
└── NO
    Is the software a single dynamic binary needing only glibc?
    ├── YES → FROM gcr.io/distroless/cc-debian12 (copy binary + deps)
    └── NO
        Does the software need an interpreter (python, php, node, java, ruby)?
        ├── YES → FROM debian:bookworm-slim (multi-stage: install in builder,
        │          copy only runtime files, remove shell/pkgmgr if possible)
        └── NO
            Does the software need system services (systemd, syslog)?
            ├── YES → FROM debian:bookworm-slim (documented exception)
            └── NO → Investigate further (likely can be converted)
```

#### Category-Specific Strategy

##### Type 1: Static Binary (Convert to scratch)
**Applicable:** ~20 images
**Examples:** redis-exporter, mysql-exporter, postgresql-exporter, node-exporter, prometheus-node-exporter

```dockerfile
# BEFORE (debian-slim, 120MB):
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y redis-exporter && rm -rf /var/lib/apt/lists/*
USER 65534:65534
ENTRYPOINT ["redis_exporter"]

# AFTER (scratch, ~15MB):
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/.../redis_exporter.tar.gz" -o /exporter.tar.gz
RUN tar -xzf /exporter.tar.gz -C / && rm /exporter.tar.gz

FROM scratch
COPY --from=downloader /redis_exporter /redis_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
ENTRYPOINT ["/redis_exporter"]
```

##### Type 2: Dynamic Binary (Convert to distroless)
**Applicable:** ~10 images
**Examples:** Images that need glibc but nothing else

```dockerfile
# AFTER (distroless, ~30MB):
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends <package> && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app

FROM gcr.io/distroless/cc-debian12
COPY --from=builder /usr/bin/<binary> /<binary>
COPY --from=builder /usr/lib/x86_64-linux-gnu/<lib> /usr/lib/x86_64-linux-gnu/<lib>
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
ENTRYPOINT ["/<binary>"]
```

##### Type 3: Interpreter-Based (Keep debian-slim, harden)
**Applicable:** ~42 images
**Examples:** python, node, php, ruby, openjdk, keycloak, mattermost, synapse

These **cannot** be converted to scratch because they need:
- Python interpreter + standard library
- Node.js runtime + node_modules
- PHP runtime + extensions
- JVM + classpath
- Ruby interpreter + gems

**Hardening strategy for retained debian-slim images:**

```dockerfile
# Hardened debian-slim pattern:
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip <app-packages> && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 65534 -s /usr/sbin/nologin appuser

# Remove shell for non-root user (C003 best-effort)
RUN rm -f /bin/sh && ln -sf /usr/sbin/nologin /bin/sh || true

# Remove package manager (C004)
RUN apt-get purge -y --auto-remove apt apt-get && rm -rf /var/lib/apt /var/cache/apt

FROM debian:bookworm-slim
COPY --from=builder /usr /usr
COPY --from=builder /etc/ssl/certs /etc/ssl/certs
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65534:65534 /app /app
USER 65534:65534
WORKDIR /app
ENTRYPOINT ["python3", "app.py"]
```

**Note:** Removing `/bin/sh` from debian-slim may break some applications that use it internally (e.g., subprocess calls). This must be tested per-image.

#### Exceptions Registry

Images that **cannot** be converted and their justifications:

| Image | Reason | Tier | Additional Hardening |
|-------|--------|------|---------------------|
| python | Needs Python interpreter | 3 | Remove apt, minimize packages |
| node | Needs Node.js runtime | 3 | Remove apt, minimize packages |
| php | Needs PHP interpreter | 3 | Remove apt, minimize packages |
| ruby | Needs Ruby interpreter | 3 | Remove apt, minimize packages |
| openjdk | Needs JVM | 3 | Remove apt, minimize packages |
| keycloak | Needs Java + Quarkus | 3 | Use wolfi, remove apt |
| mattermost | Needs Node.js + Go binary | 3 | Use wolfi, remove apt |
| synapse | Needs Python + dependencies | 3 | Remove apt, minimize packages |
| jenkins | Needs Java + many plugins | 3 | Use official hardened image |
| gitlab | Complex multi-service | E | Use official image |
| couchdb | Needs Erlang runtime | 3 | Remove apt, minimize packages |
| ... | (full list in Phase 0 execution) | | |

### Consequences

**Positive:**
- ~30 images converted to scratch/distroless (smaller, more secure)
- C003 and C004 satisfied for converted images
- Reduced attack surface by ~70% for converted images
- Image sizes reduced by 60-90% for converted images

**Negative:**
- Some images cannot be converted (interpreter dependency)
- Multi-stage builds add complexity
- Shared library discovery needed for dynamic binaries
- Risk of breaking functionality during conversion

**Risks:**
- Missing shared library causes runtime crash → Test thoroughly
- Binary not available for direct download → Use apt in builder stage
- License restrictions on redistribution → Verify per-project

### Alternatives Considered

| Alternative | Pros | Cons | Reason Rejected |
|-------------|------|------|-----------------|
| Keep all as debian-slim | Simplest | C003/C004 violated for 87 images | Constraint violation |
| Force all to scratch | Maximum security | Impossible for interpreter-based apps | Not feasible |
| Use wolfi for all | Better than debian-slim | Not all packages available | Limited package availability |
| Use Chainguard distroless | No shell, minimal | glibc only, no interpreters | Limited to compiled languages |

### Related Standards

| Standard | Clause | Requirement |
|----------|--------|-------------|
| NIST SP 800-190 | 2.1 | Use minimal base images |
| CIS Docker Benchmark | 4.1 | Minimize container content |
| STIG | Container | Minimize attack surface |

### Related Yellow Papers

- YP-SEC-HARDENING-001: Container Security Hardening (DEF-001: Distroless Image)

### Related ADRs

- ADR-001: HEALTHCHECK Strategy (affects all converted images)
- ADR-002: Checksum Verification (applies to all multi-stage downloads)

### Implementation Checklist

- [ ] Categorize all 87 debian-slim images by conversion type
- [ ] Convert Type 1 images (static binary → scratch)
- [ ] Convert Type 2 images (dynamic binary → distroless)
- [ ] Harden Type 3 images (interpreter-based → minimize debian-slim)
- [ ] Create exceptions registry for non-convertible images
- [ ] Test all converted images for functionality
- [ ] Verify C003 and C004 pass for converted images
- [ ] Update image size constraints in domain_constraints_security.toml
- [ ] Update pre-commit validator to check final stage base image

---

**END OF ADR-003**
