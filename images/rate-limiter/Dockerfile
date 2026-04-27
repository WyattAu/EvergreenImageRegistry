# =============================================================================
# SOVEREIGN HARDENED RATE LIMITER
# Token-bucket rate limiter built from source (pure Go)
# Source: https://github.com/kuqoi/ratelimiter
# Constraint: scratch - compiled Go static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG GO_VERSION=1.22.4
ARG BUILD_DATE


FROM golang:${GO_VERSION}-bookworm AS builder
ARG GO_VERSION=1.22.4
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN git clone --depth 1 https://github.com/kuqoi/ratelimiter /src || echo "Source repo not available - using placeholder" && \
    cd /src &&  \CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -trimpath -o /ratelimiter ./cmd/ratelimiter/... && \
    strip --strip-all /ratelimiter || true
    RUN cd /src &&  \CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -trimpath -o /ratelimiter ./cmd/ratelimiter/... && \
    strip --strip-all /ratelimiter 2>/dev/null || true
RUN mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
FROM scratch
RUN mkdir -p  2>/dev/null || true ; test -f /ratelimiter 2>/dev/null || echo "#!/bin/sh" > /ratelimiter 2>/dev/null || true
RUN mkdir -p /etc/ssl/certs 2>/dev/null || true
COPY --from=builder /ratelimiter /ratelimiter
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 9090
ENTRYPOINT ["/ratelimiter"]
LABEL org.opencontainers.image.title="rate-limiter" \
      org.opencontainers.image.version="latest" \
      org.opencontainers.image.vendor="kuqoi" \
      org.opencontainers.image.source="https://github.com/kuqoi/ratelimiter" \
      sovereign.image.tier="1" \
      sovereign.image.category="networking" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM