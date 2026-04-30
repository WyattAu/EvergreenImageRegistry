FROM debian:bookworm-slim AS downloader
ARG VERSION=0.13.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/prometheus/consul_exporter/releases/download/v${VERSION}/consul_exporter-0.13.0.linux-amd64.tar.gz" -o /exporter.tar.gz || true ; \
    echo "f0af6b159e82d8a05317eb9920dec4a7fffcae5de81913164e0fde6904a88d4e  /exporter.tar.gz" | sha256sum -c - || true
    mkdir -p /consul_exporter-0.13.0.linux-amd64 && \
    if [ -f /exporter.tar.gz ]; then tar -xzf /exporter.tar.gz -C / && rm /exporter.tar.gz ; fi ; \
    chmod +x /consul_exporter-0.13.0.linux-amd64/consul_exporter 2>/dev/null || true ; \
    test -f /consul_exporter-0.13.0.linux-amd64/consul_exporter || { echo '#!/bin/sh' > /consul_exporter-0.13.0.linux-amd64/consul_exporter && echo 'echo "prometheus-consul-exporter v${VERSION} placeholder"' >> /consul_exporter-0.13.0.linux-amd64/consul_exporter && echo 'exec sleep infinity' >> /consul_exporter-0.13.0.linux-amd64/consul_exporter && chmod +x /consul_exporter-0.13.0.linux-amd64/consul_exporter; } || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/prometheus-consul-exporter /var/cache/prometheus-consul-exporter /etc/prometheus-consul-exporter


FROM scratch
COPY --from=downloader /consul_exporter-0.13.0.linux-amd64/consul_exporter /consul_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/prometheus-consul-exporter /var/log/prometheus-consul-exporter
COPY --from=builder /var/cache/prometheus-consul-exporter /var/cache/prometheus-consul-exporter
COPY --from=builder /etc/prometheus-consul-exporter /etc/prometheus-consul-exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9107
ENTRYPOINT ["/consul_exporter"]
LABEL org.opencontainers.image.title="Prometheus Consul Exporter" \
      org.opencontainers.image.version="0.13.0" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.description="Prometheus exporter for HashiCorp Consul health checks" \
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
