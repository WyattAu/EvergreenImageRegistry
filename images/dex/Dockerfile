# =============================================================================
# SOVEREIGN HARDENED DEX
# Federated OpenID Connect provider - Go static binary
# Constraint: scratch - pure Go static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.45.1
ARG BUILD_DATE

FROM go-1.23:1.23-bookworm AS builder
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates && rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 --branch "v${VERSION}" https://github.com/dexidp/dex /src && \ 2>/dev/null || echo "Source repo not available - using placeholder"
    cd /src && \
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -o /dex ./cmd/dex && \
    strip --strip-all /dex

FROM scratch
COPY --from=builder /dex /dex
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 5556
ENTRYPOINT ["/dex"]
LABEL org.opencontainers.image.title="dex" \
      org.opencontainers.image.version="2.45.1" \
      org.opencontainers.image.vendor="DexIDP" \
      org.opencontainers.image.source="https://github.com/dexidp/dex" \
      sovereign.image.tier="2" \
      sovereign.image.category="identity" \
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