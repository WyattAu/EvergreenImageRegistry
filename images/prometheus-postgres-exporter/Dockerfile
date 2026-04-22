# =============================================================================
# SOVEREIGN HARDENED PROMETHEUS POSTGRES EXPORTER
# Version: 0.15.0
# Constraint: scratch - purest form, no shell, no package manager
# =============================================================================

ARG VERSION=0.15.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/prometheus-community/postgres_exporter/releases/download/v${VERSION}/postgres_exporter-${VERSION}.linux-amd64.tar.gz" -o /postgres_exporter.tar.gz && \
    echo "cb89fc5bf4485fb554e0d640d9684fae143a4b2d5fa443009bd29c59f9129e84  /postgres_exporter.tar.gz" | sha256sum -c - && \
    tar -xzf /postgres_exporter.tar.gz -C / && rm /postgres_exporter.tar.gz && chmod +x /postgres_exporter-${VERSION}.linux-amd64/postgres_exporter

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/postgres_exporter /var/cache/postgres_exporter

FROM scratch
COPY --from=downloader /postgres_exporter-${VERSION}.linux-amd64/postgres_exporter /postgres_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/postgres_exporter /var/log/postgres_exporter
COPY --from=builder /var/cache/postgres_exporter /var/cache/postgres_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9187
ENTRYPOINT ["/postgres_exporter"]
LABEL org.opencontainers.image.title="prometheus-postgres-exporter" \
      org.opencontainers.image.version="0.15.0" \
      org.opencontainers.image.vendor="Prometheus Community" \
      org.opencontainers.image.description="Prometheus exporter for PostgreSQL server metrics" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="4-5" \
      sovereign.hft.cpu-pins-mode="exclusive" \
      sovereign.hft.deploy-strategy="hft-stateful" \
      sovereign.hft.pre-stop-hook="true" \
      sovereign.hft.pre-stop-delay="5s" \
      sovereign.hft.connection-drain="true" \
      sovereign.hft.sched-policy="SCHED_OTHER"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM