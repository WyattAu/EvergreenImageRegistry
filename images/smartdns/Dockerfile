# =============================================================================
# SOVEREIGN HARDENED SMARTDNS
# Local DNS server with DoH/DoT support
# Constraint: compile from source in debian:bookworm-slim
# =============================================================================

ARG VERSION=Release48
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-base cmake libssl-dev && \
    rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/pymumu/smartdns/archive/refs/tags/${VERSION}.tar.gz" -o /smartdns.tar.gz && \
    tar -xzf /smartdns.tar.gz -C / && rm /smartdns.tar.gz && \
    mkdir -p /smartdns-${VERSION}/build && \
    cd /smartdns-${VERSION}/build && \
    cmake .. -DPREFIX=/usr -DENABLE_SYSTEMD=OFF && \
    make -j"$(nproc)" && \
    strip --strip-all /smartdns-${VERSION}/src/smartdns

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates
RUN mkdir -p /app /var/log/smartdns /var/lib/smartdns /etc/smartdns
COPY --from=builder /smartdns-${VERSION}/src/smartdns /usr/local/bin/smartdns
RUN chown -R 65532:65532 /app /var/log/smartdns /var/lib/smartdns
USER 65532:65532
WORKDIR /app
EXPOSE 53 53/udp 443 8053
ENTRYPOINT ["/usr/local/bin/smartdns"]
LABEL org.opencontainers.image.title="smartdns" \
      org.opencontainers.image.version="Release48" \
      org.opencontainers.image.vendor="pymumu" \
      org.opencontainers.image.source="https://github.com/pymumu/smartdns" \
      org.opencontainers.image.description="Local DNS server with DoH/DoT support" \
      sovereign.image.tier="1" \
      sovereign.image.category="dns" \
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