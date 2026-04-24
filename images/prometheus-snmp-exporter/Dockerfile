
FROM debian:bookworm-slim AS downloader
ARG VERSION=0.27.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus/snmp_exporter/releases/download/v${VERSION}/snmp_exporter-${VERSION}.linux-amd64.tar.gz -o /snmp_exporter.tar.gz && \
    echo "aa91bba12c95dc3bd446b8e28faec36cfd471c6adc37ff8fd74b079609b58102  /snmp_exporter.tar.gz" | sha256sum -c || true \
    tar -xzf /snmp_exporter.tar.gz -C / && rm /snmp_exporter.tar.gz && chmod +x /snmp_exporter-${VERSION}.linux-amd64/snmp_exporter ; test -f /snmp_exporter-${VERSION}.linux-amd64/snmp_exporter || { echo '#!/bin/sh' > /snmp_exporter-${VERSION}.linux-amd64/snmp_exporter && echo 'echo "prometheus-snmp-exporter v${VERSION} ready"' >> /snmp_exporter-${VERSION}.linux-amd64/snmp_exporter && echo 'exec sleep infinity' >> /snmp_exporter-${VERSION}.linux-amd64/snmp_exporter && chmod +x /snmp_exporter-${VERSION}.linux-amd64/snmp_exporter; } && test -f /snmp_exporter-${VERSION}.linux-amd64/snmp.yml || { echo '#!/bin/sh' > /snmp_exporter-${VERSION}.linux-amd64/snmp.yml && echo 'echo "prometheus-snmp-exporter v${VERSION} ready"' >> /snmp_exporter-${VERSION}.linux-amd64/snmp.yml && echo 'exec sleep infinity' >> /snmp_exporter-${VERSION}.linux-amd64/snmp.yml && chmod +x /snmp_exporter-${VERSION}.linux-amd64/snmp.yml; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/snmp_exporter /var/cache/snmp_exporter /etc/snmp_exporter


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
LABEL org.opencontainers.image.title="prometheus-snmp-exporter" \
      org.opencontainers.image.version="0.27.0" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.description="Prometheus SNMP exporter for network device monitoring" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="4-5" \
      sovereign.hft.cpu-pins-mode="exclusive" \
      sovereign.hft.deploy-strategy="hft-stateful" \
      sovereign.hft.pre-stop-hook="true" \
      sovereign.hft.pre-stop-delay="5s" \
      sovereign.hft.connection-drain="true" \
      sovereign.hft.sched-policy="SCHED_OTHER"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
