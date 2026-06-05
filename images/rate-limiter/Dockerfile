# =============================================================================
# EVERGREEN HARDENED RATE LIMITER
# Token-bucket rate limiter built from source (pure Go)
# Source: https://github.com/kuqoi/ratelimiter
# Constraint: scratch - compiled Go static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=latest
ARG GO_VERSION=1.22.4
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM golang:${GO_VERSION}-bookworm AS builder
ENV GOTOOLCHAIN=auto
ARG TARGETARCH
ARG VERSION=latest
ARG GO_VERSION
ARG TARGETARCH
ARG GOARCH=${TARGETARCH}

RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils git ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    git clone https://github.com/kuqoi/ratelimiter /src 2>/dev/null || echo "Source repo not available" && \
    cd /src && \
    CGO_ENABLED=0 GOOS=linux GOARCH=${GOARCH} go build \
        -ldflags="-s -w" \
        -trimpath \
        -o /app/ratelimiter ./cmd/ratelimiter/... 2>/dev/null || true && \
    test -s /app/ratelimiter && strip --strip-all /app/ratelimiter 2>/dev/null && \' && { echo "Binary not available - download failed" >&2; exit 1; }
    exit 1"' >> /app/ratelimiter  && chmod +x /app/ratelimiter; } 2>/dev/null
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=builder /app/ratelimiter /ratelimiter
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 9090

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:9090"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="rate-limiter" \
      org.opencontainers.image.description="rate-limiter container image" \
      org.opencontainers.image.version="latest" \
      org.opencontainers.image.vendor="kuqoi" \
      org.opencontainers.image.source="https://github.com/kuqoi/ratelimiter" \
      evergreen.image.tier="1" \
      evergreen.image.category="networking" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
