# =============================================================================
# EVERGREEN HARDENED POSTGRES
# Wolfi-based PostgreSQL 17 with health-shim as PID 1
# =============================================================================

ARG VERSION=17.10
ARG TARGETARCH
ARG SHIM_VERSION=v0.3.0

FROM ghcr.io/wyattau/evergreenshim/db-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache postgresql-17 postgresql-17-contrib ca-certificates

RUN addgroup -g 70 postgres && \
    adduser -D -u 70 -G postgres -h /var/lib/postgresql postgres && \
    mkdir -p /var/lib/postgresql/data /var/run/postgresql && \
    chown -R postgres:postgres /var/lib/postgresql /var/run/postgresql

ENV PGDATA=/var/lib/postgresql/data

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

COPY --from=shim /shim /usr/local/bin/shim
COPY shim.toml /etc/evergreen/shim.toml
RUN chmod +x /usr/local/bin/shim

USER postgres
ENV SHIM_BACKUP_ENABLED="false" \
    SHIM_BACKUP_DB_HOST="localhost" \
    SHIM_BACKUP_DB_PORT="5432" \
    SHIM_REPLICATION_ENABLED="false" \
    SHIM_MIGRATION_ENABLED="false" \
    SHIM_VAULT_ENABLED="false" \
    SHIM_AUDIT_ENABLED="true" \
    SHIM_METRICS_ENABLED="true" \
    SHIM_ALERTING_ENABLED="false" \
    SHIM_ALERTING_WEBHOOK_URL="" \
    SHIM_SCHEDULER_ENABLED="true" \
    SHIM_SCHEDULER_BACKUP_CRON="0 2 * * *"
EXPOSE 5432 9101

HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=5 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:5432"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "docker-entrypoint.sh", "--", "postgres"]
LABEL org.opencontainers.image.title="postgres" \
      org.opencontainers.image.description="PostgreSQL - advanced open source relational database" \
      org.opencontainers.image.version="17.10" \
      org.opencontainers.image.vendor="PostgreSQL" \
      evergreen.image.tier="critical" \
      evergreen.constraint.nonroot="true" \
      org.opencontainers.image.source="https://github.com/postgres/postgres"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.health.type="http"
LABEL evergreen.health.endpoint="/livez"
LABEL evergreen.health.listen="0.0.0.0:9101"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
