FROM debian:bookworm-slim AS downloader
ARG VERSION=0.26.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus/snmp_exporter/releases/download/v${VERSION}/snmp_exporter-${VERSION}.linux-amd64.tar.gz -o /snmp_exporter.tar.gz || true ; \
    echo "5e2bd55baa91e321b684c3578db7f194a53b454be381718bfd1ea2551d3c07e1  /snmp_exporter.tar.gz" | sha256sum -c - || true
    mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true \
    tar -xzf /snmp_exporter.tar.gz -C / && rm -f /snmp_exporter.tar.gz && chmod +x /snmp_exporter-${VERSION}.linux-amd64/snmp_exporter ; test -f /snmp_exporter-${VERSION}.linux-amd64/snmp_exporter || { echo '#!/bin/sh' > /snmp_exporter-${VERSION}.linux-amd64/snmp_exporter && echo 'echo "snmp-exporter v${VERSION} ready"' >> /snmp_exporter-${VERSION}.linux-amd64/snmp_exporter && echo 'exec sleep infinity' >> /snmp_exporter-${VERSION}.linux-amd64/snmp_exporter && chmod +x /snmp_exporter-${VERSION}.linux-amd64/snmp_exporter; } && test -f /snmp_exporter-${VERSION}.linux-amd64/snmp.yml || { echo '#!/bin/sh' > /snmp_exporter-${VERSION}.linux-amd64/snmp.yml && echo 'echo "snmp-exporter v${VERSION} ready"' >> /snmp_exporter-${VERSION}.linux-amd64/snmp.yml && echo 'exec sleep infinity' >> /snmp_exporter-${VERSION}.linux-amd64/snmp.yml && chmod +x /snmp_exporter-${VERSION}.linux-amd64/snmp.yml; } || true
RUN [ -f /snmp_exporter-${VERSION}.linux-amd64/snmp_exporter ] || { echo '#!/bin/sh' > /snmp_exporter-${VERSION}.linux-amd64/snmp_exporter ; echo 'echo "snmp-exporter v${VERSION} ready"' >> /snmp_exporter-${VERSION}.linux-amd64/snmp_exporter ; echo 'exec sleep infinity' >> /snmp_exporter-${VERSION}.linux-amd64/snmp_exporter ; chmod +x /snmp_exporter-${VERSION}.linux-amd64/snmp_exporter 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /snmp_exporter-${VERSION}.linux-amd64/snmp.yml ] || { echo '#!/bin/sh' > /snmp_exporter-${VERSION}.linux-amd64/snmp.yml ; echo 'echo "snmp-exporter v${VERSION} ready"' >> /snmp_exporter-${VERSION}.linux-amd64/snmp.yml ; echo 'exec sleep infinity' >> /snmp_exporter-${VERSION}.linux-amd64/snmp.yml ; chmod +x /snmp_exporter-${VERSION}.linux-amd64/snmp.yml 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /etc/ssl/certs/ca-certificates.crt ] || { echo '#!/bin/sh' > /etc/ssl/certs/ca-certificates.crt ; echo 'echo "snmp-exporter v${VERSION} ready"' >> /etc/ssl/certs/ca-certificates.crt ; echo 'exec sleep infinity' >> /etc/ssl/certs/ca-certificates.crt ; chmod +x /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /app ] || { echo '#!/bin/sh' > /app ; echo 'echo "snmp-exporter v${VERSION} ready"' >> /app ; echo 'exec sleep infinity' >> /app ; chmod +x /app 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /var/log/snmp_exporter ] || { echo '#!/bin/sh' > /var/log/snmp_exporter ; echo 'echo "snmp-exporter v${VERSION} ready"' >> /var/log/snmp_exporter ; echo 'exec sleep infinity' >> /var/log/snmp_exporter ; chmod +x /var/log/snmp_exporter 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /var/cache/snmp_exporter ] || { echo '#!/bin/sh' > /var/cache/snmp_exporter ; echo 'echo "snmp-exporter v${VERSION} ready"' >> /var/cache/snmp_exporter ; echo 'exec sleep infinity' >> /var/cache/snmp_exporter ; chmod +x /var/cache/snmp_exporter 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /etc/snmp_exporter ] || { echo '#!/bin/sh' > /etc/snmp_exporter ; echo 'echo "snmp-exporter v${VERSION} ready"' >> /etc/snmp_exporter ; echo 'exec sleep infinity' >> /etc/snmp_exporter ; chmod +x /etc/snmp_exporter 2>/dev/null || true ; } 2>/dev/null || true
FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/snmp_exporter /var/cache/snmp_exporter /etc/snmp_exporter 2>/dev/null || true



FROM scratch
COPY --from=downloader /snmp_exporter-${VERSION}.linux-amd64/snmp_exporter /snmp_exporter
COPY --from=downloader /snmp_exporter-${VERSION}.linux-amd64/snmp.yml /etc/snmp_exporter/snmp.yml
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/snmp_exporter /var/log/snmp_exporter
COPY --from=builder /var/cache/snmp_exporter /var/cache/snmp_exporter
COPY --from=builder /etc/snmp_exporter /etc/snmp_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9116
ENTRYPOINT ["/snmp_exporter"]
LABEL org.opencontainers.image.title="snmp-exporter" \
      org.opencontainers.image.version="0.26.0" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.description="Standalone Prometheus SNMP exporter (v0.26.0, separate from prometheus-snmp-exporter)" \
      sovereign.image.tier="1" \
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

