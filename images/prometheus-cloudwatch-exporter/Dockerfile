# =============================================================================
# SOVEREIGN HARDENED PROMETHEUS CLOUDWATCH EXPORTER
# Version: 0.15.0
# Constraint: scratch - purest form, no shell, no package manager
# =============================================================================

ARG VERSION=0.15.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/prometheus-community/cloudwatch_exporter/releases/download/v${VERSION}/cloudwatch_exporter-${VERSION}.linux-amd64.tar.gz" -o /cloudwatch_exporter.tar.gz && \
    tar -xzf /cloudwatch_exporter.tar.gz -C / && rm /cloudwatch_exporter.tar.gz && chmod +x /cloudwatch_exporter-${VERSION}.linux-amd64/cloudwatch_exporter

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/cloudwatch_exporter /var/cache/cloudwatch_exporter /etc/cloudwatch_exporter

FROM scratch
COPY --from=downloader /cloudwatch_exporter-${VERSION}.linux-amd64/cloudwatch_exporter /cloudwatch_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/cloudwatch_exporter /var/log/cloudwatch_exporter
COPY --from=builder /var/cache/cloudwatch_exporter /var/cache/cloudwatch_exporter
COPY --from=builder /etc/cloudwatch_exporter /etc/cloudwatch_exporter
USER 65534:65534
WORKDIR /app
EXPOSE 9106
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/cloudwatch_exporter", "--version"]
ENTRYPOINT ["/cloudwatch_exporter"]
LABEL org.opencontainers.image.title="prometheus-cloudwatch-exporter" \
      org.opencontainers.image.version="0.15.0" \
      org.opencontainers.image.vendor="Prometheus Community" \
      org.opencontainers.image.description="Prometheus exporter for AWS CloudWatch metrics" \
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
