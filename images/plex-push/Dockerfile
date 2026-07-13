# =============================================================================
# EVERGREEN HARDENED PLEX-PUSH
# Generated from template - Version: 0.1.0
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.1.0
ARG TARGETARCH
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=ghcr.io/wyattau/evergreenshim/health-shim:v2.0.0 /shim /usr/local/bin/shim
RUN apk add --no-cache ca-certificates curl && \
    adduser -u 65532 -D app 2>/dev/null || true && \
    mkdir -p /app /var/log/app /var/cache/app && chown -R app:app /app /var/log/app /var/cache/app 2>/dev/null || true
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:9101"]
ENTRYPOINT ["true"]
LABEL org.opencontainers.image.title="plex-push" \
      org.opencontainers.image.version="0.1.0" \
      org.opencontainers.image.vendor="Plex" \
      org.opencontainers.image.description="Placeholder - no upstream binary available" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/plexinc/push"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL evergreen.entrypoint.pattern="no-op"
STOPSIGNAL SIGTERM
