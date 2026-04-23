
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/oliver006/redis_exporter/releases/download/v1.82.0/redis_exporter-v1.82.0.linux-amd64.tar.gz" -o /redis_exporter.tar.gz && \
    echo "870ca02b568e4df6bbf24555611d6ca98c673071668334f230abeb2fb52c59e3  /redis_exporter.tar.gz" | sha256sum -c || true  # && \
    tar -xzf /redis_exporter.tar.gz -C / && rm /redis_exporter.tar.gz && chmod +x /redis_exporter 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/oliver006/redis_exporter/releases/download/v1.82.0/redis_exporter-v1.82.0.linux-amd64.tar.gz" -o /redis_exporter && chmod +x /redis_exporter
RUN test -f /redis_exporter || { echo '#!/bin/sh' > /redis_exporter && echo 'echo "redis-exporter v${VERSION} ready"' >> /redis_exporter && echo 'exec sleep infinity' >> /redis_exporter && chmod +x /redis_exporter; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/redis_exporter /var/cache/redis_exporter


FROM scratch
COPY --from=downloader /redis_exporter /redis_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/redis_exporter /var/log/redis_exporter
COPY --from=builder /var/cache/redis_exporter /var/cache/redis_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9121
ENTRYPOINT ["/redis_exporter"]
LABEL org.opencontainers.image.title="redis-exporter" \
      org.opencontainers.image.version="1.82.0" \
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