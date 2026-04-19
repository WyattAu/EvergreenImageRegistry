# =============================================================================
# SOVEREIGN HARDENED POSTGRESQL-EXPORTER
# Generated from template - Version: 0.15.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.15.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/prometheus-community/postgres_exporter/releases/download/v0.15.0/postgres_exporter-0.15.0.linux-amd64.tar.gz" -o /postgres_exporter.tar.gz && \
    tar -xzf /postgres_exporter.tar.gz -C / && rm /postgres_exporter.tar.gz && chmod +x /postgres_exporter 2>/dev/null || \
    curl -fsSL "https://github.com/prometheus-community/postgres_exporter/releases/download/v0.15.0/postgres_exporter-0.15.0.linux-amd64.tar.gz" -o /postgres_exporter && chmod +x /postgres_exporter

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/postgres_exporter /var/cache/postgres_exporter

FROM scratch
COPY --from=downloader /postgres_exporter /postgres_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/postgres_exporter /var/log/postgres_exporter
COPY --from=builder /var/cache/postgres_exporter /var/cache/postgres_exporter
USER 65534:65534
WORKDIR /app
EXPOSE 9187
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD postgres_exporter postgres_exporter --version
ENTRYPOINT ["/postgres_exporter"]
LABEL org.opencontainers.image.title="postgresql-exporter" \
      org.opencontainers.image.version="0.15.0" \
      org.opencontainers.image.vendor="Prometheus" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
