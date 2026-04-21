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
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN git clone --depth 1 https://github.com/kuqoi/ratelimiter /src && \
    cd /src && \
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -trimpath -o /ratelimiter ./cmd/ratelimiter/... && \
    strip --strip-all /ratelimiter

FROM scratch
COPY --from=builder /ratelimiter /ratelimiter
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
EXPOSE 9090
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["/ratelimiter", "--help"]
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
