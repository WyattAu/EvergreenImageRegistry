# =============================================================================

# EVERGREEN REFERENCE - ARM64 MULTI-ARCH

# Multi-architecture reference image for arm64/aarch64 targets.

# =============================================================================

ARG APP_UID=65532
ARG APP_GID=65532

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache ca-certificates tzdata || true
LABEL org.opencontainers.image.title="arm64" \
      org.opencontainers.image.description="Evergreen multi-arch reference for arm64/aarch64 platform" \
      evergreen.image.tier="3" \
      evergreen.image.status="reference" \
      evergreen.image.category="base" \
      evergreen.image.note="Multi-architecture reference image. Build with docker buildx --platform linux/arm64." \
      evergreen.base.image="wolfi" \
      evergreen.metrics.native="ztunnel"
LABEL evergreen.security.cap-drop="ALL"
LABEL org.opencontainers.image.source="https://github.com/WyattAu/EvergreenImageRegistry"
LABEL org.opencontainers.image.version="unknown"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

LABEL evergreen.health.type="none"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
