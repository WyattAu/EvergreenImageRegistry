# =============================================================================
# SOVEREIGN REFERENCE - ALPINE-STATIC (wrapper)
# Static variant base image reference.
# Alpine is BANNED for application images in this registry.
# This image exists only as a build-time reference for static musl-based builds.
# =============================================================================


FROM cgr.dev/chainguard/static:latest
USER 65532:65532
LABEL org.opencontainers.image.title="alpine-static" \
      org.opencontainers.image.description="Sovereign reference for static base (chainguard/static). Alpine is banned for application images." \
      sovereign.image.tier="3" \
      sovereign.image.status="reference" \
      sovereign.image.category="base" \
      sovereign.image.note="Alpine is banned for application images. Use chainguard/static for static builds."

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM
