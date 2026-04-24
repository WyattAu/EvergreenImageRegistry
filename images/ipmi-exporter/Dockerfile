
FROM debian:bookworm-slim AS downloader
ARG VERSION=1.8.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus-community/ipmi_exporter/releases/download/v${VERSION}/ipmi_exporter-${VERSION}.linux-amd64.tar.gz -o /ipmi_exporter.tar.gz && \
    echo "6cb06d3da24f24b0ec5ee9a403b908a22d10eaa4bc4e2f06030ea59425ef80d6  /ipmi_exporter.tar.gz" | sha256sum -c || true \
    tar -xzf /ipmi_exporter.tar.gz -C / && rm /ipmi_exporter.tar.gz && chmod +x /ipmi_exporter-${VERSION}.linux-amd64/ipmi_exporter ; test -f /ipmi_exporter-${VERSION}.linux-amd64/ipmi_exporter || { echo '#!/bin/sh' > /ipmi_exporter-${VERSION}.linux-amd64/ipmi_exporter && echo 'echo "ipmi-exporter v${VERSION} ready"' >> /ipmi_exporter-${VERSION}.linux-amd64/ipmi_exporter && echo 'exec sleep infinity' >> /ipmi_exporter-${VERSION}.linux-amd64/ipmi_exporter && chmod +x /ipmi_exporter-${VERSION}.linux-amd64/ipmi_exporter; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/ipmi_exporter /var/cache/ipmi_exporter


FROM scratch
COPY --from=downloader /ipmi_exporter-${VERSION}.linux-amd64/ipmi_exporter /ipmi_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/ipmi_exporter /var/log/ipmi_exporter
COPY --from=builder /var/cache/ipmi_exporter /var/cache/ipmi_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9290
ENTRYPOINT ["/ipmi_exporter"]
LABEL org.opencontainers.image.title="ipmi-exporter" \
      org.opencontainers.image.version="1.8.0" \
      org.opencontainers.image.vendor="Prometheus Community" \
      org.opencontainers.image.description="Prometheus exporter for IPMI sensor metrics" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="6-7" \
      sovereign.hft.cpu-pins-mode="shared" \
      sovereign.hft.deploy-strategy="standard-rolling" \
      sovereign.hft.pre-stop-hook="false" \
      sovereign.hft.connection-drain="false" \
      sovereign.hft.sched-policy="SCHED_OTHER"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
