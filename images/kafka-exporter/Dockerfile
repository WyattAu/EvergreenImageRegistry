# =============================================================================
# SOVEREIGN HARDENED KAFKA-EXPORTER
# Generated from template - Version: 1.7.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.7.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/danielqs/kafka_exporter/releases/download/v1.7.0/kafka_exporter-1.7.0.linux-amd64.tar.gz" -o /kafka_exporter.tar.gz && \
    tar -xzf /kafka_exporter.tar.gz -C / && rm /kafka_exporter.tar.gz && chmod +x /kafka_exporter 2>/dev/null || \
    curl -fsSL "https://github.com/danielqs/kafka_exporter/releases/download/v1.7.0/kafka_exporter-1.7.0.linux-amd64.tar.gz" -o /kafka_exporter && chmod +x /kafka_exporter

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/kafka_exporter /var/cache/kafka_exporter

FROM scratch
COPY --from=downloader /kafka_exporter /kafka_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/kafka_exporter /var/log/kafka_exporter
COPY --from=builder /var/cache/kafka_exporter /var/cache/kafka_exporter
USER 65534:65534
WORKDIR /app
EXPOSE 9308
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD kafka_exporter kafka_exporter --version
ENTRYPOINT ["/kafka_exporter"]
LABEL org.opencontainers.image.title="kafka-exporter" \
      org.opencontainers.image.version="1.7.0" \
      org.opencontainers.image.vendor="Prometheus" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
