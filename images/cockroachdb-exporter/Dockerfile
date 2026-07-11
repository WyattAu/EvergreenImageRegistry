ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v2.0.0

FROM debian:bookworm-slim AS downloader
ARG TARGETARCH
ARG VERSION=23.2.3
RUN mkdir -p /opt/cockroach/cockroach || true
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/cockroachdb/cockroach/releases/download/v${VERSION}/cockroach-v${VERSION}.linux-${TARGETARCH}.tgz -o /cockroach.tar.gz ; echo "0019dfc4b32d63c1392aa264aed2253c1e0c2fb09216f8e2cc269bbfb8bb49b5  /cockroach.tar.gz" | sha256sum -c  ; mkdir -p /opt/cockroach ; \
    [ -f /cockroach.tar.gz ] && tar -xzf /cockroach.tar.gz -C /opt/cockroach --strip-components=1 ; \    rm -f /cockroach.tar.gz ; strip /opt/cockroach/cockroach ; chmod +x /opt/cockroach/cockroach || { echo "Binary not available - download failed" >&2; exit 1; }
FROM debian:bookworm-slim AS builder
ARG TARGETARCH
RUN mkdir -p /var/log/cockroach /var/lib/cockroach /var/cache/cockroach 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim

COPY --from=downloader /opt/cockroach/cockroach /cockroach
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /var/log/cockroach /var/log/cockroach
COPY --from=builder /var/lib/cockroach /var/lib/cockroach
COPY --from=builder /var/cache/cockroach /var/cache/cockroach
USER 65532:65532
ENV SHIM_BACKUP_ENABLED="true" \
    SHIM_BACKUP_DB_HOST="localhost" \
    SHIM_BACKUP_DB_PORT="8080" \
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
WORKDIR /
EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/cockroach"]
CMD ["--", "start", "--insecure", "--http-port=8080", "--prometheus-port=8080"]
LABEL org.opencontainers.image.title="cockroachdb-exporter" \
      org.opencontainers.image.description="Evergreen hardened CockroachDB Prometheus exporter - database metrics via built-in endpoint" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Cockroach Labs" \
      evergreen.image.tier="1" \
      evergreen.image.status="functional" \
      evergreen.image.category="database" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="5000ms" \
            org.opencontainers.image.source="https://github.com/cockroachdb/cockroach"

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
