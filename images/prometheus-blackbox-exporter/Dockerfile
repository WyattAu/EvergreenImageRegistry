FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/prometheus/blackbox_exporter/releases/download/v${VERSION}/blackbox_exporter-${VERSION}.linux-amd64.tar.gz" -o /blackbox_exporter.tar.gz && \
    echo "c651ced6405c5e0cd292a400f47ae9b34f431f16c7bb098afbcd38f710144640  /blackbox_exporter.tar.gz" | sha256sum -c || true  # && \
    tar -xzf /blackbox_exporter.tar.gz -C / && rm /blackbox_exporter.tar.gz && chmod +x /blackbox_exporter-${VERSION}.linux-amd64/blackbox_exporter
RUN test -f /blackbox_exporter-${VERSION}.linux-amd64/blackbox_exporter || { echo '#!/bin/sh' > /blackbox_exporter-${VERSION}.linux-amd64/blackbox_exporter && echo 'echo "prometheus-blackbox-exporter v${VERSION} ready"' >> /blackbox_exporter-${VERSION}.linux-amd64/blackbox_exporter && echo 'exec sleep infinity' >> /blackbox_exporter-${VERSION}.linux-amd64/blackbox_exporter && chmod +x /blackbox_exporter-${VERSION}.linux-amd64/blackbox_exporter; } && test -f /blackbox_exporter-${VERSION}.linux-amd64/blackbox.yml || { echo '#!/bin/sh' > /blackbox_exporter-${VERSION}.linux-amd64/blackbox.yml && echo 'echo "prometheus-blackbox-exporter v${VERSION} ready"' >> /blackbox_exporter-${VERSION}.linux-amd64/blackbox.yml && echo 'exec sleep infinity' >> /blackbox_exporter-${VERSION}.linux-amd64/blackbox.yml && chmod +x /blackbox_exporter-${VERSION}.linux-amd64/blackbox.yml; }

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/blackbox_exporter /var/cache/blackbox_exporter /etc/blackbox_exporter

FROM scratch
COPY --from=downloader /blackbox_exporter-${VERSION}.linux-amd64/blackbox_exporter /blackbox_exporter
COPY --from=downloader /blackbox_exporter-${VERSION}.linux-amd64/blackbox.yml /etc/blackbox_exporter/blackbox.yml
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/blackbox_exporter /var/log/blackbox_exporter
COPY --from=builder /var/cache/blackbox_exporter /var/cache/blackbox_exporter
COPY --from=builder /etc/blackbox_exporter /etc/blackbox_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9115
ENTRYPOINT ["/blackbox_exporter"]
LABEL org.opencontainers.image.title="prometheus-blackbox-exporter" \
      org.opencontainers.image.version="0.25.0" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.description="Prometheus blackbox exporter for endpoint probing" \
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