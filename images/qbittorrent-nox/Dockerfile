# =============================================================================
# EVERGREEN HARDENED QBITTORRENT-NOX
# Generated from template - Version: 5.0.3
# Constraint: debian-slim - compile from source
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=5.0.3
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=5.0.3
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake libboost-dev libssl-dev zlib1g-dev \
    libtorrent-rasterbar-dev qtbase5-dev qttools5-dev-tools \
    curl ca-certificates git && rm -rf /var/lib/apt/lists/* && \
    git clone --branch v${VERSION} https://github.com/qbittorrent/qBittorrent.git /src || echo "Source repo not available - using && { echo "Binary not available - download failed" >&2; exit 1; }
    exit 1" && \
    cd /src &&  cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/app \
    -DGUI=OFF -DQT6=OFF . && \
    make -j$(nproc) && make install && \
    cd /src &&  cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/app \
    -DGUI=OFF -DQT6=OFF . && \
    make -j$(nproc) && make install && \
    mkdir -p / 2>/dev/null || true ; touch --chown=65532:65532 2>/dev/null || true
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache ca-certificates curl && \
    adduser -u 65532 -D qbittorrent 2>/dev/null || true
RUN mkdir -p /app || true
COPY --from=builder --chown=65532:65532 /app /app
RUN mkdir -p /var/log/qbittorrent /var/cache/qbittorrent /config && chown -R 65532:65532 /var/log/qbittorrent /var/cache/qbittorrent /config 2>/dev/null || true
USER 65532:65532
WORKDIR /config
EXPOSE 8080 6881 6881/udp

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:6881"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="qbittorrent-nox" \
      org.opencontainers.image.description="qbittorrent-nox container image" \
      org.opencontainers.image.version="5.0.3" \
      org.opencontainers.image.vendor="qBittorrent" \
      org.opencontainers.image.source="https://github.com/qbittorrent/qBittorrent" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
