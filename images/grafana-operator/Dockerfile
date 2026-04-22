ARG VERSION=v5.22.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/grafana-operator/grafana-operator/releases/download/v5.22.2/grafana-operator-v5.22.2-linux-amd64" -o /grafana-operator && \
    chmod +x /grafana-operator && strip /grafana-operator

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/grafana-operator /var/cache/grafana-operator

FROM scratch
COPY --from=downloader /grafana-operator /grafana-operator
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/grafana-operator /var/log/grafana-operator
COPY --from=builder /var/cache/grafana-operator /var/cache/grafana-operator
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/grafana-operator", "--version"]
ENTRYPOINT ["/grafana-operator"]
LABEL org.opencontainers.image.title="grafana-operator" \
      org.opencontainers.image.version="5.22.2" \
      org.opencontainers.image.vendor="Grafana" \
      org.opencontainers.image.description="Sovereign hardened grafana-operator - Kubernetes Grafana operator" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s"
