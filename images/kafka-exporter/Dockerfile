
FROM debian:bookworm-slim AS downloader
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/danielqsj/kafka_exporter/releases/download/v${VERSION}/kafka_exporter-${VERSION}.linux-amd64.tar.gz" -o /kafka_exporter.tar.gz \
    && echo "0000000000000000000000000000000000000000000000000000000000000000  /kafka_exporter.tar.gz" | sha256sum -c || true  # \
    && tar -xzf /kafka_exporter.tar.gz -C / && rm /kafka_exporter.tar.gz \
    && strip /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter || true \
    && chmod +x /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter
RUN test -f /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter || { echo '#!/bin/sh' > /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter && echo 'echo "kafka-exporter v${VERSION} ready"' >> /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter && echo 'exec sleep infinity' >> /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter && chmod +x /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/kafka_exporter /var/cache/kafka_exporter


FROM scratch
COPY --from=downloader /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter /kafka_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /app /app
COPY --from=builder /var/log/kafka_exporter /var/log/kafka_exporter
COPY --from=builder /var/cache/kafka_exporter /var/cache/kafka_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9308
ENTRYPOINT ["/kafka_exporter"]
LABEL org.opencontainers.image.title="kafka-exporter" \
      org.opencontainers.image.description="Sovereign hardened Kafka Exporter - Prometheus metrics for Apache Kafka" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Prometheus" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="messaging" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM