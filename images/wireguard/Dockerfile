# =============================================================================
# SOVEREIGN HARDENED WIREGUARD-GO
# WireGuard userspace implementation in Go
# Constraint: scratch - pure Go static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.0.20230223
ARG BUILD_DATE

ARG GO_VERSION=1.22.4

FROM golang:${GO_VERSION}-bookworm AS builder
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN git clone --depth 1 --branch v${VERSION} https://git.zx2c4.com/wireguard-go /src && \
    cd /src && \
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-s -w -X main.version=${VERSION}" -trimpath -o /wireguard-go && \
    strip --strip-all /wireguard-go

FROM scratch
COPY --from=builder /wireguard-go /wireguard-go
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
EXPOSE 51820/udp
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["/wireguard-go", "--version"]
ENTRYPOINT ["/wireguard-go"]
CMD ["-f", "wg0"]
LABEL org.opencontainers.image.title="wireguard" \
      org.opencontainers.image.version="0.0.20230223" \
      org.opencontainers.image.vendor="WireGuard" \
      org.opencontainers.image.source="https://git.zx2c4.com/wireguard-go" \
      sovereign.image.tier="1" \
      sovereign.image.category="networking" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
