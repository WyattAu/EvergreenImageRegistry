# =============================================================================
# EVERGREEN REFERENCE - ALPINE-STATIC (wrapper)
# Static variant base image reference.
# Alpine is BANNED for application images in this registry.
# This image exists only as a build-time reference for static musl-based builds.
# =============================================================================


FROM cgr.dev/chainguard/static@sha256:77d8b8925dc27970ec2f48243f44c7a260d52c49cd778288e4ee97566e0cb75b
USER 65532:65532
LABEL org.opencontainers.image.title="alpine-static" \
      org.opencontainers.image.description="Evergreen reference for static base (chainguard/static). Alpine is banned for application images." \
      evergreen.image.tier="3" \
      evergreen.image.status="reference" \
      evergreen.image.category="base" \
      evergreen.image.note="Alpine is banned for application images. Use chainguard/static for static builds." \
            org.opencontainers.image.source="https://github.com/alpinelinux/docker-alpine" \
                  org.opencontainers.image.version="unknown"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="none"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK NONE
