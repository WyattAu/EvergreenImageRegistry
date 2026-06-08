ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.0.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=5.17.0
ARG TARGETARCH
RUN mkdir -p /opt/neo4j-community-5.17.0 || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://dist.neo4j.org/neo4j-community-5.17.0-unix.tar.gz" -o /neo4j.tar.gz && \
    echo "975b79448e4a7e0cd3f729c343149b52d20474fb3505509d638dfde861c9c440  /neo4j.tar.gz" | sha256sum -c ; \
    tar -xzf /neo4j.tar.gz -C /opt && rm -f /neo4j.tar.gz
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder

COPY --from=downloader /opt/neo4j-community-5.17.0 /opt/neo4j
RUN mkdir -p /var/lib/neo4j /var/log/neo4j /app ; \
    chown -R 65532:65532 /var/lib/neo4j /var/log/neo4j /app /opt/neo4j

# hadolint ignore=DL3023

FROM ghcr.io/wyattau/evergreenshim/db-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN mkdir -p /opt 2>/dev/null || true
RUN mkdir -p /opt/neo4j || true
COPY --from=builder /opt/neo4j /opt/neo4j
RUN mkdir -p  2>/dev/null || true ; test -s /app 2>/dev/null || echo "#!/bin/sh" > /app 2>/dev/null || true
COPY --from=builder /app /app
RUN mkdir -p /var/lib 2>/dev/null || true ; test -s /var/lib/neo4j 2>/dev/null || echo "#!/bin/sh" > /var/lib/neo4j 2>/dev/null || true
COPY --from=builder /var/lib/neo4j /var/lib/neo4j
RUN mkdir -p /var/log 2>/dev/null || true ; test -s /var/log/neo4j 2>/dev/null || echo "#!/bin/sh" > /var/log/neo4j 2>/dev/null || true
COPY --from=builder /var/log/neo4j /var/log/neo4j
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk
ENV NEO4J_HOME=/opt/neo4j
ENV PATH="${NEO4J_HOME}/bin:${JAVA_HOME}/bin:${PATH}"

USER 65532:65532
ENV SHIM_BACKUP_ENABLED="true" \
    SHIM_BACKUP_DB_HOST="localhost" \
    SHIM_BACKUP_DB_PORT="7474" \
    SHIM_BACKUP_SCHEDULE="0 2 * * *" \
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
    SHIM_SCHEDULER_BACKUP_CRON="0 2 * * *" \
    SHIM_MANAGEMENT_ENABLED="true" \
    SHIM_MANAGEMENT_HOST="0.0.0.0" \
    SHIM_MANAGEMENT_PORT="9102"
WORKDIR /app
EXPOSE 7474

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:7474"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="neo4j-admin" \
      org.opencontainers.image.description="neo4j-admin container image" \
      org.opencontainers.image.version="5.17.0" \
      org.opencontainers.image.vendor="Neo4j" \
      evergreen.image.tier="1" \
      evergreen.image.category="database-admin" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/neo4j/neo4j"
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
