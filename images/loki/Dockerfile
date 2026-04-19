# =============================================================================
# SOVEREIGN HARDENED LOKI
# Generated from template - Version: 3.1.0
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=3.1.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends loki ca-certificates && rm -rf /var/lib/apt/lists/*
# Create non-root user
RUN useradd -m -u 65534 -g '' loki 2>/dev/null || true
RUN mkdir -p /app /var/log/loki /var/cache/loki && chown -R loki:loki /app /var/log/loki /var/cache/loki 2>/dev/null || true
USER loki:loki
WORKDIR /app
EXPOSE 3100
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /ready
ENTRYPOINT ["loki"]
LABEL org.opencontainers.image.title="loki" \
      org.opencontainers.image.version="3.1.0" \
      org.opencontainers.image.vendor="Grafana" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
