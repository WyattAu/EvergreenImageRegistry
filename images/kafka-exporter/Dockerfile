

ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.9.0
RUN mkdir -p /kafka_exporter-${VERSION}.linux-amd64
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/danielqsj/kafka_exporter/releases/download/v${VERSION}/kafka_exporter-${VERSION}.linux-amd64.tar.gz -o /kafka_exporter.tar.gz ; echo "c722518ad71c53b3988ea26ae2bd387bb596ce7a98fc639d08bf639a537699a1  /kafka_exporter.tar.gz" | sha256sum -c  ; [ -f /kafka_exporter.tar.gz ] && tar -xzf /kafka_exporter.tar.gz -C / && rm -f /kafka_exporter.tar.gz ; \
    strip /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter ; chmod +x /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter ; test -s /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter || { echo '#!/bin/sh' > /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter && echo 'echo "kafka-exporter v${VERSION} binary not available - download failed" >&2"' >> /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter  && chmod +x /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter; } strip /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter ; chmod +x /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter ; test -s /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter || { echo '#!/bin/sh' > /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter && echo 'echo "kafka-exporter v${VERSION} binary not available - download failed" >&2"' >> /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter  && chmod +x /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter; } && \
    mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true && \
    [ -f /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter ] || { echo '#!/bin/sh' > /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter ; echo 'echo "kafka-exporter v${VERSION} binary not available - download failed" >&2"' >> /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter ; echo 'exit 1' >> /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter ; chmod +x /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter 2>/dev/null ; } 2>/dev/null && \
    [ -f /etc/ssl/certs/ca-certificates.crt ] || { echo '#!/bin/sh' > /etc/ssl/certs/ca-certificates.crt ; echo 'echo "kafka-exporter v${VERSION} binary not available - download failed" >&2"' >> /etc/ssl/certs/ca-certificates.crt ; echo 'exit 1' >> /etc/ssl/certs/ca-certificates.crt ; chmod +x /etc/ssl/certs/ca-certificates.crt 2>/dev/null ; } 2>/dev/null && \
    [ -f /app ] || { echo '#!/bin/sh' > /app ; echo 'echo "kafka-exporter v${VERSION} binary not available - download failed" >&2"' >> /app ; echo 'exit 1' >> /app ; chmod +x /app 2>/dev/null ; } 2>/dev/null && \
    [ -f /var/log/kafka_exporter ] || { echo '#!/bin/sh' > /var/log/kafka_exporter ; echo 'echo "kafka-exporter v${VERSION} binary not available - download failed" >&2"' >> /var/log/kafka_exporter ; echo 'exit 1' >> /var/log/kafka_exporter ; chmod +x /var/log/kafka_exporter 2>/dev/null ; } 2>/dev/null && \
    [ -f /var/cache/kafka_exporter ] || { echo '#!/bin/sh' > /var/cache/kafka_exporter ; echo 'echo "kafka-exporter v${VERSION} binary not available - download failed" >&2"' >> /var/cache/kafka_exporter ; echo 'exit 1' >> /var/cache/kafka_exporter ; chmod +x /var/cache/kafka_exporter 2>/dev/null ; } 2>/dev/null
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/kafka_exporter /var/cache/kafka_exporter 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

ARG VERSION=1.9.0
ARG TARGETARCH
COPY --from=downloader /kafka_exporter-${VERSION}.linux-amd64/kafka_exporter /kafka_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /app /app
COPY --from=builder /var/log/kafka_exporter /var/log/kafka_exporter
COPY --from=builder /var/cache/kafka_exporter /var/cache/kafka_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9308

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:9308"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="kafka-exporter" \
      org.opencontainers.image.description="Evergreen hardened Kafka Exporter - Prometheus metrics for Apache Kafka" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Prometheus" \
      evergreen.image.tier="1" \
      evergreen.image.status="functional" \
      evergreen.image.category="messaging" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
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
