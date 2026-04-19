# =============================================================================
# SOVEREIGN HARDENED NODE-EXPORTER
# Generated from template - Version: 1.8.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.8.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/prometheus/node_exporter/releases/download/v1.8.0/node_exporter-1.8.0.linux-amd64.tar.gz" -o /node_exporter.tar.gz && \
    tar -xzf /node_exporter.tar.gz -C / && rm /node_exporter.tar.gz && chmod +x /node_exporter

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/node_exporter /var/cache/node_exporter

FROM scratch
COPY --from=downloader /node_exporter /node_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/node_exporter /var/log/node_exporter
COPY --from=builder /var/cache/node_exporter /var/cache/node_exporter
USER 65534:65534
WORKDIR /app
EXPOSE 9100
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD node_exporter --version 2>/dev/null || exit 1
ENTRYPOINT ["/node_exporter"]
LABEL org.opencontainers.image.title="node-exporter" \
      org.opencontainers.image.version="1.8.0" \
      org.opencontainers.image.vendor="Prometheus" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
