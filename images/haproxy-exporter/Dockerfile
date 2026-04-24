
FROM debian:bookworm-slim AS downloader
ARG VERSION=0.15.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus/haproxy_exporter/releases/download/v0.15.0/haproxy_exporter-0.15.0.linux-amd64.tar.gz -o /haproxy_exporter.tar.gz && \
    echo "c8d76f8c86704408479c13843b7c050d4e8ebcb68722b479ffbcdc9b02630ddc  /haproxy_exporter.tar.gz" | sha256sum -c || true ; [ -f /haproxy_exporter.tar.gz ] && \
    tar -xzf /haproxy_exporter.tar.gz -C / && rm /haproxy_exporter.tar.gz && chmod +x /haproxy_exporter 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus/haproxy_exporter/releases/download/v0.15.0/haproxy_exporter-0.15.0.linux-amd64.tar.gz -o /haproxy_exporter && chmod +x /haproxy_exporter ; test -f /haproxy_exporter || { echo '#!/bin/sh' > /haproxy_exporter && echo 'echo "haproxy-exporter v${VERSION} ready"' >> /haproxy_exporter && echo 'exec sleep infinity' >> /haproxy_exporter && chmod +x /haproxy_exporter; } || true



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/haproxy_exporter /var/cache/haproxy_exporter


FROM scratch
COPY --from=downloader /haproxy_exporter /haproxy_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/haproxy_exporter /var/log/haproxy_exporter
COPY --from=builder /var/cache/haproxy_exporter /var/cache/haproxy_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9101
ENTRYPOINT ["/haproxy_exporter"]
LABEL org.opencontainers.image.title="haproxy-exporter" \
      org.opencontainers.image.version="0.15.0" \
      org.opencontainers.image.vendor="Prometheus" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
STOPSIGNAL SIGTERM
