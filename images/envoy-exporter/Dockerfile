# =============================================================================
# SOVEREIGN HARDENED ENVOY-EXPORTER
# Generated from template - Version: 0.4.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.4.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/solo-io/envoy_exporter/releases/download/v0.4.0/envoy_exporter-0.4.0.linux-amd64.tar.gz" -o /envoy_exporter.tar.gz && \
    tar -xzf /envoy_exporter.tar.gz -C / && rm /envoy_exporter.tar.gz && chmod +x /envoy_exporter 2>/dev/null || \
    curl -fsSL "https://github.com/solo-io/envoy_exporter/releases/download/v0.4.0/envoy_exporter-0.4.0.linux-amd64.tar.gz" -o /envoy_exporter && chmod +x /envoy_exporter

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/envoy_exporter /var/cache/envoy_exporter

FROM scratch
COPY --from=downloader /envoy_exporter /envoy_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/envoy_exporter /var/log/envoy_exporter
COPY --from=builder /var/cache/envoy_exporter /var/cache/envoy_exporter
USER 65534:65534
WORKDIR /app
EXPOSE 9102
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD envoy_exporter envoy_exporter --version
ENTRYPOINT ["/envoy_exporter"]
LABEL org.opencontainers.image.title="envoy-exporter" \
      org.opencontainers.image.version="0.4.0" \
      org.opencontainers.image.vendor="Solo.io" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
