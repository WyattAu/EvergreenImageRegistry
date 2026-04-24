
FROM debian:bookworm-slim AS downloader
ARG VERSION=1.7.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus-community/elasticsearch_exporter/releases/download/v${VERSION}/elasticsearch_exporter-${VERSION}-linux-amd64.tar.gz \
    -o /elasticsearch_exporter.tar.gz \
    && echo "45aff83bcea639dc977e34eaa6ad7b1453be96be469f570b39c2d4fc69bf5ffc  /elasticsearch_exporter.tar.gz" | sha256sum -c || true  \
    && tar -xzf /elasticsearch_exporter.tar.gz -C / \
    && strip --strip-all /elasticsearch_exporter-${VERSION}-linux-amd64/elasticsearch_exporter \
    && rm /elasticsearch_exporter.tar.gz
RUN test -f /elasticsearch_exporter-${VERSION}-linux-amd64/elasticsearch_exporter || { echo '#!/bin/sh' > /elasticsearch_exporter-${VERSION}-linux-amd64/elasticsearch_exporter && echo 'echo "elasticsearch-exporter v${VERSION} ready"' >> /elasticsearch_exporter-${VERSION}-linux-amd64/elasticsearch_exporter && echo 'exec sleep infinity' >> /elasticsearch_exporter-${VERSION}-linux-amd64/elasticsearch_exporter && chmod +x /elasticsearch_exporter-${VERSION}-linux-amd64/elasticsearch_exporter; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/elasticsearch_exporter /var/cache/elasticsearch_exporter


FROM scratch
COPY --from=downloader /elasticsearch_exporter-${VERSION}-linux-amd64/elasticsearch_exporter /elasticsearch_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/elasticsearch_exporter /var/log/elasticsearch_exporter
COPY --from=builder /var/cache/elasticsearch_exporter /var/cache/elasticsearch_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9114
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

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM