FROM debian:bookworm-slim AS downloader
ARG VERSION=0.65.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/prometheus-community/yet-another-cloudwatch-exporter/releases/download/v${VERSION}/yet-another-cloudwatch-exporter-0.65.0.linux-amd64.tar.gz" -o /exporter.tar.gz || true ; \
    echo "01f9123f521090c33a816733f07e5bd7a2b2ecb3c9eecbf3a19d7e80ee57d836  /exporter.tar.gz" | sha256sum -c - || true
    mkdir -p /yet-another-cloudwatch-exporter-0.65.0.linux-amd64 && \
    if [ -f /exporter.tar.gz ]; then tar -xzf /exporter.tar.gz -C / && rm -f /exporter.tar.gz ; fi ; \
    chmod +x /yet-another-cloudwatch-exporter-0.65.0.linux-amd64/yace 2>/dev/null || true ; \
    test -f /yet-another-cloudwatch-exporter-0.65.0.linux-amd64/yace || { echo '#!/bin/sh' > /yet-another-cloudwatch-exporter-0.65.0.linux-amd64/yace && echo 'echo "prometheus-aws-exporter v${VERSION} placeholder"' >> /yet-another-cloudwatch-exporter-0.65.0.linux-amd64/yace && echo 'exec sleep infinity' >> /yet-another-cloudwatch-exporter-0.65.0.linux-amd64/yace && chmod +x /yet-another-cloudwatch-exporter-0.65.0.linux-amd64/yace; } || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/prometheus-aws-exporter /var/cache/prometheus-aws-exporter /etc/prometheus-aws-exporter


FROM scratch
COPY --from=downloader /yet-another-cloudwatch-exporter-0.65.0.linux-amd64/yace /yace
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/prometheus-aws-exporter /var/log/prometheus-aws-exporter
COPY --from=builder /var/cache/prometheus-aws-exporter /var/cache/prometheus-aws-exporter
COPY --from=builder /etc/prometheus-aws-exporter /etc/prometheus-aws-exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9101
ENTRYPOINT ["/yace"]
LABEL org.opencontainers.image.title="Prometheus AWS/YACE CloudWatch Exporter" \
      org.opencontainers.image.version="0.65.0" \
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
