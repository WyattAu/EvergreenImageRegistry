# =============================================================================
# SOVEREIGN HARDENED PROMETHEUS BLACKBOX EXPORTER
# Version: 0.25.0
# Constraint: scratch - purest form, no shell, no package manager
# =============================================================================

ARG VERSION=0.25.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/prometheus/blackbox_exporter/releases/download/v${VERSION}/blackbox_exporter-${VERSION}.linux-amd64.tar.gz" -o /blackbox_exporter.tar.gz && \
    echo "c651ced6405c5e0cd292a400f47ae9b34f431f16c7bb098afbcd38f710144640  /blackbox_exporter.tar.gz" | sha256sum -c - && \
    tar -xzf /blackbox_exporter.tar.gz -C / && rm /blackbox_exporter.tar.gz && chmod +x /blackbox_exporter-${VERSION}.linux-amd64/blackbox_exporter

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
USER 65534:65534
WORKDIR /app
EXPOSE 9115
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/blackbox_exporter", "--version"]
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
