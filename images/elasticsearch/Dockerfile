# =============================================================================
# EVERGREEN HARDENED ELASTICSEARCH
# Generated from template - Version: 8.14.0
# Constraint: wolfi-base — Java JRE runtime required
# =============================================================================

ARG VERSION=8.14.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS downloader
ARG VERSION=8.14.0
ARG TARGETARCH
RUN apk add --no-cache curl ca-certificates && \
    case "${TARGETARCH}" in \
      amd64)  ES_ARCH="linux-x86_64" ;; \
      arm64)  ES_ARCH="linux-aarch64" ;; \
      *)      echo "Unsupported arch: ${TARGETARCH}" && exit 1 ;; \
    esac && \
    curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-${VERSION}-${ES_ARCH}.tar.gz" -o /tmp/es.tar.gz && \
    tar xzf /tmp/es.tar.gz -C /opt && rm -f /tmp/es.tar.gz && \
    cd /opt && rm -f elasticsearch && \
    cp -rL elasticsearch-${VERSION} elasticsearch && \
    ln -s /opt/elasticsearch/bin/elasticsearch /usr/local/bin/elasticsearch || true

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
COPY shim.toml /etc/evergreen/shim.toml
RUN chmod +x /usr/local/bin/shim

ARG VERSION=8.14.0
RUN apk add --no-cache curl ca-certificates gosu && \
    addgroup -S -g 2 elasticsearch 2>/dev/null || true && \
    adduser -u 65532 -G elasticsearch -D -h /app -s /bin/false elasticsearch 2>/dev/null || true && \
    mkdir -p /app /var/log/elasticsearch /var/cache/elasticsearch && \
    chown -R 65532:2 /app /var/log/elasticsearch /var/cache/elasticsearch 2>/dev/null || true
COPY --from=downloader /opt/elasticsearch /opt/elasticsearch
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532
WORKDIR /app
ENV SHIM_METRICS_ENABLED="true" \
    SHIM_HEALTHCHECK_TYPE="http" \
    SHIM_HEALTHCHECK_URL="http://localhost:9200/_cluster/health"
EXPOSE 9200 9300

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--http", "http://127.0.0.1:9200/_cluster/health"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "gosu elasticsearch /opt/elasticsearch/bin/elasticsearch"]
LABEL org.opencontainers.image.title="elasticsearch" \
      org.opencontainers.image.description="Elasticsearch - distributed search and analytics engine" \
      org.opencontainers.image.version="8.14.0" \
      org.opencontainers.image.vendor="Elastic" \
      org.opencontainers.image.platforms="linux/amd64,linux/arm64" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
      org.opencontainers.image.source="https://github.com/elastic/elasticsearch"
LABEL evergreen.metrics.native="true"
LABEL evergreen.health.type="http"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"

EXPOSE 9101
STOPSIGNAL SIGTERM
