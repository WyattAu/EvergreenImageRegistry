# =============================================================================
# SOVEREIGN HARDENED ELASTICSEARCH-EXPORTER
# Generated from template - Version: 1.7.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.7.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/prometheus-community/elasticsearch_exporter/releases/download/v${VERSION}/elasticsearch_exporter-${VERSION}-linux-amd64.tar.gz" \
    -o /elasticsearch_exporter.tar.gz \
    && echo "45aff83bcea639dc977e34eaa6ad7b1453be96be469f570b39c2d4fc69bf5ffc  /elasticsearch_exporter.tar.gz" | sha256sum -c - \
    && tar -xzf /elasticsearch_exporter.tar.gz -C / \
    && strip --strip-all /elasticsearch_exporter-${VERSION}-linux-amd64/elasticsearch_exporter \
    && rm /elasticsearch_exporter.tar.gz

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/elasticsearch_exporter /var/cache/elasticsearch_exporter

FROM scratch
COPY --from=downloader /elasticsearch_exporter-${VERSION}-linux-amd64/elasticsearch_exporter /elasticsearch_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/elasticsearch_exporter /var/log/elasticsearch_exporter
COPY --from=builder /var/cache/elasticsearch_exporter /var/cache/elasticsearch_exporter
USER 65534:65534
WORKDIR /app
EXPOSE 9114
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/elasticsearch_exporter", "--version"]
ENTRYPOINT ["/elasticsearch_exporter"]
LABEL org.opencontainers.image.title="elasticsearch-exporter" \
      org.opencontainers.image.version="1.7.0" \
      org.opencontainers.image.vendor="Prometheus Community" \
      org.opencontainers.image.description="Sovereign hardened Elasticsearch Exporter - Prometheus exporter for Elasticsearch" \
      sovereign.image.tier="1" \
      sovereign.image.category="observability" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="6-7" \
      sovereign.hft.cpu-pins-mode="shared" \
      sovereign.hft.deploy-strategy="standard-rolling" \
      sovereign.hft.pre-stop-hook="false" \
      sovereign.hft.connection-drain="false" \
      sovereign.hft.sched-policy="SCHED_OTHER"
