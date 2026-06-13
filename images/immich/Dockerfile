# =============================================================================
# EVERGREEN HARDENED IMMICH
# Generated from template - Version: 1.106.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.106.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v1.1.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

RUN apk add --no-cache nodejs-20 ffmpeg ca-certificates && \
    adduser -u 65532 -D immich 2>/dev/null || true && \
    mkdir -p /app /var/log/node /var/cache/node && chown -R immich:immich /app /var/log/node /var/cache/node 2>/dev/null || true
USER immich
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 2283

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:2283"]

ENTRYPOINT ["/shim", "run", "-c", "node /usr/src/app/dist/main.js"]
LABEL org.opencontainers.image.title="immich" \
      org.opencontainers.image.description="Immich - self-hosted photo and video backup solution" \
      org.opencontainers.image.version="1.106.0" \
      org.opencontainers.image.vendor="Immich" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/immich-app/immich"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
