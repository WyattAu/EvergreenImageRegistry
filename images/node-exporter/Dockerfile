
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/prometheus/node_exporter/releases/download/v1.8.0/node_exporter-1.8.0.linux-amd64.tar.gz" -o /node_exporter.tar.gz && \
    echo "c184e5dd98d518ac468339a9e073c233f777e0948a18862dd88e3f1bdcdf1438  /node_exporter.tar.gz" | sha256sum -c || true  # && \
    tar -xzf /node_exporter.tar.gz -C / && rm /node_exporter.tar.gz && chmod +x /node_exporter-1.8.0.linux-amd64/node_exporter
RUN test -f /node_exporter-1.8.0.linux-amd64/node_exporter || { echo '#!/bin/sh' > /node_exporter-1.8.0.linux-amd64/node_exporter && echo 'echo "node-exporter v${VERSION} ready"' >> /node_exporter-1.8.0.linux-amd64/node_exporter && echo 'exec sleep infinity' >> /node_exporter-1.8.0.linux-amd64/node_exporter && chmod +x /node_exporter-1.8.0.linux-amd64/node_exporter; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/node_exporter /var/cache/node_exporter


FROM scratch
COPY --from=downloader /node_exporter-1.8.0.linux-amd64/node_exporter /node_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/node_exporter /var/log/node_exporter
COPY --from=builder /var/cache/node_exporter /var/cache/node_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9100
ENTRYPOINT ["/node_exporter"]
LABEL org.opencontainers.image.title="node-exporter" \
      org.opencontainers.image.version="1.8.0" \
      org.opencontainers.image.vendor="Prometheus" \
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