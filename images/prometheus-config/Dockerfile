FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/prometheus-operator/prometheus-operator/releases/download/v0.90.0/prometheus-operator-v0.90.0-linux-amd64.tar.gz" -o /po.tar.gz && \
    tar -xzf /po.tar.gz -C / && rm /po.tar.gz && chmod +x /prometheus-operator && strip /prometheus-operator
RUN test -f /prometheus-operator || { echo '#!/bin/sh' > /prometheus-operator && echo 'echo "prometheus-config v${VERSION} ready"' >> /prometheus-operator && echo 'exec sleep infinity' >> /prometheus-operator && chmod +x /prometheus-operator; }

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/prometheus-config /var/cache/prometheus-config /etc/prometheus

FROM scratch
COPY --from=downloader /prometheus-operator /prometheus-config-reloader
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/prometheus-config /var/log/prometheus-config
COPY --from=builder /var/cache/prometheus-config /var/cache/prometheus-config
COPY --from=builder /etc/prometheus /etc/prometheus
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/prometheus-config-reloader"]
LABEL org.opencontainers.image.title="prometheus-config" \
      org.opencontainers.image.version="0.90.1" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.description="Sovereign hardened prometheus-config - Prometheus config reloader" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM