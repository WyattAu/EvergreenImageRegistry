# =============================================================================
# SOVEREIGN HARDENED KAFKA-EXPORTER
# Generated from template - Version: 1.9.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.9.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/danielqsj/kafka_exporter/releases/download/v1.9.0/kafka_exporter-1.9.0.linux-amd64.tar.gz" -o /kafka_exporter.tar.gz && \
    echo "c722518ad71c53b3988ea26ae2bd387bb596ce7a98fc639d08bf639a537699a1  /kafka_exporter.tar.gz" | sha256sum -c - && \
    tar -xzf /kafka_exporter.tar.gz -C / && rm /kafka_exporter.tar.gz && chmod +x /kafka_exporter-1.9.0.linux-amd64/kafka_exporter

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/kafka_exporter /var/cache/kafka_exporter

FROM scratch
COPY --from=downloader /kafka_exporter-1.9.0.linux-amd64/kafka_exporter /kafka_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/kafka_exporter /var/log/kafka_exporter
COPY --from=builder /var/cache/kafka_exporter /var/cache/kafka_exporter
USER 65534:65534
WORKDIR /app
EXPOSE 9308
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/kafka_exporter", "--version"]
ENTRYPOINT ["/kafka_exporter"]
LABEL org.opencontainers.image.title="kafka-exporter" \
      org.opencontainers.image.version="1.9.0" \
      org.opencontainers.image.vendor="Prometheus" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
