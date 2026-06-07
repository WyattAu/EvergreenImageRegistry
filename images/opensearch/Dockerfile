# =============================================================================
# EVERGREEN HARDENED OPENSEARCH
# Version: 2.12.0
# Constraint: wolfi-base — Java JRE runtime required
# =============================================================================

ARG VERSION=2.12.0
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.0.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=2.12.0
ARG TARGETARCH
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    case "${TARGETARCH}" in \
      amd64)  OS_ARCH="linux-x64" ;; \
      arm64)  OS_ARCH="linux-arm64" ;; \
      *)      echo "Unsupported arch: ${TARGETARCH}" && exit 1 ;; \
    esac && \
    curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.opensearch.org/releases/bundle/opensearch/${VERSION}/opensearch-${VERSION}-${OS_ARCH}.tar.gz" -o /opensearch.tar.gz && \
    tar -xzf /opensearch.tar.gz -C /opt && rm -f /opensearch.tar.gz

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

RUN addgroup -S -g 65532 opensearch 2>/dev/null || true && \
    adduser -u 65532 -G opensearch -D -s /bin/false opensearch || true && \
    apk add --no-cache curl ca-certificates gosu && \
    mkdir -p /etc/ssl/certs /opt 2>/dev/null || true
COPY --from=downloader /opt/opensearch-${VERSION} /opt/opensearch
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN mkdir -p /app/data /app/logs /app/conf ; \
    chown -R opensearch:opensearch /app /opt/opensearch && \
    ln -sf /app/conf /opt/opensearch/config/custom
USER 65532:65532
WORKDIR /app
ENV OPENSEARCH_HOME=/opt/opensearch \
    OPENSEARCH_PATH_CONF=/app/conf \
    OPENSEARCH_JAVA_HOME=/usr/lib/jvm/java-17-openjdk \
    OPENSEARCH_STARTUP_SLEEP_TIME=5 \
    cluster.name=opensearch-cluster \
    network.host=0.0.0.0 \
    discovery.type=single-node \
    bootstrap.memory_lock=true \
    OPENSEARCH_INITIAL_ADMIN_PASSWORD=${OPENSEARCH_INITIAL_ADMIN_PASSWORD:-changeme} \
    SHIM_METRICS_ENABLED="true" \
    SHIM_HEALTHCHECK_TYPE="http" \
    SHIM_HEALTHCHECK_URL="http://localhost:9200/_cluster/health"
EXPOSE 9200 9300

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--http", "http://127.0.0.1:9200/_cluster/health"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "gosu opensearch /opt/opensearch/bin/opensearch"]
LABEL org.opencontainers.image.title="opensearch" \
      org.opencontainers.image.version="2.12.0" \
      org.opencontainers.image.vendor="OpenSearch" \
      org.opencontainers.image.platforms="linux/amd64,linux/arm64" \
      org.opencontainers.image.description="OpenSearch - distributed search and analytics engine" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="30s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="60000ms" \
      evergreen.hft.runtime="java" \
      org.opencontainers.image.source="https://github.com/opensearch-project/opensearch"
LABEL evergreen.base.image="wolfi"
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
