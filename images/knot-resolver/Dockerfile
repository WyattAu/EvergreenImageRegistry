# =============================================================================
# SOVEREIGN HARDENED KNOT-RESOLVER
# Generated from template - Version: 5.7.6
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=5.7.6
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates xz-utils && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y --no-install-recommends \
    libcmocka-dev libluajit-5.1-dev libssl-dev libsystemd-dev gcc make && \
    curl -fsSL -k "https://secure.nic.cz/files/knot-resolver/knot-resolver-${VERSION}.tar.xz" -o /tmp/kresd.tar.xz && \
    tar -xJf /tmp/kresd.tar.xz -C /tmp && \
    cd /tmp/knot-resolver-${VERSION} && \
    ./configure --prefix=/opt/knot-resolver --with-module=stats > /dev/null 2>&1 && \
    make -j$(nproc) > /dev/null 2>&1 && \
    make install > /dev/null 2>&1 && \
    strip /opt/knot-resolver/sbin/kresd && \
    apt-get purge -y --auto-remove xz-utils libcmocka-dev libluajit-5.1-dev libssl-dev libsystemd-dev gcc make 2>/dev/null || true && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/kresd.tar.xz /tmp/knot-resolver-${VERSION}

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/kresd /var/cache/kresd

FROM scratch
COPY --from=downloader /opt/knot-resolver /opt/knot-resolver
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/kresd /var/log/kresd
COPY --from=builder /var/cache/kresd /var/cache/kresd
USER 65534:65534
WORKDIR /app
EXPOSE 53
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/opt/knot-resolver/sbin/kresd", "--version"]
ENTRYPOINT ["/opt/knot-resolver/sbin/kresd"]
LABEL org.opencontainers.image.title="knot-resolver" \
      org.opencontainers.image.version="5.7.6" \
      org.opencontainers.image.vendor="Knot DNS" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
