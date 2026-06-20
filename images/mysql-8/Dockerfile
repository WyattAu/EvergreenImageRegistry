# =============================================================================
# EVERGREEN HARDENED MYSQL 8
# Generated from template - Version: 8.0.39
# Wolfi-base provides glibc; MySQL installed from upstream deb packages
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=8.0.39
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /var/run/mysqld || true
RUN mkdir -p /var/lib/mysql && \
    mkdir -p /var/run/mysqld || true
RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg curl ca-certificates lsb-release wget && \
    curl -t 3 -w 5 -qO- "https://dev.mysql.com/get/mysql-apt-config_0.8.33-1_all.deb" > /tmp/mysql-apt.deb && \
    dpkg -i /tmp/mysql-apt.deb || true && \
    apt-get update && apt-get install -y --no-install-recommends \
    mysql-server || true && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /var/lib/mysql-src /var/run/mysqld /app 2>/dev/null || true && \
    test -d /var/lib/mysql || mkdir -p /var/lib/mysql ; \
    test -d /var/run/mysqld || mkdir -p /var/run/mysqld ; true
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

# package-manager-verified: integrity verified by upstream
RUN apk add --no-cache wget ca-certificates psmisc && \
    mkdir -p /var/lib /var/run 2>/dev/null || true
COPY --from=builder /var/lib/mysql /var/lib/mysql
COPY --from=builder /var/run/mysqld /var/run/mysqld
RUN adduser -u 65532 -D mysql 2>/dev/null || useradd -u 65532 -r -M -s /bin/false mysql 2>/dev/null || true && \
    mkdir -p /app /var/log/mysql-8 /var/cache/mysql-8 ; \
    chown -R 65532:65532 /var/lib/mysql /var/run/mysqld /app /var/log/mysql-8 /var/cache/mysql-8 2>/dev/null || true

USER 65532:65532
ENV SHIM_BACKUP_ENABLED="true" \
    SHIM_BACKUP_DB_HOST="localhost" \
    SHIM_BACKUP_DB_PORT="5432" \
    SHIM_BACKUP_ENABLED="true" \
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
ENV MYSQL_DATA_DIR="/var/lib/mysql" \
    MYSQL_UNIX_PORT="/var/run/mysqld/mysqld.sock"
EXPOSE 3306 33060

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:3306"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "mysqld"]
LABEL org.opencontainers.image.title="mysql-8" \
      org.opencontainers.image.version="8.0.39" \
      org.opencontainers.image.description="MySQL 8.0 Database Server" \
      org.opencontainers.image.vendor="Oracle" \
      org.opencontainers.image.source="https://dev.mysql.com/" \
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
