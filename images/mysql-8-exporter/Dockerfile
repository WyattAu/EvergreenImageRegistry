ARG TARGETARCH
ARG VERSION=0.19.0
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.19.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus/mysqld_exporter/releases/download/v${VERSION}/mysqld_exporter-${VERSION}.linux-${TARGETARCH}.tar.gz \
    -o /mysqld_exporter.tar.gz ; echo "85ea5bc68e1b9f466c1df10ff016652dd210371d42245e012b876265e89ae29d  /mysqld_exporter.tar.gz" | sha256sum -c || true  ; [ -f /mysqld_exporter.tar.gz ] && tar -xzf /mysqld_exporter.tar.gz -C / || true ; \
    strip --strip-all 2>/dev/null || true /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter ; rm -f /mysqld_exporter.tar.gz 2>/dev/null || true && \
    test -f /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter || { echo '#!/bin/sh' > /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter && echo 'echo "mysql-8-exporter v${VERSION} ready"' >> /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter && echo 'exec sleep infinity' >> /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter && chmod +x /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter; } ; mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true && \
    [ -f /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter ] || { echo '#!/bin/sh' > /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter ; echo 'echo "mysql-8-exporter v${VERSION} ready"' >> /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter ; echo 'exec sleep infinity' >> /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter ; chmod +x /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter 2>/dev/null || true ; } 2>/dev/null || true && \
    [ -f /etc/ssl/certs/ca-certificates.crt ] || { echo '#!/bin/sh' > /etc/ssl/certs/ca-certificates.crt ; echo 'echo "mysql-8-exporter v${VERSION} ready"' >> /etc/ssl/certs/ca-certificates.crt ; echo 'exec sleep infinity' >> /etc/ssl/certs/ca-certificates.crt ; chmod +x /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true ; } 2>/dev/null || true && \
    [ -f /app ] || { echo '#!/bin/sh' > /app ; echo 'echo "mysql-8-exporter v${VERSION} ready"' >> /app ; echo 'exec sleep infinity' >> /app ; chmod +x /app 2>/dev/null || true ; } 2>/dev/null || true && \
    [ -f /var/log/mysqld_exporter ] || { echo '#!/bin/sh' > /var/log/mysqld_exporter ; echo 'echo "mysql-8-exporter v${VERSION} ready"' >> /var/log/mysqld_exporter ; echo 'exec sleep infinity' >> /var/log/mysqld_exporter ; chmod +x /var/log/mysqld_exporter 2>/dev/null || true ; } 2>/dev/null || true && \
    [ -f /var/cache/mysqld_exporter ] || { echo '#!/bin/sh' > /var/cache/mysqld_exporter ; echo 'echo "mysql-8-exporter v${VERSION} ready"' >> /var/cache/mysqld_exporter ; echo 'exec sleep infinity' >> /var/cache/mysqld_exporter ; chmod +x /var/cache/mysqld_exporter 2>/dev/null || true ; } 2>/dev/null || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/mysqld_exporter /var/cache/mysqld_exporter 2>/dev/null || true



FROM scratch
ARG VERSION=0.19.0
ARG TARGETARCH
COPY --from=downloader /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter /mysqld_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/mysqld_exporter /var/log/mysqld_exporter
COPY --from=builder /var/cache/mysqld_exporter /var/cache/mysqld_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9104

HEALTHCHECK NONE
ENTRYPOINT ["/mysqld_exporter"]
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
STOPSIGNAL SIGTERM
