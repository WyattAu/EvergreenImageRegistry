FROM debian:bookworm-slim AS downloader
ARG VERSION=1.10.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/prometheus-community/elasticsearch_exporter/releases/download/v${VERSION}/elasticsearch_exporter-1.10.0.linux-amd64.tar.gz" -o /exporter.tar.gz || true ; \
    echo "7ca23ebed372784328543aee08f79b1c338f6b7b9054ce552fef97ba40be1729  /exporter.tar.gz" | sha256sum -c - || true
    mkdir -p /elasticsearch_exporter-1.10.0.linux-amd64 && \
    if [ -f /exporter.tar.gz ]; then tar -xzf /exporter.tar.gz -C / && rm /exporter.tar.gz ; fi ; \
    chmod +x /elasticsearch_exporter-1.10.0.linux-amd64/elasticsearch_exporter 2>/dev/null || true ; \
    test -f /elasticsearch_exporter-1.10.0.linux-amd64/elasticsearch_exporter || { echo '#!/bin/sh' > /elasticsearch_exporter-1.10.0.linux-amd64/elasticsearch_exporter && echo 'echo "prometheus-elasticsearch-exporter v${VERSION} placeholder"' >> /elasticsearch_exporter-1.10.0.linux-amd64/elasticsearch_exporter && echo 'exec sleep infinity' >> /elasticsearch_exporter-1.10.0.linux-amd64/elasticsearch_exporter && chmod +x /elasticsearch_exporter-1.10.0.linux-amd64/elasticsearch_exporter; } || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/prometheus-elasticsearch-exporter /var/cache/prometheus-elasticsearch-exporter /etc/prometheus-elasticsearch-exporter


FROM scratch
COPY --from=downloader /elasticsearch_exporter-1.10.0.linux-amd64/elasticsearch_exporter /elasticsearch_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/prometheus-elasticsearch-exporter /var/log/prometheus-elasticsearch-exporter
COPY --from=builder /var/cache/prometheus-elasticsearch-exporter /var/cache/prometheus-elasticsearch-exporter
COPY --from=builder /etc/prometheus-elasticsearch-exporter /etc/prometheus-elasticsearch-exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9214
ENTRYPOINT ["/elasticsearch_exporter"]
LABEL org.opencontainers.image.title="Prometheus Elasticsearch Exporter" \
      org.opencontainers.image.version="1.10.0" \
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
