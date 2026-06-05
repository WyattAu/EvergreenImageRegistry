# Image Creation Cookbook

> **Purpose:** Step-by-step recipes for creating Evergreen-hardened container images. Each recipe follows the
> [Image Standards](standards.md) and [Dockerfile Authoring Standards](dockerfile-standards.md).

---

## Table of Contents

- [Template 1: Scratch-Based Image (Binary Download)](#template-1-scratch-based-image-binary-download)
- [Template 2: Wolfi-Based Image (Package Install)](#template-2-wolfi-based-image-package-install)
- [Template 3: Repack Image (Upstream + Hardening)](#template-3-repack-image-upstream--hardening)
- [Adding Health Checks](#adding-health-checks)
- [Adding SBOMs](#adding-sboms)
- [Setting Tier Labels](#setting-tier-labels)
- [Common Patterns](#common-patterns)
- [Anti-Patterns](#anti-patterns)

---

## Template 1: Scratch-Based Image (Binary Download)

Use when: The upstream project provides a statically compiled binary (Go, Rust, C). This is the most common pattern
(~343 images).

### Minimal Example

```dockerfile
# =============================================================================
# EVERGREEN HARDENED <SOFTWARE>
# Scratch-based with health-shim as PID 1
# =============================================================================

ARG TARGETARCH
ARG VERSION=1.0.0
ARG APP_UID=65532
ARG APP_GID=65532

# Stage 1: Download the binary
FROM debian:bookworm AS downloader
ARG TARGETARCH
ARG VERSION
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Create target directory BEFORE download (BuildKit COPY eval bug workaround)
RUN mkdir -p /out/usr/local/bin && \
    touch /out/usr/local/bin/mybin || true

RUN curl --retry 3 --retry-delay 5 -fsSL \
    "https://github.com/org/repo/releases/download/v${VERSION}/mybin_${VERSION}_linux_${TARGETARCH}.tar.gz" \
    -o /tmp/mybin.tar.gz && \
    echo "<SHA256_CHECKSUM>  /tmp/mybin.tar.gz" | sha256sum -c && \
    tar -xzf /tmp/mybin.tar.gz -C /out/usr/local/bin/ && \
    rm -f /tmp/mybin.tar.gz

# Stage 2: Get the health-shim
FROM ghcr.io/wyattau/evergreenshim/health-shim:v0.3.0 AS shim

# Stage 3: Final scratch image
FROM scratch

# Copy CA certificates for TLS
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

# Copy application binary
COPY --from=downloader /out/usr/local/bin/mybin /usr/local/bin/mybin

# Copy health-shim
COPY --from=shim /shim /usr/local/bin/shim

# Create non-root user
ARG APP_UID
ARG APP_GID
RUN mkdir -p /etc/passwd /etc/group && \
    echo "appuser:x:${APP_UID}:${APP_GID}:appuser:/app:/sbin/nologin" >> /etc/passwd && \
    echo "appgroup:x:${APP_GID}:" >> /etc/group

USER 65532:65532

# Health check configuration
ENV HEALTH_CMD="tcp:8080" \
    SHIM_METRICS_ENABLED="true"

WORKDIR /app
EXPOSE 8080 9101

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
    CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "/usr/local/bin/mybin", "--"]

# Metadata labels
LABEL org.opencontainers.image.title="mybin" \
      org.opencontainers.image.description="My Application" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Org Name" \
      org.opencontainers.image.source="https://github.com/org/repo"

LABEL evergreen.base.image="scratch" \
      evergreen.image.tier="standard" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.hardened="true" \
      evergreen.health.type="tcp" \
      evergreen.health.endpoint="/livez" \
      evergreen.health.listen="0.0.0.0:9101" \
      evergreen.security.cap-drop="ALL" \
      evergreen.security.no-new-privileges="true" \
      evergreen.security.read-only-rootfs="true" \
      evergreen.security.seccomp="runtime-default"

STOPSIGNAL SIGTERM
```

### Key Points

- **Multi-stage build:** debian downloader → scratch final
- **BuildKit workaround:** `RUN mkdir -p` and `RUN touch` in separate steps before COPY
- **Checksum verification:** SHA256 checksum on downloaded artifact
- **Health-shim as PID 1:** Handles health checks, metrics, signal forwarding
- **Non-root:** UID 65532 (configurable via `APP_UID`/`APP_GID`)
- **No shell:** Final image has no `/bin/sh`

---

## Template 2: Wolfi-Based Image (Package Install)

Use when: The software is available as a Wolfi package, or needs glibc/libc at runtime. Used for databases, caches, and
applications with native dependencies (~175 images).

### Minimal Example

```dockerfile
# =============================================================================
# EVERGREEN HARDENED <SOFTWARE>
# Wolfi-based with health-shim as PID 1
# =============================================================================

ARG VERSION=1.0.0
ARG TARGETARCH

# Stage 1: Get the health-shim
FROM ghcr.io/wyattau/evergreenshim/health-shim:v0.3.0 AS shim

# Stage 2: Final wolfi image
FROM cgr.dev/chainguard/wolfi-base:latest

# Install packages (wolfi uses apk, NOT apt)
RUN apk add --no-cache \
    ca-certificates \
    <software-package>-${VERSION}

# Create non-root user
ARG APP_UID=65532
ARG APP_GID=65532
RUN adduser -D -u ${APP_UID} -s /bin/false appuser 2>/dev/null || true && \
    mkdir -p /app /var/log/<software> /var/cache/<software> && \
    chown -R ${APP_UID}:${APP_GID} /app /var/log/<software> /var/cache/<software>

# Copy health-shim
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

# Health check configuration
ENV HEALTH_CMD="tcp:8080" \
    READY_CMD="" \
    SHIM_METRICS_ENABLED="true"

USER 65532:65532
WORKDIR /app
EXPOSE 8080 9101

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "<software-binary>", "--"]

# Metadata labels
LABEL org.opencontainers.image.title="<software>" \
      org.opencontainers.image.description="<Software Description>" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="<Vendor>" \
      org.opencontainers.image.source="https://github.com/org/repo"

LABEL evergreen.base.image="wolfi" \
      evergreen.image.tier="standard" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.hardened="true" \
      evergreen.health.type="tcp" \
      evergreen.health.endpoint="/livez" \
      evergreen.health.listen="0.0.0.0:9101" \
      evergreen.security.cap-drop="ALL" \
      evergreen.security.no-new-privileges="true"

STOPSIGNAL SIGTERM
```

### Key Points

- **wolfi-base:** Uses `cgr.dev/chainguard/wolfi-base` (glibc, not musl)
- **apk, not apt:** Wolfi uses Alpine package manager syntax
- **No curl:** Use `wget` instead of `curl` in wolfi stages
- **ca-certificates:** Install explicitly (`apk add --no-cache ca-certificates`)
- **Health-shim:** Same pattern as scratch images

---

## Template 3: Repack Image (Upstream + Hardening)

Use when: The upstream project provides an official Docker image. We repackage it with hardening (non-root, labels,
health checks). Used for complex applications (~262 images).

### Minimal Example

```dockerfile
# =============================================================================
# EVERGREEN HARDENED <SOFTWARE>
# Repack of upstream image with hardening
# =============================================================================

ARG VERSION=1.0.0
ARG TARGETARCH

# Stage 1: Upstream image
FROM upstream/<software>:${VERSION} AS upstream

# Stage 2: Get the health-shim
FROM ghcr.io/wyattau/evergreenshim/health-shim:v0.3.0 AS shim

# Stage 3: Final hardened image
FROM cgr.dev/chainguard/wolfi-base:latest

# Install CA certificates and required packages
RUN apk add --no-cache ca-certificates

# Copy application from upstream
COPY --from=upstream /usr/local/bin/<software> /usr/local/bin/<software>
COPY --from=upstream /etc/<software>/ /etc/<software>/

# Copy health-shim
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

# Create non-root user
ARG APP_UID=65532
ARG APP_GID=65532
RUN adduser -D -u ${APP_UID} -s /bin/false appuser 2>/dev/null || true && \
    mkdir -p /app /var/log/<software> && \
    chown -R ${APP_UID}:${APP_GID} /app /var/log/<software>

# Health check configuration
ENV HEALTH_CMD="tcp:8080" \
    SHIM_METRICS_ENABLED="true"

USER 65532:65532
WORKDIR /app
EXPOSE 8080 9101

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "/usr/local/bin/<software>", "--"]

# Metadata labels
LABEL org.opencontainers.image.title="<software>" \
      org.opencontainers.image.description="<Software Description>" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="<Vendor>" \
      org.opencontainers.image.source="https://github.com/org/repo"

LABEL evergreen.base.image="wolfi" \
      evergreen.image.tier="standard" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.hardened="true" \
      evergreen.health.type="tcp" \
      evergreen.health.endpoint="/livez" \
      evergreen.health.listen="0.0.0.0:9101" \
      evergreen.security.cap-drop="ALL" \
      evergreen.security.no-new-privileges="true"

STOPSIGNAL SIGTERM
```

### Key Points

- **Upstream image as source:** Copy binaries/configs from the official image
- **Hardening:** Non-root user, dropped capabilities, health checks
- **Repack pattern:** Extract what we need, discard the rest
- **Wolfi final stage:** Replaces the upstream's base with a minimal, hardened base

---

## Adding Health Checks

### For Scratch Images (No Shell)

Use the health-shim binary:

```dockerfile
HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
    CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]
```

### For Wolfi Images (Has Shell)

Use wget (NOT curl):

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -qO- http://localhost:8080/healthz || exit 1
```

### Health Check Types

| Type | Command                                                           | Use Case           |
| ---- | ----------------------------------------------------------------- | ------------------ |
| TCP  | `["shim", "healthcheck", "--tcp", "127.0.0.1:PORT"]`              | Port open check    |
| HTTP | `["shim", "healthcheck", "--http", "http://localhost:PORT/path"]` | HTTP 200 check     |
| Exec | `["shim", "healthcheck", "--exec", "command"]`                    | CLI tool check     |
| wget | `wget -qO- http://localhost:PORT/path \|\| exit 1`                | HTTP check (wolfi) |

### Required Parameters

| Parameter        | Value | Why                       |
| ---------------- | ----- | ------------------------- |
| `--interval`     | `30s` | Check frequency           |
| `--timeout`      | `5s`  | Max time per check        |
| `--retries`      | `3`   | Failures before unhealthy |
| `--start-period` | `10s` | Grace period at startup   |

---

## Adding SBOMs

Every image MUST include an SPDX 2.3 SBOM. Generate it after building:

### Using Syft

```bash
# Install syft
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin

# Generate SBOM for scratch image
syft <image>:<tag> -o spdx-json > images/<name>/sbom.spdx.json

# Generate SBOM for wolfi image
syft <image>:<tag> -o spdx-json > images/<name>/sbom.spdx.json
```

### SBOM Requirements

- Format: SPDX 2.3 JSON (`spdx-json`)
- Filename: `sbom.spdx.json`
- Location: In the image directory (`images/<name>/sbom.spdx.json`)
- Must be generated from the built image, not the Dockerfile

### Automating SBOM Generation

The CI pipeline generates SBOMs automatically for critical and standard tier images. For local development:

```bash
# Build the image
docker build -t evergreen-<name> images/<name>/

# Generate SBOM
syft evergreen-<name> -o spdx-json > images/<name>/sbom.spdx.json

# Verify SBOM
spdx-tools validate images/<name>/sbom.spdx.json
```

---

## Setting Tier Labels

### Tier Definitions

| Tier         | Description                                       | Labels                                  |
| ------------ | ------------------------------------------------- | --------------------------------------- |
| critical     | Essential infrastructure (databases, proxies, CI) | `evergreen.image.tier = "critical"`     |
| standard     | Useful but replaceable                            | `evergreen.image.tier = "standard"`     |
| community    | Contributed images                                | `evergreen.image.tier = "community"`    |
| experimental | Unstable or WIP                                   | `evergreen.image.tier = "experimental"` |

### Setting in Dockerfile

```dockerfile
LABEL evergreen.image.tier="critical"
```

### Setting in manifest.toml

```toml
[metadata]
tier = "critical"
```

### Tier Selection Guide

| Criteria                                | Tier         |
| --------------------------------------- | ------------ |
| Database (Postgres, MySQL, Redis)       | critical     |
| Proxy/Ingress (Nginx, Traefik, HAProxy) | critical     |
| CI/CD (Jenkins, GitLab Runner)          | critical     |
| Monitoring (Prometheus, Grafana)        | standard     |
| Web Apps (WordPress, Ghost)             | standard     |
| Tools (curl, wget, jq)                  | standard     |
| Contributed by community                | community    |
| Work in progress                        | experimental |

---

## Common Patterns

### Pattern: Multi-Stage Build with Debian Downloader

```dockerfile
FROM debian:bookworm AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

FROM scratch
COPY --from=downloader /usr/local/bin/mybin /usr/local/bin/mybin
```

### Pattern: Health-Shim as PID 1

```dockerfile
FROM ghcr.io/wyattau/evergreenshim/health-shim:v0.3.0 AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "/usr/local/bin/app", "--"]
```

### Pattern: Configurable UID/GID

```dockerfile
ARG APP_UID=65532
ARG APP_GID=65532
RUN adduser -D -u ${APP_UID} -s /bin/false appuser 2>/dev/null || true
USER 65532:65532
```

### Pattern: Environment Variable Configuration

```dockerfile
ENV HEALTH_CMD="tcp:8080" \
    READY_CMD="" \
    SHIM_METRICS_ENABLED="true" \
    APP_LOG_LEVEL="info"
```

### Pattern: BuildKit COPY Eval Workaround

```dockerfile
# Step 1: Create directory (separate RUN)
RUN mkdir -p /out/usr/local/bin

# Step 2: Touch file (separate RUN)
RUN touch /out/usr/local/bin/mybin || true

# Step 3: Download (separate RUN)
RUN curl -fsSL -o /out/usr/local/bin/mybin "https://..."

# Step 4: COPY works
COPY --from=downloader /out/usr/local/bin/mybin /usr/local/bin/mybin
```

---

## Anti-Patterns

### Anti-Pattern: Using Alpine (NEVER)

```dockerfile
# WRONG - Alpine is permanently banned
FROM alpine:3.19 AS final

# CORRECT - Use wolfi or scratch
FROM cgr.dev/chainguard/wolfi-base:latest AS final
```

### Anti-Pattern: Using curl in Wolfi

```dockerfile
# WRONG - curl is not available in wolfi
RUN curl -fsSL https://example.com/file -o /tmp/file

# CORRECT - Use wget in wolfi
RUN wget -qO /tmp/file https://example.com/file
```

### Anti-Pattern: Missing BuildKit Workaround

```dockerfile
# WRONG - Will fail with BuildKit COPY eval bug
FROM debian:bookworm AS downloader
RUN curl -fsSL -o /out/mybin "https://..."

FROM scratch
COPY --from=downloader /out/mybin /usr/local/bin/mybin
# ERROR: /out/mybin: not found

# CORRECT - Create directory first
FROM debian:bookworm AS downloader
RUN mkdir -p /out && touch /out/mybin || true
RUN curl -fsSL -o /out/mybin "https://..."

FROM scratch
COPY --from=downloader /out/mybin /usr/local/bin/mybin
```

### Anti-Pattern: Shell-Form HEALTHCHECK in Scratch

```dockerfile
# WRONG - No shell in scratch
HEALTHCHECK CMD curl -f http://localhost:8080/healthz || exit 1

# CORRECT - Use exec-form with shim
HEALTHCHECK CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]
```

### Anti-Pattern: Hardcoded Secrets

```dockerfile
# WRONG - Secrets in image layers
ENV DATABASE_PASSWORD=supersecret
RUN echo "password=supersecret" > /etc/app/config

# CORRECT - Inject at runtime
# Use Docker secrets, Kubernetes secrets, or env vars at runtime
```

### Anti-Pattern: Root Execution

```dockerfile
# WRONG - Running as root
ENTRYPOINT ["/usr/local/bin/mybin"]

# CORRECT - Non-root user
USER 65532:65532
ENTRYPOINT ["/usr/local/bin/mybin"]
```

### Anti-Pattern: Single-Stage Build

```dockerfile
# WRONG - Build tools in final image
FROM debian:bookworm
RUN apt-get update && apt-get install -y build-essential
RUN make install
# Build tools, compilers, and package manager remain in final image

# CORRECT - Multi-stage build
FROM debian:bookworm AS builder
RUN apt-get update && apt-get install -y build-essential
RUN make install

FROM scratch
COPY --from=builder /usr/local/bin/mybin /usr/local/bin/mybin
# Only the binary in the final image
```

### Anti-Pattern: Placeholder Stubs

```dockerfile
# WRONG - Stub image
FROM cgr.dev/chainguard/wolfi-base
ENTRYPOINT ["true"]
# Does nothing. Move to images/_wip/ if not ready.

# CORRECT - Functional image
FROM scratch
COPY --from=downloader /usr/local/bin/mybin /usr/local/bin/mybin
ENTRYPOINT ["/usr/local/bin/mybin"]
```

### Anti-Pattern: Orphaned ARG GITHUB_TOKEN

```dockerfile
# WRONG - Unused ARG
ARG GITHUB_TOKEN
# Never referenced in any RUN, COPY, or ENV

# CORRECT - Remove unused ARG
# Only declare ARG when actually used
```

### Anti-Pattern: Phantom Version Tags

```dockerfile
# WRONG - Version that doesn't exist upstream
ENV MYBIN_VERSION=v1.18.0
# Verify against upstream releases first!

# CORRECT - Verified version
ENV MYBIN_VERSION=v1.30.0
# Confirmed at https://github.com/org/repo/releases
```

---

## Checklist

Before submitting a new or modified image:

- [ ] Dockerfile follows [Dockerfile Authoring Standards](dockerfile-standards.md)
- [ ] Multi-stage build with approved base image (scratch > wolfi > RHEL UBI)
- [ ] SHA256 checksum verification on all downloads
- [ ] Non-root user (UID 65532)
- [ ] HEALTHCHECK instruction with required parameters
- [ ] Health-shim as PID 1 (for scratch/wolfi images)
- [ ] `manifest.toml` with correct tier, version, and metadata
- [ ] `README.md` with usage instructions, env vars, and volumes
- [ ] `.dockerignore` file
- [ ] SBOM generated (`sbom.spdx.json`)
- [ ] Local build and test successful
- [ ] Pre-commit hooks pass
- [ ] No Alpine base images
- [ ] No hardcoded secrets
- [ ] BuildKit COPY eval workaround applied
- [ ] wolfi: wget instead of curl
- [ ] Tier labels set correctly
