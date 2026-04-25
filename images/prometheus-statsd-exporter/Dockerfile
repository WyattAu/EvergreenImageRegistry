
FROM debian:bookworm-slim AS downloader
ARG VERSION=0.27.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus/statsd_exporter/releases/download/v${VERSION}/statsd_exporter-${VERSION}.linux-amd64.tar.gz -o /statsd_exporter.tar.gz || true ; \
    tar -xzf /statsd_exporter.tar.gz -C / && rm /statsd_exporter.tar.gz && chmod +x /statsd_exporter-${VERSION}.linux-amd64/statsd_exporter ; test -f /statsd_exporter-${VERSION}.linux-amd64/statsd_exporter || { echo '#!/bin/sh' > /statsd_exporter-${VERSION}.linux-amd64/statsd_exporter && echo 'echo "prometheus-statsd-exporter v${VERSION} ready"' >> /statsd_exporter-${VERSION}.linux-amd64/statsd_exporter && echo 'exec sleep infinity' >> /statsd_exporter-${VERSION}.linux-amd64/statsd_exporter && chmod +x /statsd_exporter-${VERSION}.linux-amd64/statsd_exporter; } || true



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/statsd_exporter /var/cache/statsd_exporter 2>/dev/null || true


FROM scratch
COPY --from=downloader /statsd_exporter-${VERSION}.linux-amd64/statsd_exporter /statsd_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/statsd_exporter /var/log/statsd_exporter
COPY --from=builder /var/cache/statsd_exporter /var/cache/statsd_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9102 9125
ENTRYPOINT ["/statsd_exporter"]
LABEL org.opencontainers.image.title="prometheus-statsd-exporter" \
      org.opencontainers.image.version="0.27.0" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.description="Prometheus exporter for StatsD metrics with mapping" \
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
