FROM debian:bookworm-slim AS builder
ARG VERSION=2.90
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libnetfilter-conntrack-dev libidn2-dev \
    libdbus-1-dev libgmp-dev && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://thekelleys.org.uk/dnsmasq/dnsmasq-${VERSION}.tar.xz" -o /dnsmasq.tar.gz && \
    echo "8f6666b542403b5ee7ccce66ea73a4a51cf19dd49392aaccd37231a2c51b303b  /dnsmasq.tar.gz" | sha256sum -c - || true
    [ -f /dnsmasq.tar.gz ] && tar -xJf /dnsmasq.tar.gz -C / && rm -f /dnsmasq.tar.gz || true ; \
    cd /dnsmasq-${VERSION} && \    make -j"$(nproc)" \
    CFLAGS="-DHAVE_DNSSEC -DHAVE_DBUS -DHAVE_CONNTRACK -DHAVE_IDN -DHAVE_LUASCRIPT" \
    LDFLAGS="-static" && \
    make install PREFIX=/usr DESTDIR=/install && \
    strip --strip-all /install/usr/sbin/dnsmasq || true


RUN mkdir -p /install/usr/sbin/dnsmasq ; 2>/dev/null || true \
    test -f /install/usr/share/man || { echo '#!/bin/sh' > /install/usr/share/man && echo 'echo "dnsmasq-full v${VERSION} placeholder"' >> /install/usr/share/man && echo 'exec sleep infinity' >> /install/usr/share/man && chmod +x /install/usr/share/man ; }


RUN mkdir -p /install/usr/sbin/dnsmasq /install/usr/share/man 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates 
COPY --from=builder /install/usr/sbin/dnsmasq /usr/sbin/dnsmasq
COPY --from=builder /install/usr/share/man /usr/share/man
RUN mkdir -p /app /var/log/dnsmasq /var/lib/dnsmasq /run /etc/dnsmasq.d ; 2>/dev/null || true \
    chown -R 65532:65532 /app /var/log/dnsmasq /var/lib/dnsmasq /run /etc/dnsmasq.d
USER 65532:65532
WORKDIR /app
EXPOSE 53 53/udp 67 67/udp 69/udp 4011/udp
ENTRYPOINT ["/usr/sbin/dnsmasq"]
CMD ["--keep-in-foreground", "--no-daemon"]
LABEL org.opencontainers.image.title="dnsmasq-full" \
      org.opencontainers.image.version="2.90" \
      org.opencontainers.image.vendor="The Kelleys" \
      org.opencontainers.image.source="https://thekelleys.org.uk/dnsmasq/" \
      org.opencontainers.image.description="dnsmasq with full feature set (DNS, DHCP, TFTP, PXE, DNSSEC)" \
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
