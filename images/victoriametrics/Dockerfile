# =============================================================================
# SOVEREIGN HARDENED VICTORIAMETRICS
# Generated from template - Version: 1.103.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.103.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/1.103.0/victoria-metrics-linux-amd64-1.103.0.tar.gz" -o /victoria-metrics.tar.gz && \
    tar -xzf /victoria-metrics.tar.gz -C / && rm /victoria-metrics.tar.gz && chmod +x /victoria-metrics 2>/dev/null || \
    curl -fsSL "https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/1.103.0/victoria-metrics-linux-amd64-1.103.0.tar.gz" -o /victoria-metrics && chmod +x /victoria-metrics

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/victoria-metrics /var/cache/victoria-metrics

FROM scratch
COPY --from=downloader /victoria-metrics /victoria-metrics
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/victoria-metrics /var/log/victoria-metrics
COPY --from=builder /var/cache/victoria-metrics /var/cache/victoria-metrics
USER 65534:65534
WORKDIR /app
EXPOSE 8428
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/victoria-metrics", "--version"]
ENTRYPOINT ["/victoria-metrics"]
LABEL org.opencontainers.image.title="victoriametrics" \
      org.opencontainers.image.version="1.103.0" \
      org.opencontainers.image.vendor="VictoriaMetrics" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
