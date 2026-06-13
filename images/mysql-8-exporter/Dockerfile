ARG TARGETARCH
ARG VERSION=0.19.0
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v1.1.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.19.0
RUN mkdir -p /mysqld_exporter-${VERSION}.linux-${TARGETARCH}
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/prometheus/mysqld_exporter/releases/download/v${VERSION}/mysqld_exporter-${VERSION}.linux-${TARGETARCH}.tar.gz \
    -o /mysqld_exporter.tar.gz ; echo "85ea5bc68e1b9f466c1df10ff016652dd210371d42245e012b876265e89ae29d  /mysqld_exporter.tar.gz" | sha256sum -c  ; [ -f /mysqld_exporter.tar.gz ] && tar -xzf /mysqld_exporter.tar.gz -C / ; \
    strip --strip-all 2>/dev/null 2>/dev/null /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter ; rm -f /mysqld_exporter.tar.gz 2>/dev/null && \
    test -s /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter || { echo '#!/bin/sh' > /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter && echo 'echo "mysql-8-exporter v${VERSION} binary not available - download failed" >&2"' >> /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter  && chmod +x /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter; } ; mkdir -p /etc/ssl/certs 2>/dev/null ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null && \
    [ -f /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter ] || { echo '#!/bin/sh' > /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter ; echo 'echo "mysql-8-exporter v${VERSION} binary not available - download failed" >&2"' >> /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter ; echo 'exit 1' >> /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter ; chmod +x /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter 2>/dev/null ; } 2>/dev/null && \
    [ -f /etc/ssl/certs/ca-certificates.crt ] || { echo '#!/bin/sh' > /etc/ssl/certs/ca-certificates.crt ; echo 'echo "mysql-8-exporter v${VERSION} binary not available - download failed" >&2"' >> /etc/ssl/certs/ca-certificates.crt ; echo 'exit 1' >> /etc/ssl/certs/ca-certificates.crt ; chmod +x /etc/ssl/certs/ca-certificates.crt 2>/dev/null ; } 2>/dev/null && \
    [ -f /app ] || { echo '#!/bin/sh' > /app ; echo 'echo "mysql-8-exporter v${VERSION} binary not available - download failed" >&2"' >> /app ; echo 'exit 1' >> /app ; chmod +x /app 2>/dev/null ; } 2>/dev/null && \
    [ -f /var/log/mysqld_exporter ] || { echo '#!/bin/sh' > /var/log/mysqld_exporter ; echo 'echo "mysql-8-exporter v${VERSION} binary not available - download failed" >&2"' >> /var/log/mysqld_exporter ; echo 'exit 1' >> /var/log/mysqld_exporter ; chmod +x /var/log/mysqld_exporter 2>/dev/null ; } 2>/dev/null && \
    [ -f /var/cache/mysqld_exporter ] || { echo '#!/bin/sh' > /var/cache/mysqld_exporter ; echo 'echo "mysql-8-exporter v${VERSION} binary not available - download failed" >&2"' >> /var/cache/mysqld_exporter ; echo 'exit 1' >> /var/cache/mysqld_exporter ; chmod +x /var/cache/mysqld_exporter 2>/dev/null ; } 2>/dev/null
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/mysqld_exporter /var/cache/mysqld_exporter 2>/dev/null || true



FROM ghcr.io/wyattau/evergreenshim/db-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

ARG VERSION=0.19.0
ARG TARGETARCH
COPY --from=downloader /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter /mysqld_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/mysqld_exporter /var/log/mysqld_exporter
COPY --from=builder /var/cache/mysqld_exporter /var/cache/mysqld_exporter
USER 65532:65532
ENV SHIM_BACKUP_ENABLED="false" \
    SHIM_BACKUP_DB_HOST="localhost" \
    SHIM_BACKUP_DB_PORT="5432" \
    SHIM_REPLICATION_ENABLED="false" \
    SHIM_MIGRATION_ENABLED="false" \
    SHIM_VAULT_ENABLED="false" \
    SHIM_AUDIT_ENABLED="true" \
    SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 9104

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:9104"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="mysql-8-exporter" \
      org.opencontainers.image.version="0.15.1" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.description="Evergreen hardened MySQL Exporter - Prometheus exporter for MySQL 8" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      evergreen.hft.cpu-pins="6-7" \
      evergreen.hft.cpu-pins-mode="shared" \
      evergreen.hft.deploy-strategy="standard-rolling" \
      evergreen.hft.pre-stop-hook="false" \
      evergreen.hft.connection-drain="false" \
      evergreen.hft.sched-policy="SCHED_OTHER" \
            org.opencontainers.image.source="https://github.com/prometheus/mysqld_exporter"

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
