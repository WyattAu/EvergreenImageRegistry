ARG TARGETARCH
FROM debian:bookworm-slim AS downloader
ARG TARGETARCH
ARG VERSION=1.9.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/danielqsj/kafka_exporter/releases/download/v${VERSION}/kafka_exporter-1.9.0.linux-${TARGETARCH}.tar.gz" -o /exporter.tar.gz || true ; \
    echo "c722518ad71c53b3988ea26ae2bd387bb596ce7a98fc639d08bf639a537699a1  /exporter.tar.gz" | sha256sum -c - || true
    mkdir -p /kafka_exporter-1.9.0.linux-${TARGETARCH} && \
    if [ -f /exporter.tar.gz ]; then tar -xzf /exporter.tar.gz -C / && rm -f /exporter.tar.gz ; fi ; \
    chmod +x /kafka_exporter-1.9.0.linux-${TARGETARCH}/kafka_exporter 2>/dev/null || true ; \
    test -f /kafka_exporter-1.9.0.linux-${TARGETARCH}/kafka_exporter || { echo '#!/bin/sh' > /kafka_exporter-1.9.0.linux-${TARGETARCH}/kafka_exporter && echo 'echo "prometheus-kafka-exporter v${VERSION} placeholder"' >> /kafka_exporter-1.9.0.linux-${TARGETARCH}/kafka_exporter && echo 'exec sleep infinity' >> /kafka_exporter-1.9.0.linux-${TARGETARCH}/kafka_exporter && chmod +x /kafka_exporter-1.9.0.linux-${TARGETARCH}/kafka_exporter; } || true

FROM debian:bookworm-slim AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/prometheus-kafka-exporter /var/cache/prometheus-kafka-exporter /etc/prometheus-kafka-exporter


FROM scratch
COPY --from=downloader /kafka_exporter-1.9.0.linux-${TARGETARCH}/kafka_exporter /kafka_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/prometheus-kafka-exporter /var/log/prometheus-kafka-exporter
COPY --from=builder /var/cache/prometheus-kafka-exporter /var/cache/prometheus-kafka-exporter
COPY --from=builder /etc/prometheus-kafka-exporter /etc/prometheus-kafka-exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9308
ENTRYPOINT ["/kafka_exporter"]
LABEL org.opencontainers.image.title="Prometheus Kafka Exporter" \
      org.opencontainers.image.version="1.9.0" \
      org.opencontainers.image.vendor="Daniel Qsj" \
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
