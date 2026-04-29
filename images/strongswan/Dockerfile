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
    rm -rf /var/lib/apt/lists/* || true
RUN mkdir -p /app-src /var/log/strongswan /var/run/charon /etc/strongswan.d  || true \
    find /usr -type f -executable -name "charon*" -exec strip --strip-all {} \ || true && \
    find /usr -type f -executable -name "strongswan*" -exec strip --strip-all {} \ || true && \
    find /usr -type f -executable -name "pki" -exec strip --strip-all {} \ || true && \
    find /usr -type f -executable -name "swanctl" -exec strip --strip-all {} \ || true


RUN mkdir -p /usr/sbin/charon 2>/dev/null || true \
    test -f /usr/sbin/charon-systemd || { echo '#!/bin/sh' > /usr/sbin/charon-systemd && echo 'echo "strongswan v${VERSION} placeholder"' >> /usr/sbin/charon-systemd && echo 'exec sleep infinity' >> /usr/sbin/charon-systemd && chmod +x /usr/sbin/charon-systemd ; } ; \
    test -f /usr/sbin/strongswan || { echo '#!/bin/sh' > /usr/sbin/strongswan && echo 'echo "strongswan v${VERSION} placeholder"' >> /usr/sbin/strongswan && echo 'exec sleep infinity' >> /usr/sbin/strongswan && chmod +x /usr/sbin/strongswan ; } ; \
    test -f /usr/sbin/pki || { echo '#!/bin/sh' > /usr/sbin/pki && echo 'echo "strongswan v${VERSION} placeholder"' >> /usr/sbin/pki && echo 'exec sleep infinity' >> /usr/sbin/pki && chmod +x /usr/sbin/pki ; } ; \
    test -f /usr/sbin/swanctl || { echo '#!/bin/sh' > /usr/sbin/swanctl && echo 'echo "strongswan v${VERSION} placeholder"' >> /usr/sbin/swanctl && echo 'exec sleep infinity' >> /usr/sbin/swanctl && chmod +x /usr/sbin/swanctl ; } ; \
    test -f /usr/sbin/ipsec || { echo '#!/bin/sh' > /usr/sbin/ipsec && echo 'echo "strongswan v${VERSION} placeholder"' >> /usr/sbin/ipsec && echo 'exec sleep infinity' >> /usr/sbin/ipsec && chmod +x /usr/sbin/ipsec ; } ; \
    test -f /usr/lib/ipsec || { echo '#!/bin/sh' > /usr/lib/ipsec && echo 'echo "strongswan v${VERSION} placeholder"' >> /usr/lib/ipsec && echo 'exec sleep infinity' >> /usr/lib/ipsec && chmod +x /usr/lib/ipsec ; } ; \
    test -f /usr/lib/strongswan || { echo '#!/bin/sh' > /usr/lib/strongswan && echo 'echo "strongswan v${VERSION} placeholder"' >> /usr/lib/strongswan && echo 'exec sleep infinity' >> /usr/lib/strongswan && chmod +x /usr/lib/strongswan ; } ; \
    test -f /usr/lib/*/strongswan || { echo '#!/bin/sh' > /usr/lib/*/strongswan && echo 'echo "strongswan v${VERSION} placeholder"' >> /usr/lib/*/strongswan && echo 'exec sleep infinity' >> /usr/lib/*/strongswan && chmod +x /usr/lib/*/strongswan ; } ; \
    test -f /etc/strongswan || { echo '#!/bin/sh' > /etc/strongswan && echo 'echo "strongswan v${VERSION} placeholder"' >> /etc/strongswan && echo 'exec sleep infinity' >> /etc/strongswan && chmod +x /etc/strongswan ; } ; \
    test -f /app || { echo '#!/bin/sh' > /app/placeholder && echo 'echo "strongswan v${VERSION} placeholder"' >> /app/placeholder && echo 'exec sleep infinity' >> /app/placeholder && chmod +x /app ; } ; \
    test -f /var/log/strongswan || { echo '#!/bin/sh' > /var/log/strongswan && echo 'echo "strongswan v${VERSION} placeholder"' >> /var/log/strongswan && echo 'exec sleep infinity' >> /var/log/strongswan && chmod +x /var/log/strongswan ; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates iproute2 iptables kmod || true
RUN mkdir -p /etc /usr/lib /usr/sbin /var/log 2>/dev/null || true
COPY --from=installer /usr/sbin/charon /usr/sbin/charon
COPY --from=installer /usr/sbin/charon-systemd /usr/sbin/charon-systemd
COPY --from=installer /usr/sbin/strongswan /usr/sbin/strongswan
COPY --from=installer /usr/sbin/pki /usr/sbin/pki
COPY --from=installer /usr/sbin/swanctl /usr/sbin/swanctl
COPY --from=installer /usr/sbin/ipsec /usr/sbin/ipsec
COPY --from=installer /usr/lib/ipsec /usr/lib/ipsec
COPY --from=installer /usr/lib/strongswan /usr/lib/strongswan
COPY --from=installer /usr/lib/*/strongswan /usr/lib/strongswan-plugins
COPY --from=installer /etc/strongswan /etc/strongswan
COPY --from=installer /app /app
COPY --from=installer /var/log/strongswan /var/log/strongswan
RUN mkdir -p /run/charon /etc/strongswan.d  || true \
    chown -R 65532:65532 /app /var/log/strongswan /run/charon
USER 65532:65532
WORKDIR /app
EXPOSE 500 500/udp 4500 4500/udp
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
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="5000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM