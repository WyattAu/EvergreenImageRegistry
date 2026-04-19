# =============================================================================
# SOVEREIGN HARDENED UNBOUND-EXPORTER
# Generated from template - Version: 0.5.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.5.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/prometheus-community/unbound_exporter/releases/download/v0.5.0/unbound_exporter-0.5.0.linux-amd64.tar.gz" -o /unbound_exporter.tar.gz && \
    tar -xzf /unbound_exporter.tar.gz -C / && rm /unbound_exporter.tar.gz && chmod +x /unbound_exporter 2>/dev/null || \
    curl -fsSL "https://github.com/prometheus-community/unbound_exporter/releases/download/v0.5.0/unbound_exporter-0.5.0.linux-amd64.tar.gz" -o /unbound_exporter && chmod +x /unbound_exporter

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/unbound_exporter /var/cache/unbound_exporter

FROM scratch
COPY --from=downloader /unbound_exporter /unbound_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/unbound_exporter /var/log/unbound_exporter
COPY --from=builder /var/cache/unbound_exporter /var/cache/unbound_exporter
USER 65534:65534
WORKDIR /app
EXPOSE 9167
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD unbound_exporter unbound_exporter --version
ENTRYPOINT ["/unbound_exporter"]
LABEL org.opencontainers.image.title="unbound-exporter" \
      org.opencontainers.image.version="0.5.0" \
      org.opencontainers.image.vendor="Prometheus" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
