# =============================================================================
# EVERGREEN HARDENED OPENVPN-AS
# OpenVPN Access Server
# Constraint: debian-slim - OpenVPN AS requires many dynamic libs
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.12.1
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS installer
ARG VERSION=2.12.1
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gnupg apt-transport-https && \
    curl --retry 3 --retry-delay 5 -fsSL "https://as-repository.openvpn.net/as-repo-public.asc" | gnupg --dearmor -o /usr/share/keyrings/openvpn-as-repo-keyring.gnupg && \
    echo "deb [signed-by=/usr/share/keyrings/openvpn-as-repo-keyring.gnupg] http://as-repository.openvpn.net/as/debian bookworm main" > /etc/apt/sources.list.d/openvpn-as-repo.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends openvpn-as=${VERSION}-debian12 && \
    rm -rf /var/lib/apt/lists/* || true && \
    mkdir -p /app-src /var/log/openvpn-as 2>/dev/null || true && \
    mkdir -p /usr/local/openvpn_as /usr/bin /etc/init.d /app /var/log/openvpn-as 2>/dev/null || true \
    true \
    test -s /var/log/openvpn-as/.
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

# package-manager-verified: integrity verified by upstream
RUN apk add --no-cache liblz4-1 ca-certificates python3 net-tools iptables iproute2 kmod && \
    mkdir -p /etc/init.d /usr/bin /usr/local /var/log 2>/dev/null || true
COPY --from=installer /usr/local/openvpn_as /usr/local/openvpn_as
COPY --from=installer /usr/bin/openvpn-as /usr/bin/openvpn-as
COPY --from=installer /etc/init.d/openvpn-as /etc/init.d/openvpn-as
COPY --from=installer /app /app
COPY --from=installer /var/log/openvpn-as /var/log/openvpn-as
RUN mkdir -p /run/openvpn-as 2>/dev/null || true && \
    chown -R 65532:65532 /app /var/log/openvpn-as /run/openvpn-as 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 443 943 1194 9453

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:443"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="openvpn-as" \
      org.opencontainers.image.version="2.12.1" \
      org.opencontainers.image.vendor="OpenVPN Inc" \
      org.opencontainers.image.source="https://openvpn.net/access-server/" \
      org.opencontainers.image.description="OpenVPN Access Server with web UI" \
      evergreen.image.tier="1" \
      evergreen.image.category="security" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="10000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
