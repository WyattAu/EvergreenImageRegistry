# =============================================================================
# SOVEREIGN HARDENED PROMETHEUS-ALERTMANAGER
# Generated from template - Version: 0.27.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.27.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/prometheus/alertmanager/releases/download/v0.27.0/alertmanager-0.27.0.linux-amd64.tar.gz" -o /alertmanager.tar.gz && \
    tar -xzf /alertmanager.tar.gz -C / && rm /alertmanager.tar.gz && chmod +x /alertmanager 2>/dev/null || \
    curl -fsSL "https://github.com/prometheus/alertmanager/releases/download/v0.27.0/alertmanager-0.27.0.linux-amd64.tar.gz" -o /alertmanager && chmod +x /alertmanager

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/alertmanager /var/cache/alertmanager

FROM scratch
COPY --from=downloader /alertmanager /alertmanager
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/alertmanager /var/log/alertmanager
COPY --from=builder /var/cache/alertmanager /var/cache/alertmanager
USER 65534:65534
WORKDIR /app
EXPOSE 9093
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD alertmanager alertmanager --version
ENTRYPOINT ["/alertmanager"]
LABEL org.opencontainers.image.title="prometheus-alertmanager" \
      org.opencontainers.image.version="0.27.0" \
      org.opencontainers.image.vendor="Prometheus" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
