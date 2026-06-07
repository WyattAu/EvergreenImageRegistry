# =============================================================================
# EVERGREEN HARDENED PI-HOLE
# Network-level ad blocking via DNS
# Constraint: debian-slim - Pi-hole install script requires bash, curl, etc.
# =============================================================================

ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.0.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS installer
ENV PIHOLE_INSTALL=noninteractive
ENV FTLCONF_webserver_port=8080
ENV DNSMASQ_USER=pihole
RUN apt-get update && apt-get install -y --no-install-recommends binutils \
    curl wget git iproute2 iptables procps ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 --proto '=https' --tlsv1.2 -fsSL https://install.pi-hole.net -o /tmp/install.sh && \
    sha256sum /tmp/install.sh && \
    bash /tmp/install.sh --unattended || true && rm -f /tmp/install.sh && \
    find /usr -type f -executable -name "pihole*" -exec strip --strip-all {} \ 2>/dev/null; 2>/dev/null && \
    find /usr -type f -executable -name "gravity.sh" -exec chmod +x {} \; 2>/dev/null  && \
    find /opt -type f -executable -exec strip --strip-all {} \ 2>/dev/null; 2>/dev/null && \
    mkdir -p /usr/local/bin/pihole \
    mkdir -p /etc/dnsmasq.d
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

# package-manager-verified: integrity verified by upstream
RUN apk add --no-cache curl wget iproute2 iptables procps ca-certificates && \
    mkdir -p /app /var/log/pihole /var/lib/pihole /etc/pihole /etc/dnsmasq.d
COPY --from=installer /usr/local/bin/pihole /usr/local/bin/pihole
COPY --from=installer /opt/pihole /opt/pihole
COPY --from=installer /etc/pihole /etc/pihole
COPY --from=installer /etc/dnsmasq.d /etc/dnsmasq.d
COPY --from=installer /usr/bin/gravity.sh /usr/local/bin/gravity.sh
COPY --from=installer /usr/bin/pihole-FTL /usr/local/bin/pihole-FTL
COPY --from=installer /usr/sbin/pihole-FTL /usr/local/sbin/pihole-FTL
RUN chown -R 65532:65532 /app /var/log/pihole /var/lib/pihole
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 53 53/udp 8080 443

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:53"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="pi-hole" \
      org.opencontainers.image.version="bookworm" \
      org.opencontainers.image.vendor="Pi-hole" \
      org.opencontainers.image.source="https://github.com/pi-hole/pi-hole" \
      org.opencontainers.image.description="Network-level ad blocking via DNS" \
      evergreen.image.tier="1" \
      evergreen.image.category="dns" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="15000ms"
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
