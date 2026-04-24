# =============================================================================
# SOVEREIGN REFERENCE - ALPINE (wrapper)
# Alpine is BANNED for application images in this registry.
# This image exists only as a base image reference wrapper around wolfi.
# For application images, use debian-slim, distroless, or scratch instead.
# =============================================================================


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates tzdata
LABEL org.opencontainers.image.title="alpine" \
      org.opencontainers.image.description="Sovereign reference wrapper for Alpine-compatible base (wolfi). Alpine is banned for application images." \
      sovereign.image.tier="3" \
      sovereign.image.status="reference" \
      sovereign.image.category="base" \
      sovereign.image.note="Alpine is banned for application images. This is a wolfi wrapper for build-time reference only."

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
