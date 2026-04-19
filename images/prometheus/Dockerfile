# =============================================================================
# SOVEREIGN HARDENED PROMETHEUS
# Generated from template - Version: 2.53.0
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=2.53.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends prometheus ca-certificates && rm -rf /var/lib/apt/lists/*
# Create non-root user
RUN useradd -m -u 65534 -g '' prometheus 2>/dev/null || true
RUN mkdir -p /app /var/log/prometheus /var/cache/prometheus && chown -R prometheus:prometheus /app /var/log/prometheus /var/cache/prometheus 2>/dev/null || true
USER prometheus:prometheus
WORKDIR /app
EXPOSE 9090
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /-/healthy
ENTRYPOINT ["prometheus"]
LABEL org.opencontainers.image.title="prometheus" \
      org.opencontainers.image.version="2.53.0" \
      org.opencontainers.image.vendor="Prometheus" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
