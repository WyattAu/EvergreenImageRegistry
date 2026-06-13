ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.1.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=v1.143.0
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v1.142.0/victoria-metrics-linux-${TARGETARCH}-v1.142.0-cluster.tar.gz -o /victoria-metrics.tar.gz ; \
    # TODO: update sha256 for new version
    echo "a9415aa4d6f666f1715ffd8b564128b3e3b468139b43b6ff1194ad3f5242ede3  /victoria-metrics.tar.gz" | sha256sum -c ; \
    [ -f /victoria-metrics.tar.gz ] && tar -xzf /victoria-metrics.tar.gz -C / && rm -f /victoria-metrics.tar.gz && chmod +x /victoria-metrics 2>/dev/null ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v1.142.0/victoria-metrics-linux-${TARGETARCH}-v1.142.0-cluster.tar.gz -o /victoria-metrics \
    mkdir -p /app /var/log/victoria-metrics /var/cache/victoria-metrics 2>/dev/null || true

FROM ghcr.io/wyattau/evergreenshim/db-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /victoria-metrics /victoria-metrics
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=downloader /app /app
COPY --from=downloader /var/log/victoria-metrics /var/log/victoria-metrics
COPY --from=downloader /var/cache/victoria-metrics /var/cache/victoria-metrics
USER 65532:65532
ENV SHIM_BACKUP_ENABLED="true" \
    SHIM_BACKUP_DB_HOST="localhost" \
    SHIM_BACKUP_DB_PORT="8428" \
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
    SHIM_SCHEDULER_BACKUP_CRON="0 0 2 * * *" \
    SHIM_MANAGEMENT_ENABLED="true" \
    SHIM_MANAGEMENT_HOST="0.0.0.0" \
    SHIM_MANAGEMENT_PORT="9102"
WORKDIR /app
EXPOSE 8428

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8428"]

ENTRYPOINT ["/shim", "run", "-c", "/victoria-metrics"]
LABEL org.opencontainers.image.title="victoriametrics" \
      org.opencontainers.image.description="VictoriaMetrics - fast, cost-effective time series database" \
      org.opencontainers.image.version="v1.143.0" \
      org.opencontainers.image.vendor="VictoriaMetrics" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/VictoriaMetrics/VictoriaMetrics"

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
