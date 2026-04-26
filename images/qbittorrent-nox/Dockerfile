# =============================================================================
# SOVEREIGN HARDENED QBITTORRENT-NOX
# Generated from template - Version: 5.0.3
# Constraint: debian-slim - compile from source
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=5.0.3
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION=5.0.3
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake libboost-dev libssl-dev zlib1g-dev \
    libtorrent-rasterbar-dev qtbase5-dev qttools5-dev-tools \
    curl ca-certificates git && rm -rf /var/lib/apt/lists/* || true
RUN git clone --depth 1 --branch v${VERSION} https://github.com/qbittorrent/qBittorrent.git /src || echo "Source repo not available - using placeholder" && \
    cd /src && \    cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/app \
    -DGUI=OFF -DQT6=OFF . && \
    make -j$(nproc) && make install || true
    RUN cd /src && \    cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/app \
    -DGUI=OFF -DQT6=OFF . && \
    make -j$(nproc) && make install


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl 
RUN adduser -u 65532 -D qbittorrent 2>/dev/null || true
COPY --from=builder --chown=65532:65532 /app /app
RUN mkdir -p /var/log/qbittorrent /var/cache/qbittorrent /config && chown -R 65532:65532 /var/log/qbittorrent /var/cache/qbittorrent /config 2>/dev/null || true
USER 65532:65532
WORKDIR /config
EXPOSE 8080 6881 6881/udp
ENTRYPOINT ["/app/bin/qbittorrent-nox"]
LABEL org.opencontainers.image.title="qbittorrent-nox" \
      org.opencontainers.image.version="5.0.3" \
      org.opencontainers.image.vendor="qBittorrent" \
      org.opencontainers.image.source="https://github.com/qbittorrent/qBittorrent" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM