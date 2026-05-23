# Dockerfile Authoring Standards

> **Scope:** Production-grade container images for the Evergreen Image Registry. All rules herein apply to every
> Dockerfile committed to this repository.

---

## 1. Base Image Selection

Reference: ADR-007.

The approved base image hierarchy, ordered by preference:

1. `scratch`
2. `wolfi` (wolfi-base)
3. `rhel/ubi9-micro`
4. `rhel/ubi9-minimal`
5. `rhel/ubi9`

**BANNED (permanently, no exceptions):** `debian-slim`, `alpine`, `ubuntu`, `centos`, `amazonlinux`.

The final stage of every Dockerfile MUST use one of the approved bases above.

Build stages MAY use `debian:bookworm` as a downloader or builder. The debian layer is discarded in the final image.

### DO

```dockerfile
FROM debian:bookworm AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*

FROM scratch AS final
COPY --from=downloader /usr/local/bin/mybin /usr/local/bin/mybin
```

### DO NOT

```dockerfile
FROM alpine:3.19 AS downloader
# alpine is permanently banned, even for build stages

FROM debian:bookworm AS final
# debian is banned as final stage
```

---

## 2. Multi-Stage Build Rules

Every image MUST use a multi-stage build. At minimum: a `downloader` (or `builder`) stage and a `final` stage.

### BuildKit COPY EVAL Bug

BuildKit evaluates `COPY --from=stage /path/file` source paths during the **solve phase**, BEFORE the `RUN` instruction
that creates the file has completed. This means:

- For **directory** references: the directory MUST exist before the RUN that populates it. Use `RUN mkdir -p /dir` in a
  **separate earlier** RUN step.
- For **file** references: the file MUST exist before the RUN that creates it. Use `RUN touch /path/file || true` in a
  **separate earlier** RUN step. A bare `mkdir -p` is **insufficient** for files.
- A path that is first created and then populated within the **same** RUN step will cause a COPY failure.

When possible, prefer single-stage wolfi builds that download directly with wget, avoiding the multi-stage COPY
entirely.

### DO

```dockerfile
FROM debian:bookworm AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /out/usr/local/bin
RUN touch /out/usr/local/bin/mybin || true
RUN curl -fsSL -o /out/usr/local/bin/mybin "https://example.com/mybin-v1.0.0"

FROM scratch AS final
COPY --from=downloader /out/usr/local/bin/mybin /usr/local/bin/mybin
```

### DO NOT

```dockerfile
FROM debian:bookworm AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL -o /usr/local/bin/mybin "https://example.com/mybin-v1.0.0"

FROM scratch AS final
COPY --from=downloader /usr/local/bin/mybin /usr/local/bin/mybin
# FAILS: /usr/local/bin/mybin does not exist when BuildKit evaluates the COPY source
```

### DO NOT

```dockerfile
FROM debian:bookworm AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /out/usr/local/bin && curl -fsSL -o /out/usr/local/bin/mybin "https://example.com/mybin-v1.0.0"

FROM scratch AS final
COPY --from=downloader /out/usr/local/bin/mybin /usr/local/bin/mybin
# FAILS: mkdir and curl are in the same RUN step; the file does not exist at solve time
```

---

## 3. Download Integrity

Every downloaded artifact MUST be verified with a SHA256 checksum. Reference: ADR-002.

### PLACEHOLDER_SHA Pattern

During initial image authoring, when the real checksum is not yet known, use a placeholder. The placeholder value MUST
be followed by `|| true` so that the intentional mismatch does not abort the build. MUST NOT use `|| exit 1`.

### Corrupted Checksums

SHA256 values MUST be exactly 64 hexadecimal characters. A recurring pattern of corrupted 96-character values (truncated
SHA256 concatenated with another truncated hash) has been observed. All checksums MUST be validated as 64 hex chars
before committing.

### DO -- Upstream Checksum File

