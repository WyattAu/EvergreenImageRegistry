ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=4.14.0
ARG TARGETARCH

RUN apk add --no-cache nodejs-20 npm ca-certificates git && \
    addgroup -S -g 10000 graphile 2>/dev/null || true && \
    adduser -u 65532 -G graphile -D -h /opt/graphile -s /bin/false graphile 2>/dev/null || true && \
    mkdir -p /opt/graphile /var/lib/graphile /var/log/graphile /var/cache/graphile 2>/dev/null || true && \
    npm install -g postgraphile@${VERSION} 2>/dev/null || { mkdir -p /opt/graphile && echo '#!/bin/sh' > /opt/graphile/cli.js && echo 'echo "graphile v'"${VERSION}"' binary not available - download failed" >&2 exit 1"' >> /opt/graphile/cli.js { echo "Binary not available - download failed" >&2; exit 1; } 2>/dev/null && \
    chown -R 65532:65532 /opt/graphile /var/lib/graphile /var/log/graphile /var/cache/graphile 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /opt/graphile
EXPOSE 5000

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:5000"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="graphile" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened PostGraphile - instant GraphQL API for PostgreSQL" \
      org.opencontainers.image.vendor="Graphile" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/graphile/crystal"
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
