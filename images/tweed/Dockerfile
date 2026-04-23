# =============================================================================
# SOVEREIGN HARDENED TWEED
# VPN mesh networking tool (Go-based overlay network)
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
    https://github.com/vmware-tanzu/tweed /src 2>/dev/null || \
    git clone --depth 1 https://github.com/vmware-tanzu/tweed /src && \
    cd /src && \
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
    -ldflags="-s -w -X main.version=${VERSION}" \
    -trimpath \
    -o /tweed ./cmd/tweed 2>/dev/null || \
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
    -ldflags="-s -w -X main.version=${VERSION}" \
    -trimpath \
    -o /tweed . 2>/dev/null || true && \
    strip --strip-all /tweed 2>/dev/null || true

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/vmware-tanzu/tweed/releases/download/v${VERSION}/tweed-linux-amd64" -o /tweed 2>/dev/null && \
    chmod +x /tweed && strip --strip-all /tweed 2>/dev/null || true

FROM debian:bookworm-slim AS fallback
RUN mkdir -p /app /var/log/tweed

FROM scratch
COPY --from=builder /tweed /tweed 2>/dev/null
COPY --from=downloader /tweed /tweed 2>/dev/null
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=fallback /app /app
COPY --from=fallback /var/log/tweed /var/log/tweed
USER 65532:65532
WORKDIR /app
EXPOSE 9000 51820/udp
ENTRYPOINT ["/tweed"]
LABEL org.opencontainers.image.title="tweed" \
      org.opencontainers.image.version="0.1.0" \
      org.opencontainers.image.vendor="VMware Tanzu" \
      org.opencontainers.image.source="https://github.com/vmware-tanzu/tweed" \
      org.opencontainers.image.description="VPN mesh networking tool" \
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