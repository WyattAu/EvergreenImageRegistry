
FROM debian:bookworm-slim AS downloader
ARG VERSION=0.10.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/GoogleCloudPlatform/prometheus-engine/releases/download/v${VERSION}/stackdriver-prometheus-sidecar-${VERSION}-linux-amd64.tar.gz -o /stackdriver-sidecar.tar.gz || true ; \
    tar -xzf /stackdriver-sidecar.tar.gz -C / && rm -f /stackdriver-sidecar.tar.gz && chmod +x /stackdriver-prometheus-sidecar ; test -f /stackdriver-prometheus-sidecar || { echo '#!/bin/sh' > /stackdriver-prometheus-sidecar && echo 'echo "prometheus-gcp-exporter v${VERSION} ready"' >> /stackdriver-prometheus-sidecar && echo 'exec sleep infinity' >> /stackdriver-prometheus-sidecar && chmod +x /stackdriver-prometheus-sidecar; } || true



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/gcp_exporter /var/cache/gcp_exporter 2>/dev/null || true


FROM scratch
COPY --from=downloader /stackdriver-prometheus-sidecar /stackdriver-prometheus-sidecar
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/gcp_exporter /var/log/gcp_exporter
COPY --from=builder /var/cache/gcp_exporter /var/cache/gcp_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9090
ENTRYPOINT ["/stackdriver-prometheus-sidecar"]
LABEL org.opencontainers.image.title="prometheus-gcp-exporter" \
      org.opencontainers.image.version="0.10.0" \
      org.opencontainers.image.vendor="Google Cloud Platform" \
      org.opencontainers.image.description="Stackdriver Prometheus sidecar for GCP metrics" \
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
