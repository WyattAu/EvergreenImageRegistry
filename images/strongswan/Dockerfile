# =============================================================================
# SOVEREIGN HARDENED STRONGSWAN
# IPsec-based VPN (IKEv1/IKEv2)
# Constraint: debian-slim - strongswan requires dynamic libs and plugins
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=5.9.14
ARG BUILD_DATE

FROM debian:bookworm-slim AS installer
RUN apt-get update && apt-get install -y --no-install-recommends \
    strongswan strongswan-pki libcharon-extra-plugins \
    libcharon-extauth-plugins libstrongswan-extra-plugins && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/strongswan /var/run/charon /etc/strongswan.d && \
    find /usr -type f -executable -name "charon*" -exec strip --strip-all {} \; 2>/dev/null || true && \
    find /usr -type f -executable -name "strongswan*" -exec strip --strip-all {} \; 2>/dev/null || true && \
    find /usr -type f -executable -name "pki" -exec strip --strip-all {} \; 2>/dev/null || true && \
    find /usr -type f -executable -name "swanctl" -exec strip --strip-all {} \; 2>/dev/null || true

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl3 libgmp10 ca-certificates \
    iproute2 iptables kmod && \
    rm -rf /var/lib/apt/lists/*
COPY --from=installer /usr/sbin/charon /usr/sbin/charon
COPY --from=installer /usr/sbin/charon-systemd /usr/sbin/charon-systemd 2>/dev/null || true
COPY --from=installer /usr/sbin/strongswan /usr/sbin/strongswan
COPY --from=installer /usr/sbin/pki /usr/sbin/pki
COPY --from=installer /usr/sbin/swanctl /usr/sbin/swanctl
COPY --from=installer /usr/sbin/ipsec /usr/sbin/ipsec
COPY --from=installer /usr/lib/ipsec /usr/lib/ipsec
COPY --from=installer /usr/lib/strongswan /usr/lib/strongswan
COPY --from=installer /usr/lib/*/strongswan /usr/lib/strongswan-plugins 2>/dev/null || true
COPY --from=installer /etc/strongswan /etc/strongswan
COPY --from=installer /app /app
COPY --from=installer /var/log/strongswan /var/log/strongswan
RUN mkdir -p /run/charon /etc/strongswan.d && \
    chown -R 65534:65534 /app /var/log/strongswan /run/charon
USER 65534:65534
WORKDIR /app
EXPOSE 500 500/udp 4500 4500/udp
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/sbin/swanctl", "--stats"]
ENTRYPOINT ["/usr/sbin/charon"]
LABEL org.opencontainers.image.title="strongswan" \
      org.opencontainers.image.version="5.9.14" \
      org.opencontainers.image.vendor="strongSwan Project" \
      org.opencontainers.image.source="https://github.com/strongswan/strongswan" \
      org.opencontainers.image.description="IPsec-based VPN (IKEv1/IKEv2)" \
      sovereign.image.tier="1" \
      sovereign.image.category="security" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="5000ms"
