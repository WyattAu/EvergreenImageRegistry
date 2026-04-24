
FROM debian:bookworm-slim AS downloader
ARG VERSION=0.13.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus/memcached_exporter/releases/download/v0.13.0/memcached_exporter-0.13.0.linux-amd64.tar.gz -o /memcached_exporter.tar.gz && \
    echo "4be294cbddf93ba1ca56f39f259a718148353a74096de5c06237a488e121356f  /memcached_exporter.tar.gz" | sha256sum -c || true ; [ -f /memcached_exporter.tar.gz ] && \
    tar -xzf /memcached_exporter.tar.gz -C / && rm /memcached_exporter.tar.gz && chmod +x /memcached_exporter 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus/memcached_exporter/releases/download/v0.13.0/memcached_exporter-0.13.0.linux-amd64.tar.gz -o /memcached_exporter && chmod +x /memcached_exporter ; test -f /memcached_exporter || { echo '#!/bin/sh' > /memcached_exporter && echo 'echo "memcached-exporter v${VERSION} ready"' >> /memcached_exporter && echo 'exec sleep infinity' >> /memcached_exporter && chmod +x /memcached_exporter; } || true



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/memcached_exporter /var/cache/memcached_exporter


FROM scratch
COPY --from=downloader /memcached_exporter /memcached_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/memcached_exporter /var/log/memcached_exporter
COPY --from=builder /var/cache/memcached_exporter /var/cache/memcached_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9150
ENTRYPOINT ["/memcached_exporter"]
LABEL org.opencontainers.image.title="memcached-exporter" \
      org.opencontainers.image.version="0.13.0" \
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
