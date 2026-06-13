ARG VERSION=5.0.8
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v1.1.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION
RUN mkdir -p /opt/apache-cassandra-${VERSION} || true
RUN mkdir -p /opt/apache-cassandra-${VERSION} || true
RUN mkdir -p /opt/apache-cassandra-${VERSION}
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://dlcdn.apache.org/cassandra/${VERSION}/apache-cassandra-${VERSION}-bin.tar.gz" -o /cassandra.tar.gz ; \
    echo "1579d7d3f2d812741a28cd2c2cbe29e83541bb4d25fb21ec2c00c1e4fb3b9a8f  /cassandra.tar.gz" | sha256sum -c && \
    tar -xzf /cassandra.tar.gz -C /opt ; rm -f /cassandra.tar.gz ; \
    test -s /opt/apache-cassandra-${VERSION} || { echo '#!/bin/sh' > /opt/apache-cassandra-${VERSION} && echo 'echo "cassandra v${VERSION} binary not available - download failed" >&2 \
    exit 1"' >> /opt/apache-cassandra-${VERSION}  && chmod +x /opt/apache-cassandra-${VERSION}; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=5.0.8
RUN mkdir -p /opt/cassandra || true
COPY --from=downloader /opt/apache-cassandra-${VERSION} /opt/cassandra
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-17-jre-headless && \
    rm -rf /var/lib/apt/lists/* || true && \
    mkdir -p /var/lib/cassandra /var/log/cassandra /app 2>/dev/null || true ; \
    chown -R 65532:65532 /var/lib/cassandra /var/log/cassandra /app /opt/cassandra 2>/dev/null || true

# hadolint ignore=DL3023

FROM ghcr.io/wyattau/evergreenshim/db-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ENV HEALTH_CMD="nodetool status" \
    READY_CMD="nodetool netstats" \
    STARTUP_CMD="nodetool status" \
    EVERGREEN_LOG_LEVEL=info

RUN mkdir -p /usr/lib/jvm || true
COPY --from=builder /usr/lib/jvm /usr/lib/jvm
RUN mkdir -p /opt/cassandra || true
COPY --from=builder /opt/cassandra /opt/cassandra
RUN mkdir -p /app || true
COPY --from=builder /app /app
RUN mkdir -p /var/lib/cassandra || true
COPY --from=builder /var/lib/cassandra /var/lib/cassandra
RUN mkdir -p /var/log/cassandra || true
COPY --from=builder /var/log/cassandra /var/log/cassandra
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk
ENV CASSANDRA_HOME=/opt/cassandra
ENV PATH="${CASSANDRA_HOME}/bin:${JAVA_HOME}/bin:${PATH}"

USER 65532:65532
ENV SHIM_BACKUP_ENABLED="true" \
    SHIM_BACKUP_DB_HOST="localhost" \
    SHIM_BACKUP_DB_PORT="9042" \
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
EXPOSE 9042

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:9042"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "nodetool", "--", "/opt/cassandra/bin/cassandra", "-f"]
LABEL org.opencontainers.image.title="cassandra" \
      org.opencontainers.image.description="Apache Cassandra - distributed NoSQL database" \
      org.opencontainers.image.version="5.0" \
      org.opencontainers.image.vendor="Apache" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      evergreen.hft.cpu-pins="4-5" \
      evergreen.hft.cpu-pins-mode="exclusive" \
      evergreen.hft.deploy-strategy="hft-stateful" \
      evergreen.hft.pre-stop-hook="true" \
      evergreen.hft.pre-stop-delay="5s" \
      evergreen.hft.connection-drain="true" \
      evergreen.hft.sched-policy="SCHED_OTHER" \
            org.opencontainers.image.source="https://github.com/apache/cassandra"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="true"
LABEL evergreen.health.type="http"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
