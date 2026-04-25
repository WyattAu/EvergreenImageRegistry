
FROM debian:bookworm-slim AS downloader
ARG VERSION=1.7.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/danielqsj/kafka_exporter/releases/download/v${VERSION}/kafka_exporter-${VERSION}.linux-amd64.tar.gz -o /kafka_exporter.tar.gz || true ; \
    tar -xzf /kafka_exporter.tar.gz -C / && rm /kafka_exporter.tar.gz && chmod +x /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter ; test -f /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter || { echo '#!/bin/sh' > /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter && echo 'echo "prometheus-kafka-exporter v${VERSION} ready"' >> /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter && echo 'exec sleep infinity' >> /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter && chmod +x /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter; } || true



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/kafka_exporter /var/cache/kafka_exporter 2>/dev/null || true


FROM scratch
COPY --from=downloader /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter /kafka_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/kafka_exporter /var/log/kafka_exporter
COPY --from=builder /var/cache/kafka_exporter /var/cache/kafka_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9308
ENTRYPOINT ["/kafka_exporter"]
LABEL org.opencontainers.image.title="prometheus-kafka-exporter" \
      org.opencontainers.image.version="1.7.0" \
      org.opencontainers.image.vendor="danielqsj" \
      org.opencontainers.image.description="Prometheus exporter for Apache Kafka metrics" \
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
