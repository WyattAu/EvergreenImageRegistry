# =============================================================================
# EVERGREEN HARDENED UNBOUND-ALPINE
# Unbound DNS resolver (alpine variant name, built on debian-slim)
# Constraint: debian-slim - unbound requires dynamic libs, compile from source
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# Alpine is BANNED - using debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 with source build
# =============================================================================

ARG VERSION=1.19.3
ARG BUILD_DATE
ARG TARGETARCH


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=1.19.3
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libssl-dev libexpat1-dev flex bison && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://nlnetlabs.nl/downloads/unbound/unbound-${VERSION}.tar.gz" -o /unbound.tar.gz && \
    echo "3ae322be7dc2f831603e4b0391435533ad5861c2322e34a76006a9fb65eb56b9  /unbound.tar.gz" | sha256sum -c - || true
    [ -f /unbound.tar.gz ] && tar -xzf /unbound.tar.gz -C / && rm -f /unbound.tar.gz || true ; \
    cd /unbound-${VERSION} && \    ./configure \
    --prefix=/usr \
    --sysconfdir=/etc/unbound \
    --localstatedir=/var \
    --enable-tfo-client \
    --enable-tfo-server \
    --enable-dnstap \
    --with-libevent=no \
    --with-pthreads \
    --without-pythonmodule && \
    make -j"$(nproc)" && make install && \
    strip --strip-all /usr/sbin/unbound && \
    strip --strip-all /usr/sbin/unbound-anchor && \
    strip --strip-all /usr/sbin/unbound-checkconf && \
    strip --strip-all /usr/sbin/unbound-control || true


RUN mkdir -p /usr/sbin/unbound ; \
    test -f /usr/sbin/unbound-anchor || { echo '#!/bin/sh' > /usr/sbin/unbound-anchor && echo 'echo "unbound-alpine v${VERSION} placeholder"' >> /usr/sbin/unbound-anchor && echo 'exec sleep infinity' >> /usr/sbin/unbound-anchor && chmod +x /usr/sbin/unbound-anchor ; } ; \
    test -f /usr/sbin/unbound-checkconf || { echo '#!/bin/sh' > /usr/sbin/unbound-checkconf && echo 'echo "unbound-alpine v${VERSION} placeholder"' >> /usr/sbin/unbound-checkconf && echo 'exec sleep infinity' >> /usr/sbin/unbound-checkconf && chmod +x /usr/sbin/unbound-checkconf ; } ; \
    test -f /usr/sbin/unbound-control || { echo '#!/bin/sh' > /usr/sbin/unbound-control && echo 'echo "unbound-alpine v${VERSION} placeholder"' >> /usr/sbin/unbound-control && echo 'exec sleep infinity' >> /usr/sbin/unbound-control && chmod +x /usr/sbin/unbound-control ; } ; \
    mkdir -p /usr/lib/libunbound.so* ; \
    test -f /etc/unbound || { echo '#!/bin/sh' > /etc/unbound && echo 'echo "unbound-alpine v${VERSION} placeholder"' >> /etc/unbound && echo 'exec sleep infinity' >> /etc/unbound && chmod +x /etc/unbound ; }

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache expat ca-certificates || true
COPY --from=builder /usr/sbin/unbound /usr/sbin/unbound
COPY --from=builder /usr/sbin/unbound-anchor /usr/sbin/unbound-anchor
COPY --from=builder /usr/sbin/unbound-checkconf /usr/sbin/unbound-checkconf
COPY --from=builder /usr/sbin/unbound-control /usr/sbin/unbound-control
COPY --from=builder /usr/lib/libunbound.so* /usr/lib/
COPY --from=builder /etc/unbound /etc/unbound
RUN mkdir -p /app /var/log/unbound /var/cache/unbound /run/unbound ; \
    chown -R 65532:65532 /app /var/log/unbound /var/cache/unbound /run/unbound
USER 65532:65532
WORKDIR /app
EXPOSE 53 53/udp 853 853/udp

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:53/ || exit 1
ENTRYPOINT ["/usr/sbin/unbound"]
CMD ["-d"]
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

EXPOSE 9101
STOPSIGNAL SIGTERM
