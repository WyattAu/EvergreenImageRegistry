# =============================================================================
# EVERGREEN HARDENED REDIS7
# Generated from template - Version: 7.4.1
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=7.4.1
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache ca-certificates && adduser -u 65532 -D 2>/dev/null &&  mkdir -p /app /var/log/redis7 /var/cache/redis7 && chown -R redis:redis /app /var/log/redis7 /var/cache/redis7 2>/dev/null
# NOTE: redis server not available in wolfi; uses pre-compiled binary
USER redis:redis
WORKDIR /app
EXPOSE 6379

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD redis-cli ping
ENTRYPOINT ["redis"]
LABEL org.opencontainers.image.title="redis7" \
      org.opencontainers.image.description="redis7 container image" \
      org.opencontainers.image.version="7.4.1" \
      org.opencontainers.image.vendor="Redis" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/redis/redis"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
