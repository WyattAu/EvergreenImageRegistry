# =============================================================================
# EVERGREEN HARDENED RSS2EMAIL
# Generated from template - Version: 3.15.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.15.1
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache ca-certificates curl && \
    pip install --no-cache-dir --break-system-packages rss2email==3.15.1 2>/dev/null || \
    pip install --no-cache-dir rss2email==3.15.1 && \
    adduser -u 65532 -D app 2>/dev/null || true && \
    mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:8080/ || exit 1
ENTRYPOINT ["r2e"]
LABEL org.opencontainers.image.title="rss2email" \
      org.opencontainers.image.description="rss2email container image" \
      org.opencontainers.image.version="3.15.1" \
      org.opencontainers.image.vendor="RSS2Email" \
      org.opencontainers.image.source="https://github.com/rss2email/rss2email" \
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
