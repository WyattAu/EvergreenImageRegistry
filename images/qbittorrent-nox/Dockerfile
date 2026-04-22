# =============================================================================
# SOVEREIGN HARDENED QBITTORRENT-NOX
# Generated from template - Version: 5.0.3
# Constraint: debian-slim - compile from source
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=5.0.3
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake libboost-dev libssl-dev zlib1g-dev \
    libtorrent-rasterbar-dev qtbase5-dev qttools5-dev-tools \
    curl ca-certificates git && rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 --branch v${VERSION} https://github.com/qbittorrent/qBittorrent.git /src && \
    cd /src && \
    cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/app \
    -DGUI=OFF -DQT6=OFF . && \
    make -j$(nproc) && make install

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' qbittorrent 2>/dev/null || true
COPY --from=builder --chown=65534:65534 /app /app
RUN mkdir -p /var/log/qbittorrent /var/cache/qbittorrent /config && chown -R 65534:65534 /var/log/qbittorrent /var/cache/qbittorrent /config 2>/dev/null || true
USER 65534:65534
WORKDIR /config
EXPOSE 8080 6881 6881/udp
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:8080/api/v2/app/version || exit 1
ENTRYPOINT ["/app/bin/qbittorrent-nox"]
LABEL org.opencontainers.image.title="qbittorrent-nox" \
      org.opencontainers.image.version="5.0.3" \
      org.opencontainers.image.vendor="qBittorrent" \
      org.opencontainers.image.source="https://github.com/qbittorrent/qBittorrent" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
