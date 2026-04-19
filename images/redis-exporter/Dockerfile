# =============================================================================
# SOVEREIGN HARDENED REDIS-EXPORTER
# Generated from template - Version: 1.54.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.54.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/oliver006/redis_exporter/releases/download/v1.54.0/redis_exporter-1.54.0.linux-amd64.tar.gz" -o /redis_exporter.tar.gz && \
    tar -xzf /redis_exporter.tar.gz -C / && rm /redis_exporter.tar.gz && chmod +x /redis_exporter 2>/dev/null || \
    curl -fsSL "https://github.com/oliver006/redis_exporter/releases/download/v1.54.0/redis_exporter-1.54.0.linux-amd64.tar.gz" -o /redis_exporter && chmod +x /redis_exporter

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/redis_exporter /var/cache/redis_exporter

FROM scratch
COPY --from=downloader /redis_exporter /redis_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/redis_exporter /var/log/redis_exporter
COPY --from=builder /var/cache/redis_exporter /var/cache/redis_exporter
USER 65534:65534
WORKDIR /app
EXPOSE 9121
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/redis_exporter", "--version"]
ENTRYPOINT ["/redis_exporter"]
LABEL org.opencontainers.image.title="redis-exporter" \
      org.opencontainers.image.version="1.54.0" \
      org.opencontainers.image.vendor="Prometheus" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
