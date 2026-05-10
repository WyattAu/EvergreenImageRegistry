# =============================================================================
# EVERGREEN HARDENED OUTLINE
# Generated from template - Version: 0.77.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=0.77.0
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache nodejs-20 npm postgresql-client ca-certificates || true && \
    adduser -u 65532 -D outline 2>/dev/null || true && \
    mkdir -p /app /var/log/node /var/cache/node && chown -R outline:outline /app /var/log/node /var/cache/node 2>/dev/null || true
USER outline
WORKDIR /app
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:3000/ || exit 1
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="outline" \
      org.opencontainers.image.description="outline container image" \
      org.opencontainers.image.version="0.77.0" \
      org.opencontainers.image.vendor="Outline" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/outline/outline"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
