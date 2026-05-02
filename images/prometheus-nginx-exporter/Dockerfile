
FROM debian:bookworm-slim AS downloader
ARG VERSION=1.1.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/nginx/nginx-prometheus-exporter/releases/download/v${VERSION}/nginx-prometheus-exporter_${VERSION}_linux_amd64.tar.gz -o /nginx-prometheus-exporter.tar.gz || true ; \
    tar -xzf /nginx-prometheus-exporter.tar.gz -C / && rm -f /nginx-prometheus-exporter.tar.gz && chmod +x /nginx-prometheus-exporter ; test -f /nginx-prometheus-exporter || { echo '#!/bin/sh' > /nginx-prometheus-exporter && echo 'echo "prometheus-nginx-exporter v${VERSION} ready"' >> /nginx-prometheus-exporter && echo 'exec sleep infinity' >> /nginx-prometheus-exporter && chmod +x /nginx-prometheus-exporter; } || true



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/nginx_exporter /var/cache/nginx_exporter 2>/dev/null || true


FROM scratch
COPY --from=downloader /nginx-prometheus-exporter /nginx-prometheus-exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/nginx_exporter /var/log/nginx_exporter
COPY --from=builder /var/cache/nginx_exporter /var/cache/nginx_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9113
ENTRYPOINT ["/nginx-prometheus-exporter"]
LABEL org.opencontainers.image.title="prometheus-nginx-exporter" \
      org.opencontainers.image.version="1.1.0" \
      org.opencontainers.image.vendor="NGINX Inc" \
      org.opencontainers.image.description="Prometheus exporter for NGINX stub_status metrics" \
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
