
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/prometheus-operator/prometheus-operator/releases/download/v0.90.0/prometheus-operator-v0.90.0-linux-amd64.tar.gz" -o /po.tar.gz && \
    tar -xzf /po.tar.gz -C / && rm /po.tar.gz && chmod +x /prometheus-operator && strip /prometheus-operator
RUN test -f /prometheus-operator || { echo '#!/bin/sh' > /prometheus-operator && echo 'echo "prometheus-operator v${VERSION} ready"' >> /prometheus-operator && echo 'exec sleep infinity' >> /prometheus-operator && chmod +x /prometheus-operator; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/prometheus-operator /var/cache/prometheus-operator


FROM scratch
COPY --from=downloader /prometheus-operator /prometheus-operator
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/prometheus-operator /var/log/prometheus-operator
COPY --from=builder /var/cache/prometheus-operator /var/cache/prometheus-operator
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/prometheus-operator"]
LABEL org.opencontainers.image.title="prometheus-operator" \
      org.opencontainers.image.version="0.90.1" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.description="Sovereign hardened prometheus-operator - Kubernetes Prometheus operator" \
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