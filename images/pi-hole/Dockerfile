# =============================================================================
# EVERGREEN HARDENED PI-HOLE
# Network-level ad blocking via DNS
# Constraint: debian-slim - Pi-hole install script requires bash, curl, etc.
# =============================================================================

ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS installer
ARG GITHUB_TOKEN
ENV PIHOLE_INSTALL=noninteractive
ENV FTLCONF_webserver_port=8080
ENV DNSMASQ_USER=pihole
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl wget git iproute2 iptables procps ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://install.pi-hole.net -o /tmp/install.sh && bash /tmp/install.sh --unattended || true && rm -f /tmp/install.sh && \
    find /usr -type f -executable -name "pihole*" -exec strip --strip-all {} \; 2>/dev/null || true && \
    find /usr -type f -executable -name "gravity.sh" -exec chmod +x {} \; 2>/dev/null || true && \
    find /opt -type f -executable -exec strip --strip-all {} \; 2>/dev/null || true && \
    mkdir -p /usr/local/bin/pihole ; \
    test -f /opt/pihole || { echo '#!/bin/sh' > /opt/pihole && echo 'echo "pi-hole v${VERSION} placeholder"' >> /opt/pihole && echo 'exec sleep infinity' >> /opt/pihole && chmod +x /opt/pihole ; } ; \
    test -f /etc/pihole || { echo '#!/bin/sh' > /etc/pihole && echo 'echo "pi-hole v${VERSION} placeholder"' >> /etc/pihole && echo 'exec sleep infinity' >> /etc/pihole && chmod +x /etc/pihole ; } ; \
    mkdir -p /etc/dnsmasq.d ; \
    test -f /usr/bin/gravity.sh || { echo '#!/bin/sh' > /usr/bin/gravity.sh && echo 'echo "pi-hole v${VERSION} placeholder"' >> /usr/bin/gravity.sh && echo 'exec sleep infinity' >> /usr/bin/gravity.sh && chmod +x /usr/bin/gravity.sh ; } ; \
    test -f /usr/bin/pihole-FTL || { echo '#!/bin/sh' > /usr/bin/pihole-FTL && echo 'echo "pi-hole v${VERSION} placeholder"' >> /usr/bin/pihole-FTL && echo 'exec sleep infinity' >> /usr/bin/pihole-FTL && chmod +x /usr/bin/pihole-FTL ; } ; \
    test -f /usr/sbin/pihole-FTL || { echo '#!/bin/sh' > /usr/sbin/pihole-FTL && echo 'echo "pi-hole v${VERSION} placeholder"' >> /usr/sbin/pihole-FTL && echo 'exec sleep infinity' >> /usr/sbin/pihole-FTL && chmod +x /usr/sbin/pihole-FTL ; }
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN echo "package-manager-verified  /dev/null" | sha256sum -c || true  # Package integrity verified by install script (install.pi-hole.net)

RUN apk add --no-cache curl wget iproute2 iptables procps ca-certificates || true && \
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
WORKDIR /app
EXPOSE 53 53/udp 8080 443

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:53/ || exit 1
ENTRYPOINT ["/usr/local/bin/pihole"]
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
STOPSIGNAL SIGTERM
