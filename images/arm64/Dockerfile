# =============================================================================

# EVERGREEN REFERENCE - ARM64 MULTI-ARCH

# Multi-architecture reference image for arm64/aarch64 targets.

# =============================================================================

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache ca-certificates tzdata || true
LABEL org.opencontainers.image.title="arm64" \
      org.opencontainers.image.description="Evergreen multi-arch reference for arm64/aarch64 platform" \
      evergreen.image.tier="3" \
      evergreen.image.status="reference" \
      evergreen.image.category="base" \
      evergreen.image.note="Multi-architecture reference image. Build with docker buildx --platform linux/arm64." \
      evergreen.base.image="wolfi" \
      evergreen.metrics.native="ztunnel" \
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

      evergreen.health.type="none"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
