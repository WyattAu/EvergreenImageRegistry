# =============================================================================
# SOVEREIGN REFERENCE - DISTROLESS
# Reference image pointing to gcr.io/distroless/static-debian12.
# Use as a base for Go/Rust static binaries that need no shell.
# =============================================================================


FROM gcr.io/distroless/static-debian12:latest
LABEL org.opencontainers.image.title="distroless" \
      org.opencontainers.image.description="Sovereign reference to gcr.io/distroless/static-debian12 for static binary containers" \
      sovereign.image.tier="3" \
      sovereign.image.status="reference" \
      sovereign.image.category="base" \
      sovereign.image.note="Reference image. Use as FROM base for static Go/Rust binaries."

LABEL sovereign.base.image="distroless"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM
