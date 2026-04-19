# =============================================================================
# SOVEREIGN HARDENED QBITTORRENT
# Generated from template - Version: 4.6.5
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.6.5
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends qbittorrent-nox ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' qbittorrent 2>/dev/null || true
RUN mkdir -p /app /var/log/qbittorrent-nox /var/cache/qbittorrent-nox && chown -R qbittorrent:qbittorrent /app /var/log/qbittorrent-nox /var/cache/qbittorrent-nox 2>/dev/null || true
USER qbittorrent
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD qbittorrent-nox curl -s localhost:8080/api/v2/app/version
ENTRYPOINT ["qbittorrent-nox"]
LABEL org.opencontainers.image.title="qbittorrent" \
      org.opencontainers.image.version="4.6.5" \
      org.opencontainers.image.vendor="QBitTorrent" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
