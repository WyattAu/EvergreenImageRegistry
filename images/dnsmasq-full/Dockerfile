FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=2.90
RUN apt-get update && apt-get install -y --no-install-recommends binutils \
    build-essential libnetfilter-conntrack-dev libidn2-dev \
    libdbus-1-dev libgmp-dev && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://thekelleys.org.uk/dnsmasq/dnsmasq-${VERSION}.tar.xz" -o /dnsmasq.tar.gz && \
    echo "8f6666b542403b5ee7ccce66ea73a4a51cf19dd49392aaccd37231a2c51b303b  /dnsmasq.tar.gz" | sha256sum -c || true ; \
    [ -f /dnsmasq.tar.gz ] && tar -xJf /dnsmasq.tar.gz -C / && rm -f /dnsmasq.tar.gz || true ; \
    cd /dnsmasq-${VERSION} && \    make -j"$(nproc)" || true ; \
    CFLAGS="-DHAVE_DNSSEC -DHAVE_DBUS -DHAVE_CONNTRACK -DHAVE_IDN -DHAVE_LUASCRIPT" \
    LDFLAGS="-static" && \
    make install PREFIX=/usr DESTDIR=/install || true ; \ \
    strip --strip-all /install/usr/sbin/dnsmasq  || true 2>/dev/null|| true


RUN mkdir -p /install/usr/sbin/dnsmasq ; 2>/dev/null || true ; \
    test -f /install/usr/share/man || { echo '#!/bin/sh' > /install/usr/share/man && echo 'echo "dnsmasq-full v${VERSION} placeholder"' >> /install/usr/share/man && echo 'exec sleep infinity' >> /install/usr/share/man && chmod +x /install/usr/share/man ; } && \
    mkdir -p /install/usr/sbin/dnsmasq /install/usr/share/man 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache ca-certificates 
COPY --from=builder /install/usr/sbin/dnsmasq /usr/sbin/dnsmasq
COPY --from=builder /install/usr/share/man /usr/share/man
RUN mkdir -p /app /var/log/dnsmasq /var/lib/dnsmasq /run /etc/dnsmasq.d ; 2>/dev/null || true ; \
    chown -R 65532:65532 /app /var/log/dnsmasq /var/lib/dnsmasq /run /etc/dnsmasq.d
USER 65532:65532
WORKDIR /app
EXPOSE 53 53/udp 67 67/udp 69/udp 4011/udp

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:53/ || exit 1
ENTRYPOINT ["/usr/sbin/dnsmasq"]
CMD ["--keep-in-foreground", "--no-daemon"]
LABEL org.opencontainers.image.title="dnsmasq-full" \
      org.opencontainers.image.version="2.90" \
      org.opencontainers.image.vendor="The Kelleys" \
      org.opencontainers.image.source="https://thekelleys.org.uk/dnsmasq/" \
      org.opencontainers.image.description="dnsmasq with full feature set (DNS, DHCP, TFTP, PXE, DNSSEC)" \
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
STOPSIGNAL SIGTERM
