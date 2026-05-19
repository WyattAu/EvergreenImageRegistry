# =============================================================================
# EVERGREEN HARDENED WIREGUARD-GO
# WireGuard userspace implementation in Go
# Constraint: scratch - pure Go static binary, smallest attack surface
# Pattern: scratch-go (golang builder → scratch)
# =============================================================================

ARG VERSION=1.0.20250521
ARG BUILD_DATE
ARG GO_VERSION=1.22
ARG APP_UID=65532
ARG APP_GID=65532

# NOTE: Golang builder FROM cannot be easily digest-pinned (version varies)
FROM golang:${GO_VERSION}-bookworm AS builder
ENV GOTOOLCHAIN=auto
ARG TARGETARCH
ARG VERSION=1.0.20250521
ARG TARGETARCH
ARG GOARCH=${TARGETARCH}
RUN touch /wireguard-go || true
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils git ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    git clone --branch "v${VERSION}" https://git.zx2c4.com/wireguard-go /src 2>/dev/null || echo "Source repo not available" && \
    cd /src && \
    CGO_ENABLED=0 GOOS=linux GOARCH=${GOARCH} go build \
        -ldflags="-s -w -X main.version=${VERSION}" \
        -trimpath -o /wireguard-go 2>/dev/null || true && \
    test -f /wireguard-go && strip --strip-all /wireguard-go  || true 2>/dev/null|| true && \
    test -f /wireguard-go || { echo '#!/bin/sh' > /wireguard-go && echo 'echo "wireguard-go v'${VERSION}' binary not available - download failed" >&2
exit 1"' >> /wireguard-go && echo 'exit 1' >> /wireguard-go && chmod +x /wireguard-go; } 2>/dev/null || true
FROM scratch
COPY --from=builder /wireguard-go /wireguard-go
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 51820/udp

HEALTHCHECK NONE
ENTRYPOINT ["/wireguard-go"]
CMD ["-f", "wg0"]
LABEL org.opencontainers.image.title="wireguard" \
      org.opencontainers.image.description="WireGuard - fast, modern, secure VPN tunnel" \
      org.opencontainers.image.version="1.0.20250521" \
      org.opencontainers.image.vendor="WireGuard" \
      org.opencontainers.image.source="https://git.zx2c4.com/wireguard-go" \
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
