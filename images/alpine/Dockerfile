# =============================================================================
# EVERGREEN REFERENCE - ALPINE (wrapper)
# Alpine is BANNED for application images in this registry.
# This image exists only as a base image reference wrapper around wolfi.
# For application images, use debian-slim, distroless, or scratch instead.
# =============================================================================


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache ca-certificates tzdata 
LABEL org.opencontainers.image.title="alpine" \
      org.opencontainers.image.description="Evergreen reference wrapper for Alpine-compatible base (wolfi). Alpine is banned for application images." \
      evergreen.image.tier="3" \
      evergreen.image.status="reference" \
      evergreen.image.category="base" \
      evergreen.image.note="Alpine is banned for application images. This is a wolfi wrapper for build-time reference only."

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="none"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
