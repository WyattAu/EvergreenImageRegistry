# =============================================================================
# EVERGREEN HARDENED MYTHTV
# Generated from template - Version: 34.0
# Constraint: debian-slim - system packages required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=34.0
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache ca-certificates && \
    adduser -u 65532 -D mythtv 2>/dev/null || true && \
    mkdir -p /app /var/log/mythtv /var/cache/mythtv && chown -R mythtv:mythtv /app /var/log/mythtv /var/cache/mythtv 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 6543

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:6543/ || exit 1
ENTRYPOINT ["mythbackend"]
LABEL org.opencontainers.image.title="mythtv" \
      org.opencontainers.image.description="mythtv container image" \
      org.opencontainers.image.version="34.0" \
      org.opencontainers.image.vendor="MythTV" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/MythTV/mythtv"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
