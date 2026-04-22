# =============================================================================
# SOVEREIGN HARDENED QBITTORRENT
# Generated from template - Version: 4.6.5
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.6.5
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates
RUN useradd -m -u 65532 -g '' qbittorrent 2>/dev/null || true
RUN mkdir -p /app /var/log/qbittorrent-nox /var/cache/qbittorrent-nox && chown -R qbittorrent:qbittorrent /app /var/log/qbittorrent-nox /var/cache/qbittorrent-nox 2>/dev/null || true
USER qbittorrent
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["qbittorrent-nox"]
LABEL org.opencontainers.image.title="qbittorrent" \
      org.opencontainers.image.version="4.6.5" \
      org.opencontainers.image.vendor="QBitTorrent" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM