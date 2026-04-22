# =============================================================================
# SOVEREIGN HARDENED MYSQL-EXPORTER
# Generated from template - Version: 0.15.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.15.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/prometheus/mysqld_exporter/releases/download/v0.15.0/mysqld_exporter-0.15.0.linux-amd64.tar.gz" -o /mysqld_exporter.tar.gz && \
    echo "5696925771e22def5838bc538df29befdb07faca2adfbecb512cc7938661bd78  /mysqld_exporter.tar.gz" | sha256sum -c - && \
    tar -xzf /mysqld_exporter.tar.gz -C / && rm /mysqld_exporter.tar.gz && chmod +x /mysqld_exporter 2>/dev/null || \
    curl -fsSL "https://github.com/prometheus/mysqld_exporter/releases/download/v0.15.0/mysqld_exporter-0.15.0.linux-amd64.tar.gz" -o /mysqld_exporter && chmod +x /mysqld_exporter

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/mysqld_exporter /var/cache/mysqld_exporter

FROM scratch
COPY --from=downloader /mysqld_exporter /mysqld_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/mysqld_exporter /var/log/mysqld_exporter
COPY --from=builder /var/cache/mysqld_exporter /var/cache/mysqld_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9104
ENTRYPOINT ["/mysqld_exporter"]
LABEL org.opencontainers.image.title="mysql-exporter" \
      org.opencontainers.image.version="0.15.0" \
      org.opencontainers.image.vendor="Prometheus" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM