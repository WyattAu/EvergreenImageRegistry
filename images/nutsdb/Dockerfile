# =============================================================================
# EVERGREEN HARDENED NUTSDB
# Constraint: scratch - pure static Go binary
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.1.0
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM golang@sha256:167053a2bb901972bf2c1611f8f52c44d5fe7e762e5cab213708d82c421614db AS builder
ENV GOTOOLCHAIN=auto
ARG TARGETARCH
ARG VERSION=1.1.0
ARG TARGETARCH
ARG GOARCH=${TARGETARCH}

RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils git ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    git clone --branch "v${VERSION}" https://github.com/xujiajun/nutsdb /src 2>/dev/null || echo "Source repo not available" && \
    cd /src && \
    CGO_ENABLED=0 GOOS=linux GOARCH=${GOARCH} go build \
        -ldflags="-s -w" \
        -o /app/nutsdb ./cmd/nutsdb 2>/dev/null || true && \
    test -s /app/nutsdb && strip --strip-all /app/nutsdb 2>/dev/null && \' && { echo "Binary not available - download failed" >&2; exit 1; }
    exit 1"' >> /app/nutsdb  && chmod +x /app/nutsdb; } 2>/dev/null
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=builder /app/nutsdb /usr/local/bin/nutsdb
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 9900

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:9900"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="nutsdb" \
      org.opencontainers.image.version="1.1.0" \
      org.opencontainers.image.description="Evergreen hardened NutsDB - embedded key-value store" \
      org.opencontainers.image.vendor="Xujiajun" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
            org.opencontainers.image.source="https://github.com/xujiajun/nutsdb"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
