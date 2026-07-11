# =============================================================================
# EVERGREEN META - UPSTREAM
# This is a metadata directory for upstream references, not a container image.
# =============================================================================


ARG APP_UID=65532
ARG APP_GID=65532

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache ca-certificates
LABEL org.opencontainers.image.title="upstream" \
      org.opencontainers.image.description="Meta directory for upstream version tracking. Not a runnable container." \
      evergreen.image.tier="3" \
      evergreen.image.status="reference" \
      evergreen.image.category="meta" \
      evergreen.image.note="Upstream tracking directory, not a container image." \
            org.opencontainers.image.source="https://github.com/WyattAu/EvergreenImageRegistry" \
                  org.opencontainers.image.version="unknown"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="none"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
LABEL evergreen.entrypoint.pattern="base-image"
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
