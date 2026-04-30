ARG VERSION=5.9.16
ARG BUILD_DATE

FROM debian:bookworm-slim AS installer
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
        strongswan strongswan-pki libcharon-extra-plugins \
        libcharon-extauth-plugins libstrongswan-extra-plugins \
        charon-systemd && \
    rm -rf /var/lib/apt/lists/* || true
RUN mkdir -p /app-src /var/log/strongswan /var/run/charon \
        /etc/strongswan.d /etc/ipsec.d 2>/dev/null || true
RUN strip --strip-all /usr/sbin/charon 2>/dev/null || true && \
    strip --strip-all /usr/sbin/charon-systemd 2>/dev/null || true && \
    strip --strip-all /usr/sbin/strongswan 2>/dev/null || true && \
    strip --strip-all /usr/sbin/pki 2>/dev/null || true && \
    strip --strip-all /usr/sbin/swanctl 2>/dev/null || true && \
    strip --strip-all /usr/sbin/ipsec 2>/dev/null || true && \
    find /usr/lib -type f -name "lib*.so*" -exec strip --strip-unneeded {} \; 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION
RUN apk add --no-cache ca-certificates iproute2 iptables kmod \
        libcurl openssl-libs talloc \
        gmp libcrypto1.1 zlib || true
RUN mkdir -p /etc /usr/lib /usr/sbin /var/log /run/charon \
        /etc/strongswan.d /etc/ipsec.d /app 2>/dev/null || true
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
COPY --from=installer /etc/ipsec.d /etc/ipsec.d
COPY --from=installer /app /app
COPY --from=installer /var/log/strongswan /var/log/strongswan
RUN mkdir -p /run/charon /etc/strongswan.d 2>/dev/null || true && \
    chown -R 65532:65532 /app /var/log/strongswan /run/charon 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 500 500/udp 4500 4500/udp
ENTRYPOINT ["/usr/sbin/charon"]
LABEL org.opencontainers.image.title="strongswan" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="strongSwan Project" \
      org.opencontainers.image.source="https://github.com/strongswan/strongswan" \
      org.opencontainers.image.description="IPsec-based VPN (IKEv1/IKEv2) with PKI and plugins" \
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
