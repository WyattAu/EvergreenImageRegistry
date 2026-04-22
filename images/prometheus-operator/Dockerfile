ARG VERSION=v0.90.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/prometheus-operator/prometheus-operator/releases/download/v0.90.0/prometheus-operator-v0.90.0-linux-amd64.tar.gz" -o /po.tar.gz && \
    tar -xzf /po.tar.gz -C / && rm /po.tar.gz && chmod +x /prometheus-operator && strip /prometheus-operator

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/prometheus-operator /var/cache/prometheus-operator

FROM scratch
COPY --from=downloader /prometheus-operator /prometheus-operator
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/prometheus-operator /var/log/prometheus-operator
COPY --from=builder /var/cache/prometheus-operator /var/cache/prometheus-operator
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/prometheus-operator", "--version"]
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
