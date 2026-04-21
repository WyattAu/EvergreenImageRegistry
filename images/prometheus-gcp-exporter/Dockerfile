# =============================================================================
# SOVEREIGN HARDENED PROMETHEUS GCP EXPORTER
# Version: 0.10.0
# Constraint: scratch - purest form, no shell, no package manager
# =============================================================================

ARG VERSION=0.10.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/GoogleCloudPlatform/prometheus-engine/releases/download/v${VERSION}/stackdriver-prometheus-sidecar-${VERSION}-linux-amd64.tar.gz" -o /stackdriver-sidecar.tar.gz && \
    tar -xzf /stackdriver-sidecar.tar.gz -C / && rm /stackdriver-sidecar.tar.gz && chmod +x /stackdriver-prometheus-sidecar

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/gcp_exporter /var/cache/gcp_exporter

FROM scratch
COPY --from=downloader /stackdriver-prometheus-sidecar /stackdriver-prometheus-sidecar
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/gcp_exporter /var/log/gcp_exporter
COPY --from=builder /var/cache/gcp_exporter /var/cache/gcp_exporter
USER 65534:65534
WORKDIR /app
EXPOSE 9090
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/stackdriver-prometheus-sidecar", "--version"]
ENTRYPOINT ["/stackdriver-prometheus-sidecar"]
LABEL org.opencontainers.image.title="prometheus-gcp-exporter" \
      org.opencontainers.image.version="0.10.0" \
      org.opencontainers.image.vendor="Google Cloud Platform" \
      org.opencontainers.image.description="Stackdriver Prometheus sidecar for GCP metrics" \
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