```dockerfile
RUN curl -fsSL -o /tmp/mybin.tar.gz "https://example.com/mybin-v1.0.0.tar.gz" && \
    curl -fsSL -o /tmp/mybin.tar.gz.sha256 "https://example.com/mybin-v1.0.0.tar.gz.sha256" && \
    cd /tmp && sha256sum -c mybin.tar.gz.sha256
```

### DO -- Hardcoded Fallback

```dockerfile
RUN curl -fsSL -o /tmp/mybin.tar.gz "https://example.com/mybin-v1.0.0.tar.gz" && \
    echo "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2  /tmp/mybin.tar.gz" | sha256sum -c
```

### DO -- Placeholder (during development)

```dockerfile
RUN curl -fsSL -o /tmp/mybin.tar.gz "https://example.com/mybin-v1.0.0.tar.gz" && \
    echo "PLACEHOLDER_SHA  /tmp/mybin.tar.gz" | sha256sum -c || true
```

### DO NOT

```dockerfile
RUN curl -fsSL -o /tmp/mybin.tar.gz "https://example.com/mybin-v1.0.0.tar.gz" && \
    echo "PLACEHOLDER_SHA  /tmp/mybin.tar.gz" | sha256sum -c || exit 1
# exit 1 is redundant (sha256sum -c already exits non-zero on mismatch)
# and obscures the intent that this is a deliberate placeholder
```

### DO NOT

```dockerfile
RUN curl -fsSL -o /tmp/mybin.tar.gz "https://example.com/mybin-v1.0.0.tar.gz" && \
    echo "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2  /tmp/mybin.tar.gz" | sha256sum -c
# 96-char value: corrupted, not a valid SHA256
```

---

## 4. wolfi-Specific Rules

wolfi has NO `curl` package (confirmed via `locked_config.json`). busybox provides `wget` only.

### wget Substitutions

MUST use `wget` instead of `curl` in all wolfi contexts:

| Purpose            | curl (banned on wolfi)                     | wget (required on wolfi)                  |
| ------------------ | ------------------------------------------ | ----------------------------------------- |
| Download to file   | `curl -fsSL -o /path URL`                  | `wget -qO /path URL`                      |
| Download to stdout | `curl -fsSL URL`                           | `wget -qO- URL`                           |
| Healthcheck probe  | `curl -fsSL http://localhost:8080/healthz` | `wget -qO- http://localhost:8080/healthz` |

### DO

```dockerfile
FROM wolfi-base AS final
RUN apk add --no-cache ca-certificates
RUN wget -qO /tmp/mybin "https://example.com/mybin-v1.0.0" && \
    echo "a1b2c3...64chars  /tmp/mybin" | sha256sum -c
HEALTHCHECK --interval=30s --timeout=5s --retries=3 --start-period=10s \
    CMD wget -qO- http://localhost:8080/healthz || exit 1
```

### DO NOT

```dockerfile
FROM wolfi-base AS final
RUN apk add --no-cache curl || true
# curl silently not installed; apk exits 0 because of || true
# any subsequent RUN using curl will fail at runtime

HEALTHCHECK CMD curl -fsSL http://localhost:8080/healthz || exit 1
# curl does not exist in wolfi
```

### libc

Chainguard wolfi uses glibc, NOT musl. (Chainguard static uses musl.) Dynamic binaries linked against musl will fail to
load in a wolfi final stage at runtime. When downloading prebuilt binaries, prefer statically linked binaries or build
from source on wolfi.

### ca-certificates

`ca-certificates` is not guaranteed to be present in `wolfi-base`. MUST install explicitly:

```dockerfile
RUN apk add --no-cache ca-certificates
```

---

## 5. GITHUB_TOKEN Rules

`${{ secrets.GITHUB_TOKEN }}` is scoped to the current repository only. It authenticates as the `GITHUB_TOKEN` app with
read access limited to the repo where the workflow runs.

### DO -- Public Release (No Auth Needed)

```dockerfile
ARG MYBIN_VERSION=1.0.0
RUN curl -fsSL -o /tmp/mybin "https://github.com/org/repo/releases/download/v${MYBIN_VERSION}/mybin"
```

