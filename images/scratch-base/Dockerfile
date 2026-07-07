# =============================================================================
# EVERGREEN SCRATCH-BASE
# Minimal FROM scratch base image with CA certs, timezone data, and standard
# directory layout. All source-build images use this as their final stage.
#
# Provides:
#   - /etc/ssl/certs/ca-certificates.crt (Mozilla CA bundle)
#   - /usr/share/zoneinfo/UTC (timezone)
#   - /app, /var/log/app, /var/cache/app directories
#   - User 65532:65532 (nonroot)
#
# Size: ~6MB (CA certs) + 3KB (tzdata UTC) = ~6MB total
# =============================================================================

ARG APP_UID=65532
ARG APP_GID=65532

FROM ghcr.io/wyattau/evergreenimageregistry/mirror-debian-f9c6a2fd2ddb:latest AS certs
RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates tzdata && \
    mkdir -p /app /var/log/app /var/cache/app && \
    chown -R 65532:65532 /app /var/log/app /var/cache/app && \
    rm -rf /var/lib/apt/lists/*

FROM scratch
COPY --from=certs /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=certs /usr/share/zoneinfo/UTC /usr/share/zoneinfo/UTC
COPY --from=certs /usr/share/zoneinfo/posix/UTC /usr/share/zoneinfo/posix/UTC
COPY --from=certs /usr/share/zoneinfo/right/UTC /usr/share/zoneinfo/right/UTC
COPY --from=certs /app /app
COPY --from=certs /var/log/app /var/log/app
COPY --from=certs /var/cache/app /var/cache/app

USER 65532:65532
WORKDIR /app

LABEL org.opencontainers.image.title="scratch-base" \
      org.opencontainers.image.description="Minimal FROM scratch base with CA certs, tzdata, and standard directories" \
      org.opencontainers.image.vendor="EvergreenImageRegistry" \
      evergreen.image.tier="0" \
      evergreen.image.role="base" \
      evergreen.constraint.nonroot="true"
LABEL evergreen.security.cap-drop="ALL"
LABEL org.opencontainers.image.source="https://github.com/WyattAu/EvergreenImageRegistry"
LABEL org.opencontainers.image.version="unknown"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

LABEL evergreen.constraint.scratch="true"
LABEL evergreen.entrypoint.pattern="base-image"
STOPSIGNAL SIGTERM

HEALTHCHECK NONE
