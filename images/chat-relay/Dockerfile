ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.0.0

FROM docker.io/matrixdotorg/complement@sha256:779cdbc9c92ae386ee19cb3c55eb3ae96b12be205117fe30caffbd4cf5b2a20f AS upstream

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

RUN apk add --no-cache ca-certificates && \
    adduser -D -u 65532 complement 2>/dev/null || true && \
    mkdir -p /app /var/log/complement 2>/dev/null || true

COPY --from=upstream /complement /usr/local/bin/complement
RUN mkdir -p /etc/ssl/certs || true && COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 9004

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:9004"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="chat-relay" \
      org.opencontainers.image.description="Matrix chat relay (complement) - testing tool for Matrix homeservers" \
      org.opencontainers.image.version="0.5.0" \
      org.opencontainers.image.vendor="matrix-org" \
      org.opencontainers.image.source="https://github.com/matrix-org/complement" \
      evergreen.image.tier="2" \
      evergreen.image.category="chat" \
      evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="tcp"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
