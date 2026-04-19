# =============================================================================
# SOVEREIGN HARDENED VICTORIAMETRICS
# Generated from template - Version: 1.103.0
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=1.103.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends victoria-metrics ca-certificates && rm -rf /var/lib/apt/lists/*
# Create non-root user
RUN useradd -m -u 65534 -g '' victoria 2>/dev/null || true
RUN mkdir -p /app /var/log/victoriametrics /var/cache/victoriametrics && chown -R victoria:victoria /app /var/log/victoriametrics /var/cache/victoriametrics 2>/dev/null || true
USER victoria:victoria
WORKDIR /app
EXPOSE 8428
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /health
ENTRYPOINT ["victoria-metrics"]
LABEL org.opencontainers.image.title="victoriametrics" \
      org.opencontainers.image.version="1.103.0" \
      org.opencontainers.image.vendor="VictoriaMetrics" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
