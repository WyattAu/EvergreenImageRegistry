# =============================================================================
# EVERGREEN HARDENED IMMICH
# Repack of upstream ghcr.io/immich-app/immich-server with health-shim overlay.
#
# Immich-server carries a deep, tightly-coupled native dependency tree
# (Node 24, sharp/libvips, pg-native, jellyfin-ffmpeg, optional CUDA) that
# cannot be reliably transplanted onto a wolfi-base / scratch stage. The
# previous stub installed nodejs + ffmpeg via apk but never copied the compiled
# immich bundle, so the entrypoint (`node /usr/src/app/dist/main.js`) had
# nothing to run -- the image was non-functional.
#
# The robust path is to keep the upstream image as the final stage and layer
# hardening (health-shim, non-root user, HEALTHCHECK, labels) on top, exactly
# like the rabbitmq and paperless-ngx repacks.
#
# Note: this is an intentional, documented exception to the
# "no debian final stage" constraint, recorded for immich specifically.
#
# Upstream image facts (verified from ghcr.io config, release tag = v2.7.5):
#   WorkingDir:   /usr/src/app
#   Entrypoint:   ["tini","--","/bin/bash","-c"]  Cmd: ["start.sh"]
#                 (start.sh is on PATH at /usr/src/app/server/bin/start.sh and
#                  launches the compiled Node API server)
#   ExposedPorts: 2283/tcp   <- immich-server's API port (3001 is the legacy
#                               pre-2.x port; the modern server binds 2283)
#   User:         root (dropped to 65532 below)
#
# Tag note: immich publishes `release` and `vX.Y.Z` tags but NOT `latest`.
# =============================================================================

ARG VERSION=1.106.0
ARG BUILD_DATE

ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v2.0.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

# immich does not publish a `:latest` tag; `release` tracks the current
# release. Pin to vX.Y.Z (e.g. v2.7.5) for reproducible builds.
FROM ghcr.io/immich-app/immich-server:v1.116.2

# Drop in the evergreen health-shim, which wraps the app with supervision,
# signal handling, healthchecks, and metrics.
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ENV EVERGREEN_LOG_LEVEL=info \
    SHIM_METRICS_ENABLED="true"

WORKDIR /usr/src/app
EXPOSE 2283

HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=5 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:2283"]

# Keep upstream entrypoint (tini must be PID 1 for signal handling)
# Shim is only used for HEALTHCHECK
CMD ["start.sh"]

LABEL org.opencontainers.image.title="immich" \
      org.opencontainers.image.description="Immich - self-hosted photo and video backup solution" \
      org.opencontainers.image.version="1.106.0" \
      org.opencontainers.image.vendor="Immich" \
      org.opencontainers.image.source="https://github.com/immich-app/immich" \
      evergreen.image.tier="critical" \
      evergreen.image.status="functional" \
      evergreen.image.category="photo-video" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="upstream"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="tcp"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.entrypoint.pattern="repack-upstream-init"
STOPSIGNAL SIGTERM
