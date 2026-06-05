# =============================================================================
# EVERGREEN HARDENED POSTGRESQL PATRONI
# Generated from template - Version: 4.0.3
# Constraint: debian-slim - Python runtime requires glibc + pip
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=4.0.3
ARG TARGETARCH
ARG BUILD_DATE
ARG PYTHON_VERSION=3.12-slim
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v0.3.0

FROM python:${PYTHON_VERSION} AS builder
ARG VERSION=4.0.3
ARG PYTHON_VERSION=3.12-slim
RUN pip install --no-cache-dir --prefix=/install patroni[postgresql]=="${VERSION}" && \
    pip install --no-cache-dir --prefix=/install psycopg2-binary==2.9.9 && \
    find /install -type f -name "*.pyc" -delete && \
    find /install -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

FROM ghcr.io/wyattau/evergreenshim/db-shim:${SHIM_VERSION} AS shim

FROM registry.access.redhat.com/ubi9/ubi-minimal@sha256:10c773dc96763e3201275bae7865d278ca4b91db586117adec79079a2d7cdb80
COPY --from=shim /shim /shim

LABEL evergreen.base.fallback_reason="Python C extensions require glibc"

RUN microdnf install -y libpq curl ca-certificates
COPY --from=builder /install /usr/local
RUN adduser -u 65532 -s /bin/false patroni 2>/dev/null || true && \
    mkdir -p /app /var/log/patroni /var/cache/patroni ; \
    chown -R 65532:65532 /app /var/log/patroni /var/cache/patroni
USER 65532:65532
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
WORKDIR /app
EXPOSE 8008 5432
ENV PATRONI_RESTAPI_LISTEN="0.0.0.0:8008"

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8008"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="postgresql-patroni" \
      org.opencontainers.image.version="4.0.3" \
      org.opencontainers.image.description="Patroni - PostgreSQL High Availability with etcd/Consul/ZooKeeper" \
      org.opencontainers.image.vendor="Zalando" \
      org.opencontainers.image.source="https://github.com/patroni/patroni" \
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
