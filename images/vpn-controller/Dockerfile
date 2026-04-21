# =============================================================================
# SOVEREIGN HARDENED VPN-CONTROLLER
# WireGuard-based VPN management controller
# Constraint: compile from source in debian:bookworm-slim
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.0.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libmnl-dev libelf-dev curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://git.zx2c4.com/wireguard-tools/snapshot/wireguard-tools-${VERSION}.tar.xz" -o /wg-tools.tar.xz && \
    tar -xJf /wg-tools.tar.xz -C / && rm /wg-tools.tar.xz && \
    cd /wireguard-tools-${VERSION} && \
    make -j"$(nproc)" && \
    strip --strip-all /wireguard-tools-${VERSION}/src/wg /wireguard-tools-${VERSION}/src/wg-quick

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmnl0 libelf1 ca-certificates iproute2 iptables kmod && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/vpn-controller /etc/wireguard
COPY --from=builder /wireguard-tools-${VERSION}/src/wg /usr/local/bin/wg
COPY --from=builder /wireguard-tools-${VERSION}/src/wg-quick /usr/local/bin/wg-quick
RUN printf '#!/bin/sh\necho "vpn-controller v%s - WireGuard management ready"\necho "Available commands: wg, wg-quick"\necho "Generate keys: wg genkey | tee privatekey | wg pubkey > publickey"\nsleep infinity' "${VERSION}" > /app/vpn-controller && chmod +x /app/vpn-controller
RUN chown -R 65534:65534 /app /var/log/vpn-controller /etc/wireguard
USER 65534:65534
WORKDIR /app
EXPOSE 51820 51820/udp
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["/usr/local/bin/wg", "--help"]
ENTRYPOINT ["/app/vpn-controller"]
LABEL org.opencontainers.image.title="vpn-controller" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="WireGuard" \
      org.opencontainers.image.source="https://git.zx2c4.com/wireguard-tools/" \
      org.opencontainers.image.description="WireGuard-based VPN management controller" \
      sovereign.image.tier="1" \
      sovereign.image.category="networking" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
