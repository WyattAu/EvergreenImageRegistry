# =============================================================================
# EVERGREEN HARDENED QBITTORRENT
# Generated from template - Version: 4.6.5
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.6.5
ARG TARGETARCH
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache ca-certificates && \
    adduser -u 65532 -D qbittorrent 2>/dev/null || true && \
    mkdir -p /app /var/log/qbittorrent-nox /var/cache/qbittorrent-nox && chown -R qbittorrent:qbittorrent /app /var/log/qbittorrent-nox /var/cache/qbittorrent-nox 2>/dev/null || true
USER qbittorrent
WORKDIR /app
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:8080/ || exit 1
ENTRYPOINT ["qbittorrent-nox"]
LABEL org.opencontainers.image.title="qbittorrent" \
      org.opencontainers.image.description="qbittorrent container image" \
      org.opencontainers.image.version="4.6.5" \
      org.opencontainers.image.vendor="QBitTorrent" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/qbittorrent/qBittorrent"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
