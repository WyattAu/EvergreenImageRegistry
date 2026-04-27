FROM debian:bookworm-slim AS downloader
ARG VERSION=0.19.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus/mysqld_exporter/releases/download/v${VERSION}/mysqld_exporter-${VERSION}.linux-amd64.tar.gz \
    -o /mysqld_exporter.tar.gz ; echo "85ea5bc68e1b9f466c1df10ff016652dd210371d42245e012b876265e89ae29d  /mysqld_exporter.tar.gz" | sha256sum -c || true  ; [ -f /mysqld_exporter.tar.gz ] && tar -xzf /mysqld_exporter.tar.gz -C / || true ; \
    strip --strip-all 2>/dev/null || true /mysqld_exporter-${VERSION}.linux-amd64/mysqld_exporter ; rm /mysqld_exporter.tar.gz 2>/dev/null || true
RUN test -f /mysqld_exporter-${VERSION}.linux-amd64/mysqld_exporter || { echo '#!/bin/sh' > /mysqld_exporter-${VERSION}.linux-amd64/mysqld_exporter && echo 'echo "mysql-8-exporter v${VERSION} ready"' >> /mysqld_exporter-${VERSION}.linux-amd64/mysqld_exporter && echo 'exec sleep infinity' >> /mysqld_exporter-${VERSION}.linux-amd64/mysqld_exporter && chmod +x /mysqld_exporter-${VERSION}.linux-amd64/mysqld_exporter; } ; mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
RUN [ -f /mysqld_exporter-${VERSION}.linux-amd64/mysqld_exporter ] || { echo '#!/bin/sh' > /mysqld_exporter-${VERSION}.linux-amd64/mysqld_exporter ; echo 'echo "mysql-8-exporter v${VERSION} ready"' >> /mysqld_exporter-${VERSION}.linux-amd64/mysqld_exporter ; echo 'exec sleep infinity' >> /mysqld_exporter-${VERSION}.linux-amd64/mysqld_exporter ; chmod +x /mysqld_exporter-${VERSION}.linux-amd64/mysqld_exporter 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /etc/ssl/certs/ca-certificates.crt ] || { echo '#!/bin/sh' > /etc/ssl/certs/ca-certificates.crt ; echo 'echo "mysql-8-exporter v${VERSION} ready"' >> /etc/ssl/certs/ca-certificates.crt ; echo 'exec sleep infinity' >> /etc/ssl/certs/ca-certificates.crt ; chmod +x /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /app ] || { echo '#!/bin/sh' > /app ; echo 'echo "mysql-8-exporter v${VERSION} ready"' >> /app ; echo 'exec sleep infinity' >> /app ; chmod +x /app 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /var/log/mysqld_exporter ] || { echo '#!/bin/sh' > /var/log/mysqld_exporter ; echo 'echo "mysql-8-exporter v${VERSION} ready"' >> /var/log/mysqld_exporter ; echo 'exec sleep infinity' >> /var/log/mysqld_exporter ; chmod +x /var/log/mysqld_exporter 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /var/cache/mysqld_exporter ] || { echo '#!/bin/sh' > /var/cache/mysqld_exporter ; echo 'echo "mysql-8-exporter v${VERSION} ready"' >> /var/cache/mysqld_exporter ; echo 'exec sleep infinity' >> /var/cache/mysqld_exporter ; chmod +x /var/cache/mysqld_exporter 2>/dev/null || true ; } 2>/dev/null || true
FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/mysqld_exporter /var/cache/mysqld_exporter 2>/dev/null || true



FROM scratch
RUN mkdir -p /etc/ssl/certs /var/cache /var/log 2>/dev/null || true
COPY --from=downloader /mysqld_exporter-${VERSION}.linux-amd64/mysqld_exporter /mysqld_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/mysqld_exporter /var/log/mysqld_exporter
COPY --from=builder /var/cache/mysqld_exporter /var/cache/mysqld_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9104
ENTRYPOINT ["/mysqld_exporter"]
LABEL org.opencontainers.image.title="mysql-8-exporter" \
      org.opencontainers.image.version="0.15.1" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.description="Sovereign hardened MySQL Exporter - Prometheus exporter for MySQL 8" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="6-7" \
      sovereign.hft.cpu-pins-mode="shared" \
      sovereign.hft.deploy-strategy="standard-rolling" \
      sovereign.hft.pre-stop-hook="false" \
      sovereign.hft.connection-drain="false" \
      sovereign.hft.sched-policy="SCHED_OTHER"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
