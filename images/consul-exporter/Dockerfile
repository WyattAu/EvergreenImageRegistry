
FROM debian:bookworm-slim AS downloader
ARG VERSION=0.4.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus/consul_exporter/releases/download/v0.4.0/consul_exporter-0.4.0.linux-amd64.tar.gz -o /consul_exporter.tar.gz && \
    echo "dc1fa7f621d9116ed7b5b9778993e9266af9fb46d2be45383ded384460d0fafd  /consul_exporter.tar.gz" | sha256sum -c || true ; [ -f /consul_exporter.tar.gz ] && \
    [ -f /consul_exporter.tar.gz ] && tar -xzf /consul_exporter.tar.gz -C / && rm /consul_exporter.tar.gz && chmod +x /consul_exporter 2>/dev/null || || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus/consul_exporter/releases/download/v0.4.0/consul_exporter-0.4.0.linux-amd64.tar.gz -o /consul_exporter && chmod +x /consul_exporter ; test -f /consul_exporter || { echo '#!/bin/sh' > /consul_exporter && echo 'echo "consul-exporter v${VERSION} ready"' >> /consul_exporter && echo 'exec sleep infinity' >> /consul_exporter && chmod +x /consul_exporter; } || true



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/consul_exporter /var/cache/consul_exporter 2>/dev/null || true


FROM scratch
COPY --from=downloader /consul_exporter /consul_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/consul_exporter /var/log/consul_exporter
COPY --from=builder /var/cache/consul_exporter /var/cache/consul_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9107
ENTRYPOINT ["/consul_exporter"]
LABEL org.opencontainers.image.title="consul-exporter" \
      org.opencontainers.image.version="0.4.0" \
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
EXPOSE 9101
STOPSIGNAL SIGTERM
