# =============================================================================
# SOVEREIGN HARDENED PROMETHEUS NGINX EXPORTER
# Version: 1.1.0
# Constraint: scratch - purest form, no shell, no package manager
# =============================================================================

ARG VERSION=1.1.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/nginxinc/nginx-prometheus-exporter/releases/download/v${VERSION}/nginx-prometheus-exporter-${VERSION}-linux-amd64.tar.gz" -o /nginx-prometheus-exporter.tar.gz && \
    tar -xzf /nginx-prometheus-exporter.tar.gz -C / && rm /nginx-prometheus-exporter.tar.gz && chmod +x /nginx-prometheus-exporter

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/nginx_exporter /var/cache/nginx_exporter

FROM scratch
COPY --from=downloader /nginx-prometheus-exporter /nginx-prometheus-exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/nginx_exporter /var/log/nginx_exporter
COPY --from=builder /var/cache/nginx_exporter /var/cache/nginx_exporter
USER 65534:65534
WORKDIR /app
EXPOSE 9113
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/nginx-prometheus-exporter", "--version"]
ENTRYPOINT ["/nginx-prometheus-exporter"]
LABEL org.opencontainers.image.title="prometheus-nginx-exporter" \
      org.opencontainers.image.version="1.1.0" \
      org.opencontainers.image.vendor="NGINX Inc" \
      org.opencontainers.image.description="Prometheus exporter for NGINX stub_status metrics" \
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
