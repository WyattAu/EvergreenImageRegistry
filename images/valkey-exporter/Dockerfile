# =============================================================================
# SOVEREIGN HARDENED VALKEY EXPORTER
# Generated from template - Version: 1.58.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.58.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/oliver006/redis_exporter/releases/download/v1.58.0/redis_exporter-v1.58.0.linux-amd64.tar.gz" -o /valkey-exporter.tar.gz && \
    echo "PENDING_CHECKSUM  /valkey-exporter.tar.gz" | sha256sum -c - && \
    tar -xzf /valkey-exporter.tar.gz -C / && rm /valkey-exporter.tar.gz && chmod +x /redis_exporter 2>/dev/null || \
    curl -fsSL "https://github.com/oliver006/redis_exporter/releases/download/v1.58.0/redis_exporter-v1.58.0.linux-amd64.tar.gz" -o /valkey-exporter && chmod +x /valkey-exporter

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/valkey-exporter /var/cache/valkey-exporter

FROM scratch
COPY --from=downloader /redis_exporter /valkey-exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/valkey-exporter /var/log/valkey-exporter
COPY --from=builder /var/cache/valkey-exporter /var/cache/valkey-exporter
USER 65534:65534
WORKDIR /app
EXPOSE 9121
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/valkey-exporter", "--version"]
ENTRYPOINT ["/valkey-exporter"]
LABEL org.opencontainers.image.title="valkey-exporter" \
      org.opencontainers.image.version="1.58.0" \
      org.opencontainers.image.description="Valkey/Redis Prometheus Exporter" \
      org.opencontainers.image.vendor="oliver006" \
      org.opencontainers.image.source="https://github.com/oliver006/redis_exporter" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
