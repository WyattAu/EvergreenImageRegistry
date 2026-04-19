# =============================================================================
# SOVEREIGN HARDENED NGINX-EXPORTER
# Generated from template - Version: 1.1.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.1.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/nginxinc/nginx-prometheus-exporter/releases/download/v1.1.0/nginx-prometheus-exporter_1.1.0_linux_amd64.tar.gz" -o /nginx_exporter.tar.gz && \
    tar -xzf /nginx_exporter.tar.gz -C / && rm /nginx_exporter.tar.gz && chmod +x /nginx_exporter 2>/dev/null || \
    curl -fsSL "https://github.com/nginxinc/nginx-prometheus-exporter/releases/download/v1.1.0/nginx-prometheus-exporter_1.1.0_linux_amd64.tar.gz" -o /nginx_exporter && chmod +x /nginx_exporter

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/nginx_exporter /var/cache/nginx_exporter

FROM scratch
COPY --from=downloader /nginx_exporter /nginx_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/nginx_exporter /var/log/nginx_exporter
COPY --from=builder /var/cache/nginx_exporter /var/cache/nginx_exporter
USER 65534:65534
WORKDIR /app
EXPOSE 9113
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD nginx_exporter nginx_exporter --version
ENTRYPOINT ["/nginx_exporter"]
LABEL org.opencontainers.image.title="nginx-exporter" \
      org.opencontainers.image.version="1.1.0" \
      org.opencontainers.image.vendor="Nginx Inc" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
