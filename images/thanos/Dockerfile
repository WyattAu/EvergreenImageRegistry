# =============================================================================
# SOVEREIGN HARDENED THANOS
# Generated from template - Version: 0.35.0
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=0.35.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends thanos ca-certificates && rm -rf /var/lib/apt/lists/*
# Create non-root user
RUN useradd -m -u 65534 -g '' thanos 2>/dev/null || true
RUN mkdir -p /app /var/log/thanos /var/cache/thanos && chown -R thanos:thanos /app /var/log/thanos /var/cache/thanos 2>/dev/null || true
USER thanos:thanos
WORKDIR /app
EXPOSE 10902
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /-/healthy
ENTRYPOINT ["thanos"]
LABEL org.opencontainers.image.title="thanos" \
      org.opencontainers.image.version="0.35.0" \
      org.opencontainers.image.vendor="Thanos" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
