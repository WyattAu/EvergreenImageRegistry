ARG VERSION=5.9.16
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS installer
ARG VERSION=5.9.16
RUN apt-get update && apt-get install -y --no-install-recommends binutils \
        strongswan strongswan-pki libcharon-extra-plugins \
        libcharon-extauth-plugins libstrongswan-extra-plugins \
        charon-systemd && \
    rm -rf /var/lib/apt/lists/* || true && \
    mkdir -p /app-src /var/log/strongswan /var/run/charon \
        /etc/strongswan.d /etc/ipsec.d 2>/dev/null || true && \
    strip --strip-all /usr/sbin/charon 2>/dev/null 2>/dev/null && \
    strip --strip-all /usr/sbin/charon-systemd 2>/dev/null 2>/dev/null && \
    strip --strip-all /usr/sbin/strongswan 2>/dev/null 2>/dev/null && \
    strip --strip-all /usr/sbin/pki 2>/dev/null 2>/dev/null && \
    strip --strip-all /usr/sbin/swanctl 2>/dev/null 2>/dev/null && \
    strip --strip-all /usr/sbin/ipsec 2>/dev/null 2>/dev/null && \
    find /usr/lib -type f -name "lib*.so*" -exec strip --strip-unneeded {} \; 2>/dev/null
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=5.9.16
RUN apk add --no-cache ca-certificates iproute2 iptables kmod libcurl talloc gmp openssl-libs zlib 2>/dev/null && mkdir -p /etc /usr/lib /usr/sbin /var/log /run/charon /etc/strongswan.d /etc/ipsec.d /app 2>/dev/null

COPY --from=installer /usr/sbin/charon /usr/sbin/charon

COPY --from=installer /usr/sbin/charon-systemd /usr/sbin/charon-systemd

COPY --from=installer /usr/sbin/strongswan /usr/sbin/strongswan

COPY --from=installer /usr/sbin/pki /usr/sbin/pki

COPY --from=installer /usr/sbin/swanctl /usr/sbin/swanctl

COPY --from=installer /usr/sbin/ipsec /usr/sbin/ipsec
RUN mkdir -p /usr/lib/ipsec
COPY --from=installer /usr/lib/ipsec /usr/lib/ipsec
RUN mkdir -p /usr/lib/strongswan || true
COPY --from=installer /usr/lib/strongswan /usr/lib/strongswan
RUN mkdir -p /usr/lib/strongswan-plugins || true
COPY --from=installer /usr/lib/*/strongswan /usr/lib/strongswan-plugins
RUN mkdir -p /etc/strongswan || true
COPY --from=installer /etc/strongswan /etc/strongswan

COPY --from=installer /etc/ipsec.d /etc/ipsec.d
RUN mkdir -p /app || true
COPY --from=installer /app /app
RUN mkdir -p /var/log/strongswan || true
COPY --from=installer /var/log/strongswan /var/log/strongswan
RUN mkdir -p /run/charon /etc/strongswan.d 2>/dev/null || true && \
    chown -R 65532:65532 /app /var/log/strongswan /run/charon 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 500 500/udp 4500 4500/udp

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:500"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="strongswan" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="strongSwan Project" \
      org.opencontainers.image.source="https://github.com/strongswan/strongswan" \
      org.opencontainers.image.description="IPsec-based VPN (IKEv1/IKEv2) with PKI and plugins" \
      evergreen.image.tier="1" \
      evergreen.image.category="security" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="5000ms"
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
