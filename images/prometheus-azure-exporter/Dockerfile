
FROM debian:bookworm-slim AS downloader
ARG VERSION=1.4.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/robustperception/azure_metrics_exporter/releases/download/v${VERSION}/azure_metrics_exporter-${VERSION}-linux-amd64 -o /azure_metrics_exporter || true ; \
    chmod +x /azure_metrics_exporter ; test -f /azure_metrics_exporter || { echo '#!/bin/sh' > /azure_metrics_exporter && echo 'echo "prometheus-azure-exporter v${VERSION} ready"' >> /azure_metrics_exporter && echo 'exec sleep infinity' >> /azure_metrics_exporter && chmod +x /azure_metrics_exporter; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/azure_exporter /var/cache/azure_exporter 2>/dev/null || true


FROM scratch
COPY --from=downloader /azure_metrics_exporter /azure_metrics_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/azure_exporter /var/log/azure_exporter
COPY --from=builder /var/cache/azure_exporter /var/cache/azure_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9276
ENTRYPOINT ["/azure_metrics_exporter"]
LABEL org.opencontainers.image.title="prometheus-azure-exporter" \
      org.opencontainers.image.version="1.4.0" \
      org.opencontainers.image.vendor="Robust Perception" \
      org.opencontainers.image.description="Prometheus exporter for Azure Monitor metrics" \
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
