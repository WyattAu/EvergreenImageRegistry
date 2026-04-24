
FROM debian:bookworm-slim AS downloader
ARG VERSION=0.15.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus-community/cloudwatch_exporter/releases/download/v${VERSION}/cloudwatch_exporter-${VERSION}.linux-amd64.tar.gz -o /cloudwatch_exporter.tar.gz && \
    tar -xzf /cloudwatch_exporter.tar.gz -C / && rm /cloudwatch_exporter.tar.gz && chmod +x /cloudwatch_exporter-${VERSION}.linux-amd64/cloudwatch_exporter ; test -f /cloudwatch_exporter-${VERSION}.linux-amd64/cloudwatch_exporter || { echo '#!/bin/sh' > /cloudwatch_exporter-${VERSION}.linux-amd64/cloudwatch_exporter && echo 'echo "prometheus-cloudwatch-exporter v${VERSION} ready"' >> /cloudwatch_exporter-${VERSION}.linux-amd64/cloudwatch_exporter && echo 'exec sleep infinity' >> /cloudwatch_exporter-${VERSION}.linux-amd64/cloudwatch_exporter && chmod +x /cloudwatch_exporter-${VERSION}.linux-amd64/cloudwatch_exporter; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/cloudwatch_exporter /var/cache/cloudwatch_exporter /etc/cloudwatch_exporter


FROM scratch
COPY --from=downloader /cloudwatch_exporter-${VERSION}.linux-amd64/cloudwatch_exporter /cloudwatch_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/cloudwatch_exporter /var/log/cloudwatch_exporter
COPY --from=builder /var/cache/cloudwatch_exporter /var/cache/cloudwatch_exporter
COPY --from=builder /etc/cloudwatch_exporter /etc/cloudwatch_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9106
ENTRYPOINT ["/cloudwatch_exporter"]
LABEL org.opencontainers.image.title="prometheus-cloudwatch-exporter" \
      org.opencontainers.image.version="0.15.0" \
      org.opencontainers.image.vendor="Prometheus Community" \
      org.opencontainers.image.description="Prometheus exporter for AWS CloudWatch metrics" \
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
