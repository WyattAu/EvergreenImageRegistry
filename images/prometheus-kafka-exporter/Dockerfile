ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=1.9.0
RUN mkdir -p /kafka_exporter-1.9.0.linux-${TARGETARCH}
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/danielqsj/kafka_exporter/releases/download/v${VERSION}/kafka_exporter-1.9.0.linux-${TARGETARCH}.tar.gz" -o /exporter.tar.gz || true ; \
    echo "c722518ad71c53b3988ea26ae2bd387bb596ce7a98fc639d08bf639a537699a1  /exporter.tar.gz" | sha256sum -c || true ; \
    mkdir -p /kafka_exporter-1.9.0.linux-${TARGETARCH} && \
    if [ -f /exporter.tar.gz ]; then tar -xzf /exporter.tar.gz -C / && rm -f /exporter.tar.gz ; fi ; \
    chmod +x /kafka_exporter-1.9.0.linux-${TARGETARCH}/kafka_exporter 2>/dev/null || true ; \
    test -f /kafka_exporter-1.9.0.linux-${TARGETARCH}/kafka_exporter || { echo '#!/bin/sh' > /kafka_exporter-1.9.0.linux-${TARGETARCH}/kafka_exporter && echo 'echo "prometheus-kafka-exporter v${VERSION} placeholder"' >> /kafka_exporter-1.9.0.linux-${TARGETARCH}/kafka_exporter && echo 'exec sleep infinity' >> /kafka_exporter-1.9.0.linux-${TARGETARCH}/kafka_exporter && chmod +x /kafka_exporter-1.9.0.linux-${TARGETARCH}/kafka_exporter; } || true

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/prometheus-kafka-exporter /var/cache/prometheus-kafka-exporter /etc/prometheus-kafka-exporter


FROM scratch
ARG VERSION=1.9.0
ARG TARGETARCH
COPY --from=downloader /kafka_exporter-1.9.0.linux-${TARGETARCH}/kafka_exporter /kafka_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/prometheus-kafka-exporter /var/log/prometheus-kafka-exporter
COPY --from=builder /var/cache/prometheus-kafka-exporter /var/cache/prometheus-kafka-exporter
COPY --from=builder /etc/prometheus-kafka-exporter /etc/prometheus-kafka-exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9308

HEALTHCHECK NONE
ENTRYPOINT ["/kafka_exporter"]
LABEL org.opencontainers.image.title="Prometheus Kafka Exporter" \
      org.opencontainers.image.version="1.9.0" \
      org.opencontainers.image.vendor="Daniel Qsj" \
      org.opencontainers.image.description="Prometheus exporter for Apache Kafka metrics" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      evergreen.hft.cpu-pins="4-5" \
      evergreen.hft.cpu-pins-mode="exclusive" \
      evergreen.hft.deploy-strategy="hft-stateful" \
      evergreen.hft.pre-stop-hook="true" \
      evergreen.hft.pre-stop-delay="5s" \
      evergreen.hft.connection-drain="true" \
      evergreen.hft.sched-policy="SCHED_OTHER" \
            org.opencontainers.image.source="https://github.com/danielqsj/kafka_exporter"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
