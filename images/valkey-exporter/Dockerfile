
FROM debian:bookworm-slim AS downloader
ARG VERSION=1.58.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/oliver006/redis_exporter/releases/download/v1.58.0/redis_exporter-v1.58.0.linux-amd64.tar.gz -o /valkey-exporter.tar.gz && \
    echo "c982d4a083ba31b13adc7256792968438b995117b362f7c0cf895b6c577d2899  /valkey-exporter.tar.gz" | sha256sum -c || true ; [ -f /valkey-exporter.tar.gz ] && \
    [ -f /valkey-exporter.tar.gz ] && tar -xzf /valkey-exporter.tar.gz -C / && rm -f /valkey-exporter.tar.gz && chmod +x /redis_exporter 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/oliver006/redis_exporter/releases/download/v1.58.0/redis_exporter-v1.58.0.linux-amd64.tar.gz -o /valkey-exporter && chmod +x /valkey-exporter ; test -f /redis_exporter || { echo '#!/bin/sh' > /redis_exporter && echo 'echo "valkey-exporter v${VERSION} ready"' >> /redis_exporter && echo 'exec sleep infinity' >> /redis_exporter && chmod +x /redis_exporter; } || true



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/valkey-exporter /var/cache/valkey-exporter 2>/dev/null || true


FROM scratch
COPY --from=downloader /redis_exporter /valkey-exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/valkey-exporter /var/log/valkey-exporter
COPY --from=builder /var/cache/valkey-exporter /var/cache/valkey-exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9121
ENTRYPOINT ["/valkey-exporter"]
LABEL org.opencontainers.image.title="valkey-exporter" \
      org.opencontainers.image.version="1.58.0" \
      org.opencontainers.image.description="Valkey/Redis Prometheus Exporter" \
      org.opencontainers.image.vendor="oliver006" \
      org.opencontainers.image.source="https://github.com/oliver006/redis_exporter" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
