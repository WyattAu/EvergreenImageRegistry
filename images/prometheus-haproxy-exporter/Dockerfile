# =============================================================================
# SOVEREIGN HARDENED PROMETHEUS HAPROXY EXPORTER
# Version: 0.15.0
# Constraint: scratch - purest form, no shell, no package manager
# =============================================================================

ARG VERSION=0.15.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/prometheus/haproxy_exporter/releases/download/v${VERSION}/haproxy_exporter-${VERSION}.linux-amd64.tar.gz" -o /haproxy_exporter.tar.gz && \
    echo "ac200872b734e2f9c0211997f7f9c0ca5ad6522996c37aed39a732d5f3c0de16  /haproxy_exporter.tar.gz" | sha256sum -c - && \
    tar -xzf /haproxy_exporter.tar.gz -C / && rm /haproxy_exporter.tar.gz && chmod +x /haproxy_exporter-${VERSION}.linux-amd64/haproxy_exporter

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/haproxy_exporter /var/cache/haproxy_exporter

FROM scratch
COPY --from=downloader /haproxy_exporter-${VERSION}.linux-amd64/haproxy_exporter /haproxy_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/haproxy_exporter /var/log/haproxy_exporter
COPY --from=builder /var/cache/haproxy_exporter /var/cache/haproxy_exporter
USER 65534:65534
WORKDIR /app
EXPOSE 9101
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/haproxy_exporter", "--version"]
ENTRYPOINT ["/haproxy_exporter"]
LABEL org.opencontainers.image.title="prometheus-haproxy-exporter" \
      org.opencontainers.image.version="0.15.0" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.description="Prometheus exporter for HAProxy metrics" \
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
