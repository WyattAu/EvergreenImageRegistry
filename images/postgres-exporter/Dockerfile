
ARG TARGETARCH
ARG VERSION=0.19.1
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v0.3.0

FROM ghcr.io/wyattau/evergreenshim/db-shim:${SHIM_VERSION} AS shim

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
COPY --from=shim /shim /shim

ARG TARGETARCH
ARG VERSION=0.19.1
RUN mkdir -p /tmp/pe/postgres_exporter || true
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* ; \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/prometheus-community/postgres_exporter/releases/download/v${VERSION}/postgres_exporter-${VERSION}.linux-${TARGETARCH}.tar.gz" -o /postgres_exporter.tar.gz ; \
    mkdir -p /tmp/pe && \
    if [ -f /postgres_exporter.tar.gz ]; then tar -xzf /postgres_exporter.tar.gz -C /tmp/pe && rm -f /postgres_exporter.tar.gz ; fi ; \
    mv /tmp/pe/postgres_exporter-${VERSION}.linux-${TARGETARCH}/postgres_exporter /tmp/pe/postgres_exporter 2>/dev/null ; \
    strip --strip-all /tmp/pe/postgres_exporter 2>/dev/null ; \FROM scratch
ARG VERSION=0.19.1
ARG TARGETARCH
COPY --from=downloader /tmp/pe/postgres_exporter /postgres_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
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
    SHIM_ALERTING_WEBHOOK_URL=""
WORKDIR /app
EXPOSE 9187

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:9187"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="postgres-exporter" \
      org.opencontainers.image.version="0.19.1" \
      org.opencontainers.image.vendor="Prometheus Community" \
      org.opencontainers.image.description="Evergreen hardened Postgres Exporter - Prometheus exporter for PostgreSQL" \
      evergreen.image.tier="critical" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      org.opencontainers.image.source="https://github.com/prometheus-community/postgres_exporter"

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
