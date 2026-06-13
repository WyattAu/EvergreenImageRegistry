ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v1.0.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=3.6.10
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/etcd-io/etcd/releases/download/v${VERSION}/etcd-v${VERSION}-linux-${TARGETARCH}.tar.gz" -o /etcd.tar.gz && \
    echo "230566b9e0311690faf515404fb2a57199faf2c0685b39c5c7a0a0ba5ad9a631  /etcd.tar.gz" | sha256sum -c && \
    if [ -f /etcd.tar.gz ]; then tar -xzf /etcd.tar.gz -C /tmp && chmod +x /tmp/etcd-v${VERSION}-linux-${TARGETARCH}/etcd && mv /tmp/etcd-v${VERSION}-linux-${TARGETARCH}/etcd /etcd && rm -rf /etcd.tar.gz /tmp/etcd-v${VERSION}-linux-${TARGETARCH}; fi && \' && { echo "Binary not available - download failed" >&2; exit 1; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/etcd /var/cache/etcd /etcd-data 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/db-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

ARG VERSION=3.6.10
COPY --from=downloader /etcd /etcd
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/etcd /var/log/etcd
COPY --from=builder /var/cache/etcd /var/cache/etcd
COPY --from=builder /etcd-data /etcd-data
USER 65532:65532
ENV SHIM_BACKUP_ENABLED="true" \
    SHIM_BACKUP_DB_HOST="localhost" \
    SHIM_BACKUP_DB_PORT="2379" \
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
EXPOSE 2379 2380

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:2379"]

ENTRYPOINT ["/shim", "run"]
CMD ["-c", "/etcd", "--", "--data-dir", "/etcd-data", "--listen-client-urls", "http://0.0.0.0:2379", "--advertise-client-urls", "http://localhost:2379"]
LABEL org.opencontainers.image.title="etcd-empty" \
      org.opencontainers.image.description="etcd-empty container image" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="etcd" \
      org.opencontainers.image.source="https://github.com/etcd-io/etcd" \
      evergreen.image.tier="1" \
      evergreen.image.status="functional" \
      evergreen.image.category="database" \
      evergreen.image.note="Empty etcd for bootstrapping new clusters. Mount persistent volume at /etcd-data." \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      evergreen.hft.deploy-strategy="hft-stateful" \
      evergreen.hft.sched-policy="SCHED_OTHER"

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
