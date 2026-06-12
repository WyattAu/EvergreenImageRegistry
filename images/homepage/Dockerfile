ARG VERSION=v1.13.1
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

# NOTE: Upstream image digest not pinned - update @sha256:... when stable digest is available
ARG SHIM_VERSION=v1.0.0

FROM ghcr.io/gethomepage/homepage:v1.5 AS upstream

FROM cgr.dev/chainguard/wolfi-base
RUN apk add --no-cache nodejs npm ca-certificates

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base
COPY --from=shim /shim /shim
RUN apk add --no-cache nodejs npm ca-certificates

COPY --from=upstream /app /app
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

WORKDIR /app

EXPOSE 3000
EXPOSE 9101

LABEL org.opencontainers.image.title="homepage" org.opencontainers.image.description="Homepage - Application dashboard" org.opencontainers.image.vendor="benphelps" org.opencontainers.image.source="https://github.com/benphelps/homepage" evergreen.image.tier="3" evergreen.constraint.nonroot="true" evergreen.constraint.scratch="true" \
      org.opencontainers.image.version="v1.13.1"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"

LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:3000"]

ENTRYPOINT ["/shim", "run", "-c", "node /app/server.js"]
