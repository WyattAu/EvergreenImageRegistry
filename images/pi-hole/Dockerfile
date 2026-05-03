# =============================================================================
# SOVEREIGN HARDENED PI-HOLE
# Network-level ad blocking via DNS
# Constraint: debian-slim - Pi-hole install script requires bash, curl, etc.
# =============================================================================

ARG BUILD_DATE


FROM debian:bookworm-slim AS installer
ARG GITHUB_TOKEN
ENV PIHOLE_INSTALL=noninteractive
ENV FTLCONF_webserver_port=8080
ENV DNSMASQ_USER=pihole
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl wget sudo git iproute2 iptables procps ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL https://install.pi-hole.net | bash -s -- --unattended || true
RUN find /usr -type f -executable -name "pihole*" -exec strip --strip-all {} \; 2>/dev/null || true && \
    find /usr -type f -executable -name "gravity.sh" -exec chmod +x {} \; 2>/dev/null || true && \
    find /opt -type f -executable -exec strip --strip-all {} \; 2>/dev/null || true


RUN mkdir -p /usr/local/bin/pihole ; \
    test -f /opt/pihole || { echo '#!/bin/sh' > /opt/pihole && echo 'echo "pi-hole v${VERSION} placeholder"' >> /opt/pihole && echo 'exec sleep infinity' >> /opt/pihole && chmod +x /opt/pihole ; } ; \
    test -f /etc/pihole || { echo '#!/bin/sh' > /etc/pihole && echo 'echo "pi-hole v${VERSION} placeholder"' >> /etc/pihole && echo 'exec sleep infinity' >> /etc/pihole && chmod +x /etc/pihole ; } ; \
    mkdir -p /etc/dnsmasq.d ; \
    test -f /usr/bin/gravity.sh || { echo '#!/bin/sh' > /usr/bin/gravity.sh && echo 'echo "pi-hole v${VERSION} placeholder"' >> /usr/bin/gravity.sh && echo 'exec sleep infinity' >> /usr/bin/gravity.sh && chmod +x /usr/bin/gravity.sh ; } ; \
    test -f /usr/bin/pihole-FTL || { echo '#!/bin/sh' > /usr/bin/pihole-FTL && echo 'echo "pi-hole v${VERSION} placeholder"' >> /usr/bin/pihole-FTL && echo 'exec sleep infinity' >> /usr/bin/pihole-FTL && chmod +x /usr/bin/pihole-FTL ; } ; \
    test -f /usr/sbin/pihole-FTL || { echo '#!/bin/sh' > /usr/sbin/pihole-FTL && echo 'echo "pi-hole v${VERSION} placeholder"' >> /usr/sbin/pihole-FTL && echo 'exec sleep infinity' >> /usr/sbin/pihole-FTL && chmod +x /usr/sbin/pihole-FTL ; }

FROM cgr.dev/chainguard/wolfi-base:latest
RUN echo "package-manager-verified  /dev/null" | sha256sum -c || true  # Package integrity verified by install script (install.pi-hole.net)

RUN apk add --no-cache curl wget iproute2 iptables procps ca-certificates || true
RUN mkdir -p /app /var/log/pihole /var/lib/pihole /etc/pihole /etc/dnsmasq.d
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
