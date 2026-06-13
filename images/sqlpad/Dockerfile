ARG VERSION=7.5.1
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.1.0

FROM sqlpad/sqlpad:${VERSION} AS upstream

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache wget ca-certificates bash
RUN mkdir -p /app /var/lib/sqlpad || true
COPY --from=upstream /docker-entrypoint /docker-entrypoint
COPY --from=upstream /usr/app /app
RUN adduser -u 65532 -s /bin/false sqlpad 2>/dev/null || true && \
    chown -R 65532:65532 /app


WORKDIR /app

EXPOSE 3000
EXPOSE 9101

LABEL org.opencontainers.image.title="sqlpad" org.opencontainers.image.version="7.5.1" org.opencontainers.image.description="SQLPad - Web-based SQL Editor with Query Visualization" org.opencontainers.image.vendor="SQLPad" org.opencontainers.image.source="https://github.com/sqlpad/sqlpad" evergreen.image.tier="1" evergreen.constraint.nonroot="true" evergreen.base.image="wolfi"
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
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:3000"]

ENTRYPOINT ["/shim", "run", "-c", "node /app/server.js"]
