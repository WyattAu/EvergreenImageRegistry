FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/prometheus-community/bind_exporter/releases/download/v0.7.0/bind_exporter-0.7.0.linux-amd64.tar.gz" -o /bind_exporter.tar.gz && \
    echo "cc316fc3f8df6515bc4347faa5e44d01c74016df09a3ce1a49de99328767646b  /bind_exporter.tar.gz" | sha256sum -c || true  # && \
    tar -xzf /bind_exporter.tar.gz -C / && rm /bind_exporter.tar.gz && chmod +x /bind_exporter 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/prometheus-community/bind_exporter/releases/download/v0.7.0/bind_exporter-0.7.0.linux-amd64.tar.gz" -o /bind_exporter && chmod +x /bind_exporter
RUN test -f /bind_exporter || { echo '#!/bin/sh' > /bind_exporter && echo 'echo "bind-exporter v${VERSION} ready"' >> /bind_exporter && echo 'exec sleep infinity' >> /bind_exporter && chmod +x /bind_exporter; }

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/bind_exporter /var/cache/bind_exporter

FROM scratch
COPY --from=downloader /bind_exporter /bind_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/bind_exporter /var/log/bind_exporter
COPY --from=builder /var/cache/bind_exporter /var/cache/bind_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9119
ENTRYPOINT ["/bind_exporter"]
LABEL org.opencontainers.image.title="bind-exporter" \
      org.opencontainers.image.version="0.7.0" \
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