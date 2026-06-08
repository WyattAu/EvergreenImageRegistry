ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.0.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=1.97.0
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v1.97.0/victoria-metrics-linux-${TARGETARCH}-v1.97.0-cluster.tar.gz -o /vm-cluster.tar.gz ; \
    echo "798f6e6e6f78e4502a17977a0dcc95fd237fbf7a89b59a1c46ae11790e029e21  /vm-cluster.tar.gz" | sha256sum -c ; \
    [ -f /vm-cluster.tar.gz ] && tar -xzf /vm-cluster.tar.gz -C /tmp && rm -f /vm-cluster.tar.gz ; \
    strip --strip-all /tmp/vminsert-prod 2>/dev/null&& \
    strip --strip-all /tmp/vmselect-prod 2>/dev/null&& \
    strip --strip-all /tmp/vmstorage-prod 2>/dev/null&& \
    mv /tmp/vminsert-prod /vminsert && \
    mv /tmp/vmselect-prod /vmselect && \
    mv /tmp/vmstorage-prod /vmstorage && { echo "Binary not available - download failed" >&2; exit 1; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/lib/victoriametrics /var/log/victoriametrics 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/db-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /vminsert /vminsert
COPY --from=downloader /vmselect /vmselect
COPY --from=downloader /vmstorage /vmstorage
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/lib/victoriametrics /var/lib/victoriametrics
COPY --from=builder /var/log/victoriametrics /var/log/victoriametrics
USER 65532:65532
ENV SHIM_BACKUP_ENABLED="true" \
    SHIM_BACKUP_DB_HOST="localhost" \
    SHIM_BACKUP_DB_PORT="8480" \
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
EXPOSE 8480

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8480"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="victoriametrics-cluster" \
      org.opencontainers.image.description="victoriametrics-cluster container image" \
      org.opencontainers.image.version="1.97.0" \
      org.opencontainers.image.vendor="VictoriaMetrics" \
      evergreen.image.tier="1" \
      evergreen.image.category="tsdb" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
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