### DO -- Same-Repo Download with Guard

```dockerfile
ARG GITHUB_TOKEN
RUN if [ -n "${GITHUB_TOKEN}" ]; then \
        curl -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
            -o /tmp/mybin "https://github.com/${GITHUB_REPOSITORY}/releases/download/v${VERSION}/mybin"; \
    else \
        curl -fsSL -o /tmp/mybin "https://github.com/${GITHUB_REPOSITORY}/releases/download/v${VERSION}/mybin"; \
    fi
```

### DO NOT -- Cross-Repo with GITHUB_TOKEN

```dockerfile
ARG GITHUB_TOKEN
RUN curl -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    -o /tmp/other-repo-bin "https://github.com/other-org/other-repo/releases/download/v1.0.0/bin"
# GITHUB_TOKEN is scoped to THIS repo only. Cross-repo returns 404.
```

### DO NOT -- Orphaned ARG

```dockerfile
ARG GITHUB_TOKEN
# Declared but never used in any RUN, COPY, or ENV
# Wastes build cache layer on token change
```

---

## 6. Shell Compatibility Rules

Debian uses `dash` as `/bin/sh`. All `RUN` commands execute under `/bin/sh` unless `RUN ["/bin/bash", "-c", "..."]` is
used. The following bash-only constructs MUST NOT appear in unqualified RUN instructions.

### Banned Bash-Only Syntax

| Construct       | Example              | Why it fails on dash       |
| --------------- | -------------------- | -------------------------- |
| Brace expansion | `echo {a,b,c}`       | No brace expansion in dash |
| `[[ ]]`         | `[[ -f /tmp/file ]]` | No `[[` in dash            |
| Arrays          | `arr=(a b c)`        | No arrays in dash          |
| `&>` redirect   | `cmd &>/dev/null`    | Not recognized by dash     |
| Here-strings    | `cmd <<< "input"`    | Not recognized by dash     |

### DO

```dockerfile
RUN if [ -f /tmp/file ]; then echo "exists"; fi && \
    printf '%s\n' "line1" "line2" "line3" > /tmp/config
```

### DO NOT

```dockerfile
RUN if [[ -f /tmp/file ]]; then echo "exists"; fi && \
    echo -e "line1\nline2\nline3" > /tmp/config
# [[ ]] is bash-only; echo -e behavior varies across shells
```

### RUN Line Continuation

Backslash `\` MUST be the last character on the line (no trailing whitespace, no trailing comment, no trailing
semicolon).

### DO

```dockerfile
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
```

### DO NOT

```dockerfile
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates; true
# Missing \ after ; true -- next line parsed as a Dockerfile instruction, not a shell continuation

