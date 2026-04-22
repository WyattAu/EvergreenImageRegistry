# =============================================================================
# SOVEREIGN HARDENED PI-HOLE
# Network-level ad blocking via DNS
# Constraint: debian-slim - Pi-hole install script requires bash, curl, etc.
# =============================================================================

ARG BUILD_DATE

FROM debian:bookworm-slim AS installer
ENV PIHOLE_INSTALL=noninteractive
ENV FTLCONF_webserver_port=8080
ENV DNSMASQ_USER=pihole
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl wget sudo git iproute2 iptables procps ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://install.pi-hole.net | bash -s -- --unattended
RUN find /usr -type f -executable -name "pihole*" -exec strip --strip-all {} \; 2>/dev/null || true && \
    find /usr -type f -executable -name "gravity.sh" -exec chmod +x {} \; 2>/dev/null || true && \
    find /opt -type f -executable -exec strip --strip-all {} \; 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache curl wget iproute2 iptables procps ca-certificates
RUN mkdir -p /app /var/log/pihole /var/lib/pihole /etc/pihole /etc/dnsmasq.d
COPY --from=installer /usr/local/bin/pihole /usr/local/bin/pihole
COPY --from=installer /opt/pihole /opt/pihole
COPY --from=installer /etc/pihole /etc/pihole 2>/dev/null || true
COPY --from=installer /etc/dnsmasq.d /etc/dnsmasq.d 2>/dev/null || true
COPY --from=installer /usr/bin/gravity.sh /usr/local/bin/gravity.sh 2>/dev/null || true
COPY --from=installer /usr/bin/pihole-FTL /usr/local/bin/pihole-FTL 2>/dev/null || true
COPY --from=installer /usr/sbin/pihole-FTL /usr/local/sbin/pihole-FTL 2>/dev/null || true
RUN chown -R 65532:65532 /app /var/log/pihole /var/lib/pihole
USER 65532:65532
WORKDIR /app
EXPOSE 53 53/udp 8080 443
ENTRYPOINT ["/usr/local/bin/pihole"]
LABEL org.opencontainers.image.title="pi-hole" \
      org.opencontainers.image.version="bookworm" \
      org.opencontainers.image.vendor="Pi-hole" \
      org.opencontainers.image.source="https://github.com/pi-hole/pi-hole" \
      org.opencontainers.image.description="Network-level ad blocking via DNS" \
      sovereign.image.tier="1" \
      sovereign.image.category="dns" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="15000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM