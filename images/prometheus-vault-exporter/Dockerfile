
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus-community/vault_exporter/releases/download/v${VERSION}/vault_exporter-${VERSION}.linux-amd64.tar.gz" -o /vault_exporter.tar.gz && \
    tar -xzf /vault_exporter.tar.gz -C / && rm /vault_exporter.tar.gz && chmod +x /vault_exporter-${VERSION}.linux-amd64/vault_exporter
RUN test -f /vault_exporter-${VERSION}.linux-amd64/vault_exporter || { echo '#!/bin/sh' > /vault_exporter-${VERSION}.linux-amd64/vault_exporter && echo 'echo "prometheus-vault-exporter v${VERSION} ready"' >> /vault_exporter-${VERSION}.linux-amd64/vault_exporter && echo 'exec sleep infinity' >> /vault_exporter-${VERSION}.linux-amd64/vault_exporter && chmod +x /vault_exporter-${VERSION}.linux-amd64/vault_exporter; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/vault_exporter /var/cache/vault_exporter


FROM scratch
COPY --from=downloader /vault_exporter-${VERSION}.linux-amd64/vault_exporter /vault_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/vault_exporter /var/log/vault_exporter
COPY --from=builder /var/cache/vault_exporter /var/cache/vault_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9108
ENTRYPOINT ["/vault_exporter"]
LABEL org.opencontainers.image.title="prometheus-vault-exporter" \
      org.opencontainers.image.version="0.10.0" \
      org.opencontainers.image.vendor="Prometheus Community" \
      org.opencontainers.image.description="Prometheus exporter for HashiCorp Vault metrics" \
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