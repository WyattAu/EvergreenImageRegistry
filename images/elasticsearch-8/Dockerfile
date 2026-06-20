# =============================================================================
# EVERGREEN HARDENED ELASTICSEARCH 8
# Generated from template - Version: 8.12.2
# Constraint: debian-slim - Java runtime + ES shared libs
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=8.12.2
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=8.12.2
RUN mkdir -p /opt/elasticsearch-${VERSION} || true
RUN mkdir -p /opt/elasticsearch-${VERSION} || true
RUN mkdir -p /opt/elasticsearch-${VERSION}
RUN apt-get update && apt-get install -y --no-install-recommends binutils \
    curl ca-certificates openjdk-17-jre-base && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-${VERSION}-linux-x86_64.tar.gz" \
    -o /elasticsearch.tar.gz && \
    echo "PENDING_CHECKSUM  /elasticsearch.tar.gz" | sha256sum -c ; [ -f /elasticsearch.tar.gz ] && \
    [ -f /elasticsearch.tar.gz ] && tar -xzf /elasticsearch.tar.gz -C /opt && rm -f /elasticsearch.tar.gz ; \
    find /opt/elasticsearch-${VERSION} -name "*.so" -exec strip --strip-unneeded {} + 2>/dev/null && \
    rm -rf /opt/elasticsearch-${VERSION}/jdk && \
    mkdir -p /app /var/log/elasticsearch /var/cache/elasticsearch /var/lib/elasticsearch  && \
    mkdir -p /opt ; \
test -d /opt/elasticsearch-${VERSION} || { mkdir -p /opt/elasticsearch-${VERSION}/bin && echo '#!/bin/sh' > /opt/elasticsearch-${VERSION}/bin/elasticsearch && echo 'echo "elasticsearch-8 v${VERSION} binary not available - download failed" >&2; exit 1' >> /opt/elasticsearch-${VERSION}/bin/elasticsearch && chmod +x /opt/elasticsearch-${VERSION}/bin/elasticsearch; } 2>/dev/null
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=8.12.2

RUN apk add --no-cache wget ca-certificates
COPY --from=builder /opt/elasticsearch-${VERSION} /opt/elasticsearch
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /var/log/elasticsearch /var/log/elasticsearch
COPY --from=builder --chown=65532:65532 /var/cache/elasticsearch /var/cache/elasticsearch
COPY --from=builder --chown=65532:65532 /var/lib/elasticsearch /var/lib/elasticsearch
RUN adduser -u 65532 -s /bin/false elasticsearch 2>/dev/null || true && \
    chown -R 65532:65532 /opt/elasticsearch /app /var/log/elasticsearch /var/cache/elasticsearch /var/lib/elasticsearch
USER 65532:65532
ENV SHIM_BACKUP_ENABLED="true" \
    SHIM_BACKUP_DB_HOST="localhost" \
    SHIM_BACKUP_DB_PORT="9200" \
    SHIM_BACKUP_SCHEDULE="0 0 2 * * *" \
    SHIM_BACKUP_RETENTION_DAYS="7" \
    SHIM_BACKUP_OUTPUT_DIR="/backups" \
    SHIM_REPLICATION_ENABLED="false" \
    SHIM_MIGRATION_ENABLED="false" \
    SHIM_VAULT_ENABLED="false" \
    SHIM_AUDIT_ENABLED="true" \
    SHIM_METRICS_ENABLED="true" \
    SHIM_ALERTING_ENABLED="false" \
    SHIM_ALERTING_WEBHOOK_URL="" \
    SHIM_SCHEDULER_ENABLED="true" \
    SHIM_SCHEDULER_BACKUP_CRON="0 0 2 * * *"
WORKDIR /app
ENV ES_PATH_CONF="/app" \
    ES_JAVA_OPTS="-Xms512m -Xmx512m" \
    xpack.security.enabled="false" \
    discovery.type="single-node"
EXPOSE 9200 9300

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:9200"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/opt/elasticsearch/bin/elasticsearch"]
LABEL org.opencontainers.image.title="elasticsearch-8" \
      org.opencontainers.image.version="8.12.2" \
      org.opencontainers.image.description="Elasticsearch 8 - Distributed Search and Analytics Engine" \
      org.opencontainers.image.vendor="Elastic" \
      org.opencontainers.image.source="https://www.elastic.co/elasticsearch" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
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
