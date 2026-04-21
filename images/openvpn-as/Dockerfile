# =============================================================================
# SOVEREIGN HARDENED OPENVPN-AS
# OpenVPN Access Server
# Constraint: debian-slim - OpenVPN AS requires many dynamic libs
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.12.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS installer
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gnupg2 apt-transport-https && \
    curl -fsSL "https://as-repository.openvpn.net/as-repo-public.asc" | gpg --dearmor -o /usr/share/keyrings/openvpn-as-repo-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/openvpn-as-repo-keyring.gpg] http://as-repository.openvpn.net/as/debian bookworm main" > /etc/apt/sources.list.d/openvpn-as-repo.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends openvpn-as=${VERSION}-debian12 && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/openvpn-as

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl3 liblzo2-2 liblz4-1 libpkcs11-helper1 ca-certificates \
    python3 net-tools iptables iproute2 kmod && \
    rm -rf /var/lib/apt/lists/*
COPY --from=installer /usr/local/openvpn_as /usr/local/openvpn_as
COPY --from=installer /usr/bin/openvpn-as /usr/bin/openvpn-as 2>/dev/null || true
COPY --from=installer /etc/init.d/openvpn-as /etc/init.d/openvpn-as 2>/dev/null || true
COPY --from=installer /app /app
COPY --from=installer /var/log/openvpn-as /var/log/openvpn-as
RUN mkdir -p /run/openvpn-as && \
    chown -R 65534:65534 /app /var/log/openvpn-as /run/openvpn-as
USER 65534:65534
WORKDIR /app
EXPOSE 443 943 1194 9453
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["/usr/local/openvpn_as/scripts/sacli", "--version"]
ENTRYPOINT ["/usr/local/openvpn_as/scripts/ovpn-init"]
LABEL org.opencontainers.image.title="openvpn-as" \
      org.opencontainers.image.version="2.12.1" \
      org.opencontainers.image.vendor="OpenVPN Inc" \
      org.opencontainers.image.source="https://openvpn.net/access-server/" \
      org.opencontainers.image.description="OpenVPN Access Server with web UI" \
      sovereign.image.tier="1" \
      sovereign.image.category="security" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms"
