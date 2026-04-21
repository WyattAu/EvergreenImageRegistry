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
    chown -R 65534:65534 /app /var/log/wireguard /run/wireguard

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    wireguard-tools iproute2 iptables ca-certificates kmod && \
    rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
COPY --from=builder /var/log/wireguard /var/log/wireguard
COPY --from=builder /run/wireguard /run/wireguard
USER 65534:65534
WORKDIR /app
EXPOSE 51820/udp
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["/usr/bin/wg", "show"]
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
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