# comment && \
apt-get install -y curl
# Backslash is inside the comment. Subsequent lines silently discarded.
```

---

## 7. Go Source Build Rules

### GOTOOLCHAIN

Go 1.25+ requires `GOTOOLCHAIN=auto` when the base image ships Go 1.24. Without this, Go refuses to download the
required toolchain and the build fails.

### DO

```dockerfile
FROM golang:1.24 AS builder
ENV GOTOOLCHAIN=auto
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o /out/mybin ./cmd/mybin
```

### DO NOT

```dockerfile
FROM golang:1.24 AS builder
# Missing GOTOOLCHAIN=auto
# If go.mod requires go 1.25.0, build fails with:
# go: go.mod requires go >= 1.25.0 (running go 1.24.x)
```

### multiarch in manifest.toml

Go source builds with `multiarch = true` will attempt QEMU-emulated arm64 builds. Go 1.25 toolchain bootstrap under QEMU
exits with code 255. MUST set `multiarch = false` in `manifest.toml` for all Go source builds.

### GONOSUMCHECK

Private Go modules (not proxied by a checksum database) MUST be listed in `GONOSUMCHECK`:

```dockerfile
ENV GONOSUMCHECK=github.com/your-org/private-module/*
```

---

## 8. External FROM References

Every `FROM` instruction referencing an external image MUST reference a valid, publicly pullable tag.

### DO

```dockerfile
FROM golang:1.24-bookworm AS builder
# Verify: docker pull golang:1.24-bookworm
```

### DO NOT

```dockerfile
FROM golang:1.99-bookworm AS builder
# Tag never existed; build fails at pull time
```

### Verification

Before committing a Dockerfile with a new or changed external FROM reference, the author MUST verify the tag exists
using one of:

```bash
docker pull golang:1.24-bookworm
docker manifest inspect golang:1.24-bookworm
skopeo inspect docker://golang:1.24-bookworm
```

When an upstream project removes a release tag, find an alternative source or mark the image as deprecated (see Section
11).

---

## 9. Version Pinning Rules

MUST NOT pin a version that does not exist in the upstream release history. Verify against the upstream GitHub Releases
page or package repository before committing.

### DO NOT -- Phantom Versions

```dockerfile
# dragonflydb: v1.18.0 never existed. Releases jumped from 1.x to 1.3x.
ENV DRAGONFLY_VERSION=v1.18.0

# vault-secrets-operator: 1.19.0 was confused with Vault server version.
ENV VSO_VERSION=1.19.0

# cstate: 5.7.0 never existed. Releases jumped from 5.6.1 to 6.0.0.
ENV CSTATE_VERSION=5.7.0
```

### DO

```dockerfile
# Verified against https://github.com/dragonflydb/dragonfly/releases
ENV DRAGONFLY_VERSION=v1.30.0

# Verified against https://github.com/hashicorp/vault-secrets-operator/releases
ENV VSO_VERSION=0.10.0

# Verified against https://github.com/cstate/cstate/releases
ENV CSTATE_VERSION=6.0.0
```

---

## 10. Dockerfile Hygiene

### Structure

The instruction order within the final stage MUST be:

1. `FROM`
2. `LABEL` (metadata, maintainer, evergreen.\* labels)
3. `EXPOSE`
4. `WORKDIR`
5. `COPY` / `RUN` (installation)
6. `HEALTHCHECK`
7. `USER`
8. `ENTRYPOINT`
9. `CMD`
10. `STOPSIGNAL SIGTERM`

### USER

All images MUST run as a non-root user. The standard is `USER 65532:65532` (the `nonroot` UID/GID from the OpenShift SCC
range). A single `USER` instruction MUST appear in the final stage.

### HEALTHCHECK

All images exposing a network service MUST include a HEALTHCHECK with these parameters:

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --retries=3 --start-period=10s \
    CMD wget -qO- http://localhost:8080/healthz || exit 1
```

Parameter constraints:

| Parameter        | Required Value |
| ---------------- | -------------- |
| `--interval`     | `30s`          |
| `--timeout`      | `5s`           |
| `--retries`      | `3`            |
| `--start-period` | `10s`          |

### Formatting

- Maximum 1 consecutive blank line between logical sections.
- MUST NOT produce Dockerfiles exceeding 120 lines for simple binary-download images. Complex source-build images MAY
  exceed this but MUST be justified.
- Comments MUST explain WHY, not WHAT. The code already explains what.

### DO

```dockerfile
FROM scratch AS final

LABEL org.opencontainers.image.source="https://github.com/org/mybin" \
      org.opencontainers.image.version="1.0.0"

EXPOSE 8080

WORKDIR /app

COPY --from=downloader /usr/local/bin/mybin /usr/local/bin/mybin

HEALTHCHECK --interval=30s --timeout=5s --retries=3 --start-period=10s \
    CMD ["/usr/local/bin/mybin", "--healthcheck-addr=:8080"]

USER 65532:65532

ENTRYPOINT ["/usr/local/bin/mybin"]

STOPSIGNAL SIGTERM
```

### DO NOT

```dockerfile
FROM scratch AS final

# Copy the binary
COPY --from=downloader /usr/local/bin/mybin /usr/local/bin/mybin

# Set working directory
WORKDIR /app

# Expose port 8080
EXPOSE 8080

# Health check
HEALTHCHECK CMD wget -qO- http://localhost:8080/healthz || exit 1
# Missing interval, timeout, retries, start-period

ENTRYPOINT ["/usr/local/bin/mybin"]
# Missing USER instruction
# Missing STOPSIGNAL
```

---

## 11. No Stubs or Skeleton Images (C026)

Every image MUST contain a functional application binary. Placeholder stubs are prohibited.

### DO NOT

```dockerfile
FROM cgr.dev/chainguard/wolfi-base
RUN apk add --no-cache ca-certificates curl
ENTRYPOINT ["true"]
# This is a stub. It does nothing. It MUST NOT be in the build matrix.
```

If an image cannot be completed (no upstream binary, proprietary, not containerizable), move it to `images/_wip/<name>/`
with `LABEL evergreen.status="wip"`. Do not leave it in the active `images/` directory.

---

## 12. libc Consistency Across Stages (C027)

Compiled artifacts MUST use the same libc as the final stage. Copying glibc-compiled artifacts (Python C extensions,
Node native modules) into a wolfi/musl final stage will crash at runtime.

### DO

```dockerfile
# Option A: Build Python venv inside wolfi (preferred)
FROM cgr.dev/chainguard/wolfi-base AS builder
RUN apk add --no-cache python3 py3-pip py3-gcc py3-dev
RUN pip install --no-cache-dir psycopg2 Pillow cryptography

FROM cgr.dev/chainguard/wolfi-base
COPY --from=builder /usr/lib/python3 /usr/lib/python3
# C extensions compiled against musl -- compatible with wolfi final stage
```

```dockerfile
# Option B: If musl compilation fails, use glibc final stage
FROM python:3.12-slim AS builder
RUN pip install --no-cache-dir psycopg2 Pillow cryptography

FROM registry.access.redhat.com/ubi9/ubi-minimal
COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=builder /usr/local/bin/python3.12 /usr/local/bin/python3.12
# C extensions compiled against glibc -- compatible with UBI final stage
LABEL evergreen.base.fallback_reason="Python C extensions require glibc"
```

### DO NOT

```dockerfile
FROM python:3.12-slim AS builder
RUN pip install psycopg2 Pillow cryptography  # compiled against glibc

FROM cgr.dev/chainguard/wolfi-base
COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
# CRASH: import psycopg2 -> ImportError: libc.so.6: version GLIBC_2.34 not found
```

---

## 13. Configurable Runtime UID (C028)

Every image MUST support `APP_UID` and `APP_GID` environment variables for runtime UID override. Default: 65532:65532.

### DO

```dockerfile
ARG APP_UID=65532
ARG APP_GID=65532

FROM cgr.dev/chainguard/wolfi-base AS builder
# ... download application ...

FROM scratch
COPY --from=builder /usr/local/bin/mybin /usr/local/bin/mybin
COPY --from=builder /usr/local/bin/su-exec /usr/local/bin/su-exec
COPY --from=builder /usr/local/bin/entrypoint /usr/local/bin/entrypoint

RUN mkdir -p /etc/passwd /etc/group
# Build-time user creation
RUN echo "appuser:x:${APP_UID}:${APP_GID}:appuser:/app:/sbin/nologin" >> /etc/passwd && \
    echo "appgroup:x:${APP_GID}:" >> /etc/group

USER 65532:65532
ENTRYPOINT ["/usr/local/bin/entrypoint"]
CMD ["/usr/local/bin/mybin"]
```

The entrypoint script handles runtime UID remapping:

```sh
#!/bin/sh
TARGET_UID="${APP_UID:-65532}"
TARGET_GID="${APP_GID:-65532}"

if [ "$(id -u)" != "${TARGET_UID}" ]; then
  # Running with overridden UID
  echo "appuser:x:${TARGET_UID}:${TARGET_GID}:appuser:/app:/sbin/nologin" > /etc/passwd
  echo "appgroup:x:${TARGET_GID}:" > /etc/group
  chown -R "${TARGET_UID}:${TARGET_GID}" /data /var/lib/app 2>/dev/null || true
fi

exec su-exec appuser "$@"
```

### DO NOT

```dockerfile
USER 65532:65532
# No APP_UID/APP_GID support -- consumers with existing volume permissions cannot use this image
```

---

## 14. Data Service Initialization (C029)

Images for databases, message queues, and key-value stores MUST include upstream initialization entrypoint scripts for
self-contained operation. They MUST also support binary-only mode for orchestrator-managed initialization.

### DO

```dockerfile
# Self-contained mode (default): upstream entrypoint handles init
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["postgres"]

# Binary-only mode: override at runtime
# docker run --entrypoint postgres myimage:tag -c config_file=/etc/postgresql/postgresql.conf
```

The upstream `docker-entrypoint.sh` script handles first-run detection, data store initialization, user/database
creation from environment variables, and configuration rendering.

---

## 15. Deprecated Image Handling

When an upstream project is archived, deleted, or no longer releases, the image MUST be marked as deprecated.

### Required Actions

1. Add deprecation label to the Dockerfile:

```dockerfile
LABEL evergreen.status="deprecated" \
      evergreen.deprecation.reason="Upstream project archived on 2025-03-15" \
      evergreen.deprecation.last-known-version="1.0.0" \
      evergreen.deprecation.suggested-alternative="org/alternative-image"
```

1. Remove the image from the active build matrix (e.g., remove from CI workflow dispatch inputs, image listing scripts).
2. Keep the Dockerfile in the repository for historical reference. Do NOT delete it.
3. Document in the image's README:

```markdown
## Status: DEPRECATED

- **Last known good version:** 1.0.0
- **Reason:** Upstream project archived on 2025-03-15. No further releases expected.
- **Suggested alternative:** org/alternative-image (active, maintained)
```

### DO NOT

Delete the Dockerfile or leave the image in the active build matrix without a deprecation label.

---

## 16. Metrics Endpoint Convention

Images that are Prometheus exporters or monitoring agents MUST expose metrics in the Prometheus exposition format.
Application images SHOULD expose metrics if the upstream binary supports it.

### Port Convention

| Image Type                      | Port             | Example                           |
| ------------------------------- | ---------------- | --------------------------------- |
| Standalone exporter             | `9100`           | node-exporter, zfs-exporter       |
| Application with native metrics | Application port | Traefik on 8080, Keycloak on 9000 |
| Proxy/middleware                | Application port | oauth2-proxy on 4180              |

### Path Convention

- **Path:** `/metrics` (Prometheus ecosystem standard)
- **Exception:** Upstream applications with non-overridable paths (e.g., Synapse `/_synapse/metrics`). Document the
  exception in a Dockerfile comment.

### OCI Labels

Images exposing a metrics endpoint MUST include these labels:

```dockerfile
LABEL org.opencontainers.image.metrics.port="9100" \
      org.opencontainers.image.metrics.path="/metrics"
```

### Expose Directive

The metrics port MUST be listed in `EXPOSE`. If the image also serves an application on a different port, both ports
MUST be listed:

```dockerfile
EXPOSE 8080 9100
```

### DO

```dockerfile
FROM scratch AS final

LABEL org.opencontainers.image.metrics.port="9100" \
      org.opencontainers.image.metrics.path="/metrics"

EXPOSE 9100

HEALTHCHECK --interval=30s --timeout=5s --retries=3 --start-period=10s \
    CMD wget -qO- http://localhost:9100/metrics || exit 1

USER 65532:65532
ENTRYPOINT ["/usr/local/bin/exporter"]
STOPSIGNAL SIGTERM
```

### DO NOT

```dockerfile
EXPOSE 8080
# Missing metrics port in EXPOSE -- metrics port undocumented

ENTRYPOINT ["/usr/local/bin/exporter"]
# No HEALTHCHECK against the metrics endpoint -- upstream may change the path
# silently and go undetected
```
