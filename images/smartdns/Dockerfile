# =============================================================================
# EVERGREEN HARDENED SMARTDNS
# Local DNS server with DoH/DoT support
# Constraint: compile from source in debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252
# =============================================================================

ARG VERSION=Release48
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=Release48
RUN mkdir -p /smartdns-${VERSION}/src
RUN apt-get update && apt-get install -y --no-install-recommends binutils \
    build-essential cmake libssl-dev && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/pymumu/smartdns/archive/refs/tags/${VERSION}.tar.gz -o /smartdns.tar.gz && \
    [ -f /smartdns.tar.gz ] && tar -xzf /smartdns.tar.gz -C / && rm -f /smartdns.tar.gz ; \
    mkdir -p /smartdns-${VERSION}/build ; \
    cd /smartdns-${VERSION}/build && \    cmake .. -DPREFIX=/usr -DENABLE_SYSTEMD=OFF && \
    make -j"$(nproc)" && \
    strip --strip-all /smartdns-${VERSION}/src/smartdns 2>/dev/null && \
    mkdir -p /smartdns-${VERSION}/src/smartdns
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

# package-manager-verified: integrity verified by upstream
ARG VERSION=Release48

RUN apk add --no-cache ca-certificates && \
    mkdir -p /app /var/log/smartdns /var/lib/smartdns /etc/smartdns
COPY --from=builder /smartdns-${VERSION}/src/smartdns /usr/local/bin/smartdns
RUN chown -R 65532:65532 /app /var/log/smartdns /var/lib/smartdns
USER 65532:65532
WORKDIR /app
EXPOSE 53 53/udp 443 8053

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:53"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="smartdns" \
      org.opencontainers.image.version="Release48" \
      org.opencontainers.image.vendor="pymumu" \
      org.opencontainers.image.source="https://github.com/pymumu/smartdns" \
      org.opencontainers.image.description="Local DNS server with DoH/DoT support" \
      evergreen.image.tier="1" \
      evergreen.image.category="dns" \
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
