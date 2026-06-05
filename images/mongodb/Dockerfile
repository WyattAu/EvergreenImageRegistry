# =============================================================================
# EVERGREEN HARDENED MONGODB
# Uses official mongo image as upstream binary source on Wolfi base
# =============================================================================

ARG VERSION=7.0.11
ARG TARGETARCH

ARG SHIM_VERSION=v0.3.0

FROM mongo:${VERSION} AS upstream

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ENV HEALTH_CMD="echo 'db.adminCommand(\\\"ping\\\")' | mongosh --quiet" \
    READY_CMD="echo 'db.adminCommand(\\\"ping\\\")' | mongosh --quiet" \
    STARTUP_CMD="echo 'db.adminCommand(\\\"ping\\\")' | mongosh --quiet" \
    EVERGREEN_LOG_LEVEL=info

RUN apk add --no-cache ca-certificates

COPY --from=upstream /usr/bin/mongod /usr/bin/mongod
COPY --from=upstream /usr/bin/mongos /usr/bin/mongos
COPY --from=upstream /usr/bin/mongosh /usr/bin/mongosh

RUN adduser -D -u 65532 -s /bin/false mongodb 2>/dev/null || true && \
    mkdir -p /app /var/log/mongod /var/cache/mongod /data/db && \
    chown -R 65532:65532 /app /var/log/mongod /var/cache/mongod /data/db

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 27017

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:27017"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "mongod", "--", "--bind_ip", "0.0.0.0", "--dbpath", "/data/db"]
LABEL org.opencontainers.image.title="mongodb" \
      org.opencontainers.image.description="MongoDB - document-oriented NoSQL database" \
      org.opencontainers.image.version="7.0.11" \
      org.opencontainers.image.vendor="MongoDB" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.hardened="true" \
      org.opencontainers.image.source="https://github.com/mongodb/mongo"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="true"
LABEL evergreen.health.type="http"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
