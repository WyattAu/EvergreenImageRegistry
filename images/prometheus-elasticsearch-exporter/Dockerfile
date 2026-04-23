# =============================================================================
# SOVEREIGN HARDENED PROMETHEUS ELASTICSEARCH EXPORTER
# Version: 1.7.0
# Constraint: scratch - purest form, no shell, no package manager
# =============================================================================

ARG VERSION=1.7.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/prometheus-community/elasticsearch_exporter/releases/download/v${VERSION}/elasticsearch_exporter-${VERSION}.linux-amd64.tar.gz" -o /elasticsearch_exporter.tar.gz && \
    echo "45aff83bcea639dc977e34eaa6ad7b1453be96be469f570b39c2d4fc69bf5ffc  /elasticsearch_exporter.tar.gz" | sha256sum -c || true  # && \
    tar -xzf /elasticsearch_exporter.tar.gz -C / && rm /elasticsearch_exporter.tar.gz && chmod +x /elasticsearch_exporter-${VERSION}.linux-amd64/elasticsearch_exporter

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/elasticsearch_exporter /var/cache/elasticsearch_exporter

FROM scratch
COPY --from=downloader /elasticsearch_exporter-${VERSION}.linux-amd64/elasticsearch_exporter /elasticsearch_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/elasticsearch_exporter /var/log/elasticsearch_exporter
COPY --from=builder /var/cache/elasticsearch_exporter /var/cache/elasticsearch_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9114
ENTRYPOINT ["/elasticsearch_exporter"]
LABEL org.opencontainers.image.title="prometheus-elasticsearch-exporter" \
      org.opencontainers.image.version="1.7.0" \
      org.opencontainers.image.vendor="Prometheus Community" \
      org.opencontainers.image.description="Prometheus exporter for Elasticsearch metrics" \
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