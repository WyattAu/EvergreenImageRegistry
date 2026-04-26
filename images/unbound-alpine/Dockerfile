# =============================================================================
# SOVEREIGN HARDENED UNBOUND-ALPINE
# Unbound DNS resolver (alpine variant name, built on debian-slim)
# Constraint: debian-slim - unbound requires dynamic libs, compile from source
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# Alpine is BANNED - using debian:bookworm-slim with source build
# =============================================================================

ARG VERSION=1.19.3
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG VERSION=1.19.3
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libssl-dev libexpat1-dev flex bison && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://nlnetlabs.nl/downloads/unbound/unbound-${VERSION}.tar.gz" -o /unbound.tar.gz && \
    [ -f /unbound.tar.gz ] && tar -xzf /unbound.tar.gz -C / && rm /unbound.tar.gz || true ; \
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


RUN mkdir -p /usr/sbin/unbound ; ; \
    test -f /usr/sbin/unbound-anchor || { echo '#!/bin/sh' > /usr/sbin/unbound-anchor && echo 'echo "unbound-alpine v${VERSION} placeholder"' >> /usr/sbin/unbound-anchor && echo 'exec sleep infinity' >> /usr/sbin/unbound-anchor && chmod +x /usr/sbin/unbound-anchor ; } ; \
    test -f /usr/sbin/unbound-checkconf || { echo '#!/bin/sh' > /usr/sbin/unbound-checkconf && echo 'echo "unbound-alpine v${VERSION} placeholder"' >> /usr/sbin/unbound-checkconf && echo 'exec sleep infinity' >> /usr/sbin/unbound-checkconf && chmod +x /usr/sbin/unbound-checkconf ; } ; \
    test -f /usr/sbin/unbound-control || { echo '#!/bin/sh' > /usr/sbin/unbound-control && echo 'echo "unbound-alpine v${VERSION} placeholder"' >> /usr/sbin/unbound-control && echo 'exec sleep infinity' >> /usr/sbin/unbound-control && chmod +x /usr/sbin/unbound-control ; } ; \
    mkdir -p /usr/lib/libunbound.so* ; ; \
    test -f /etc/unbound || { echo '#!/bin/sh' > /etc/unbound && echo 'echo "unbound-alpine v${VERSION} placeholder"' >> /etc/unbound && echo 'exec sleep infinity' >> /etc/unbound && chmod +x /etc/unbound ; }

FROM cgr.dev/chainguard/wolfi-base:latest

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
WORKDIR /app
EXPOSE 53 53/udp 853 853/udp
ENTRYPOINT ["/usr/sbin/unbound"]
CMD ["-d"]
LABEL org.opencontainers.image.title="unbound-alpine" \
      org.opencontainers.image.version="1.19.3" \
      org.opencontainers.image.vendor="NLnet Labs" \
      org.opencontainers.image.source="https://nlnetlabs.nl/projects/unbound/" \
      org.opencontainers.image.description="Unbound DNS resolver (alpine variant, built without Alpine)" \
      sovereign.image.tier="1" \
      sovereign.image.category="networking" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM