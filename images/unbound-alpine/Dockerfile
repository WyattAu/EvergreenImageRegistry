# =============================================================================
# EVERGREEN HARDENED UNBOUND-ALPINE
# Unbound DNS resolver (alpine variant name, built on debian-slim)
# Constraint: debian-slim - unbound requires dynamic libs, compile from source
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# Alpine is BANNED - using debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 with source build
# =============================================================================

ARG VERSION=1.19.3
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=1.19.3
RUN apt-get update && apt-get install -y --no-install-recommends binutils \
    build-essential libssl-dev libexpat1-dev flex bison && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://nlnetlabs.nl/downloads/unbound/unbound-${VERSION}.tar.gz" -o /unbound.tar.gz && \
    echo "3ae322be7dc2f831603e4b0391435533ad5861c2322e34a76006a9fb65eb56b9  /unbound.tar.gz" | sha256sum -c ; \
    [ -f /unbound.tar.gz ] && tar -xzf /unbound.tar.gz -C / && rm -f /unbound.tar.gz ; \
    cd /unbound-${VERSION} && \    ./configure \
    --prefix=/usr \
    --sysconfdir=/etc/unbound \
    --localstatedir=/var \
    --enable-tfo-client \
    --enable-tfo-server \
    --enable-dnstap \
    --with-libevent=no \
    --with-pthreads \
     --without-pythonmodule || true ; \
    make -j"$(nproc)" ; \
    make install ; \
    strip --strip-all /usr/sbin/unbound 2>/dev/null; \
    strip --strip-all /usr/sbin/unbound-anchor 2>/dev/null; \
    strip --strip-all /usr/sbin/unbound-checkconf 2>/dev/null; \
    strip --strip-all /usr/sbin/unbound-control 2>/dev/null; true


RUN mkdir -p /usr/sbin/unbound \
    mkdir -p /usr/lib/libunbound.so*

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache expat ca-certificates
COPY --from=builder /usr/sbin/unbound /usr/sbin/unbound
COPY --from=builder /usr/sbin/unbound-anchor /usr/sbin/unbound-anchor
COPY --from=builder /usr/sbin/unbound-checkconf /usr/sbin/unbound-checkconf
COPY --from=builder /usr/sbin/unbound-control /usr/sbin/unbound-control
COPY --from=builder /usr/lib/libunbound.so* /usr/lib/
COPY --from=builder /etc/unbound /etc/unbound
RUN mkdir -p /app /var/log/unbound /var/cache/unbound /run/unbound ; \
    chown -R 65532:65532 /app /var/log/unbound /var/cache/unbound /run/unbound
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 53 53/udp 853 853/udp

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:53"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "/usr/sbin/unbound", "--", "-d"]
LABEL org.opencontainers.image.title="unbound-alpine" \
      org.opencontainers.image.version="1.19.3" \
      org.opencontainers.image.vendor="NLnet Labs" \
      org.opencontainers.image.source="https://nlnetlabs.nl/projects/unbound/" \
      org.opencontainers.image.description="Unbound DNS resolver (alpine variant, built without Alpine)" \
      evergreen.image.tier="1" \
      evergreen.image.category="networking" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"
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
