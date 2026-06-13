ARG VERSION=1.12.0
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.1.0

FROM ghcr.io/zalando/postgres-operator:v${VERSION} AS upstream

FROM ghcr.io/wyattau/evergreenshim/db-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=upstream /postgres-operator /usr/local/bin/postgres-operator
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
ENV SHIM_BACKUP_ENABLED="true" \
    SHIM_BACKUP_DB_HOST="localhost" \
    SHIM_BACKUP_DB_PORT="5432" \
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
EXPOSE 8080 8443

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="postgres-operator" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Zalando PostgreSQL Operator for Kubernetes" \
      org.opencontainers.image.vendor="Zalando" \
      org.opencontainers.image.source="https://github.com/zalando/postgres-operator" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"

LABEL evergreen.base.image="scratch"
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
