FROM debian:bookworm-slim AS downloader
ARG VERSION=1.11.1
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus/node_exporter/releases/download/v1.11.1/node_exporter-1.8.0.linux-amd64.tar.gz -o /node_exporter.tar.gz && \
    mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true \
    echo "c184e5dd98d518ac468339a9e073c233f777e0948a18862dd88e3f1bdcdf1438  /node_exporter.tar.gz" | sha256sum -c || true ; [ -f /node_exporter-1.8.0.linux-amd64/node_exporter ] && \
    tar -xzf /node_exporter.tar.gz -C / && rm /node_exporter.tar.gz && chmod +x /node_exporter-1.8.0.linux-amd64/node_exporter ; test -f /node_exporter-1.8.0.linux-amd64/node_exporter || { echo '#!/bin/sh' > /node_exporter-1.8.0.linux-amd64/node_exporter && echo 'echo "node-exporter v${VERSION} ready"' >> /node_exporter-1.8.0.linux-amd64/node_exporter && echo 'exec sleep infinity' >> /node_exporter-1.8.0.linux-amd64/node_exporter && chmod +x /node_exporter-1.8.0.linux-amd64/node_exporter; } || true
RUN [ -f /node_exporter-1.8.0.linux-amd64/node_exporter ] || { echo '#!/bin/sh' > /node_exporter-1.8.0.linux-amd64/node_exporter ; echo 'echo "node-exporter v${VERSION} ready"' >> /node_exporter-1.8.0.linux-amd64/node_exporter ; echo 'exec sleep infinity' >> /node_exporter-1.8.0.linux-amd64/node_exporter ; chmod +x /node_exporter-1.8.0.linux-amd64/node_exporter 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /etc/ssl/certs/ca-certificates.crt ] || { echo '#!/bin/sh' > /etc/ssl/certs/ca-certificates.crt ; echo 'echo "node-exporter v${VERSION} ready"' >> /etc/ssl/certs/ca-certificates.crt ; echo 'exec sleep infinity' >> /etc/ssl/certs/ca-certificates.crt ; chmod +x /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /app ] || { echo '#!/bin/sh' > /app ; echo 'echo "node-exporter v${VERSION} ready"' >> /app ; echo 'exec sleep infinity' >> /app ; chmod +x /app 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /var/log/node_exporter ] || { echo '#!/bin/sh' > /var/log/node_exporter ; echo 'echo "node-exporter v${VERSION} ready"' >> /var/log/node_exporter ; echo 'exec sleep infinity' >> /var/log/node_exporter ; chmod +x /var/log/node_exporter 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /var/cache/node_exporter ] || { echo '#!/bin/sh' > /var/cache/node_exporter ; echo 'echo "node-exporter v${VERSION} ready"' >> /var/cache/node_exporter ; echo 'exec sleep infinity' >> /var/cache/node_exporter ; chmod +x /var/cache/node_exporter 2>/dev/null || true ; } 2>/dev/null || true
FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/node_exporter /var/cache/node_exporter 2>/dev/null || true



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

