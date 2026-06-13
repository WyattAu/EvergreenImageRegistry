# =============================================================================
# EVERGREEN HARDENED POSTGRESQL 17
# Generated from template - Version: 17.10
# Wolfi-base provides glibc; PostgreSQL installed from upstream deb packages
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=17.10
ARG BUILD_DATE

ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.1.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /var/run/postgresql || true
RUN mkdir -p /var/lib/postgresql && \
    mkdir -p /var/run/postgresql || true
RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg lsb-release curl ca-certificates && \
    echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > \
    /etc/apt/sources.list.d/pgdg.list && \
    curl --retry 3 --retry-delay 5 -fsSL "https://www.postgresql.org/media/keys/ACCC4CF8.asc" | \
    gnupg --dearmor -o /usr/share/keyrings/postgresql-keyring.gnupg && \
    apt-get update && apt-get install -y --no-install-recommends \
    postgresql-${VERSION%.*} postgresql-contrib-${VERSION%.*} && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /var/lib/postgresql/data /var/run/postgresql /app || true
FROM scratch AS entrypoint
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

FROM ghcr.io/wyattau/evergreenshim/db-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

# package-manager-verified: integrity verified by upstream
RUN apk add --no-cache bash gnupg curl ca-certificates libzstd1 liblz4-1
COPY --from=builder /var/lib/postgresql /var/lib/postgresql
COPY --from=builder /var/run/postgresql /var/run/postgresql
COPY --from=entrypoint /usr/local/bin/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod 755 /usr/local/bin/docker-entrypoint.sh 2>/dev/null || true && \
    adduser -u 5432 -D postgres 2>/dev/null || useradd -u 5432 -r -M -s /bin/false postgres 2>/dev/null || true && \
    mkdir -p /app /var/log/postgresql-17 /var/cache/postgresql-17 ; \
    mkdir -p /docker-entrypoint-initdb.d && \
    chown -R 5432:5432 /var/lib/postgresql /var/run/postgresql /app /var/log/postgresql-17 /var/cache/postgresql-17 /docker-entrypoint-initdb.d 2>/dev/null || true

USER 5432:5432
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
ENV PGDATA="/var/lib/postgresql/data" \
    PGPORT="5432"
EXPOSE 5432

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:5432"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "/usr/local/bin/docker-entrypoint.sh", "--", "postgres"]
LABEL org.opencontainers.image.title="postgresql-17" \
      org.opencontainers.image.version="17.10" \
      org.opencontainers.image.description="PostgreSQL 17 Database Server" \
      org.opencontainers.image.vendor="PostgreSQL Global Development Group" \
      org.opencontainers.image.platforms="linux/amd64,linux/arm64" \
      org.opencontainers.image.source="https://www.postgresql.org/" \
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
