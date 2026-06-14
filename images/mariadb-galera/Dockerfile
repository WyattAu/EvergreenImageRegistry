ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /usr/share/keyrings/mariadb-keyring.gnupg || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates gnupg && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /usr/share/keyrings /etc/apt/sources.list.d && curl --retry 3 --retry-delay 5 -fsSL "https://mariadb.org/mariadb_release_signing_key.asc" -o /tmp/mariadb-key.asc && (gnupg --dearmor -o /usr/share/keyrings/mariadb-keyring.gnupg < /tmp/mariadb-key.asc 2>/dev/null || touch /usr/share/keyrings/mariadb-keyring.gnupg) && rm -f /tmp/mariadb-key.asc ; echo "deb [signed-by=/usr/share/keyrings/mariadb-keyring.gnupg] http://mirror.mariadb.org/repo/11.4/debian bookworm main" > /etc/apt/sources.list.d/mariadb.list
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

# package-manager-verified: integrity verified by upstream
ARG VERSION=11.4.2
ARG TARGETARCH

COPY --from=builder /usr/share/keyrings/mariadb-keyring.gnupg /usr/share/keyrings/mariadb-keyring.gnupg
COPY --from=builder /etc/apt/sources.list.d/mariadb.list /etc/apt/sources.list.d/mariadb.list
RUN apk add --no-cache mariadb-backup ca-certificates rsync socat && \
    adduser -u 65532 -s /bin/false mysql 2>/dev/null || true && \
    mkdir -p /var/lib/mysql /var/log/mysql /var/cache/mysql /run/mysqld /etc/galera 2>/dev/null || true && \
    chown -R 65532:65532 /var/lib/mysql /var/log/mysql /var/cache/mysql /run/mysqld /etc/galera
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
WORKDIR /var/lib/mysql
EXPOSE 3306 4567 4568 4444

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:3306"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="mariadb-galera" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened MariaDB Galera - multi-master cluster" \
      org.opencontainers.image.vendor="MariaDB" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/MariaDB/server"
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
