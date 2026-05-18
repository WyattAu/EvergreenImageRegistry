# =============================================================================
# EVERGREEN HARDENED IMMICH
# Generated from template - Version: 1.106.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.106.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache nodejs-20 ffmpeg ca-certificates || true && \
    adduser -u 65532 -D immich 2>/dev/null || true && \
    mkdir -p /app /var/log/node /var/cache/node && chown -R immich:immich /app /var/log/node /var/cache/node 2>/dev/null || true
USER immich
WORKDIR /app
EXPOSE 2283

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:2283/ || exit 1
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="immich" \
      org.opencontainers.image.description="Immich - self-hosted photo and video backup solution" \
      org.opencontainers.image.version="1.106.0" \
      org.opencontainers.image.vendor="Immich" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/immich-app/immich"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
