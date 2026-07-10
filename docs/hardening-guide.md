# Image Hardening Cookbook

> Patterns and templates for hardening container images

## Hardening Patterns

### Pattern 1: Go Binary → Scratch

**Best for:** Go applications (Prometheus exporters, NATS, Traefik, etc.)

```dockerfile
ARG VERSION=v1.0.0
ARG SHIM_VERSION=v2.0.0

FROM debian:bookworm-slim AS downloader
ARG VERSION
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    arch=$(case ${TARGETARCH} in amd64) echo "linux-amd64";; arm64) echo "linux-arm64";; esac) && \
    curl -fsSL "https://github.com/<org>/<repo>/releases/download/${VERSION}/<binary>${VERSION}.${arch}.tar.gz" \
      -o /tmp/app.tar.gz && \
    tar -xzf /tmp/app.tar.gz -C /tmp && \
    cp /tmp/<binary> /app && chmod +x /app

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=downloader /app /usr/local/bin/app
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532
EXPOSE 8080 9101
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/usr/local/bin/app"]
```

**Examples:** redis, traefik, prometheus, alertmanager, grafana, nats, node-exporter

### Pattern 2: Chainguard Wolfi Repack

**Best for:** Complex applications needing glibc (PostgreSQL, MariaDB)

```dockerfile
ARG SHIM_VERSION=v2.0.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/<app>:latest
USER 0
COPY --from=shim /shim /usr/local/bin/shim
RUN chown -R <uid>:<gid> /var/lib/<app> 2>/dev/null || true
USER <uid>

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:<port>"]
```

**Examples:** postgresql-16 (UID 70), mariadb (UID 65532)

### Pattern 3: Source Build → Scratch

**Best for:** C/C++ applications that can be statically linked

```dockerfile
ARG VERSION=7.0.0
ARG SHIM_VERSION=v2.0.0

FROM debian:bookworm-slim AS builder
ARG VERSION
RUN apt-get update && apt-get install -y build-essential curl && \
    curl -fsSL "https://example.com/app-${VERSION}.tar.gz" | tar -xz && \
    cd app-${VERSION} && \
    make MALLOC=libc && \
    cp src/app /app

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=builder /app /usr/local/bin/app

USER 65532:65532
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/usr/local/bin/app"]
```

**Examples:** redis (source build with MALLOC=libc)

### Pattern 4: Upstream Repack (Non-Root)

**Best for:** Applications with no binary download and no Chainguard equivalent

```dockerfile
ARG SHIM_VERSION=v2.0.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM <upstream>:<version>
COPY --from=shim /shim /usr/local/bin/shim
HEALTHCHECK CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:<port>"]
# Note: No USER override — inherit upstream's user model
```

**Examples:** vaultwarden, freshrss, paperless-ngx

### Pattern 5: Wolfi apk-install

**Best for:** Applications needing shared libraries but minimal base

```dockerfile
ARG SHIM_VERSION=v2.0.0

FROM cgr.dev/chainguard/wolfi-base:latest AS base
RUN apk add --no-cache nginx && \
    mkdir -p /var/lib/nginx /var/log/nginx /run/nginx && \
    chown -R 65532:65532 /var/lib/nginx /var/log/nginx /run/nginx

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=base / /

USER 65532:65532
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "nginx"]
```

**Examples:** nginx

## Verification Checklist

For each hardened image, verify ALL of the following:

- [ ] **Build succeeds** — `docker build` completes without error
- [ ] **Non-root user** — `docker inspect --format '{{.Config.User}}'` returns non-root UID
- [ ] **No shell** — `docker run --rm --entrypoint "" <img> sh -c "echo test"` fails
- [ ] **Health check works** — Container starts and HEALTHCHECK passes within start-period
- [ ] **Metrics available** — `curl http://localhost:9101/metrics` returns data (if shim enabled)
- [ ] **App functional** — Application-specific test passes (HTTP, TCP, DB query)
- [ ] **Signed** — `cosign verify` succeeds
- [ ] **SBOM exists** — `cosign verify-attestation --type spdxjson` succeeds

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Container exits immediately | Binary not found at expected path | Check `COPY --from=downloader` paths |
| Permission denied | Non-root UID can't write to data dir | Use `--tmpfs /data:uid=65532,gid=65532` or pre-create directories |
| HEALTHCHECK fails | App needs more startup time | Increase `--start-period` |
| Can't bind port | Port < 1024 requires root | Use ports > 1024 or add `NET_BIND_SERVICE` capability |
| Missing CA certs | scratch has no certs | `COPY --from=downloader /etc/ssl/certs/ca-certificates.crt` |
| DNS resolution fails | scratch has no /etc/resolv.conf | Mount or copy resolv.conf |
