ARG VERSION=7.3.3
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM ghcr.io/matrix-org/matrix-hookshot:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS builder
RUN apk add --no-cache nodejs npm
COPY --from=upstream /app /app
RUN cd /app && npm install --omit=dev && \
    mkdir -p /var/log/matrix-hookshot /etc/matrix-hookshot

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

RUN apk add --no-cache nodejs ca-certificates
COPY --from=builder /app /app
COPY --from=builder /var/log/matrix-hookshot /var/log/matrix-hookshot
COPY --from=builder /etc/matrix-hookshot /etc/matrix-hookshot
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 9993

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:9993"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "node", "--", "."]

LABEL org.opencontainers.image.title="matrix-hookshot" \
      org.opencontainers.image.description="Matrix Hookshot - multi-purpose Matrix bot bridge framework" \
      org.opencontainers.image.version="7.3.3" \
      org.opencontainers.image.vendor="matrix.org" \
      org.opencontainers.image.source="https://github.com/matrix-org/matrix-hookshot" \
      evergreen.image.tier="2" \
      evergreen.image.category="messaging" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="10s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="30000ms"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
