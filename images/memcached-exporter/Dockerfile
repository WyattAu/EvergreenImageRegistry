# =============================================================================
# SOVEREIGN HARDENED MEMCACHED-EXPORTER
# Generated from template - Version: 0.13.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.13.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/prometheus/memcached_exporter/releases/download/v0.13.0/memcached_exporter-0.13.0.linux-amd64.tar.gz" -o /memcached_exporter.tar.gz && \
    tar -xzf /memcached_exporter.tar.gz -C / && rm /memcached_exporter.tar.gz && chmod +x /memcached_exporter 2>/dev/null || \
    curl -fsSL "https://github.com/prometheus/memcached_exporter/releases/download/v0.13.0/memcached_exporter-0.13.0.linux-amd64.tar.gz" -o /memcached_exporter && chmod +x /memcached_exporter

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/memcached_exporter /var/cache/memcached_exporter

FROM scratch
COPY --from=downloader /memcached_exporter /memcached_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/memcached_exporter /var/log/memcached_exporter
COPY --from=builder /var/cache/memcached_exporter /var/cache/memcached_exporter
USER 65534:65534
WORKDIR /app
EXPOSE 9150
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/memcached_exporter", "--version"]
ENTRYPOINT ["/memcached_exporter"]
LABEL org.opencontainers.image.title="memcached-exporter" \
      org.opencontainers.image.version="0.13.0" \
      org.opencontainers.image.vendor="Prometheus" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
