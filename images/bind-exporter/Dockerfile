# =============================================================================
# SOVEREIGN HARDENED BIND-EXPORTER
# Generated from template - Version: 0.7.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.7.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/prometheus-community/bind_exporter/releases/download/v0.7.0/bind_exporter-0.7.0.linux-amd64.tar.gz" -o /bind_exporter.tar.gz && \
    tar -xzf /bind_exporter.tar.gz -C / && rm /bind_exporter.tar.gz && chmod +x /bind_exporter 2>/dev/null || \
    curl -fsSL "https://github.com/prometheus-community/bind_exporter/releases/download/v0.7.0/bind_exporter-0.7.0.linux-amd64.tar.gz" -o /bind_exporter && chmod +x /bind_exporter

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/bind_exporter /var/cache/bind_exporter

FROM scratch
COPY --from=downloader /bind_exporter /bind_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/bind_exporter /var/log/bind_exporter
COPY --from=builder /var/cache/bind_exporter /var/cache/bind_exporter
USER 65534:65534
WORKDIR /app
EXPOSE 9119
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD bind_exporter bind_exporter --version
ENTRYPOINT ["/bind_exporter"]
LABEL org.opencontainers.image.title="bind-exporter" \
      org.opencontainers.image.version="0.7.0" \
      org.opencontainers.image.vendor="Prometheus" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
