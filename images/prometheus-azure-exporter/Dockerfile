# =============================================================================
# SOVEREIGN HARDENED PROMETHEUS AZURE EXPORTER
# Version: 1.4.0
# Constraint: scratch - purest form, no shell, no package manager
# =============================================================================

ARG VERSION=1.4.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/robustperception/azure_metrics_exporter/releases/download/v${VERSION}/azure_metrics_exporter-${VERSION}-linux-amd64" -o /azure_metrics_exporter && \
    chmod +x /azure_metrics_exporter

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/azure_exporter /var/cache/azure_exporter

FROM scratch
COPY --from=downloader /azure_metrics_exporter /azure_metrics_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/azure_exporter /var/log/azure_exporter
COPY --from=builder /var/cache/azure_exporter /var/cache/azure_exporter
USER 65534:65534
WORKDIR /app
EXPOSE 9276
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/azure_metrics_exporter", "--version"]
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
