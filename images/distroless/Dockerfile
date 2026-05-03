# =============================================================================
# EVERGREEN REFERENCE - DISTROLESS
# Reference image pointing to gcr.io/distroless/static-debian12.
# Use as a base for Go/Rust static binaries that need no shell.
# =============================================================================


FROM gcr.io/distroless/static-debian12@sha256:20bc6c0bc4d625a22a8fde3e55f6515709b32055ef8fb9cfbddaa06d1760f838
LABEL org.opencontainers.image.title="distroless" \
      org.opencontainers.image.description="Evergreen reference to gcr.io/distroless/static-debian12 for static binary containers" \
      evergreen.image.tier="3" \
      evergreen.image.status="reference" \
      evergreen.image.category="base" \
      evergreen.image.note="Reference image. Use as FROM base for static Go/Rust binaries."

LABEL evergreen.base.image="distroless"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="none"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK NONE
