# =============================================================================
# SOVEREIGN HARDENED WG-QUICK
# WireGuard quick setup wrapper with wireguard-tools
# Constraint: debian-slim - requires shell, iproute2, and wireguard-tools
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.0.20210914
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    wireguard-tools iproute2 iptables kmod && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/wireguard /run/wireguard && \
    chown -R 65532:65532 /app /var/log/wireguard /run/wireguard

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007

RUN apk add --no-cache wireguard-tools iproute2 iptables ca-certificates kmod
COPY --from=builder /app /app
COPY --from=builder /var/log/wireguard /var/log/wireguard
COPY --from=builder /run/wireguard /run/wireguard
USER 65532:65532
WORKDIR /app
EXPOSE 51820/udp
ENTRYPOINT ["/usr/bin/wg-quick"]
LABEL org.opencontainers.image.title="wg-quick" \
      org.opencontainers.image.version="1.0.20210914" \
      org.opencontainers.image.vendor="WireGuard" \
      org.opencontainers.image.source="https://www.wireguard.com" \
      org.opencontainers.image.description="WireGuard quick setup wrapper with wireguard-tools" \
      sovereign.image.tier="1" \
      sovereign.image.category="networking" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM