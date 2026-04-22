# =============================================================================
# SOVEREIGN HARDENED RABBITMQ-EXPORTER
# Generated from template - Version: 1.1.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.1.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/kbudde/rabbitmq_exporter/releases/download/v${VERSION}/rabbitmq_exporter-${VERSION}-linux-amd64.tar.gz" \
    -o /rabbitmq_exporter.tar.gz \
    && echo "PENDING  /rabbitmq_exporter.tar.gz" | sha256sum -c - \
    && tar -xzf /rabbitmq_exporter.tar.gz -C / \
    && strip --strip-all /rabbitmq_exporter-${VERSION}-linux-amd64/rabbitmq_exporter \
    && rm /rabbitmq_exporter.tar.gz

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/rabbitmq_exporter /var/cache/rabbitmq_exporter

FROM scratch
COPY --from=downloader /rabbitmq_exporter-${VERSION}-linux-amd64/rabbitmq_exporter /rabbitmq_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/rabbitmq_exporter /var/log/rabbitmq_exporter
COPY --from=builder /var/cache/rabbitmq_exporter /var/cache/rabbitmq_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9090
ENTRYPOINT ["/rabbitmq_exporter"]
LABEL org.opencontainers.image.title="rabbitmq-exporter" \
      org.opencontainers.image.version="1.1.0" \
      org.opencontainers.image.vendor="kbudde" \
      org.opencontainers.image.description="Sovereign hardened RabbitMQ Exporter - Prometheus exporter for RabbitMQ" \
      sovereign.image.tier="1" \
      sovereign.image.category="messaging" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="6-7" \
      sovereign.hft.cpu-pins-mode="shared" \
      sovereign.hft.deploy-strategy="standard-rolling" \
      sovereign.hft.pre-stop-hook="false" \
      sovereign.hft.connection-drain="false" \
      sovereign.hft.sched-policy="SCHED_OTHER"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM