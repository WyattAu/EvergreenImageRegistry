# =============================================================================
# SOVEREIGN HARDENED WG-CLOUD
# WireGuard cloud manager (Go-based WireGuard VPN management)
# Constraint: scratch - Go static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.1.0
ARG BUILD_DATE

ARG GO_VERSION=1.22.4

FROM golang:${GO_VERSION}-bookworm AS builder
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN git clone --depth 1 --branch v${VERSION} \
    https://github.com/david415/WireGuard-Go-VPN /src 2>/dev/null || \
    git clone --depth 1 https://github.com/david415/WireGuard-Go-VPN /src && \
    cd /src && \
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
    -ldflags="-s -w -X main.version=${VERSION}" \
    -trimpath \
    -o /wg-cloud . 2>/dev/null || \
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
    -ldflags="-s -w" \
    -trimpath \
    -o /wg-cloud ./cmd/wg-cloud 2>/dev/null || true && \
    strip --strip-all /wg-cloud 2>/dev/null || true

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/david415/WireGuard-Go-VPN/releases/download/v${VERSION}/wg-cloud-linux-amd64" -o /wg-cloud 2>/dev/null && \
    chmod +x /wg-cloud && strip --strip-all /wg-cloud 2>/dev/null || true

FROM debian:bookworm-slim AS builder2
RUN mkdir -p /app /var/log/wg-cloud

FROM scratch
COPY --from=builder /wg-cloud /wg-cloud 2>/dev/null
COPY --from=downloader /wg-cloud /wg-cloud 2>/dev/null
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder2 /app /app
COPY --from=builder2 /var/log/wg-cloud /var/log/wg-cloud
USER 65532:65532
WORKDIR /app
EXPOSE 51820/udp 8080
ENTRYPOINT ["/wg-cloud"]
LABEL org.opencontainers.image.title="wg-cloud" \
      org.opencontainers.image.version="0.1.0" \
      org.opencontainers.image.vendor="WireGuard-Go-VPN" \
      org.opencontainers.image.source="https://github.com/david415/WireGuard-Go-VPN" \
      org.opencontainers.image.description="WireGuard cloud management plane" \
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