ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS builder
ARG VERSION=2.5.0
ARG TARGETARCH
RUN mkdir -p /opt/mongosh || true
RUN apk add --no-cache wget ca-certificates && \
    wget -t 3 -T 10 -qO /tmp/mongosh.tgz \
    "https://fastdl.mongodb.org/tools/mongodb-mongosh/${VERSION}/mongosh-${VERSION}-linux-x64.tgz" && \
    mkdir -p /opt/mongosh && \
    tar -xzf /tmp/mongosh.tgz -C /opt/mongosh --strip-components=1 && \
    rm -f /tmp/mongosh.tgz || true
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=2.5.0
RUN apk add --no-cache ca-certificates && \
    addgroup -S -g 10000 mongosh 2>/dev/null || true && \
    adduser -u 65532 -G mongosh -D -h /app -s /bin/false mongosh 2>/dev/null || true && \
    mkdir -p /app /var/log/mongosh 2>/dev/null || true
COPY --from=builder /opt/mongosh /opt/mongosh
RUN chown -R 65532:65532 /app /var/log/mongosh 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
ENV PATH="/opt/mongosh/bin:${PATH}"
EXPOSE 27017

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:27017"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="mongodb-opsmanager" \
      org.opencontainers.image.description="MongoDB Ops Manager - mongosh CLI tool" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="MongoDB" \
      org.opencontainers.image.source="https://www.mongodb.com/docs/mongodb-shell/" \
      evergreen.image.tier="2" \
      evergreen.image.category="database" \
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
